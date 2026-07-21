import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Search } from "lucide-react";
import { useState } from "react";
import { MoleculeGlyph } from "@/components/premium/three-d";

export const Route = createFileRoute("/app/similarity")({ component: Page });

const RESULTS = [
  { name: "Salicylic acid", sim: 92, class: "Analgesic" },
  { name: "Diflunisal", sim: 84, class: "NSAID" },
  { name: "Methyl salicylate", sim: 78, class: "Topical" },
  { name: "Salsalate", sim: 74, class: "NSAID" },
  { name: "Choline salicylate", sim: 69, class: "Analgesic" },
  { name: "Mesalamine", sim: 63, class: "GI" },
];

function Page() {
  const [q, setQ] = useState("Aspirin");
  return (
    <div className="space-y-8">
      <PageHeader title="Similarity Search" subtitle="Find structurally & functionally similar compounds"
        icon={<Search className="w-5 h-5 text-primary" />} />

      <GlassCard hover={false}>
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input value={q} onChange={(e) => setQ(e.target.value)} className="w-full pl-10 pr-4 py-3 bg-muted/40 rounded-full border border-border focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm" />
          </div>
          <button className="px-6 py-3 rounded-full text-sm font-medium text-white" style={{ background: "var(--gradient-primary)" }}>
            Search
          </button>
        </div>
      </GlassCard>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {RESULTS.map((r) => (
          <GlassCard key={r.name}>
            <div className="aspect-square rounded-xl bg-gradient-to-br from-primary/10 to-ai/10 grid place-items-center mb-4">
              <MoleculeGlyph className="w-32 h-32" />
            </div>
            <div className="flex items-start justify-between">
              <div>
                <div className="font-semibold">{r.name}</div>
                <div className="text-xs text-muted-foreground">{r.class}</div>
              </div>
              <div className="text-right">
                <div className="text-xl font-semibold gradient-text">{r.sim}%</div>
                <div className="text-[10px] uppercase tracking-widest text-muted-foreground">Similarity</div>
              </div>
            </div>
            <div className="mt-4 h-1 rounded-full bg-muted overflow-hidden">
              <div className="h-full" style={{ width: `${r.sim}%`, background: "var(--gradient-primary)" }} />
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
