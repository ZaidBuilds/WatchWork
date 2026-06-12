export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export type ContentItem = {
  id: string;
  platform: string;
  source_url: string;
  title: string | null;
  channel_name: string | null;
  thumbnail_url: string | null;
  status: "pending" | "transcribing" | "analyzing" | "ready" | "failed";
  error_message: string | null;
  created_at: string;
};

export type Task = {
  id: string;
  title: string;
  description: string | null;
  category: string;
  priority: "low" | "medium" | "high";
  estimated_minutes: number | null;
  is_done: boolean;
};

export type Plan = {
  id: string;
  summary: string;
  key_concepts: string[];
  completion_pct: number;
  tasks: Task[];
};

export type ContentDetail = ContentItem & {
  transcript_preview: string | null;
  plan: Plan | null;
};

export type AuthUser = {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
  name: string | null;
};

export type Job = {
  id: string;
  content_item_id: string;
  status: "pending" | "running" | "completed" | "failed";
  result: string | null;
  error_message: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
};

export type PaginatedResponse<T> = {
  items: T[];
  total: number;
  offset: number;
  limit: number;
};

function isClient(): boolean {
  return typeof window !== "undefined";
}

function getAuthToken(): string | null {
  if (!isClient()) return null;
  try {
    return localStorage.getItem("action_engine_token");
  } catch {
    return null;
  }
}

export function setAuthToken(token: string) {
  if (!isClient()) return;
  localStorage.setItem("action_engine_token", token);
}

export function clearAuthToken() {
  if (!isClient()) return;
  try {
    localStorage.removeItem("action_engine_token");
    localStorage.removeItem("action_engine_user");
  } catch {
    // silently ignore
  }
}

export function getStoredUser(): AuthUser | null {
  if (!isClient()) return null;
  try {
    const raw = localStorage.getItem("action_engine_user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    clearAuthToken();
    return null;
  }
}

export function storeUser(user: AuthUser) {
  if (!isClient()) return;
  localStorage.setItem("action_engine_user", JSON.stringify(user));
  setAuthToken(user.access_token);
}

function authHeaders(): Record<string, string> {
  const token = getAuthToken();
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (res.status === 401) {
    clearAuthToken();
    throw new Error("UNAUTHORIZED");
  }
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`);
  }
  return res.json();
}

export async function apiPatch<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  if (res.status === 401) {
    clearAuthToken();
    throw new Error("UNAUTHORIZED");
  }
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`);
  }
  return res.json();
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: authHeaders(),
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 401) {
    clearAuthToken();
    throw new Error("UNAUTHORIZED");
  }
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status}`);
  }
  return res.json();
}

export async function apiLogin(email: string, password: string): Promise<AuthUser> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail || "Login failed");
  }
  const data: AuthUser = await res.json();
  storeUser(data);
  return data;
}

export async function apiRegister(email: string, password: string, name?: string): Promise<AuthUser> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, name }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Registration failed" }));
    throw new Error(err.detail || "Registration failed");
  }
  const data: AuthUser = await res.json();
  storeUser(data);
  return data;
}

export async function pollJob(jobId: string, onDone: (job: Job) => void, onError: (msg: string) => void) {
  const maxAttempts = 120;
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const job = await apiGet<Job>(`/jobs/${jobId}`);
      if (job.status === "completed" || job.status === "failed") {
        onDone(job);
        return;
      }
    } catch {
      onError("Failed to check job status.");
      return;
    }
    await new Promise((r) => setTimeout(r, 2000));
  }
  onError("Job timed out.");
}
