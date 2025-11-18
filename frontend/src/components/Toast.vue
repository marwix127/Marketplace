<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    enum: ['success', 'error', 'info', 'warning'],
    default: 'info'
  },
  duration: {
    type: Number,
    default: 3000
  }
})

const emit = defineEmits(['close'])
const isVisible = ref(true)

onMounted(() => {
  if (props.duration > 0) {
    setTimeout(() => {
      isVisible.value = false
      emit('close')
    }, props.duration)
  }
})

const handleClose = () => {
  isVisible.value = false
  emit('close')
}
</script>

<template>
  <transition name="toast-slide">
    <div v-if="isVisible" :class="['toast', `toast-${type}`]">
      <div class="toast-content">
        <span class="toast-icon">
          <span v-if="type === 'success'">✓</span>
          <span v-else-if="type === 'error'">✕</span>
          <span v-else-if="type === 'warning'">⚠</span>
          <span v-else>ℹ</span>
        </span>
        <p class="toast-message">{{ message }}</p>
      </div>
      <button class="toast-close" @click="handleClose">×</button>
    </div>
  </transition>
</template>

<style scoped>
.toast {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.toast-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.toast-message {
  margin: 0;
  font-size: 0.95rem;
}

.toast-success {
  background-color: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
}

.toast-success .toast-icon {
  color: #10b981;
}

.toast-error {
  background-color: #fee2e2;
  border: 1px solid #fca5a5;
  color: #7f1d1d;
}

.toast-error .toast-icon {
  color: #ef4444;
}

.toast-warning {
  background-color: #fef3c7;
  border: 1px solid #fcd34d;
  color: #78350f;
}

.toast-warning .toast-icon {
  color: #f59e0b;
}

.toast-info {
  background-color: #dbeafe;
  border: 1px solid #93c5fd;
  color: #0c2340;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: currentColor;
  padding: 0;
  margin-left: 1rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.toast-close:hover {
  opacity: 1;
}

.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.3s ease;
}

.toast-slide-enter-from {
  transform: translateX(400px);
  opacity: 0;
}

.toast-slide-leave-to {
  transform: translateX(400px);
  opacity: 0;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
