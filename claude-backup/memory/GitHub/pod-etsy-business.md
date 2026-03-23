---
name: POD Printful×Etsy事業 (AsuInk)
description: Print-on-Demand事業。50デザイン×3商品=150リスティング。Etsy/Printfulアカウント開設待ち
type: project
---

ストア名「AsuInk」でPrintful×EtsyのPOD事業を立ち上げ（2026-03-16構築）

**Why:** 在庫ゼロ・発送自動・運用コスト$0の完全自動収入源。

**How to apply:** `claude-code/products/pod-etsy/` 配下に全ファイル格納。

## 商品構成
- 5ニッチ × 10デザイン = 50デザイン
- 各デザイン × 3商品（Tシャツ$24.99、マグ$17.99、ポスター$19.99）= 150リスティング
- ニッチ: 日本禅、南米、日西バイリンガル、デジタルノマド、名言哲学

## ステータス（2026-03-16）
- Geminiプロンプト50本: 完成（`designs/prompts/`）
- Etsyリスティング150本: 完成（`listings/`）
- Pinterest/X マーケティング: 完成（`marketing/`）
- セットアップガイド: 完成（`setup/launch-checklist.md`）
- 自動化スクリプト3本: 完成（`scripts/`）
  - `generate_designs.py` → `resize_for_printful.py` → `upload_to_printful.py`

## ブロッカー
- **Gemini画像生成**: 無料プランでは画像生成API不可。有料プランまたは代替（DALL-E、Midjourney等）が必要
- **Etsy/Printfulアカウント**: 未開設

## 次のステップ
1. Etsy/Printfulアカウント開設・連携
2. 画像生成手段の確保（Gemini有料 or 代替）
3. デザイン50個生成 → リサイズ → Printfulアップロード
4. Etsyリスティング150本公開

## 収益目標
月$200〜$1,000（6ヶ月後）、初期費用$10
