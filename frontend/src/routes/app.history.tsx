import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { History, Search } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { drugsApi } from "@/services/api";
import { useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";

export const Route = createFileRoute("/app/history")({ component: Page });

function Page() {
  const { data } = useQuery({ queryKey: ["hist"], queryFn: () => drugsApi.listPredictions() });
  const [q, setQ] = useState("");
  const filtered = (data ?? []).filter(p => p.drug.toLowerCase().includes(q.toLowerCase()));

  return (
    <div className="space-y-8">
      <PageHeader title="Prediction History" subtitle="Browse, filter, and export all past predictions"
        icon={<History className="w-5 h-5 text-primary" />} />

      <GlassCard hover={false}>
        <div className="flex gap-3 mb-4">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search compounds…"
              className="w-full pl-10 pr-4 py-2 bg-muted/40 rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm" />
          </div>
          <select className="px-3 py-2 bg-muted/40 rounded-lg border border-border text-sm">
            <option>All models</option>
            <option>GraphNN-v3</option>
            <option>Transformer-XL</option>
          </select>
          <button className="px-4 py-2 rounded-lg glass text-sm">Export</button>
        </div>

        {!data ? <Skeleton className="h-96" /> : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-xs text-muted-foreground uppercase border-b border-border/50">
                <tr>
                  {["ID", "Compound", "Model", "Toxicity", "Confidence", "Created"].map(h => (
                    <th key={h} className="text-left py-3 font-medium">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {filtered.map(p => (
                  <tr key={p.id} className="hover:bg-accent/30">
                    <td className="py-3 font-mono text-xs">{p.id}</td>
                    <td className="py-3 font-medium">{p.drug}</td>
                    <td className="py-3 text-muted-foreground">{p.model}</td>
                    <td className="py-3">{p.toxicity}%</td>
                    <td className="py-3 font-mono text-xs">{p.confidence}%</td>
                    <td className="py-3 text-muted-foreground text-xs">{new Date(p.createdAt).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
              <span>Showing {filtered.length} of {data.length}</span>
              <div className="flex gap-1">
                {[1, 2, 3, "…", 12].map((p, i) => (
                  <button key={i} className={`w-8 h-8 rounded-lg text-xs ${p === 1 ? "text-white" : "hover:bg-accent"}`}
                    style={p === 1 ? { background: "var(--gradient-primary)" } : undefined}>{p}</button>
                ))}
              </div>
            </div>
          </div>
        )}
      </GlassCard>
    </div>
  );
}
