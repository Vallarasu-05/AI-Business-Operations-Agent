import { useEffect, useState } from "react";
import MeetingCard from "../components/MeetingCard";
import { api, type Meeting as M } from "../services/api";

export default function Meeting() {
  const [data, setData] = useState<{ date: string; meetings: M[] } | null>(null);
  useEffect(() => { api.tomorrow().then(setData); }, []);
  return (
    <div className="space-y-2">
      <h1 className="text-lg font-semibold">Meetings on {data?.date}</h1>
      {data?.meetings.map((m) => <MeetingCard key={m.event_id} m={m} />)}
    </div>
  );
}
