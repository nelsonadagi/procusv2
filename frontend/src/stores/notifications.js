import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../services/api';

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref([]);
  const notificationFeed = ref([]);
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

    const fallbackApi = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? `${window.location.protocol}//${window.location.hostname}:8007/api`
      : `${window.location.origin}/api`;
    const apiBase = import.meta.env.VITE_API_URL || fallbackApi;
    const apiUrl = new URL(apiBase, window.location.origin);
    const protocol = apiUrl.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${apiUrl.host}/ws/notifications/?token=${token}`;
  }

  function connect() {
    const token = localStorage.getItem('token');
    
    if (!token) return;
    if (socket.value && [WebSocket.OPEN, WebSocket.CONNECTING].includes(socket.value.readyState)) return;

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
    const item = {
      timestamp: new Date().toISOString(),
      ...notification,
      id: notification.id || id,
      read: false
    };
    notifications.value.push(item);
    notificationFeed.value = [item, ...notificationFeed.value.filter((entry) => entry.id !== item.id)].slice(0, 20);
    
    // Auto remove after 5 seconds if it's a toast
    setTimeout(() => {
        removeNotification(notification.id || id);
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

  async function fetchNotifications() {
    const token = localStorage.getItem('token');
    if (!token) {
      notificationFeed.value = [];
      return [];
    }
    const res = await api.get('/notifications/');
    const items = res.data.results || res.data || [];
    notificationFeed.value = items.map((item) => ({
      id: item.id,
      type: item.type,
      subject: item.subject,
      message: item.message,
      status: item.status,
      timestamp: item.created_at || item.sent_at || new Date().toISOString(),
      data: item.data || { notification_id: item.id },
      read: item.status === 'SENT'
    }));
    return notificationFeed.value;
  }

  return {
    notifications,
    notificationFeed,
    isConnected,
    connect,
    disconnect,
    fetchNotifications,
    addNotification,
    removeNotification
  };
});
