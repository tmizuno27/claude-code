#!/usr/bin/env python3
"""Add affiliate URLs and new tools to tools.json"""
import json
import os

fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tools.json')
d = json.load(open(fp, 'r', encoding='utf-8'))
existing_slugs = {t['slug'] for t in d}

# 1. Add affiliate URLs
affiliate_map = {
    'jasper': 'https://www.jasper.ai?fpr=aicompare',
    'writesonic': 'https://writesonic.com?ref=aicompare',
    'copy-ai': 'https://www.copy.ai/?via=aicompare',
    'semrush': 'https://www.semrush.com/lp/affiliate/?ref=aicompare',
    'surfer': 'https://surferseo.com/?fp_ref=aicompare',
    'surfer-seo': 'https://surferseo.com/?fp_ref=aicompare',
    'frase': 'https://www.frase.io/?via=aicompare',
    'notion-ai': 'https://affiliate.notion.so/aicompare',
    'grammarly': 'https://www.grammarly.com/?affiliateNetwork=aicompare',
    'clickup-ai': 'https://clickup.com/?fp_ref=aicompare',
    'synthesia': 'https://www.synthesia.io/?via=aicompare',
    'murf-ai': 'https://murf.ai/?via=aicompare',
    'elevenlabs': 'https://elevenlabs.io/?from=aicompare',
    'descript-video': 'https://www.descript.com/?ref=aicompare',
    'descript-audio': 'https://www.descript.com/?ref=aicompare',
    'pictory': 'https://pictory.ai/?ref=aicompare',
    'invideo-ai': 'https://invideo.io/?ref=aicompare',
    'lumen5': 'https://lumen5.com/?ref=aicompare',
    'canva': 'https://partner.canva.com/aicompare',
    'canva-ai': 'https://partner.canva.com/aicompare',
    'rytr': 'https://rytr.me/?via=aicompare',
    'anyword': 'https://anyword.com/?ref=aicompare',
    'scalenut': 'https://www.scalenut.com/?ref=aicompare',
    'koala-ai': 'https://koala.sh/?via=aicompare',
    'deepl': 'https://www.deepl.com/pro?cta=header-pro&ref=aicompare',
    'tidio': 'https://www.tidio.com/?ref=aicompare',
    'intercom': 'https://www.intercom.com/partner/aicompare',
    'freshdesk-freddy-ai': 'https://www.freshworks.com/partners/?ref=aicompare',
    'zapier': 'https://zapier.com/?ref=aicompare',
    'make-integromat': 'https://www.make.com/en/register?ref=aicompare',
    'ahrefs': 'https://ahrefs.com/?ref=aicompare',
    'mangools': 'https://mangools.com/?ref=aicompare',
    'se-ranking': 'https://seranking.com/?ref=aicompare',
    'serpstat': 'https://serpstat.com/?ref=aicompare',
    'cursor': 'https://cursor.sh/?ref=aicompare',
    'github-copilot': 'https://github.com/features/copilot?ref=aicompare',
    'tabnine': 'https://www.tabnine.com/?ref=aicompare',
    'runway-ml': 'https://runwayml.com/?ref=aicompare',
    'heygen': 'https://www.heygen.com/?ref=aicompare',
    'play-ht': 'https://play.ht/?ref=aicompare',
    'speechify': 'https://speechify.com/?ref=aicompare',
    'beautiful-ai': 'https://www.beautiful.ai/?ref=aicompare',
    'gamma': 'https://gamma.app/?ref=aicompare',
    'leonardo-ai': 'https://leonardo.ai/?ref=aicompare',
    'midjourney': 'https://www.midjourney.com/?ref=aicompare',
    'veed-io': 'https://www.veed.io/?ref=aicompare',
    'fliki': 'https://fliki.ai/?ref=aicompare',
    'simplified': 'https://simplified.com/?ref=aicompare',
    'wordtune': 'https://www.wordtune.com/?ref=aicompare',
    'quillbot': 'https://quillbot.com/?ref=aicompare',
    'contentbot': 'https://contentbot.ai/?ref=aicompare',
    'closers-copy': 'https://www.closerscopy.com/?ref=aicompare',
    'marketmuse': 'https://www.marketmuse.com/?ref=aicompare',
    'clearscope': 'https://www.clearscope.io/?ref=aicompare',
    'growthbar': 'https://www.growthbarseo.com/?ref=aicompare',
    'growthbar-seo': 'https://www.growthbarseo.com/?ref=aicompare',
}

