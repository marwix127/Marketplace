<script setup>
import { ref } from "vue";
import api from "../api/axios";
import { useRouter } from "vue-router";
import { useToast } from "../composables/useToast";

const router = useRouter();
const { error: showError, success: showSuccess } = useToast();

const title = ref("");
const description = ref("");
const price = ref(null);
const file = ref(null);
const preview = ref(null);

const onFileSelected = (e) => {
  const f = e.target.files[0];
  file.value = f;
  if (f) {
    preview.value = URL.createObjectURL(f);
  } else {
    preview.value = null;
  }
};

const createProduct = async () => {
  try {
    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("description", description.value);
    // Normalizar precio: aceptar coma como separador decimal si el usuario la introduce
    let p = price.value
    if (typeof p === 'string') p = p.replace(',', '.')
    formData.append("price", p);

    if (file.value) {
      formData.append("image", file.value);
    }

    await api.post("products/", formData, {
      headers: {
        // Let axios set the proper multipart boundary
        "Content-Type": "multipart/form-data",
      },
    });

    showSuccess("Producto creado correctamente.");
    // small delay then redirect
    setTimeout(() => router.push("/"), 800);
  } catch (err) {
    showError(err.response?.data?.detail || "Error al crear producto");
  }
};
</script>


<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Añadir Producto</h1>
        <p class="text-subtitle">Completa los datos para publicar tu producto</p>
      </div>

      <form class="auth-form" @submit.prevent="createProduct">
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
          <input id="price" type="number" step="0.01" v-model.number="price" required />
        </div>

        <div class="form-group">
          <label for="image">Imagen</label>
          <input id="image" type="file" accept="image/*" @change="onFileSelected" />
          <div v-if="preview" class="preview">
            <img :src="preview" alt="Preview" />
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">Crear producto</button>
          <button type="button" class="btn-muted" @click="router.back()">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
.preview img { max-width: 200px; border-radius: 8px; margin-top: .5rem; }
.form-actions { display:flex; gap: .75rem; margin-top: 1rem }
.btn-muted { background: transparent; border: 1px solid var(--border-color); padding: .6rem 1rem; border-radius: .5rem }
</style>
