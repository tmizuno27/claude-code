# Product Factory — アーキテクチャ設計書

## 概要
OpenClawの「Felix」モデルにインスパイアされたAIエージェント駆動のデジタル商品自動量産システム。
Claude Codeエージェントが市場調査→商品制作→出品素材生成を自動実行する。

## 全体アーキテクチャ

```
product-factory（司令官）
  ├── market-researcher  → inputs/pipeline.json に商品企画を追加
  ├── product-builder    → カテゴリ別に商品本体を生成
  ├── listing-publisher  → 出品テキスト・サムネイル・X投稿を生成
  └── nightly-reviewer   → 毎晩23:00 PYT、売上分析→改善→新企画
```

## データフロー

```
[market-researcher]
    │ WebSearchで需要調査
    ▼
pipeline.json（商品キュー）
    │ status: queued → in_progress
    ▼
[product-builder]
    │ カテゴリ別にコード/テンプレート生成
    ▼
outputs/{date}/{slug}/（成果物）
    │
    ▼
[listing-publisher]
    │ 出品テキスト・サムネ・X投稿生成
    ▼
ready-to-publish.json（手動出品チェックリスト）
```

## pipeline.json フォーマット

```json
{
  "queue": [
    {
      "id": "gumroad-011",
      "category": "gumroad-notion",
      "name": "Startup Pitch Deck Planner",
      "price": 14,
      "rationale": "Gumroad上位50にpitch deck系が3件、全て$20+。$14で差別化",
      "target_audience": "スタートアップ創業者、ピッチ準備中の起業家",
      "key_features": ["Pitch structure builder", "Investor tracker", "Funding timeline"],
      "priority": 8,
      "status": "queued",
      "created": "2026-03-20"
    }
  ],
  "completed": []
}
```

### status遷移
- `queued` → `in_progress` → `completed`
- `failed`（制作失敗時）

## 商品カテゴリ別仕様

### gumroad-notion
- **出力物**: listing.md + template-design.md + thumbnail-spec.json + x-posts.json
- **参照テンプレート**: `gumroad-notion/listings/01-freelance-business-os.md`
- **価格帯**: $9-19、バンドル$49
- **言語**: 英語（グローバル市場向け）

### rapidapi
- **出力物**: src/index.js + wrangler.toml + openapi.json + rapidapi-listing.json + package.json
- **参照テンプレート**: `api-services/01-qr-code-api/`
- **料金**: Basic($0/500req) → Pro($5.99/50K) → Ultra($14.99/500K) → Mega($49.99/5M)
- **ホスティング**: Cloudflare Workers（無料枠）

### chrome-ext
- **出力物**: manifest.json + popup.html/css/js + store/description.txt + privacy-policy.html
- **参照テンプレート**: `chrome-extensions/json-formatter/`
- **Manifest V3必須**

### vscode-ext
- **出力物**: package.json + src/extension.ts + tsconfig.json + README.md
- **参照テンプレート**: `vscode-extensions/paste-and-transform/`
- **Publisher**: miccho27

## 自己改善ループ（Phase 3）

### nightly_review.py（毎晩23:00 PYT）
1. **統計収集**: Gumroad API売上、RapidAPI stats、Chrome DL数、VSCode DL数
2. **スコアリング**: 各商品のパフォーマンスを算出
3. **改善指示**: 売上ゼロ商品のリスティング改善案を生成
4. **新企画**: 好調カテゴリで類似商品をpipeline.jsonに自動追加
5. **レポート**: `reports/{date}-review.md` に出力
6. **Healthchecks.io**: ping送信

## 段階的ロールアウト

| Phase | 期間 | 内容 |
|-------|------|------|
| 1 | 1-2日 | 最小構成: エージェント4体 + Gumroadテンプレ1商品自動生成 |
| 2 | 3-5日後 | 量産: 週5商品ペース + RapidAPI着手 + Task Scheduler登録 |
| 3 | 1週間後 | 自己改善: nightly_review + 統計収集 + 自動最適化 |
