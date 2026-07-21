import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "motion/react";
import { ArrowRight, Atom, Brain, Cpu, FlaskConical, Github, Shield, Sparkles, Star, Twitter, Zap } from "lucide-react";
import { DnaHelix, FloatingMolecules } from "@/components/premium/three-d";
import { GlassCard, AnimatedCounter } from "@/components/premium/glass-card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

export const Route = createFileRoute("/")({
  component: Landing,
});

const stats = [
  { label: "AI Accuracy", value: 96.4, suffix: "%" },
  { label: "Prediction Speed", value: 42, suffix: "ms" },
  { label: "Compounds Screened", value: 12.8, suffix: "M", decimals: 1 },
  { label: "Research Labs", value: 320, suffix: "+" },
];

const features = [
  { icon: FlaskConical, title: "Toxicity Prediction", desc: "State-of-the-art transformer models predict hepatotoxicity, cardiotoxicity, and mutagenicity with 96%+ accuracy." },
  { icon: Atom, title: "Drug–Target Binding", desc: "Deep graph networks estimate binding affinity across 20K+ human protein targets in milliseconds." },
  { icon: Brain, title: "Explainable AI", desc: "SHAP & LIME visualizations reveal exactly which molecular substructures drive every prediction." },
  { icon: Zap, title: "ADMET Profiling", desc: "Full absorption, distribution, metabolism, excretion, and toxicity scoring in a single pass." },
  { icon: Shield, title: "Enterprise Security", desc: "SOC 2 Type II, HIPAA-ready infrastructure with private VPC deployment for regulated workloads." },
  { icon: Cpu, title: "MLflow Integration", desc: "Reproducible experiments, model registry, and one-click deployment to production GPU clusters." },
];

const testimonials = [
  { quote: "DrugAI cut our lead identification timeline from 18 months to 6 weeks. It's a paradigm shift.", author: "Dr. Sarah Chen", role: "VP Discovery, Meridian Bio" },
  { quote: "The explainability layer is what finally got our medicinal chemists to trust ML predictions.", author: "Marcus Reeves", role: "Head of Computational Chem, Novaxis" },
  { quote: "We've screened 2.3M compounds through DrugAI in Q1 alone. Nothing else scales like this.", author: "Dr. Priya Patel", role: "CSO, Helios Therapeutics" },
];

const plans = [
  { name: "Research", price: "$0", desc: "For academic labs and individual researchers", features: ["1,000 predictions / month", "Public model catalog", "Community support"], cta: "Start free" },
  { name: "Team", price: "$1,499", desc: "For biotech startups and small teams", features: ["500K predictions / month", "Private workspaces", "Custom model training", "Priority support"], cta: "Start trial", featured: true },
  { name: "Enterprise", price: "Custom", desc: "For pharma & regulated environments", features: ["Unlimited predictions", "Private VPC deployment", "SOC 2 + HIPAA", "Dedicated GPU cluster", "24/7 SLA"], cta: "Contact sales" },
];

const faqs = [
  { q: "What models power DrugAI's predictions?", a: "We ensemble Graph Neural Networks, Transformer-XL architectures pretrained on 500M molecules, and gradient-boosted models — dynamically selected per task." },
  { q: "Can I bring my own private compound library?", a: "Yes. Enterprise workspaces support fully private ingestion via encrypted SDF, CSV, or API upload. Your data never leaves your VPC." },
  { q: "How accurate are toxicity predictions?", a: "On the Tox21 benchmark we hit 96.4% ROC-AUC. Real-world performance is calibrated per assay with active learning." },
  { q: "Do you integrate with our existing MLOps stack?", a: "Native MLflow, Weights & Biases, and Kubeflow integrations. REST + Python SDK for everything else." },
];

