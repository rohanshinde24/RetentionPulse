const API_BASE = import.meta.env.VITE_API_BASE;

export async function predict(data: any) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function explain(data: any, topK = 6) {
  const url = new URL(`${API_BASE}/explain`);
  url.searchParams.set("top_k", String(topK));
  const res = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function gatewayHealth() {
  const res = await fetch(`${API_BASE}/`);
  return res.json();
}
