"use client";

import { API } from "@/lib/api";
import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState("My Restaurant");
  const [currency, setCurrency] = useState("PLN");
  const [lang, setLang] = useState("eng");
  const [resp, setResp] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setErr(null);
    try {
      const fd = new FormData();
      fd.append("image", file);
      fd.append("restaurant_name", name);
      fd.append("currency", currency);
      fd.append("lang", lang);
      const r = await fetch(`${API}/ingest/menu`, { method: "POST", body: fd });
      const j = await r.json();
      if (!r.ok) throw new Error(j?.detail || r.statusText);
      setResp(j);
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Upload a Menu</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block"
          required
        />
        <div className="flex gap-2">
          <input
            className="border rounded px-2 py-1 flex-1"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Restaurant name"
          />
          <input
            className="border rounded px-2 py-1 w-24"
            value={currency}
            onChange={(e) => setCurrency(e.target.value)}
            placeholder="PLN"
          />
          <input
            className="border rounded px-2 py-1 w-28"
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            placeholder="eng or eng+pol"
          />
        </div>
        <button
          disabled={!file || loading}
          className="px-3 py-2 border rounded"
        >
          {loading ? "Processing..." : "Ingest menu"}
        </button>
      </form>

      {err && <p className="text-red-600">{err}</p>}

      {resp && (
        <div className="border rounded p-3">
          <p className="mb-2">
            Saved items: <b>{resp.items_saved}</b>, embedded:{" "}
            <b>{resp.embedded}</b>
          </p>
          <a className="underline" href={`/menu/${resp.restaurant_id}`}>
            Open menu →
          </a>
          <pre className="mt-3 bg-gray-100 p-2 rounded text-sm overflow-auto">
            {JSON.stringify(resp.preview, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