function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <header className="fixed top-0 inset-x-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg grid place-items-center animate-pulse-glow"
              style={{ background: "var(--gradient-ai)" }}>
              <Atom className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold tracking-tight">DrugAI</span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition-colors">Platform</a>
            <a href="#pricing" className="hover:text-foreground transition-colors">Pricing</a>
            <a href="#faq" className="hover:text-foreground transition-colors">FAQ</a>
            <a href="#" className="hover:text-foreground transition-colors">Docs</a>
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/login" className="text-sm text-muted-foreground hover:text-foreground">Sign in</Link>
            <Link to="/app" className="inline-flex items-center gap-1.5 text-sm font-medium px-4 py-2 rounded-full text-white transition-transform hover:scale-105"
              style={{ background: "var(--gradient-primary)", boxShadow: "0 8px 24px oklch(0.68 0.19 245 / 0.4)" }}>
              Launch app <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative pt-40 pb-32 overflow-hidden mesh-bg">
        <div className="absolute inset-0 grid-bg opacity-30" />
        <FloatingMolecules />
        <div className="max-w-7xl mx-auto px-6 relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs mb-6">
                <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "var(--color-success)" }} />
                <span className="text-muted-foreground">Series B — $52M led by Andreessen Horowitz</span>
              </div>
              <h1 className="text-5xl lg:text-7xl font-semibold tracking-tighter leading-[1.02]">
                Accelerating<br />
                <span className="gradient-text-ai animate-gradient" style={{ backgroundSize: "200% 200%" }}>drug discovery</span>
                <br />with AI.
              </h1>
              <p className="mt-6 text-lg text-muted-foreground max-w-xl leading-relaxed">
                DrugAI is the intelligence layer for modern pharmaceutical R&D. Predict toxicity, model
                protein binding, and explain every molecular decision — from lead identification to IND.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link to="/app" className="group inline-flex items-center gap-2 px-6 py-3 rounded-full text-sm font-medium text-white transition-transform hover:scale-[1.03]"
                  style={{ background: "var(--gradient-primary)", boxShadow: "0 10px 30px oklch(0.68 0.19 245 / 0.5)" }}>
                  <Sparkles className="w-4 h-4" /> Start free trial
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </Link>
                <a href="#features" className="inline-flex items-center gap-2 px-6 py-3 rounded-full glass text-sm font-medium hover:bg-accent transition-colors">
                  See the platform
                </a>
              </div>
              <div className="mt-10 flex items-center gap-6 text-xs text-muted-foreground">
                <div className="flex items-center gap-1.5"><Shield className="w-4 h-4" /> SOC 2 Type II</div>
                <div className="flex items-center gap-1.5"><Shield className="w-4 h-4" /> HIPAA-ready</div>
                <div className="flex items-center gap-1.5"><Shield className="w-4 h-4" /> GDPR</div>
              </div>
            </motion.div>

            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8, delay: 0.2 }}
              className="relative h-[520px]">
              <div className="absolute inset-0 rounded-3xl overflow-hidden glass">
                <div className="absolute inset-0" style={{ background: "radial-gradient(circle at 50% 40%, oklch(0.68 0.22 295 / 0.25), transparent 60%)" }} />
                <DnaHelix className="absolute inset-0 flex items-center justify-center" />
              </div>
              {/* floating metric cards */}
              <motion.div animate={{ y: [0, -12, 0] }} transition={{ duration: 5, repeat: Infinity }}
                className="absolute -left-4 top-16 glass rounded-2xl p-4 elegant-shadow w-56">
                <div className="text-xs text-muted-foreground">Prediction confidence</div>
                <div className="text-2xl font-semibold mt-1"><AnimatedCounter value={96.4} decimals={1} suffix="%" /></div>
                <div className="mt-2 h-1.5 rounded-full bg-muted overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: "96%" }} transition={{ duration: 2 }}
                    className="h-full rounded-full" style={{ background: "var(--gradient-primary)" }} />
                </div>
              </motion.div>
              <motion.div animate={{ y: [0, 12, 0] }} transition={{ duration: 6, repeat: Infinity, delay: 1 }}
                className="absolute -right-4 bottom-20 glass rounded-2xl p-4 elegant-shadow w-56">
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span className="w-1.5 h-1.5 rounded-full" style={{ background: "var(--color-success)" }} />
                  Active model: GraphNN-v3
                </div>
                <div className="text-2xl font-semibold mt-1 font-mono">42<span className="text-sm text-muted-foreground ml-1">ms</span></div>
                <div className="text-xs text-muted-foreground">avg inference latency</div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 border-y border-border/50 bg-card/30">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((s, i) => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }} transition={{ delay: i * 0.1 }} className="text-center">
              <div className="text-4xl md:text-5xl font-semibold tracking-tight gradient-text">
                <AnimatedCounter value={s.value} suffix={s.suffix} decimals={s.decimals ?? 0} />
              </div>
              <div className="mt-2 text-xs uppercase tracking-widest text-muted-foreground">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-32">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="text-center max-w-2xl mx-auto">
            <div className="text-xs uppercase tracking-widest text-primary mb-3">Platform</div>
            <h2 className="text-4xl md:text-5xl font-semibold tracking-tighter">
              The complete AI stack for<br />modern drug discovery.
            </h2>
            <p className="mt-4 text-muted-foreground">
              One platform — from molecular property prediction to production deployment.
            </p>
          </motion.div>

          <div className="mt-16 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }} transition={{ delay: i * 0.05 }}>
                <GlassCard className="h-full">
                  <div className="w-11 h-11 rounded-xl grid place-items-center mb-4"
                    style={{ background: "linear-gradient(135deg, oklch(0.68 0.19 245 / 0.2), oklch(0.68 0.22 295 / 0.15))" }}>
                    <f.icon className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="font-semibold text-lg tracking-tight">{f.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 bg-card/30 border-y border-border/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <div className="text-xs uppercase tracking-widest text-primary mb-3">Trusted by leaders</div>
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tighter">Powering research at the world's top labs.</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((t) => (
              <GlassCard key={t.author} className="flex flex-col" hover={false}>
                <div className="flex gap-0.5 mb-4">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-primary text-primary" />
                  ))}
                </div>
                <p className="text-sm leading-relaxed flex-1">"{t.quote}"</p>
                <div className="mt-6 pt-4 border-t border-border/50">
                  <div className="font-medium text-sm">{t.author}</div>
                  <div className="text-xs text-muted-foreground">{t.role}</div>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-32">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <div className="text-xs uppercase tracking-widest text-primary mb-3">Pricing</div>
            <h2 className="text-4xl md:text-5xl font-semibold tracking-tighter">Simple, usage-based pricing.</h2>
            <p className="mt-4 text-muted-foreground">Start free. Scale to millions of predictions without changing a line of code.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {plans.map((p) => (
              <motion.div key={p.name} whileHover={{ y: -6 }} transition={{ type: "spring", stiffness: 300 }}
                className={`relative rounded-2xl p-8 ${p.featured ? "glass elegant-shadow" : "glass"}`}
                style={p.featured ? { boxShadow: "0 0 40px oklch(0.68 0.19 245 / 0.3), 0 0 0 1px oklch(0.68 0.19 245 / 0.4)" } : undefined}>
                {p.featured && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-semibold uppercase tracking-widest px-3 py-1 rounded-full text-white"
                    style={{ background: "var(--gradient-ai)" }}>Most popular</div>
                )}
                <div className="text-sm text-muted-foreground">{p.name}</div>
                <div className="mt-3 text-4xl font-semibold tracking-tight">{p.price}<span className="text-sm text-muted-foreground font-normal">{p.name !== "Enterprise" && "/mo"}</span></div>
                <div className="mt-2 text-sm text-muted-foreground">{p.desc}</div>
                <ul className="mt-6 space-y-3 text-sm">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2">
                      <div className="w-4 h-4 rounded-full grid place-items-center mt-0.5 shrink-0" style={{ background: "oklch(0.72 0.18 155 / 0.2)" }}>
                        <div className="w-1.5 h-1.5 rounded-full" style={{ background: "var(--color-success)" }} />
                      </div>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                <button className={`w-full mt-8 py-2.5 rounded-full text-sm font-medium transition-transform hover:scale-[1.02] ${p.featured ? "text-white" : "glass"}`}
                  style={p.featured ? { background: "var(--gradient-primary)" } : undefined}>
                  {p.cta}
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="py-24 border-t border-border/50">
        <div className="max-w-3xl mx-auto px-6">
          <div className="text-center mb-12">
            <div className="text-xs uppercase tracking-widest text-primary mb-3">FAQ</div>
            <h2 className="text-4xl font-semibold tracking-tighter">Common questions</h2>
          </div>
          <Accordion type="single" collapsible className="glass rounded-2xl p-2">
            {faqs.map((f, i) => (
              <AccordionItem key={i} value={`i-${i}`} className="border-border/50 px-4">
                <AccordionTrigger className="text-left hover:no-underline">{f.q}</AccordionTrigger>
                <AccordionContent className="text-muted-foreground">{f.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="max-w-5xl mx-auto px-6">
          <div className="relative rounded-3xl overflow-hidden p-16 text-center glass elegant-shadow">
            <div className="absolute inset-0 mesh-bg opacity-80" />
            <div className="relative">
              <h2 className="text-4xl md:text-5xl font-semibold tracking-tighter">Ready to accelerate discovery?</h2>
              <p className="mt-4 text-muted-foreground max-w-lg mx-auto">Join 320+ research teams using DrugAI to bring life-saving therapies to patients faster.</p>
              <Link to="/app" className="mt-8 inline-flex items-center gap-2 px-8 py-3 rounded-full text-sm font-medium text-white transition-transform hover:scale-105"
                style={{ background: "var(--gradient-primary)", boxShadow: "0 10px 40px oklch(0.68 0.19 245 / 0.5)" }}>
                Launch platform <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-border/50 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-wrap gap-6 items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-md grid place-items-center" style={{ background: "var(--gradient-ai)" }}>
              <Atom className="w-4 h-4 text-white" />
            </div>
            <span>© 2026 DrugAI Intelligence, Inc.</span>
          </div>
          <div className="flex items-center gap-6">
            <a href="#" className="hover:text-foreground">Privacy</a>
            <a href="#" className="hover:text-foreground">Terms</a>
            <a href="#" className="hover:text-foreground">Security</a>
            <a href="#" className="hover:text-foreground"><Twitter className="w-4 h-4" /></a>
            <a href="#" className="hover:text-foreground"><Github className="w-4 h-4" /></a>
          </div>
        </div>
      </footer>
    </div>
  );
}
