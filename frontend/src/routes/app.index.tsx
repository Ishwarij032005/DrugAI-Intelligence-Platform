import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard, AnimatedCounter } from "@/components/premium/glass-card";
import { motion } from "motion/react";
import { Activity, Cpu, FlaskConical, Gauge, Sparkles, TrendingUp, Users, Zap } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { analyticsApi, drugsApi } from "@/services/api";
import { Area, AreaChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Skeleton } from "@/components/ui/skeleton";

export const Route = createFileRoute("/app/")({
  component: Dashboard,
});

const stats = [
  { label: "Today's predictions", value: 12420, icon: FlaskConical, delta: "+18.2%", tone: "primary" },
  { label: "Model accuracy", value: 96.4, suffix: "%", decimals: 1, icon: Gauge, delta: "+0.4%", tone: "success" },
  { label: "Avg inference", value: 42, suffix: "ms", icon: Zap, delta: "-6ms", tone: "ai" },
  { label: "GPU utilization", value: 78, suffix: "%", icon: Cpu, delta: "8× A100", tone: "warning" },
];

function Dashboard() {
  const { data: trend } = useQuery({ queryKey: ["trend"], queryFn: () => analyticsApi.trend() });
  const { data: classes } = useQuery({ queryKey: ["classes"], queryFn: () => analyticsApi.classDistribution() });
  const { data: preds } = useQuery({ queryKey: ["preds"], queryFn: () => drugsApi.listPredictions() });

  return (
    <div className="space-y-8">
      <PageHeader
        title="Welcome back, Dr. Sinclair"
        subtitle="Here's what's happening across your discovery pipeline today."
        icon={<Sparkles className="w-5 h-5 text-primary" />}
        actions={
          <button className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium text-white"
            style={{ background: "var(--gradient-primary)" }}>
            <Sparkles className="w-4 h-4" /> New prediction
          </button>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
            <GlassCard className="p-5">
              <div className="flex items-start justify-between">
                <div className="w-10 h-10 rounded-lg grid place-items-center"
                  style={{ background: `oklch(from var(--color-${s.tone}) l c h / 0.15)` }}>
                  <s.icon className="w-4 h-4" style={{ color: `var(--color-${s.tone})` }} />
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full" style={{ background: "oklch(0.72 0.18 155 / 0.15)", color: "var(--color-success)" }}>
                  {s.delta}
                </span>
              </div>
              <div className="mt-4 text-3xl font-semibold tracking-tight">
                <AnimatedCounter value={s.value} suffix={s.suffix ?? ""} decimals={s.decimals ?? 0} />
              </div>
              <div className="mt-1 text-xs text-muted-foreground">{s.label}</div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <GlassCard className="lg:col-span-2" hover={false}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Last 14 days</div>
              <h3 className="text-lg font-semibold tracking-tight mt-1">Prediction volume & accuracy</h3>
            </div>
            <TrendingUp className="w-4 h-4 text-primary" />
          </div>
          {!trend ? <Skeleton className="h-72 w-full" /> : (
            <ResponsiveContainer width="100%" height={288}>
              <AreaChart data={trend}>
                <defs>
                  <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0" stopColor="oklch(0.68 0.19 245)" stopOpacity={0.5} />
                    <stop offset="1" stopColor="oklch(0.68 0.19 245)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(1 0 0 / 0.05)" />
                <XAxis dataKey="day" stroke="var(--color-muted-foreground)" fontSize={11} />
                <YAxis stroke="var(--color-muted-foreground)" fontSize={11} />
                <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Area type="monotone" dataKey="predictions" stroke="oklch(0.68 0.19 245)" strokeWidth={2} fill="url(#g1)" />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </GlassCard>

        <GlassCard hover={false}>
          <div className="mb-6">
            <div className="text-xs uppercase tracking-widest text-muted-foreground">Distribution</div>
            <h3 className="text-lg font-semibold tracking-tight mt-1">Drug classes</h3>
          </div>
          {!classes ? <Skeleton className="h-64 w-full" /> : (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={classes} dataKey="value" innerRadius={55} outerRadius={90} paddingAngle={4}>
                  {classes.map((_, i) => (
                    <Cell key={i} fill={`var(--color-chart-${(i % 5) + 1})`} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Legend iconSize={8} wrapperStyle={{ fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <GlassCard className="lg:col-span-2" hover={false}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold tracking-tight">Recent predictions</h3>
            <button className="text-xs text-primary hover:underline">View all</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-left text-xs text-muted-foreground uppercase tracking-wider border-b border-border/50">
                <tr>
                  <th className="pb-3 font-medium">Compound</th>
                  <th className="pb-3 font-medium">Model</th>
                  <th className="pb-3 font-medium">Toxicity</th>
                  <th className="pb-3 font-medium">Confidence</th>
                  <th className="pb-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {(preds ?? []).slice(0, 6).map((p) => (
                  <tr key={p.id} className="hover:bg-accent/30 transition-colors">
                    <td className="py-3">
                      <div className="font-medium">{p.drug}</div>
                      <div className="text-xs text-muted-foreground font-mono truncate max-w-[180px]">{p.smiles}</div>
                    </td>
                    <td className="py-3 text-muted-foreground">{p.model}</td>
                    <td className="py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-1.5 rounded-full bg-muted overflow-hidden">
                          <div className="h-full rounded-full" style={{
                            width: `${p.toxicity}%`,
                            background: p.status === "danger" ? "var(--color-destructive)" : p.status === "warning" ? "var(--color-warning)" : "var(--color-success)",
                          }} />
                        </div>
                        <span className="text-xs font-mono">{p.toxicity}%</span>
                      </div>
                    </td>
                    <td className="py-3 font-mono text-xs">{p.confidence}%</td>
                    <td className="py-3">
                      <span className="text-[10px] uppercase font-semibold px-2 py-1 rounded-full"
                        style={{ background: `oklch(from var(--color-${p.status === "danger" ? "destructive" : p.status === "warning" ? "warning" : "success"}) l c h / 0.15)`, color: `var(--color-${p.status === "danger" ? "destructive" : p.status === "warning" ? "warning" : "success"})` }}>
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="text-lg font-semibold tracking-tight mb-4">Activity</h3>
          <ul className="space-y-4">
            {[
              { icon: Sparkles, text: "GraphNN-v3 trained on Tox21+", time: "12m ago" },
              { icon: FlaskConical, text: "Batch of 2,400 compounds screened", time: "1h ago" },
              { icon: Users, text: "Dr. Kim shared 'Kinase Set A'", time: "3h ago" },
              { icon: Activity, text: "MLflow experiment #482 completed", time: "5h ago" },
              { icon: Cpu, text: "GPU cluster auto-scaled (8→12)", time: "1d ago" },
            ].map((a, i) => (
              <li key={i} className="flex gap-3">
                <div className="w-8 h-8 rounded-full glass grid place-items-center shrink-0">
                  <a.icon className="w-3.5 h-3.5 text-primary" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm">{a.text}</div>
                  <div className="text-xs text-muted-foreground">{a.time}</div>
                </div>
              </li>
            ))}
          </ul>
        </GlassCard>
      </div>
    </div>
  );
}
