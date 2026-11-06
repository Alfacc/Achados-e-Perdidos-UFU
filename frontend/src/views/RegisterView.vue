<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { parseApiError } from "../utils/errors";
import AuthLayout from "../components/AuthLayout.vue";

const auth = useAuthStore();
const router = useRouter();

const form = reactive({ name: "", email: "", password: "", confirm: "" });
const errors = ref({});
const message = ref("");
const loading = ref(false);

const rules = computed(() => [
  { label: "Pelo menos 8 caracteres", ok: form.password.length >= 8 },
  { label: "Uma letra maiúscula", ok: /\p{Lu}/u.test(form.password) },
  { label: "Uma letra minúscula", ok: /\p{Ll}/u.test(form.password) },
  { label: "Um número", ok: /\d/.test(form.password) },
]);
const passwordOk = computed(() => rules.value.every((r) => r.ok));

async function submit() {
  errors.value = {};
  message.value = "";
  if (form.password !== form.confirm) {
    errors.value = { confirm: "As senhas não conferem." };
    return;
  }
  if (!passwordOk.value) {
    errors.value = { password: "A senha não atende aos requisitos abaixo." };
    return;
  }
  loading.value = true;
  try {
    await auth.register({ name: form.name, email: form.email, password: form.password });
    router.push({ name: "home" });
  } catch (e) {
    const parsed = parseApiError(e);
    errors.value = parsed.fields;
    message.value = parsed.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <AuthLayout>
    <section class="card">
      <h1>Criar conta</h1>
      <form @submit.prevent="submit">
        <label>Nome
          <input v-model="form.name" required autocomplete="name" />
          <small v-if="errors.name" class="error">{{ errors.name }}</small>
        </label>
        <label>E-mail UFU
          <input v-model="form.email" type="email" placeholder="voce@ufu.br" required autocomplete="email" />
          <small v-if="errors.email" class="error">{{ errors.email }}</small>
        </label>
        <label>Senha
          <input v-model="form.password" type="password" required autocomplete="new-password" />
          <ul class="rules">
            <li v-for="r in rules" :key="r.label" :class="{ ok: r.ok }">
              {{ r.ok ? "✓" : "•" }} {{ r.label }}
            </li>
          </ul>
          <small v-if="errors.password" class="error">{{ errors.password }}</small>
        </label>
        <label>Confirmar senha
          <input v-model="form.confirm" type="password" required autocomplete="new-password" />
          <small v-if="errors.confirm" class="error">{{ errors.confirm }}</small>
        </label>
        <p v-if="message && !Object.keys(errors).length" class="error">{{ message }}</p>
        <button class="btn" :disabled="loading">{{ loading ? "Criando..." : "Cadastrar" }}</button>
      </form>
    </section>
  </AuthLayout>
</template>