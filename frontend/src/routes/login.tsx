import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { GlassCard } from "@/components/premium/glass-card";
import { FloatingMolecules } from "@/components/premium/three-d";
import { Atom, Github } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/login")({ component: Login });

function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");

  return (
    <div className="min-h-screen relative overflow-hidden mesh-bg grid place-items-center px-4">
      <FloatingMolecules />
      <div className="absolute inset-0 grid-bg opacity-30" />
      <div className="relative w-full max-w-md">
        <Link to="/" className="flex items-center gap-2 justify-center mb-8">
          <div className="w-9 h-9 rounded-lg grid place-items-center" style={{ background: "var(--gradient-ai)" }}>
            <Atom className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold tracking-tight">DrugAI</span>
        </Link>

        <GlassCard hover={false} className="p-8">
          <h1 className="text-2xl font-semibold tracking-tight text-center">Welcome back</h1>
          <p className="text-sm text-muted-foreground text-center mt-1">Sign in to your workspace</p>

          <form onSubmit={(e) => { e.preventDefault(); nav({ to: "/app" }); }} className="mt-8 space-y-4">
            <div>
              <label className="text-xs uppercase tracking-wider text-muted-foreground">Email</label>
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                className="mt-2 w-full px-4 py-2.5 bg-muted/40 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm" />
            </div>
            <div>
              <label className="text-xs uppercase tracking-wider text-muted-foreground">Password</label>
              <input type="password" required value={pw} onChange={e => setPw(e.target.value)}
                className="mt-2 w-full px-4 py-2.5 bg-muted/40 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm" />
            </div>
            <div className="flex items-center justify-between text-xs">
              <label className="flex items-center gap-2 text-muted-foreground">
                <input type="checkbox" className="accent-primary" /> Remember me
              </label>
              <a href="#" className="text-primary hover:underline">Forgot password?</a>
            </div>
            <button type="submit" className="w-full py-2.5 rounded-full text-sm font-medium text-white"
              style={{ background: "var(--gradient-primary)", boxShadow: "0 10px 30px oklch(0.68 0.19 245 / 0.4)" }}>
              Sign in
            </button>

            <div className="relative py-2">
              <div className="absolute inset-0 flex items-center"><div className="w-full h-px bg-border" /></div>
              <div className="relative flex justify-center text-xs uppercase"><span className="bg-card px-2 text-muted-foreground">Or</span></div>
            </div>

            <button type="button" className="w-full py-2.5 rounded-full glass text-sm inline-flex items-center justify-center gap-2">
              <Github className="w-4 h-4" /> Continue with GitHub
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Don't have an account? <Link to="/signup" className="text-primary hover:underline">Sign up</Link>
          </p>
        </GlassCard>
      </div>
    </div>
  );
}
