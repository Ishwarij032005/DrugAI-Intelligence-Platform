import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Beaker, RotateCcw } from "lucide-react";
import { MoleculeGlyph } from "@/components/premium/three-d";
import { motion } from "motion/react";

export const Route = createFileRoute("/app/visualization")({ component: Page });

const props = [
  { l: "Molecular weight", v: "180.16", u: "g/mol" },
  { l: "LogP", v: "1.19" },
  { l: "TPSA", v: "63.6", u: "Å²" },
  { l: "H-bond donors", v: "1" },
  { l: "H-bond acceptors", v: "4" },
  { l: "Rotatable bonds", v: "3" },
  { l: "Ring count", v: "1" },
  { l: "Heavy atoms", v: "13" },
];

function Page() {
  return (
    <div className="space-y-8">
      <PageHeader title="Molecular Viewer" subtitle="Interactive 2D & 3D structure analysis with real-time property computation"
        icon={<Beaker className="w-5 h-5 text-primary" />} />

      <div className="grid lg:grid-cols-3 gap-4">
        <GlassCard hover={false} className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="font-semibold text-lg">Aspirin</div>
              <div className="text-xs text-muted-foreground font-mono">CC(=O)OC1=CC=CC=C1C(=O)O</div>
            </div>
            <div className="flex gap-2">
              {["2D", "3D", "Surface"].map((v, i) => (
                <button key={v} className={`px-3 py-1.5 rounded-full text-xs ${i === 1 ? "text-white" : "glass"}`}
                  style={i === 1 ? { background: "var(--gradient-primary)" } : undefined}>{v}</button>
              ))}
              <button className="w-8 h-8 grid place-items-center glass rounded-full"><RotateCcw className="w-3.5 h-3.5" /></button>
            </div>
          </div>
          <div className="rounded-xl aspect-[16/10] relative overflow-hidden bg-gradient-to-br from-primary/5 via-transparent to-ai/10 grid place-items-center">
            <div className="absolute inset-0 grid-bg opacity-20" />
            <motion.div animate={{ rotateY: 360 }} transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              style={{ transformStyle: "preserve-3d" }}>
              <MoleculeGlyph className="w-72 h-72" />
            </motion.div>
          </div>
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="font-semibold text-lg mb-4">Physicochemical properties</h3>
          <div className="space-y-3">
            {props.map((p) => (
              <div key={p.l} className="flex items-baseline justify-between py-2 border-b border-border/40 last:border-0">
                <span className="text-sm text-muted-foreground">{p.l}</span>
                <span className="font-mono text-sm">
                  {p.v}<span className="text-muted-foreground ml-1 text-xs">{p.u}</span>
                </span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
