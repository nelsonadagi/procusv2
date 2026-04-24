<template>
  <section class="pz-entry-hero" :class="{ 'pz-entry-hero--search-only': searchOnly }">
    <div class="pz-entry-hero__mesh" aria-hidden="true"></div>
    <div class="pz-l-container pz-entry-hero__container">
      <div v-if="!searchOnly" class="pz-entry-hero__intro">
        <p v-if="eyebrow" class="pz-entry-hero__eyebrow">{{ eyebrow }}</p>
        <h1 class="pz-entry-hero__title">{{ title }}</h1>
        <p class="pz-entry-hero__description">{{ description }}</p>
      </div>

      <div class="pz-entry-hero__panel">
        <form class="pz-entry-hero__search" :class="{ 'pz-entry-hero__search--compact': compact }" @submit.prevent="$emit('submit')">
          <div v-if="compact && browseOptions.length" class="pz-entry-hero__control">
            <label class="pz-entry-hero__control-label">{{ browseLabel }}</label>
            <select
              :value="browseValue"
              class="pz-entry-hero__select"
              @change="$emit('update:browseValue', $event.target.value)"
            >
              <option v-for="option in browseOptions" :key="String(option.value)" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <div v-if="compact" class="pz-entry-hero__control pz-entry-hero__control--search">
            <label class="pz-entry-hero__control-label">{{ searchGroupLabel }}</label>
            <div class="pz-entry-hero__search-stack">
              <select
                v-if="searchOptions.length"
                :value="searchOptionValue"
                class="pz-entry-hero__select pz-entry-hero__select--search-mode"
                @change="$emit('update:searchOptionValue', $event.target.value)"
              >
                <option v-for="option in searchOptions" :key="String(option.value)" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
              <div class="pz-entry-hero__search-input">
                <span class="pz-entry-hero__search-icon" aria-hidden="true">⌕</span>
                <input
                  :value="modelValue"
                  :placeholder="placeholder"
                  class="pz-entry-hero__input"
                  @input="$emit('update:modelValue', $event.target.value)"
                  @keyup.enter="$emit('submit')"
                >
              </div>
            </div>
          </div>

          <div v-else class="pz-entry-hero__search-input">
            <span class="pz-entry-hero__search-icon" aria-hidden="true">⌕</span>
            <input
              :value="modelValue"
              :placeholder="placeholder"
              class="pz-entry-hero__input"
              @input="$emit('update:modelValue', $event.target.value)"
              @keyup.enter="$emit('submit')"
            >
          </div>
          <div class="pz-entry-hero__search-actions">
            <slot name="actions"></slot>
            <Button variant="primary" size="lg" type="submit">{{ searchLabel }}</Button>
          </div>
        </form>

        <div v-if="links.length" class="pz-entry-hero__links">
          <router-link
            v-for="link in links"
            :key="`${link.to}-${link.label}`"
            :to="link.to"
            class="pz-entry-hero__link"
          >
            {{ link.label }}
          </router-link>
        </div>

        <div v-if="chips.length" class="pz-entry-hero__chips">
          <button
            v-for="chip in chips"
            :key="chip.id"
            type="button"
            class="pz-entry-hero__chip"
            :class="{ 'pz-entry-hero__chip--active': chip.active }"
            @click="$emit('chip-select', chip)"
          >
            {{ chip.label }}
          </button>
        </div>

        <div v-if="stats.length" class="pz-entry-hero__stats">
          <div v-for="stat in stats" :key="stat.label" class="pz-entry-hero__stat">
            <span class="pz-entry-hero__stat-value">{{ stat.value }}</span>
            <span class="pz-entry-hero__stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import Button from './Button.vue';

defineProps({
  eyebrow: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  searchOnly: {
    type: Boolean,
    default: false
  },
  compact: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: 'Search'
  },
  searchLabel: {
    type: String,
    default: 'Search'
  },
  modelValue: {
    type: String,
    default: ''
  },
  links: {
    type: Array,
    default: () => []
  },
  chips: {
    type: Array,
    default: () => []
  },
  stats: {
    type: Array,
    default: () => []
  },
  browseLabel: {
    type: String,
    default: 'Browse'
  },
  browseValue: {
    type: [String, Number],
    default: ''
  },
  browseOptions: {
    type: Array,
    default: () => []
  },
  searchGroupLabel: {
    type: String,
    default: 'Search'
  },
  searchOptionValue: {
    type: [String, Number],
    default: ''
  },
  searchOptions: {
    type: Array,
    default: () => []
  }
});

