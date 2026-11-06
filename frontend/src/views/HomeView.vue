<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";

const items = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await api.get("/items/");
    items.value = data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section>
    <div class="row between">
      <h1>Objetos cadastrados</h1>
      <RouterLink to="/objetos/perdi" class="btn">Perdi um objeto</RouterLink>
    </div>
    <p v-if="loading" class="muted">Carregando...</p>
    <p v-else-if="!items.length" class="muted">Nenhum objeto cadastrado ainda.</p>
    <ul class="list">
      <li v-for="item in items" :key="item.id" class="card">
        <div class="row between">
          <strong>{{ item.title }}</strong>
          <span class="tag" :class="item.type === 'LOST' ? 'tag-lost' : 'tag-found'">
            {{ item.type === "LOST" ? "Perdido" : "Encontrado" }}
          </span>
        </div>
        <p class="muted">{{ item.category_name }} · {{ item.location }} · {{ item.date_occurred }}</p>
        <p>{{ item.description }}</p>
        <img v-if="item.photo" :src="item.photo" alt="" class="thumb" />
      </li>
    </ul>
  </section>
</template>
