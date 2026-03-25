export const metadata = {
  title: 'Contact Us',
  description: 'Contact AI Tool Compare. Get in touch with questions, suggestions, or tool submissions.',
  alternates: { canonical: '/contact/' },
};

export default function ContactPage() {
  return (
    <div className="container prose" style={{ padding: '60px 20px', maxWidth: 800, margin: '0 auto' }}>
      <h1>Contact Us</h1>

      <p>
        We would love to hear from you. Whether you have a question about our comparisons, want to suggest a tool
        for review, or have feedback about our site, do not hesitate to reach out.
      </p>

      <h2>Email</h2>
      <p>
        The best way to reach us is by email:{' '}
        <a href="mailto:contact@ai-tool-compare.com">contact@ai-tool-compare.com</a>
      </p>

      <h2>What You Can Contact Us About</h2>
      <ul>
        <li><strong>Tool Submissions:</strong> Want your AI tool featured on our site? Let us know.</li>
        <li><strong>Data Corrections:</strong> Found incorrect information in one of our comparisons? We will fix it promptly.</li>
        <li><strong>Partnership Inquiries:</strong> Interested in working with us? We are open to collaborations.</li>
        <li><strong>General Feedback:</strong> Suggestions for improving the site are always welcome.</li>
      </ul>

      <h2>Response Time</h2>
      <p>We aim to respond to all inquiries within 48 hours.</p>
    </div>
  );
}
