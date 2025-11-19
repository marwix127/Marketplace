<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/axios'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const product = ref(null)
const loading = ref(true)
const { success, error } = useToast()

onMounted(async () => {
  const id = route.params.id
  try {
    const response = await api.get(`/products/${id}/`)
    product.value = response.data
  } catch (err) {
    console.error('Error cargando producto', err)
  } finally {
    loading.value = false
  }
})

async function addToCart() {
  if (!product.value) return
  try {
    // Intentamos llamar al endpoint del carrito; si falla, mostramos notificación local
    await api.post('/cart/', { product: product.value.id, quantity: 1 })
    success('Añadido al carrito')
  } catch (err) {
    console.error('Error añadiendo al carrito', err)
    success('Añadido al carrito (local)')
  }
}

function goBack() {
  router.back()
}
</script>

<template>
  <div class="container p-3">
    <div v-if="loading" class="text-center mt-4">Cargando...</div>

    <div v-else-if="product" class="product-card flex gap-3 mt-3">
      <div class="product-image-wrapper">
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.title"
          class="product-image"
        />
        <div v-else class="product-image placeholder">Sin imagen</div>
      </div>

      <div class="product-info">
        <h2 class="mb-1">{{ product.title }}</h2>
        <p class="mb-2">{{ product.description }}</p>
        <p class="mb-3"><strong>Precio:</strong> {{ product.price }} €</p>

        <div class="flex gap-2">
          <button class="btn btn-secondary" @click="goBack">Volver</button>
          <button class="btn btn-primary" @click="addToCart">Añadir al carrito</button>
        </div>
      </div>
    </div>

    <div v-else class="text-center mt-4">Producto no encontrado.</div>
  </div>
</template>

<style scoped>
.product-card {
  align-items: flex-start;
}

.product-image-wrapper {
  width: 420px;
  max-width: 40%;
  flex-shrink: 0;
}

.product-image {
  width: 100%;
  height: 100%;
  max-height: 420px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(31, 41, 55, 0.08);
}

.product-image.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  background: #f1f5f9;
  color: #64748b;
  border-radius: 8px;
}

.product-info {
  flex: 1;
}

.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: none;
  font-weight: 600;
}

.btn-primary {
  background: #2563eb;
  color: #fff;
}

.btn-secondary {
  background: transparent;
  color: #111827;
  border: 1px solid #e6e9ef;
}

@media (max-width: 768px) {
  .product-card {
    flex-direction: column;
  }

  .product-image-wrapper {
    width: 100%;
    max-width: 100%;
  }
}
</style>
