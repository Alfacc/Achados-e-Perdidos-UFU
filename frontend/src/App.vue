<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

// Login e cadastro têm layout próprio (AuthLayout), sem o topo do app.
const isAuthPage = computed(() => !!route.meta.guestOnly);

function logout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <RouterView v-if="isAuthPage" />
  <template v-else>
    <header class="topbar">
      <RouterLink to="/" class="brand">
        <img src="/logo.svg" alt="" class="brand-logo" />
        <span>Achados e Perdidos <span class="brand-accent">UFU</span></span>
      </RouterLink>
      <nav v-if="auth.isAuthenticated">
        <span class="user-name muted" :title="auth.user?.email">{{ auth.user?.name }}</span>
        <button class="btn btn-ghost btn-sm" @click="logout">Sair</button>
      </nav>
    </header>
    <main class="container">
      <RouterView />
    </main>
  </template>
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

.brand-accent {
    color: var(--primary);
}

.user-name {
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

@media (max-width: 600px) {
    .topbar {
        padding: 10px 16px;
    }

    .brand > span {
        font-size: 15px;
    }

    .user-name {
        display: none;
    }
}
</style>
