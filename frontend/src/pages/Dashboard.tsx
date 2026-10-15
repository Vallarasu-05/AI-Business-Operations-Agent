import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatBox from "../components/ChatBox";
import MeetingCard from "../components/MeetingCard";
import { api, type Meeting } from "../services/api";

export default function Dashboard() {
  const nav = useNavigate();
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  useEffect(() => { api.tomorrow().then((r) => setMeetings(r.meetings)).catch((e) => setErr(String(e))); }, []);

  const run = async (text: string) => {
    setBusy(true);
    try { nav(`/execution/${(await api.run(text)).execution_id}`); }
    catch (e) { setErr(String(e)); setBusy(false); }
  };
  return (
    <div className="space-y-6">
      <ChatBox onRun={run} busy={busy} />
      {err && <div className="rounded-md bg-rose-50 p-3 text-sm text-rose-700">{err} (is the backend running on :8000?)</div>}
      <section>
        <h2 className="mb-2 font-semibold">Upcoming meetings</h2>
        <div className="space-y-2">
          {meetings.map((m) => <MeetingCard key={m.event_id} m={m} onPrepare={() => run(`Prepare tomorrow's sales meeting with ${m.title.split(" - ")[0]}`)} />)}
          {meetings.length === 0 && <div className="text-sm text-slate-500">No meetings tomorrow.</div>}
        </div>
      </section>
    </div>
  );
}
