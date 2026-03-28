# docs/ - プロジェクト横断ドキュメント

このディレクトリには、プロジェクト全体に関わるドキュメントを配置する。

## 配置ルール

| 種類 | 配置先 | 例 |
|------|--------|------|
| 事業計画・戦略 | `docs/` | 年間計画、ロードマップ |
| サイト固有ルール | `sites/{site}/CLAUDE.md` | 記事テンプレ、SEOルール |
| 日次/週次レポート | `logs/pdca/` | daily-completion-report |
| SEOレポート | `logs/seo/` | seo-pdca-report |
| API/プロダクトログ | `logs/api/` | rapidapi-stats |
| インフラログ | `logs/infrastructure/` | auto-sync, task-healthcheck |
| アクションプラン（日付付き） | `logs/pdca/` | improvement-action-plan |

## 関連

- 全体ハブ: `/CLAUDE.md`（GitHub/直下）
- メモリ: `~/.claude/projects/.../memory/MEMORY.md`
- エージェント定義: `.claude/agents/`
- コマンド定義: `.claude/commands/`
