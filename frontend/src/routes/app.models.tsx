import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { GitCompare } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { modelsApi } from "@/services/api";
import { Bar, BarChart, CartesianGrid, PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Skeleton } from "@/components/ui/skeleton";

export const Route = createFileRoute("/app/models")({ component: Page });

function Page() {
  const { data } = useQuery({ queryKey: ["models"], queryFn: () => modelsApi.list() });
  return (
    <div className="space-y-8">
      <PageHeader title="Model Comparison" subtitle="Benchmark and compare production model performance"
        icon={<GitCompare className="w-5 h-5 text-primary" />} />

      {!data ? <Skeleton className="h-96" /> : (
        <>
          <GlassCard hover={false}>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-xs uppercase text-muted-foreground border-b border-border/50">
                  <tr>
                    {["Model", "Type", "Accuracy", "Precision", "Recall", "F1", "ROC", "Latency"].map(h => (
                      <th key={h} className="text-left py-3 font-medium">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {data.map(m => (
                    <tr key={m.id} className="hover:bg-accent/30">
                      <td className="py-3 font-medium">{m.name}</td>
                      <td className="py-3 text-muted-foreground">{m.type}</td>
                      {[m.accuracy, m.precision, m.recall, m.f1, m.roc].map((v, i) => (
                        <td key={i} className="py-3 font-mono">{(v * 100).toFixed(1)}%</td>
                      ))}
                      <td className="py-3 font-mono">{m.latencyMs}ms</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>

          <div className="grid lg:grid-cols-2 gap-4">
            <GlassCard hover={false}>
              <h3 className="font-semibold mb-4">Performance radar</h3>
              <ResponsiveContainer width="100%" height={320}>
                <RadarChart data={["accuracy", "precision", "recall", "f1", "roc"].map(k => ({
                  metric: k.toUpperCase(),
                  ...Object.fromEntries(data.map(m => [m.name, (m as any)[k] * 100])),
                }))}>
                  <PolarGrid stroke="oklch(1 0 0 / 0.08)" />
                  <PolarAngleAxis dataKey="metric" tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }} />
                  {data.map((m, i) => (
                    <Radar key={m.id} dataKey={m.name} stroke={`var(--color-chart-${(i % 5) + 1})`} fill={`var(--color-chart-${(i % 5) + 1})`} fillOpacity={0.12} />
                  ))}
                </RadarChart>
              </ResponsiveContainer>
            </GlassCard>
            <GlassCard hover={false}>
              <h3 className="font-semibold mb-4">Accuracy vs latency</h3>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="oklch(1 0 0 / 0.05)" />
                  <XAxis dataKey="name" fontSize={10} stroke="var(--color-muted-foreground)" />
                  <YAxis fontSize={10} stroke="var(--color-muted-foreground)" />
                  <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                  <Bar dataKey="accuracy" fill="oklch(0.68 0.19 245)" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="latencyMs" fill="oklch(0.68 0.22 295)" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </GlassCard>
          </div>
        </>
      )}
    </div>
  );
}
