# Property Investment Tracker — Notion Template Design

## データベース一覧（8 DB）

### DB1: Properties（物件）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Property Name | Title | 物件名・住所 |
| Type | Select | Single Family / Multi-Family / Condo / Apartment / Commercial / Short-Term Rental |
| Status | Select | Active / Vacant / Under Renovation / For Sale / Sold |
| Purchase Price | Number ($) | 購入価格 |
| Current Value | Number ($) | 現在の市場価値 |
| Purchase Date | Date | 購入日 |
| Units | Number | 部屋数・ユニット数 |
| Square Footage | Number | 平米・平方フィート |
| Address | Text | 所在地 |
| Mortgages | Relation → Mortgages | 紐付くローン |
| Tenants | Relation → Tenants | 入居者 |
| Transactions | Relation → Transactions | 収支 |
| Maintenance | Relation → Maintenance | 修繕履歴 |
| Documents | Relation → Documents | 関連書類 |
| Equity | Formula | `Current Value - (Mortgages remaining balance sum)` |
| Monthly Cash Flow | Rollup → Transactions | 月次キャッシュフロー |
| Photo | Files & Media | 物件写真 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全物件一覧（Status でソート）
- Board: Status でグループ化
- Board by Type: Type でグループ化
- Gallery: 物件カード表示（写真・キャッシュフロー・ステータス）

### DB2: Transactions（収支）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Description | Title | 取引内容 |
| Property | Relation → Properties | 対象物件 |
| Type | Select | Income / Expense |
| Category | Select | Rent / Airbnb Booking / Security Deposit / Mortgage Payment / Insurance / Property Tax / Repairs / Maintenance / HOA / Utilities / Management Fee / Legal / Other |
| Amount | Number ($) | 金額 |
| Date | Date | 取引日 |
| Tenant | Relation → Tenants | 関連テナント |
| Tax Deductible | Checkbox | 税控除対象 |
| Tax Category | Select | Repairs & Maintenance / Depreciation / Insurance / Management / Taxes / Utilities / Interest / Other |
| Receipt | Files & Media | 領収書 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全取引一覧（Date で降順ソート）
- Board: Category でグループ化
- Calendar: 月別カレンダー表示
- Table - Income Only: Type = Income でフィルタ
- Table - Expenses Only: Type = Expense でフィルタ
- Table - Tax Deductions: Tax Deductible = true でフィルタ
- Board by Property: Property でグループ化

### DB3: Mortgages（ローン）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Loan Name | Title | ローン名（例: "123 Main St - Primary Mortgage"） |
| Property | Relation → Properties | 対象物件 |
| Lender | Text | 金融機関名 |
| Original Amount | Number ($) | 借入額 |
| Remaining Balance | Number ($) | 残高 |
| Interest Rate | Number (%) | 金利 |
| Term (Years) | Number | 返済期間 |
| Monthly Payment | Formula | `(Original Amount * (Interest Rate/100/12)) / (1 - (1 + Interest Rate/100/12)^(-Term*12))` |
| Start Date | Date | 借入開始日 |
| Maturity Date | Date | 満期日 |
| Status | Select | Active / Paid Off / Refinanced |
| Notes | Text | メモ |

**ビュー:**
- Table: 全ローン一覧
- Board: Status でグループ化

### DB4: Tenants（入居者）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Tenant Name | Title | 入居者名 |
| Property | Relation → Properties | 入居物件 |
| Unit | Text | 部屋番号 |
| Email | Email | メールアドレス |
| Phone | Phone | 電話番号 |
| Lease Start | Date | 契約開始日 |
| Lease End | Date | 契約終了日 |
| Monthly Rent | Number ($) | 月額家賃 |
| Security Deposit | Number ($) | 敷金 |
| Status | Select | Active / Notice Given / Moved Out / Evicted |
| Payment History | Relation → Transactions | 支払い履歴 |
| Maintenance Requests | Relation → Maintenance | 修繕依頼 |
| Lease Document | Files & Media | 契約書 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全入居者一覧
- Board: Status でグループ化
- Calendar: Lease End でカレンダー表示（更新期限管理）
- Filtered - Expiring Soon: Lease End が30日以内

