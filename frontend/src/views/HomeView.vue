<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";
import { parseApiError } from "../utils/errors";
import ItemCreateModal from "../components/ItemCreateModal.vue";

const items = ref([]);
const loading = ref(true);
const error = ref("");
const showCreate = ref(false);
const created = ref(false);

// O objeto recém-criado entra no topo da lista na hora, sem buscar tudo de novo.
function onCreated(item) {
  items.value.unshift(item);
  showCreate.value = false;
  created.value = true;
}

// "2026-11-03" -> "03/11/2026" (sem passar por Date, para não sofrer com fuso horário).
function formatDate(iso) {
  return iso ? iso.split("-").reverse().join("/") : "";
}

async function loadItems() {
  error.value = "";
  loading.value = true;
  try {
    const { data } = await api.get("/items/");
    items.value = data;
  } catch (e) {
    error.value = parseApiError(e).message;
  } finally {
    loading.value = false;
  }
}

onMounted(loadItems);
</script>

<template>
  <section>
    <div class="page-header">
      <div>
        <h1>Objetos cadastrados</h1>
        <p class="muted">Itens perdidos e encontrados no campus.</p>
      </div>
      <button type="button" class="btn" @click="showCreate = true">+ Perdi um objeto</button>
    </div>

    <p v-if="created" class="notice" role="status">
      Objeto cadastrado com sucesso!
      <button type="button" class="notice-close" aria-label="Fechar aviso" @click="created = false">×</button>
    </p>

    <p v-if="loading" class="muted">Carregando...</p>

    <div v-else-if="error" class="card empty">
      <p class="error">{{ error }}</p>
      <button type="button" class="btn btn-ghost btn-sm" @click="loadItems">Tentar de novo</button>
    </div>

    <div v-else-if="!items.length" class="card empty">
      <p><strong>Nenhum objeto cadastrado ainda.</strong></p>
      <p class="muted">Perdeu alguma coisa? Cadastre e aumente as chances de alguém encontrar.</p>
      <button type="button" class="btn btn-sm" @click="showCreate = true">Cadastrar objeto perdido</button>
    </div>

    <ul v-else class="list">
      <li v-for="item in items" :key="item.id" class="card item">
        <img v-if="item.photo" :src="item.photo" :alt="item.title" class="item-photo" loading="lazy" />
        <div v-else class="item-photo item-photo-empty" aria-hidden="true">
          <img src="/logo.svg" alt="" />
        </div>

        <div class="item-body">
          <div class="item-head">
            <strong class="item-title">{{ item.title }}</strong>
            <span class="tags">
              <span v-if="item.status === 'RESOLVED'" class="tag tag-resolved">Resolvido</span>
              <span class="tag" :class="item.type === 'LOST' ? 'tag-lost' : 'tag-found'">
                {{ item.type === "LOST" ? "Perdido" : "Encontrado" }}
              </span>
            </span>
          </div>
          <p class="item-meta muted">
            {{ item.category_name }} · {{ item.location }} · {{ formatDate(item.date_occurred) }}
          </p>
          <p class="item-description">{{ item.description }}</p>
          <p class="item-owner muted">Cadastrado por {{ item.owner_name }}</p>
        </div>
      </li>
    </ul>

    <ItemCreateModal v-if="showCreate" @created="onCreated" @close="showCreate = false" />
  </section>
</template>

<style scoped>
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
}

.page-header h1 {
    margin: 0 0 4px;
}

.page-header p {
    margin: 0;
}

.notice-close {
    background: none;
    border: 0;
    font-size: 20px;
    line-height: 1;
    color: inherit;
    cursor: pointer;
}

.empty {
    text-align: center;
    padding: 32px 20px;
}

.empty p {
    margin: 0 0 8px;
}

.empty .btn {
    margin-top: 8px;
}

.item {
    display: grid;
    grid-template-columns: 112px 1fr;
    gap: 16px;
    align-items: start;
}

.item-photo {
    width: 112px;
    height: 112px;
    object-fit: cover;
    border-radius: 8px;
    background: var(--bg);
}

.item-photo-empty {
    display: grid;
    place-items: center;
}

.item-photo-empty img {
    width: 44px;
    opacity: 0.35;
}

.item-body {
    min-width: 0;
}

.item-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
}

.item-title {
    font-size: 17px;
    overflow-wrap: anywhere;
}

.tags {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
}

.item-meta {
    margin: 4px 0 8px;
    font-size: 14px;
}

.item-description {
    margin: 0 0 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    overflow-wrap: anywhere;
    white-space: pre-line;
}

.item-owner {
    margin: 0;
    font-size: 13px;
}

@media (max-width: 600px) {
    .page-header {
        flex-direction: column;
        align-items: stretch;
    }

    .item {
        grid-template-columns: 72px 1fr;
        gap: 12px;
    }

    .item-photo {
        width: 72px;
        height: 72px;
    }

    .item-head {
        flex-direction: column;
    }
}
</style>
