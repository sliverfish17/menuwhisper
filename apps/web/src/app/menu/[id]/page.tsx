import { API } from "@/lib/api";
import MenuClient from "./ui";

export default async function MenuPage({ params }: { params: { id: string } }) {
  const res = await fetch(`${API}/menu/${params.id}`, { cache: "no-store" });
  if (!res.ok) {
    return (
      <main className="p-8">
        Failed to load menu: {res.status} {res.statusText}
      </main>
    );
  }
  const data = await res.json();
  return (
    <MenuClient
      restaurant={data.restaurant}
      items={data.items}
      restaurantId={params.id}
    />
  );
}