defineEmits([
  'update:modelValue',
  'update:browseValue',
  'update:searchOptionValue',
  'submit',
  'chip-select'
]);
</script>

<style scoped>
.pz-entry-hero {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  padding: clamp(3.75rem, 8vw, 5.75rem) 0 clamp(1.6rem, 3vw, 2.2rem);
  background:
    linear-gradient(180deg, rgba(255, 252, 247, 0.92), rgba(243, 239, 231, 0.96)),
    radial-gradient(circle at top left, rgba(212, 101, 42, 0.16), transparent 30%),
    radial-gradient(circle at 85% 18%, rgba(16, 185, 129, 0.12), transparent 18%);
  border-bottom: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-entry-hero--search-only {
  padding: 1rem 0 0.75rem;
  background:
    linear-gradient(180deg, rgba(255, 252, 247, 0.84), rgba(243, 239, 231, 0.9));
}

.pz-entry-hero--search-only::before,
.pz-entry-hero--search-only::after {
  display: none;
}

.pz-entry-hero::before,
.pz-entry-hero::after {
  content: "";
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
  z-index: 0;
}

.pz-entry-hero::before {
  width: 26rem;
  height: 26rem;
  top: -9rem;
  right: -7rem;
  background: radial-gradient(circle, rgba(212, 101, 42, 0.22), rgba(212, 101, 42, 0));
  filter: blur(8px);
}

.pz-entry-hero::after {
  width: 18rem;
  height: 18rem;
  left: -6rem;
  bottom: -7rem;
  background: radial-gradient(circle, rgba(10, 10, 15, 0.08), rgba(10, 10, 15, 0));
}

.pz-entry-hero__mesh {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.032) calc(100% - 1px)),
    linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.024) calc(100% - 1px)),
    linear-gradient(135deg, rgba(255, 255, 255, 0.45), transparent 38%);
  background-size: 84px 84px, 84px 84px, auto;
  opacity: 0.8;
  pointer-events: none;
}

.pz-entry-hero__container {
  position: relative;
  z-index: 1;
  display: grid;
  gap: var(--pz-space-8);
  align-items: end;
}

.pz-entry-hero--search-only .pz-entry-hero__container {
  gap: 0;
}

.pz-entry-hero__intro {
  max-width: 49rem;
  display: grid;
  gap: var(--pz-space-2);
}

.pz-entry-hero__eyebrow {
  margin: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-entry-hero__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(2.25rem, 5vw, 4.25rem);
  line-height: 0.95;
  letter-spacing: -0.06em;
  color: var(--pz-color-foundation-black);
  text-wrap: balance;
}

.pz-entry-hero__description {
  max-width: 46rem;
  margin: var(--pz-space-3) 0 0;
  font-size: 1.02rem;
  line-height: 1.75;
  color: var(--pz-color-text-secondary);
}

.pz-entry-hero__panel {
  display: grid;
  gap: var(--pz-space-5);
  padding: clamp(1rem, 2vw, 1.4rem);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 250, 242, 0.92));
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow:
    0 26px 60px rgba(10, 10, 15, 0.09),
    18px 18px 0 rgba(10, 10, 15, 0.05);
  backdrop-filter: blur(14px);
}

.pz-entry-hero--search-only .pz-entry-hero__panel {
  gap: 0;
  padding: 0;
  background: transparent;
  border: 0;
  box-shadow: none;
  backdrop-filter: none;
}

.pz-entry-hero__search {
  display: grid;
  gap: var(--pz-space-3);
}

.pz-entry-hero--search-only .pz-entry-hero__search {
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: stretch;
}

.pz-entry-hero__control {
  display: grid;
  gap: 0.55rem;
}

.pz-entry-hero__control-label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-entry-hero__search-stack {
  display: grid;
  gap: var(--pz-space-2);
}

