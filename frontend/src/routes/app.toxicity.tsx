import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard, Gauge } from "@/components/premium/glass-card";
import { FlaskConical, Upload, Sparkles, Download } from "lucide-react";
import { useState } from "react";
import { drugsApi } from "@/services/api";
import { motion, AnimatePresence } from "motion/react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { toast } from "sonner";

export const Route = createFileRoute("/app/toxicity")({
  component: Page,
});

function Page() {
  const [smiles, setSmiles] = useState("CC(=O)OC1=CC=CC=C1C(=O)O");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Awaited<ReturnType<typeof drugsApi.predictToxicity>> | null>(null);

  const run = async () => {
    setLoading(true);
    setResult(null);
    try {
      const r = await drugsApi.predictToxicity({ smiles });
      setResult(r);
      toast.success("Prediction complete");
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Drug Toxicity Prediction"
        subtitle="Multi-endpoint toxicity scoring powered by GraphNN-v3 & Transformer-XL ensembles."
        icon={<FlaskConical className="w-5 h-5 text-primary" />}
        actions={
          <button className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass text-sm">
            <Download className="w-4 h-4" /> Export report
          </button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <GlassCard className="lg:col-span-2" hover={false}>
          <h3 className="text-lg font-semibold tracking-tight">Input compound</h3>
          <p className="text-xs text-muted-foreground mt-1">Provide a SMILES string, upload MOL/SDF, or drag a CSV batch.</p>

          <div className="mt-6 space-y-4">
            <label className="text-xs uppercase tracking-wider text-muted-foreground">SMILES</label>
            <textarea
              value={smiles}
              onChange={(e) => setSmiles(e.target.value)}
              rows={3}
              className="w-full font-mono text-sm p-3 rounded-lg bg-muted/40 border border-border focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
            <div className="grid grid-cols-3 gap-2">
              {["MOL", "SDF", "CSV"].map((t) => (
                <button key={t} className="glass rounded-lg py-3 text-xs hover:bg-accent transition-colors flex flex-col items-center gap-1">
                  <Upload className="w-4 h-4" />
                  {t}
                </button>
              ))}
            </div>
            <div className="border-2 border-dashed border-border rounded-xl p-6 text-center text-xs text-muted-foreground">
              Drop files here or click to browse
            </div>
            <button
              onClick={run}
              disabled={loading}
              className="w-full py-3 rounded-full text-sm font-medium text-white transition-transform hover:scale-[1.01] disabled:opacity-70"
              style={{ background: "var(--gradient-primary)", boxShadow: "0 10px 30px oklch(0.68 0.19 245 / 0.4)" }}
            >
              {loading ? (
                <span className="inline-flex items-center gap-2">
                  <motion.span animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="inline-block w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full" />
                  Analyzing molecule…
                </span>
              ) : (
                <span className="inline-flex items-center gap-2"><Sparkles className="w-4 h-4" /> Run prediction</span>
              )}
            </button>
          </div>
        </GlassCard>

        <div className="lg:col-span-3 space-y-4">
          <GlassCard hover={false} className="min-h-[280px]">
            <AnimatePresence mode="wait">
              {loading && (
                <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="h-64 flex flex-col items-center justify-center">
                  <div className="relative w-24 h-24">
                    <motion.div className="absolute inset-0 rounded-full border-2 border-primary/30" animate={{ scale: [1, 1.4, 1], opacity: [1, 0, 1] }} transition={{ duration: 1.8, repeat: Infinity }} />
                    <motion.div className="absolute inset-2 rounded-full border-2 border-ai/40" animate={{ scale: [1, 1.4, 1], opacity: [1, 0, 1] }} transition={{ duration: 1.8, repeat: Infinity, delay: 0.3 }} />
                    <div className="absolute inset-0 grid place-items-center">
                      <FlaskConical className="w-6 h-6 text-primary animate-pulse" />
                    </div>
                  </div>
                  <p className="mt-4 text-sm text-muted-foreground">Running ensemble over 4 models…</p>
                </motion.div>
              )}
              {!loading && result && (
                <motion.div key="result" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                  className="grid grid-cols-3 gap-6 items-center">
                  <Gauge value={result.toxicity} label="Toxicity" tone={result.riskLevel === "high" ? "danger" : result.riskLevel === "medium" ? "warning" : "success"} />
                  <Gauge value={result.confidence} label="Confidence" tone="primary" />
                  <div>
                    <div className="text-xs uppercase tracking-widest text-muted-foreground">Risk level</div>
                    <div className="mt-2 text-3xl font-semibold capitalize">{result.riskLevel}</div>
                    <div className="mt-4 text-xs text-muted-foreground">Based on ensemble of GraphNN, Transformer-XL, XGBoost.</div>
                  </div>
                </motion.div>
              )}
              {!loading && !result && (
                <div className="h-64 flex items-center justify-center text-sm text-muted-foreground">
                  Run a prediction to see results
                </div>
              )}
            </AnimatePresence>
          </GlassCard>

          {result && (
            <>
              <GlassCard hover={false}>
                <h3 className="text-sm font-semibold mb-4">Endpoint breakdown</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={result.breakdown}>
                    <CartesianGrid strokeDasharray="3 3" stroke="oklch(1 0 0 / 0.05)" />
                    <XAxis dataKey="label" fontSize={10} stroke="var(--color-muted-foreground)" />
                    <YAxis fontSize={10} stroke="var(--color-muted-foreground)" />
                    <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                    <Bar dataKey="value" fill="oklch(0.68 0.19 245)" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </GlassCard>

              <GlassCard hover={false} className="border-l-4" style={{ borderLeftColor: "var(--color-ai)" }}>
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg grid place-items-center shrink-0"
                    style={{ background: "var(--gradient-ai)" }}>
                    <Sparkles className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-widest text-muted-foreground">Explainability</div>
                    <p className="mt-2 text-sm leading-relaxed">{result.explanation}</p>
                  </div>
                </div>
              </GlassCard>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
