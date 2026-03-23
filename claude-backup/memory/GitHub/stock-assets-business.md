---
name: stock-assets-business
description: Adobe Stock/Freepik向けストック素材自動生成・販売事業の進捗状況
type: project
---

## Stock Assets事業（ストック素材販売）

AI生成パターン・アイコン・背景をAdobe Stock/Freepikで販売する事業。

**プロジェクトパス**: `claude-code/stock-assets/`

### 現状（2026-03-23）
- プロンプトライブラリ: 630個完成（パターン540 + アイコン40 + 背景50）
- 画像生成済み: 87枚（1024×1024 PNG → 4096×4096 JPEG アップスケール済み）
- メタデータ: Adobe Stock / Freepik用CSV完成
- 生成API: genspark2api（ローカル localhost:7055）、モデル: Recraft v3 / DALL-E 3
- 残り: 543プロンプト未生成

### スクリプト
- `scripts/batch_generate_v2.py` — 画像生成〜アップスケール一括
- `scripts/generate_metadata.py` — メタデータCSV生成
- `scripts/upscale_images.py` — 4096×4096アップスケール

### 次ステップ
1. Adobe Stockアカウント開設 → 87枚テスト出品
2. 承認後、残り543プロンプト順次生成
3. Freepikへ150枚以上で初回一括提出（現在87枚で不足）

**Why:** 完全自動パイプライン確立済み、運用コスト$0のストック収入源
**How to apply:** stock-assets関連の依頼時にこの進捗を前提に提案する
