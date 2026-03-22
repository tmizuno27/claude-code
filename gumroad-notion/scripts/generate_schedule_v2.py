"""Generate x-schedule-v2.json from the v2 tweet library."""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT = os.path.join(BASE_DIR, "config", "x-schedule-v2.json")

STORE = "https://tatsuya27.gumroad.com"
URLS = {
    "Freelance Business OS": "https://tatsuya27.gumroad.com/l/jrjhs",
    "Content Creator Dashboard": "https://tatsuya27.gumroad.com/l/ahymjd",
    "Student Study Hub": "https://tatsuya27.gumroad.com/l/qbxihb",
    "Life OS": "https://tatsuya27.gumroad.com/l/jyszka",
    "Small Business CRM": "https://tatsuya27.gumroad.com/l/sbrzyv",
    "Side Hustle Tracker": "https://tatsuya27.gumroad.com/l/hyilko",
    "Social Media Planner": "https://tatsuya27.gumroad.com/l/piaiby",
    "Job Search Tracker": "https://tatsuya27.gumroad.com/l/xeygaj",
    "Book & Learning Tracker": "https://tatsuya27.gumroad.com/l/zuesph",
    "Digital Products OS": STORE,
    "Bundle": "https://tatsuya27.gumroad.com/l/zsabbu",
}

tweets = []
tid = 1


def add(category, text, product="", is_thread=False):
    global tid
    entry = {"id": tid, "category": category, "text": text, "posted": False}
    if product:
        entry["product"] = product
    if is_thread:
        entry["is_thread"] = True
    tweets.append(entry)
    tid += 1


# ═══════════════════════════════════════
# VALUE POSTS (V01-V20)
# ═══════════════════════════════════════

add("value", (
    "The Eisenhower Matrix in 30 seconds:\n\n"
    "Urgent + Important = Do it now\n"
    "Important, not urgent = Schedule it\n"
    "Urgent, not important = Delegate it\n"
    "Neither = Delete it\n\n"
    "90% of your stress comes from treating everything as box 1.\n\n"
    "#Productivity"
))

add("value", (
    "Freelancer reality check:\n\n"
    "If you bill 40 hrs/week but spend 15 hrs on admin, "
    "your real rate is 62% of what you think.\n\n"
    "Track your non-billable hours. The number will shock you.\n\n"
    "#FreelanceTips"
))

add("value", (
    "The human brain can hold 4-7 items in working memory.\n\n"
    "Your to-do list has 47.\n\n"
    "Write. Everything. Down.\n\n"
    "Not in your head. Not on sticky notes. In ONE system you trust.\n\n"
    "#SecondBrain #Productivity"
))

add("value", (
    "Sunday habit that changed my life:\n\n"
    "1. Clear all inboxes (5 min)\n"
    "2. Review last week's wins (3 min)\n"
    "3. Pick 3 priorities for next week (5 min)\n"
    "4. Move stalled tasks to \"Someday\" (2 min)\n\n"
    "15 minutes. Entire week feels different.\n\n"
    "#ProductivityTips"
))

add("value", (
    "Stop creating content day-by-day.\n\n"
    "Monday: Write 5 posts\n"
    "Tuesday: Design all graphics\n"
    "Wednesday: Schedule the week\n"
    "Thursday-Sunday: Engage\n\n"
    "Batch creation. Daily distribution. Stress drops 80%.\n\n"
    "#ContentCreator"
))

add("value", (
    "I tracked my subscriptions last month:\n\n"
    "- Todoist: $5\n"
    "- Trello: $10\n"
    "- Airtable: $20\n"
    "- Calendly: $12\n"
    "- Notion: $0\n\n"
    "Guess which one replaced the other four.\n\n"
    "#Notion"
))

add("value", (
    "Hot take: Most side hustles are negative hourly rate.\n\n"
    "Revenue sounds great until you subtract:\n"
    "- Tools/subscriptions\n"
    "- Taxes set aside\n"
    "- Hours actually worked\n\n"
    "Know your REAL $/hour before calling it \"passive income.\"\n\n"
    "#SideHustle"
))

