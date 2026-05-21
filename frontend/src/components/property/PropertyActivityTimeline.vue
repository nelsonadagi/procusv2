<template>
  <div class="property-activity-timeline">
    <div class="pat-header">
      <div>
        <div class="pat-header__eyebrow">Timeline</div>
        <h4 class="pat-header__title">Property activity</h4>
      </div>
      <span class="pat-header__count">{{ events.length }}</span>
    </div>

    <div v-if="!events.length" class="pat-empty">
      No activity yet. The timeline will populate when the property is created, published, booked, or linked.
    </div>

    <div v-else class="pat-list">
      <div v-for="event in events" :key="event.id" class="pat-item" :class="`pat-item--${event.variant}`">
        <span class="pat-item__dot" aria-hidden="true"></span>
        <div class="pat-item__body">
          <div class="pat-item__meta">
            <strong class="pat-item__title">{{ event.title }}</strong>
            <span class="pat-item__time">{{ formatTime(event.timestamp) }}</span>
          </div>
          <p class="pat-item__message">{{ event.message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  events: { type: Array, default: () => [] },
});

function formatTime(value) {
  if (!value) return '';
  const date = new Date(value);
  return date.toLocaleString();
}
</script>

<style scoped>
.property-activity-timeline {
  display: grid;
  gap: 0.8rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: #fff;
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.03);
}

.pat-header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
}

.pat-header__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pat-header__title {
  margin: 0.2rem 0 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pat-header__count {
  display: inline-flex;
  align-items: center;
  min-height: 1.6rem;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.1);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
}

.pat-empty {
  padding: 0.75rem 0;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.6;
}

.pat-list {
  display: grid;
  gap: 0.7rem;
}

.pat-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  padding: 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.95);
}

.pat-item__dot {
  width: 0.7rem;
  height: 0.7rem;
  margin-top: 0.3rem;
  border-radius: 50%;
  background: var(--pz-color-earth-orange);
}

.pat-item--success .pat-item__dot {
  background: #16a34a;
}

.pat-item--warn .pat-item__dot {
  background: #d97706;
}

.pat-item--info .pat-item__dot {
  background: #2563eb;
}

.pat-item__body {
  display: grid;
  gap: 0.25rem;
  min-width: 0;
}

.pat-item__meta {
  display: flex;
  gap: 0.5rem;
  justify-content: space-between;
  align-items: baseline;
}

.pat-item__title {
  font-family: var(--pz-font-display);
  font-size: 0.9rem;
  color: var(--pz-color-foundation-black);
}

.pat-item__time,
.pat-item__message {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pat-item__message {
  margin: 0;
}
</style>
