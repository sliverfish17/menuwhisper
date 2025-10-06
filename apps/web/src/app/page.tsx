export default async function Home() {
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${api}/health`, { cache: "no-store" }).catch(
    () => null
  );
  const health = res ? await res.json() : { status: "down" };
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">MenuWhisper</h1>
      <div className="flex gap-3">
        <a className="px-3 py-2 border rounded" href="/upload">
          Upload menu
        </a>
        <a className="px-3 py-2 border rounded" href="/seed">
          Seed demo
        </a>
      </div>
      <pre className="mt-4 p-4 bg-gray-100 rounded">
        {JSON.stringify(health, null, 2)}
      </pre>
    </main>
  );
}
