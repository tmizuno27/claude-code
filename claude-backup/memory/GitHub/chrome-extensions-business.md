---
name: Chrome拡張ポートフォリオ事業
description: Chrome拡張11本（公開2+審査待ち9）。全PPurl設定済み(homepage-three-ochre.vercel.app)。Tab Manager CWS提出準備完了。
type: project
---

## 2026-03-29更新
- **合計11本**（公開2: AI Text Rewriter + Regex Tester、審査中8本、Tab Manager: 提出準備完了）
- **Tab Manager**: アイコン生成+ZIP作成+store素材整備→CWS提出可能状態
- **プライバシーポリシーURL**: 全11本 `https://homepage-three-ochre.vercel.app/privacy-policy-{ext}.html` に統一済み（GitHub Pages無効化のためVercelに移行）
- **ストア説明文SEO強化**: Regex Tester（大幅改善）、Lorem Ipsum Generator（強化）、AI Text Rewriter（BYOK訴求強化）
- **フリーミアム実装済み**: AI Text Rewriter（10回/日制限）、Regex Tester（Gumroad）、Tab Manager（3セッション制限）

## 2026-03-28更新
- **合計11本**（新規Tab Manager追加）
- AI Text Rewriter: scripting権限バグ修正（v1.2.0）→ CWS再アップロード必要
- JSON Formatter Pro: 不要権限削除+host_permissions明示
- プライバシーポリシー: https://keisan-tools.com/chrome-privacy/ で公開中
- Tab Manager & Session Saver: 開発完了（アイコン追加→CWS提出待ち）

Chrome拡張ポートフォリオ事業を2026-03-16に開始。10個の拡張を開発しChrome Web Storeに審査申請。
2026-03-24時点: 4本公開済み（AI Text Rewriter 1user, Color Picker 0, Domain WHOIS 1user, SEO Inspector 0）、4本審査待ち（Quick Currency, JSON Formatter, Lorem Ipsum, Page Speed）。
Regex Testerは「スパムとストア掲載順位」ポリシー違反で却下→取り下げ済み。
Hash & Encode Toolは「不正確な説明 - 機能しない」で却下（2026-03-24）。右クリックコンテキストメニュー機能が審査で動作確認できず。→ storageパーミッション追加+background.js修正+再提出済み（2026-03-24）、審査待ち。
Quick Currency Converterは再提出済み（2026-03-20）、審査待ち。

## プライバシーポリシーURL設定（2026-03-27）
7/8拡張のプライバシーポリシーURLをGitHub Pages経由で設定完了:
- https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-{ext}.html
- Hash & Encode Toolは審査中のため編集不可、審査通過後に設定予定

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
- プライバシーポリシー: Vercel（https://homepage-three-ochre.vercel.app/privacy-policy-{ext}.html）※GitHub Pages無効化済み
- プロジェクトパス: `claude-code/products/chrome-extensions/`
- 全拡張: Apple風ダークUI、Manifest V3

## Tab Manager CWS提出手順（提出準備完了）
1. CWSダッシュボード: https://chrome.google.com/webstore/devconsole
2. 新規アイテム → ZIPアップロード: `tab-manager/store/extension.zip`
3. Short description: `tab-manager/store/short-description.txt`
4. Detailed description: `tab-manager/store/description.txt`
5. Screenshots: `tab-manager/store-assets/screenshot-1280x800.png`
6. Promo tile: `tab-manager/store-assets/promo-440x280.png`
7. Privacy policy URL: `https://homepage-three-ochre.vercel.app/privacy-policy-tab-manager.html`
