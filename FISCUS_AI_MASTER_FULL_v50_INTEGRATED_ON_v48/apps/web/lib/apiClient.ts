
export function getAuthHeaders(): Record<string, string> {
  try {
    const raw = typeof window !== 'undefined' ? localStorage.getItem('fiscus_auth') : null;
    if (!raw) return {};
    const obj = JSON.parse(raw);
    const headers: Record<string, string> = {};
    if (obj.token) headers['Authorization'] = `Bearer ${obj.token}`;
    if (obj.role) headers['X-User-Role'] = obj.role;
    if (obj.org) headers['X-Org'] = obj.org;
    return headers;
  } catch { return {}; }
}

export async function apiFetch(input: string, init: RequestInit = {}) {
  const headers = { ...(init.headers || {}), ...getAuthHeaders() };
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const url = input.startsWith('http') ? input : `${base}${input}`;

  let attempt = 0;
  let lastErr: any = null;
  const max = 3;
  while (attempt < max) {
    try {
      const res = await fetch(url, { ...init, headers });
      if (!res.ok) {
        if (res.status >= 500 && attempt < max - 1) {
          await new Promise(r => setTimeout(r, 200 * (attempt + 1)));
          attempt++; continue;
        }
        const text = await res.text();
        throw new Error(`HTTP ${res.status} – ${text}`);
      }
      return res;
    } catch (e) {
      lastErr = e;
      if (attempt >= max - 1) throw e;
      await new Promise(r => setTimeout(r, 200 * (attempt + 1)));
      attempt++;
    }
  }
  throw lastErr;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await apiFetch(path, { method: 'GET' });
  return res.json() as Promise<T>;
}

export async function apiPost<T>(path: string, body?: any): Promise<T> {
  const res = await apiFetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  return res.json() as Promise<T>;
}


export async function apiPut<T>(path: string, body?: any): Promise<T> {
  const res = await apiFetch(path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  return res.json() as Promise<T>;
}

export async function apiDelete<T>(path: string): Promise<T> {
  const res = await apiFetch(path, { method: 'DELETE' });
  try { return await res.json() as T; } catch { return {} as T; }
}


export async function apiPatch<T>(path: string, body?: any): Promise<T> {
  const res = await apiFetch(path, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  try { return await res.json() as T; } catch { return {} as T; }
}

export async function apiDelete<T>(path: string): Promise<T> {
  const res = await apiFetch(path, { method: 'DELETE' });
  try { return await res.json() as T; } catch { return {} as T; }
}
