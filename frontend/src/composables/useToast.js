import { ref } from 'vue'

const notifications = ref([])

let notificationId = 0

export function useToast() {
  const addNotification = (message, type = 'info', duration = 3000) => {
    const id = notificationId++
    const notification = { id, message, type, duration }
    notifications.value.push(notification)
    return id
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const success = (message, duration = 3000) => addNotification(message, 'success', duration)
  const error = (message, duration = 4000) => addNotification(message, 'error', duration)
  const warning = (message, duration = 3000) => addNotification(message, 'warning', duration)
  const info = (message, duration = 3000) => addNotification(message, 'info', duration)

  return {
    notifications,
    addNotification,
    removeNotification,
    success,
    error,
    warning,
    info
  }
}
