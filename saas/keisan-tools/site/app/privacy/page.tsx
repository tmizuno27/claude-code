import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'プライバシーポリシー｜keisan.tools',
  description: 'keisan-tools.comのプライバシーポリシー。個人情報の取り扱い、Cookie、Google Analytics、広告についてご説明します。',
};

export default function PrivacyPage() {
  return (
    <div className="container">
      <nav className="breadcrumb">
        <a href="/">ホーム</a>
        <span className="breadcrumb-sep">/</span>
        <span>プライバシーポリシー</span>
      </nav>

      <div className="content-section">
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1.5rem' }}>
          プライバシーポリシー
        </h1>

        <p>
          keisan-tools.com（以下「当サイト」）は、ユーザーの個人情報の保護に努めています。
          本プライバシーポリシーでは、当サイトにおける個人情報の取り扱いについてご説明します。
        </p>

        <h2>1. 個人情報の収集について</h2>
        <p>
          当サイトでは、計算ツールの利用にあたり、ユーザー登録やログインは不要です。
          お問い合わせの際にメールアドレス等の情報をご提供いただく場合がありますが、
          これらの情報はお問い合わせへの回答にのみ使用し、第三者に提供することはありません。
        </p>

        <h2>2. アクセス解析ツールについて</h2>
        <p>
          当サイトでは、Googleによるアクセス解析ツール「Google Analytics」を使用しています。
          Google Analyticsはデータの収集のためにCookieを使用します。
          このデータは匿名で収集されており、個人を特定するものではありません。
        </p>
        <p>
          この機能はCookieを無効にすることで収集を拒否できますので、
          お使いのブラウザの設定をご確認ください。
          Google Analyticsの利用規約については、
          <a href="https://marketingplatform.google.com/about/analytics/terms/jp/" target="_blank" rel="noopener noreferrer">
            Google アナリティクス利用規約
          </a>
          をご覧ください。
        </p>

        <h2>3. 広告について</h2>
        <p>
          当サイトでは、第三者配信の広告サービス「Google AdSense」を利用する場合があります。
          Google AdSenseでは、ユーザーの興味に応じた広告を表示するためにCookieを使用することがあります。
        </p>
        <p>
          Cookieを使用することにより、ユーザーがそのサイトや他のサイトに過去にアクセスした際の情報に基づいて
          広告を配信することが可能になります。
          ユーザーは、
          <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener noreferrer">
            広告設定
          </a>
          でパーソナライズ広告を無効にすることができます。
        </p>

        <h2>4. Cookieについて</h2>
        <p>
          Cookie（クッキー）とは、ウェブサイトがユーザーのブラウザに送信する小さなテキストファイルです。
          当サイトでは以下の目的でCookieを使用しています。
        </p>
        <ul>
          <li>アクセス解析（Google Analytics）</li>
          <li>広告配信の最適化（Google AdSense）</li>
        </ul>
        <p>
          ブラウザの設定によりCookieの受け入れを拒否することが可能ですが、
          一部の機能が正常に動作しない場合があります。
        </p>

        <h2>5. 免責事項</h2>
        <p>
          当サイトに掲載されている計算ツールの結果は参考値であり、正確性を保証するものではありません。
          計算結果に基づく判断はユーザーご自身の責任において行ってください。
        </p>

        <h2>6. プライバシーポリシーの変更</h2>
        <p>
          当サイトは、必要に応じて本プライバシーポリシーを変更することがあります。
          変更後のプライバシーポリシーは、当ページに掲載した時点から効力を生じるものとします。
        </p>

        <h2>7. お問い合わせ</h2>
        <p>
          本ポリシーに関するお問い合わせは、
          <a href="/contact/">お問い合わせページ</a>よりご連絡ください。
        </p>

        <p style={{ marginTop: '2rem', fontSize: '0.8125rem', color: 'var(--gray-400)' }}>
          制定日: 2026年3月24日<br />
          運営者: keisan-tools運営チーム
        </p>
      </div>
    </div>
  );
}
