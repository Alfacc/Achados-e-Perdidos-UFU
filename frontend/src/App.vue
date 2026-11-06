<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
const router = useRouter();

function logout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <header class="topbar">
    <RouterLink to="/" class="brand">
      <img src="/logo.svg" alt="" class="brand-logo" />
      <span>Achados e Perdidos UFU</span>
    </RouterLink>
    <nav v-if="auth.isAuthenticated">
      <span class="muted">{{ auth.user?.name }}</span>
      <button class="btn btn-ghost" @click="logout">Sair</button>
    </nav>
  </header>
  <main class="container">
    <RouterView />
  </main>
</template>

<style scoped>
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-logo {
    width: 36px;
    height: 36px;
}
</style>