"use client";

import { API } from "@/lib/api";
import { useState } from "react";

export default function SeedPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function seedDemo() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/menu/seed`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          restaurant_name: "Demo Restaurant",
          items: [
            {
              title: "Spaghetti Carbonara",
              desc: "Creamy pasta with bacon and eggs",
              price_cents: 4500,
              currency: "PLN",
            },
            {
              title: "Margherita Pizza",
              desc: "Tomato sauce, mozzarella, fresh basil",
              price_cents: 3800,
              currency: "PLN",
            },
            {
              title: "Caesar Salad",
              desc: "Romaine lettuce, parmesan, croutons",
              price_cents: 3200,
              currency: "PLN",
            },
            {
              title: "Beef Steak",
              desc: "Grilled ribeye with herbs",
              price_cents: 8500,
              currency: "PLN",
            },
            {
              title: "Chocolate Cake",
              desc: "Rich chocolate dessert",
              price_cents: 2500,
              currency: "PLN",
            },
          ],
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || res.statusText);
      setResult(data);
    } catch (e: any) {
      setError(e.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Seed Demo Data</h1>

      <button
        onClick={seedDemo}
        disabled={loading}
        className="px-4 py-2 border rounded bg-blue-50 hover:bg-blue-100"
      >
        {loading ? "Creating..." : "Create Demo Restaurant"}
      </button>

      {error && <p className="text-red-600">{error}</p>}

      {result && (
        <div className="border rounded p-4">
          <p className="mb-2">
            Created restaurant with <b>{result.count}</b> items
          </p>
          <a
            className="underline text-blue-600"
            href={`/menu/${result.restaurant_id}`}
          >
            View Menu →
          </a>
        </div>
      )}
    </main>
  );
}
