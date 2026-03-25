# Product Description Writer Prompt

## Objective
Generate marketplace-optimized product descriptions for digital products on Gumroad, Etsy, Chrome Web Store, VS Code Marketplace, or any platform.

## Required Context / Inputs
- Product name and type
- Key features list
- Target platform
- Target audience
- Price point

## Prompt

```
Write a complete marketplace listing for my digital product.

**Product Details:**
- Name: [PRODUCT NAME]
- Type: [template / extension / API / guide / tool]
- Platform: [Gumroad / Etsy / Chrome Web Store / VS Code Marketplace / RapidAPI]
- Price: [PRICE]
- Target Audience: [WHO IS THIS FOR]
- Key Features: [LIST 5-10 FEATURES]
- Problem It Solves: [WHAT PAIN POINT DOES THIS ADDRESS]

**Generate the following:**

1. **Title** (under 80 characters):
   - Include the primary benefit
   - Use power words (Ultimate, Complete, Pro, Essential)
   - Include a number if applicable ("50+ Templates", "20 Prompts")

2. **Subtitle/Tagline** (under 120 characters):
   - Complement the title, don't repeat it
   - Focus on the outcome the buyer gets

3. **Description** (300-500 words):
   - Hook: Start with the problem the buyer faces
   - Solution: Introduce your product as the answer
   - Features: Bullet-pointed list with benefit-focused language
   - Social proof placeholder: "[X] customers already using this"
   - Call to action: Why buy now
   - Formatting: Use emoji sparingly, headers for scannability

4. **Tags/Keywords** (10-15):
   - Mix of broad and specific
   - Include the product category, use case, and platform

5. **FAQ Section** (3-5 questions):
   - "What's included?"
   - "Is this compatible with [X]?"
   - "Do I get updates?"
   - Platform-specific questions

6. **SEO Meta Description** (150-160 characters):
   - For platforms that support it

Output format: Save as listings/[product-slug]-listing.md
```

## Expected Output
- `listings/[product-slug]-listing.md` — complete listing copy

## Example Usage

```
Product Details:
- Name: Freelance Business OS
- Type: Notion template
- Platform: Gumroad
- Price: $9.99
- Target Audience: Freelancers managing clients, projects, and finances
- Key Features: Client CRM, project tracker, invoice generator, time tracker, revenue dashboard
- Problem It Solves: Freelancers juggling spreadsheets, sticky notes, and 5 different apps to manage their business
```

## Tips
- Tailor the tone to the platform (Gumroad = casual/direct, Chrome Web Store = technical/concise)
- A/B test descriptions by generating 2-3 variants
- Include specific numbers (saves 5 hours/week, 50+ templates) over vague claims
