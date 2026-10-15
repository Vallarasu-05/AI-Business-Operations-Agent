import type { Evidence } from "../services/api";

export default function EvidencePanel({ items }: { items: Evidence[] }) {
  return (
    <details className="rounded-xl border bg-white p-4 text-sm">
      <summary className="cursor-pointer font-medium">Evidence ({items.length})</summary>
      <table className="mt-3 w-full text-left text-xs">
        <thead className="text-slate-500"><tr><th className="py-1">ID</th><th>Source</th><th>Claim</th><th>Conf.</th></tr></thead>
        <tbody>
          {items.map((e) => (
            <tr key={e.id} className="border-t align-top">
              <td className="py-1 pr-2 font-mono">{e.id}</td>
              <td className="pr-2">{e.source}<div className="text-slate-400">{e.source_id}</div></td>
              <td className="pr-2">{e.claim}</td>
              <td>{e.confidence.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}
