<template>
  <div class="property-notification-panel">
    <div class="pnp-header">
      <div>
        <div class="pnp-header__eyebrow">Alerts</div>
        <h4 class="pnp-header__title">Property notifications</h4>
      </div>
      <span v-if="unreadCount" class="pnp-badge">{{ unreadCount }}</span>
    </div>

    <div v-if="!notifications.length" class="pnp-empty">
      No property alerts right now.
    </div>

    <div v-else class="pnp-list">
      <button
        v-for="item in notifications"
        :key="item.id"
        type="button"
        class="pnp-item"
        :class="{ 'pnp-item--unread': !item.read }"
        @click="$emit('action', item)"
      >
        <span class="pnp-item__icon">{{ item.icon }}</span>
        <span class="pnp-item__body">
          <span class="pnp-item__title">{{ item.title }}</span>
          <span class="pnp-item__message">{{ item.message }}</span>
          <span class="pnp-item__time">{{ formatTime(item.timestamp) }}</span>
        </span>
        <span v-if="item.actionLabel" class="pnp-item__cta">{{ item.actionLabel }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

defineEmits(['action']);

const props = defineProps({
  notifications: { type: Array, default: () => [] },
});

const unreadCount = computed(() => props.notifications.filter((n) => !n.read).length);

function formatTime(value) {
  if (!value) return '';
  const date = new Date(value);
  const diff = Math.max(0, Math.floor((Date.now() - date.getTime()) / 1000));
  if (diff < 60) return 'Just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}
</script>

<style scoped>
.property-notification-panel {
  display: grid;
  gap: 0.8rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: #fff;
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.03);
}

.pnp-header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
}

.pnp-header__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pnp-header__title {
  margin: 0.2rem 0 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pnp-badge {
  display: inline-flex;
  align-items: center;
  min-height: 1.6rem;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  background: var(--pz-color-earth-orange);
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
}

.pnp-empty {
  padding: 0.75rem 0;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
}

.pnp-list {
  display: grid;
  gap: 0.5rem;
}

.pnp-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.75rem;
  padding: 0.85rem 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.96);
  text-align: left;
}

.pnp-item--unread {
  border-color: rgba(212, 101, 42, 0.2);
  background: rgba(212, 101, 42, 0.04);
}

.pnp-item__icon {
  display: grid;
  place-items: center;
  width: 1.9rem;
  height: 1.9rem;
  border-radius: 8px;
  background: rgba(212, 101, 42, 0.1);
  font-size: 1rem;
}

.pnp-item__body {
  display: grid;
  gap: 0.15rem;
  min-width: 0;
}

.pnp-item__title {
  font-family: var(--pz-font-display);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pnp-item__message,
.pnp-item__time {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pnp-item__cta {
  align-self: center;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}
</style>
