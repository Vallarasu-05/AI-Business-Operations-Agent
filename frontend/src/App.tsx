import { Link, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Execution from "./pages/Execution";
import Meeting from "./pages/Meeting";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <Link to="/" className="text-lg font-semibold">AI Business Operations Agent</Link>
          <nav className="flex gap-4 text-sm text-slate-600">
            <Link to="/">Dashboard</Link>
            <Link to="/meetings">Meetings</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/meetings" element={<Meeting />} />
          <Route path="/execution/:id" element={<Execution />} />
        </Routes>
      </main>
    </div>
  );
}
