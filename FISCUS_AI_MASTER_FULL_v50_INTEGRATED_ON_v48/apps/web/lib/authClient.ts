export function getAuthHeaders() {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem('fiscus_auth') || '{}';
    const obj = JSON.parse(raw);
    const headers: Record<string,string> = {};
    if (obj.token) headers['Authorization'] = `Bearer ${obj.token}`;
    if (obj.role) headers['X-User-Role'] = obj.role;
    if (obj.org) headers['X-Org'] = obj.org;
    return headers;
  } catch {
    return {};
  }
}
