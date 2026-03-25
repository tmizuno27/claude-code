import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="container" style={{ textAlign: 'center', padding: '4rem 1rem' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>404</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Currency pair not found. Please check the URL and try again.
      </p>
      <Link href="/" style={{ padding: '0.75rem 1.5rem', background: 'var(--primary)', color: 'white', borderRadius: '8px', display: 'inline-block' }}>
        Back to Home
      </Link>
    </div>
  );
}
