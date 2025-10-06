"use server";

async function seedSample() {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${api}/menu/seed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    body: JSON.stringify({
      restaurant_name: "Pasta Mia",
      items: [
        {
          title: "Spaghetti Carbonara",
          desc: "Creamy sauce, pancetta",
          price_cents: 4500,
          currency: "PLN",
        },
        {
          title: "Margherita Pizza",
          desc: "Tomato, mozzarella, basil",
          price_cents: 3800,
          currency: "PLN",
        },
      ],
    }),
  });
  if (!res.ok) throw new Error(`Seed failed: ${res.status} ${res.statusText}`);
  return res.json() as Promise<{ restaurant_id: string; count: number }>;
}

export default async function Page() {
  const data = await seedSample();

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">Seed OK</h1>
      <p>
        Created items: <b>{data.count}</b>
      </p>
      <p>
        Restaurant ID:{" "}
        <code className="px-2 py-1 bg-gray-100 rounded">
          {data.restaurant_id}
        </code>
      </p>
      <a
        className="inline-block px-3 py-2 rounded border"
        href={`/menu/${data.restaurant_id}`}
      >
        View menu →
      </a>
    </main>
  );
}
