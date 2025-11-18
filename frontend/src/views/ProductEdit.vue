<script setup>
import { ref, onMounted } from "vue";
import api from "../api/axios";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "../composables/useToast";

const route = useRoute();
const router = useRouter();
const { error: showError, success: showSuccess } = useToast();

const id = route.params.id;

const title = ref("");
const description = ref("");
const price = ref("");
const currentImage = ref(null);
const file = ref(null);
const preview = ref(null);

const loading = ref(true);

onMounted(async () => {
  try {
    const response = await api.get(`products/${id}/`);
    title.value = response.data.title;
    description.value = response.data.description;
    price.value = response.data.price;
    currentImage.value = response.data.image || null;
  } catch (e) {
    showError("Error cargando el producto.");
  }
  loading.value = false;
});

const onFileSelected = (e) => {
  const f = e.target.files[0];
  file.value = f;
  if (f) preview.value = URL.createObjectURL(f);
  else preview.value = null;
};

const updateProduct = async () => {
  try {
    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("description", description.value);
    formData.append("price", price.value);
    if (file.value) {
      formData.append("image", file.value);
    }

    // Use PATCH so we can send multipart and update partially
    await api.patch(`products/${id}/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    showSuccess("Producto actualizado.");
    setTimeout(() => router.push('/'), 700);
  } catch (e) {
    showError(e.response?.data?.detail || "No tienes permiso para actualizar este producto.");
  }
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Editar Producto</h1>
        <p class="text-subtitle">Actualiza los campos del producto</p>
      </div>

      <div v-if="loading">Cargando...</div>

      <div v-else>
        <form class="auth-form" @submit.prevent="updateProduct">
          <div class="form-group">
            <label for="title">Título</label>
            <input id="title" v-model="title" required />
          </div>

          <div class="form-group">
            <label for="description">Descripción</label>
            <textarea id="description" v-model="description"></textarea>
          </div>

          <div class="form-group">
            <label for="price">Precio (€)</label>
            <input id="price" type="number" v-model="price" required />
          </div>

          <div class="form-group">
            <label for="image">Imagen (cambiar)</label>
            <input id="image" type="file" accept="image/*" @change="onFileSelected" />

            <div class="preview-area">
              <div v-if="preview">
                <p class="mb-1">Preview nueva:</p>
                <img :src="preview" alt="preview" />
              </div>
              <div v-else-if="currentImage">
                <p class="mb-1">Imagen actual:</p>
                <img :src="(currentImage && (currentImage.startsWith('http') ? currentImage : 'http://127.0.0.1:8000' + currentImage))" alt="current" />
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button class="btn-primary" type="submit">Actualizar</button>
            <button type="button" class="btn-muted" @click="router.back()">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
.preview-area img { max-width: 240px; border-radius: 8px; margin-top: .5rem }
.form-actions { display:flex; gap: .75rem; margin-top: 1rem }
.btn-muted { background: transparent; border: 1px solid var(--border-color); padding: .6rem 1rem; border-radius: .5rem }
</style>
