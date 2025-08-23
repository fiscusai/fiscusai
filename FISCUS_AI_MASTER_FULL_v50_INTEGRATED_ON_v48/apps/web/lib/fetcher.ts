export async function fetchServer<T>(url: string, revalidateSec: number = 60): Promise<T> {
  const res = await fetch(url, { next: { revalidate: revalidateSec } });
  if (!res.ok) throw new Error(`Fetch failed ${res.status}`);
  return res.json() as Promise<T>;
}
