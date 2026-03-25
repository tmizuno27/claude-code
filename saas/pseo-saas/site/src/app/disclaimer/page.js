export const metadata = {
  title: 'Affiliate Disclaimer',
  description: 'Affiliate disclosure for AI Tool Compare. Learn how we earn revenue through affiliate partnerships.',
  alternates: { canonical: '/disclaimer/' },
};

export default function DisclaimerPage() {
  return (
    <div className="container prose" style={{ padding: '60px 20px', maxWidth: 800, margin: '0 auto' }}>
      <h1>Affiliate Disclaimer</h1>
      <p><strong>Last updated:</strong> March 25, 2026</p>

      <h2>Disclosure</h2>
      <p>
        AI Tool Compare is a participant in various affiliate programs. This means that some of the links on our
        website are affiliate links. When you click on these links and make a purchase or sign up for a service,
        we may receive a commission at no additional cost to you.
      </p>

      <h2>Editorial Independence</h2>
      <p>
        Our comparisons, ratings, and verdicts are based on objective criteria including features, pricing, user
        ratings, and overall value. Affiliate partnerships do not influence our editorial content or tool rankings.
        We compare tools using the same methodology regardless of whether we have an affiliate relationship.
      </p>

      <h2>How We Earn</h2>
      <p>
        We earn revenue through affiliate commissions when visitors click affiliate links and subsequently purchase
        products or services. This revenue helps us maintain the website, research new tools, and provide free
        comparison content to our users.
      </p>

      <h2>Your Trust Matters</h2>
      <p>
        We believe transparency is essential. If you have any concerns about our affiliate relationships or how
        they might affect our content, please <a href="/contact/">contact us</a>.
      </p>
    </div>
  );
}
