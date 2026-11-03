
export const API_BASE = (
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "https://asrr.onrender.com"
).replace(/\/+$/, "");

type CsrfResponse = {
  csrfToken?: string;
  csrf_token?: string;
};

async function getCsrfToken(): Promise<string> {
  const response = await fetch(`${API_BASE}/member/csrf/`, {
    method: "GET",
    credentials: "include",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Unable to initialize CSRF protection");
  }

  const data: CsrfResponse = await response.json();

  const token = data.csrfToken ?? data.csrf_token;

  if (typeof token !== "string" || !token) {
    throw new Error("CSRF token missing from backend response");
  }

  return token;
}

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {
  const method = (options.method ?? "GET").toUpperCase();

  const unsafeMethod = [
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
  ].includes(method);

  const headers = new Headers(options.headers);

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (unsafeMethod) {
    const csrfToken = await getCsrfToken();

    headers.set("X-CSRFToken", csrfToken);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    method,
    credentials: "include",
    headers,
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.error ||
      data?.detail ||
      data?.message ||
      `Request failed (${response.status})`
    );
  }

  return data;
}
