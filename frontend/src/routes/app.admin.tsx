import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard, AnimatedCounter } from "@/components/premium/glass-card";
import { Users, Shield, KeyRound, Server } from "lucide-react";

export const Route = createFileRoute("/app/admin")({ component: Page });

const USERS = [
  { name: "Dr. Emily Sinclair", role: "Owner", status: "active" },
  { name: "Marcus Reeves", role: "Admin", status: "active" },
  { name: "Priya Patel", role: "Researcher", status: "active" },
  { name: "James Okonkwo", role: "Researcher", status: "invited" },
];

function Page() {
  return (
    <div className="space-y-8">
      <PageHeader title="Admin Panel" subtitle="Users, roles, API keys, deployment, and system health"
        icon={<Shield className="w-5 h-5 text-primary" />} />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Active users", value: 148, icon: Users },
          { label: "API keys", value: 24, icon: KeyRound },
          { label: "GPUs online", value: 12, icon: Server },
          { label: "Storage (TB)", value: 8.4, decimals: 1, icon: Server },
        ].map(s => (
          <GlassCard key={s.label}>
            <div className="flex items-center justify-between">
              <s.icon className="w-4 h-4 text-primary" />
              <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Live</span>
            </div>
            <div className="mt-4 text-3xl font-semibold"><AnimatedCounter value={s.value} decimals={s.decimals ?? 0} /></div>
            <div className="mt-1 text-xs text-muted-foreground">{s.label}</div>
          </GlassCard>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-4">
        <GlassCard hover={false} className="lg:col-span-2">
          <h3 className="font-semibold mb-4">Team members</h3>
          <table className="w-full text-sm">
            <thead className="text-xs text-muted-foreground uppercase border-b border-border/50">
              <tr>
                <th className="text-left py-3 font-medium">Name</th>
                <th className="text-left py-3 font-medium">Role</th>
                <th className="text-left py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {USERS.map(u => (
                <tr key={u.name} className="hover:bg-accent/30">
                  <td className="py-3 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full text-xs font-semibold text-white grid place-items-center"
                      style={{ background: "var(--gradient-ai)" }}>
                      {u.name.split(" ").map(n => n[0]).join("").slice(0, 2)}
                    </div>
                    {u.name}
                  </td>
                  <td className="py-3 text-muted-foreground">{u.role}</td>
                  <td className="py-3">
                    <span className="text-[10px] uppercase font-semibold px-2 py-1 rounded-full"
                      style={{ background: `oklch(from var(--color-${u.status === "active" ? "success" : "warning"}) l c h / 0.15)`, color: `var(--color-${u.status === "active" ? "success" : "warning"})` }}>
                      {u.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </GlassCard>

        <GlassCard hover={false}>
          <h3 className="font-semibold mb-4">System health</h3>
          <div className="space-y-4">
            {[
              { l: "API latency", v: "42ms", t: "success" },
              { l: "GPU utilization", v: "78%", t: "warning" },
              { l: "DB response", v: "12ms", t: "success" },
              { l: "Uptime (30d)", v: "99.98%", t: "success" },
            ].map(h => (
              <div key={h.l} className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">{h.l}</span>
                <span className="font-mono">
                  <span className="inline-block w-1.5 h-1.5 rounded-full mr-2" style={{ background: `var(--color-${h.t})`, boxShadow: `0 0 6px var(--color-${h.t})` }} />
                  {h.v}
                </span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
