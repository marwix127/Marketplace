<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../api/axios";

const route = useRoute();
const product = ref(null);

onMounted(async () => {
  const id = route.params.id;
  const response = await api.get(`/products/${id}/`);
  product.value = response.data;
});
</script>

<template>
  <div v-if="product">
    <h2>{{ product.title }}</h2>
    <p>{{ product.description }}</p>
    <p><strong>Precio:</strong> {{ product.price }} €</p>
  </div>
</template>