.pz-entry-hero__search-input {
  display: flex;
  align-items: center;
  gap: var(--pz-space-3);
  padding: 0 var(--pz-space-4);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 247, 242, 0.92));
  border: 1px solid rgba(10, 10, 15, 0.09);
  min-height: 4.2rem;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

.pz-entry-hero--search-only .pz-entry-hero__search-input {
  min-height: 4rem;
  box-shadow: 0 10px 30px rgba(10, 10, 15, 0.06);
}

.pz-entry-hero__select {
  min-height: 4.2rem;
  border: 1px solid rgba(10, 10, 15, 0.09);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(249, 247, 242, 0.92));
  padding: 0 1rem;
  font-family: var(--pz-font-primary);
  font-size: 0.96rem;
  color: var(--pz-color-foundation-black);
  outline: none;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

.pz-entry-hero__search-icon {
  color: var(--pz-color-earth-orange);
  font-size: 1.1rem;
}

.pz-entry-hero__input {
  flex: 1;
  width: 100%;
  border: none;
  background: transparent;
  font-size: 1.02rem;
  color: var(--pz-color-foundation-black);
}

.pz-entry-hero__input::placeholder {
  color: rgba(69, 77, 95, 0.58);
}

.pz-entry-hero__input:focus {
  outline: none;
}

.pz-entry-hero__search-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--pz-space-3);
  align-items: stretch;
}

.pz-entry-hero--search-only .pz-entry-hero__search-actions {
  flex-wrap: nowrap;
  justify-content: flex-end;
}

.pz-entry-hero--search-only .pz-entry-hero__links,
.pz-entry-hero--search-only .pz-entry-hero__chips,
.pz-entry-hero--search-only .pz-entry-hero__stats {
  display: none;
}

.pz-entry-hero__links,
.pz-entry-hero__chips,
.pz-entry-hero__stats {
  display: flex;
  flex-wrap: wrap;
  gap: var(--pz-space-3);
}

.pz-entry-hero__link,
.pz-entry-hero__chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.7rem;
  padding: 0.65rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.82);
  font-family: var(--pz-font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--pz-color-foundation-black);
  transition: transform var(--pz-transition-spring), border-color var(--pz-transition-base), background var(--pz-transition-base), box-shadow var(--pz-transition-base);
}

.pz-entry-hero__link:hover,
.pz-entry-hero__chip:hover,
.pz-entry-hero__chip--active {
  transform: translate(-2px, -2px);
  border-color: var(--pz-color-earth-orange);
  background: #fff7ee;
  box-shadow: 8px 8px 0 rgba(10, 10, 15, 0.05);
}

.pz-entry-hero__chip {
  cursor: pointer;
}

.pz-entry-hero__stat {
  min-width: 9rem;
  padding: var(--pz-space-3) var(--pz-space-4);
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: linear-gradient(180deg, rgba(10, 10, 15, 0.05), rgba(10, 10, 15, 0.02));
}

.pz-entry-hero__stat-value {
  display: block;
  font-family: var(--pz-font-display);
  font-size: 1.25rem;
  color: var(--pz-color-foundation-black);
}

.pz-entry-hero__stat-label {
  display: block;
  margin-top: 0.2rem;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

@media (min-width: 900px) {
  .pz-entry-hero__container {
    grid-template-columns: minmax(0, 1.15fr) minmax(24rem, 0.95fr);
  }

  .pz-entry-hero__search {
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: stretch;
  }

  .pz-entry-hero__search--compact {
    grid-template-columns: minmax(14rem, 0.78fr) minmax(0, 1.35fr) auto;
    align-items: end;
  }

  .pz-entry-hero__search-actions {
    flex-wrap: nowrap;
  }
}

@media (max-width: 640px) {
  .pz-entry-hero--search-only .pz-entry-hero__search {
    grid-template-columns: 1fr;
  }

  .pz-entry-hero--search-only .pz-entry-hero__search-actions {
    flex-wrap: wrap;
  }

  .pz-entry-hero__panel {
    padding: var(--pz-space-4);
    box-shadow:
      0 20px 44px rgba(10, 10, 15, 0.08),
      12px 12px 0 rgba(10, 10, 15, 0.05);
  }

  .pz-entry-hero__stat {
    min-width: calc(50% - var(--pz-space-3));
  }
}
</style>
