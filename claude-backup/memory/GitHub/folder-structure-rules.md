---
name: フォルダ構成ルール
description: GitHub/claude-code/ のディレクトリ構成ルールと整理規約（2026-03-28整理済み）
type: project
---

## 2026-03-28 フォルダ整理完了

### ログの一元管理ルール
全てのログ・レポートは `claude-code/logs/` に集約する。`products/logs/` や `sites/logs/` は使わない。

**logs/ サブディレクトリ構成:**
| ディレクトリ | 内容 |
|-------------|------|
| `seo/` | SEO PDCAレポート、インデックス、内部リンク、stale content |
| `pdca/` | 全事業PDCAレポート、日次完了レポート、アクションプラン |
| `api/` | RapidAPI、Gumroad、Dev.to等プロダクト関連ログ |
| `affiliate/` | アフィリエイト監査ログ |
| `infrastructure/` | 自動同期、タスクヘルスチェック、デプロイ |
| `misc/` | X投稿、はてな、その他 |

### ファイル配置ルール
- **一時ファイルをGitHub/ルートに放置しない** → 適切なディレクトリに即移動
- **RapidAPI関連スクリプト** → `products/api-services/scripts/`
- **汎用ユーティリティ** → `infrastructure/tools/`
- **日付付きアクションプラン/レポート** → `logs/pdca/`（docs/ではない）
- **docs/** はプロジェクト横断の永続ドキュメント専用

### 整理で移動したファイル
- `tmp_crosssell.py` → `products/api-services/scripts/crosssell.py`
- `tmp_listings.py` → `products/api-services/scripts/listings.py`
- `tmp_update_listings.py` → `products/api-services/scripts/update_listings.py`
- `wp_post.py` → `infrastructure/tools/wp_post.py`
- `logs/indexing-api-sim-runner.py` → `sites/sim-hikaku.online/scripts/`

**Why:** ファイル散乱で作業効率低下、Claude Codeが構造を把握しにくくなる
**How to apply:** 新しいファイル生成時は必ず適切なディレクトリに配置。ルートやlogs/にスクリプトを置かない
