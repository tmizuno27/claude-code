# Google Maps Scraper

Scrape Google Maps business listings — name, address, phone, website, ratings, reviews, and coordinates.

## Features

- **Search mode**: Search by query (e.g., "restaurants in Tokyo")
- **Direct URL mode**: Scrape specific Google Maps place URLs
- **Multi-language**: Supports any Google Maps language
- **Review details**: Optionally fetch detailed place info
- **Geo coordinates**: Latitude/longitude for each listing

## Input

### Search Mode
```json
{
  "searchQuery": "coffee shops in New York",
  "maxResults": 20,
  "includeReviews": true,
  "language": "en"
}
```

### Direct URL Mode
```json
{
  "placeUrls": [
    "https://www.google.com/maps/place/..."
  ]
}
```

## Output

| Field | Description |
|-------|-------------|
| name | Business name |
| address | Street address |
| phone | Phone number |
| website | Business website URL |
| rating | Average star rating (1-5) |
| reviewCount | Total number of reviews |
| category | Business category |
| latitude | GPS latitude |
| longitude | GPS longitude |
| openingHours | Business hours |

## Use Cases

- Local business lead generation
- Competitor mapping and analysis
- Location-based market research
- Business directory building