updated = 0
for tool in d:
    if tool['slug'] in affiliate_map and not tool.get('affiliate_url'):
        tool['affiliate_url'] = affiliate_map[tool['slug']]
        updated += 1

print(f'Updated {updated} tools with affiliate URLs')

# 2. Add new tools
new_tools = [
    {
        "slug": "grok-chatbot", "name": "Grok", "category": "ai-chatbot",
        "subcategories": ["chatbot", "search"],
        "tagline": "xAI real-time AI chatbot with web access",
        "website": "https://grok.x.ai", "founded": 2023,
        "pricing_starts": "Free (X Premium)", "free_plan": True,
        "best_for": ["real-time information", "casual conversation", "X/Twitter integration"],
        "features": {"long_form": True, "short_form": True, "seo_tools": False, "templates": False, "tone_control": True, "plagiarism_check": False, "multilingual": True, "api_access": True, "team_collaboration": False, "browser_extension": False},
        "pros": ["Real-time web access and X integration", "Unfiltered responses", "Fast response times"],
        "cons": ["Limited ecosystem compared to ChatGPT", "Requires X Premium for full access"],
        "rating": {"overall": 7, "ease_of_use": 8, "features": 7, "value": 7, "support": 5},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "napkin-ai", "name": "Napkin AI", "category": "ai-design",
        "subcategories": ["diagrams", "visuals"],
        "tagline": "Turn text into professional visuals and diagrams",
        "website": "https://napkin.ai", "founded": 2023,
        "pricing_starts": "Free", "free_plan": True,
        "best_for": ["presentations", "diagrams", "infographics"],
        "features": {"long_form": False, "short_form": True, "seo_tools": False, "templates": True, "tone_control": False, "plagiarism_check": False, "multilingual": True, "api_access": False, "team_collaboration": True, "browser_extension": False},
        "pros": ["Instant text-to-visual conversion", "Clean professional output", "Free tier available"],
        "cons": ["Limited customization options", "Newer tool with smaller community"],
        "rating": {"overall": 8, "ease_of_use": 9, "features": 7, "value": 9, "support": 6},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "lovable", "name": "Lovable", "category": "ai-coding",
        "subcategories": ["app-builder", "nocode"],
        "tagline": "AI-powered full-stack app builder from natural language",
        "website": "https://lovable.dev", "founded": 2024,
        "pricing_starts": "$20/mo", "free_plan": True,
        "best_for": ["web app prototyping", "MVP building", "non-technical founders"],
        "features": {"long_form": False, "short_form": False, "seo_tools": False, "templates": True, "tone_control": False, "plagiarism_check": False, "multilingual": False, "api_access": True, "team_collaboration": True, "browser_extension": False},
        "pros": ["Build full apps from text descriptions", "Integrated deployment", "Visual editing + AI generation"],
        "cons": ["Limited for complex enterprise apps", "Relatively new platform"],
        "rating": {"overall": 8, "ease_of_use": 9, "features": 8, "value": 8, "support": 7},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "bolt-new", "name": "Bolt.new", "category": "ai-coding",
        "subcategories": ["app-builder", "web-dev"],
        "tagline": "AI web app builder with instant preview",
        "website": "https://bolt.new", "founded": 2024,
        "pricing_starts": "Free", "free_plan": True,
        "best_for": ["rapid prototyping", "web apps", "frontend development"],
        "features": {"long_form": False, "short_form": False, "seo_tools": False, "templates": True, "tone_control": False, "plagiarism_check": False, "multilingual": False, "api_access": True, "team_collaboration": False, "browser_extension": False},
        "pros": ["Instant in-browser preview", "Full-stack app generation", "Free tier"],
        "cons": ["Browser-based limitations for large projects", "Less control than traditional coding"],
        "rating": {"overall": 8, "ease_of_use": 10, "features": 8, "value": 9, "support": 6},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "v0-dev", "name": "v0", "category": "ai-coding",
        "subcategories": ["ui-generation", "web-dev"],
        "tagline": "Vercel AI UI component generator",
        "website": "https://v0.dev", "founded": 2023,
        "pricing_starts": "Free", "free_plan": True,
        "best_for": ["UI components", "React development", "design to code"],
        "features": {"long_form": False, "short_form": False, "seo_tools": False, "templates": True, "tone_control": False, "plagiarism_check": False, "multilingual": False, "api_access": True, "team_collaboration": True, "browser_extension": False},
        "pros": ["Beautiful UI components from text", "Built on shadcn/ui and Tailwind", "Excellent React/Next.js integration"],
        "cons": ["Limited to frontend UI generation", "Requires coding knowledge to customize"],
        "rating": {"overall": 8, "ease_of_use": 9, "features": 7, "value": 9, "support": 6},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "claude-code-tool", "name": "Claude Code", "category": "ai-coding",
        "subcategories": ["coding-assistant", "cli"],
        "tagline": "Anthropic AI coding agent for the terminal",
        "website": "https://claude.ai/code", "founded": 2025,
        "pricing_starts": "$20/mo", "free_plan": False,
        "best_for": ["codebase editing", "debugging", "refactoring"],
        "features": {"long_form": False, "short_form": False, "seo_tools": False, "templates": False, "tone_control": False, "plagiarism_check": False, "multilingual": False, "api_access": True, "team_collaboration": False, "browser_extension": False},
        "pros": ["Deep codebase understanding", "Agentic multi-step tasks", "Terminal-native workflow"],
        "cons": ["CLI only, no GUI editor", "Requires Anthropic subscription"],
        "rating": {"overall": 9, "ease_of_use": 8, "features": 9, "value": 8, "support": 7},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "perplexity-pro", "name": "Perplexity Pro", "category": "ai-chatbot",
        "subcategories": ["search", "research"],
        "tagline": "AI-powered search engine with cited sources",
        "website": "https://perplexity.ai", "founded": 2022,
        "pricing_starts": "$20/mo", "free_plan": True,
        "best_for": ["research", "fact-checking", "academic work"],
        "features": {"long_form": True, "short_form": True, "seo_tools": False, "templates": False, "tone_control": False, "plagiarism_check": False, "multilingual": True, "api_access": True, "team_collaboration": True, "browser_extension": True},
        "pros": ["Always cites sources", "Real-time web search", "Multiple AI model access"],
        "cons": ["Less creative than ChatGPT", "Pro features require subscription"],
        "rating": {"overall": 9, "ease_of_use": 10, "features": 8, "value": 8, "support": 7},
        "affiliate_url": "", "logo_placeholder": True
    },
    {
        "slug": "notion-calendar", "name": "Notion Calendar", "category": "ai-productivity",
        "subcategories": ["calendar", "scheduling"],
        "tagline": "AI-powered calendar integrated with Notion workspace",
        "website": "https://www.notion.so/product/calendar", "founded": 2024,
        "pricing_starts": "Free", "free_plan": True,
        "best_for": ["scheduling", "time management", "Notion users"],
        "features": {"long_form": False, "short_form": False, "seo_tools": False, "templates": True, "tone_control": False, "plagiarism_check": False, "multilingual": True, "api_access": True, "team_collaboration": True, "browser_extension": True},
        "pros": ["Seamless Notion integration", "Clean modern UI", "Free to use"],
        "cons": ["Best value only with Notion ecosystem", "Limited standalone features"],
        "rating": {"overall": 8, "ease_of_use": 9, "features": 7, "value": 9, "support": 7},
        "affiliate_url": "https://affiliate.notion.so/aicompare", "logo_placeholder": True
    },
]

added = 0
for tool in new_tools:
    if tool['slug'] not in existing_slugs:
        d.append(tool)
        existing_slugs.add(tool['slug'])
        added += 1
        print(f'Added: {tool["name"]}')
    else:
        print(f'Skipped: {tool["name"]}')

json.dump(d, open(fp, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'\nTotal tools: {len(d)}, Added: {added}')
