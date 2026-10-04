import { getToken, removeToken } from "../auth/auth";
const API_URL = import.meta.env.VITE_API_URL;

// The backend wraps errors as { error: { message } } (or { error: "..." } for
// rate limits), so check those shapes before FastAPI's default { detail }.
function extractMessage(data) {
  if (!data) return null;

  const error = data.error;
  if (typeof error === "string") return error;
  if (Array.isArray(error?.details) && error.details.length) {
    return error.details.map((item) => item.msg).join(", ");
  }
  if (error?.message) return error.message;

  const detail = data.detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg).join(", ");
  return typeof detail === "string" ? detail : null;
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...options.headers,
    },
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    // Response has no JSON body.
  }
  if (response.status === 401) {
    removeToken();
    window.location.href = "/login";
    return;
  }
  if (!response.ok) {
    throw new Error(extractMessage(data) || "Request failed");
  }

  return data;
}

// POST that reads a text/event-stream response. Calls onEvent(parsedJson) for
// every `data:` frame. fetch is used instead of EventSource because
// EventSource can't send an Authorization header or a POST body.
async function stream(endpoint, body, { signal, onEvent } = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
      ...authHeaders(),
    },
    body: JSON.stringify(body),
    signal,
  });

  if (response.status === 401) {
    removeToken();
    window.location.href = "/login";
    return;
  }

  if (!response.ok) {
    let data = null;
    try {
      data = await response.json();
    } catch {
      // Response has no JSON body.
    }
    throw new Error(extractMessage(data) || "Request failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const line = frame.split("\n").find((l) => l.startsWith("data: "));
      if (!line) continue;
      onEvent?.(JSON.parse(line.slice(6)));
    }
  }
}

export const api = {
  get: (endpoint, options = {}) =>
    request(endpoint, {
      ...options,
      method: "GET",
    }),

  post: (endpoint, body, options = {}) =>
    request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(body),
    }),

  put: (endpoint, body, options = {}) =>
    request(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(body),
    }),

  delete: (endpoint, options = {}) =>
    request(endpoint, {
      ...options,
      method: "DELETE",
    }),

  stream,
};