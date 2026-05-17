import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref([]);
  const socket = ref(null);
  const isConnected = ref(false);
  const reconnectInterval = 5000;

  function getWebSocketUrl(token) {
    const explicitWsUrl = import.meta.env.VITE_WS_URL;
    if (explicitWsUrl) {
      const url = new URL(explicitWsUrl);
      url.searchParams.set('token', token);
      return url.toString();
    }

    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    const apiUrl = new URL(apiBase, window.location.origin);
    const protocol = apiUrl.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${apiUrl.host}/ws/notifications/?token=${token}`;
  }

  function connect() {
    const token = localStorage.getItem('token');
    
    if (!token) return;

    const wsUrl = getWebSocketUrl(token);
    
    socket.value = new WebSocket(wsUrl);

    socket.value.onopen = () => {
      console.log('Notification WS Connected');
      isConnected.value = true;
    };

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      addNotification(data);
    };

    socket.value.onclose = () => {
      console.log('Notification WS Disconnected');
      isConnected.value = false;
      setTimeout(connect, reconnectInterval);
    };
    
    socket.value.onerror = (err) => {
        console.error('Notification WS Error', err);
    };
  }

  function addNotification(notification) {
    // Add unique ID if missing
    const id = Date.now() + Math.random().toString(36).substr(2, 9);
    notifications.value.push({ ...notification, id, read: false });
    
    // Auto remove after 5 seconds if it's a toast
    setTimeout(() => {
        removeNotification(id);
    }, 5000);
  }

  function removeNotification(id) {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  }

  function disconnect() {
    if (socket.value) {
      socket.value.close();
      socket.value = null;
    }
  }

  return {
    notifications,
    isConnected,
    connect,
    disconnect,
    addNotification,
    removeNotification
  };
});
