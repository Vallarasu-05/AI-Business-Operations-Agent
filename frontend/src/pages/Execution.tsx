import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ApprovalPanel from "../components/ApprovalPanel";
import BriefingCard from "../components/BriefingCard";
import EvidencePanel from "../components/EvidencePanel";
import Timeline from "../components/Timeline";
import { api, type ExecutionView } from "../services/api";

export default function Execution() {
  const { id = "" } = useParams();
  const [ex, setEx] = useState<ExecutionView | null>(null);
  const [err, setErr] = useState("");

  const load = useCallback(() => api.execution(id).then(setEx).catch((e) => setErr(String(e))), [id]);
  useEffect(() => { load(); }, [load]);
  // poll while the agent is working
  useEffect(() => {
    if (!ex || !["queued", "running"].includes(ex.status)) return;
    const t = setInterval(load, 800);
    return () => clearInterval(t);
  }, [ex, load]);

  const decide = async (s: "approved" | "edited" | "rejected", body?: string) => {
    await api.approve(id, s, body);
    setEx((e) => (e ? { ...e, status: "running", interrupt: null } : e));
    load();
  };

  if (err) return <div className="rounded-md bg-rose-50 p-3 text-sm text-rose-700">{err}</div>;
  if (!ex) return <div className="text-sm text-slate-500">Loading…</div>;
  const st = ex.state;
  return (
    <div className="grid gap-6 md:grid-cols-[260px_1fr]">
      <aside className="space-y-3">
        <Timeline ex={ex} />
        <div className="text-xs text-slate-500">Run {ex.id} · status <b>{ex.status}</b></div>
        {st.quality && (
          <div className={`rounded-xl border p-3 text-xs ${st.quality.passed ? "bg-emerald-50" : "bg-rose-50"}`}>
            <div className="font-semibold">Quality check: {st.quality.passed ? "passed" : "failed"}</div>
            <div>Accuracy {st.quality.factual_accuracy} · Coverage {st.quality.source_coverage} · Halluc. risk {st.quality.hallucination_risk}</div>
            {st.quality.issues.map((i) => <div key={i}>• {i}</div>)}
          </div>
        )}
      </aside>
      <section className="space-y-4">
        {ex.error && <div className="rounded-md bg-rose-50 p-3 text-sm text-rose-700">{ex.error}</div>}
        {st.errors?.map((e, i) => <div key={i} className="rounded-md bg-amber-50 p-2 text-xs text-amber-800">{e.node}: {e.msg}</div>)}
        {ex.status === "waiting_approval" && ex.interrupt && <ApprovalPanel interrupt={ex.interrupt} onDecide={decide} />}
        {st.delivery && (
          <div className="rounded-md bg-emerald-50 p-3 text-sm">
            Delivered. Email: <b>{st.delivery.email?.status}</b>
            {st.delivery.pdf && <> · <a className="underline" href={`/api/briefings/${ex.id}/pdf`} target="_blank">Download PDF</a></>}
          </div>
        )}
        {st.briefing_markdown ? <BriefingCard markdown={st.briefing_markdown} /> : ex.status === "running" && <div className="text-sm text-slate-500">Agent is working…</div>}
        {st.validated_evidence && <EvidencePanel items={st.validated_evidence} />}
      </section>
    </div>
  );
}
