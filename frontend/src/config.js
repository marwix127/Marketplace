// Backend API base URL. Set VITE_API_URL in frontend/.env.local to change it (see .env.example)
export const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/").replace(/\/?$/, "/");

// Backend origin, used to build absolute URLs for media files the API returns as relative paths
export const BACKEND_URL = new URL(API_URL).origin;
