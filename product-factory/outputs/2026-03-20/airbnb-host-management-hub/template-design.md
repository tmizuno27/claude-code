# Airbnb Host Management Hub — Notion Template Design

## データベース一覧（7 DB）

### DB1: Listings（物件・リスティング）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Listing Name | Title | 物件名（例: "Sunny Downtown Loft"） |
| Platform | Multi-Select | Airbnb / VRBO / Booking.com / Direct |
| Status | Select | Active / Paused / Under Maintenance / Deactivated |
| Property Type | Select | Entire Home / Private Room / Shared Room / Unique Stay |
| Location | Text | 住所・エリア |
| Bedrooms | Number | 寝室数 |
| Bathrooms | Number | バスルーム数 |
| Max Guests | Number | 最大収容人数 |
| Base Nightly Rate | Number ($) | 基本1泊料金 |
| Cleaning Fee | Number ($) | クリーニング料金 |
| Listing URL | URL | プラットフォームのリスティングURL |
| Bookings | Relation → Bookings | 予約履歴 |
| Cleanings | Relation → Cleanings | 清掃履歴 |
| Transactions | Relation → Transactions | 収支 |
| Maintenance | Relation → Maintenance | メンテナンス |
| Supplies | Relation → Supplies | 備品 |
| Occupancy Rate | Formula | `(Booked Nights / Total Available Nights) * 100` |
| Photo | Files & Media | 物件写真 |
| WiFi Password | Text | WiFiパスワード |
| Check-in Instructions | Text | チェックイン手順 |
| House Rules | Text | ハウスルール |
| Notes | Text | メモ |

**ビュー:**
- Table: 全リスティング一覧（Status でソート）
- Board: Status でグループ化
- Gallery: 物件カード表示（写真・Occupancy Rate・Base Rate）
- Board by Platform: Platform でグループ化

### DB2: Bookings（予約・ゲスト管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Guest Name | Title | ゲスト名 |
| Listing | Relation → Listings | 対象物件 |
| Platform | Select | Airbnb / VRBO / Booking.com / Direct |
| Check-in | Date | チェックイン日 |
| Check-out | Date | チェックアウト日 |
| Nights | Formula | `dateBetween(Check-out, Check-in, "days")` |
| Guests | Number | ゲスト人数 |
| Nightly Rate | Number ($) | 実際の1泊料金 |
| Total Payout | Number ($) | プラットフォーム支払い額（手数料差引後） |
| Status | Select | Confirmed / Checked In / Checked Out / Cancelled / No-Show |
| Communication Stage | Select | Pre-Arrival / Welcome Sent / Mid-Stay / Checkout Sent / Review Requested / Complete |
| Guest Email | Email | ゲストメール |
| Guest Phone | Phone | ゲスト電話 |
| Special Requests | Text | 特別リクエスト |
| Rating Given | Select | 5 Stars / 4 Stars / 3 Stars / 2 Stars / 1 Star / Not Yet |
| Review Written | Checkbox | レビュー回答済み |
| Cleaning | Relation → Cleanings | 紐付く清掃 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全予約一覧（Check-in で降順ソート）
- Calendar: チェックイン/チェックアウトカレンダー
- Board: Status でグループ化
- Board by Communication: Communication Stage でグループ化
- Filtered - Upcoming: Check-in が今日以降、Status = Confirmed
- Filtered - Needs Review Response: Review Written = false, Status = Checked Out
- Board by Listing: Listing でグループ化

