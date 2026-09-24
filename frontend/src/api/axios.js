import axios from "axios";
import { API_URL as BASE_URL } from "../config";
import { useToast } from "../composables/useToast";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Endpoints where a 401 means bad credentials, not an expired access token
const AUTH_ENDPOINTS = /users\/(login|refresh)\/?$/;

export function clearSession() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  localStorage.removeItem("email");
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Shared so that several requests failing at once trigger a single refresh
let refreshPromise = null;

function refreshAccessToken() {
  if (!refreshPromise) {
    const refresh = localStorage.getItem("refresh");
    refreshPromise = axios
      .post(`${BASE_URL}users/refresh/`, { refresh })
      .then((response) => {
        localStorage.setItem("access", response.data.access);
        // Only present if ROTATE_REFRESH_TOKENS is enabled in the backend
        if (response.data.refresh) {
          localStorage.setItem("refresh", response.data.refresh);
        }
      })
      .catch((err) => {
        // The server rejected the refresh token: the session is over
        if (err.response) {
          clearSession();
          window.dispatchEvent(new Event("auth-changed"));
          useToast().warning("Tu sesión ha expirado. Inicia sesión de nuevo.");
        }
        throw err;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;

    if (
      error.response?.status !== 401 ||
      !config ||
      config._retry ||
      AUTH_ENDPOINTS.test(config.url || "") ||
      !localStorage.getItem("refresh")
    ) {
      return Promise.reject(error);
    }

    config._retry = true;

    try {
      await refreshAccessToken();
    } catch (refreshError) {
      // Network error: keep the session and report the original failure
      if (!refreshError.response) {
        return Promise.reject(error);
      }

      // Session expired: retry without token so public endpoints still work
      delete config.headers.Authorization;
      try {
        return await api(config);
      } catch (retryError) {
        if (retryError.response?.status === 401) {
          window.dispatchEvent(new Event("session-expired"));
        }
        return Promise.reject(retryError);
      }
    }

    // New access token is picked up by the request interceptor
    return api(config);
  }
);

export default api;
