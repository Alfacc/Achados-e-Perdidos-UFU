import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Obs.: tokens em localStorage são simples e suficientes para o projeto da disciplina.
// Em produção, o ideal seria cookie HttpOnly (trade-off: proteção contra XSS).
export const tokenStorage = {
  get access() { return localStorage.getItem("access_token"); },
  get refresh() { return localStorage.getItem("refresh_token"); },
  set({ access, refresh }) {
    if (access) localStorage.setItem("access_token", access);
    if (refresh) localStorage.setItem("refresh_token", refresh);
  },
  clear() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },
};

const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  if (tokenStorage.access) config.headers.Authorization = `Bearer ${tokenStorage.access}`;
  return config;
});

// Se o access token expirar, tenta renovar uma vez com o refresh token.
// Várias requisições podem receber 401 ao mesmo tempo: todas aguardam o mesmo refresh.
let refreshing = null;

function refreshAccessToken() {
  refreshing ??= axios
    .post(`${API_URL}/auth/token/refresh/`, { refresh: tokenStorage.refresh })
    .then(({ data }) => {
      tokenStorage.set({ access: data.access, refresh: data.refresh });
      return data.access;
    })
    .finally(() => {
      refreshing = null;
    });
  return refreshing;
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const isAuthCall = original?.url?.includes("/auth/login/") || original?.url?.includes("/auth/token/refresh/");
    if (error.response?.status === 401 && original && !original._retry && !isAuthCall && tokenStorage.refresh) {
      original._retry = true;
      try {
        const access = await refreshAccessToken();
        original.headers.Authorization = `Bearer ${access}`;
        return api(original);
      } catch {
        // Sessão expirada: limpa tudo e volta para o login (o reload também zera o Pinia).
        tokenStorage.clear();
        window.location.assign("/login");
      }
    }
    return Promise.reject(error);
  }
);

export default api;
