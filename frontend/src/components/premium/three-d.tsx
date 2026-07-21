import { motion } from "motion/react";

// Animated DNA helix + orbiting molecule visualization used on the landing hero.
export function DnaHelix({ className = "" }: { className?: string }) {
  const rungs = 22;
  return (
    <div className={`relative ${className}`} style={{ perspective: 1000 }}>
      <motion.div
        className="relative mx-auto"
        style={{ width: 260, height: 420, transformStyle: "preserve-3d" }}
        animate={{ rotateY: 360 }}
        transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
      >
        {Array.from({ length: rungs }).map((_, i) => {
          const t = (i / rungs) * Math.PI * 4;
          const y = (i / rungs) * 420 - 210;
          const x1 = Math.sin(t) * 80;
          const x2 = Math.sin(t + Math.PI) * 80;
          const z1 = Math.cos(t) * 80;
          const z2 = Math.cos(t + Math.PI) * 80;
          return (
            <div key={i} className="absolute left-1/2 top-1/2" style={{ transform: `translate(-50%, -50%) translateY(${y}px)`, transformStyle: "preserve-3d" }}>
              <div
                className="absolute rounded-full"
                style={{
                  width: 14, height: 14,
                  transform: `translate3d(${x1}px, 0, ${z1}px)`,
                  background: "linear-gradient(135deg, oklch(0.68 0.19 245), oklch(0.78 0.15 210))",
                  boxShadow: "0 0 20px oklch(0.68 0.19 245 / 0.7)",
                }}
              />
              <div
                className="absolute rounded-full"
                style={{
                  width: 14, height: 14,
                  transform: `translate3d(${x2}px, 0, ${z2}px)`,
                  background: "linear-gradient(135deg, oklch(0.68 0.22 295), oklch(0.68 0.19 245))",
                  boxShadow: "0 0 20px oklch(0.68 0.22 295 / 0.7)",
                }}
              />
              <div
                className="absolute h-[2px] top-[6px]"
                style={{
                  width: 160,
                  transform: `translate3d(${(x1 + x2) / 2 - 80}px, 0, ${(z1 + z2) / 2}px) rotateY(${(Math.atan2(z2 - z1, x2 - x1) * 180) / Math.PI}deg)`,
                  background: "linear-gradient(90deg, oklch(0.68 0.19 245 / 0.4), oklch(0.68 0.22 295 / 0.4))",
                  transformOrigin: "left center",
                }}
              />
            </div>
          );
        })}
      </motion.div>
    </div>
  );
}

export function FloatingMolecules({ className = "" }: { className?: string }) {
  const items = Array.from({ length: 14 });
  return (
    <div className={`pointer-events-none absolute inset-0 overflow-hidden ${className}`}>
      {items.map((_, i) => {
        const size = 6 + Math.random() * 14;
        const left = Math.random() * 100;
        const top = Math.random() * 100;
        const delay = Math.random() * 5;
        const dur = 8 + Math.random() * 12;
        return (
          <motion.div
            key={i}
            className="absolute rounded-full"
            style={{
              left: `${left}%`, top: `${top}%`, width: size, height: size,
              background: i % 2 === 0
                ? "radial-gradient(circle, oklch(0.68 0.19 245 / 0.9), oklch(0.68 0.19 245 / 0))"
                : "radial-gradient(circle, oklch(0.68 0.22 295 / 0.9), oklch(0.68 0.22 295 / 0))",
              filter: "blur(1px)",
            }}
            animate={{ y: [0, -40, 0], x: [0, 20, 0], opacity: [0.3, 1, 0.3] }}
            transition={{ duration: dur, repeat: Infinity, delay, ease: "easeInOut" }}
          />
        );
      })}
    </div>
  );
}

export function MoleculeGlyph({ className = "" }: { className?: string }) {
  // Placeholder for molecule 2D/3D viewer.
  return (
    <svg viewBox="0 0 200 200" className={className} fill="none">
      <defs>
        <linearGradient id="mg1" x1="0" x2="1">
          <stop offset="0" stopColor="oklch(0.68 0.19 245)" />
          <stop offset="1" stopColor="oklch(0.68 0.22 295)" />
        </linearGradient>
      </defs>
      {[[100, 100, 40, 20], [100, 100, 100, 20], [100, 100, 160, 20], [100, 100, 40, 100], [100, 100, 160, 100], [100, 100, 40, 180], [100, 100, 100, 180], [100, 100, 160, 180]].map(([x1, y1, x2, y2], i) => (
        <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="url(#mg1)" strokeWidth="1.5" opacity="0.5" />
      ))}
      {[[40, 20], [100, 20], [160, 20], [40, 100], [100, 100], [160, 100], [40, 180], [100, 180], [160, 180]].map(([cx, cy], i) => (
        <circle key={i} cx={cx} cy={cy} r={i === 4 ? 10 : 7} fill="url(#mg1)" opacity={i === 4 ? 1 : 0.85} />
      ))}
    </svg>
  );
}
