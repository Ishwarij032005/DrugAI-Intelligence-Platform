import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { BarChart3 } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { analyticsApi } from "@/services/api";
import { Area, AreaChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Skeleton } from "@/components/ui/skeleton";

export const Route = createFileRoute("/app/analytics")({ component: Page });

function Page() {
  const { data: trend } = useQuery({ queryKey: ["a-trend"], queryFn: () => analyticsApi.trend() });
  const { data: cls } = useQuery({ queryKey: ["a-cls"], queryFn: () => analyticsApi.classDistribution() });
  const heat = Array.from({ length: 7 }, () => Array.from({ length: 24 }, () => Math.random()));

  return (
    <div className="space-y-8">
      <PageHeader title="Analytics" subtitle="Executive-level insights across your discovery pipeline"
        icon={<BarChart3 className="w-5 h-5 text-primary" />} />

      <div className="grid lg:grid-cols-3 gap-4">
        <GlassCard hover={false} className="lg:col-span-2">
          <h3 className="font-semibold mb-4">Prediction trend</h3>
          {!trend ? <Skeleton className="h-64" /> : (
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={trend}>
                <defs>
                  <linearGradient id="ag" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0" stopColor="oklch(0.68 0.19 245)" stopOpacity={0.4} />
                    <stop offset="1" stopColor="oklch(0.68 0.19 245)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(1 0 0 / 0.05)" />
                <XAxis dataKey="day" fontSize={11} stroke="var(--color-muted-foreground)" />
                <YAxis fontSize={11} stroke="var(--color-muted-foreground)" />
                <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Area dataKey="predictions" stroke="oklch(0.68 0.19 245)" strokeWidth={2} fill="url(#ag)" />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">By class</h3>
          {!cls ? <Skeleton className="h-64" /> : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={cls} dataKey="value" innerRadius={50} outerRadius={80} paddingAngle={4}>
                  {cls.map((_, i) => <Cell key={i} fill={`var(--color-chart-${(i % 5) + 1})`} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </GlassCard>
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">Usage heatmap</h3>
          <div className="space-y-1">
            {heat.map((row, r) => (
              <div key={r} className="flex gap-1 items-center">
                <div className="w-8 text-[10px] text-muted-foreground">{["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][r]}</div>
                {row.map((v, c) => (
                  <div key={c} className="flex-1 aspect-square rounded" style={{ background: `oklch(0.68 0.19 245 / ${v})` }} />
                ))}
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">Model accuracy over time</h3>
          {trend && (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="oklch(1 0 0 / 0.05)" />
                <XAxis dataKey="day" fontSize={11} stroke="var(--color-muted-foreground)" />
                <YAxis domain={[80, 100]} fontSize={11} stroke="var(--color-muted-foreground)" />
                <Tooltip contentStyle={{ background: "var(--color-popover)", border: "1px solid var(--color-border)", borderRadius: 8 }} />
                <Line dataKey="accuracy" stroke="oklch(0.68 0.22 295)" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </GlassCard>
      </div>

      <div className="grid lg:grid-cols-3 gap-4">
        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">Confusion matrix</h3>
          <div className="grid grid-cols-2 gap-1 max-w-[220px] mx-auto">
            {[[820, 42], [38, 780]].flat().map((v, i) => (
              <div key={i} className="aspect-square rounded-lg grid place-items-center text-sm font-mono"
                style={{ background: `oklch(0.68 0.19 245 / ${v > 500 ? 0.6 : 0.2})` }}>
                {v}
              </div>
            ))}
          </div>
        </GlassCard>
        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">ROC curve</h3>
          <svg viewBox="0 0 200 160" className="w-full h-40">
            <line x1="20" y1="140" x2="180" y2="140" stroke="var(--color-border)" />
            <line x1="20" y1="20" x2="20" y2="140" stroke="var(--color-border)" />
            <line x1="20" y1="140" x2="180" y2="20" stroke="var(--color-muted)" strokeDasharray="3 3" />
            <path d="M20,140 Q30,40 60,30 T180,20" stroke="oklch(0.68 0.19 245)" strokeWidth="2" fill="none" style={{ filter: "drop-shadow(0 0 6px oklch(0.68 0.19 245))" }} />
          </svg>
        </GlassCard>
        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">PR curve</h3>
          <svg viewBox="0 0 200 160" className="w-full h-40">
            <line x1="20" y1="140" x2="180" y2="140" stroke="var(--color-border)" />
            <line x1="20" y1="20" x2="20" y2="140" stroke="var(--color-border)" />
            <path d="M20,30 Q100,40 180,120" stroke="oklch(0.68 0.22 295)" strokeWidth="2" fill="none" style={{ filter: "drop-shadow(0 0 6px oklch(0.68 0.22 295))" }} />
          </svg>
        </GlassCard>
      </div>
    </div>
  );
}
