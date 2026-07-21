import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard, Gauge } from "@/components/premium/glass-card";
import { Activity } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { drugsApi } from "@/services/api";
import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer } from "recharts";
import { Skeleton } from "@/components/ui/skeleton";

export const Route = createFileRoute("/app/admet")({ component: Page });

function Page() {
  const { data } = useQuery({ queryKey: ["admet"], queryFn: () => drugsApi.admet() });
  const tone = (v: number) => v > 70 ? "success" : v > 40 ? "warning" : "danger";

  return (
    <div className="space-y-8">
      <PageHeader title="ADMET Profile" subtitle="Absorption, Distribution, Metabolism, Excretion, Toxicity"
        icon={<Activity className="w-5 h-5 text-primary" />} />

      {!data ? (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-52" />)}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {data.map((d) => (
              <GlassCard key={d.label} className="text-center">
                <Gauge value={d.value} label={d.label} tone={tone(d.value)} size={130} />
                <p className="mt-3 text-xs text-muted-foreground">{d.note}</p>
              </GlassCard>
            ))}
          </div>

          <div className="grid lg:grid-cols-2 gap-4">
            <GlassCard hover={false}>
              <h3 className="text-lg font-semibold mb-4">ADMET radar</h3>
              <ResponsiveContainer width="100%" height={320}>
                <RadarChart data={data}>
                  <PolarGrid stroke="oklch(1 0 0 / 0.08)" />
                  <PolarAngleAxis dataKey="label" tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
                  <Radar dataKey="value" stroke="oklch(0.68 0.19 245)" fill="oklch(0.68 0.19 245)" fillOpacity={0.35} />
                </RadarChart>
              </ResponsiveContainer>
            </GlassCard>

            <GlassCard hover={false}>
              <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
              <ul className="space-y-3">
                {[
                  { title: "High CYP3A4 affinity", desc: "Consider drug-drug interaction screening", tone: "warning" },
                  { title: "Low BBB penetration", desc: "May limit CNS efficacy — consider prodrug", tone: "warning" },
                  { title: "Good oral bioavailability", desc: "Suitable for oral dosing", tone: "success" },
                  { title: "Low hERG risk", desc: "Cardiac safety profile acceptable", tone: "success" },
                ].map((r) => (
                  <li key={r.title} className="flex gap-3 items-start p-3 rounded-lg bg-muted/30">
                    <div className="w-2 h-2 rounded-full mt-2" style={{ background: `var(--color-${r.tone})`, boxShadow: `0 0 8px var(--color-${r.tone})` }} />
                    <div>
                      <div className="text-sm font-medium">{r.title}</div>
                      <div className="text-xs text-muted-foreground">{r.desc}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </GlassCard>
          </div>
        </>
      )}
    </div>
  );
}