add("value", (
    "The students getting A's aren't smarter.\n\n"
    "They just track:\n"
    "- Every assignment + due date\n"
    "- Study hours per subject\n"
    "- Grade trends over time\n\n"
    "When you see the data, you know exactly where to focus.\n\n"
    "#StudyTips"
))

add("value", (
    "You don't lose clients because your work is bad.\n\n"
    "You lose clients because you forgot to follow up.\n\n"
    "A follow-up system beats talent every single time.\n\n"
    "#FreelanceTips #SmallBusiness"
))

add("value", (
    "The problem with New Year goals:\n\n"
    "- Written on January 1\n"
    "- Forgotten by February\n"
    "- No tracking system\n"
    "- No weekly check-in\n\n"
    "Goals without a system are just wishes.\n\n"
    "#Productivity"
))

add("value", (
    "I deleted 9 apps from my phone last month.\n\n"
    "Replaced them all with one workspace on my laptop.\n\n"
    "Less context switching = more deep work = better output.\n\n"
    "#DigitalMinimalism #Productivity"
))

add("value", (
    "I tracked 200+ job applications in a spreadsheet.\n\n"
    "Key insight: The jobs I got interviews for had one thing "
    "in common \u2014 I customized the first sentence of my cover letter.\n\n"
    "Data reveals patterns your gut never will.\n\n"
    "#JobSearch"
))

add("value", (
    "Read 20 books this year and remember nothing?\n\n"
    "Try this:\n"
    "- 3 key takeaways per chapter\n"
    "- 1 action item per book\n"
    "- Review notes monthly\n\n"
    "Retention goes from 10% to 70%.\n\n"
    "#Reading #SecondBrain"
))

add("value", (
    "As a solopreneur, your most dangerous habit is \"busy work.\"\n\n"
    "Checking email 30 times isn't working.\n"
    "Reorganizing your desktop isn't working.\n"
    "47 browser tabs isn't working.\n\n"
    "Ruthlessly protect deep work blocks.\n\n"
    "#Solopreneur"
))

add("value", (
    "Social media tip that took me too long to learn:\n\n"
    "Plan content in categories, not chronologically.\n\n"
    "- 40% educational\n"
    "- 30% personal/story\n"
    "- 20% promotional\n"
    "- 10% engagement\n\n"
    "A system beats inspiration every time.\n\n"
    "#ContentCreator"
))

add("value", (
    "Want to build a habit? Attach it to one you already have.\n\n"
    "\"After I pour my morning coffee, I write 3 priorities for the day.\"\n\n"
    "One sentence. Life-changing compound effect over 365 days.\n\n"
    "#HabitStacking #Productivity"
))

add("value", (
    "Freelancer tip: Send your invoice the SAME DAY you finish the work.\n\n"
    "Every day you delay = lower chance of getting paid on time.\n\n"
    "Set up a \"days since invoiced\" tracker. Automate the follow-up.\n\n"
    "#FreelanceTips"
))

add("value", (
    "The best productivity system is the one you actually use.\n\n"
    "Not the prettiest. Not the most complex. "
    "Not the one your favorite YouTuber uses.\n\n"
    "The one YOU open every single day.\n\n"
    "#Notion #Productivity"
))

add("value", (
    "Decision fatigue is why you eat junk food at 9 PM.\n\n"
    "You made 35,000 decisions today. Your brain is fried.\n\n"
    "Solution: Automate the small decisions. "
    "Meal prep. Outfit rotation. Pre-planned content calendar.\n\n"
    "Save brainpower for what matters.\n\n"
    "#Productivity"
))

add("value", (
    "1% better every day = 37x better in a year.\n\n"
    "But only if you track it.\n\n"
    "You can't improve what you don't measure.\n\n"
    "#Productivity #CompoundEffect"
))


# ═══════════════════════════════════════
# PROMO POSTS (P01-P20)
# ═══════════════════════════════════════

