import { Bell, Command, Moon, Search, Sun, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import { useTheme } from "@/providers/theme-provider";
import { CommandPalette } from "@/components/premium/command-palette";
import { motion } from "motion/react";

export function Topbar() {
  const { theme, toggle } = useTheme();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, []);

  return (
    <>
      <header className="sticky top-0 z-20 h-16 border-b border-border/50 bg-background/60 backdrop-blur-xl">
        <div className="h-full px-6 flex items-center gap-4">
          <button
            onClick={() => setOpen(true)}
            className="flex-1 max-w-md flex items-center gap-3 h-10 px-3 rounded-lg glass text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <Search className="w-4 h-4" />
            <span className="flex-1 text-left">Search drugs, models, experiments…</span>
            <kbd className="hidden sm:flex items-center gap-1 text-[10px] font-mono px-1.5 py-0.5 rounded border border-border">
              <Command className="w-3 h-3" /> K
            </kbd>
          </button>

          <div className="flex-1" />

          <div className="hidden md:flex items-center gap-2 h-9 px-3 rounded-full glass text-xs">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" style={{ background: "var(--color-success)" }} />
              <span className="relative inline-flex rounded-full h-2 w-2" style={{ background: "var(--color-success)" }} />
            </span>
            <span className="text-muted-foreground">All systems operational</span>
          </div>

          <button className="relative w-10 h-10 grid place-items-center rounded-lg hover:bg-accent transition-colors">
            <Zap className="w-4 h-4" />
          </button>

          <button className="relative w-10 h-10 grid place-items-center rounded-lg hover:bg-accent transition-colors">
            <Bell className="w-4 h-4" />
            <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-primary animate-pulse" />
          </button>

          <button onClick={toggle} className="relative w-10 h-10 grid place-items-center rounded-lg hover:bg-accent transition-colors">
            <motion.div key={theme} initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} transition={{ duration: 0.3 }}>
              {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </motion.div>
          </button>

          <div className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-semibold text-white"
            style={{ background: "var(--gradient-ai)" }}>
            ES
          </div>
        </div>
      </header>
      <CommandPalette open={open} onOpenChange={setOpen} />
    </>
  );
}
