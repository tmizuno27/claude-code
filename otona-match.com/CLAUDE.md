# CLAUDE.md — otona-match.com

## プロジェクト概要

**サイト名**: 大人のマッチングナビ
**ドメイン**: otona-match.com
**コンセプト**: 30代・40代のための出会い系・マッチングアプリ徹底比較ガイド
**テーマ**: Cocoon（Apple風CSSカスタマイズ適用済み）
**WordPress認証**: Basic認証（`config/secrets.json`参照）

## カテゴリ構成

| slug | 名前 | WP ID |
|------|------|-------|
| matching-apps | マッチングアプリ | 2 |
| deaikei | 出会い系サイト | 3 |
| konkatsu | 婚活 | 4 |
| renai-technique | 恋愛テクニック | 5 |
| safety | 安全・トラブル対策 | 6 |
| reviews | 体験談・口コミ | 7 |

## 現在の記事（20本・全て公開済み）

### マッチングアプリ（5本）
- ID:9 matching-app-ranking-2026（ランキングTOP10）
- ID:10 pairs-review（ペアーズレビュー）
- ID:11 with-review（ウィズレビュー）
- ID:12 matching-app-first-date-guide（初デートガイド）
- ID:13 matching-app-price-comparison（料金比較）

### 出会い系サイト（3本）
- ID:14 deaikei-vs-matching-app（出会い系vs.マッチングアプリ）
- ID:15 happy-mail-review（ハッピーメール）
- ID:16 pcmax-review（PCMAX）

### 婚活（3本）
- ID:17 konkatsu-app-osusume（婚活アプリおすすめ）
- ID:18 kekkon-soudan-vs-app（結婚相談所vs.アプリ）
- ID:19 konkatsu-30dai（30代からの婚活）

### 恋愛テクニック（5本）
- ID:20 profile-photo-tips（プロフィール写真）
- ID:21 matching-app-no-reply（返信が来ない問題）
- ID:22 first-date-manual（初デートマニュアル）
- ID:23 sakura-gyosha-miwakekata（サクラ・業者の見分け方）
- ID:24 matching-app-mibare-taisaku（身バレ対策）

### 安全・トラブル対策（2本）
- ID:25 anzen-checklist（安全チェックリスト）

### 体験談・口コミ（2本）
- ID:26 matching-app-kekkon-taikendan（結婚した人のストーリー）
- ID:27 40dai-50dai-taikendan（40代・50代の体験談）
- ID:28 matching-app-yamedoki（やめどき）

## ディレクトリ構成

```
otona-match.com/
├── CLAUDE.md              ← このファイル
├── config/                ← 設定ファイル
│   ├── settings.json
│   ├── secrets.json       ← 認証情報（.gitignore対象）
│   └── affiliate-links.json
├── docs/                  ← 事業計画書
├── images/                ← 画像
├── inputs/                ← KWキュー
├── outputs/               ← 生成記事・管理CSV
├── published/             ← 投稿ログ
├── scripts/               ← 自動化スクリプト
│   ├── content/           ← 記事生成
│   ├── publishing/        ← WordPress投稿
│   ├── analytics/         ← 分析
│   ├── social/            ← SNS
│   ├── media/             ← 画像
│   └── maintenance/       ← メンテナンス
├── templates/             ← 記事テンプレート
└── theme/                 ← CSS/JS
    ├── css/
    └── assets/js/
```

## ライティングルール

### 文体
- 客観的・信頼感のある比較メディアの文体
- 男女両方が読者対象（偏らない表現）
- 具体的な料金・数字を必ず明記
- 「実際に使った」体験談風の記述を含める

### 禁止事項
- AI的な表現：「いかがでしたでしょうか」「〜と言えるでしょう」
- 特定のアプリを過度に推す（公平な比較を維持）
- 性的・過激な表現
- 根拠のない断定（「絶対に出会える」等）

### SEOルール
- タイトルにメインKWを含める（左寄せ）
- H2-H4の見出し階層を正しく使う
- 比較表・ランキングを積極的に使用
- 内部リンクを記事間で張り巡らせる

### アフィリエイト
- `config/affiliate-links.json` から取得
- 1記事あたり上限5リンク
- 免責文を記事末尾に配置
- 高単価案件（結婚相談所 > マッチングアプリ > 出会い系）を優先

## 技術スタック

- **CMS**: WordPress on ConoHa WING + Cocoon + Rank Math SEO
- **スクリプト**: Python 3.13
- **API**: WordPress REST API（Basic認証）
- **デザイン**: Apple風CSS（frosted glassヘッダー、カード型UI）
