<template>
  <div id="app">
    <NotificationsContainer />

    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-brand">
          <router-link to="/" class="logo">🛍️ MarketPlace</router-link>
        </div>

        <ul class="nav-menu">
          <li>
            <router-link to="/" class="nav-link">Inicio</router-link>
          </li>

          <li v-if="isAuthenticated">
            <button class="nav-link create-product" @click="goToAddProduct">
              Crear producto
            </button>
          </li>

          <li v-if="isAuthenticated">
            <router-link to="/cart" class="nav-link">
              🛒 Carrito
              <span v-if="cartCount > 0" class="cart-badge">({{ cartCount }})</span>
            </router-link>
          </li>

          <li v-if="!isAuthenticated">
            <router-link to="/login" class="nav-link">Inicia Sesión</router-link>
          </li>

          <li v-if="!isAuthenticated">
            <router-link to="/register" class="nav-link btn-register">Registrarse</router-link>
          </li>

          <li v-if="isAuthenticated" class="nav-user">
            <span class="nav-link">Hola, {{ username }}</span>
          </li>

          <li v-if="isAuthenticated">
            <button class="nav-link logout" @click="logout">Cerrar sesión</button>
          </li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2025 MarketPlace. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NotificationsContainer from './components/NotificationsContainer.vue'
import api from './api/axios'

const router = useRouter()

const username = ref(localStorage.getItem('username') || '')
const isAuthenticated = ref(!!localStorage.getItem('access'))
const cartCount = ref(0)

function updateAuthFromStorage() {
  username.value = localStorage.getItem('username') || ''
  isAuthenticated.value = !!localStorage.getItem('access')
}

async function loadCartCount() {
  if (!isAuthenticated.value) {
    cartCount.value = 0
    return
  }

  try {
    const res = await api.get('cart/my_cart/')
    const items = res.data.items || []
    cartCount.value = items.reduce((sum, it) => sum + (it.quantity || 0), 0)
  } catch (e) {
    cartCount.value = 0
  }
}

function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('username')
  updateAuthFromStorage()
  window.dispatchEvent(new Event('auth-changed'))
  window.dispatchEvent(new Event('cart-changed'))
  router.push('/')
}

onMounted(() => {
  window.addEventListener('auth-changed', async () => {
    updateAuthFromStorage()
    await loadCartCount()
  })
  window.addEventListener('storage', async () => {
    updateAuthFromStorage()
    await loadCartCount()
  })
  window.addEventListener('cart-changed', loadCartCount)

  updateAuthFromStorage()
  loadCartCount()
})

const goToAddProduct = () => {
  router.push('/products/add')
}
</script>

<style>
:root {
  --primary-color: #2563eb;
  --primary-dark: #1e40af;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
}

.navbar {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  box-shadow: var(--shadow);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
}

.logo {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: opacity 0.3s ease;
}

.logo:hover {
  opacity: 0.9;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 1rem;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s ease;
  cursor: pointer;
  background: transparent;
  border: none;
  padding: 0.25rem 0.5rem;
}

.nav-link:hover {
  opacity: 0.85;
}

.nav-link.router-link-active {
  border-bottom: 2px solid rgba(255,255,255,0.9);
  padding-bottom: 0.25rem;
}

.btn-register {
  background: white;
  color: var(--primary-color);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.btn-register:hover {
  background: var(--bg-light);
}

.nav-user .nav-link {
  color: #fff;
  font-weight: 600;
}

.logout {
  background: rgba(255,255,255,0.08);
  color: #fff;
  border-radius: 6px;
}

.create-product {
  background: rgb(255, 255, 255);
  color:#2563eb;
  border-radius: 6px;
}
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

.footer {
  background-color: var(--bg-light);
  border-top: 1px solid var(--border-color);
  padding: 2rem;
  text-align: center;
  color: var(--text-light);
  margin-top: auto;
}

@media (max-width: 768px) {
  .navbar-container { padding: 0 1rem; }
  .nav-menu { gap: .75rem; font-size: .95rem; }
  .btn-register { padding: .4rem .8rem; }
  .main-content { padding: 1rem; }
}
</style>
