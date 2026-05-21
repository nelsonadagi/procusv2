<template>
  <div class="pz-dashboard-shell" :class="[`pz-dashboard-shell--accent-${accent}`]">
    <div class="pz-l-container pz-dashboard-shell__layout">
      <!-- Sidebar -->
      <aside class="pz-dashboard-shell__sidebar">
        <nav class="pz-side-nav" aria-label="Dashboard navigation">
          <div
            v-for="(group, gIndex) in sidebarGroups"
            :key="gIndex"
            class="pz-side-nav__group"
            :class="{ 'u-mt-12': gIndex > 0 }"
          >
            <h3 class="pz-side-nav__title">{{ group.title }}</h3>
            <button
              v-for="item in group.items"
              :key="item.id"
              class="pz-side-nav__item"
              :class="{ 'pz-side-nav__item--active': activeSection === item.id }"
              :aria-current="activeSection === item.id ? 'page' : undefined"
              @click="item.action ? item.action() : $emit('update:activeSection', item.id)"
            >
              <span class="pz-side-nav__icon" aria-hidden="true">{{ item.icon }}</span>
              <span class="pz-side-nav__label">{{ item.label }}</span>
            </button>
          </div>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="pz-dashboard-shell__main">
        <!-- Masthead: signal + quickstats -->
        <div v-if="signalText || quickstats.length" class="pz-dashboard-shell__masthead">
          <div v-if="signalText" class="pz-dashboard-shell__signal">
            <span class="pz-dashboard-shell__signal-dot" aria-hidden="true"></span>
            <span>{{ signalText }}</span>
          </div>
          <div v-if="quickstats.length" class="pz-dashboard-shell__quickstats">
            <div
              v-for="(stat, i) in quickstats"
              :key="i"
              class="pz-dashboard-shell__quickstat"
            >
              <span class="pz-dashboard-shell__quickstat-label">{{ stat.label }}</span>
              <strong>{{ stat.value }}</strong>
            </div>
          </div>
        </div>

        <!-- Header row -->
        <header class="pz-dashboard-shell__header">
          <div class="pz-dashboard-shell__header-main">
            <div v-if="eyebrow" class="pz-dashboard-shell__eyebrow">{{ eyebrow }}</div>
            <h1 class="pz-u-text-display pz-dashboard-shell__title">{{ title }}</h1>
          </div>
          <div v-if="$slots.headerActions" class="pz-dashboard-shell__header-actions">
            <slot name="headerActions" />
          </div>
        </header>

        <!-- Content -->
        <div class="pz-dashboard-shell__content">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
defineProps({
  accent: {
    type: String,
    default: 'earth',
    validator: (v) => ['earth', 'copper', 'savanna', 'steel'].includes(v)
  },
  activeSection: {
    type: String,
    default: ''
  },
  sidebarGroups: {
    type: Array,
    default: () => []
  },
  signalText: {
    type: String,
    default: ''
  },
  quickstats: {
    type: Array,
    default: () => []
  },
  eyebrow: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    required: true
  }
});

defineEmits(['update:activeSection']);
</script>

<style scoped>
.pz-dashboard-shell {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding: var(--pz-space-4) 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(245, 243, 238, 0.9)),
    radial-gradient(circle at top right, rgba(212, 101, 42, 0.08), transparent 24%);
}

.pz-dashboard-shell--accent-copper {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(245, 243, 238, 0.9)),
    radial-gradient(circle at top right, rgba(184, 115, 51, 0.1), transparent 24%);
}

.pz-dashboard-shell--accent-savanna {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(245, 243, 238, 0.9)),
    radial-gradient(circle at top right, rgba(5, 150, 105, 0.08), transparent 24%);
}

.pz-dashboard-shell--accent-steel {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(245, 243, 238, 0.9)),
    radial-gradient(circle at top right, rgba(37, 99, 235, 0.08), transparent 24%);
}

/* Subtle grid overlay - reduced opacity for less visual fatigue */
.pz-dashboard-shell::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.022) calc(100% - 1px)),
    linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.018) calc(100% - 1px));
  background-size: 96px 96px;
  pointer-events: none;
}

@media (min-width: 768px) {
  .pz-dashboard-shell {
    padding: var(--pz-space-8) 0;
  }
}

.pz-dashboard-shell__layout {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-6);
}

@media (min-width: 1024px) {
  .pz-dashboard-shell__layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: var(--pz-space-8);
    align-items: start;
  }
}

.pz-dashboard-shell__sidebar {
  height: auto;
}

@media (min-width: 1024px) {
  .pz-dashboard-shell__sidebar {
    position: sticky;
    top: var(--pz-space-8);
    height: fit-content;
  }
}

.pz-dashboard-shell__main {
  min-width: 0;
  align-self: start;
}

/* Side Navigation */
.pz-side-nav {
  padding: 1.25rem;
  background: rgba(10, 10, 15, 0.96);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 16px 16px 0 rgba(10, 10, 15, 0.1);
}

