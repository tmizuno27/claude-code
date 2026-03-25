# Amazon Product Scraper

Scrape Amazon product details or search results. Extracts price, ratings, reviews, features, BSR, and more.

## Features

- **Product mode**: Scrape full details from product URLs
- **Search mode**: Search by keyword and get top results
- **Multi-marketplace**: Supports amazon.com, .co.uk, .de, .co.jp, etc.
- **Anti-detection**: Random delays and browser-like headers

## Input

### Product Mode
```json
{
  "mode": "product",
  "urls": [
    "https://www.amazon.com/dp/B0XXXXXXXXX"
  ]
}
```

### Search Mode
```json
{
  "mode": "search",
  "keywords": "wireless bluetooth headphones",
  "marketplace": "com",
  "maxResults": 20
}
```

## Output

### Product
| Field | Description |
|-------|-------------|
| asin | Amazon Standard Identification Number |
| title | Product title |
| brand | Brand name |
| price | Current price |
| currency | Price currency symbol |
| rating | Average star rating (1-5) |
| reviewCount | Total number of reviews |
| availability | Stock status |
| features | Bullet point features |
| bestSellersRank | BSR rank and category |
| mainImage | Main product image URL |

## Use Cases

- Price monitoring and comparison
- Market research and competitor analysis
- Product catalog building
- Review sentiment tracking
