<template>
  <div class="pz-empty-state" :class="{ 'pz-empty-state--compact': compact }">
    <div v-if="icon" class="pz-empty-state__icon" aria-hidden="true">{{ icon }}</div>
    <h3 v-if="title" class="pz-empty-state__title">{{ title }}</h3>
    <p v-if="description" class="pz-empty-state__description">{{ description }}</p>
    <div v-if="$slots.action" class="pz-empty-state__action">
      <slot name="action" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, default: '' },
  title: { type: String, default: '' },
  description: { type: String, default: '' },
  compact: { type: Boolean, default: false }
});
</script>

<style scoped>
.pz-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: clamp(2.5rem, 6vw, 4rem) clamp(1.5rem, 4vw, 2.5rem);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-empty-state--compact {
  padding: clamp(1.25rem, 3vw, 2rem);
}

.pz-empty-state__icon {
  font-size: 2.5rem;
  line-height: 1;
  margin-bottom: var(--pz-space-4);
  opacity: 0.7;
}

.pz-empty-state__title {
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-weight: var(--pz-weight-bold);
  color: var(--pz-color-foundation-black);
  margin: 0 0 var(--pz-space-2);
  letter-spacing: -0.03em;
}

.pz-empty-state__description {
  font-family: var(--pz-font-mono);
  font-size: 0.8rem;
  color: var(--pz-color-concrete-grey);
  max-width: 42ch;
  margin: 0 0 var(--pz-space-6);
  line-height: 1.6;
}

.pz-empty-state__action {
  display: flex;
  gap: var(--pz-space-3);
  flex-wrap: wrap;
  justify-content: center;
}
</style>