add("promo", (
    "Running a freelance business with spreadsheets "
    "is like driving with your eyes closed.\n\n"
    "Freelance Business OS for Notion:\n"
    "- Clients + revenue at a glance\n"
    "- Project pipeline (Kanban)\n"
    "- Invoice tracker with reminders\n"
    "- Time tracking per client\n\n"
    "$19 once. $0/month forever.\n\n"
    f"{URLS['Freelance Business OS']}"
), "Freelance Business OS")

add("promo", (
    "Unpopular opinion: You don't need more motivation.\n\n"
    "You need a system that works when motivation doesn't.\n\n"
    "Life OS \u2014 goals, habits, tasks, journal, finances, health.\n\n"
    "10 databases. 45+ views. One Notion workspace.\n\n"
    f"{URLS['Life OS']}"
), "Life OS")

add("promo", (
    "Math:\n\n"
    "10 Notion templates bought separately = $142\n"
    "The same 10 in a bundle = $49\n\n"
    "You save $93. That's 66% off.\n\n"
    "70+ databases. 300+ views. Every part of your life, organized.\n\n"
    f"{URLS['Bundle']}"
), "Bundle")

add("promo", (
    "Creators: Can you answer these in 5 seconds?\n\n"
    "- What should you post tomorrow?\n"
    "- What performed best last month?\n"
    "- How many brand deals are in your pipeline?\n\n"
    "If not, you need Content Creator Dashboard.\n\n"
    "$15. One workspace. Zero guesswork.\n\n"
    f"{URLS['Content Creator Dashboard']}"
), "Content Creator Dashboard")

add("promo", (
    "Salesforce: $25/user/month\n"
    "HubSpot: $45/month\n"
    "Notion CRM: $17 once\n\n"
    "Same features for 90% of small businesses:\n"
    "- Contact database\n"
    "- Deal pipeline\n"
    "- Follow-up reminders\n"
    "- Activity log\n\n"
    "No monthly fees. Ever.\n\n"
    f"{URLS['Small Business CRM']}"
), "Small Business CRM")

add("promo", (
    "Built this for a friend in college.\n\n"
    "She went from missing 3 deadlines/semester to zero.\n\n"
    "GPA up 0.4 points in one term.\n\n"
    "Student Study Hub \u2014 $9.\n\n"
    "Cheaper than one late assignment penalty.\n\n"
    f"{URLS['Student Study Hub']}"
), "Student Study Hub")

add("promo", (
    "87% of side hustles fail in the first year.\n\n"
    "The #1 reason? Not tracking the numbers.\n\n"
    "Side Hustle Tracker:\n"
    "- Revenue & expenses per hustle\n"
    "- Real $/hour calculation\n"
    "- P&L dashboard\n\n"
    "Know your numbers. Keep your hustle alive.\n\n"
    f"$12 \u2192 {URLS['Side Hustle Tracker']}"
), "Side Hustle Tracker")

add("promo", (
    "POV: It's Monday morning and your entire week "
    "of social media is already planned.\n\n"
    "Content calendar. Hashtag library. "
    "Analytics tracker. Campaign manager.\n\n"
    "Social Media Planner for Notion \u2014 $14.\n\n"
    "Never scramble for content again.\n\n"
    f"{URLS['Social Media Planner']}"
), "Social Media Planner")

add("promo", (
    "Before: Applied to 50 jobs. Lost track of 30. "
    "Missed 3 follow-ups.\n\n"
    "After Job Search Tracker:\n"
    "- Every application in a pipeline\n"
    "- Interview prep notes per company\n"
    "- Automatic follow-up reminders\n\n"
    "$9. Land the job faster.\n\n"
    f"{URLS['Job Search Tracker']}"
), "Job Search Tracker")

add("promo", (
    "I used to read 30 books a year and remember nothing.\n\n"
    "Now I capture 3 takeaways per chapter in Notion.\n\n"
    "Book & Learning Tracker:\n"
    "- Reading list with progress\n"
    "- Notes & highlights\n"
    "- Annual reading challenge\n\n"
    "Read more. Forget less. $9.\n\n"
    f"{URLS['Book & Learning Tracker']}"
), "Book & Learning Tracker")

