<template>
  <div class="vendor-product-timeline">
    <div class="vpt-header">
      <h4 class="vpt-title">📅 Activity Timeline</h4>
    </div>
    <div v-if="loading" class="vpt-loading">Loading history...</div>
    <div v-else-if="!events.length" class="vpt-empty">
      No activity recorded yet.
    </div>
    <div v-else class="vpt-timeline">
      <div v-for="(event, index) in events" :key="event.id" class="vpt-event">
        <div class="vpt-event__line" :class="{ 'vpt-event__line--last': index === events.length - 1 && !upcomingEvents.length }">
          <div class="vpt-event__dot">{{ event.icon }}</div>
        </div>
        <div class="vpt-event__body">
          <div class="vpt-event__title">{{ event.title }}</div>
          <div class="vpt-event__desc">{{ event.description }}</div>
          <div class="vpt-event__meta">
            <span v-if="event.actor">by {{ event.actor }}</span>
            <span>{{ formatTime(event.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Upcoming Events -->
    <div v-if="upcomingEvents.length" class="vpt-upcoming">
      <div class="vpt-upcoming__header">⏳ Upcoming</div>
      <div v-for="evt in upcomingEvents" :key="evt.id" class="vpt-upcoming__item">
        <span class="vpt-upcoming__icon">{{ evt.icon }}</span>
        <div class="vpt-upcoming__body">
          <div class="vpt-upcoming__title">{{ evt.title }}</div>
          <div class="vpt-upcoming__date">{{ evt.date }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../services/api';

const props = defineProps({
  productId: { type: String, required: true },
  product: { type: Object, default: null },
});

const events = ref([]);
const loading = ref(false);

async function fetchTimeline() {
  loading.value = true;
  try {
    const res = await api.get(`/v1/products/${props.productId}/timeline/`);
    events.value = res.data.events || [];
  } catch (err) {
    console.error('Failed to load timeline', err);
  } finally {
    loading.value = false;
  }
}

function formatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
    + ' at ' + d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

function daysUntil(dateStr) {
  const d = new Date(dateStr);
  const diff = Math.ceil((d - Date.now()) / 86400000);
  return diff;
}

const upcomingEvents = computed(() => {
  const evts = [];
  const certs = props.product?.certification_entries || [];
  certs.forEach((c) => {
    if (c.expires_on) {
      const days = daysUntil(c.expires_on);
      if (days <= 90) {
        evts.push({
          id: `cert-${c.id}`,
          icon: days <= 30 ? '⚠️' : '📅',
          title: `${c.display_name || c.registry?.name || 'Certification'} expires in ${days} days`,
          date: new Date(c.expires_on).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }),
        });
      }
    }
  });
  return evts.sort((a, b) => new Date(a.date) - new Date(b.date));
});

onMounted(fetchTimeline);
</script>

<style scoped>
.vendor-product-timeline {
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(10, 10, 15, 0.04);
}

.vpt-header {
  margin-bottom: 0.75rem;
}

.vpt-title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 600;
}

.vpt-loading,
.vpt-empty {
  font-size: 0.85rem;
  color: var(--pz-color-concrete-grey);
  padding: 1rem 0;
  text-align: center;
}

.vpt-timeline {
  display: grid;
  gap: 0;
}

.vpt-event {
  display: grid;
  grid-template-columns: 2rem 1fr;
  gap: 0.75rem;
}

.vpt-event__line {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.vpt-event__line::before {
  content: '';
  width: 2px;
  flex: 1;
  background: rgba(10, 10, 15, 0.08);
  min-height: 0.5rem;
}

.vpt-event__line::after {
  content: '';
  width: 2px;
  flex: 1;
  background: rgba(10, 10, 15, 0.08);
  min-height: 0.5rem;
}

.vpt-event__line--last::after {
  display: none;
}

.vpt-event:first-child .vpt-event__line::before {
  display: none;
}

.vpt-event__dot {
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 50%;
  background: rgba(247, 244, 239, 0.9);
  border: 1px solid rgba(10, 10, 15, 0.08);
  display: grid;
  place-items: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.vpt-event__body {
  padding-bottom: 1rem;
}

.vpt-event__title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.vpt-event__desc {
  font-size: 0.8rem;
  color: var(--pz-color-text-secondary);
  margin-top: 0.15rem;
  line-height: 1.4;
}

.vpt-event__meta {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.3rem;
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  font-family: var(--pz-font-mono);
}

/* Upcoming Events */
.vpt-upcoming {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
}

.vpt-upcoming__header {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
  margin-bottom: 0.5rem;
}

.vpt-upcoming__item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0;
  font-size: 0.82rem;
}

.vpt-upcoming__icon {
  font-size: 1rem;
}

.vpt-upcoming__title {
  color: var(--pz-color-foundation-black);
}

.vpt-upcoming__date {
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  font-family: var(--pz-font-mono);
}
</style>
