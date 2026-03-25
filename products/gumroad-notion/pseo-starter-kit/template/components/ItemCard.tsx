import type { Item } from '@/lib/data';

interface ItemCardProps {
  item: Item;
}

export function ItemCard({ item }: ItemCardProps) {
  return (
    <a
      href={`/${item.slug}/`}
      style={{
        display: 'block',
        padding: '16px 20px',
        backgroundColor: '#fff',
        border: '1px solid #e5e5e5',
        borderRadius: '8px',
        textDecoration: 'none',
        color: 'inherit',
        transition: 'box-shadow 0.2s',
      }}
    >
      <span
        style={{
          display: 'inline-block',
          fontSize: '11px',
          textTransform: 'uppercase',
          color: '#0066cc',
          fontWeight: 600,
          marginBottom: '6px',
        }}
      >
        {item.category}
      </span>
      <h3 style={{ fontSize: '16px', margin: '0 0 8px', lineHeight: 1.3 }}>
        {item.title.split('—')[0].trim()}
      </h3>
      <p
        style={{
          fontSize: '13px',
          color: '#666',
          lineHeight: 1.5,
          margin: 0,
          display: '-webkit-box',
          WebkitLineClamp: 3,
          WebkitBoxOrient: 'vertical' as const,
          overflow: 'hidden',
        }}
      >
        {item.metaDescription}
      </p>
    </a>
  );
}
