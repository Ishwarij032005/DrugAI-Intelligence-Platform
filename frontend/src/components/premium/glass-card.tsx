import { motion, useMotionValue, useSpring, useTransform, type MotionProps } from "motion/react";
import { useEffect, useRef, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export function GlassCard({
  children,
  className,
  hover = true,
  ...rest
}: { children: ReactNode; className?: string; hover?: boolean } & MotionProps) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rx = useSpring(useTransform(y, [-40, 40], [6, -6]), { stiffness: 200, damping: 20 });
  const ry = useSpring(useTransform(x, [-40, 40], [-6, 6]), { stiffness: 200, damping: 20 });
  const ref = useRef<HTMLDivElement>(null);

  return (
    <motion.div
      ref={ref}
      onMouseMove={(e) => {
        if (!hover || !ref.current) return;
        const r = ref.current.getBoundingClientRect();
        x.set(e.clientX - r.left - r.width / 2);
        y.set(e.clientY - r.top - r.height / 2);
      }}
      onMouseLeave={() => {
        x.set(0);
        y.set(0);
      }}
      style={hover ? { rotateX: rx, rotateY: ry, transformPerspective: 1000 } : undefined}
      className={cn(
        "glass elegant-shadow rounded-2xl p-6 relative overflow-hidden",
        className,
      )}
      {...rest}
    >
      <div className="pointer-events-none absolute inset-0 opacity-0 hover:opacity-100 transition-opacity duration-500"
        style={{ background: "radial-gradient(600px circle at var(--mx,50%) var(--my,50%), oklch(0.68 0.19 245 / 0.08), transparent 40%)" }} />
      {children}
    </motion.div>
  );
}

export function AnimatedCounter({ value, decimals = 0, suffix = "", prefix = "" }: {
  value: number; decimals?: number; suffix?: string; prefix?: string;
}) {
  const mv = useMotionValue(0);
  const spring = useSpring(mv, { stiffness: 60, damping: 20 });
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    mv.set(value);
  }, [value, mv]);

  useEffect(() => {
    return spring.on("change", (v) => {
      if (ref.current) ref.current.textContent = `${prefix}${v.toFixed(decimals)}${suffix}`;
    });
  }, [spring, decimals, suffix, prefix]);

  return <span ref={ref}>{`${prefix}0${suffix}`}</span>;
}

export function Gauge({ value, size = 140, label, tone = "primary" }: {
  value: number; size?: number; label?: string; tone?: "primary" | "success" | "warning" | "danger" | "ai";
}) {
  const stroke = 10;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (Math.min(100, Math.max(0, value)) / 100) * c;
  const color = {
    primary: "var(--color-primary)",
    success: "var(--color-success)",
    warning: "var(--color-warning)",
    danger: "var(--color-destructive)",
    ai: "var(--color-ai)",
  }[tone];

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={r} stroke="var(--color-muted)" strokeWidth={stroke} fill="none" />
          <motion.circle
            cx={size / 2} cy={size / 2} r={r}
            stroke={color} strokeWidth={stroke} fill="none" strokeLinecap="round"
            strokeDasharray={c}
            initial={{ strokeDashoffset: c }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            style={{ filter: `drop-shadow(0 0 8px ${color})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-semibold tracking-tight">
            <AnimatedCounter value={value} suffix="%" />
          </span>
        </div>
      </div>
      {label && <span className="text-xs uppercase tracking-wider text-muted-foreground">{label}</span>}
    </div>
  );
}
