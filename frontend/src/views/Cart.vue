<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { success, error } = useToast()

const cart = ref(null)
const loading = ref(true)
const checkingOut = ref(false)

const backendURL = 'http://127.0.0.1:8000'

async function loadCart() {
  loading.value = true
  try {
    const response = await api.get('cart/my_cart/')
    cart.value = response.data
  } catch (err) {
    error('Error cargando el carrito')
    console.error('Error loading cart:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCart()
})

function imageUrl(product) {
  const img = product?.image
  if (!img) return `https://via.placeholder.com/400x300?text=${encodeURIComponent(product?.title || 'Producto')}`
  if (typeof img === 'string' && (img.startsWith('http://') || img.startsWith('https://'))) {
    return img
  }
  const path = img.startsWith('/') ? img : `/${img}`
  return backendURL + path
}

async function updateQuantity(itemId, newQuantity) {
  try {
    const response = await api.post('cart/update_item/', {
      item_id: itemId,
      quantity: newQuantity
    })
    // Update local cart
    if (cart.value) {
      const item = cart.value.items.find(i => i.id === itemId)
      if (item) {
        item.quantity = response.data.quantity
        item.subtotal = response.data.subtotal
        // Recalculate total
        cart.value.total_price = cart.value.items.reduce((sum, i) => sum + i.subtotal, 0)
      }
    }
    // notify navbar to refresh count
    window.dispatchEvent(new Event('cart-changed'))
  } catch (err) {
    error('Error actualizando cantidad')
  }
}

async function removeItem(itemId) {
  try {
    await api.post('cart/remove_item/', { item_id: itemId })
    // Remove from local cart
    if (cart.value) {
      cart.value.items = cart.value.items.filter(i => i.id !== itemId)
      cart.value.total_price = cart.value.items.reduce((sum, i) => sum + i.subtotal, 0)
    }
    success('Item removido del carrito')
    // notify navbar to refresh count
    window.dispatchEvent(new Event('cart-changed'))
  } catch (err) {
    error('Error removiendo item')
  }
}

async function clearCart() {
  if (!confirm('¿Estás seguro de que deseas vaciar el carrito?')) return
  try {
    await api.post('cart/clear/')
    cart.value.items = []
    cart.value.total_price = 0
    success('Carrito vaciado')
    window.dispatchEvent(new Event('cart-changed'))
  } catch (err) {
    error('Error vaciando carrito')
  }
}

async function checkout() {
  if (checkingOut.value) return
  checkingOut.value = true
  try {
    await api.post('cart/checkout/')
    success('¡Pedido realizado con éxito!')
    window.dispatchEvent(new Event('cart-changed'))
    router.push('/orders')
  } catch (err) {
    error('Error al procesar el pedido')
    console.error('Checkout error:', err)
  } finally {
    checkingOut.value = false
  }
}

function goToProduct(productId) {
  router.push(`/product/${productId}`)
}
</script>

<template>
  <div class="cart-container">
    <h1>Carrito de Compras</h1>

    <div v-if="loading" class="loading">Cargando carrito...</div>

    <div v-else-if="!cart || cart.items.length === 0" class="empty-cart">
      <p>Tu carrito está vacío</p>
      <button class="btn-primary" @click="router.push('/')">Continuar comprando</button>
    </div>

    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="item in cart.items" :key="item.id" class="cart-item">
          <img :src="imageUrl(item.product)" :alt="item.product.title" class="item-image" />
          <div class="item-details">
            <h3>{{ item.product.title }}</h3>
            <p class="item-price">{{ item.product.price }}€</p>
            <button class="btn-product-link" @click="goToProduct(item.product.id)">
              Ver producto
            </button>
          </div>
          <div class="item-quantity">
            <label for="">Cantidad:</label>
            <div class="quantity-controls">
              <button @click="updateQuantity(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">−</button>
              <input type="number" v-model.number="item.quantity" @change="updateQuantity(item.id, item.quantity)" min="1" />
              <button @click="updateQuantity(item.id, item.quantity + 1)">+</button>
            </div>
          </div>
          <div class="item-subtotal">
            <p>{{ item.subtotal.toFixed(2) }}€</p>
          </div>
          <button class="btn-remove" @click="removeItem(item.id)">Eliminar</button>
        </div>
      </div>

      <div class="cart-summary">
        <h2>Resumen del Carrito</h2>
        <div class="summary-row">
          <span>Total items:</span>
          <strong>{{ cart.items.length }}</strong>
        </div>
        <div class="summary-row total">
          <span>Total:</span>
          <strong>{{ cart.total_price.toFixed(2) }}€</strong>
        </div>
        <button 
          class="btn-primary btn-checkout" 
          @click="checkout"
          :disabled="checkingOut"
        >
          {{ checkingOut ? 'Procesando...' : 'Proceder al pago' }}
        </button>
        <button class="btn-secondary" @click="clearCart">Vaciar carrito</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #2563eb;
  --primary-dark: #1e40af;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-container h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-dark);
  text-align: center;
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.alert-error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--text-light);
}

.empty-cart {
  text-align: center;
  padding: 3rem 2rem;
  background: var(--bg-light);
  border-radius: 0.75rem;
}

.empty-cart p {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: var(--text-light);
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cart-item {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow);
}

.item-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.item-details {
  flex: 1;
  min-width: 0;
}

.item-details h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-dark);
  font-size: 1.1rem;
  word-break: break-word;
}

.item-price {
  color: var(--primary-color);
  font-weight: 600;
  margin: 0.25rem 0;
}

.btn-product-link {
  background: none;
  border: none;
  color: var(--primary-color);
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}

.btn-product-link:hover {
  text-decoration: none;
}

.item-quantity {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-quantity label {
  font-size: 0.9rem;
  color: var(--text-light);
}

.quantity-controls {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.quantity-controls button {
  width: 32px;
  height: 32px;
  border: 1px solid var(--border-color);
  background: white;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.quantity-controls button:hover:not(:disabled) {
  background: var(--primary-color);
  color: white;
}

.quantity-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-controls input {
  width: 50px;
  text-align: center;
  border: 1px solid var(--border-color);
  border-radius: 0.25rem;
  padding: 0.25rem;
}

.item-subtotal {
  min-width: 80px;
  text-align: right;
}

.item-subtotal p {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.btn-remove {
  background: #fee2e2;
  color: #991b1b;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.btn-remove:hover {
  background: #fecaca;
}

.cart-summary {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.cart-summary h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  color: var(--text-dark);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  color: var(--text-light);
}

.summary-row.total {
  border-top: 2px solid var(--border-color);
  padding-top: 1rem;
  font-size: 1.25rem;
  color: var(--text-dark);
}

.btn-primary, .btn-secondary {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.75rem;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.btn-secondary:hover {
  background: rgba(37, 99, 235, 0.06);
}

@media (max-width: 768px) {
  .cart-content {
    grid-template-columns: 1fr;
  }

  .cart-item {
    flex-wrap: wrap;
  }

  .item-image {
    width: 100px;
    height: 100px;
  }

  .cart-summary {
    position: static;
  }
}
</style>