### DB5: Maintenance（修繕）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Request Title | Title | 修繕内容 |
| Property | Relation → Properties | 対象物件 |
| Tenant | Relation → Tenants | 依頼テナント |
| Priority | Select | Emergency / High / Medium / Low |
| Status | Select | Reported / In Progress / Waiting for Parts / Completed |
| Reported Date | Date | 報告日 |
| Completed Date | Date | 完了日 |
| Cost | Number ($) | 修繕費用 |
| Expense | Relation → Transactions | 紐付く支出 |
| Contractor | Text | 業者名 |
| Photos | Files & Media | 写真 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全リクエスト一覧
- Board: Status でグループ化（カンバン）
- Board by Priority: Priority でグループ化
- Filtered - Open: Status ≠ Completed

### DB6: Documents（書類）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Document Name | Title | 書類名 |
| Property | Relation → Properties | 対象物件 |
| Type | Select | Lease / Insurance Policy / Inspection Report / Closing Docs / Tax Return / Appraisal / Other |
| File | Files & Media | ファイル |
| Expiry Date | Date | 有効期限 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全書類一覧
- Board: Type でグループ化
- Filtered - Expiring: Expiry Date が60日以内

### DB7: Vacancies（空室）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Unit | Title | ユニット名 |
| Property | Relation → Properties | 物件 |
| Vacant Since | Date | 空室開始日 |
| Days Vacant | Formula | `dateBetween(now(), Vacant Since, "days")` |
| Expected Rent | Number ($) | 想定家賃 |
| Lost Income | Formula | `Days Vacant / 30 * Expected Rent` |
| Status | Select | Listed / Showing / Application Received / Leased |
| Listing URL | URL | 掲載リンク |
| Notes | Text | メモ |

**ビュー:**
- Table: 全空室一覧（Days Vacant で降順ソート）
- Board: Status でグループ化

### DB8: Portfolio KPIs（ポートフォリオ指標）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Metric Name | Title | 指標名 |
| Property | Relation → Properties | 対象物件（空欄 = ポートフォリオ全体） |
| Period | Select | Monthly / Quarterly / Annual |
| Date | Date | 対象期間 |
| Total Income | Number ($) | 総収入 |
| Total Expenses | Number ($) | 総支出 |
| NOI | Formula | `Total Income - Total Expenses` |
| Cap Rate | Formula | `(NOI * 12) / Purchase Price * 100` (年次化) |
| Cash on Cash Return | Formula | `(NOI - Annual Mortgage Payments) / Total Cash Invested * 100` |
| Occupancy Rate | Formula | `Occupied Units / Total Units * 100` |
| Notes | Text | メモ |

**ビュー:**
- Table: 全KPI一覧
- Board: Period でグループ化

## ダッシュボード構成

```
┌─────────────────────────────────────┐
│  🏠 Property Investment Tracker     │
│  "Your Real Estate Command Center"  │
├─────────────────────────────────────┤
│  Portfolio Summary:                  │
│  Total Properties: 5                │
│  Total Value: $1,250,000            │
│  Total Equity: $480,000             │
│  Monthly Cash Flow: +$3,200         │
├──────────────────┬──────────────────┤
│ 📊 Property Cards│ 💰 Monthly P&L  │
│ (Gallery view    │ (Transactions    │
│  from Properties)│  summary view)   │
├──────────────────┼──────────────────┤
│ 🔧 Open Maint.  │ 📅 Lease Expiry  │
│ Requests         │ (Next 90 days)   │
│ (Filtered view)  │ (Calendar view)  │
├──────────────────┼──────────────────┤
│ 🏚️ Vacancies     │ 📈 ROI by       │
│ (Lost income     │ Property         │
│  highlight)      │ (KPI table)      │
├──────────────────┴──────────────────┤
│ Quick Links:                         │
│ [Properties] [Transactions]          │
│ [Tenants] [Maintenance] [Documents]  │
│ [Mortgages] [Vacancies] [KPIs]       │
└─────────────────────────────────────┘
```

