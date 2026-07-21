import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { HeartPulse } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { drugsApi } from "@/services/api";

export const Route = createFileRoute("/app/side-effects")({ component: Page });

function Page() {
  const { data = [] } = useQuery({ queryKey: ["side"], queryFn: () => drugsApi.sideEffects() });
  const sevColor = { mild: "success", moderate: "warning", severe: "danger" } as const;

  return (
    <div className="space-y-8">
      <PageHeader title="Side Effect Prediction" subtitle="Adverse event probability across body systems"
        icon={<HeartPulse className="w-5 h-5 text-primary" />} />

      <div className="grid lg:grid-cols-3 gap-4">
        <GlassCard hover={false} className="lg:col-span-1 flex items-center justify-center">
          <svg viewBox="0 0 200 400" className="h-96">
            <defs>
              <linearGradient id="body" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0" stopColor="oklch(0.68 0.19 245 / 0.4)" />
                <stop offset="1" stopColor="oklch(0.68 0.22 295 / 0.4)" />
              </linearGradient>
            </defs>
            <circle cx="100" cy="40" r="30" fill="url(#body)" />
            <rect x="70" y="70" width="60" height="20" rx="10" fill="url(#body)" />
            <rect x="55" y="90" width="90" height="120" rx="20" fill="url(#body)" />
            <rect x="30" y="95" width="20" height="90" rx="10" fill="url(#body)" />
            <rect x="150" y="95" width="20" height="90" rx="10" fill="url(#body)" />
            <rect x="70" y="210" width="25" height="120" rx="10" fill="url(#body)" />
            <rect x="105" y="210" width="25" height="120" rx="10" fill="url(#body)" />
            {/* pulse markers */}
            {[[100, 50], [95, 120], [100, 160], [80, 260], [130, 100]].map(([cx, cy], i) => (
              <g key={i}>
                <circle cx={cx} cy={cy} r="6" fill="oklch(0.65 0.24 25)" opacity="0.7">
                  <animate attributeName="r" values="6;12;6" dur="2s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="0.7;0;0.7" dur="2s" repeatCount="indefinite" />
                </circle>
                <circle cx={cx} cy={cy} r="4" fill="oklch(0.65 0.24 25)" />
              </g>
            ))}
          </svg>
        </GlassCard>

        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-3">
          {data.map((s) => (
            <GlassCard key={s.name}>
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-semibold">{s.name}</div>
                  <div className="text-xs text-muted-foreground capitalize">{s.severity} severity</div>
                </div>
                <span className="text-[10px] uppercase font-semibold px-2 py-1 rounded-full"
                  style={{ background: `oklch(from var(--color-${sevColor[s.severity as keyof typeof sevColor]}) l c h / 0.15)`, color: `var(--color-${sevColor[s.severity as keyof typeof sevColor]})` }}>
                  {s.severity}
                </span>
              </div>
              <div className="mt-4 flex items-center gap-3">
                <div className="flex-1 h-1.5 rounded-full bg-muted overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${s.probability}%`, background: "var(--gradient-primary)" }} />
                </div>
                <span className="text-sm font-mono">{s.probability}%</span>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </div>
  );
}
