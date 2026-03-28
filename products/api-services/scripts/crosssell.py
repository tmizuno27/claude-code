import os

BASE = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\products\api-services"

cross_sell = {
    "01-qr-code-api": [
        ("PDF Generator API", "Generate PDFs with embedded QR codes", "22-pdf-generator-api"),
        ("Screenshot API", "Capture QR code landing pages for previews", "04-screenshot-api"),
        ("URL Shortener API", "Shorten URLs before encoding in QR codes", "07-url-shortener-api"),
        ("Placeholder Image API", "Generate placeholder images for prototypes", "23-placeholder-image-api"),
    ],
    "02-email-validation-api": [
        ("IP Geolocation API", "Detect signup fraud by geo-locating user IPs", "06-ip-geolocation-api"),
        ("Company Data API", "Enrich validated emails with company info", "20-company-data-api"),
        ("Hash & Encoding API", "Hash emails for secure storage and deduplication", "09-hash-encoding-api"),
        ("Text Analysis API", "Analyze email content for spam/sentiment", "05-text-analysis-api"),
    ],
    "03-link-preview-api": [
        ("Screenshot API", "Capture full-page screenshots alongside OG data", "04-screenshot-api"),
        ("SEO Analyzer API", "Deep SEO audit after extracting metadata", "14-seo-analyzer-api"),
        ("WHOIS Domain API", "Look up domain ownership for extracted URLs", "16-whois-domain-api"),
        ("Markdown Converter API", "Convert extracted content to Markdown", "24-markdown-converter-api"),
    ],
    "04-screenshot-api": [
        ("Link Preview API", "Extract OG metadata alongside screenshots", "03-link-preview-api"),
        ("SEO Analyzer API", "Audit the page you are screenshotting", "14-seo-analyzer-api"),
        ("PDF Generator API", "Convert screenshots to PDF reports", "22-pdf-generator-api"),
        ("QR Code API", "Generate QR codes linking to screenshot URLs", "01-qr-code-api"),
    ],
    "05-text-analysis-api": [
        ("AI Text API", "Generate text then analyze its quality", "11-ai-text-api"),
        ("AI Translation API", "Translate then analyze sentiment per language", "18-ai-translate-api"),
        ("SEO Analyzer API", "Combine content analysis with technical SEO", "14-seo-analyzer-api"),
        ("News Aggregator API", "Analyze sentiment of news headlines", "17-news-aggregator-api"),
    ],
    "06-ip-geolocation-api": [
        ("Email Validation API", "Combine IP geo with email validation for fraud prevention", "02-email-validation-api"),
        ("Currency Exchange API", "Auto-detect user currency from IP location", "10-currency-exchange-api"),
        ("Weather API", "Get weather for the detected location", "15-weather-api"),
        ("Company Data API", "Enrich IP data with company information", "20-company-data-api"),
    ],
    "07-url-shortener-api": [
        ("QR Code API", "Generate QR codes for shortened URLs", "01-qr-code-api"),
        ("Link Preview API", "Extract metadata before shortening", "03-link-preview-api"),
        ("IP Geolocation API", "Geo-locate users who click short links", "06-ip-geolocation-api"),
        ("Screenshot API", "Capture thumbnails for link previews", "04-screenshot-api"),
    ],
    "08-json-formatter-api": [
        ("Hash & Encoding API", "Encode/hash JSON data for secure storage", "09-hash-encoding-api"),
        ("Markdown Converter API", "Convert JSON to readable Markdown docs", "24-markdown-converter-api"),
        ("PDF Generator API", "Generate PDF reports from JSON data", "22-pdf-generator-api"),
        ("Text Analysis API", "Analyze text fields within JSON payloads", "05-text-analysis-api"),
    ],
    "09-hash-encoding-api": [
        ("Email Validation API", "Validate then hash emails for secure storage", "02-email-validation-api"),
        ("JSON Formatter API", "Format and validate data before hashing", "08-json-formatter-api"),
        ("PDF Generator API", "Generate PDF certificates with hash verification", "22-pdf-generator-api"),
        ("IP Geolocation API", "Hash IP addresses for privacy-compliant logging", "06-ip-geolocation-api"),
    ],
    "10-currency-exchange-api": [
        ("IP Geolocation API", "Auto-detect user currency from IP location", "06-ip-geolocation-api"),
        ("Crypto Data API", "Combine fiat and crypto rates in one dashboard", "13-crypto-data-api"),
        ("Company Data API", "Enrich company data with local currency info", "20-company-data-api"),
        ("PDF Generator API", "Generate multi-currency invoices", "22-pdf-generator-api"),
    ],
    "11-ai-text-api": [
        ("AI Translation API", "Generate text then translate to any language", "18-ai-translate-api"),
        ("Text Analysis API", "Analyze AI-generated text for quality", "05-text-analysis-api"),
        ("SEO Analyzer API", "Generate SEO content then audit the page", "14-seo-analyzer-api"),
        ("Markdown Converter API", "Convert AI output to HTML or Markdown", "24-markdown-converter-api"),
    ],
    "12-social-video-api": [
        ("Screenshot API", "Capture video page thumbnails", "04-screenshot-api"),
        ("Link Preview API", "Extract video metadata and OG tags", "03-link-preview-api"),
        ("Trends API", "Find trending videos to download", "19-trends-api"),
        ("AI Text API", "Generate descriptions for downloaded videos", "11-ai-text-api"),
    ],
    "13-crypto-data-api": [
        ("Currency Exchange API", "Combine crypto + fiat rates for full coverage", "10-currency-exchange-api"),
        ("Trends API", "Track which coins are trending on social media", "19-trends-api"),
        ("News Aggregator API", "Get crypto news alongside price data", "17-news-aggregator-api"),
        ("AI Text API", "Generate market analysis from crypto data", "11-ai-text-api"),
    ],
    "14-seo-analyzer-api": [
        ("Link Preview API", "Extract OG tags for SEO preview validation", "03-link-preview-api"),
        ("Screenshot API", "Visual SEO audit with page screenshots", "04-screenshot-api"),
        ("WHOIS Domain API", "Check domain age and registration for SEO context", "16-whois-domain-api"),
        ("WP Internal Link API", "Optimize internal links after SEO audit", "21-wp-internal-link-api"),
    ],
    "15-weather-api": [
        ("IP Geolocation API", "Auto-detect user location for weather lookup", "06-ip-geolocation-api"),
        ("AI Text API", "Generate weather-based content or notifications", "11-ai-text-api"),
        ("News Aggregator API", "Combine weather with local news", "17-news-aggregator-api"),
        ("Currency Exchange API", "Travel planning: weather + currency info", "10-currency-exchange-api"),
    ],
    "16-whois-domain-api": [
        ("SEO Analyzer API", "Full SEO audit after domain lookup", "14-seo-analyzer-api"),
        ("Link Preview API", "Extract metadata for discovered domains", "03-link-preview-api"),
        ("Screenshot API", "Capture screenshots of looked-up domains", "04-screenshot-api"),
        ("Email Validation API", "Validate emails on discovered domains", "02-email-validation-api"),
    ],
    "17-news-aggregator-api": [
        ("AI Text API", "Summarize or rewrite news articles", "11-ai-text-api"),
        ("AI Translation API", "Translate news to multiple languages", "18-ai-translate-api"),
        ("Text Analysis API", "Sentiment analysis on news headlines", "05-text-analysis-api"),
        ("Trends API", "Cross-reference news with trending topics", "19-trends-api"),
    ],
    "18-ai-translate-api": [
        ("AI Text API", "Generate content then translate to any language", "11-ai-text-api"),
        ("Text Analysis API", "Analyze sentiment in the source language", "05-text-analysis-api"),
        ("News Aggregator API", "Translate international news headlines", "17-news-aggregator-api"),
        ("PDF Generator API", "Generate multilingual PDF documents", "22-pdf-generator-api"),
    ],
    "19-trends-api": [
        ("News Aggregator API", "Get full articles for trending topics", "17-news-aggregator-api"),
        ("AI Text API", "Generate content about trending topics", "11-ai-text-api"),
        ("Social Video API", "Find trending videos on social platforms", "12-social-video-api"),
        ("Crypto Data API", "Track trending cryptocurrencies", "13-crypto-data-api"),
    ],
    "20-company-data-api": [
        ("Email Validation API", "Validate company email addresses", "02-email-validation-api"),
        ("IP Geolocation API", "Geo-locate company headquarters", "06-ip-geolocation-api"),
        ("WHOIS Domain API", "Look up company domain registration", "16-whois-domain-api"),
        ("Screenshot API", "Capture company website screenshots", "04-screenshot-api"),
    ],
    "21-wp-internal-link-api": [
        ("SEO Analyzer API", "Full SEO audit alongside link optimization", "14-seo-analyzer-api"),
        ("Link Preview API", "Extract metadata for link context", "03-link-preview-api"),
        ("Text Analysis API", "Analyze content for keyword relevance", "05-text-analysis-api"),
        ("AI Text API", "Generate anchor text suggestions", "11-ai-text-api"),
    ],
    "22-pdf-generator-api": [
        ("QR Code API", "Embed QR codes in generated PDFs", "01-qr-code-api"),
        ("Markdown Converter API", "Convert Markdown to HTML, then to PDF", "24-markdown-converter-api"),
        ("Screenshot API", "Include page screenshots in PDF reports", "04-screenshot-api"),
        ("Currency Exchange API", "Multi-currency invoices", "10-currency-exchange-api"),
    ],
    "23-placeholder-image-api": [
        ("QR Code API", "Generate QR codes for prototyping", "01-qr-code-api"),
        ("Screenshot API", "Capture real screenshots to replace placeholders", "04-screenshot-api"),
        ("PDF Generator API", "Include placeholder images in PDF mockups", "22-pdf-generator-api"),
        ("JSON Formatter API", "Mock API responses with placeholder data", "08-json-formatter-api"),
    ],
    "24-markdown-converter-api": [
        ("PDF Generator API", "Convert Markdown to HTML to PDF pipeline", "22-pdf-generator-api"),
        ("AI Text API", "Generate content in Markdown format", "11-ai-text-api"),
        ("JSON Formatter API", "Convert JSON data to Markdown tables", "08-json-formatter-api"),
        ("Text Analysis API", "Analyze Markdown content for readability", "05-text-analysis-api"),
    ],
}

for api_dir, related in cross_sell.items():
    readme_path = os.path.join(BASE, api_dir, "README.md")
    if not os.path.exists(readme_path):
        print(f"SKIP: {readme_path} not found")
        continue

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Also From This Publisher" in content or "Related APIs" in content:
        print(f"SKIP: {api_dir} already has cross-sell")
        continue

    section = "\n## Also From This Publisher\n\n"
    section += "Build powerful workflows by combining APIs:\n\n"
    section += "| API | Why Combine? |\n|-----|-------------|\n"
    for name, reason, _ in related:
        section += f"| **{name}** | {reason} |\n"
    section += "\n> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).\n"

    if "## Keywords" in content:
        content = content.replace("## Keywords", section + "\n## Keywords")
    else:
        content += section

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK: {api_dir}")

print("\nDone!")