add("promo", (
    "Launching a digital product is 20% creation, "
    "80% everything else.\n\n"
    "Digital Products OS:\n"
    "- Product catalog\n"
    "- Sales tracking\n"
    "- Launch checklists\n"
    "- Customer feedback\n\n"
    "Built for Gumroad/Etsy sellers. $19.\n\n"
    f"{STORE}"
), "Digital Products OS")

add("promo", (
    "Here's what $49 gets you:\n\n"
    "1. Run a freelance business\n"
    "2. Manage content creation\n"
    "3. Track your studies\n"
    "4. Build a second brain\n"
    "5. Manage customers (CRM)\n"
    "6. Track side hustles\n"
    "7. Plan social media\n"
    "8. Organize job searches\n"
    "9. Log reading & learning\n"
    "10. Launch digital products\n\n"
    f"All 10. $49.\n\n{URLS['Bundle']}"
), "Bundle")

add("promo", (
    "$19 for Freelance Business OS.\n\n"
    "But consider:\n"
    "- 1 recovered unpaid invoice = $500+\n"
    "- 15 hrs/month saved on admin = $750+\n"
    "- 1 new client from better follow-up = $2,000+\n\n"
    "ROI in week one.\n\n"
    f"{URLS['Freelance Business OS']}"
), "Freelance Business OS")

add("promo", (
    "Your brain is full.\n\n"
    "Ideas. Tasks. Goals. Notes. Bookmarks. Plans. Dreams.\n\n"
    "Stop holding it all in your head.\n\n"
    "Life OS \u2014 externalize everything into one trusted system.\n\n"
    "10 databases. 45+ views. $19.\n\n"
    f"{URLS['Life OS']}"
), "Life OS")

add("promo", (
    "$49 for 10 templates = $4.90 each.\n\n"
    "That's less than a latte for a system "
    "you'll use every single day.\n\n"
    "70+ databases. 300+ views. 10 complete systems.\n\n"
    f"{URLS['Bundle']}"
), "Bundle")

add("promo", (
    "I lost a $3,000 client because I forgot to follow up.\n\n"
    "Never again.\n\n"
    "Built a CRM in Notion. Now every contact has:\n"
    "- Last interaction date\n"
    "- Next follow-up reminder\n"
    "- Deal stage\n"
    "- Revenue history\n\n"
    f"$17 once \u2192 {URLS['Small Business CRM']}"
), "Small Business CRM")

add("promo", (
    "Content creators: You don't have a creativity problem.\n\n"
    "You have a systems problem.\n\n"
    "When you sit down to create, do you know:\n"
    "- What to post today?\n"
    "- What worked last week?\n"
    "- What's in your pipeline?\n\n"
    "Content Creator Dashboard. $15.\n\n"
    f"{URLS['Content Creator Dashboard']}"
), "Content Creator Dashboard")

add("promo", (
    "Content creation hack most people miss:\n\n"
    "Batch by TYPE, not by platform.\n\n"
    "Monday: Write 5 captions\n"
    "Tuesday: Create 5 graphics\n"
    "Wednesday: Schedule everything\n\n"
    "Social Media Planner makes this visual. $14.\n\n"
    f"{URLS['Social Media Planner']}"
), "Social Media Planner")

add("promo", (
    "Side hustle reality check:\n\n"
    "Revenue: $2,000/mo (sounds great)\n"
    "Expenses: $400/mo\n"
    "Hours: 80 hrs/mo\n\n"
    "Actual rate: $20/hr\n\n"
    "Worth it? Only the numbers can tell you.\n\n"
    "Side Hustle Tracker calculates this automatically. $12.\n\n"
    f"{URLS['Side Hustle Tracker']}"
), "Side Hustle Tracker")

add("promo", (
    "People ask: \"Which template should I start with?\"\n\n"
    "My answer: Get the bundle.\n\n"
    "It's $49 for all 10 ($142 value).\n\n"
    "Start with 2-3 that fit your life right now.\n"
    "Add more as you grow.\n"
    "They're yours forever.\n\n"
    f"{URLS['Bundle']}"
), "Bundle")


