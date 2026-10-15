import type { Meeting } from "../services/api";

export default function MeetingCard({ m, onPrepare }: { m: Meeting; onPrepare?: () => void }) {
  return (
    <div className="flex items-center justify-between rounded-lg border bg-white p-3">
      <div>
        <div className="font-medium">{m.start} – {m.end} · {m.title}</div>
        <div className="text-xs text-slate-500">{m.attendees.map((a) => a.name).join(", ")}</div>
      </div>
      {onPrepare && <button onClick={onPrepare} className="rounded-md border px-3 py-1 text-sm hover:bg-slate-50">Prepare</button>}
    </div>
  );
}
