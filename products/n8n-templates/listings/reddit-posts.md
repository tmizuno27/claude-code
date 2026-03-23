# Reddit Post Drafts - n8n Templates

---

## Post 1: r/n8n

**Title:** I made 10 n8n workflow templates for common business tasks - sharing them here

**Body:**

Hey everyone,

I've been using n8n for about a year now and kept rebuilding the same workflows for different clients and projects. Eventually I decided to clean them up and package them as reusable templates.

Here's what I've got so far:

- **AI Lead Generation Pipeline** - Scrapes leads from multiple sources, enriches them with company data, scores them, and drops qualified ones into your CRM. Probably the one I use the most myself.
- **Client Onboarding Automation** - Takes a new client form submission and handles the whole chain: welcome email sequence, Slack notification, project folder creation, task setup in your PM tool.
- **Invoice & Payment Tracker** - Watches for payments, matches them against invoices, sends reminders for overdue ones, and syncs everything to your accounting sheet.

Each template comes with a setup guide and the JSON you can import directly. I tried to make them modular so you can swap out nodes without breaking things.

I put them up on Gumroad if anyone wants to grab them: [tatsuya27.gumroad.com](https://tatsuya27.gumroad.com)

Happy to answer questions about any of the workflows or how I structured them. Also open to suggestions - if there's a workflow you keep rebuilding, let me know and I might add it to the collection.

---

## Post 2: r/automation

**Title:** Moved all my Zapier workflows to n8n - here's what I learned (and the templates I made)

**Body:**

I was paying ~$50/month for Zapier to run about 15 zaps. Nothing crazy, mostly lead capture, email sequences, CRM syncing, and invoice tracking. It worked fine but the costs kept creeping up every time I added a step or hit a task limit.

Switched everything to n8n (self-hosted on a $5 VPS) and my automation costs dropped to basically nothing. The migration took a couple weekends, but most of it was straightforward once I figured out the patterns.

A few things I noticed:

- **Multi-step workflows are way easier in n8n.** Zapier charges you per step. In n8n you can branch, loop, and merge without worrying about pricing tiers.
- **Error handling is actually usable.** You can set up retry logic and fallback paths instead of just getting a "your zap failed" email.
- **The learning curve is real but short.** If you've used Zapier, you already understand the concepts. The UI is different but you get used to it in a day or two.

After migrating I cleaned up my workflows and turned them into importable templates. I also put together a migration kit that maps common Zapier triggers/actions to their n8n equivalents, so you don't have to dig through docs for every node.

Everything's on my Gumroad: [tatsuya27.gumroad.com](https://tatsuya27.gumroad.com)

If you're on the fence about switching, happy to share more details about the migration process.

---

## Post 3: r/SideProject

**Title:** Built a small digital product business selling n8n automation templates - here's how it's going

**Body:**

Wanted to share what I've been working on since I don't see many people talking about selling workflow templates as a product.

**The idea:** I work with n8n (open-source automation tool, basically self-hosted Zapier) and kept building the same workflows over and over. Lead gen pipelines, onboarding sequences, invoice trackers, social media schedulers - the usual stuff small businesses need. Figured other people were rebuilding these too, so I packaged mine as templates.

**What the templates actually are:** Importable JSON files with step-by-step setup guides. Each one is a complete workflow you can drop into your n8n instance and customize. I have about 10 right now covering things like AI-powered lead generation, client onboarding, payment tracking, and a Zapier-to-n8n migration kit.

**Pricing:** Most individual templates are $9-19. I also bundle them at a discount. Low price point means lower friction, and the margins are 95%+ since there's no COGS after the initial build.

**What's working:**
- n8n's community is growing fast (lots of people switching from Zapier) so there's real demand
- Once a template is built and documented, it's pure passive income
- The migration kit angle has been good - people actively searching for Zapier alternatives

**What I'd do differently:**
- Should have started with fewer templates and validated demand first
- Documentation takes 2-3x longer than building the actual workflow
- Would have set up an email list from day one

Everything's on Gumroad: [tatsuya27.gumroad.com](https://tatsuya27.gumroad.com)

If anyone has questions about selling digital products in the automation/developer tools space, happy to chat.