# ═══════════════════════════════════════
# THREAD STARTERS (T01-T15)
# ═══════════════════════════════════════

add("thread", (
    "5 Notion mistakes that are killing your productivity:\n\n"
    "1/ Building databases you never look at again\n"
    "2/ No weekly review ritual\n"
    "3/ Too many separate pages (use linked databases!)\n"
    "4/ No templates for recurring workflows\n"
    "5/ Making it pretty before making it functional\n\n"
    f"Fix all 5 with a proven system \u2192 {STORE}\n\n"
    "#Notion #Productivity"
))

add("thread", (
    "I replaced 6 apps with one Notion workspace. "
    "Here's my entire freelance stack:\n\n"
    "CLIENT MGMT: One database. Every client, project, dollar linked.\n"
    "PROJECT TRACKING: Kanban + Timeline + Table views.\n"
    "TIME TRACKING: Quick-log linked to projects.\n"
    "INVOICING: \"Days Since Sent\" formula. Auto follow-up.\n"
    "EXPENSES: Categorized, tagged for tax deductions.\n\n"
    f"$19 once. $0/month.\n\n{URLS['Freelance Business OS']}"
), "Freelance Business OS")

add("thread", (
    "\"Why pay for a Notion template when Notion is free?\"\n\n"
    "Because you're not paying for databases. "
    "You're paying for ARCHITECTURE.\n\n"
    "Building from scratch: 20-40 hours\n"
    "Buying a template + customizing: 30 minutes\n\n"
    "If your time is worth $25/hr, building costs $500+.\n"
    "A template costs less than lunch.\n\n"
    f"{STORE}"
))

add("thread", (
    "How to set up your entire life system in 30 minutes:\n\n"
    "1. Rate 8 life areas 1-10 (5 min)\n"
    "2. Set 3 goals for lowest areas (5 min)\n"
    "3. Break into projects + tasks (5 min)\n"
    "4. Pick 3-5 daily habits (5 min)\n"
    "5. Start 2-min daily journal (5 min)\n"
    "6. Weekly review every Sunday (5 min)\n\n"
    f"Life OS has all of this pre-built \u2192 {URLS['Life OS']}"
), "Life OS")

add("thread", (
    "How to audit your side hustle in 15 minutes:\n\n"
    "1. Write down ALL income (last 3 months)\n"
    "2. Write down ALL expenses\n"
    "3. Estimate total HOURS/month\n"
    "4. Calculate: (Revenue - Expenses) / Hours = Real $/hour\n"
    "5. Compare to your day job rate\n\n"
    "If it pays less than your 9-5... you have a hobby, not a business.\n\n"
    f"Side Hustle Tracker automates this \u2192 {URLS['Side Hustle Tracker']}"
), "Side Hustle Tracker")

add("thread", (
    "My content calendar system that saves 5+ hours/week:\n\n"
    "1. CATEGORIES: Educational 40%, Personal 30%, Promo 20%, Engagement 10%\n"
    "2. BATCHING: Mon=write, Tue=design, Wed=schedule\n"
    "3. HASHTAG LIBRARY: Pre-researched by niche\n"
    "4. ANALYTICS: Sunday review. Double down on winners.\n"
    "5. REPURPOSE: Top tweets become LinkedIn posts.\n\n"
    f"Social Media Planner \u2192 {URLS['Social Media Planner']}"
), "Social Media Planner")

add("thread", (
    "How I manage 50+ business contacts without Salesforce:\n\n"
    "1. CONTACT DB: name, company, email, deal stage\n"
    "2. DEAL PIPELINE: Kanban \u2014 Lead \u2192 Contacted \u2192 Proposal \u2192 Won/Lost\n"
    "3. ACTIVITY LOG: Every call/email linked to contact\n"
    "4. FOLLOW-UP: \"Days Since Last Contact\" formula\n\n"
    f"$17 once. $0/month.\n\n{URLS['Small Business CRM']}"
), "Small Business CRM")

