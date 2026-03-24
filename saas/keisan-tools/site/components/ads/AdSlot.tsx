interface AdSlotProps {
  position?: string;
}

export default function AdSlot({ position = 'sidebar' }: AdSlotProps) {
  return (
    <div className="ad-slot" data-ad-position={position}>
      広告
    </div>
  );
}
