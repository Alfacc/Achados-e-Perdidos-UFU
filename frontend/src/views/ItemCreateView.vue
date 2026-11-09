<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { parseApiError } from "../utils/errors";

// Mesmos limites do back-end (models.Item e settings.MAX_PHOTO_MB).
const MAX_DESCRIPTION = 1000;
const MAX_PHOTO_MB = 5;
const FORM_FIELDS = ["title", "category", "description", "location", "date_occurred", "photo"];

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
const loadingCategories = ref(false);
const form = reactive({ title: "", description: "", category: "", location: "", date_occurred: today });
const photo = ref(null);
const photoPreview = ref("");
const errors = ref({});
const message = ref("");
const loading = ref(false);

async function loadCategories() {
  categoriesError.value = "";
  loadingCategories.value = true;
  try {
    const { data } = await api.get("/categories/");
    categories.value = data;
  } catch (e) {
    categoriesError.value = parseApiError(e).message;
  } finally {
    loadingCategories.value = false;
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
  const { photo: _, ...rest } = errors.value;
  errors.value = rest;

  if (file && !file.type.startsWith("image/")) {
    errors.value = { ...errors.value, photo: "Escolha um arquivo de imagem (JPG, PNG...)." };
  } else if (file && file.size > MAX_PHOTO_MB * 1024 * 1024) {
    errors.value = { ...errors.value, photo: `A foto deve ter no máximo ${MAX_PHOTO_MB} MB.` };
  }

  if (errors.value.photo) {
    event.target.value = "";
    photo.value = null;
    setPreview(null);
    return;
  }
  photo.value = file;
  setPreview(file);
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
    const { fields, message: general } = parseApiError(e);
    // Erros de campos que não aparecem no formulário (ex.: "type") vão para a mensagem geral.
    const hidden = Object.entries(fields).filter(([k]) => !FORM_FIELDS.includes(k));
    errors.value = Object.fromEntries(Object.entries(fields).filter(([k]) => FORM_FIELDS.includes(k)));
    message.value = hidden.length && !Object.keys(errors.value).length
      ? hidden.map(([, v]) => v).join(" ")
      : general;
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
        <select v-model="form.category" :disabled="loadingCategories || !!categoriesError" required>
          <option value="" disabled>{{ loadingCategories ? "Carregando..." : "Selecione..." }}</option>
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
          rows="4"
          :maxlength="MAX_DESCRIPTION"
          placeholder="Cor, marca, características..."
          required
        />
        <small class="muted counter">{{ form.description.length }}/{{ MAX_DESCRIPTION }}</small>
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
      <label>Foto (opcional, até {{ MAX_PHOTO_MB }} MB)
        <input type="file" accept="image/*" @change="onFile" />
        <img v-if="photoPreview" :src="photoPreview" alt="Prévia da foto" class="thumb" />
        <small v-if="errors.photo" class="error">{{ errors.photo }}</small>
      </label>
      <p v-if="message" class="error" role="alert">{{ message }}</p>
      <div class="row">
        <RouterLink to="/" class="btn btn-ghost">Cancelar</RouterLink>
        <button class="btn" :disabled="loading || !!categoriesError">{{ loading ? "Salvando..." : "Cadastrar" }}</button>
      </div>
    </form>
  </section>
</template>