### DB3: Cleanings（清掃管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Cleaning Task | Title | タスク名（例: "Turnover - Sunny Loft - Mar 20"） |
| Listing | Relation → Listings | 対象物件 |
| Booking | Relation → Bookings | 紐付く予約（チェックアウト後の清掃） |
| Cleaner | Select | Cleaner A / Cleaner B / Cleaner C / Self |
| Date | Date | 清掃日 |
| Time Slot | Select | Morning (8-11am) / Afternoon (12-3pm) / Evening (4-7pm) |
| Status | Select | Scheduled / In Progress / Completed / Issue Reported |
| Type | Select | Turnover / Deep Clean / Mid-Stay / Inspection |
| Checklist Completed | Checkbox | チェックリスト完了 |
| Cost | Number ($) | 清掃費用 |
| Supply Notes | Text | 補充が必要な備品 |
| Photos | Files & Media | 清掃完了写真 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全清掃一覧（Date でソート）
- Calendar: 清掃カレンダー
- Board: Status でグループ化（カンバン）
- Board by Cleaner: Cleaner でグループ化
- Filtered - Today: Date = today
- Filtered - Upcoming 7 Days: Date が7日以内

### DB4: Transactions（収支管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Description | Title | 取引内容 |
| Listing | Relation → Listings | 対象物件 |
| Type | Select | Income / Expense |
| Category | Select | Booking Payout / Cleaning Fee Collected / Direct Payment / Cleaning Cost / Maintenance / Supplies / Platform Fee / Insurance / Utilities / Mortgage / Property Tax / Furnishing / Marketing / Other |
| Amount | Number ($) | 金額 |
| Date | Date | 取引日 |
| Booking | Relation → Bookings | 紐付く予約 |
| Tax Deductible | Checkbox | 税控除対象 |
| Receipt | Files & Media | 領収書 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全取引一覧（Date で降順ソート）
- Board: Category でグループ化
- Calendar: 月別カレンダー
- Table - Income Only: Type = Income でフィルタ
- Table - Expenses Only: Type = Expense でフィルタ
- Board by Listing: Listing でグループ化（物件別P&L）
- Table - Tax Deductions: Tax Deductible = true でフィルタ

### DB5: Maintenance（メンテナンス・問題管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Issue Title | Title | 問題内容 |
| Listing | Relation → Listings | 対象物件 |
| Reported By | Select | Guest / Cleaner / Self / Neighbor |
| Priority | Select | Emergency / High / Medium / Low |
| Status | Select | Reported / Scheduled / In Progress / Waiting for Parts / Completed |
| Reported Date | Date | 報告日 |
| Resolved Date | Date | 解決日 |
| Cost | Number ($) | 修理費用 |
| Expense | Relation → Transactions | 紐付く支出 |
| Contractor | Text | 業者名・連絡先 |
| Photos | Files & Media | 写真 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全件一覧
- Board: Status でグループ化（カンバン）
- Board by Priority: Priority でグループ化
- Filtered - Open Issues: Status ≠ Completed

### DB6: Supplies（備品在庫管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Item Name | Title | 備品名 |
| Listing | Relation → Listings | 対象物件 |
| Category | Select | Toiletries / Linens / Kitchen / Cleaning Products / Welcome Kit / Electronics / Furniture / Other |
| Current Stock | Number | 現在の在庫数 |
| Reorder Threshold | Number | 発注ライン |
| Needs Reorder | Formula | `if(Current Stock <= Reorder Threshold, "Yes", "No")` |
| Unit Cost | Number ($) | 単価 |
| Supplier | Text | 仕入先 |
| Purchase URL | URL | 購入リンク |
| Last Restocked | Date | 最終補充日 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全備品一覧
- Board: Category でグループ化
- Filtered - Needs Reorder: Needs Reorder = "Yes"
- Board by Listing: Listing でグループ化

### DB7: Pricing Calendar（料金戦略プランナー）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Period Name | Title | 期間名（例: "Summer Peak", "Christmas Week"） |
| Listing | Relation → Listings | 対象物件 |
| Season | Select | Peak / High / Mid / Low / Holiday / Event |
| Start Date | Date | 開始日 |
| End Date | Date | 終了日 |
| Nightly Rate | Number ($) | 設定料金 |
| Minimum Stay | Number | 最低宿泊数 |
| Competitor Rate | Number ($) | 競合の料金 |
| Rate Difference | Formula | `Nightly Rate - Competitor Rate` |
| Occupancy Target | Number (%) | 目標稼働率 |
| Notes | Text | メモ |