## リレーション
- Properties ↔ Transactions: 物件ごとの収支
- Properties ↔ Mortgages: 物件ごとのローン
- Properties ↔ Tenants: 物件ごとの入居者
- Properties ↔ Maintenance: 物件ごとの修繕
- Properties ↔ Documents: 物件ごとの書類
- Properties ↔ Vacancies: 物件ごとの空室
- Properties ↔ Portfolio KPIs: 物件ごとのKPI
- Tenants ↔ Transactions: テナント支払い履歴
- Tenants ↔ Maintenance: テナント修繕依頼
- Maintenance ↔ Transactions: 修繕の支出紐付け

## 主要数式

### Cap Rate (%)
```
(Annual NOI / Current Property Value) × 100
```

### Cash-on-Cash Return (%)
```
(Annual Cash Flow after Debt Service / Total Cash Invested) × 100
```

### NOI (Net Operating Income)
```
Gross Rental Income - Operating Expenses (excluding mortgage)
```

### Monthly Cash Flow
```
Monthly Rental Income - Monthly Expenses - Monthly Mortgage Payment
```

### Equity
```
Current Market Value - Remaining Mortgage Balance
```

### Lost Vacancy Income
```
(Days Vacant / 30) × Expected Monthly Rent
```

## サンプルデータ

### Properties（5件）
1. "123 Oak Street" — Type: Single Family, Status: Active, Purchase: $280,000, Value: $320,000, Units: 1
2. "456 Maple Avenue, Unit A-D" — Type: Multi-Family, Status: Active, Purchase: $520,000, Value: $610,000, Units: 4
3. "789 Beach Blvd #12" — Type: Condo, Status: Active, Purchase: $180,000, Value: $195,000, Units: 1
4. "Sunset Cottage" — Type: Short-Term Rental, Status: Active, Purchase: $150,000, Value: $175,000, Units: 1
5. "1010 Industrial Way" — Type: Commercial, Status: Under Renovation, Purchase: $400,000, Value: $400,000, Units: 2

### Transactions（6件）
1. "March Rent - 123 Oak" — Income, Rent, $1,800, 2026-03-01
2. "March Rent - 456 Maple A" — Income, Rent, $1,200, 2026-03-01
3. "Plumbing repair - 123 Oak" — Expense, Repairs, $450, 2026-03-05
4. "Property Insurance - 789 Beach" — Expense, Insurance, $120, 2026-03-10
5. "Mortgage - 123 Oak" — Expense, Mortgage Payment, $1,350, 2026-03-01
6. "Airbnb Booking #4821" — Income, Airbnb Booking, $280, 2026-03-08

### Tenants（3件）
1. "John Smith" — 123 Oak Street, Lease: 2025-06-01 to 2026-05-31, Rent: $1,800, Status: Active
2. "Maria Garcia" — 456 Maple Ave Unit A, Lease: 2025-09-01 to 2026-08-31, Rent: $1,200, Status: Active
3. "David Chen" — 789 Beach Blvd #12, Lease: 2025-12-01 to 2026-11-30, Rent: $1,500, Status: Active

### Mortgages（3件）
1. "123 Oak St - Primary" — $224,000 original, $198,000 remaining, 4.5%, 30yr, $1,135/mo
2. "456 Maple - Primary" — $416,000 original, $389,000 remaining, 5.2%, 30yr, $2,284/mo
3. "789 Beach - Primary" — $144,000 original, $131,000 remaining, 3.8%, 15yr, $1,054/mo

### Maintenance（2件）
1. "Leaking faucet - kitchen" — 123 Oak, Tenant: John Smith, Priority: Medium, Status: Completed, Cost: $450
2. "HVAC not cooling" — 456 Maple Unit B, Priority: High, Status: In Progress, Cost: TBD
