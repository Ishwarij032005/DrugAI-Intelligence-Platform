import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { GlassCard } from "@/components/premium/glass-card";
import { FloatingMolecules } from "@/components/premium/three-d";
import { Atom, Check } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/signup")({ component: Signup });

function scorePw(pw: string) {
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}

function Signup() {
  const nav = useNavigate();
  const [pw, setPw] = useState("");
  const s = scorePw(pw);
  const tone = ["destructive", "destructive", "warning", "primary", "success"][s];

  return (
    <div className="min-h-screen relative overflow-hidden mesh-bg grid place-items-center px-4">
      <FloatingMolecules />
      <div className="relative w-full max-w-md">
        <Link to="/" className="flex items-center gap-2 justify-center mb-8">
          <div className="w-9 h-9 rounded-lg grid place-items-center" style={{ background: "var(--gradient-ai)" }}>
            <Atom className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold tracking-tight">DrugAI</span>
        </Link>
        <GlassCard hover={false} className="p-8">
          <h1 className="text-2xl font-semibold tracking-tight text-center">Create your workspace</h1>
          <p className="text-sm text-muted-foreground text-center mt-1">Start with 1,000 free predictions</p>
          <form onSubmit={(e) => { e.preventDefault(); nav({ to: "/app" }); }} className="mt-8 space-y-4">
            <input placeholder="Full name" className="w-full px-4 py-2.5 bg-muted/40 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50" />
            <input type="email" placeholder="Work email" className="w-full px-4 py-2.5 bg-muted/40 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50" />
            <div>
              <input type="password" placeholder="Password" value={pw} onChange={e => setPw(e.target.value)}
                className="w-full px-4 py-2.5 bg-muted/40 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50" />
              <div className="mt-2 flex gap-1">
                {[0, 1, 2, 3].map(i => (
                  <div key={i} className="h-1 flex-1 rounded-full transition-colors" style={{ background: i < s ? `var(--color-${tone})` : "var(--color-muted)" }} />
                ))}
              </div>
              <p className="mt-1 text-[10px] text-muted-foreground">Use 8+ characters with uppercase, number, symbol</p>
            </div>
            <button type="submit" className="w-full py-2.5 rounded-full text-sm font-medium text-white"
              style={{ background: "var(--gradient-primary)" }}>
              <Check className="w-4 h-4 inline mr-1" /> Create account
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account? <Link to="/login" className="text-primary hover:underline">Sign in</Link>
          </p>
        </GlassCard>
      </div>
    </div>
  );
}
