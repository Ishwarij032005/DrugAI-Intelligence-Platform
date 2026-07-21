import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Brain, Sparkles } from "lucide-react";

export const Route = createFileRoute("/app/explainability")({ component: Page });

const features = [
  { name: "Aromatic ring system", shap: 0.34 },
  { name: "Carbonyl group (C=O)", shap: 0.21 },
  { name: "Ester linkage", shap: 0.14 },
  { name: "Hydroxyl group (-OH)", shap: 0.09 },
  { name: "Molecular weight", shap: 0.07 },
  { name: "LogP", shap: -0.05 },
  { name: "Ring count", shap: -0.11 },
  { name: "TPSA", shap: -0.16 },
];

function Page() {
  return (
    <div className="space-y-8">
      <PageHeader title="Explainable AI" subtitle="SHAP & LIME interpretations of every prediction"
        icon={<Brain className="w-5 h-5 text-primary" />} />

      <GlassCard hover={false} className="border-l-4" style={{ borderLeftColor: "var(--color-ai)" }}>
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg grid place-items-center shrink-0" style={{ background: "var(--gradient-ai)" }}>
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="text-xs uppercase tracking-widest text-muted-foreground">Why did the AI predict this?</div>
            <p className="mt-2 leading-relaxed">
              The model classified <strong>Aspirin</strong> as <strong>low-toxicity</strong> primarily because
              its aromatic ring system aligns with 94% of the benign compounds in the Tox21 reference set. The
              carbonyl group contributed positively to hepatic clearance predictions, while low TPSA reduced
              BBB penetration concerns.
            </p>
          </div>
        </div>
      </GlassCard>

      <div className="grid lg:grid-cols-2 gap-4">
        <GlassCard hover={false}>
          <h3 className="font-semibold text-lg mb-4">SHAP feature importance</h3>
          <div className="space-y-3">
            {features.map((f) => {
              const positive = f.shap > 0;
              const w = Math.abs(f.shap) * 200;
              return (
                <div key={f.name} className="flex items-center gap-3 text-sm">
                  <div className="w-40 truncate text-muted-foreground">{f.name}</div>
                  <div className="flex-1 relative h-6 flex items-center">
                    <div className="absolute left-1/2 top-0 bottom-0 w-px bg-border" />
                    <div className="absolute h-4 rounded" style={{
                      [positive ? "left" : "right"]: "50%",
                      width: `${w}%`,
                      background: positive ? "var(--color-destructive)" : "var(--color-success)",
                    }} />
                  </div>
                  <div className="w-14 text-right font-mono text-xs">{f.shap > 0 ? "+" : ""}{f.shap.toFixed(2)}</div>
                </div>
              );
            })}
          </div>
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="font-semibold text-lg mb-4">LIME local explanation</h3>
          <div className="rounded-xl aspect-square bg-gradient-to-br from-primary/10 to-ai/10 relative overflow-hidden grid place-items-center">
            <svg viewBox="0 0 200 200" className="w-full h-full">
              {Array.from({ length: 12 }).map((_, i) => {
                const angle = (i / 12) * Math.PI * 2;
                const r = 60 + (i % 3) * 20;
                const x = 100 + Math.cos(angle) * r;
                const y = 100 + Math.sin(angle) * r;
                const intensity = Math.random();
                return (
                  <g key={i}>
                    <line x1="100" y1="100" x2={x} y2={y} stroke={`oklch(0.68 0.19 245 / ${intensity})`} strokeWidth="1" />
                    <circle cx={x} cy={y} r={6 + intensity * 8} fill={`oklch(0.68 0.19 245 / ${intensity})`}
                      style={{ filter: `drop-shadow(0 0 6px oklch(0.68 0.19 245 / ${intensity}))` }} />
                  </g>
                );
              })}
              <circle cx="100" cy="100" r="18" fill="url(#center)" />
              <defs>
                <radialGradient id="center">
                  <stop offset="0" stopColor="oklch(0.68 0.22 295)" />
                  <stop offset="1" stopColor="oklch(0.68 0.19 245)" />
                </radialGradient>
              </defs>
            </svg>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