**ビュー:**
- Table: 全期間一覧（Start Date でソート）
- Calendar: 料金カレンダー
- Board: Season でグループ化
- Board by Listing: Listing でグループ化

## ダッシュボード構成

```
┌─────────────────────────────────────┐
│  🏡 Airbnb Host Management Hub     │
│  "Your Short-Term Rental HQ"       │
├─────────────────────────────────────┤
│  Portfolio Snapshot:                 │
│  Active Listings: 4                │
│  This Month Revenue: $8,420        │
│  Avg Occupancy: 78%                │
│  Upcoming Check-ins: 6             │
├──────────────────┬──────────────────┤
│ 📊 Listing Cards │ 📅 Booking      │
│ (Gallery view    │ Calendar         │
│  from Listings)  │ (Calendar view)  │
├──────────────────┼──────────────────┤
│ 🧹 Today's       │ 💬 Needs Reply  │
│ Cleanings        │ (Guests needing  │
│ (Filtered view)  │  review response)│
├──────────────────┼──────────────────┤
│ 💰 Monthly P&L   │ 🔧 Open Issues  │
│ by Property      │ (Maintenance     │
│ (Board view)     │  kanban)         │
├──────────────────┼──────────────────┤
│ 📦 Low Stock     │ 💲 Pricing      │
│ Alerts           │ Calendar         │
│ (Filtered view)  │ (Calendar view)  │
├──────────────────┴──────────────────┤
│ Quick Links:                         │
│ [Listings] [Bookings] [Cleanings]   │
│ [Revenue] [Maintenance] [Supplies]  │
│ [Pricing Calendar]                   │
└─────────────────────────────────────┘
```

## Guest Communication Templates（ページ内テンプレート）

ダッシュボードに「Guest Communication Templates」セクションとして以下をToggle Headingで配置:

### 1. Booking Confirmation
> Hi [Guest Name]! Thanks for booking [Listing Name]. We're excited to host you from [Check-in] to [Check-out]. I'll send detailed check-in instructions 2 days before your arrival. In the meantime, let me know if you have any questions!

### 2. Check-in Instructions (2 Days Before)
> Hi [Guest Name]! Your stay is almost here. Here's everything you need:
> - **Address:** [Address]
> - **Check-in time:** [Time]
> - **Lockbox/Smart Lock code:** [Code]
> - **WiFi:** [Network] / Password: [Password]
> - **Parking:** [Instructions]
> - **House manual:** [Link/location]
> Let me know if you need anything before arrival!

### 3. Welcome Message (Check-in Day)
> Welcome, [Guest Name]! I hope you arrived safely. Everything should be ready for you. A few quick tips:
> - Thermostat is set to [temp] — feel free to adjust
> - Extra towels/blankets are in [location]
> - Trash/recycling goes out on [day]
> Enjoy your stay! I'm just a message away if you need anything.

### 4. Mid-Stay Check-in (Day 2-3 of Longer Stays)
> Hi [Guest Name]! Just checking in — is everything going well? Do you need anything? Happy to help with local restaurant recommendations or activity suggestions. Enjoy the rest of your stay!

### 5. Checkout Reminder (Day Before)
> Hi [Guest Name]! Just a friendly reminder that checkout is tomorrow at [Time]. Before you go:
> - Please start the dishwasher if you used dishes
> - Leave used towels in the bathtub
> - Lock the door behind you (it auto-locks / use code [code])
> Thank you for being a wonderful guest! If you enjoyed your stay, I'd truly appreciate a review. Safe travels!

