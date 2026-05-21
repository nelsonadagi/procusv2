<template>
  <div class="vendor-notification-panel">
    <div class="vnp-header">
      <h4 class="vnp-title">🔔 Alerts</h4>
      <span v-if="unreadCount" class="vnp-badge">{{ unreadCount }}</span>
    </div>
    <div v-if="!notifications.length" class="vnp-empty">
      No new alerts. You're all caught up.
    </div>
    <div v-else class="vnp-list">
      <div
        v-for="n in notifications"
        :key="n.id"
        class="vnp-item"
        :class="{ 'vnp-item--unread': !n.read }"
        @click="handleClick(n)"
      >
        <div class="vnp-item__icon">{{ n.icon }}</div>
        <div class="vnp-item__body">
          <div class="vnp-item__title">{{ n.title }}</div>
          <div class="vnp-item__message">{{ n.message }}</div>
          <div class="vnp-item__time">{{ formatTime(n.timestamp) }}</div>
        </div>
        <div v-if="n.actionLabel" class="vnp-item__action">
          <Button size="sm" variant="ghost" @click.stop="handleClick(n)">{{ n.actionLabel }}</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import Button from '../ui/Button.vue';

const props = defineProps({
  notifications: { type: Array, default: () => [] },
});

const emit = defineEmits(['action']);

const unreadCount = computed(() => props.notifications.filter((n) => !n.read).length);

function formatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  const now = new Date();
  const diff = Math.floor((now - d) / 1000);
  if (diff < 60) return 'Just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function handleClick(n) {
  if (n.action) {
    emit('action', n);
  }
}
</script>

<style scoped>
.vendor-notification-panel {
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(10, 10, 15, 0.04);
}

.vnp-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.vnp-title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 600;
}

.vnp-badge {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  padding: 0.15rem 0.5rem;
  background: var(--pz-color-earth-orange);
  color: white;
  border-radius: 99px;
}

.vnp-empty {
  font-size: 0.85rem;
  color: var(--pz-color-concrete-grey);
  padding: 1rem 0;
  text-align: center;
}

.vnp-list {
  display: grid;
  gap: 0.4rem;
}

.vnp-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.6rem;
  align-items: start;
  padding: 0.6rem 0.5rem;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.12s ease;
}

.vnp-item:hover {
  background: rgba(10, 10, 15, 0.03);
}

.vnp-item--unread {
  background: rgba(212, 101, 42, 0.04);
}

.vnp-item--unread:hover {
  background: rgba(212, 101, 42, 0.08);
}

.vnp-item__icon {
  font-size: 1.1rem;
  line-height: 1.4;
}

.vnp-item__title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
  line-height: 1.3;
}

.vnp-item__message {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.4;
  margin-top: 0.1rem;
}

.vnp-item__time {
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.25rem;
  font-family: var(--pz-font-mono);
}

.vnp-item__action {
  opacity: 0;
  transition: opacity 0.15s ease;
}

.vnp-item:hover .vnp-item__action {
  opacity: 1;
}
</style>
