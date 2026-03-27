# SIM比較ナビ SEO記事テンプレート v1.0

> **使用方法**: `{{variable}}` 部分を実際の内容に置き換えてください。

---

## メタ情報（フロントマター）

```yaml
---
title: {{main_keyword}}【{{year}}年最新】{{benefit}}
focus_keyword: {{main_keyword}}
meta_description: {{meta_description_120chars}}
category: {{category}}  # kakuyasu-sim / esim / carrier-hikaku / sim-guide
tags: [{{tag1}}, {{tag2}}, {{tag3}}]
article_type: {{article_type}}  # 比較記事 / レビュー記事 / ガイド記事 / キャンペーン記事
affiliate_disclosure: true
---
```

---

## アフィリエイト免責

```
※この記事にはアフィリエイトリンクが含まれています。リンクを経由してお申し込みいただいた場合、当サイトに紹介料が発生しますが、読者の皆様への費用負担は一切ありません。
```

---

# {{main_keyword}}【{{year}}年最新】{{benefit}}

## はじめに（200字以内）

[読者の悩みに共感する1-2文]

この記事では、以下のことがわかります：
- {{learning_point_1}}
- {{learning_point_2}}
- {{learning_point_3}}

## {{h2_comparison_section}}（比較表）

| キャリア | 月額料金 | データ容量 | 通話 | 特徴 |
|---------|---------|-----------|------|------|
| {{carrier_1}} | {{price_1}} | {{data_1}} | {{call_1}} | {{feature_1}} |
| {{carrier_2}} | {{price_2}} | {{data_2}} | {{call_2}} | {{feature_2}} |
| {{carrier_3}} | {{price_3}} | {{data_3}} | {{call_3}} | {{feature_3}} |

## {{h2_detail_section_1}}（400-600字）

### {{h3_subsection_1}}

[本文 — 料金・プラン詳細、メリット・デメリット]

### {{h3_subsection_2}}

[本文 — 実際の使用感、速度テスト結果等]

## {{h2_detail_section_2}}（400-600字）

[本文]

## {{h2_use_case}}（用途別おすすめ）

### データをたくさん使いたい人

[おすすめキャリアと理由]

### とにかく安くしたい人

[おすすめキャリアと理由]

### 通話が多い人

[おすすめキャリアと理由]

## 乗り換え手順（ステップ形式）

1. **MNP予約番号を取得**: {{step_1_detail}}
2. **申し込み**: {{step_2_detail}}
3. **SIM到着・設定**: {{step_3_detail}}
4. **回線切り替え**: {{step_4_detail}}

## よくある質問（FAQ — 構造化データ対応）

```html
<div itemscope itemtype="https://schema.org/FAQPage">
  <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">{{faq_q1}}</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">{{faq_a1}}</p>
    </div>
  </div>
</div>
```

## まとめ

[結論を1-2文で。おすすめキャリアを明示し、申し込みリンクを配置]

---

## ライティングルール

### 必須
- 最新の料金・キャンペーン情報はWebSearchでファクトチェック
- 具体的な数字を必ず含める（「安い」→「月額990円」）
- 比較表を必ず含める（SIM比較サイトの核心）
- 乗り換え手順を含める（読者の行動を促す）
- FAQ構造化データを含める（リッチスニペット獲得）

### 禁止
- AI的表現：「いかがでしたでしょうか」「〜と言えるでしょう」
- 古い料金情報の掲載（必ず最新を確認）
- 根拠のないランキング（料金・速度等の客観データに基づく）

### アフィリエイト
- `config/affiliate-links.json` から取得
- 比較表内 + まとめセクションに自然配置
- 1記事あたり上限5リンク
