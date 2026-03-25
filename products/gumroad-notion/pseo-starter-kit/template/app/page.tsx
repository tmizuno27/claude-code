import { getAllItems, getAllCategories } from '@/lib/data';
import { ItemCard } from '@/components/ItemCard';

export default function HomePage() {
  const items = getAllItems();
  const categories = getAllCategories();

  return (
    <div>
      <section style={{ marginBottom: '48px' }}>
        <h1 style={{ fontSize: '32px', marginBottom: '8px' }}>
          Compare Developer Tools & Frameworks
        </h1>
        <p style={{ color: '#666', fontSize: '18px', lineHeight: 1.6 }}>
          Detailed, side-by-side comparisons to help you choose the right
          technology for your next project. {items.length} comparisons across{' '}
          {categories.length} categories.
        </p>
      </section>

      {categories.map((category) => {
        const categoryItems = items.filter((item) => item.category === category);
        return (
          <section key={category} style={{ marginBottom: '40px' }}>
            <h2
              style={{
                fontSize: '22px',
                textTransform: 'capitalize',
                borderBottom: '2px solid #e5e5e5',
                paddingBottom: '8px',
                marginBottom: '16px',
              }}
            >
              {category}
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                gap: '16px',
              }}
            >
              {categoryItems.map((item) => (
                <ItemCard key={item.slug} item={item} />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
