const API_BASE = import.meta.env.VITE_API_BASE;

export async function predict(data: any) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
