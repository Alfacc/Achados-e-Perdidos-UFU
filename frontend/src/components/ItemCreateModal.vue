<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from "vue";
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

// Modal aberto pela Home: avisa o objeto criado ("created") para entrar na lista sem recarregar.
// O mesmo formulário serve para as duas histórias: "LOST" (perdi) e "FOUND" (encontrei).
const props = defineProps({
  type: { type: String, default: "LOST", validator: (v) => ["LOST", "FOUND"].includes(v) },
});
const emit = defineEmits(["created", "close"]);

const TEXTS = {
  LOST: {
    heading: "Cadastrar objeto perdido",
    subtitle: "Quanto mais detalhes, maior a chance de alguém reconhecer o seu objeto.",
    title: "O que você perdeu?",
    titlePlaceholder: "Ex.: Garrafa térmica azul",
    location: "Onde perdeu?",
    date: "Quando perdeu?",
  },
  FOUND: {
    heading: "Cadastrar objeto encontrado",
    subtitle: "Descreva o objeto e onde ele foi encontrado para o dono conseguir reconhecê-lo.",
    title: "O que você encontrou?",
    titlePlaceholder: "Ex.: Carteira preta",
    location: "Onde encontrou?",
    date: "Quando encontrou?",
  },
};
const t = TEXTS[props.type];
const dialog = ref(null);
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

onMounted(() => {
  dialog.value.showModal(); // <dialog> nativo: Esc fecha, foco fica preso no modal
  loadCategories();
});

function onCancel(event) {
  if (loading.value) event.preventDefault(); // não fecha no meio do envio
}

// Clique no fundo escurecido (fora do conteúdo) fecha o modal.
function onBackdropClick(event) {
  if (event.target === dialog.value && !loading.value) dialog.value.close();
}

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
    body.append("type", props.type);
    Object.entries(form).forEach(([k, v]) => body.append(k, v));
    if (photo.value) body.append("photo", photo.value);
    const { data } = await api.post("/items/", body);
    emit("created", data);
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
  <dialog
    ref="dialog"
    class="modal"
    aria-labelledby="item-modal-title"
    @cancel="onCancel"
    @close="emit('close')"
    @click="onBackdropClick"
  >
    <div class="modal-body">
      <button type="button" class="modal-close" aria-label="Fechar" :disabled="loading" @click="dialog.close()">×</button>
      <h1 id="item-modal-title">{{ t.heading }}</h1>
      <p class="muted subtitle">{{ t.subtitle }}</p>
      <form @submit.prevent="submit">
        <label>{{ t.title }}
          <input v-model="form.title" :aria-invalid="!!errors.title" maxlength="120" :placeholder="t.titlePlaceholder" required />
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
        <label>{{ t.location }}
          <input v-model="form.location" :aria-invalid="!!errors.location" maxlength="150" placeholder="Ex.: Bloco 1B, sala 101" required />
          <small v-if="errors.location" class="error">{{ errors.location }}</small>
        </label>
        <label>{{ t.date }}
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
          <button type="button" class="btn btn-ghost" :disabled="loading" @click="dialog.close()">Cancelar</button>
          <button class="btn" :disabled="loading || !!categoriesError">{{ loading ? "Salvando..." : "Cadastrar" }}</button>
        </div>
      </form>
    </div>
  </dialog>
</template>

<style scoped>
.modal {
    width: min(520px, calc(100% - 32px));
    max-height: calc(100dvh - 32px);
    padding: 0;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--card);
    color: var(--text);
    box-shadow: 0 20px 48px rgba(16, 24, 40, 0.2);
}

.modal::backdrop {
    background: rgba(16, 24, 40, 0.45);
}

.modal-body {
    position: relative;
    padding: 20px;
}

.modal-close {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 32px;
    height: 32px;
    border: 0;
    border-radius: 8px;
    background: none;
    color: var(--muted);
    font-size: 22px;
    line-height: 1;
    cursor: pointer;
}

.modal-close:hover:not(:disabled) {
    background: var(--bg);
    color: var(--text);
}

h1 {
    margin: 0 0 4px;
    padding-right: 32px;
    font-size: 1.4rem;
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
