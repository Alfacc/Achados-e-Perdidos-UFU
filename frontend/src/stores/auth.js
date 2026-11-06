import { defineStore } from "pinia";
import api, { tokenStorage } from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user") || "null"),
    hasToken: !!tokenStorage.access,
  }),
  getters: {
    isAuthenticated: (state) => state.hasToken,
  },
  actions: {
    async login(email, password) {
      const { data } = await api.post("/auth/login/", { email, password });
      tokenStorage.set({ access: data.access, refresh: data.refresh });
      localStorage.setItem("user", JSON.stringify(data.user));
      this.user = data.user;
      this.hasToken = true;
    },
    async register({ name, email, password }) {
      await api.post("/auth/register/", { name, email, password });
      await this.login(email, password); // já entra logado após o cadastro
    },
    logout() {
      tokenStorage.clear();
      this.user = null;
      this.hasToken = false;
    },
  },
});
