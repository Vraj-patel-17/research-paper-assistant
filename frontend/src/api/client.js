import { getToken, removeToken } from "../auth/auth";
const API_URL = import.meta.env.VITE_API_URL;

async function request(endpoint, options = {}) {
  const token = getToken();
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && {
        Authorization: `Bearer ${token}`,
      }),
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
    throw new Error(data?.detail || "Request failed");
  }

  return data;
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
};