"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

export default function NewSitePage() {
  const [domain, setDomain] = useState("");
  const [gscPropertyUrl, setGscPropertyUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const supabase = createClient();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      router.push("/login");
      return;
    }

    // ドメインの正規化
    const normalizedDomain = domain
      .replace(/^https?:\/\//, "")
      .replace(/\/$/, "")
      .toLowerCase();

    const { error: insertError } = await supabase.from("sites").insert({
      user_id: user.id,
      domain: normalizedDomain,
      gsc_property_url: gscPropertyUrl.trim(),
    });

    if (insertError) {
      if (insertError.code === "23505") {
        setError("このGSCプロパティはすでに登録されています");
      } else {
        setError("サイトの追加に失敗しました: " + insertError.message);
      }
      setLoading(false);
      return;
    }

    router.push("/dashboard");
    router.refresh();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4 h-16">
            <Link
              href="/dashboard"
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              ← ダッシュボード
            </Link>
            <span className="text-gray-300">|</span>
            <h1 className="font-bold text-gray-900">サイトを追加</h1>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl border border-gray-200 p-8">
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            監視サイトを追加
          </h2>
          <p className="text-gray-600 text-sm mb-8">
            Google Search ConsoleのプロパティURLを正確に入力してください。
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            <div>
              <label
                htmlFor="domain"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                サイトドメイン
              </label>
              <input
                id="domain"
                type="text"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                required
                placeholder="example.com"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all"
              />
              <p className="mt-1 text-xs text-gray-500">
                例: nambei-oyaji.com（http/https不要）
              </p>
            </div>

            <div>
              <label
                htmlFor="gscPropertyUrl"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                GSCプロパティURL
              </label>
              <input
                id="gscPropertyUrl"
                type="text"
                value={gscPropertyUrl}
                onChange={(e) => setGscPropertyUrl(e.target.value)}
                required
                placeholder="sc-domain:example.com"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all"
              />
              <div className="mt-2 p-3 bg-gray-50 rounded-lg text-xs text-gray-600 space-y-1">
                <p className="font-medium">GSCプロパティURLの確認方法:</p>
                <p>1. Google Search Console を開く</p>
                <p>2. 左上のプロパティ選択ドロップダウンをクリック</p>
                <p>
                  3. プロパティ名をそのままコピー（例:{" "}
                  <code className="bg-gray-200 px-1 rounded">
                    sc-domain:example.com
                  </code>{" "}
                  または{" "}
                  <code className="bg-gray-200 px-1 rounded">
                    https://example.com/
                  </code>
                  ）
                </p>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-6 bg-brand-600 text-white rounded-xl font-semibold hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "追加中..." : "サイトを追加してデータ取得を開始"}
            </button>
          </form>
        </div>

        {/* 補足説明 */}
        <div className="mt-6 p-4 bg-brand-50 border border-brand-100 rounded-xl text-sm text-brand-700">
          <p className="font-medium mb-1">📊 データ取得について</p>
          <p>
            サイト追加後、翌日AM3:00（JST）から日次データの取得が始まります。
            初回は過去90日分のデータを一括取得します。
          </p>
        </div>
      </main>
    </div>
  );
}
