<template>
  <div class="notification-center">
    <transition-group name="slide-fade">
      <div 
        v-for="notification in notificationStore.notifications" 
        :key="notification.id"
        class="notification-toast"
        :class="getVariantClass(notification.type)"
        @click="handleClick(notification)"
      >
        <div class="notification-icon">
           <svg v-if="notification.type === 'CHAT'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
           <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        </div>
        <div class="notification-content">
          <p class="notification-message">{{ notification.message }}</p>
          <span class="notification-time">{{ new Date(notification.timestamp).toLocaleTimeString() }}</span>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useNotificationStore } from '../../stores/notifications';
import { useUIStore } from '../../stores/ui'; // Import UI store

const notificationStore = useNotificationStore();
const uiStore = useUIStore(); // Use UI store

const getVariantClass = (type) => {
  switch (type) {
    case 'CHAT': return 'notification-toast--chat';
    case 'BID': return 'notification-toast--info';
    case 'PAYMENT': return 'notification-toast--success';
    default: return 'notification-toast--default';
  }
};

const handleClick = (notification) => {
  if (notification.type === 'CHAT' && notification.data && notification.data.room_id) {
    uiStore.openChat(notification.data.room_id);
  }
  // Dismiss notification
  notificationStore.removeNotification(notification.id);
};
</script>

<style scoped>
.notification-center {
  position: fixed;
  top: 80px; /* Below nav */
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none; /* Let clicks pass through empty space */
}

.notification-toast {
  pointer-events: auto;
  background: rgba(248, 246, 240, 0.97);
  border: 1px solid rgba(10, 10, 15, 0.12);
  border-left: 4px solid #ccc;
  box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.1);
  padding: 12px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 300px;
  max-width: 400px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-toast:hover {
  transform: translate(-4px, -4px);
}

.notification-icon {
  color: var(--pz-color-concrete-grey);
  margin-top: 2px;
}

.notification-content {
  flex: 1;
}

.notification-message {
  font-size: 0.88rem;
  color: var(--pz-color-foundation-black);
  margin: 0 0 4px 0;
  line-height: 1.4;
}

.notification-time {
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  font-family: var(--pz-font-mono);
  letter-spacing: 0.08em;
}

/* Variants */
.notification-toast--chat {
  border-left-color: var(--pz-color-steel-blue);
}
.notification-toast--chat .notification-icon {
  color: var(--pz-color-steel-blue);
}

.notification-toast--success {
  border-left-color: var(--pz-color-savanna-green);
}
.notification-toast--success .notification-icon {
  color: var(--pz-color-savanna-green);
}

.notification-toast--info {
  border-left-color: var(--pz-color-earth-orange);
}

.notification-toast--default {
  border-left-color: var(--pz-color-copper-circuit);
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
