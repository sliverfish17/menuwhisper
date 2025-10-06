"use client";

import { API } from "@/lib/api";
import { useEffect, useState } from "react";

type Item = {
  id: string;
  title: string | null;
  desc?: string | null;
  price_cents: number | null;
  currency: string | null;
};

export default function MenuClient({
  restaurant,
  items,
  restaurantId,
}: {
  restaurant: { id: string; name: string };
  items: Item[];
  restaurantId: string;
}) {
  // user identity (храним в localStorage)
  const [email, setEmail] = useState<string>("");
  const [userId, setUserId] = useState<string | null>(null);
  useEffect(() => {
    const e = localStorage.getItem("mw_email") || "";
    const u = localStorage.getItem("mw_user_id");
    if (e) setEmail(e);
    if (u) setUserId(u);
  }, []);

  async function sendFeedback(menu_item_id: string, liked: boolean) {
    // если userId неизвестен — используем email, API вернёт user_id
    const body: any = { menu_item_id, liked };
    if (userId) body.user_id = userId;
    else if (email) body.email = email;
    const r = await fetch(`${API}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const j = await r.json();
    if (r.ok && j.user_id) {
      setUserId(j.user_id);
      localStorage.setItem("mw_user_id", j.user_id);
    }
  }

  const [q, setQ] = useState("");
  const [recs, setRecs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function fetchRecs() {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      params.set("restaurant_id", restaurantId);
      params.set("k", "8");
      if (userId) params.set("user_id", userId);
      const r = await fetch(`${API}/recommend?` + params.toString(), {
        cache: "no-store",
      });
      const j = await r.json();
      setRecs(j.items || []);
    } finally {
      setLoading(false);
    }
  }

  const nice = (cents: number | null, cur: string | null) =>
    cents != null && cur ? `${(cents / 100).toFixed(2)} ${cur}` : "";

  return (
    <main className="p-8 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold">{restaurant?.name ?? "Menu"}</h1>
        <div className="flex items-center gap-2">
          <input
            className="border rounded px-2 py-1"
            placeholder="your@email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              localStorage.setItem("mw_email", e.target.value);
            }}
          />
          <span className="text-xs opacity-70">
            {userId ? `user: ${userId.slice(0, 8)}…` : "no user yet"}
          </span>
        </div>
      </div>

      {/* Поиск/рекомендации */}
      <div className="border rounded p-3 space-y-2">
        <div className="flex gap-2">
          <input
            className="border rounded px-2 py-1 flex-1"
            placeholder="e.g. spicy tomato pasta"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          <button
            onClick={fetchRecs}
            className="px-3 py-2 border rounded"
            disabled={loading}
          >
            {loading ? "Loading…" : "Recommend"}
          </button>
        </div>
        {recs.length > 0 && (
          <ul className="grid gap-2">
            {recs.map((r) => (
              <li key={r.id} className="border rounded p-3">
                <div className="flex items-center justify-between">
                  <b>{r.title || "Untitled"}</b>
                  <span className="text-sm opacity-70">
                    {nice(r.price_cents, r.currency)}
                  </span>
                </div>
                {r.desc && <p className="text-sm opacity-80 mt-1">{r.desc}</p>}
                <div className="text-xs opacity-60 mt-1">
                  score: {r.score?.toFixed(3)}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Список блюд с лайками */}
      <ul className="grid gap-3">
        {items.map((i) => (
          <li key={i.id} className="border rounded p-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold">{i.title || "Untitled"}</div>
                {i.desc && <div className="text-sm opacity-80">{i.desc}</div>}
              </div>
              <div className="text-right">
                <div className="font-mono">
                  {nice(i.price_cents, i.currency)}
                </div>
                <div className="mt-2 flex gap-2 justify-end">
                  <button
                    onClick={() => sendFeedback(i.id, true)}
                    className="px-2 py-1 border rounded"
                  >
                    👍 Like
                  </button>
                  <button
                    onClick={() => sendFeedback(i.id, false)}
                    className="px-2 py-1 border rounded"
                  >
                    👎 Dislike
                  </button>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}
