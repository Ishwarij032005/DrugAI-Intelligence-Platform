import { createFileRoute } from "@tanstack/react-router";
import { PageHeader } from "@/components/premium/page-header";
import { GlassCard } from "@/components/premium/glass-card";
import { Cpu, Activity, PlayCircle } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/app/mlflow")({ component: Page });

const RUNS = [
  { id: "482", model: "GraphNN-v3", acc: 0.955, loss: 0.108, epoch: 32, status: "completed", time: "2h 14m" },
  { id: "481", model: "Transformer-XL", acc: 0.94, loss: 0.121, epoch: 20, status: "completed", time: "4h 02m" },
  { id: "480", model: "CNN-Mol", acc: 0.92, loss: 0.148, epoch: 50, status: "completed", time: "1h 48m" },
  { id: "479", model: "GraphNN-v3", acc: 0.94, loss: 0.132, epoch: 28, status: "failed", time: "42m" },
  { id: "478", model: "XGBoost", acc: 0.9, loss: 0.19, epoch: 1, status: "completed", time: "8m" },
];

function Page() {
  const [liveLogs, setLiveLogs] = useState<{ status: string; epoch?: number; loss?: number }[]>([]);
  const [isTraining, setIsTraining] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const startLiveTraining = () => {
    setIsTraining(true);
    setLiveLogs([]);
    
    // Calculate WS URL based on env
    const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
    const wsBase = apiBase.replace("http", "ws");
    
    // Assuming job_id is just random for demonstration
    const jobId = Math.random().toString(36).substring(7);
    
    const ws = new WebSocket(`${wsBase}/ws/training/${jobId}`);
    wsRef.current = ws;
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.status === "training" && data.meta) {
          setLiveLogs(prev => [...prev.slice(-4), { 
            status: "training", 
            epoch: data.meta.current_epoch, 
            loss: data.meta.loss 
          }]);
        } else if (data.status === "completed" || data.status === "failed") {
          setIsTraining(false);
          ws.close();
        }
      } catch (e) {
        console.error("WS parse error", e);
      }
    };
    
    ws.onclose = () => setIsTraining(false);
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  return (
    <div className="space-y-8">
      <PageHeader title="MLflow" subtitle="Experiments, runs, and model registry"
        icon={<Cpu className="w-5 h-5 text-primary" />} />

      <div className="grid lg:grid-cols-4 gap-4">
        <GlassCard>
          <div className="text-xs uppercase text-muted-foreground">Experiments</div>
          <div className="text-3xl font-semibold mt-2">24</div>
        </GlassCard>
        <GlassCard>
          <div className="text-xs uppercase text-muted-foreground">Runs</div>
          <div className="text-3xl font-semibold mt-2">482</div>
        </GlassCard>
        <GlassCard>
          <div className="text-xs uppercase text-muted-foreground">Registered models</div>
          <div className="text-3xl font-semibold mt-2">12</div>
        </GlassCard>
        <GlassCard>
          <div className="text-xs uppercase text-muted-foreground">Artifacts</div>
          <div className="text-3xl font-semibold mt-2">2,412</div>
        </GlassCard>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <GlassCard hover={false} className="h-full">
            <h3 className="font-semibold mb-4">Recent runs</h3>
            <div className="relative">
              <div className="absolute left-3 top-2 bottom-2 w-px bg-border" />
              <ul className="space-y-4">
                {RUNS.map(r => (
                  <li key={r.id} className="flex gap-4 items-start pl-8 relative">
                    <div className="absolute left-1 top-2 w-4 h-4 rounded-full"
                      style={{ background: r.status === "completed" ? "var(--color-success)" : "var(--color-destructive)", boxShadow: `0 0 12px var(--color-${r.status === "completed" ? "success" : "destructive"})` }} />
                    <div className="flex-1 grid grid-cols-6 gap-4 items-center p-3 rounded-lg bg-muted/30">
                      <div>
                        <div className="font-mono text-xs text-muted-foreground">#{r.id}</div>
                        <div className="font-medium text-sm">{r.model}</div>
                      </div>
                      <div className="text-xs"><span className="text-muted-foreground">acc</span> <span className="font-mono">{(r.acc * 100).toFixed(1)}%</span></div>
                      <div className="text-xs"><span className="text-muted-foreground">loss</span> <span className="font-mono">{r.loss}</span></div>
                      <div className="text-xs"><span className="text-muted-foreground">epoch</span> <span className="font-mono">{r.epoch}</span></div>
                      <div className="text-xs text-muted-foreground">{r.time}</div>
                      <div className="text-right">
                        <span className="text-[10px] uppercase font-semibold px-2 py-1 rounded-full"
                          style={{ background: `oklch(from var(--color-${r.status === "completed" ? "success" : "destructive"}) l c h / 0.15)`, color: `var(--color-${r.status === "completed" ? "success" : "destructive"})` }}>
                          {r.status}
                        </span>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </GlassCard>
        </div>
        
        <div>
          <GlassCard hover={false} className="h-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold flex items-center gap-2">
                <Activity className="w-4 h-4 text-primary" /> Live Training
              </h3>
              <Button size="sm" variant="outline" onClick={startLiveTraining} disabled={isTraining}>
                <PlayCircle className="w-4 h-4 mr-2" /> Start Demo
              </Button>
            </div>
            
            <div className="bg-black/60 rounded-md p-4 font-mono text-xs text-green-400 h-64 overflow-y-auto">
              {!isTraining && liveLogs.length === 0 ? (
                <div className="text-muted-foreground text-center h-full flex items-center justify-center">
                  No active training sessions
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="text-blue-400"># Connecting to worker node...</div>
                  {isTraining && <div className="text-blue-400 animate-pulse"># Awaiting epochs...</div>}
                  {liveLogs.map((log, i) => (
                    <div key={i} className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                      [INFO] Epoch {log.epoch}/10 - Loss: {log.loss?.toFixed(4)}
                    </div>
                  ))}
                  {!isTraining && liveLogs.length > 0 && (
                    <div className="text-blue-400 mt-4"># Training job completed. Artifacts saved.</div>
                  )}
                </div>
              )}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
