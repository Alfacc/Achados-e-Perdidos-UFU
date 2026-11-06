<script setup>
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { parseApiError } from "../utils/errors";

const router = useRouter();
const today = new Date().toISOString().slice(0, 10);

const categories = ref([]);
const form = reactive({ title: "", description: "", category: "", location: "", date_occurred: today });
const photo = ref(null);
const errors = ref({});
const message = ref("");
const loading = ref(false);

onMounted(async () => {
  const { data } = await api.get("/categories/");
  categories.value = data;
});

function onFile(event) {
  photo.value = event.target.files[0] || null;
}

async function submit() {
  errors.value = {};
  message.value = "";
  loading.value = true;
  try {
    const body = new FormData();
    body.append("type", "LOST"); // SCRUM-12: objeto perdido
    Object.entries(form).forEach(([k, v]) => body.append(k, v));
    if (photo.value) body.append("photo", photo.value);
    await api.post("/items/", body);
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
  <section class="card narrow">
    <h1>Cadastrar objeto perdido</h1>
    <form @submit.prevent="submit">
      <label>O que você perdeu?
        <input v-model="form.title" maxlength="120" placeholder="Ex.: Garrafa térmica azul" required />
        <small v-if="errors.title" class="error">{{ errors.title }}</small>
      </label>
      <label>Categoria
        <select v-model="form.category" required>
          <option value="" disabled>Selecione...</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <small v-if="errors.category" class="error">{{ errors.category }}</small>
      </label>
      <label>Descrição
        <textarea v-model="form.description" rows="4" placeholder="Cor, marca, características..." required />
        <small v-if="errors.description" class="error">{{ errors.description }}</small>
      </label>
      <label>Onde perdeu?
        <input v-model="form.location" maxlength="150" placeholder="Ex.: Bloco 1B, sala 101" required />
        <small v-if="errors.location" class="error">{{ errors.location }}</small>
      </label>
      <label>Quando perdeu?
        <input v-model="form.date_occurred" type="date" :max="today" required />
        <small v-if="errors.date_occurred" class="error">{{ errors.date_occurred }}</small>
      </label>
      <label>Foto (opcional)
        <input type="file" accept="image/*" @change="onFile" />
        <small v-if="errors.photo" class="error">{{ errors.photo }}</small>
      </label>
      <p v-if="message && !Object.keys(errors).length" class="error">{{ message }}</p>
      <div class="row">
        <RouterLink to="/" class="btn btn-ghost">Cancelar</RouterLink>
        <button class="btn" :disabled="loading">{{ loading ? "Salvando..." : "Cadastrar" }}</button>
      </div>
    </form>
  </section>
</template>
