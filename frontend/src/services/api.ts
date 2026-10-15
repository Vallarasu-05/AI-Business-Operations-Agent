export interface Step { node: string; status: string; at: number; detail: string }
export interface Evidence { id: string; claim: string; source: string; source_id: string; date?: string | null; confidence: number; topic: string }
export interface Attendee { name: string; email: string }
export interface Meeting { event_id: string; title: string; date: string; start: string; end: string; location?: string; attendees: Attendee[] }
export interface ExecutionView {
  id: string; request: string; status: "queued" | "running" | "waiting_approval" | "completed" | "failed";
  steps: Step[]; steps_order: string[]; error: string | null;
  interrupt: { action: string; draft: { to: string[]; subject: string; body: string }; quality: Record<string, unknown> } | null;
  state: {
    customer?: { name: string; industry?: string };
    briefing_markdown?: string;
    validated_evidence?: Evidence[];
    quality?: { factual_accuracy: number; source_coverage: number; hallucination_risk: number; passed: boolean; issues: string[] };
    errors?: { node: string; msg: string }[];
    delivery?: { pdf?: string; email?: { status: string } };
  };
}

const KEY = import.meta.env.VITE_API_KEY as string | undefined;
async function j<T>(url: string, init?: RequestInit): Promise<T> {
  const r = await fetch(url, { ...init, headers: { "Content-Type": "application/json", ...(KEY ? { "X-API-Key": KEY } : {}), ...(init?.headers || {}) } });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}

export const api = {
  run: (request: string) => j<{ execution_id: string }>("/api/agent/run", { method: "POST", body: JSON.stringify({ request }) }),
  execution: (id: string) => j<ExecutionView>(`/api/executions/${id}`),
  approve: (id: string, status: "approved" | "edited" | "rejected", email_body?: string) =>
    j<{ ok: boolean }>(`/api/approval/${id}`, { method: "POST", body: JSON.stringify({ status, email_body }) }),
  tomorrow: () => j<{ date: string; meetings: Meeting[] }>("/api/meetings/tomorrow"),
};
