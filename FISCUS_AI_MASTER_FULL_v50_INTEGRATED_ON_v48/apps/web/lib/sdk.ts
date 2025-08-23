export const API = process.env.NEXT_PUBLIC_API_BASE as string
export async function refresh(){ await fetch('/api/auth/refresh', { method:'POST' }) }
export async function authHeaders(){ await refresh(); const token = document.cookie.split('access_token=')[1]?.split(';')[0]; return { Authorization: 'Bearer ' + token } }
