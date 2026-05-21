<template>
  <div class="pz-empty-state" :class="{ 'pz-empty-state--compact': compact }">
    <div v-if="icon" class="pz-empty-state__icon" aria-hidden="true">{{ icon }}</div>
    <h3 v-if="title" class="pz-empty-state__title">{{ title }}</h3>
    <p v-if="description" class="pz-empty-state__description">{{ description }}</p>
    <p v-if="nextStep" class="pz-empty-state__next-step">
      <span class="pz-empty-state__next-step-label">Next step</span>
      <span class="pz-empty-state__next-step-text">{{ nextStep }}</span>
    </p>
    <div v-if="$slots.action" class="pz-empty-state__action">
      <slot name="action" />
    </div>
    <div v-else-if="actionLabel" class="pz-empty-state__action">
      <Button :variant="actionVariant" :size="actionSize" :disabled="actionDisabled" @click="$emit('action')">
        {{ actionLabel }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import Button from './Button.vue';

defineProps({
  icon: { type: String, default: '' },
  title: { type: String, default: '' },
  description: { type: String, default: '' },
  nextStep: { type: String, default: '' },
  actionLabel: { type: String, default: '' },
  actionVariant: { type: String, default: 'primary' },
  actionSize: { type: String, default: 'md' },
  actionDisabled: { type: Boolean, default: false },
  compact: { type: Boolean, default: false }
});

defineEmits(['action']);
</script>

<style scoped>
.pz-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: clamp(2.5rem, 6vw, 4rem) clamp(1.5rem, 4vw, 2.5rem);
  background: #ffffff;
  border: 1px solid rgba(10, 10, 15, 0.12);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.03);
}

.pz-empty-state--compact {
  padding: clamp(1.25rem, 3vw, 2rem);
}

.pz-empty-state__icon {
  font-size: 2.5rem;
  line-height: 1;
  margin-bottom: var(--pz-space-4);
  opacity: 0.85;
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

.pz-empty-state__next-step {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  max-width: 42ch;
  margin: 0 0 var(--pz-space-6);
}

.pz-empty-state__next-step-label {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-empty-state__next-step-text {
  font-family: var(--pz-font-mono);
  font-size: 0.8rem;
  line-height: 1.6;
  color: var(--pz-color-foundation-black);
}

.pz-empty-state__action {
  display: flex;
  gap: var(--pz-space-3);
  flex-wrap: wrap;
  justify-content: center;
}
</style>
