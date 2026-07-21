import { CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from "@/components/ui/command";
import { useNavigate } from "@tanstack/react-router";
import { LayoutDashboard, FlaskConical, Atom, Activity, BarChart3, Brain, Sparkles, Search, GitCompare, History, FileText, Users, Beaker } from "lucide-react";

export function CommandPalette({ open, onOpenChange }: { open: boolean; onOpenChange: (v: boolean) => void }) {
  const navigate = useNavigate();
  const go = (to: string) => { onOpenChange(false); navigate({ to }); };
  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Type a command or search…" />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Navigate">
          <CommandItem onSelect={() => go("/app")}><LayoutDashboard className="mr-2 w-4 h-4" />Dashboard</CommandItem>
          <CommandItem onSelect={() => go("/app/analytics")}><BarChart3 className="mr-2 w-4 h-4" />Analytics</CommandItem>
          <CommandItem onSelect={() => go("/app/toxicity")}><FlaskConical className="mr-2 w-4 h-4" />Toxicity Prediction</CommandItem>
          <CommandItem onSelect={() => go("/app/dti")}><Atom className="mr-2 w-4 h-4" />Drug–Target Interaction</CommandItem>
          <CommandItem onSelect={() => go("/app/admet")}><Activity className="mr-2 w-4 h-4" />ADMET Profile</CommandItem>
          <CommandItem onSelect={() => go("/app/visualization")}><Beaker className="mr-2 w-4 h-4" />Molecule Viewer</CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Intelligence">
          <CommandItem onSelect={() => go("/app/explainability")}><Brain className="mr-2 w-4 h-4" />Explainable AI</CommandItem>
          <CommandItem onSelect={() => go("/app/models")}><GitCompare className="mr-2 w-4 h-4" />Model Comparison</CommandItem>
          <CommandItem onSelect={() => go("/app/similarity")}><Search className="mr-2 w-4 h-4" />Similarity Search</CommandItem>
          <CommandItem onSelect={() => go("/app/recommendation")}><Sparkles className="mr-2 w-4 h-4" />Recommendations</CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Workspace">
          <CommandItem onSelect={() => go("/app/history")}><History className="mr-2 w-4 h-4" />History</CommandItem>
          <CommandItem onSelect={() => go("/app/reports")}><FileText className="mr-2 w-4 h-4" />Reports</CommandItem>
          <CommandItem onSelect={() => go("/app/admin")}><Users className="mr-2 w-4 h-4" />Admin Panel</CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
