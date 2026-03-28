"""
Gumroad Product Creator
Creates new products via Gumroad API and optionally uploads thumbnails.

Usage:
  python gumroad_create_products.py                    # Create all pending products
  python gumroad_create_products.py --dry-run          # Preview without creating
  python gumroad_create_products.py --product 18       # Create specific product only

Prerequisites:
  1. Get Gumroad access token from https://app.gumroad.com/settings/advanced#application-form
  2. Save it to config/secrets.json as {"gumroad_access_token": "YOUR_TOKEN"}
"""

import io
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRETS_PATH = os.path.join(BASE_DIR, "config", "secrets.json")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "logs")

for d in [OUTPUT_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "gumroad-create-products.log")
GUMROAD_API_BASE = "https://api.gumroad.com/v2"
PYT = timezone(timedelta(hours=-3))


# ── Data ───────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class ProductSpec:
    number: int
    name: str
    price_cents: int
    description: str
    tags: str
    url_slug: str
    thumbnail_path: str
    cover_path: str


PENDING_PRODUCTS: list[ProductSpec] = [
    ProductSpec(
        number=16,
        name="Social Media Marketing Mega Prompt Pack — 55 AI Prompts for Instagram, X, LinkedIn, TikTok & More",
        price_cents=1400,
        description=(
            "Stop staring at a blank screen wondering what to post.\n\n"
            "This pack gives you 55 battle-tested AI prompts that turn ChatGPT, Claude, or any LLM into your full social media team — content strategist, copywriter, community manager, and analytics advisor.\n\n"
            "Whether you're a solopreneur, freelancer, small business owner, or marketing manager, these prompts eliminate the guesswork and save you 10+ hours per week on social media.\n\n"
            "🎯 WHAT'S INSIDE (55 Prompts in 6 Categories):\n\n"
            "📋 Content Strategy & Planning (10 Prompts)\n"
            "• Monthly content calendar generator\n• Content pillar framework builder\n• Competitor content analysis\n• Trending topic newsjacking templates\n• Weekly content batch creator\n• Content repurposing matrix (1 piece → 8 platforms)\n• Audience persona deep dive\n• Content audit & strategy reset\n• Seasonal & holiday planner\n• Platform migration strategy\n\n"
            "✍️ Copywriting & Captions (12 Prompts)\n"
            "• Scroll-stopping hook generator (20 hooks per run)\n• Instagram carousel script writer (10-slide format)\n• X/Twitter thread writer (viral format)\n• LinkedIn thought leadership post\n• Short-form video scripts (Reels/TikTok/Shorts)\n• Story/Reel series planner\n• Engagement-bait caption formulas\n• Product launch social copy sequence\n• Bio & profile optimizer\n• UGC campaign builder\n• Caption A/B testing framework\n• Hashtag strategy builder\n\n"
            "📈 Growth & Engagement (10 Prompts)\n"
            "• Organic growth strategy (no bots, no F4F)\n• Comment & DM response templates (40+ templates)\n• Collaboration & partnership outreach\n• Viral content reverse engineering\n• Solo engagement boosting strategy\n• Giveaway & contest campaign builder\n• Social proof & testimonial maximizer\n• Cross-platform growth engine\n• Engagement recovery plan\n• Niche community building strategy\n\n"
            "📊 Analytics & Optimization (8 Prompts)\n"
            "• Weekly analytics report generator\n• A/B test planner\n• Best posting time analyzer\n• ROI calculator for social media\n• Content performance predictor\n• Audience growth funnel mapper\n• Shadowban detection & recovery\n• Monthly analytics deep dive\n\n"
            "📱 Platform-Specific Mastery (8 Prompts)\n"
            "• Instagram algorithm hack sheet (2026)\n• TikTok growth playbook\n• LinkedIn personal brand builder (90-day plan)\n• YouTube Community Tab & Shorts strategy\n• Pinterest SEO & traffic strategy\n• Facebook Group growth & monetization\n• X (Twitter) growth machine\n• Multi-platform ads strategy\n\n"
            "🚀 Crisis & Advanced Tactics (7 Prompts)\n"
            "• Crisis management plan\n• AI-powered content workflow\n• Influencer campaign manager\n• Social commerce & shoppable content\n• Personal brand content ecosystem\n• Social media automation blueprint\n• Annual strategy planner\n\n"
            "✅ WHY THIS PACK IS DIFFERENT:\n\n"
            "→ Not generic one-liners. Each prompt is 100-300 words with structured instructions, expected outputs, and pro tips.\n"
            "→ Works with ANY AI tool: ChatGPT, Claude, Gemini, Copilot, Llama, Mistral — you name it.\n"
            "→ Covers ALL major platforms: Instagram, X/Twitter, LinkedIn, TikTok, YouTube, Pinterest, Facebook.\n"
            "→ Includes a Quick Start Guide and a 15-minute daily routine.\n"
            "→ Copy, paste, fill in the [BRACKETS], and get results instantly.\n\n"
            "📦 FORMAT: Markdown file (works in any text editor, Notion, Obsidian, etc.)\n\n"
            "⚡ INSTANT DOWNLOAD — Start creating better content in the next 5 minutes."
        ),
        tags="ai prompts, social media marketing, chatgpt prompts, instagram marketing, tiktok marketing, linkedin marketing, content strategy, social media templates, twitter prompts, content calendar, social media growth, AI marketing, prompt pack, digital marketing, social media manager",
        url_slug="social-media-marketing-prompts",
        thumbnail_path=os.path.join(IMAGES_DIR, "16-social-media-marketing-prompts.png"),
        cover_path=os.path.join(IMAGES_DIR, "16-social-media-marketing-prompts-cover.png"),
    ),
    ProductSpec(
        number=17,
        name="ADHD Daily Planner — Finally, a System That Works With Your Brain (Notion Template)",
        price_cents=1400,
        description=(
            "Generic planners weren't built for your brain. This one was.\n\n"
            "You've tried 15 productivity apps. You've downloaded 10 Notion templates. You've set up elaborate systems that you used for 3 days and then abandoned.\n\n"
            "It's not a discipline problem. It's a design problem. Those systems were built for neurotypical brains.\n\n"
            "ADHD Daily Planner is designed around how ADHD brains actually work — not how productivity gurus think they should work.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Why Most Planners Fail for ADHD:\n\n"
            "• Too many tasks: Decision paralysis. You stare at a list of 20 items and do none.\n"
            "• No energy awareness: They schedule tasks without considering your energy fluctuates wildly.\n"
            "• Guilt-based design: \"You missed 5 habits!\" makes you abandon the whole system.\n"
            "• No brain dump: Your 47 random thoughts have nowhere to go.\n"
            "• Ignore hyperfocus: Your superpower gets treated as a bug.\n\n"
            "This template fixes all of that.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "What Makes This Different:\n\n"
            "• Maximum 3 tasks per day. Not 10. Not 20. Three.\n"
            "• Energy-based scheduling. Match tasks to your energy level.\n"
            "• Brain Dump Inbox. Random thought? Dump it. Sort it later. Or never.\n"
            "• Hyperfocus Logger. Track when you hyperfocus, what triggers it.\n"
            "• Dopamine Rewards. Each task has a reward field.\n"
            "• No-guilt design. Missed a day? The system resets. No shame spirals.\n"
            "• Start with 2 features. The rest are there when you're ready.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "What's Inside:\n\n"
            "• Brain Dump Inbox — Capture every random thought in <5 seconds\n"
            "• Daily Focus Board — Maximum 3 tasks. Kanban style. Dopamine rewards built in.\n"
            "• Energy & Mood Tracker — Morning/afternoon/evening energy levels\n"
            "• Hyperfocus Session Logger — What triggered it? Was it productive?\n"
            "• ADHD-Optimized Habit Tracker — Start with 1 habit. Streaks celebrate, not punish.\n"
            "• Project Parking Lot — 100 ideas? Park 98 of them. Work on 2.\n"
            "• Command Center Dashboard — Today's focus + energy + habits. One glance.\n\n"
            "6 databases. ADHD-affirming callouts throughout.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Who It's For:\n"
            "• Adults with ADHD (diagnosed or \"I'm pretty sure I have it\")\n"
            "• Anyone who's abandoned 10+ productivity systems\n"
            "• Neurodivergent professionals who need structure without rigidity\n"
            "• Students with ADHD drowning in assignments\n\n"
            "How To Use:\n"
            "1. Duplicate to Notion (free plan works perfectly)\n"
            "2. Open the Dashboard — this is your daily home\n"
            "3. Week 1: Use ONLY Brain Dump + Daily Focus Board\n"
            "4. Week 2: Add Energy Tracking\n"
            "5. Week 3: Add 1 habit\n"
            "6. Later: Add Hyperfocus Logger and Project Parking Lot\n\n"
            "The golden rule: Don't try to use everything at once. Start stupidly small."
        ),
        tags="notion, template, ADHD, ADHD planner, executive function, focus, daily planner, brain dump, dopamine, hyperfocus, habit tracker, energy tracker, neurodivergent, adult ADHD, ADHD tools, ADHD friendly, notion workspace, productivity ADHD, no subscription, 2026",
        url_slug="adhd-daily-planner",
        thumbnail_path=os.path.join(IMAGES_DIR, "17-adhd-daily-planner.png"),
        cover_path=os.path.join(IMAGES_DIR, "17-adhd-daily-planner-cover.png"),
    ),
    ProductSpec(
        number=18,
        name="AI Business Automation Mega Prompt Pack — 50+ Prompts to Run Your Business on Autopilot",
        price_cents=1200,
        description=(
            "Stop doing manually what AI can do in seconds.\n\n"
            "This pack contains 50+ battle-tested prompts designed for solopreneurs and small teams who want to automate repetitive business tasks using ChatGPT, Claude, or any LLM.\n\n"
            "Every prompt has been tested in real business operations — not theoretical templates, but actual workflows that save 10+ hours per week.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "📧 EMAIL & COMMUNICATION (10 prompts)\n"
            "• Customer inquiry auto-responder\n• Follow-up email sequence generator\n• Meeting summary & action items extractor\n• Cold outreach personalization\n• Support ticket categorizer & draft responder\n• Newsletter content generator\n• Client onboarding email sequence\n• Feedback request composer\n• Partnership proposal writer\n• Complaint resolution drafter\n\n"
            "📝 CONTENT & MARKETING (12 prompts)\n"
            "• Blog post outline from keyword\n• 30-day social media content calendar\n• Product description optimizer\n• SEO meta title & description generator\n• Ad copy A/B test variants\n• Landing page copy framework\n• Case study writer from raw notes\n• Testimonial request & formatter\n• Competitor analysis summarizer\n• Content repurposing (blog → social → email)\n• Hashtag research & strategy\n• Brand voice consistency checker\n\n"
            "⚙️ OPERATIONS & FINANCE (10 prompts)\n"
            "• Invoice data extractor\n• Expense categorizer\n• Project status report generator\n• SOP writer\n• Meeting agenda creator\n• Risk assessment analyzer\n• Vendor comparison matrix\n• KPI dashboard narrative writer\n• Process bottleneck identifier\n• Resource allocation optimizer\n\n"
            "💰 SALES & CRM (10 prompts)\n"
            "• Lead qualification scorer\n• Proposal customizer from template\n• Objection handler script generator\n• Win/loss analysis summarizer\n• Upsell opportunity identifier\n• Sales call prep briefing\n• Pipeline forecast narrator\n• Customer segment profiler\n• Referral request composer\n• Churn risk early warning analyzer\n\n"
            "📊 DATA & RESEARCH (10 prompts)\n"
            "• Market research summarizer\n• Survey response analyzer\n• Competitive pricing analyzer\n• Trend spotter from news feeds\n• SWOT analysis generator\n• Customer feedback theme extractor\n• Industry report key takeaway extractor\n• A/B test result analyzer\n• ROI calculator narrative\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ WHAT MAKES THIS DIFFERENT\n\n"
            "→ Every prompt includes [VARIABLES] you fill in — no guesswork\n"
            "→ Tested on real businesses, not made up in a lab\n"
            "→ Works with ChatGPT, Claude, Gemini, Copilot, or any LLM\n"
            "→ Includes prompt chaining guide (connect prompts for end-to-end workflows)\n"
            "→ Includes LLM comparison chart (which AI is best for each task)\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 WHO THIS IS FOR\n\n"
            "• Solopreneurs wearing all the hats\n• Freelancers scaling without hiring\n• Small business owners drowning in admin\n• Anyone who wants to work smarter, not harder\n\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "💡 THE MATH\n\n"
            "If these prompts save you just 2 hours per week, that's 100+ hours per year. At $50/hour, that's $5,000+ in time saved — for a one-time $12 investment.\n\n"
            "Buy once. Use forever. Update your business, not your to-do list."
        ),
        tags="ai prompts, business automation, chatgpt prompts, claude prompts, solopreneur tools, productivity, workflow automation, email templates, sales prompts, marketing automation",
        url_slug="business-automation-prompts",
        thumbnail_path=os.path.join(IMAGES_DIR, "18-business-automation-prompts.png"),
        cover_path=os.path.join(IMAGES_DIR, "18-business-automation-prompts-cover.png"),
    ),
]


