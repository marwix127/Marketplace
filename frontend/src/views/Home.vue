<template>
  <div class="home">
    <div class="hero-section">
      <h1>Bienvenido a MarketPlace</h1>
      <p>Descubre miles de productos increíbles</p>
    </div>

    <div class="products-section">
      <h2>Productos Destacados</h2>

      <div v-if="products.length === 0" class="no-products">
        <p>No hay productos disponibles en este momento.</p>
      </div>

      <div v-else class="products-grid">
  <div
    v-for="product in products"
    :key="product.id"
    class="product-card"
  >
    <div class="product-image">
      <img :src="imageUrl(product)" :alt="product.title" />

    </div>

    <div class="product-info">
      <h3>{{ product.title }}</h3>
      <p class="product-description">
        {{ product.description || "Sin descripción" }}
      </p>

      <!-- 🔥 NUEVO: botón para ver detalles -->
      <RouterLink :to="`/product/${product.id}`" class="btn-details">
        Ver detalles
      </RouterLink>

      <div class="product-footer">
        <span class="product-price">{{ product.price }}€</span>
        <div class="actions">
          <button class="btn-add-to-cart" @click="addToCart(product)">Añadir al carrito</button>
          <button
            v-if="isOwner(product)"
            class="btn-edit"
            @click="goToEdit(product.id)"
          >
            Editar
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from 'vue-router'
import api from "../api/axios";
import { useToast } from "../composables/useToast"

const router = useRouter()
const { success, error } = useToast()

const products = ref([]);

const username = ref(localStorage.getItem("username") || "");
// Backend base URL (ajusta si usas otra dirección/puerto)
const backendURL = 'http://127.0.0.1:8000'
const placeholderURL = (title = 'Producto') => `https://via.placeholder.com/400x300?text=${encodeURIComponent(title)}`

async function loadProducts() {
  try {
    const res = await api.get("products/");
    products.value = res.data;
    // debug: log first product owner
    // console.log('products loaded', products.value)
  } catch (err) {
    console.error("Error al cargar productos:", err);
  }
}

onMounted(() => {
  loadProducts()

  function updateUsername() {
    username.value = localStorage.getItem("username") || "";
  }

  // update when other parts of the app change auth state
  window.addEventListener('auth-changed', updateUsername)
  window.addEventListener('storage', updateUsername)

  onBeforeUnmount(() => {
    window.removeEventListener('auth-changed', updateUsername)
    window.removeEventListener('storage', updateUsername)
  })
})

function isOwner(product) {
  const owner = product?.owner
  const user = (username.value || "").toString()
  if (!owner || !user) return false

  // if owner is an object with username
  if (typeof owner === 'object') {
    return (owner.username || "").toString().toLowerCase() === user.toLowerCase()
  }

  // compare strings (case-insensitive, trimmed)
  return owner.toString().trim().toLowerCase() === user.toLowerCase().trim()
}

const goToEdit = (productId) => {
  router.push(`/products/${productId}/edit`);
};

function imageUrl(product) {
  const img = product?.image
  if (!img) return placeholderURL(product?.title || 'Producto')
  if (typeof img === 'string' && (img.startsWith('http://') || img.startsWith('https://'))) {
    return img
  }
  const path = img.startsWith('/') ? img : `/${img}`
  return backendURL + path
}

async function addToCart(product) {
  const isAuthenticated = !!localStorage.getItem('access')
  if (!isAuthenticated) {
    error('Debes iniciar sesión para añadir productos al carrito')
    setTimeout(() => {
      router.push('/login')
    }, 500)
    return
  }

    try {
    await api.post('cart/add_item/', {
      product_id: product.id,
      quantity: 1
    })
    success(`${product.title} añadido al carrito`)
    // notify navbar and other components to refresh cart count
    window.dispatchEvent(new Event('cart-changed'))
  } catch (err) {
    console.error('Error adding to cart:', err)
    error('Error al añadir producto al carrito')
  }
}
</script>

<style>
:root {
  --primary-color: #2563eb;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.home {
  padding: 2rem 0;
}

.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, #1e40af 100%);
  color: white;
  padding: 4rem 2rem;
  border-radius: 0.75rem;
  text-align: center;
  margin-bottom: 3rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
}

.hero-section p {
  font-size: 1.25rem;
  margin: 0;
  opacity: 0.9;
}

.products-section {
  width: 100%;
}

.products-section h2 {
  font-size: 2rem;
  color: var(--text-dark);
  margin-bottom: 2rem;
  text-align: center;
}

.no-products {
  text-align: center;
  padding: 3rem 2rem;
  background: var(--bg-light);
  border-radius: 0.75rem;
  color: var(--text-light);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.product-card {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--bg-light);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-info {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.product-info h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-size: 1.1rem;
  line-height: 1.4;
}

.product-description {
  color: var(--text-light);
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
  flex-grow: 1;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.product-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.btn-add-to-cart {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-add-to-cart:hover {
  background: #1e40af;
  transform: scale(1.05);
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-edit {
  padding: 0.45rem 0.9rem;
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background: rgba(37,99,235,0.06);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 1rem;
  }

  .hero-section h1 {
    font-size: 1.875rem;
  }

  .hero-section p {
    font-size: 1rem;
  }

  .products-section h2 {
    font-size: 1.5rem;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
  }
}
</style>
