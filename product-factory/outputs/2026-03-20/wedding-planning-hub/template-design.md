# Wedding Planning Hub — Notion Template Design

## データベース一覧（7 DB）

### DB1: Guests（ゲスト管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Guest Name | Title | ゲスト名 |
| Side | Select | Bride / Groom / Mutual |
| Group | Select | Family / Friends / Work / Partner's Family / Partner's Friends |
| RSVP Status | Select | Pending / Confirmed / Declined / No Response |
| Plus One | Checkbox | 同伴者あり |
| Plus One Name | Text | 同伴者名 |
| Meal Preference | Select | Standard / Vegetarian / Vegan / Gluten-Free / Halal / Kosher / Other |
| Dietary Notes | Text | アレルギー・特記事項 |
| Table | Relation → Seating | テーブル割り当て |
| Email | Email | 連絡先 |
| Phone | Phone | 電話番号 |
| Address | Text | 住所（招待状送付用） |
| Invite Sent | Checkbox | 招待状送付済み |
| Thank You Sent | Checkbox | お礼状送付済み |
| Notes | Text | メモ |

**ビュー:**
- Table: 全ゲスト一覧（Side→Group でソート）
- Board: RSVP Status でグループ化（カンバン）
- Board by Side: Bride / Groom / Mutual でグループ化
- Gallery: ゲストカード表示
- Filtered — Confirmed: 確定ゲストのみ
- Filtered — No Response: 未回答のみ

### DB2: Budget（予算管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Item | Title | 費目名 |
| Category | Select | Venue / Catering / Photography / Videography / Flowers / Music / Attire / Beauty / Stationery / Transportation / Decorations / Favors / Rings / Honeymoon / Other |
| Estimated Cost | Number ($) | 見積金額 |
| Actual Cost | Number ($) | 実際金額 |
| Difference | Formula | Estimated - Actual |
| Vendor | Relation → Vendors | 担当ベンダー |
| Paid | Checkbox | 支払済み |
| Deposit Paid | Checkbox | デポジット支払済み |
| Due Date | Date | 支払期限 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全費目一覧（Category でソート）
- Board: Category でグループ化
- Summary: Category 別 Estimated vs Actual 比較
- Filtered — Unpaid: 未払いのみ

### DB3: Vendors（ベンダー比較）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Vendor Name | Title | ベンダー名 |
| Category | Select | Venue / Catering / Photography / Videography / Florist / DJ-Band / Officiant / Baker / Hair-Makeup / Planner / Rentals / Other |
| Status | Select | Researching / Contacted / Quote Received / Booked / Rejected |
| Quote | Number ($) | 見積金額 |
| Rating | Select | ★ / ★★ / ★★★ / ★★★★ / ★★★★★ |
| Availability | Select | Available / Unavailable / TBD |
| Website | URL | サイト |
| Contact Name | Text | 担当者名 |
| Phone | Phone | 電話番号 |
| Email | Email | メール |
| Budget Items | Relation → Budget | 関連費目 |
| Pros | Text | 良い点 |
| Cons | Text | 悪い点 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全ベンダー一覧
- Board: Status でグループ化（カンバン）
- Board by Category: Category でグループ化
- Gallery: ベンダーカード表示
- Filtered — Booked: 確定ベンダーのみ

### DB4: Timeline（タイムライン＆チェックリスト）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Task | Title | タスク名 |
| Phase | Select | 12+ Months / 9-11 Months / 6-8 Months / 4-5 Months / 2-3 Months / 1 Month / 2 Weeks / 1 Week / Day Before / Wedding Day / After Wedding |
| Category | Select | Venue / Catering / Attire / Beauty / Stationery / Legal / Music / Photography / Decor / Transportation / Other |
| Status | Select | Not Started / In Progress / Completed / Skipped |
| Priority | Select | High / Medium / Low |
| Due Date | Date | 期限 |
| Vendor | Relation → Vendors | 関連ベンダー |
| Notes | Text | メモ |
| Completed | Checkbox | 完了チェック |

**ビュー:**
- Table: 全タスク（Phase でソート）
- Board: Status でグループ化（カンバン）
- Board by Phase: Phase でグループ化
- Calendar: Due Date でカレンダー表示
- Timeline: Due Date でタイムライン表示
- Filtered — This Month: 今月のタスクのみ
- Filtered — Overdue: 期限超過のみ

### DB5: Seating（席次表）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Table Name | Title | テーブル名（例: Table 1, Head Table） |
| Capacity | Number | 席数 |
| Guests | Relation → Guests | 着席ゲスト |
| Guest Count | Rollup | Guests の件数 |
| Available Seats | Formula | Capacity - Guest Count |
| Location | Select | Front / Middle / Back / Outdoor / Bar Area |
| Notes | Text | メモ（例: 近くに配置したいグループ等） |

**ビュー:**
- Table: 全テーブル一覧
- Board: Location でグループ化
- Gallery: テーブルカード（ゲスト名表示）