.pz-side-nav__title {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.2em;
  margin-bottom: var(--pz-space-4);
  text-transform: uppercase;
}

.pz-side-nav__item {
  display: flex;
  align-items: center;
  gap: var(--pz-space-3);
  width: 100%;
  padding: var(--pz-space-4);
  box-sizing: border-box;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
  transition: all var(--pz-transition-spring);
  color: rgba(255, 255, 255, 0.82);
}

.pz-side-nav__item:hover {
  border-color: rgba(212, 101, 42, 0.5);
  color: white;
  transform: translateX(4px);
}

.pz-dashboard-shell--accent-copper .pz-side-nav__item:hover {
  border-color: rgba(184, 115, 51, 0.55);
}

.pz-dashboard-shell--accent-savanna .pz-side-nav__item:hover {
  border-color: rgba(5, 150, 105, 0.5);
}

.pz-side-nav__item--active {
  background: var(--pz-color-limestone-white);
  color: var(--pz-color-foundation-black);
  border-color: var(--pz-color-earth-orange);
  box-shadow: 6px 6px 0 rgba(212, 101, 42, 0.65);
  transform: translate(-4px, -4px);
}

.pz-dashboard-shell--accent-copper .pz-side-nav__item--active {
  border-color: var(--pz-color-copper-circuit);
  box-shadow: 6px 6px 0 rgba(184, 115, 51, 0.65);
}

.pz-dashboard-shell--accent-savanna .pz-side-nav__item--active {
  border-color: var(--pz-color-savanna-green);
  box-shadow: 6px 6px 0 rgba(5, 150, 105, 0.65);
}

.pz-side-nav__icon {
  font-size: 1.125rem;
  line-height: 1;
  flex-shrink: 0;
}

/* Masthead */
.pz-dashboard-shell__masthead {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.1);
}

.pz-dashboard-shell__signal,
.pz-dashboard-shell__quickstat-label {
  font-family: var(--pz-font-mono);
  text-transform: uppercase;
  letter-spacing: 0.16em;
}

.pz-dashboard-shell__signal {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.72rem;
  color: var(--pz-color-structural-steel);
}

.pz-dashboard-shell__signal-dot {
  width: 0.7rem;
  height: 0.7rem;
  background: var(--pz-color-savanna-green);
  border-radius: 999px;
  box-shadow: 0 0 0 4px rgba(52, 102, 51, 0.16);
}

.pz-dashboard-shell--accent-earth .pz-dashboard-shell__signal-dot {
  background: var(--pz-color-earth-orange);
  box-shadow: 0 0 0 4px rgba(212, 101, 42, 0.16);
}

.pz-dashboard-shell--accent-copper .pz-dashboard-shell__signal-dot {
  background: var(--pz-color-copper-circuit);
  box-shadow: 0 0 0 4px rgba(184, 115, 51, 0.16);
}

.pz-dashboard-shell--accent-steel .pz-dashboard-shell__signal-dot {
  background: var(--pz-color-steel-blue);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.16);
}

.pz-dashboard-shell__quickstats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.pz-dashboard-shell__quickstat {
  min-width: 120px;
  display: grid;
  gap: 0.2rem;
  padding: 0.7rem 0.85rem;
  background: rgba(10, 10, 15, 0.04);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-dashboard-shell__quickstat-label {
  font-size: 0.62rem;
  color: var(--pz-color-concrete-grey);
}

.pz-dashboard-shell__quickstat strong {
  font-size: 0.95rem;
  color: var(--pz-color-foundation-black);
}

/* Header */
.pz-dashboard-shell__header {
  margin-bottom: var(--pz-space-6);
  padding: clamp(1.25rem, 3vw, 2rem);
  background: rgba(255, 255, 255, 0.78);
  border: 2px solid var(--pz-color-foundation-black);
  box-shadow: 14px 14px 0 rgba(10, 10, 15, 0.08);
  backdrop-filter: blur(10px);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--pz-space-4);
}

@media (min-width: 768px) {
  .pz-dashboard-shell__header {
    margin-bottom: var(--pz-space-8);
  }
}

.pz-dashboard-shell__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  margin-bottom: var(--pz-space-2);
}

.pz-dashboard-shell--accent-copper .pz-dashboard-shell__eyebrow {
  color: var(--pz-color-copper-circuit);
}

.pz-dashboard-shell--accent-savanna .pz-dashboard-shell__eyebrow {
  color: var(--pz-color-savanna-green);
}

.pz-dashboard-shell--accent-steel .pz-dashboard-shell__eyebrow {
  color: var(--pz-color-steel-blue);
}

.pz-dashboard-shell__title {
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 0.92;
  letter-spacing: -0.06em;
  margin: 0;
}

/* Content */
.pz-dashboard-shell__content {
  padding: clamp(1rem, 2.5vw, 1.5rem);
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

/* Utility */
.u-mt-12 {
  margin-top: var(--pz-space-12);
}
</style>
