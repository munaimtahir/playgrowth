const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

type ListResponse<T> = { results: T[] } | T[];

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  return apiRequest<T>(path, 'POST', body);
}

export async function apiPatch<T>(path: string, body: unknown): Promise<T> {
  return apiRequest<T>(path, 'PATCH', body);
}

export async function apiDelete(path: string): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`DELETE ${path} failed`);
}

export async function apiUpload<T>(path: string, formData: FormData): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error(`POST ${path} failed`);
  return res.json();
}

export async function getList<T>(path: string): Promise<T[]> {
  const data = await apiGet<ListResponse<T>>(path);
  return Array.isArray(data) ? data : data.results;
}

async function apiRequest<T>(path: string, method: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `${method} ${path} failed`);
  }
  return res.json();
}

export { API_BASE };