add("thread", (
    "10 Notion templates in 60 seconds:\n\n"
    "1. Freelance Business OS ($19)\n"
    "2. Content Creator Dashboard ($15)\n"
    "3. Student Study Hub ($9)\n"
    "4. Life OS / Second Brain ($19)\n"
    "5. Small Business CRM ($17)\n"
    "6. Side Hustle Tracker ($12)\n"
    "7. Social Media Planner ($14)\n"
    "8. Job Search Tracker ($9)\n"
    "9. Book & Learning Tracker ($9)\n"
    "10. Digital Products OS ($19)\n\n"
    f"All 10 for $49 (normally $142) \u2192 {URLS['Bundle']}"
), "Bundle")

add("thread", (
    "I applied to 200+ jobs. Here's the system that got me hired:\n\n"
    "PIPELINE: Applied \u2192 Phone Screen \u2192 Interview \u2192 Offer\n"
    "COMPANY RESEARCH: Culture notes, salary data, contacts\n"
    "FOLLOW-UP: 5 business days after applying. Every time.\n"
    "INTERVIEW PREP: 3 stories + 3 questions per company\n\n"
    f"$9 \u2192 {URLS['Job Search Tracker']}"
), "Job Search Tracker")

add("thread", (
    "My digital product launch checklist:\n\n"
    "PRE-LAUNCH: Product page, thumbnail, 3 teaser posts, email list\n"
    "LAUNCH DAY: Post on 3 platforms before 9 AM, reply to every comment\n"
    "POST-LAUNCH: Track sales daily, collect feedback, plan v2\n\n"
    f"Digital Products OS tracks all of this \u2192 {STORE}"
), "Digital Products OS")

add("thread", (
    "How to actually remember what you read:\n\n"
    "1. While reading: highlight 3 things/chapter\n"
    "2. After each chapter: 1-sentence summary\n"
    "3. After the book: 3 key takeaways\n"
    "4. Pick 1 action item for THIS WEEK\n"
    "5. Monthly: review all book notes (15 min)\n\n"
    f"Retention: ~10% \u2192 ~70%\n\nBook & Learning Tracker \u2192 {URLS['Book & Learning Tracker']}"
), "Book & Learning Tracker")

add("thread", (
    "College students \u2014 never miss a deadline again:\n\n"
    "1. Enter every syllabus deadline on day 1\n"
    "2. Link assignments to courses\n"
    "3. Track study hours per subject\n"
    "4. Review grade trends weekly\n"
    "5. Use \"due this week\" view every Monday\n\n"
    f"30 min setup. 30+ hours panic saved per semester.\n\n$9 \u2192 {URLS['Student Study Hub']}"
), "Student Study Hub")

add("thread", (
    "My complete productivity stack costs $49 total:\n\n"
    "Morning: Life OS dashboard \u2192 today's priorities\n"
    "Work: Freelance Business OS \u2192 client tasks\n"
    "Content: Creator Dashboard \u2192 what to post\n"
    "Evening: Habit tracker \u2192 daily check-off\n"
    "Sunday: Weekly review \u2192 plan next week\n\n"
    f"All connected. All in Notion.\n\n{URLS['Bundle']}"
), "Bundle")

add("thread", (
    "5 freelancer mistakes that cost me $10,000+:\n\n"
    "1. Not tracking billable vs non-billable hours\n"
    "2. Forgetting to invoice within 48 hours\n"
    "3. No follow-up system (lost 5 warm leads)\n"
    "4. Mixing personal + business expenses\n"
    "5. No client profitability view\n\n"
    f"All 5 solved with one template \u2192 {URLS['Freelance Business OS']}"
), "Freelance Business OS")

