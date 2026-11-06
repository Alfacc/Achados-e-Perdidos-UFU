<script setup>
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { parseApiError } from "../utils/errors";
import AuthLayout from "../components/AuthLayout.vue";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const form = reactive({ email: "", password: "" });
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(form.email, form.password);
    router.push(route.query.redirect || { name: "home" });
  } catch (e) {
    error.value = parseApiError(e).message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <AuthLayout>
    <section class="card">
      <h1>Entrar</h1>
      <form @submit.prevent="submit">
        <label>E-mail UFU
          <input v-model="form.email" type="email" placeholder="voce@ufu.br" required autocomplete="email" />
        </label>
        <label>Senha
          <input v-model="form.password" type="password" required autocomplete="current-password" />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="btn" :disabled="loading">{{ loading ? "Entrando..." : "Entrar" }}</button>
      </form>
    </section>
  </AuthLayout>
</template>