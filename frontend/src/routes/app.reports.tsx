import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { FileText, Download } from "lucide-react";

export const Route = createFileRoute("/app/reports")({ component: Page });

const REPORTS = [
  { name: "Q4 Toxicity Screening Summary", type: "PDF", size: "2.4 MB", date: "2026-07-14" },
  { name: "Aspirin — Full ADMET Report", type: "PDF", size: "1.1 MB", date: "2026-07-12" },
  { name: "Kinase Set A — Batch Predictions", type: "CSV", size: "384 KB", date: "2026-07-10" },
  { name: "GraphNN-v3 Model Card", type: "PDF", size: "912 KB", date: "2026-07-08" },
];

function Page() {
  return (
    <div className="space-y-8">
      <PageHeader title="Reports" subtitle="Generate, download, and share research-grade reports"
        icon={<FileText className="w-5 h-5 text-primary" />}
        actions={
          <button className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium text-white"
            style={{ background: "var(--gradient-primary)" }}>
            Generate report
          </button>
        }
      />

      <div className="grid md:grid-cols-3 gap-4">
        {[
          { title: "Research Report", desc: "Full explainability, charts, methodology", icon: "📄" },
          { title: "Batch CSV", desc: "All predictions in machine-readable format", icon: "📊" },
          { title: "Executive Summary", desc: "Board-ready PDF with key metrics", icon: "📈" },
        ].map(t => (
          <GlassCard key={t.title}>
            <div className="text-3xl">{t.icon}</div>
            <div className="mt-3 font-semibold">{t.title}</div>
            <div className="text-xs text-muted-foreground mt-1">{t.desc}</div>
            <button className="mt-4 text-xs text-primary hover:underline">Create →</button>
          </GlassCard>
        ))}
      </div>

      <GlassCard hover={false}>
        <h3 className="font-semibold mb-4">Download history</h3>
        <table className="w-full text-sm">
          <thead className="text-xs text-muted-foreground uppercase border-b border-border/50">
            <tr>
              <th className="text-left py-3 font-medium">Report</th>
              <th className="text-left py-3 font-medium">Type</th>
              <th className="text-left py-3 font-medium">Size</th>
              <th className="text-left py-3 font-medium">Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {REPORTS.map(r => (
              <tr key={r.name} className="hover:bg-accent/30">
                <td className="py-3 font-medium">{r.name}</td>
                <td className="py-3"><span className="text-[10px] uppercase font-semibold px-2 py-1 rounded bg-muted">{r.type}</span></td>
                <td className="py-3 font-mono text-xs text-muted-foreground">{r.size}</td>
                <td className="py-3 text-muted-foreground">{r.date}</td>
                <td className="py-3 text-right">
                  <button className="inline-flex items-center gap-1 text-xs text-primary hover:underline"><Download className="w-3 h-3" /> Download</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  );
}
