# Product Factory — Phase 2 計画

作成日: 2026-03-28

---

## Phase 1 完了状況

- 完了商品: 16点（Gumroad 13 + RapidAPI 3）
- pipeline.json: キュー空
- 出品済み: Gumroad 13商品（メモリ情報）+ 新商品1出品待ち

## Phase 2 方針

### 方向転換: 「量産」から「既存最適化 + 高単価商品」へ

Phase 1で16商品を生成したが、Gumroad全体の収益は$0に近い状態。
量産を続けても「売れない商品が増えるだけ」になるリスクが高い。

### Phase 2の3本柱

#### 1. 既存商品の改善（最優先）
- Gumroad 13+商品のサムネイル品質向上
- 商品説明のA/Bテスト
- 価格戦略見直し（$9-19 → 一部$0+tip方式で集客）
- SEOタグ・カテゴリの最適化

#### 2. バンドル商品の作成
- 既存商品を組み合わせたバンドル（$39-49）
- 例: "Solopreneur Complete Kit" = AI Toolkit + Finance Dashboard + Launch Checklist
- バンドルの方が単価が高く利益率も良い

#### 3. リード獲得型の無料商品
- 1-2点の無料テンプレートをGumroadで公開
- メールアドレス取得 → メルマガで有料商品に誘導
- 無料商品はSNS拡散されやすい

### pipeline.json 更新案

```json
{
  "queue": [
    {
      "id": "bundle-001",
      "category": "gumroad-notion",
      "name": "Solopreneur Complete Business Kit (Bundle)",
      "price": 49,
      "type": "bundle",
      "includes": ["prompt-006", "gumroad-016", "gumroad-011"]
    },
    {
      "id": "free-001",
      "category": "gumroad-notion",
      "name": "Weekly Planner Template (Free Lead Magnet)",
      "price": 0,
      "type": "lead-magnet"
    },
    {
      "id": "bundle-002",
      "category": "gumroad-notion",
      "name": "Content Creator Toolkit (Bundle)",
      "price": 39,
      "type": "bundle",
      "includes": ["gumroad-018", "prompt-007"]
    }
  ]
}
```

## 次のアクション

1. ☐ 既存Gumroad商品のサムネイルを全てPillow再生成（高品質版）
2. ☐ 上記バンドル2つ + 無料商品1つをpipeline.jsonに追加
3. ☐ 各商品のGumroadページのSEOタグを見直し
4. ☐ X(@prodhq27)で無料商品の告知投稿を予約
