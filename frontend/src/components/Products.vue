<template>
  <div>
    <h2>Productos</h2>
    <ul>
      <li v-for="p in products" :key="p.id">{{ p.title }} - {{ p.price }}€</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const products = ref([]);

onMounted(async () => {
  const res = await api.get("products/");
  products.value = res.data;
});
</script>