### 6. Review Request (1-2 Days After Checkout)
> Hi [Guest Name]! Thanks again for staying at [Listing Name]. I hope you had a great time! If you have a moment, I'd really appreciate a review — it helps future guests and means a lot to me as a host. Thanks and hope to host you again!

## Review Response Templates（ページ内テンプレート）

ダッシュボードに「Review Response Templates」セクションとして配置:

### 5-Star Responses (5 templates)
1. "Thank you so much, [Guest]! You were an absolute dream guest. The place was spotless when you left. You're welcome back anytime!"
2. "What a kind review, [Guest]! We loved hosting you and hope to see you again on your next visit to [City]."
3. "[Guest], thank you for the wonderful words! Guests like you are what make hosting so rewarding. Our door is always open."
4. "So glad you enjoyed your stay, [Guest]! We're always working to make the experience even better. Come back soon!"
5. "Thank you, [Guest]! It was a pleasure having you. We hope [City] treated you well — until next time!"

### 4-Star Responses (5 templates)
1. "Thanks for the great review, [Guest]! We appreciate the feedback and are always looking for ways to improve. Hope to host you again!"
2. "Thank you, [Guest]! We're glad you enjoyed most of your stay. If there's anything we could do better, we'd love to hear — we're always improving."
3. "[Guest], thanks for staying with us! Your feedback helps us grow. We've noted your suggestions and look forward to welcoming you back."
4. "Appreciate the honest review, [Guest]! We take all feedback seriously and are making improvements. Hope to exceed your expectations next time."
5. "Thank you for the kind words, [Guest]! We're committed to making every stay a 5-star experience. See you next time!"

### Negative Review Recovery (5 templates)
1. "Thank you for your feedback, [Guest]. I'm sorry your experience didn't meet expectations. I've [specific action taken] to prevent this in the future. I'd love the chance to make it right if you visit again."
2. "[Guest], I appreciate you sharing your experience. This isn't the standard we aim for, and I take full responsibility. We've since [specific fix]. I hope you'll give us another chance."
3. "Thank you for your honesty, [Guest]. I've personally addressed [issue] and made changes to ensure future guests have a better experience. Your feedback genuinely helps me improve."
4. "[Guest], I'm sorry to hear about [issue]. I reached out privately to address this but want to publicly acknowledge it here too. We've implemented [fix] and are committed to doing better."
5. "I appreciate you taking the time to share this, [Guest]. Your concerns are valid and I've already [action]. I hold myself to a high standard and your feedback is helping me get there."

## リレーション
- Listings ↔ Bookings: 物件ごとの予約
- Listings ↔ Cleanings: 物件ごとの清掃
- Listings ↔ Transactions: 物件ごとの収支
- Listings ↔ Maintenance: 物件ごとのメンテナンス
- Listings ↔ Supplies: 物件ごとの備品
- Listings ↔ Pricing Calendar: 物件ごとの料金設定
- Bookings ↔ Cleanings: 予約に紐付く清掃（チェックアウト後ターンオーバー）
- Bookings ↔ Transactions: 予約に紐付く収入
- Maintenance ↔ Transactions: メンテナンスに紐付く支出

## 主要数式

### Occupancy Rate (%)
```
(Total Booked Nights in Period / Total Available Nights in Period) * 100
```

### Revenue Per Available Night (RevPAN)
```
Total Revenue / Total Available Nights
```

### Average Daily Rate (ADR)
```
Total Booking Revenue / Total Booked Nights
```

### Monthly Net Income (Per Listing)
```
Sum(Income Transactions) - Sum(Expense Transactions)
```

### Needs Reorder (Supplies)
```
if(Current Stock <= Reorder Threshold, "Yes", "No")
```

### Rate Difference (Pricing)
```
Your Nightly Rate - Competitor Rate
```

## サンプルデータ

