# Email Sequence Writer Prompt

## Objective
Generate a complete email drip sequence for product launches, lead nurturing, or customer onboarding.

## Required Context / Inputs
- Product or offer details
- Target audience
- Sequence purpose (launch, nurture, onboard)
- Number of emails needed

## Prompt

```
Create a complete email sequence.

**Sequence Details:**
- Purpose: [product launch / lead nurture / onboarding / re-engagement]
- Product/Offer: [WHAT YOU'RE PROMOTING]
- Target audience: [WHO RECEIVES THESE]
- Sequence length: [NUMBER] emails over [TIMEFRAME]
- CTA: [WHAT ACTION DO YOU WANT THEM TO TAKE]

**For each email, generate:**
1. Subject line (under 50 chars, curiosity or benefit-driven)
2. Preview text (40-90 chars)
3. Body copy (200-400 words)
4. CTA button text
5. Send timing (Day X, time recommendation)

**Sequence Structure:**

For a product launch (7 emails):
- Email 1 (Day -3): Problem awareness — paint the pain
- Email 2 (Day -1): Solution teaser — hint at what's coming
- Email 3 (Day 0): Launch announcement — full pitch + early bird offer
- Email 4 (Day 1): Social proof / testimonials
- Email 5 (Day 3): FAQ / objection handling
- Email 6 (Day 5): Scarcity — price going up / bonus expiring
- Email 7 (Day 7): Last chance — final push

For a nurture sequence (5 emails):
- Email 1: Welcome + quick win (immediate value)
- Email 2: Deeper insight on topic (build authority)
- Email 3: Case study / story (build trust)
- Email 4: Common mistake to avoid (show expertise)
- Email 5: Soft pitch (transition to offer)

**Tone:** [conversational / professional / urgent / educational]

**Output:**
- Save to outputs/emails/[sequence-name]/
- One file per email: 01-subject-slug.md, 02-subject-slug.md, etc.
- Include a sequence-overview.md with the full timeline

Sequence name: [YOUR SEQUENCE NAME]
```

## Expected Output
- `outputs/emails/[sequence-name]/` directory with individual email files
- `sequence-overview.md` with timeline and strategy notes

## Tips
- Subject lines make or break open rates — generate 3 options per email and A/B test
- Each email should be valuable standalone, even if they skip the CTA
- Use the PS line for a secondary CTA or personal touch
