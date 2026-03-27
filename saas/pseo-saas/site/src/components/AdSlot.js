'use client';

import { useEffect, useRef } from 'react';

const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

export default function AdSlot({ position = 'default', format = 'auto' }) {
  const pushed = useRef(false);

  useEffect(() => {
    if (pushed.current) return;
    try {
      const adsbygoogle = window.adsbygoogle || [];
      adsbygoogle.push({});
      pushed.current = true;
    } catch {
      // AdSense not loaded
    }
  }, []);

  return (
    <div className="ad-slot" data-ad-position={position} style={{ margin: '24px 0', textAlign: 'center' }}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={ADSENSE_CLIENT_ID}
        data-ad-slot="5678901234"
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}
