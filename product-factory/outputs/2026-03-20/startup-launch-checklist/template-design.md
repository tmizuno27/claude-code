# Startup Launch Checklist — Notion Template Design

## データベース一覧（6 DB）

### DB1: Tasks（タスク）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Task Name | Title | タスク名 |
| Phase | Select | Idea Validation / MVP Build / Pre-Launch / Launch Day |
| Category | Select | Legal / Finance / Marketing / Product / Operations |
| Status | Select | Not Started / In Progress / Completed / Blocked |
| Priority | Select | High / Medium / Low |
| Due Date | Date | 期限 |
| Milestone | Relation → Milestones | 紐付くマイルストーン |
| Resources | Relation → Resources | 参考リソース |
| Notes | Text | メモ・詳細 |
| Completed | Checkbox | 完了チェック |

**ビュー:**
- Table: 全タスク一覧（Phase→Category でソート）
- Board: Status でグループ化（カンバン）
- Board by Phase: Phase でグループ化
- Calendar: Due Date でカレンダー表示
- Gallery: Category 別カード表示
- Filtered: Blocked タスクのみ

### DB2: Milestones（マイルストーン）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Milestone Name | Title | マイルストーン名 |
| Phase | Select | Idea Validation / MVP Build / Pre-Launch / Launch Day |
| Target Date | Date | 目標日 |
| Status | Select | Upcoming / In Progress / Completed |
| Tasks | Relation → Tasks | 紐付くタスク |
| Progress | Formula | 完了タスク数/全タスク数 (%) |

**ビュー:**
- Timeline: Target Date でタイムライン表示
- Table: 全マイルストーン一覧
- Board: Phase でグループ化

### DB3: Budget（予算）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Item | Title | 費目名 |
| Category | Select | Legal / Software / Marketing / Operations / Other |
| Type | Select | One-time / Monthly / Annual |
| Amount | Number ($) | 金額 |
| Paid | Checkbox | 支払済み |
| Due Date | Date | 支払予定日 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全費目一覧
- Board: Category でグループ化
- Summary: Type でグループ化（月額/一回/年額の合計が一目でわかる）

### DB4: Resources（リソース）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Resource Name | Title | リソース名 |
| Type | Select | Article / Tool / Video / Template / Book |
| URL | URL | リンク |
| Category | Select | Legal / Finance / Marketing / Product / Operations |
| Tasks | Relation → Tasks | 関連タスク |
| Rating | Select | ⭐ / ⭐⭐ / ⭐⭐⭐ |
| Notes | Text | メモ |

**ビュー:**
- Table: 全リソース一覧
- Board: Type でグループ化
- Gallery: カード表示

### DB5: Competitors（競合分析）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Company Name | Title | 競合名 |
| Website | URL | サイトURL |
| Pricing | Text | 料金体系 |
| Key Features | Multi-select | 主要機能 |
| Strengths | Text | 強み |
| Weaknesses | Text | 弱み |
| Our Differentiator | Text | 差別化ポイント |

**ビュー:**
- Table: 競合一覧
- Gallery: カード比較

### DB6: Launch Day Playbook（ローンチ当日）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Action | Title | アクション名 |
| Time | Text | 実行時刻（例: 9:00 AM） |
| Channel | Select | Twitter / Email / Reddit / Product Hunt / LinkedIn / Other |
| Content | Text | 投稿文・メール文 |
| Status | Select | Prepared / Posted / Skipped |
| Link | URL | 投稿先リンク |

**ビュー:**
- Table: 時系列順
- Board: Channel でグループ化

## ダッシュボード構成

```
┌─────────────────────────────────────┐
│  🚀 Startup Launch Checklist        │
│  "From Idea to Launch Day"          │
├─────────────────────────────────────┤
│  Phase Progress:                     │
│  [████████░░] Idea Validation ✓      │
│  [████░░░░░░] MVP Build ●            │
│  [░░░░░░░░░░] Pre-Launch ○           │
│  [░░░░░░░░░░] Launch Day ○           │
├──────────────────┬──────────────────┤
│ 📋 Today's Tasks │ ⏰ Upcoming      │
│ (Filtered view)  │ Milestones       │
│                  │ (Timeline)       │
├──────────────────┼──────────────────┤
│ 💰 Budget Summary│ 🚧 Blocked Tasks │
│ (Summary view)   │ (Filtered view)  │
├──────────────────┴──────────────────┤
│ Quick Links:                         │
│ [Tasks] [Milestones] [Budget]        │
│ [Resources] [Competitors] [Launch]   │
└─────────────────────────────────────┘
```

## リレーション
- Tasks ↔ Milestones: タスクがどのマイルストーンに属するか
- Tasks ↔ Resources: タスクに関連するリソース

## サンプルデータ

### Tasks（5件）
1. "Register business entity" — Phase: Idea Validation, Category: Legal, Status: Completed, Priority: High
2. "Build landing page" — Phase: MVP Build, Category: Marketing, Status: In Progress, Priority: High
3. "Set up Stripe payments" — Phase: MVP Build, Category: Product, Status: Not Started, Priority: Medium
4. "Create social media accounts" — Phase: Pre-Launch, Category: Marketing, Status: Not Started, Priority: Low
5. "Write launch email sequence" — Phase: Pre-Launch, Category: Marketing, Status: Not Started, Priority: Medium

### Milestones（4件）
1. "Idea Validated" — Phase: Idea Validation, Target: Week 2
2. "MVP Ready" — Phase: MVP Build, Target: Week 6
3. "Pre-Launch Complete" — Phase: Pre-Launch, Target: Week 8
4. "Launch Day" — Phase: Launch Day, Target: Week 10

### Budget（4件）
1. "Domain name" — Software, One-time, $12
2. "Hosting (Vercel)" — Software, Monthly, $0
3. "LLC registration" — Legal, One-time, $200
4. "Google Ads test" — Marketing, One-time, $100
