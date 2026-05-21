import { defineStore } from 'pinia';
import { ref, onMounted, onUnmounted } from 'vue';

const QUEUE_KEY = 'vendor_offline_stock_queue';

function loadQueue() {
  try {
    return JSON.parse(localStorage.getItem(QUEUE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveQueue(queue) {
  try {
    localStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
  } catch {
    // Ignore storage errors
  }
}

export const useOfflineQueueStore = defineStore('offlineQueue', () => {
  const queue = ref(loadQueue());
  const isOnline = ref(navigator.onLine);
  const syncing = ref(false);

  function add(item) {
    queue.value.push({
      ...item,
      queuedAt: new Date().toISOString(),
      id: Date.now() + Math.random().toString(36).substr(2, 9),
    });
    saveQueue(queue.value);
  }

  function remove(id) {
    queue.value = queue.value.filter((q) => q.id !== id);
    saveQueue(queue.value);
  }

  function clear() {
    queue.value = [];
    saveQueue([]);
  }

  async function sync(processFn) {
    if (!isOnline.value || !queue.value.length || syncing.value) return;
    syncing.value = true;
    const items = [...queue.value];
    for (const item of items) {
      try {
        await processFn(item);
        remove(item.id);
      } catch {
        // Leave in queue for next sync
      }
    }
    syncing.value = false;
  }

  function handleOnline() {
    isOnline.value = true;
  }

  function handleOffline() {
    isOnline.value = false;
  }

  onMounted(() => {
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
  });

  onUnmounted(() => {
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
  });

  return {
    queue,
    isOnline,
    syncing,
    add,
    remove,
    clear,
    sync,
  };
});
