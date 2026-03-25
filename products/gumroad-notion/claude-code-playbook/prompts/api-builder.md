# API Builder Prompt

## Objective
Design and build a complete REST API — from specification to deployed code — ready to host on Cloudflare Workers, Vercel, or any serverless platform.

## Required Context / Inputs
- API concept (what data/service it provides)
- Target platform (Cloudflare Workers, Vercel, AWS Lambda)
- Monetization plan (free, freemium, paid via RapidAPI)

## Prompt

```
Build a complete REST API from scratch.

**API Specification:**
- Name: [API NAME]
- Purpose: [What does this API do? What problem does it solve?]
- Target users: [developers, businesses, data analysts]
- Platform: [Cloudflare Workers / Vercel Serverless / Express.js]
- Monetization: [free / freemium via RapidAPI / paid]

**Generate the following:**

1. **API Design**:
   - Define endpoints (method, path, parameters, response format)
   - Design consistent JSON response envelope:
     ```json
     { "success": true, "data": {...}, "error": null }
     ```
   - Define rate limiting rules
   - Define authentication method (API key, none, OAuth)

2. **Implementation**:
   - Write the complete API code for the target platform
   - Include input validation on all parameters
   - Include proper error handling with meaningful error messages
   - Add CORS headers
   - Add request logging

3. **Testing**:
   - Generate test cases (happy path + edge cases)
   - Create a test script using curl or fetch
   - Include example requests and expected responses

4. **Documentation**:
   - README.md with setup instructions
   - API reference with all endpoints documented
   - Example code snippets (JavaScript, Python, curl)

5. **Deployment**:
   - Platform-specific config (wrangler.toml for CF Workers, vercel.json, etc.)
   - Environment variable setup instructions
   - Deployment commands

6. **Marketplace Listing** (if RapidAPI):
   - API title and description
   - Pricing tiers (Basic free, Pro, Ultra)
   - Tags and categories

**Output:**
- Save all files to products/api-services/[api-slug]/
- Include: src/, tests/, README.md, deployment config

API concept: [DESCRIBE YOUR API IDEA]
```

## Expected Output
- Complete API project in `products/api-services/[api-slug]/`
- Working code, tests, documentation, and deployment config

## Example Usage

```
API Specification:
- Name: SEO Meta Analyzer
- Purpose: Analyze any webpage and return SEO metadata (title, description, headers, Open Graph, schema markup)
- Target users: SEO tools, developers building link previews
- Platform: Cloudflare Workers
- Monetization: Freemium via RapidAPI (100 free requests/month, $9.99/mo for 10,000)
```

## Tips
- Start with a simple, focused API (one clear use case) rather than a Swiss army knife
- Free tier attracts users; paid tier monetizes power users
- APIs with no external dependencies (pure computation, scraping, transformation) are cheapest to run
- Cloudflare Workers free tier = 100,000 requests/day, making it ideal for bootstrapped API businesses