### Listings（4件）
1. "Sunny Downtown Loft" — Entire Home, Active, 1BR/1BA, 4 guests, $120/night, Airbnb + VRBO
2. "Cozy Beach Cottage" — Entire Home, Active, 2BR/1BA, 6 guests, $180/night, Airbnb
3. "Modern Studio near Airport" — Entire Home, Active, Studio/1BA, 2 guests, $75/night, Airbnb + Booking.com
4. "Mountain View Cabin" — Entire Home, Paused, 3BR/2BA, 8 guests, $250/night, Airbnb + Direct

### Bookings（6件）
1. "Sarah M." — Sunny Downtown Loft, Mar 18-21, 2 guests, $110/night, $297 payout, Checked Out
2. "James K." — Cozy Beach Cottage, Mar 22-27, 4 guests, $180/night, $810 payout, Confirmed
3. "Emily R." — Modern Studio, Mar 19-20, 1 guest, $75/night, $64 payout, Checked Out
4. "Carlos D." — Sunny Downtown Loft, Mar 22-25, 3 guests, $120/night, $324 payout, Confirmed
5. "Yuki T." — Cozy Beach Cottage, Mar 28-Apr 2, 2 guests, $195/night, $878 payout, Confirmed
6. "Mike & Lisa" — Mountain View Cabin, Apr 5-12, 6 guests, $250/night, $1,575 payout, Confirmed

### Cleanings（4件）
1. "Turnover - Loft - Mar 21" — Sunny Downtown Loft, Cleaner A, Turnover, Completed, $60
2. "Turnover - Studio - Mar 20" — Modern Studio, Cleaner B, Turnover, Completed, $40
3. "Turnover - Loft - Mar 25" — Sunny Downtown Loft, Cleaner A, Turnover, Scheduled, $60
4. "Deep Clean - Beach Cottage" — Cozy Beach Cottage, Cleaner A, Deep Clean, Scheduled, $120

### Transactions（8件）
1. "Payout - Sarah M." — Income, Booking Payout, $297, Mar 21, Sunny Downtown Loft
2. "Payout - Emily R." — Income, Booking Payout, $64, Mar 20, Modern Studio
3. "Cleaning - Loft Mar 21" — Expense, Cleaning Cost, $60, Mar 21, Sunny Downtown Loft
4. "Cleaning - Studio Mar 20" — Expense, Cleaning Cost, $40, Mar 20, Modern Studio
5. "New bedding set" — Expense, Supplies, $85, Mar 15, Cozy Beach Cottage
6. "Lockbox battery replacement" — Expense, Maintenance, $12, Mar 18, Modern Studio
7. "Airbnb service fee" — Expense, Platform Fee, $45, Mar 21, Sunny Downtown Loft
8. "Direct booking - cabin deposit" — Income, Direct Payment, $500, Mar 19, Mountain View Cabin

### Supplies（4件）
1. "Shampoo bottles (travel size)" — Toiletries, Sunny Downtown Loft, Stock: 8, Threshold: 5, $2.50/ea
2. "Bath towel sets" — Linens, Cozy Beach Cottage, Stock: 3, Threshold: 4, $15/ea — Needs Reorder!
3. "Coffee pods (variety)" — Kitchen, Modern Studio, Stock: 12, Threshold: 10, $0.80/ea
4. "Toilet paper (12-pack)" — Toiletries, Sunny Downtown Loft, Stock: 2, Threshold: 3, $12/pack — Needs Reorder!

### Pricing Calendar（4件）
1. "Spring Shoulder Season" — Sunny Downtown Loft, Mid, Mar 1-May 31, $110/night, Min 2 nights, Competitor: $115
2. "Summer Peak" — Cozy Beach Cottage, Peak, Jun 1-Aug 31, $250/night, Min 3 nights, Competitor: $230
3. "Airport Hotel Alternative" — Modern Studio, Low, Year-round, $75/night, Min 1 night, Competitor: $80
4. "Holiday Premium" — Mountain View Cabin, Holiday, Dec 20-Jan 5, $350/night, Min 5 nights, Competitor: $320
