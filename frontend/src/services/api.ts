// Real API service layer connected to FastAPI backend.

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export type Prediction = {
  id: string;
  drug: string;
  smiles: string;
  toxicity: number;
  confidence: number;
  model: string;
  status: "success" | "warning" | "danger";
  createdAt: string;
};

export type ModelStat = {
  id: string;
  name: string;
  type: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc: number;
  latencyMs: number;
};

// Helper for fetching data
async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem("access_token");
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export const drugsApi = {
  async listPredictions(): Promise<Prediction[]> {
    const data = await fetchApi("/predictions/");
    return data.map((item: any) => ({
      id: item.predictionId || item.id,
      drug: item.drugName || item.inputSmiles || "Unknown",
      smiles: item.inputSmiles,
      toxicity: item.toxicityScore || 0,
      confidence: item.confidenceScore || 0,
      model: item.modelUsed,
      status: item.status,
      createdAt: item.createdAt,
    }));
  },

  async predictToxicity(input: { smiles: string }): Promise<{
    toxicity: number;
    confidence: number;
    riskLevel: "low" | "medium" | "high";
    breakdown: { label: string; value: number }[];
    explanation: string;
  }> {
    return fetchApi("/predictions/toxicity", {
      method: "POST",
      body: JSON.stringify(input),
    });
  },

  async admet(smiles?: string): Promise<{ label: string; value: number; note: string }[]> {
    const data = await fetchApi(`/predictions/admet${smiles ? `?smiles=${encodeURIComponent(smiles)}` : ""}`);
    return data;
  },

  async sideEffects(smiles?: string) {
    const data = await fetchApi(`/predictions/side-effects${smiles ? `?smiles=${encodeURIComponent(smiles)}` : ""}`);
    return data;
  },
};

export const modelsApi = {
  async list(): Promise<ModelStat[]> {
    return fetchApi("/models/");
  },
};

export const analyticsApi = {
  async trend() {
    return fetchApi("/analytics/trend?days=14");
  },
  async classDistribution() {
    return fetchApi("/analytics/class-distribution");
  },
};
