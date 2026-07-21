import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "motion/react";
import {
  LayoutDashboard, FlaskConical, Atom, Activity, HeartPulse, Sparkles, Search,
  GitCompare, Cpu, BarChart3, FileText, History, Users, Beaker, Brain,
  Settings, ChevronLeft, ChevronRight,
} from "lucide-react";
import { useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Topbar } from "./topbar";

const NAV: { section: string; items: { to: string; label: string; icon: any; badge?: string }[] }[] = [
  {
    section: "Overview",
    items: [
      { to: "/app", label: "Dashboard", icon: LayoutDashboard },
      { to: "/app/analytics", label: "Analytics", icon: BarChart3 },
    ],
  },
  {
    section: "Discovery",
    items: [
      { to: "/app/toxicity", label: "Toxicity Prediction", icon: FlaskConical, badge: "AI" },
      { to: "/app/dti", label: "Drug–Target", icon: Atom },
      { to: "/app/admet", label: "ADMET Profile", icon: Activity },
      { to: "/app/side-effects", label: "Side Effects", icon: HeartPulse },
      { to: "/app/visualization", label: "Molecule Viewer", icon: Beaker },
      { to: "/app/similarity", label: "Similarity Search", icon: Search },
      { to: "/app/recommendation", label: "Recommendations", icon: Sparkles },
    ],
  },
  {
    section: "Intelligence",
    items: [
      { to: "/app/explainability", label: "Explainable AI", icon: Brain },
      { to: "/app/models", label: "Model Comparison", icon: GitCompare },
      { to: "/app/mlflow", label: "MLflow", icon: Cpu },
    ],
  },
  {
    section: "Workspace",
    items: [
      { to: "/app/reports", label: "Reports", icon: FileText },
      { to: "/app/history", label: "History", icon: History },
      { to: "/app/admin", label: "Admin", icon: Users },
    ],
  },
];

export function AppShell({ children }: { children: ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <div className="min-h-screen bg-background mesh-bg">
      <div className="flex">
        <motion.aside
          initial={false}
          animate={{ width: collapsed ? 76 : 268 }}
          transition={{ type: "spring", stiffness: 200, damping: 24 }}
          className="sticky top-0 h-screen border-r border-border/50 bg-sidebar/60 backdrop-blur-xl flex flex-col z-30"
        >
          <div className="h-16 flex items-center gap-3 px-5 border-b border-border/50">
            <div className="w-9 h-9 rounded-lg grid place-items-center relative overflow-hidden"
              style={{ background: "var(--gradient-ai)", boxShadow: "0 0 20px oklch(0.68 0.19 245 / 0.6)" }}>
              <Atom className="w-5 h-5 text-white" />
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <div className="font-semibold tracking-tight text-sm">DrugAI</div>
                <div className="text-[10px] text-muted-foreground uppercase tracking-widest">Intelligence</div>
              </div>
            )}
          </div>

          <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
            {NAV.map((group) => (
              <div key={group.section}>
                {!collapsed && (
                  <div className="px-3 mb-2 text-[10px] font-medium uppercase tracking-widest text-muted-foreground">
                    {group.section}
                  </div>
                )}
                <ul className="space-y-1">
                  {group.items.map((it) => {
                    const active = pathname === it.to || (it.to !== "/app" && pathname.startsWith(it.to));
                    const Icon = it.icon;
                    return (
                      <li key={it.to}>
                        <Link
                          to={it.to}
                          className={cn(
                            "group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                            active
                              ? "bg-sidebar-accent text-sidebar-accent-foreground"
                              : "text-muted-foreground hover:text-foreground hover:bg-sidebar-accent/60",
                          )}
                        >
                          {active && (
                            <motion.span
                              layoutId="sidebar-active"
                              className="absolute inset-0 rounded-lg -z-10"
                              style={{ background: "linear-gradient(90deg, oklch(0.68 0.19 245 / 0.15), transparent)" }}
                            />
                          )}
                          {active && (
                            <span className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[3px] rounded-r-full bg-primary" />
                          )}
                          <Icon className="w-4 h-4 shrink-0" />
                          {!collapsed && (
                            <>
                              <span className="flex-1 truncate">{it.label}</span>
                              {it.badge && (
                                <span className="text-[9px] px-1.5 py-0.5 rounded-full font-mono font-semibold"
                                  style={{ background: "var(--gradient-ai)", color: "white" }}>
                                  {it.badge}
                                </span>
                              )}
                            </>
                          )}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </nav>

          <div className="p-3 border-t border-border/50 space-y-1">
            <Link to="/app/admin" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-sidebar-accent/60">
              <Settings className="w-4 h-4" />
              {!collapsed && <span>Settings</span>}
            </Link>
            <button
              onClick={() => setCollapsed((c) => !c)}
              className="w-full flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-sidebar-accent/60"
            >
              {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
              {!collapsed && <span>Collapse</span>}
            </button>
          </div>
        </motion.aside>

        <div className="flex-1 min-w-0">
          <Topbar />
          <main className="p-6 lg:p-8 max-w-[1600px] mx-auto">{children}</main>
        </div>
      </div>
    </div>
  );
}
