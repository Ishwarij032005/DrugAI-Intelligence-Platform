import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Atom, Sparkles } from "lucide-react";
import { MoleculeGlyph } from "@/components/premium/three-d";
import { useState } from "react";

export const Route = createFileRoute("/app/dti")({ component: Page });

const heatmap = Array.from({ length: 8 }, () => Array.from({ length: 12 }, () => Math.random()));

function Page() {
  const [drug, setDrug] = useState("Imatinib");
  const [protein, setProtein] = useState("BCR-ABL1 (P00519)");
  return (
    <div className="space-y-8">
      <PageHeader title="Drug–Target Interaction" subtitle="Predict binding affinity across the human proteome."
        icon={<Atom className="w-5 h-5 text-primary" />} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <GlassCard hover={false}>
          <h3 className="font-semibold text-lg mb-4">Inputs</h3>
          <div className="space-y-4">
            <div>
              <label className="text-xs uppercase tracking-wider text-muted-foreground">Compound</label>
              <input value={drug} onChange={(e) => setDrug(e.target.value)} className="mt-2 w-full px-3 py-2 rounded-lg bg-muted/40 border border-border focus:ring-2 focus:ring-primary/50 focus:outline-none text-sm" />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wider text-muted-foreground">Target protein</label>
              <input value={protein} onChange={(e) => setProtein(e.target.value)} className="mt-2 w-full px-3 py-2 rounded-lg bg-muted/40 border border-border focus:ring-2 focus:ring-primary/50 focus:outline-none text-sm" />
            </div>
            <button className="w-full py-2.5 rounded-full text-sm font-medium text-white"
              style={{ background: "var(--gradient-primary)" }}>
              <Sparkles className="w-4 h-4 inline mr-1" /> Predict binding
            </button>
          </div>
        </GlassCard>

        <GlassCard hover={false} className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-lg">Binding pocket</h3>
            <div className="text-xs text-muted-foreground">Predicted Kd: <span className="font-mono text-foreground">14.2 nM</span></div>
          </div>
          <div className="relative rounded-xl overflow-hidden aspect-[16/9] bg-gradient-to-br from-primary/10 via-transparent to-ai/10 grid place-items-center">
            <MoleculeGlyph className="w-64 h-64" />
            <div className="absolute inset-0 grid-bg opacity-20" />
          </div>
        </GlassCard>
      </div>

      <GlassCard hover={false}>
        <h3 className="font-semibold text-lg mb-4">Binding affinity heatmap</h3>
        <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(12, minmax(0, 1fr))` }}>
          {heatmap.flat().map((v, i) => (
            <div key={i} className="aspect-square rounded" style={{
              background: `oklch(0.68 0.19 245 / ${v})`,
              boxShadow: v > 0.75 ? "0 0 8px oklch(0.68 0.19 245 / 0.6)" : undefined,
            }} title={`${(v * 100).toFixed(1)}%`} />
          ))}
        </div>
        <div className="mt-4 flex items-center gap-3 text-xs text-muted-foreground">
          <span>Low</span>
          <div className="flex-1 h-1.5 rounded-full" style={{ background: "linear-gradient(90deg, oklch(0.68 0.19 245 / 0.05), oklch(0.68 0.19 245))" }} />
          <span>High</span>
        </div>
      </GlassCard>

      <GlassCard hover={false}>
        <h3 className="font-semibold text-lg mb-4">Top predicted interactions</h3>
        <table className="w-full text-sm">
          <thead className="text-xs text-muted-foreground uppercase tracking-wider border-b border-border/50">
            <tr><th className="text-left pb-3">Target</th><th className="text-left pb-3">UniProt</th><th className="text-left pb-3">Kd</th><th className="text-left pb-3">Confidence</th></tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {[
              ["BCR-ABL1", "P00519", "14.2 nM", 98],
              ["c-KIT", "P10721", "42 nM", 92],
              ["PDGFRα", "P16234", "180 nM", 87],
              ["c-SRC", "P12931", "620 nM", 74],
            ].map(([t, u, k, c]) => (
              <tr key={t as string} className="hover:bg-accent/30">
                <td className="py-3 font-medium">{t}</td>
                <td className="py-3 font-mono text-xs">{u}</td>
                <td className="py-3">{k}</td>
                <td className="py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-1 rounded-full bg-muted overflow-hidden">
                      <div className="h-full" style={{ width: `${c}%`, background: "var(--gradient-primary)" }} />
                    </div>
                    <span className="text-xs font-mono">{c}%</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  );
}
