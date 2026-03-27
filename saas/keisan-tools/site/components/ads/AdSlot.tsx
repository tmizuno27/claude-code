'use client';

import { useEffect, useRef } from 'react';

interface AdSlotProps {
  position?: string;
  format?: 'auto' | 'rectangle' | 'horizontal' | 'vertical';
  responsive?: boolean;
}

const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

export default function AdSlot({
  position = 'sidebar',
  format = 'auto',
  responsive = true,
}: AdSlotProps) {
  const adRef = useRef<HTMLDivElement>(null);
  const pushed = useRef(false);

  useEffect(() => {
    if (pushed.current) return;
    try {
      const adsbygoogle = (window as unknown as { adsbygoogle: unknown[] }).adsbygoogle || [];
      adsbygoogle.push({});
      pushed.current = true;
    } catch {
      // AdSense not loaded
    }
  }, []);

  const slotMap: Record<string, string> = {
    'after-result': '1234567890',
    'sidebar-top': '2345678901',
    'sidebar-bottom': '3456789012',
    'in-article': '4567890123',
  };

  const slot = slotMap[position] || slotMap['sidebar-top'];

  return (
    <div className="ad-slot" data-ad-position={position} ref={adRef}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={ADSENSE_CLIENT_ID}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive={responsive ? 'true' : 'false'}
      />
    </div>
  );
}
