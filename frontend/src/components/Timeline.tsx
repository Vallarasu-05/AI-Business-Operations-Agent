import type { ExecutionView } from "../services/api";

const LABEL: Record<string, string> = {
  understand_request: "Understand request", find_meetings: "Calendar", identify_customer: "Customer identification",
  research_crm: "CRM", research_email: "Gmail", research_documents: "Documents", research_sheets: "Sales data",
  research_web: "Web research", validate_evidence: "Evidence validation", analyze_customer: "Analysis",
  identify_risks: "Risk detection", generate_topics: "Recommended topics", generate_briefing: "Briefing",
  quality_check: "Quality check", human_review: "Human approval", deliver: "Delivery",
};

export default function Timeline({ ex }: { ex: ExecutionView }) {
  const done = new Set(ex.steps.map((s) => s.node));
  const detail = Object.fromEntries(ex.steps.map((s) => [s.node, s.detail]));
  const firstPending = ex.steps_order.find((n) => !done.has(n));
  return (
    <ol className="space-y-1.5 rounded-xl border bg-white p-4 text-sm">
      {ex.steps_order.map((n) => {
        const isDone = done.has(n);
        const waiting = ex.status === "waiting_approval" && n === "human_review";
        const running = ex.status === "running" && n === firstPending;
        const icon = isDone ? "✓" : waiting ? "⏸" : running ? "⏳" : "·";
        const cls = isDone ? "text-emerald-700" : waiting ? "text-amber-600" : running ? "text-indigo-600" : "text-slate-400";
        return (
          <li key={n} className={`flex gap-2 ${cls}`}>
            <span className="w-4 text-center">{icon}</span>
            <span>{LABEL[n] ?? n}</span>
            {detail[n] && <span className="text-xs text-slate-400">({detail[n]})</span>}
          </li>
        );
      })}
    </ol>
  );
}