# ── Helpers ────────────────────────────────────────────────────────────────
def log(message: str) -> None:
    timestamp = datetime.now(PYT).strftime("%Y-%m-%d %H:%M:%S PYT")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_access_token() -> Optional[str]:
    """Load Gumroad access token from config/secrets.json."""
    if not os.path.exists(SECRETS_PATH):
        return None
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        token = data.get("gumroad_access_token", "")
        if not token or token.startswith("YOUR_"):
            return None
        return token
    except (json.JSONDecodeError, OSError):
        return None


def create_product(token: str, spec: ProductSpec) -> dict:
    """Create a product on Gumroad via API."""
    url = f"{GUMROAD_API_BASE}/products"
    payload = {
        "access_token": token,
        "name": spec.name,
        "price": spec.price_cents,
        "description": spec.description,
        "tags": spec.tags,
        "url": spec.url_slug,
        "preview_url": "",
        "require_shipping": "false",
        "customizable_price": "true",
    }
    resp = requests.post(url, data=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def upload_thumbnail(token: str, product_id: str, image_path: str) -> dict:
    """Upload a thumbnail/cover image to an existing Gumroad product."""
    url = f"{GUMROAD_API_BASE}/products/{product_id}"
    if not os.path.exists(image_path):
        log(f"  WARNING: Thumbnail not found: {image_path}")
        return {"success": False, "error": f"File not found: {image_path}"}
    with open(image_path, "rb") as img_file:
        files = {"preview": (os.path.basename(image_path), img_file, "image/png")}
        data = {"access_token": token}
        resp = requests.put(url, data=data, files=files, timeout=60)
        resp.raise_for_status()
        return resp.json()


def publish_product(token: str, product_id: str) -> dict:
    """Publish an unpublished product."""
    url = f"{GUMROAD_API_BASE}/products/{product_id}/enable"
    resp = requests.put(url, data={"access_token": token}, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Main ───────────────────────────────────────────────────────────────────
def main() -> None:
    dry_run = "--dry-run" in sys.argv
    target_number = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            target_number = int(arg)
        elif arg.startswith("--product"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                target_number = int(sys.argv[idx + 1])

    token = load_access_token()
    if not token and not dry_run:
        log("ERROR: Gumroad access token not found.")
        log(f"  1. Go to https://app.gumroad.com/settings/advanced#application-form")
        log(f"  2. Create an application and get an access token")
        log(f"  3. Save to {SECRETS_PATH}:")
        log(f'     {{"gumroad_access_token": "your_token_here"}}')
        sys.exit(1)

    products_to_create = PENDING_PRODUCTS
    if target_number is not None:
        products_to_create = [p for p in PENDING_PRODUCTS if p.number == target_number]
        if not products_to_create:
            log(f"ERROR: Product #{target_number} not found in pending list")
            sys.exit(1)

    log(f"{'[DRY RUN] ' if dry_run else ''}Creating {len(products_to_create)} product(s)...")

    results = []
    for spec in products_to_create:
        log(f"\n{'='*60}")
        log(f"Product #{spec.number}: {spec.name}")
        log(f"  Price: ${spec.price_cents / 100:.2f}")
        log(f"  URL slug: {spec.url_slug}")
        log(f"  Tags: {spec.tags[:60]}...")
        log(f"  Thumbnail: {'EXISTS' if os.path.exists(spec.thumbnail_path) else 'MISSING'}")
        log(f"  Cover: {'EXISTS' if os.path.exists(spec.cover_path) else 'MISSING'}")

        if dry_run:
            log("  [DRY RUN] Would create this product. Skipping.")
            results.append({"number": spec.number, "status": "dry_run", "name": spec.name})
            continue

        try:
            # Step 1: Create product
            log("  Creating product...")
            result = create_product(token, spec)
            if not result.get("success"):
                log(f"  FAILED: {result}")
                results.append({"number": spec.number, "status": "failed", "error": str(result)})
                continue

            product_data = result.get("product", {})
            product_id = product_data.get("id", "")
            product_url = product_data.get("short_url", "")
            log(f"  Created! ID: {product_id}")
            log(f"  URL: {product_url}")

            # Step 2: Upload cover image
            cover_to_use = spec.cover_path if os.path.exists(spec.cover_path) else spec.thumbnail_path
            if os.path.exists(cover_to_use):
                log(f"  Uploading thumbnail: {os.path.basename(cover_to_use)}...")
                thumb_result = upload_thumbnail(token, product_id, cover_to_use)
                if thumb_result.get("success"):
                    log("  Thumbnail uploaded!")
                else:
                    log(f"  Thumbnail upload issue: {thumb_result}")

            # Step 3: Publish
            log("  Publishing product...")
            pub_result = publish_product(token, product_id)
            if pub_result.get("success"):
                log("  Published!")
            else:
                log(f"  Publish issue: {pub_result}")

            results.append({
                "number": spec.number,
                "status": "created",
                "name": spec.name,
                "id": product_id,
                "url": product_url,
            })

        except requests.exceptions.HTTPError as e:
            log(f"  HTTP ERROR: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log(f"  Response: {e.response.text[:500]}")
            results.append({"number": spec.number, "status": "error", "error": str(e)})
        except Exception as e:
            log(f"  ERROR: {e}")
            results.append({"number": spec.number, "status": "error", "error": str(e)})

    # Save results
    log(f"\n{'='*60}")
    log("SUMMARY:")
    for r in results:
        status = r.get("status", "unknown")
        name = r.get("name", f"#{r['number']}")
        url = r.get("url", "")
        log(f"  #{r['number']} {name}: {status} {url}")

    results_path = os.path.join(OUTPUT_DIR, "gumroad-create-results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({
            "created_at": datetime.now(PYT).isoformat(),
            "results": results,
        }, f, indent=2, ensure_ascii=False)
    log(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