add("thread", (
    "The real cost of building your own Notion system:\n\n"
    "Week 1: Watch 10 YouTube tutorials (5 hrs)\n"
    "Week 2: Build v1 (10 hrs)\n"
    "Week 3: Relations are wrong. Rebuild. (8 hrs)\n"
    "Week 4: Formulas break. Fix. (6 hrs)\n"
    "Week 8: Need 3 more databases. Start over.\n\n"
    "Total: 40+ hours.\n\n"
    f"OR: Buy a template. Customize in 30 min.\n\n$4.90/template \u2192 {URLS['Bundle']}"
), "Bundle")


# ═══════════════════════════════════════
# ENGAGEMENT HOOKS (E01-E15)
# ═══════════════════════════════════════

add("engagement", (
    "Quick poll: How many apps do you use to manage your work/life?\n\n"
    "A) 1-3 (minimalist king)\n"
    "B) 4-6 (average)\n"
    "C) 7-10 (it's complicated)\n"
    "D) 10+ (send help)"
))

add("engagement", (
    "What's the ONE productivity habit that actually stuck for you?\n\n"
    "Genuinely curious. Drop it below."
))

add("engagement", (
    "This or That:\n\n"
    "Start your day with a to-do list\n"
    "OR\n"
    "Start your day with your calendar\n\n"
    "(My answer might surprise you)"
))

add("engagement", (
    "Hot take: Most \"productivity systems\" are just "
    "procrastination with extra steps.\n\n"
    "The best system is the one you actually open every day.\n\n"
    "Agree or disagree?"
))

add("engagement", (
    "Freelancers: What's your biggest time sink "
    "that ISN'T client work?\n\n"
    "I'll go first: Chasing invoices."
))

add("engagement", (
    "Fill in the blank:\n\n"
    "\"If I had a system for _____, my life would be 10x easier.\""
))

add("engagement", (
    "Side hustlers: How many hours/week do you "
    "actually spend on your hustle?\n\n"
    "Be honest. Include the hours you don't think \"count.\""
))

add("engagement", (
    "Debate: Is Notion better than...\n\n"
    "A) Google Sheets for project management\n"
    "B) Trello for Kanban boards\n"
    "C) Apple Notes for quick capture\n"
    "D) All of the above\n\n"
    "My take: For SYSTEMS \u2014 Notion wins."
))

add("engagement", (
    "Students: What's the biggest challenge with staying organized?\n\n"
    "- Too many deadlines at once?\n"
    "- Losing track of grades?\n"
    "- No study schedule?\n"
    "- Something else?"
))

add("engagement", (
    "Confession: I used to spend more time ORGANIZING my to-do list "
    "than actually DOING the tasks.\n\n"
    "Anyone else? Or just me?"
))

add("engagement", (
    "Be honest: How many of your January goals are still alive?\n\n"
    "If less than half \u2014 it's not a motivation problem. "
    "It's a tracking problem."
))

add("engagement", (
    "Would you rather:\n\n"
    "A) One perfect productivity system you use forever\n"
    "B) Try a new app every month hoping it's \"the one\"\n\n"
    "(Most people say A but live like B)"
))

add("engagement", (
    "Content creators: What takes you longer?\n\n"
    "A) Coming up with ideas\n"
    "B) Actually creating the content\n"
    "C) Figuring out when/where to post"
))

add("engagement", (
    "Hot take: Paying $19 for a Notion template "
    "saves you more time than a $200 online course.\n\n"
    "The course teaches theory.\n"
    "The template gives you a working system.\n\n"
    "Fight me."
))

add("engagement", (
    "If you could wave a magic wand and have ONE system "
    "perfectly organized, what would it be?\n\n"
    "A) Finances\n"
    "B) Health/fitness\n"
    "C) Work projects\n"
    "D) Knowledge/notes\n"
    "E) All of the above (mood)"
))


# ═══════════════════════════════════════
# SEASONAL (S01-S10)
# ═══════════════════════════════════════

add("seasonal", (
    "It's Q1. Your goals are fresh.\n\n"
    "But 92% of New Year resolutions fail by February.\n\n"
    "The difference? A tracking system.\n\n"
    "Life OS has built-in goal tracking + weekly reviews.\n\n"
    f"Don't be the 92%.\n\n{URLS['Life OS']}"
), "Life OS")

