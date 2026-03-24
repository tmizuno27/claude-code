import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'お問い合わせ｜keisan.tools',
  description: 'keisan-tools.comへのお問い合わせページ。ご質問・ご要望・不具合報告などお気軽にご連絡ください。',
};

export default function ContactPage() {
  return (
    <div className="container">
      <nav className="breadcrumb">
        <a href="/">ホーム</a>
        <span className="breadcrumb-sep">/</span>
        <span>お問い合わせ</span>
      </nav>

      <div className="content-section">
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1.5rem' }}>
          お問い合わせ
        </h1>

        <p>
          当サイトに関するご質問、ご要望、不具合の報告など、お気軽にご連絡ください。
        </p>

        <h2>メールでのお問い合わせ</h2>
        <p>以下のメールアドレス宛にお送りください。</p>

        <div style={{
          background: 'var(--gray-50)',
          border: '1px solid var(--gray-200)',
          borderRadius: 'var(--radius)',
          padding: '1.5rem',
          textAlign: 'center',
          margin: '1.5rem 0',
        }}>
          <a
            href="mailto:t.mizuno27@gmail.com?subject=keisan-tools.comへのお問い合わせ"
            style={{
              display: 'inline-block',
              padding: '0.875rem 2rem',
              background: 'var(--primary)',
              color: '#fff',
              borderRadius: 'var(--radius)',
              fontWeight: 700,
              fontSize: '1rem',
              textDecoration: 'none',
            }}
          >
            メールで問い合わせる
          </a>
          <p style={{ marginTop: '0.75rem', fontSize: '0.8125rem', color: 'var(--gray-500)' }}>
            t.mizuno27@gmail.com
          </p>
        </div>

        <h2>お問い合わせの際のお願い</h2>
        <ul>
          <li>件名に「keisan-tools.com」と記載いただけるとスムーズです</li>
          <li>不具合報告の場合は、ご利用のブラウザ・端末情報をお知らせください</li>
          <li>返信までに数日お時間をいただく場合があります</li>
        </ul>

        <h2>よくあるご質問</h2>

        <h3>Q. 計算結果は正確ですか？</h3>
        <p>
          当サイトの計算結果はあくまで参考値です。
          重要な判断（税金、ローン等）には必ず専門家にご相談ください。
        </p>

        <h3>Q. 新しい計算ツールのリクエストはできますか？</h3>
        <p>
          はい、上記メールアドレスまでお気軽にリクエストをお送りください。
          可能な限り対応いたします。
        </p>

        <h3>Q. 利用料金はかかりますか？</h3>
        <p>
          全ての計算ツールは完全無料でご利用いただけます。
          登録やログインも不要です。
        </p>
      </div>
    </div>
  );
}
