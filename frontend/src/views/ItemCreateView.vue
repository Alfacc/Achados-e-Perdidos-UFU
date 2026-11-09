<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { parseApiError } from "../utils/errors";

// Mesmos limites do back-end (models.Item e settings.MAX_PHOTO_MB).
const MAX_DESCRIPTION = 1000;
const MAX_PHOTO_MB = 5;

// Data de hoje no fuso do navegador. toISOString() usa UTC e, depois das 21h
// em Brasília, já devolveria o dia seguinte (que o back-end recusa como futuro).
function localToday() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

const router = useRouter();
const today = localToday();

const categories = ref([]);
const categoriesError = ref("");
const form = reactive({ title: "", description: "", category: "", location: "", date_occurred: today });
const photo = ref(null);
const photoPreview = ref("");
const errors = ref({});
const message = ref("");
const loading = ref(false);

async function loadCategories() {
  categoriesError.value = "";
  try {
    const { data } = await api.get("/categories/");
    categories.value = data;
  } catch (e) {
    categoriesError.value = parseApiError(e).message;
  }
}

onMounted(loadCategories);

function setPreview(file) {
  if (photoPreview.value) URL.revokeObjectURL(photoPreview.value);
  photoPreview.value = file ? URL.createObjectURL(file) : "";
}

onBeforeUnmount(() => setPreview(null));

function onFile(event) {
  const file = event.target.files[0] || null;
  let error = "";
  if (file && !file.type.startsWith("image/")) error = "Escolha um arquivo de imagem (JPG, PNG...).";
  else if (file && file.size > MAX_PHOTO_MB * 1024 * 1024) error = `A foto deve ter no máximo ${MAX_PHOTO_MB} MB.`;

  if (error) event.target.value = "";
  errors.value = { ...errors.value, photo: error };
  photo.value = error ? null : file;
  setPreview(photo.value);
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
    router.push({ name: "home", query: { cadastrado: "1" } });
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
    <p class="muted subtitle">Quanto mais detalhes, maior a chance de alguém reconhecer o seu objeto.</p>
    <form @submit.prevent="submit">
      <label>O que você perdeu?
        <input v-model="form.title" :aria-invalid="!!errors.title" maxlength="120" placeholder="Ex.: Garrafa térmica azul" required />
        <small v-if="errors.title" class="error">{{ errors.title }}</small>
      </label>
      <label>Categoria
        <select v-model="form.category" :aria-invalid="!!errors.category" :disabled="!categories.length" required>
          <option value="" disabled>Selecione...</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <small v-if="categoriesError" class="error">
          {{ categoriesError }}
          <button type="button" class="link-btn" @click="loadCategories">Tentar de novo</button>
        </small>
        <small v-if="errors.category" class="error">{{ errors.category }}</small>
      </label>
      <label>Descrição
        <textarea
          v-model="form.description"
          :aria-invalid="!!errors.description"
          rows="4"
          :maxlength="MAX_DESCRIPTION"
          placeholder="Cor, marca, características..."
          required
        />
        <small class="muted counter">{{ form.description.length }}/{{ MAX_DESCRIPTION }}</small>
        <small v-if="errors.description" class="error">{{ errors.description }}</small>
      </label>
      <label>Onde perdeu?
        <input v-model="form.location" :aria-invalid="!!errors.location" maxlength="150" placeholder="Ex.: Bloco 1B, sala 101" required />
        <small v-if="errors.location" class="error">{{ errors.location }}</small>
      </label>
      <label>Quando perdeu?
        <input v-model="form.date_occurred" :aria-invalid="!!errors.date_occurred" type="date" :max="today" required />
        <small v-if="errors.date_occurred" class="error">{{ errors.date_occurred }}</small>
      </label>
      <label>Foto (opcional, até {{ MAX_PHOTO_MB }} MB)
        <input type="file" accept="image/*" :aria-invalid="!!errors.photo" @change="onFile" />
        <img v-if="photoPreview" :src="photoPreview" alt="Prévia da foto" class="thumb" />
        <small v-if="errors.photo" class="error">{{ errors.photo }}</small>
      </label>
      <p v-if="message" class="error" role="alert">{{ message }}</p>
      <div class="row actions">
        <RouterLink to="/" class="btn btn-ghost">Cancelar</RouterLink>
        <button class="btn" :disabled="loading || !!categoriesError">{{ loading ? "Salvando..." : "Cadastrar" }}</button>
      </div>
    </form>
  </section>
</template>

<style scoped>
h1 {
    margin: 0 0 4px;
}

.subtitle {
    margin: 0 0 20px;
    font-size: 14px;
}

.actions {
    justify-content: flex-end;
    margin-top: 4px;
}
</style>