add("seasonal", (
    "Tax season reminder for freelancers:\n\n"
    "If you tracked expenses all year, tax prep takes 30 minutes.\n\n"
    "If you didn't... 30 hours.\n\n"
    "Freelance Business OS has expense tracking built in.\n\n"
    f"Start now. Future-you says thanks.\n\n{URLS['Freelance Business OS']}"
), "Freelance Business OS")

add("seasonal", (
    "Spring cleaning your digital life:\n\n"
    "1. Delete apps you haven't opened in 30 days\n"
    "2. Unsubscribe from 10 newsletters\n"
    "3. Consolidate tools into one workspace\n"
    "4. Set up a weekly review habit\n\n"
    "Your brain will thank you.\n\n"
    "#Productivity"
))

add("seasonal", (
    "New grads: The job market is competitive.\n\n"
    "The candidates who stand out aren't just applying "
    "\u2014 they're TRACKING.\n\n"
    "Every application. Every follow-up. Every interview.\n\n"
    f"Job Search Tracker \u2192 $9.\n\n{URLS['Job Search Tracker']}"
), "Job Search Tracker")

add("seasonal", (
    "Back to school season.\n\n"
    "This semester, try something different:\n"
    "Enter EVERY deadline from your syllabus in one dashboard.\n\n"
    "Zero missed deadlines. Better grades. Less stress.\n\n"
    f"Student Study Hub \u2192 $9\n\n{URLS['Student Study Hub']}"
), "Student Study Hub")

add("seasonal", (
    "Summer = peak side hustle season.\n\n"
    "Before you start: set up tracking from DAY ONE.\n\n"
    "Revenue. Expenses. Hours. Real $/hour.\n\n"
    "The hustles that survive track their numbers.\n\n"
    f"{URLS['Side Hustle Tracker']}"
), "Side Hustle Tracker")

add("seasonal", (
    "Black Friday deal:\n\n"
    "10 Notion templates.\n"
    "Normally $142.\n"
    "Today: $49.\n\n"
    "That's 66% off.\n\n"
    "No subscription. No monthly fees. Yours forever.\n\n"
    f"{URLS['Bundle']}"
), "Bundle")

add("seasonal", (
    "December tradition: The Annual Review.\n\n"
    "Open your dashboard:\n"
    "- Goals hit vs. missed\n"
    "- Habits maintained\n"
    "- Books read\n"
    "- Revenue earned\n\n"
    "You can't review what you didn't track.\n\n"
    f"Start tracking \u2192 {URLS['Life OS']}"
), "Life OS")

add("seasonal", (
    "Everyone's talking about AI tools.\n\n"
    "But AI can't organize your life for you.\n\n"
    "It can help you CREATE content faster.\n"
    "It can't help you MANAGE your business.\n\n"
    "That's what systems are for.\n\n"
    "#Productivity #AI"
))

add("seasonal", (
    "Remote work tip: Your home office needs "
    "a digital command center.\n\n"
    "Not just a to-do list. A SYSTEM.\n\n"
    "Projects. Tasks. Time tracking. Goals. Habits.\n\n"
    "When nobody's watching, your system keeps you accountable.\n\n"
    "#RemoteWork"
))


# ═══════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════

schedule = {
    "version": 2,
    "posting_times_pyt": ["10:00", "14:00", "19:00"],
    "note": (
        "V2: 5 categories (value/promo/thread/engagement/seasonal). "
        "80 tweets total. ~27 day cycle. "
        "Auto-reset when a category is exhausted."
    ),
    "category_schedule": {
        "10:00": "value or engagement (weekends)",
        "14:00": "value or thread (Tue/Thu)",
        "19:00": "promo (even days) or value (odd days)",
    },
    "tweets": tweets,
}

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(schedule, f, indent=2, ensure_ascii=False)

print(f"Created {OUTPUT}")
print(f"Total tweets: {len(tweets)}")
cats = {}
for t in tweets:
    c = t["category"]
    cats[c] = cats.get(c, 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")
