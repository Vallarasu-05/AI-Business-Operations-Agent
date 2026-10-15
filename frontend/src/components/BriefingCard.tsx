import type { ReactNode } from "react";

/** Minimal markdown renderer for the briefing (headings, bullets, bold). */
function inline(s: string): ReactNode[] {
  return s.split(/(\*\*[^*]+\*\*|\[E\d+\])/g).map((p, i) =>
    p.startsWith("**") ? <strong key={i}>{p.slice(2, -2)}</strong>
    : /^\[E\d+\]$/.test(p) ? <sup key={i} className="mx-0.5 rounded bg-indigo-50 px-1 text-[10px] text-indigo-700">{p.slice(1, -1)}</sup>
    : p);
}

export default function BriefingCard({ markdown }: { markdown: string }) {
  return (
    <article className="space-y-1 rounded-xl border bg-white p-5 text-sm leading-relaxed">
      {markdown.split("\n").map((line, i) => {
        if (line.startsWith("# ")) return <h1 key={i} className="mb-2 text-xl font-semibold">{line.slice(2)}</h1>;
        if (line.startsWith("## ")) return <h2 key={i} className="mt-4 border-b pb-1 text-base font-semibold">{line.slice(3)}</h2>;
        if (line.startsWith("- ")) return <div key={i} className="ml-4 list-item list-disc">{inline(line.slice(2))}</div>;
        if (line.trim() === "") return null;
        return <div key={i}>{inline(line.trim())}</div>;
      })}
    </article>
  );
}
