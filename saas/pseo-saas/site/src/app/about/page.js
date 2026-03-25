export const metadata = {
  title: 'About Us',
  description: 'About AI Tool Compare — our mission to help you find the best AI tools through data-driven comparisons.',
  alternates: { canonical: '/about/' },
};

export default function AboutPage() {
  return (
    <div className="container prose" style={{ padding: '60px 20px', maxWidth: 800, margin: '0 auto' }}>
      <h1>About AI Tool Compare</h1>

      <h2>Our Mission</h2>
      <p>
        The AI tool landscape is growing at an unprecedented pace. With hundreds of new tools launching every month,
        finding the right solution for your needs can be overwhelming. AI Tool Compare was built to solve this problem.
      </p>
      <p>
        We provide detailed, data-driven comparisons of AI and SaaS tools across every major category — from AI writing
        assistants and image generators to coding tools, chatbots, and automation platforms. Our goal is simple:
        help you make confident, informed decisions.
      </p>

      <h2>How We Compare</h2>
      <p>Every comparison on our site is built on a structured methodology:</p>
      <ul>
        <li><strong>Feature Analysis:</strong> We catalog each tool&apos;s capabilities and compare them side by side.</li>
        <li><strong>Pricing Breakdown:</strong> We analyze starting prices, free plans, and overall value for money.</li>
        <li><strong>User Ratings:</strong> We aggregate user satisfaction scores across multiple dimensions including ease of use and value.</li>
        <li><strong>Use Case Matching:</strong> We identify which tool fits best for different types of users and workflows.</li>
        <li><strong>Objective Verdict:</strong> We deliver a clear recommendation based on the data, not opinions.</li>
      </ul>

      <h2>Our Numbers</h2>
      <ul>
        <li><strong>329+</strong> AI tools analyzed</li>
        <li><strong>4,700+</strong> side-by-side comparisons</li>
        <li><strong>20+</strong> categories covered</li>
      </ul>

      <h2>Affiliate Disclosure</h2>
      <p>
        Some links on our website are affiliate links. This means we may earn a commission if you click through and
        make a purchase or sign up for a service. This comes at no extra cost to you and helps us keep the site running.
        Importantly, our comparisons and ratings are never influenced by affiliate partnerships — the data speaks for itself.
      </p>

      <h2>Contact</h2>
      <p>
        Have questions, suggestions, or want to submit a tool for review? Reach out to us at{' '}
        <a href="mailto:contact@ai-tool-compare.com">contact@ai-tool-compare.com</a>.
      </p>
    </div>
  );
}
