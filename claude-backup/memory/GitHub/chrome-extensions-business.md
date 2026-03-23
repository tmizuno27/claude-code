---
name: Chrome拡張ポートフォリオ事業
description: Chrome Web Storeに10個の拡張を出品。Rick Blyth方式のポートフォリオ戦略で放置型収益を目指す
type: project
---

Chrome拡張ポートフォリオ事業を2026-03-16に開始。10個の拡張を開発しChrome Web Storeに審査申請。
2026-03-23時点: 1本公開済み（AI Text Rewriter）、8本審査待ち。
Regex Testerは「スパムとストア掲載順位」ポリシー違反で却下→削除予定（キーワード詰め込みが原因）。
Color Picker & Converterは`activeTab`未使用で却下→修正して再提出済み。
Quick Currency Converterは「機能しない」で却下（APIエンドポイントURL誤り）→修正して2026-03-20再提出済み。

**Why:** RapidAPI 20本と同じ「マーケットプレイスに出して放置」モデルの横展開。開発コスト$0、運用コスト$0。

**How to apply:** 審査結果を確認し、通過後はさらに量産 or フリーミアム課金（Stripe連携）を検討。

## 出品一覧（全10個、2026-03-16申請）

| # | 拡張名 | アクセント色 | API使用 |
|---|--------|-----------|---------|
| 1 | SEO Inspector | 青紫 | 自社Workers API |
| 2 | JSON Formatter Pro | 青 | なし（ローカル） |
| 3 | Quick Currency Converter | 緑 | exchangerate API |
| 4 | Domain WHOIS Lookup | 紫 | WHOIS API |
| 5 | AI Text Rewriter | オレンジ | OpenAI API（BYOK） |
| 6 | Color Picker & Converter | レインボー | なし（ローカル） |
| 7 | Page Speed Checker | 緑 | Google PSI API |
| 8 | Hash & Encode Tool | シアン | なし（ローカル） |
| 9 | Lorem Ipsum Generator | ピンク | なし（ローカル） |
| 10 | Regex Tester | 紫 | なし（ローカル） |

## インフラ
- デベロッパーアカウント: t.mizuno27（登録料$5）
- プライバシーポリシー: 各拡張ごとにCloudflare Workersでホスティング
- プロジェクトパス: `claude-code/chrome-extensions/`
- 全拡張: Apple風ダークUI、Manifest V3
