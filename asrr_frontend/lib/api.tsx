export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";


function getCookie(
  name: string
): string | null {

  if (typeof document === "undefined") {
    return null;
  }

  const cookies =
    document.cookie.split(";");

  for (const cookie of cookies) {
    const trimmed =
      cookie.trim();

    if (
      trimmed.startsWith(
        `${name}=`
      )
    ) {
      return decodeURIComponent(
        trimmed.substring(
          name.length + 1
        )
      );
    }
  }

  return null;
}


async function ensureCsrfCookie() {
  let csrfToken =
    getCookie("csrftoken");

  if (csrfToken) {
    return csrfToken;
  }


  await fetch(
    `${API_BASE}/member/csrf/`,
    {
      method: "GET",
      credentials: "include",
    }
  );


  csrfToken =
    getCookie("csrftoken");

  return csrfToken;
}


export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {

  const method =
    (
      options.method ??
      "GET"
    ).toUpperCase();


  const unsafeMethod =
    [
      "POST",
      "PUT",
      "PATCH",
      "DELETE",
    ].includes(method);


  const headers =
    new Headers(
      options.headers
    );


  if (
    !headers.has(
      "Content-Type"
    ) &&
    options.body
  ) {
    headers.set(
      "Content-Type",
      "application/json"
    );
  }


  if (unsafeMethod) {

    const csrfToken =
      await ensureCsrfCookie();


    if (csrfToken) {
      headers.set(
        "X-CSRFToken",
        csrfToken
      );
    }
  }


  const response =
    await fetch(
      `${API_BASE}${endpoint}`,
      {
        ...options,

        credentials:
          "include",

        headers,
      }
    );


  let data = null;


  try {
    data =
      await response.json();

  } catch {
    data = null;
  }


  if (!response.ok) {

    throw new Error(
      data?.error ||
      data?.detail ||
      data?.message ||
      "Something went wrong."
    );
  }


  return data;
}