### DB6: Registry（ギフトレジストリ）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Item | Title | 商品名 |
| Registry | Select | Amazon / Target / Zola / Crate & Barrel / Custom / Other |
| Price | Number ($) | 金額 |
| Status | Select | Listed / Purchased / Received |
| Purchased By | Text | 購入者名 |
| Thank You Sent | Checkbox | お礼状送付済み |
| URL | URL | 商品リンク |
| Notes | Text | メモ |

**ビュー:**
- Table: 全アイテム一覧
- Board: Status でグループ化
- Board by Registry: Registry でグループ化
- Filtered — Need Thank You: Received かつ Thank You Sent = false

### DB7: Inspiration（インスピレーション）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Title | Title | タイトル |
| Category | Select | Venue / Flowers / Dress / Cake / Decor / Color Palette / Hair / Table Setting / Invitation / Other |
| Image URL | URL | 画像リンク |
| Source | URL | 参照元 |
| Notes | Text | メモ |
| Favorite | Checkbox | お気に入り |

**ビュー:**
- Gallery: カード表示（画像メイン）
- Board: Category でグループ化

## ダッシュボード構成

```
┌─────────────────────────────────────┐
│  💒 Wedding Planning Hub            │
│  "[Partner A] & [Partner B]"        │
│  "Wedding Date: [Date]"            │
├─────────────────────────────────────┤
│  RSVP Summary:                      │
│  ✅ Confirmed: 82  ⏳ Pending: 34   │
│  ❌ Declined: 8   📨 Total: 124    │
├──────────────────┬──────────────────┤
│ 📋 Upcoming Tasks│ 💰 Budget        │
│ (This Month)     │ Estimated: $25K  │
│ (Filtered view)  │ Spent: $12K      │
│                  │ Remaining: $13K  │
├──────────────────┼──────────────────┤
│ 🏪 Vendors       │ 🪑 Seating       │
│ Booked: 8/12     │ Assigned: 82/120 │
│ Pending: 4       │ Tables: 12       │
├──────────────────┴──────────────────┤
│ Quick Links:                         │
│ [Guests] [Budget] [Vendors]          │
│ [Timeline] [Seating] [Registry]      │
│ [Inspiration]                        │
└─────────────────────────────────────┘
```

## リレーション
- Guests ↔ Seating: ゲストがどのテーブルに着席するか
- Budget ↔ Vendors: 費目がどのベンダーに紐づくか
- Timeline ↔ Vendors: タスクがどのベンダーに関連するか

## サンプルデータ

### Guests（5件）
1. "Sarah Johnson" — Side: Bride, Group: Family, RSVP: Confirmed, Meal: Standard, Table: Head Table
2. "Mike & Lisa Chen" — Side: Groom, Group: Friends, RSVP: Confirmed, Meal: Vegetarian, Plus One: yes, Table: Table 3
3. "David Williams" — Side: Bride, Group: Work, RSVP: Pending, Meal: TBD
4. "Grandma Rose" — Side: Bride, Group: Family, RSVP: Confirmed, Meal: Gluten-Free, Table: Table 1
5. "Tom & Amy Park" — Side: Mutual, Group: Friends, RSVP: No Response, Plus One: yes

### Budget（5件）
1. "Venue rental" — Venue, Estimated: $5,000, Actual: $4,800, Paid: yes
2. "Photographer" — Photography, Estimated: $3,000, Actual: $2,800, Deposit Paid: yes
3. "Catering (per head)" — Catering, Estimated: $8,000, Actual: $0, Paid: no
4. "Wedding dress" — Attire, Estimated: $2,000, Actual: $1,850, Paid: yes
5. "DJ / Band" — Music, Estimated: $1,500, Actual: $0, Deposit Paid: no

### Vendors（4件）
1. "Rosewood Garden Estate" — Venue, Status: Booked, Quote: $4,800, Rating: ★★★★★
2. "Capture Moments Photography" — Photography, Status: Booked, Quote: $2,800, Rating: ★★★★
3. "Fresh Blooms Floristry" — Florist, Status: Quote Received, Quote: $1,200, Rating: ★★★★
4. "DJ Smooth" — DJ-Band, Status: Researching, Quote: $800, Rating: ★★★

### Timeline（5件）
1. "Book venue" — Phase: 12+ Months, Category: Venue, Status: Completed, Priority: High
2. "Send save-the-dates" — Phase: 6-8 Months, Category: Stationery, Status: Completed, Priority: High
3. "Final dress fitting" — Phase: 1 Month, Category: Attire, Status: Not Started, Priority: High
4. "Confirm final headcount with caterer" — Phase: 2 Weeks, Category: Catering, Status: Not Started, Priority: High
5. "Send invitations" — Phase: 4-5 Months, Category: Stationery, Status: In Progress, Priority: High

### Seating（3件）
1. "Head Table" — Capacity: 8, Location: Front, Guests: 4 assigned
2. "Table 1" — Capacity: 10, Location: Front, Guests: 6 assigned
3. "Table 3" — Capacity: 10, Location: Middle, Guests: 4 assigned
