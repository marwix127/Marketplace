<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'
import { useToast } from '../composables/useToast'

const router = useRouter()
const { error } = useToast()

const orders = ref([])
const loading = ref(true)
const expandedOrders = ref(new Set())

async function loadOrders() {
  loading.value = true
  try {
    const response = await api.get('orders/')
    orders.value = response.data
  } catch (err) {
    error('Error cargando los pedidos')
    console.error('Error loading orders:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadOrders()
})

function toggleOrder(orderId) {
  if (expandedOrders.value.has(orderId)) {
    expandedOrders.value.delete(orderId)
  } else {
    expandedOrders.value.add(orderId)
  }
  // Force reactivity
  expandedOrders.value = new Set(expandedOrders.value)
}

function isExpanded(orderId) {
  return expandedOrders.value.has(orderId)
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatPrice(price) {
  return parseFloat(price).toFixed(2)
}
</script>

<template>
  <div class="orders-container">
    <h1>Mis Pedidos</h1>

    <div v-if="loading" class="loading">Cargando pedidos...</div>

    <div v-else-if="orders.length === 0" class="empty-orders">
      <p>No tienes pedidos aún</p>
      <button class="btn-primary" @click="router.push('/')">Ir a comprar</button>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header" @click="toggleOrder(order.id)">
          <div class="order-info">
            <h3>Pedido #{{ order.id }}</h3>
            <p class="order-date">{{ formatDate(order.created_at) }}</p>
          </div>
          <div class="order-summary">
            <span class="order-status" :class="order.status">{{ order.status }}</span>
            <span class="order-total">{{ formatPrice(order.total_price) }}€</span>
            <span class="expand-icon">{{ isExpanded(order.id) ? '▲' : '▼' }}</span>
          </div>
        </div>

        <div v-if="isExpanded(order.id)" class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <div class="item-info">
              <span class="item-title">{{ item.product_title }}</span>
              <span class="item-quantity">x{{ item.quantity }}</span>
            </div>
            <div class="item-prices">
              <span class="item-unit-price">{{ formatPrice(item.product_price) }}€/u</span>
              <span class="item-subtotal">{{ formatPrice(item.subtotal) }}€</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.orders-container h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #1f2937;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.empty-orders {
  text-align: center;
  padding: 3rem 2rem;
  background: #f9fafb;
  border-radius: 0.75rem;
}

.empty-orders p {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: #6b7280;
}

.btn-primary {
  background: #2563eb;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #1e40af;
  transform: translateY(-2px);
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.order-header:hover {
  background: #f9fafb;
}

.order-info h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.order-date {
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.order-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.order-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.order-status.completed {
  background: #d1fae5;
  color: #065f46;
}

.order-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.order-status.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.order-total {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2563eb;
}

.expand-icon {
  color: #9ca3af;
  font-size: 0.75rem;
}

.order-items {
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
  background: #f9fafb;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.order-item:last-child {
  border-bottom: none;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.item-title {
  font-weight: 500;
  color: #1f2937;
}

.item-quantity {
  color: #6b7280;
  font-size: 0.875rem;
}

.item-prices {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.item-unit-price {
  color: #6b7280;
  font-size: 0.875rem;
}

.item-subtotal {
  font-weight: 600;
  color: #1f2937;
}

@media (max-width: 640px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .order-summary {
    width: 100%;
    justify-content: space-between;
  }

  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .item-prices {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
