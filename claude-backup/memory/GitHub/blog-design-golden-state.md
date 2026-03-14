---
name: ブログデザイン・ゴールデンステート（2026-03-14確定版）
description: nambei-oyaji.comの理想デザイン確定版。復元用リファレンス＆新サイト作成時のテンプレート。ユーザーが「過去最高」と評価した状態
type: reference
---

# nambei-oyaji.com デザイン確定版（2026-03-14）

ユーザーが「PC版・スマホ版ともに過去最高」と評価した状態。
**復元が必要な場合、または新サイト作成時のフォーマットとして使用する。**

## サイト構成

- **CMS**: WordPress + Cocoon テーマ
- **デザイン手法**: Cocoonのデフォルトを全てCSSオーバーライド（Apple風デザイン）
- **グローバルCSS/JS**: Widget `custom_html-2`（sidebar: content-top）に全て格納
- **トップページ**: 固定ページ ID:47（カスタムHTML）
- **お問い合わせ**: 固定ページ ID:1890（formsubmit.co使用）

## カラーシステム（Apple準拠）

| 用途 | カラーコード |
|------|------------|
| メインテキスト | #1d1d1f |
| サブテキスト | #86868b |
| リンク/アクセント | #06c (#0066CC) |
| ボーダー | #e5e5e7 |
| 薄い背景 | #f5f5f7 |
| フッター背景 | #1d1d1f |
| マーカー（黄） | #fff9c4 |
| マーカー（ピンク） | #fce4ec |
| マーカー（青） | #e3f2fd |

## フォントスタック

```css
font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
```

## ヘッダー（全ページ共通）

- **レイアウト**: ロゴ左 + ナビ右（flexbox）
- **スタイル**: sticky, frosted glass（backdrop-filter: blur(20px)）, z-index: 9999
- **背景**: rgba(255,255,255,0.92)
- **ナビ項目**: パラグアイ生活 / 移住準備・お金 / 海外で稼ぐ / 子育て・教育 / プロフィール / お問い合わせ
- **ナビリンク**: /category/paraguay/ / /category/ijuu-junbi/ / /category/side-business/ / /category/kids/ / /about/ / /contact/
- **モバイル**: ナビ非表示（768px以下）
- **実装場所**: Widget custom_html-2 内のJS（DOMContentLoaded でheader-inを書き換え）

## フッター

- 背景: #1d1d1f
- テキスト: #86868b
- リンク: #d2d2d7

## トップページ構成（ID:47）

1. **Hero**: 家族イラスト + グラデーションテキスト + CTAボタン2つ
2. **6つのカテゴリーで発信中**: 6カードグリッド（3列×2行、タブレット2列、モバイル横並び）
   - 各カード: アイコン + カテゴリー名 + 説明文
   - パラグアイは丸型国旗画像（hatscripts circle-flags SVG）
3. **Value Props**: 3カード（一次情報/働き方/数字）
4. **Stats**: 実績数字
5. **About**: ダーク背景 + アバター + プロフィール
6. **CTA**: X フォローボタン
- **アニメーション**: IntersectionObserver + `.nao-anim` → `.nao-visible`（fade-up）
- **非表示**: SNSボタン, TOC, 記事ヘッダー, Cocoonデフォルトフッター, サイドバー

## 記事ページ

- **レイアウト**: メイン + サイドバー（336px）
- **本文**: 16px, line-height 2.4
- **H2**: 26px, 中央揃え, ボーダーなし
- **H3**: 20px, 左揃え
- **サイドバー**: Apple風カード（プロフィール/検索/カテゴリ/新着/目次）
  - border-radius: 16px, border: 1px solid #e5e5e7
  - 目次: sticky (top: 80px)
- **視覚的強調**: 太字+カラーマーカー（黄=結論/数字、ピンク=注意、青=メリット）
- **非表示**: SNSボタン, Cocoon目次（独自目次使用）, details要素

## 6カテゴリー

| カテゴリー | スラッグ | WP ID | アイコン |
|-----------|---------|-------|---------|
| パラグアイ生活 | paraguay | 3 | 🇵🇾 (circle-flags SVG) |
| 移住準備・お金 | ijuu-junbi | 10 | 💰 |
| 海外で稼ぐ | side-business | 4 | 💻 |
| 子育て・教育 | kids | 13 | 👧 |
| 起業・ビジネス | business | 14 | 🏢 |
| 健康・医療 | health | 15 | 🩺 |

## モバイル対応ブレークポイント

- **768px以下**: ヘッダーナビ非表示
- **834px以下**: アーカイブ2カラム→1カラム
- **734px以下**: 6カテゴリーカード横並び（アイコン左+テキスト右）、1列
- **600px以下**: 各種フォントサイズ縮小

## 復元に必要なファイル

1. **Widget CSS/JS**: `blog/temp_widget.txt`（custom_html-2の全内容）
2. **トップページHTML**: WordPress ID:47のcontent
3. **記事CSS**: `blog/theme/css/single-article.css`（Apple風記事デザイン）
4. **グローバルCSS**: `blog/theme/css/nao-global.css`
5. **ホームページテンプレ**: `blog/theme/homepage.html`

## 新サイト作成時の再利用ポイント

- カラーシステム（Apple準拠の6色）
- ヘッダー（frosted glass + sticky）
- サイドバーカードデザイン（border-radius:16px）
- IntersectionObserver アニメーション
- レスポンシブブレークポイント（768/834/734/600）
- フォントスタック
- 視覚的強調ルール（3色マーカー）
