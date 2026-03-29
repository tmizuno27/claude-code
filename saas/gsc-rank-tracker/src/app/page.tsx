import Link from "next/link";

const FEATURES = [
  {
    icon: "📊",
    title: "GSCデータを無期限保存",
    desc: "Googleの16ヶ月制限を突破。過去2年・3年のデータも確認できます。",
  },
  {
    icon: "🔔",
    title: "順位急落アラート",
    desc: "順位が急落したら即メール通知。気づかないペナルティも見逃しません。",
  },
  {
    icon: "💡",
    title: "CTR改善フラグ",
    desc: "「表示回数は多いがクリックが少ない」記事を自動検出。タイトル改善の優先度付けを支援。",
  },
  {
    icon: "🌐",
    title: "複数サイト一元管理",
    desc: "最大10サイトまで1つのダッシュボードで管理。ブログ・ECサイト・企業サイトを横断確認。",
  },
  {
    icon: "📈",
    title: "長期トレンドグラフ",
    desc: "記事別・キーワード別の順位推移を美しいグラフで可視化。改善効果を一目で確認。",
  },
  {
    icon: "⚡",
    title: "設定5分で開始",
    desc: "Googleアカウントで認証するだけ。複雑な設定不要で今日からデータ蓄積開始。",
  },
];

