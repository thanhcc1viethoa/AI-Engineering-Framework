// REST client — Antigravity_Build_Guide.md section 11.
export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export function getToken() {
  return sessionStorage.getItem("dashboard_token");
}

export function setToken(token) {
  if (token) sessionStorage.setItem("dashboard_token", token);
  else sessionStorage.removeItem("dashboard_token");
}

async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (response.status === 401) {
    setToken(null);
    throw new Error("UNAUTHORIZED");
  }
  if (!response.ok) {
    let detail = response.statusText;
    try {
      detail = (await response.json()).detail ?? detail;
    } catch {
      // response body was not JSON — keep statusText
    }
    throw new Error(`${response.status}: ${detail}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

function toQueryString(params) {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== "");
  return entries.length ? `?${new URLSearchParams(entries).toString()}` : "";
}

export const api = {
  login: (password) => request("/auth/login", { method: "POST", body: JSON.stringify({ password }) }),
  getSystemStatus: () => request("/system/status"),
  getSystemConfig: () => request("/system/config"),
  getSystemLogs: (lines = 200) => request(`/system/logs${toQueryString({ lines })}`),
  listAgents: () => request("/agents"),
  getAgent: (id) => request(`/agents/${id}`),
  listTasks: (params = {}) => request(`/tasks${toQueryString(params)}`),
  submitTask: (data) => request("/tasks", { method: "POST", body: JSON.stringify(data) }),
  getTask: (id) => request(`/tasks/${id}`),
  cancelTask: (id) => request(`/tasks/${id}`, { method: "DELETE" }),
  executeWorkflow: (data) => request("/workflows", { method: "POST", body: JSON.stringify(data) }),
  getWorkflow: (id) => request(`/workflows/${id}`),
};
