import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'サイトについて｜keisan.tools',
  description: 'keisan-tools.comは無料で使えるオンライン計算ツール集です。スマホ対応、登録不要、完全無料でご利用いただけます。',
};

export default function AboutPage() {
  return (
    <div className="container">
      <nav className="breadcrumb">
        <a href="/">ホーム</a>
        <span className="breadcrumb-sep">/</span>
        <span>サイトについて</span>
      </nav>

      <div className="content-section">
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1.5rem' }}>
          keisan.tools について
        </h1>

        <h2>サイトの目的</h2>
        <p>
          keisan.tools は、日常生活やビジネスで必要な計算を手軽にオンラインで行えるツール集です。
          住宅ローン、税金、健康、投資など、幅広いジャンルの計算ツールを無料で提供しています。
        </p>

        <h2>特徴</h2>
        <ul>
          <li>
            <strong>完全無料</strong> ー 全ての計算ツールを無料でご利用いただけます。隠れた課金は一切ありません
          </li>
          <li>
            <strong>登録不要</strong> ー ユーザー登録やログインなしで、すぐに使えます
          </li>
          <li>
            <strong>スマホ対応</strong> ー PC、タブレット、スマートフォンのどれからでも快適にご利用いただけます
          </li>
          <li>
            <strong>わかりやすい解説付き</strong> ー 各ツールには計算の仕組みや関連知識の解説を掲載しています
          </li>
          <li>
            <strong>プライバシー重視</strong> ー 入力データはブラウザ上で処理され、サーバーに送信されません
          </li>
        </ul>

        <h2>カテゴリ一覧</h2>
        <ul>
          <li><a href="/money/">お金・金融</a> ー 住宅ローン、税金、投資、保険、年金など</li>
          <li><a href="/health/">健康</a> ー BMI、基礎代謝、カロリー計算など</li>
          <li><a href="/life/">生活・日常</a> ー 日数計算、単位変換、年齢計算など</li>
          <li><a href="/business/">ビジネス</a> ー 損益分岐点、利益率、ROI計算など</li>
          <li><a href="/math/">数学</a> ー 面積、体積、三角関数、統計など</li>
          <li><a href="/education/">教育</a> ー 学費、偏差値、成績計算など</li>
        </ul>

        <h2>運営について</h2>
        <p>
          keisan.tools は、keisan-tools運営チームが運営しています。
          より便利な計算ツールの提供を目指して、日々改善を続けています。
        </p>
        <p>
          ご意見・ご要望・不具合報告は
          <a href="/contact/">お問い合わせページ</a>よりお気軽にご連絡ください。
        </p>
      </div>
    </div>
  );
}