const PLANS = [
  {
    name: "Free",
    price: "$0",
    period: "永久無料",
    description: "個人ブロガーの方に",
    features: [
      "1サイト",
      "3ヶ月分データ保存",
      "日次データ取得",
      "基本ダッシュボード",
    ],
    cta: "無料で始める",
    href: "/signup",
    highlighted: false,
  },
  {
    name: "Starter",
    price: "$9",
    period: "/月",
    description: "複数サイト運営者に",
    features: [
      "3サイト",
      "無期限データ保存",
      "日次データ取得",
      "メールアラート",
      "CTRフラグ機能",
      "CSV エクスポート",
    ],
    cta: "Starterを始める",
    href: "/signup?plan=starter",
    highlighted: true,
  },
  {
    name: "Pro",
    price: "$19",
    period: "/月",
    description: "SEO担当者・フリーランスに",
    features: [
      "10サイト",
      "無期限データ保存",
      "日次データ取得",
      "メール + Slackアラート",
      "CTRフラグ機能",
      "CSV エクスポート",
      "優先サポート",
    ],
    cta: "Proを始める",
    href: "/signup?plan=pro",
    highlighted: false,
  },
  {
    name: "Agency",
    price: "$49",
    period: "/月",
    description: "SEO代理店・大規模運営者に",
    features: [
      "無制限サイト",
      "無期限データ保存",
      "日次データ取得",
      "メール + Slackアラート",
      "CTRフラグ機能",
      "クライアントレポート",
      "API アクセス",
      "専任サポート",
    ],
    cta: "Agencyを始める",
    href: "/signup?plan=agency",
    highlighted: false,
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* ナビゲーション */}
      <nav className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <span className="text-2xl">📊</span>
              <span className="font-bold text-gray-900 text-lg">
                GSC Rank Tracker
                <span className="text-brand-600 ml-1">Pro</span>
              </span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a
                href="#features"
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                機能
              </a>
              <a
                href="#pricing"
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                料金
              </a>
              <Link
                href="/login"
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                ログイン
              </Link>
              <Link
                href="/signup"
                className="inline-flex items-center px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 transition-colors"
              >
                無料で始める
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* ヒーローセクション */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          {/* バッジ */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 text-brand-700 text-sm font-medium mb-8 border border-brand-100">
            <span className="w-2 h-2 rounded-full bg-brand-500 animate-pulse" />
            GSCデータを無期限保存・無料で開始
          </div>

          {/* メインヘッドライン */}
          <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight mb-6 text-balance">
            Google Search Console の
            <br />
            <span className="text-brand-600">16ヶ月制限</span>を突破する
          </h1>

          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            GSCデータを毎日自動取得・無期限保存。順位急落アラート、CTR改善提案、複数サイト管理を
            <strong className="text-gray-900">設定5分</strong>で始められます。
          </p>

          {/* CTA ボタン */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/signup"
              className="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-brand-600 text-white text-lg font-semibold hover:bg-brand-700 transition-all shadow-lg shadow-brand-200 hover:shadow-xl hover:-translate-y-0.5"
            >
              無料で始める（クレジットカード不要）
            </Link>
            <a
              href="#features"
              className="inline-flex items-center justify-center px-8 py-4 rounded-xl border-2 border-gray-200 text-gray-700 text-lg font-semibold hover:border-gray-300 hover:bg-gray-50 transition-all"
            >
              機能を見る →
            </a>
          </div>

          {/* ソーシャルプルーフ */}
          <p className="mt-8 text-sm text-gray-500">
            🎉 クレジットカード不要 · 1サイト永久無料 · いつでもキャンセル可能
          </p>
        </div>

        {/* ダッシュボードモックアップ */}
        <div className="max-w-5xl mx-auto mt-16">
          <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
            <div className="bg-gray-800 px-4 py-3 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500" />
              <span className="w-3 h-3 rounded-full bg-yellow-500" />
              <span className="w-3 h-3 rounded-full bg-green-500" />
              <span className="ml-4 text-gray-400 text-xs">
                app.gsc-rank-tracker.com/dashboard
              </span>
            </div>
            <div className="bg-gray-50 p-8">
              {/* モックダッシュボード */}
              <div className="grid grid-cols-4 gap-4 mb-6">
                {[
                  {
                    label: "平均順位",
                    value: "4.2",
                    change: "↑ 0.8",
                    color: "green",
                  },
                  {
                    label: "総クリック数",
                    value: "12,430",
                    change: "↑ 23%",
                    color: "green",
                  },
                  {
                    label: "表示回数",
                    value: "284,100",
                    change: "↑ 15%",
                    color: "green",
                  },
                  {
                    label: "平均CTR",
                    value: "4.37%",
                    change: "↑ 0.4%",
                    color: "green",
                  },
                ].map((stat) => (
                  <div key={stat.label} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">{stat.label}</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {stat.value}
                    </p>
                    <p className="text-xs text-green-600 mt-1">{stat.change}</p>
                  </div>
                ))}
              </div>
              {/* グラフ模擬 */}
              <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 h-40 flex items-end gap-1 overflow-hidden">
                {Array.from({ length: 30 }, (_, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-brand-200 rounded-t"
                    style={{
                      height: `${30 + Math.sin(i * 0.5) * 20 + Math.random() * 30}%`,
                    }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 課題セクション */}
      <section className="py-20 bg-gray-50 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Google Search Consoleだけでは足りない理由
          </h2>
          <p className="text-gray-600 mb-12">
            無料のGSCは強力なツールですが、本格的なSEO管理には致命的な制限があります
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                problem: "過去16ヶ月分しか見られない",
                solution: "無期限でデータを保存・比較",
              },
              {
                problem: "順位急落に気づくのが遅れる",
                solution: "即時メール/Slackアラート",
              },
              {
                problem: "どの記事を改善すべきかわからない",
                solution: "CTR改善余地を自動フラグ",
              },
              {
                problem: "複数サイトの管理が煩雑",
                solution: "1ダッシュボードで横断管理",
              },
            ].map((item) => (
              <div
                key={item.problem}
                className="flex gap-4 bg-white p-6 rounded-xl border border-gray-200 text-left"
              >
                <div className="shrink-0">
                  <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center text-red-600">
                    ✕
                  </div>
                </div>
                <div>
                  <p className="text-gray-500 line-through text-sm">
                    {item.problem}
                  </p>
                  <p className="text-gray-900 font-medium mt-1 flex items-center gap-2">
                    <span className="text-green-600">✓</span> {item.solution}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 機能セクション */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              SEOを「見える化」するすべての機能
            </h2>
            <p className="text-gray-600">
              GSCデータに特化したシンプルで強力なツールセット
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {FEATURES.map((feature) => (
              <div
                key={feature.title}
                className="p-6 rounded-2xl border border-gray-100 hover:border-brand-200 hover:shadow-md transition-all"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="font-bold text-gray-900 text-lg mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 料金セクション */}
      <section id="pricing" className="py-20 bg-gray-50 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              シンプルな料金プラン
            </h2>
            <p className="text-gray-600">
              Ahrefs（$99/月）・SEMrush（$119/月）の1/10以下の価格で同等のGSC分析を
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {PLANS.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-2xl p-6 ${
                  plan.highlighted
                    ? "bg-brand-600 text-white shadow-xl shadow-brand-200 scale-105"
                    : "bg-white border border-gray-200"
                }`}
              >
                {plan.highlighted && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-amber-400 text-amber-900 text-xs font-bold rounded-full">
                    人気 No.1
                  </div>
                )}
                <h3
                  className={`font-bold text-lg mb-1 ${plan.highlighted ? "text-white" : "text-gray-900"}`}
                >
                  {plan.name}
                </h3>
                <p
                  className={`text-sm mb-4 ${plan.highlighted ? "text-brand-200" : "text-gray-500"}`}
                >
                  {plan.description}
                </p>
                <div className="flex items-baseline gap-1 mb-6">
                  <span
                    className={`text-4xl font-bold ${plan.highlighted ? "text-white" : "text-gray-900"}`}
                  >
                    {plan.price}
                  </span>
                  <span
                    className={`text-sm ${plan.highlighted ? "text-brand-200" : "text-gray-500"}`}
                  >
                    {plan.period}
                  </span>
                </div>
                <ul className="space-y-2 mb-8">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-2 text-sm">
                      <span
                        className={plan.highlighted ? "text-brand-200" : "text-brand-600"}
                      >
                        ✓
                      </span>
                      <span
                        className={plan.highlighted ? "text-white" : "text-gray-700"}
                      >
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>
                <Link
                  href={plan.href}
                  className={`block text-center py-3 px-6 rounded-xl font-semibold text-sm transition-all ${
                    plan.highlighted
                      ? "bg-white text-brand-600 hover:bg-brand-50"
                      : "bg-brand-600 text-white hover:bg-brand-700"
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA セクション */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-brand-600">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            今日からGSCデータの蓄積を開始しよう
          </h2>
          <p className="text-brand-200 text-lg mb-10">
            設定5分、クレジットカード不要。無料プランで今すぐ始めて、
            SEOデータが積み上がる感覚を体験してください。
          </p>
          <Link
            href="/signup"
            className="inline-flex items-center justify-center px-10 py-4 rounded-xl bg-white text-brand-700 text-lg font-bold hover:bg-brand-50 transition-all shadow-lg hover:-translate-y-0.5"
          >
            無料アカウントを作成 →
          </Link>
          <p className="mt-6 text-brand-300 text-sm">
            すでにアカウントをお持ちの方は{" "}
            <Link href="/login" className="underline text-white">
              ログイン
            </Link>
          </p>
        </div>
      </section>

      {/* フッター */}
      <footer className="py-12 bg-gray-900 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xl">📊</span>
              <span className="font-bold text-white">GSC Rank Tracker Pro</span>
            </div>
            <div className="flex gap-6 text-sm text-gray-400">
              <Link href="/privacy" className="hover:text-white transition-colors">
                プライバシーポリシー
              </Link>
              <Link href="/terms" className="hover:text-white transition-colors">
                利用規約
              </Link>
              <a
                href="mailto:support@gsc-rank-tracker.com"
                className="hover:text-white transition-colors"
              >
                お問い合わせ
              </a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
            © 2026 GSC Rank Tracker Pro. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
