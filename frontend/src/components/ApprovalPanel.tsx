import { useState } from "react";
import type { ExecutionView } from "../services/api";

export default function ApprovalPanel({ interrupt, onDecide }: {
  interrupt: NonNullable<ExecutionView["interrupt"]>;
  onDecide: (s: "approved" | "edited" | "rejected", body?: string) => void;
}) {
  const [body, setBody] = useState(interrupt.draft.body);
  const edited = body !== interrupt.draft.body;
  return (
    <div className="rounded-xl border-2 border-amber-300 bg-amber-50 p-4 text-sm">
      <div className="mb-1 font-semibold">Approval required: send briefing email</div>
      <div className="text-xs text-slate-600">To: {interrupt.draft.to.join(", ") || "(none)"} · Subject: {interrupt.draft.subject}</div>
      <textarea className="mt-2 w-full rounded-md border bg-white p-2" rows={7} value={body} onChange={(e) => setBody(e.target.value)} />
      <div className="mt-3 flex gap-2">
        <button onClick={() => onDecide(edited ? "edited" : "approved", edited ? body : undefined)}
          className="rounded-md bg-emerald-600 px-3 py-1.5 text-white">{edited ? "Approve edited" : "Approve"}</button>
        <button onClick={() => onDecide("rejected")} className="rounded-md bg-rose-600 px-3 py-1.5 text-white">Reject</button>
      </div>
    </div>
  );
}
