-- GSC Rank Tracker Pro - 初期スキーマ
-- 実行方法: Supabase Dashboard > SQL Editor に貼り付けて実行

-- ==========================================
-- ENUM 型
-- ==========================================
CREATE TYPE plan_type AS ENUM ('free', 'starter', 'pro', 'agency');
CREATE TYPE alert_type AS ENUM ('position_drop', 'ctr_low', 'impressions_spike');

-- ==========================================
-- ユーザー管理テーブル
-- auth.users と連携（Supabase Auth）
-- ==========================================
CREATE TABLE public.users (
  id          uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email       text NOT NULL,
  plan        plan_type NOT NULL DEFAULT 'free',
  stripe_customer_id  text,
  gsc_access_token    text,   -- 暗号化推奨（本番ではVault使用）
  gsc_refresh_token   text,   -- 暗号化推奨
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);

-- ==========================================
-- サイト管理テーブル
-- ==========================================
CREATE TABLE public.sites (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          uuid NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  domain           text NOT NULL,
  gsc_property_url text NOT NULL,  -- 例: "sc-domain:example.com" または "https://example.com/"
  is_active        boolean NOT NULL DEFAULT true,
  last_synced_at   timestamptz,
  created_at       timestamptz NOT NULL DEFAULT now(),
  UNIQUE(user_id, gsc_property_url)
);

-- ==========================================
-- キーワード管理テーブル（重要KWのトラッキング）
-- ==========================================
CREATE TABLE public.keywords (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id     uuid NOT NULL REFERENCES public.sites(id) ON DELETE CASCADE,
  query       text NOT NULL,
  is_tracked  boolean NOT NULL DEFAULT true,
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE(site_id, query)
);

-- ==========================================
-- 順位データテーブル（メインテーブル・大容量）
-- ==========================================
CREATE TABLE public.rankings (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id     uuid NOT NULL REFERENCES public.sites(id) ON DELETE CASCADE,
  date        date NOT NULL,
  page_url    text NOT NULL,
  query       text NOT NULL,
  position    numeric(6,2) NOT NULL,
  impressions integer NOT NULL DEFAULT 0,
  clicks      integer NOT NULL DEFAULT 0,
  ctr         numeric(6,4) NOT NULL DEFAULT 0,  -- 0.0000 〜 1.0000
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE(site_id, date, page_url, query)
);

-- クエリ最適化インデックス
CREATE INDEX idx_rankings_site_date     ON public.rankings (site_id, date DESC);
CREATE INDEX idx_rankings_site_page     ON public.rankings (site_id, page_url);
CREATE INDEX idx_rankings_site_query    ON public.rankings (site_id, query);
CREATE INDEX idx_rankings_date          ON public.rankings (date DESC);

-- ==========================================
-- アラートルールテーブル
-- ==========================================
CREATE TABLE public.alerts (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id                 uuid NOT NULL REFERENCES public.sites(id) ON DELETE CASCADE,
  alert_type              alert_type NOT NULL,
  threshold               numeric NOT NULL,
  -- 例: {"email": true, "slack_webhook": "https://hooks.slack.com/..."}
  notification_channels   jsonb NOT NULL DEFAULT '{"email": true}'::jsonb,
  is_active               boolean NOT NULL DEFAULT true,
  created_at              timestamptz NOT NULL DEFAULT now()
);

-- ==========================================
-- アラート発火履歴テーブル
-- ==========================================
CREATE TABLE public.alert_logs (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  alert_id      uuid NOT NULL REFERENCES public.alerts(id) ON DELETE CASCADE,
  triggered_at  timestamptz NOT NULL DEFAULT now(),
  -- 例: {"query": "パラグアイ 移住", "page_url": "...", "prev_position": 3, "curr_position": 15}
  payload       jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_alert_logs_alert_id ON public.alert_logs (alert_id, triggered_at DESC);

-- ==========================================
-- Row Level Security (RLS) 設定
-- ==========================================
ALTER TABLE public.users     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sites     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.keywords  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rankings  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alerts    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alert_logs ENABLE ROW LEVEL SECURITY;

-- users: 自分のレコードのみ参照・更新可
CREATE POLICY "users_select_own"  ON public.users FOR SELECT  USING (auth.uid() = id);
CREATE POLICY "users_update_own"  ON public.users FOR UPDATE  USING (auth.uid() = id);
CREATE POLICY "users_insert_own"  ON public.users FOR INSERT  WITH CHECK (auth.uid() = id);

-- sites: 自分のサイトのみ操作可
CREATE POLICY "sites_select_own"  ON public.sites FOR SELECT  USING (auth.uid() = user_id);
CREATE POLICY "sites_insert_own"  ON public.sites FOR INSERT  WITH CHECK (auth.uid() = user_id);
CREATE POLICY "sites_update_own"  ON public.sites FOR UPDATE  USING (auth.uid() = user_id);
CREATE POLICY "sites_delete_own"  ON public.sites FOR DELETE  USING (auth.uid() = user_id);

-- keywords: サイトの所有者のみ操作可
CREATE POLICY "keywords_select_own" ON public.keywords FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));
CREATE POLICY "keywords_insert_own" ON public.keywords FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));
CREATE POLICY "keywords_delete_own" ON public.keywords FOR DELETE
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));

-- rankings: サイトの所有者のみ参照可（INSERT/UPDATEはService Roleのみ）
CREATE POLICY "rankings_select_own" ON public.rankings FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));

-- alerts: サイトの所有者のみ操作可
CREATE POLICY "alerts_select_own" ON public.alerts FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));
CREATE POLICY "alerts_insert_own" ON public.alerts FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));
CREATE POLICY "alerts_update_own" ON public.alerts FOR UPDATE
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));
CREATE POLICY "alerts_delete_own" ON public.alerts FOR DELETE
  USING (EXISTS (SELECT 1 FROM public.sites WHERE id = site_id AND user_id = auth.uid()));

-- alert_logs: アラートの所有者のみ参照可
CREATE POLICY "alert_logs_select_own" ON public.alert_logs FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM public.alerts a
    JOIN public.sites s ON s.id = a.site_id
    WHERE a.id = alert_id AND s.user_id = auth.uid()
  ));

-- ==========================================
-- ユーザー作成トリガー（auth.users → public.users）
-- ==========================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (new.id, new.email);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ==========================================
-- updated_at 自動更新トリガー
-- ==========================================
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_users_updated_at
  BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ==========================================
-- プラン別サイト数制限ビュー（参考）
-- ==========================================
-- free: 1サイト | starter: 3サイト | pro: 10サイト | agency: 無制限
COMMENT ON TABLE public.users    IS 'GSC Rank Tracker Pro ユーザー';
COMMENT ON TABLE public.sites    IS '監視対象サイト（GSCプロパティと1:1対応）';
COMMENT ON TABLE public.keywords IS 'サイトごとの重要キーワード';
COMMENT ON TABLE public.rankings IS 'GSCから取得した日次順位データ（メインテーブル）';
COMMENT ON TABLE public.alerts   IS '順位急落・CTR低下などのアラートルール';
COMMENT ON TABLE public.alert_logs IS 'アラート発火履歴';
