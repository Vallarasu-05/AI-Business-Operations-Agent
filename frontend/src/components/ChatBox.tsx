import { useState } from "react";

export default function ChatBox({ onRun, busy }: { onRun: (text: string) => void; busy?: boolean }) {
  const [text, setText] = useState("Prepare tomorrow's sales meeting with ABC Corporation");
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <label className="mb-2 block text-sm font-medium">What would you like me to prepare?</label>
      <textarea className="w-full rounded-md border p-2 text-sm" rows={2} value={text} onChange={(e) => setText(e.target.value)} />
      <button disabled={busy || !text.trim()} onClick={() => onRun(text)}
        className="mt-3 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50">
        {busy ? "Starting…" : "Run Agent"}
      </button>
    </div>
  );
}
