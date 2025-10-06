type MenuItem = {
  id: string;
  title: string | null;
  description?: string | null;
  price_cents: number | null;
  currency: string | null;
};

export default async function MenuPage({ params }: { params: { id: string } }) {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${api}/menu/${params.id}`, { cache: "no-store" });
  if (!res.ok) {
    return (
      <main className="p-8">
        <h1 className="text-2xl font-bold">Menu</h1>
        <p className="text-red-600">
          Failed to load menu: {res.status} {res.statusText}
        </p>
      </main>
    );
  }
  const data = await res.json();
  const items: MenuItem[] = data.items ?? [];

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">{data.restaurant?.name ?? "Menu"}</h1>
      <ul className="grid gap-4">
        {items.map((i) => (
          <li key={i.id} className="border rounded p-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">{i.title ?? "Untitled"}</h2>
              {i.price_cents != null && i.currency && (
                <span>
                  {(i.price_cents / 100).toFixed(2)} {i.currency}
                </span>
              )}
            </div>
            {("description" in i ? i.description : (i as any).desc) && (
              <p className="text-sm opacity-80 mt-2">
                {
                  ("description" in i
                    ? i.description
                    : (i as any).desc) as string
                }
              </p>
            )}
          </li>
        ))}
      </ul>
    </main>
  );
}
