<template>
  <button 
    :class="buttonClasses"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="pz-button__spinner"></span>
    <slot v-else></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'tertiary', 'ghost'].includes(v)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large', 'xsmall'].includes(v)
  },
  disabled: Boolean,
  loading: Boolean,
  fullWidth: Boolean
})

defineEmits(['click'])

const buttonClasses = computed(() => ({
  'pz-button': true,
  [`pz-button--${props.variant}`]: true,
  [`pz-button--${props.size}`]: true,
  'pz-button--full-width': props.fullWidth,
  'pz-button--loading': props.loading
}))
</script>

<style scoped>
.pz-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--pz-space-1);
  font-family: var(--pz-font-mono);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border: var(--pz-border-width) solid var(--pz-border-color-strong);
  border-radius: var(--pz-border-radius-sm);
  cursor: pointer;
  transition: all var(--pz-transition-base);
  text-decoration: none;
  box-shadow: var(--pz-shadow-sm);
}

.pz-button--xsmall {
  padding: 0.4rem 0.7rem;
  font-size: 0.68rem;
}

.pz-button--small {
  padding: var(--pz-space-1) var(--pz-space-2);
  font-size: var(--pz-text-caption);
}

.pz-button--medium {
  padding: var(--pz-space-2) var(--pz-space-3);
  font-size: var(--pz-text-small);
}

.pz-button--large {
  padding: calc(var(--pz-space-2) + 0.25rem) var(--pz-space-4);
  font-size: var(--pz-text-body);
}

.pz-button--primary {
  background-color: var(--pz-color-earth-orange);
  color: var(--pz-color-limestone-white);
  border-color: var(--pz-color-earth-orange);
  box-shadow: var(--pz-shadow-offset-sm);
}

.pz-button--primary:hover:not(:disabled) {
  background-color: #A84C1F;
  border-color: #A84C1F;
  transform: translate(-2px, -2px);
}

.pz-button--secondary {
  background-color: var(--pz-color-foundation-black);
  color: var(--pz-color-limestone-white);
  border-color: var(--pz-color-foundation-black);
  box-shadow: var(--pz-shadow-offset-sm);
}

.pz-button--secondary:hover:not(:disabled) {
  transform: translate(-2px, -2px);
}

.pz-button--tertiary {
  background-color: transparent;
  color: var(--pz-color-text-primary);
  border-color: transparent;
  text-transform: none;
  letter-spacing: normal;
  font-weight: var(--pz-weight-medium);
}

.pz-button--tertiary::after {
  content: '→';
  margin-left: var(--pz-space-1);
  transition: transform var(--pz-transition-base);
}

.pz-button--tertiary:hover:not(:disabled)::after {
  transform: translateX(4px);
}

.pz-button--ghost {
  background-color: transparent;
  color: var(--pz-color-text-secondary);
  border-color: transparent;
  box-shadow: none;
}

.pz-button--ghost:hover:not(:disabled) {
  background-color: rgba(10, 10, 15, 0.05);
  color: var(--pz-color-foundation-black);
}

.pz-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pz-button--full-width {
  width: 100%;
}

.pz-button__spinner {
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: pz-spin 0.75s linear infinite;
}

@keyframes pz-spin {
  to { transform: rotate(360deg); }
}
</style>
