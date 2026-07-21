import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Sparkles } from "lucide-react";

export const Route = createFileRoute("/app/recommendation")({ component: Page });

const R = [
  { name: "Celecoxib", safety: 88, eff: 82, note: "COX-2 selective; safer GI profile" },
  { name: "Naproxen", safety: 76, eff: 87, note: "Long half-life; strong analgesic" },
  { name: "Meloxicam", safety: 81, eff: 79, note: "Preferential COX-2 inhibition" },
  { name: "Diclofenac", safety: 71, eff: 89, note: "High potency; hepatic monitoring" },
];

function Page() {
  return (
    <div className="space-y-8">
      <PageHeader title="Drug Recommendations" subtitle="Ranked alternatives with safety & efficacy scoring"
        icon={<Sparkles className="w-5 h-5 text-primary" />} />

      <div className="grid md:grid-cols-2 gap-4">
        {R.map((d, i) => (
          <GlassCard key={d.name}>
            <div className="flex items-start justify-between">
              <div>
                <div className="text-[10px] uppercase tracking-widest text-muted-foreground">Rank #{i + 1}</div>
                <div className="font-semibold text-xl mt-1">{d.name}</div>
              </div>
              <div className="text-right">
                <div className="text-3xl font-semibold gradient-text">{Math.round((d.safety + d.eff) / 2)}</div>
                <div className="text-[10px] uppercase tracking-widest text-muted-foreground">Overall</div>
              </div>
            </div>
            <p className="mt-3 text-sm text-muted-foreground">{d.note}</p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              {[["Safety", d.safety, "success"], ["Effectiveness", d.eff, "primary"]].map(([l, v, tone]) => (
                <div key={l as string}>
                  <div className="flex justify-between text-xs">
                    <span className="text-muted-foreground">{l}</span>
                    <span className="font-mono">{v}%</span>
                  </div>
                  <div className="mt-1 h-1 rounded-full bg-muted overflow-hidden">
                    <div className="h-full" style={{ width: `${v}%`, background: `var(--color-${tone})` }} />
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
