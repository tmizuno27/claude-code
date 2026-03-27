import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy - Chrome Extensions by miccho27',
  description: 'Privacy policy for Chrome extensions published by miccho27. No data collection, no tracking, no personal information stored.',
  robots: { index: true, follow: true },
};

export default function ChromePrivacyPage() {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem 1rem', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif', color: '#1d1d1f', lineHeight: 1.7 }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Privacy Policy</h1>
      <p style={{ color: '#6e6e73', marginBottom: '2rem' }}>Chrome Extensions by miccho27</p>
      <p style={{ color: '#6e6e73', fontSize: '0.875rem', marginBottom: '2rem' }}>Last updated: March 27, 2026</p>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>1. Overview</h2>
        <p>This privacy policy applies to all Chrome extensions published by miccho27 on the Chrome Web Store. We are committed to protecting your privacy and being transparent about our data practices.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>2. Data Collection</h2>
        <p style={{ fontWeight: 600, color: '#1d8348', marginBottom: '0.5rem' }}>We do NOT collect, store, transmit, or share any personal data.</p>
        <p>Our extensions:</p>
        <ul style={{ paddingLeft: '1.5rem', marginTop: '0.5rem' }}>
          <li>Do not collect personal information</li>
          <li>Do not use cookies or tracking technologies</li>
          <li>Do not include analytics or telemetry</li>
          <li>Do not transmit any data to external servers</li>
          <li>Do not share data with third parties</li>
        </ul>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>3. Covered Extensions</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e5e5ea' }}>
                <th style={{ textAlign: 'left', padding: '0.5rem' }}>Extension</th>
                <th style={{ textAlign: 'left', padding: '0.5rem' }}>Permissions</th>
                <th style={{ textAlign: 'left', padding: '0.5rem' }}>Purpose</th>
              </tr>
            </thead>
            <tbody>
              {[
                { name: 'Regex Tester', perms: 'None', purpose: 'All processing is done locally in the popup' },
                { name: 'AI Text Rewriter', perms: 'activeTab, scripting', purpose: 'Access selected text on the current page for rewriting' },
                { name: 'JSON Formatter Pro', perms: 'host_permissions', purpose: 'Format JSON content displayed on web pages' },
                { name: 'Color Picker Pro', perms: 'activeTab', purpose: 'Pick colors from the current page' },
                { name: 'Lorem Ipsum Generator', perms: 'None', purpose: 'All processing is done locally' },
                { name: 'Hash & Encode Toolkit', perms: 'None', purpose: 'All processing is done locally' },
                { name: 'Page Speed Insights', perms: 'activeTab', purpose: 'Analyze the current page performance' },
                { name: 'WHOIS Lookup', perms: 'None', purpose: 'Query public WHOIS data' },
                { name: 'Currency Converter', perms: 'storage', purpose: 'Save preferred currencies locally' },
                { name: 'SEO Inspector', perms: 'activeTab', purpose: 'Read meta tags from the current page' },
                { name: 'Tab Manager & Session Saver', perms: 'tabs, storage', purpose: 'List and save browser tabs locally' },
              ].map((ext) => (
                <tr key={ext.name} style={{ borderBottom: '1px solid #e5e5ea' }}>
                  <td style={{ padding: '0.5rem', fontWeight: 500 }}>{ext.name}</td>
                  <td style={{ padding: '0.5rem' }}><code style={{ background: '#f5f5f7', padding: '2px 6px', borderRadius: '4px', fontSize: '0.8rem' }}>{ext.perms}</code></td>
                  <td style={{ padding: '0.5rem' }}>{ext.purpose}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>4. Local Storage</h2>
        <p>Some extensions use <code style={{ background: '#f5f5f7', padding: '2px 6px', borderRadius: '4px' }}>chrome.storage.local</code> to save user preferences (e.g., settings, saved sessions). This data is stored entirely on your device and is never transmitted anywhere.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>5. Permissions Explanation</h2>
        <ul style={{ paddingLeft: '1.5rem' }}>
          <li><strong>activeTab</strong>: Only accesses the current tab when you explicitly click the extension icon. No background access.</li>
          <li><strong>storage</strong>: Saves preferences locally on your device only.</li>
          <li><strong>tabs</strong>: Lists open tabs for session management. Tab data stays on your device.</li>
          <li><strong>scripting</strong>: Injects content scripts to interact with page content when requested by you.</li>
          <li><strong>host_permissions</strong>: Required for content scripts to run on web pages you visit.</li>
        </ul>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>6. GDPR Compliance</h2>
        <p>Since we do not collect any personal data, GDPR data subject rights (access, rectification, erasure, portability) are not applicable. There is no data to access, correct, or delete.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>7. CCPA Compliance</h2>
        <p>We do not sell personal information. We do not collect personal information. California residents have no data to request disclosure of, as none is collected.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>8. Children&apos;s Privacy (COPPA)</h2>
        <p>Our extensions do not collect any information from anyone, including children under 13.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>9. Changes to This Policy</h2>
        <p>If we ever change our data practices, we will update this page. Since we collect no data, changes are unlikely.</p>
      </section>

      <section style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>10. Contact</h2>
        <p>If you have questions about this privacy policy, contact us at: <a href="mailto:t.mizuno27@gmail.com" style={{ color: '#0071e3' }}>t.mizuno27@gmail.com</a></p>
      </section>
    </div>
  );
}
