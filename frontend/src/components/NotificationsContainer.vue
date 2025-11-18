<script setup>
import { useToast } from '../composables/useToast'
import Toast from './Toast.vue'

const { notifications, removeNotification } = useToast()

const handleToastClose = (id) => {
  removeNotification(id)
}
</script>

<template>
  <div class="notifications-container">
    <Toast
      v-for="notification in notifications"
      :key="notification.id"
      :message="notification.message"
      :type="notification.type"
      :duration="notification.duration"
      @close="handleToastClose(notification.id)"
    />
  </div>
</template>

<style scoped>
.notifications-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
}

@media (max-width: 768px) {
  .notifications-container {
    left: 10px;
    right: 10px;
    max-width: none;
    top: 70px;
  }
}
</style>
