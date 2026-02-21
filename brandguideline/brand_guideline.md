# Paanguzo Brand Implementation Guide
## Vue 3 + Vanilla CSS + BEM Methodology

---

## 1. Project Structure

```text
src/
├── styles/
│   ├── variables.css
│   ├── base.css
│   ├── utilities.css
│   └── main.css
├── components/
│   ├── PzButton.vue
│   ├── PzCard.vue
│   ├── PzInput.vue
│   ├── PzBadge.vue
│   ├── PzDataTable.vue
│   ├── PzNavigation.vue
│   └── PzPhaseIndicator.vue
└── main.js
```

---

## 2. Global Styles

### `src/styles/variables.css`

```css
:root {
  /* Primary Colors */
  --pz-color-foundation-black: #0A0A0F;
  --pz-color-structural-steel: #2D3748;
  --pz-color-concrete-grey: #718096;
  --pz-color-limestone-white: #FAFAF8;
  
  /* Accent Colors */
  --pz-color-earth-orange: #D4652A;
  --pz-color-copper-circuit: #B87333;
  --pz-color-steel-blue: #2563EB;
  --pz-color-savanna-green: #059669;
  --pz-color-african-violet: #7C3AED;
  
  /* Semantic Mappings */
  --pz-color-text-primary: var(--pz-color-foundation-black);
  --pz-color-text-secondary: var(--pz-color-structural-steel);
  --pz-color-text-tertiary: var(--pz-color-concrete-grey);
  --pz-color-background-primary: var(--pz-color-limestone-white);
  --pz-color-background-dark: var(--pz-color-foundation-black);
  --pz-color-accent-primary: var(--pz-color-earth-orange);
  --pz-color-accent-finance: var(--pz-color-copper-circuit);
  --pz-color-accent-tech: var(--pz-color-steel-blue);
  --pz-color-accent-success: var(--pz-color-savanna-green);
  --pz-color-accent-innovation: var(--pz-color-african-violet);
  
  /* Typography */
  --pz-font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --pz-font-display: 'Space Grotesk', sans-serif;
  --pz-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Type Scale */
  --pz-text-display: 4rem;
  --pz-text-h1: 3rem;
  --pz-text-h2: 2rem;
  --pz-text-h3: 1.5rem;
  --pz-text-h4: 1.25rem;
  --pz-text-body-lg: 1.125rem;
  --pz-text-body: 1rem;
  --pz-text-small: 0.875rem;
  --pz-text-caption: 0.75rem;
  
  /* Font Weights */
  --pz-weight-regular: 400;
  --pz-weight-medium: 500;
  --pz-weight-semibold: 600;
  --pz-weight-bold: 700;
  
  /* Line Heights */
  --pz-leading-tight: 1.1;
  --pz-leading-snug: 1.2;
  --pz-leading-normal: 1.3;
  --pz-leading-relaxed: 1.4;
  --pz-leading-loose: 1.5;
  --pz-leading-body: 1.6;
  
  /* Spacing Scale (8px base) */
  --pz-space-1: 0.5rem;
  --pz-space-2: 1rem;
  --pz-space-3: 1.5rem;
  --pz-space-4: 2rem;
  --pz-space-6: 3rem;
  --pz-space-8: 4rem;
  --pz-space-12: 6rem;
  
  /* Borders */
  --pz-border-width: 1px;
  --pz-border-width-thick: 2px;
  --pz-border-radius: 0px;
  
  /* Shadows */
  --pz-shadow-none: none;
  --pz-shadow-sm: 0 1px 2px rgba(10, 10, 15, 0.05);
  
  /* Transitions */
  --pz-transition-fast: 150ms ease-in-out;
  --pz-transition-base: 200ms ease-in-out;
  
  /* Z-index Scale */
  --pz-z-base: 0;
  --pz-z-dropdown: 100;
  --pz-z-sticky: 200;
  --pz-z-modal: 300;
  --pz-z-popover: 400;
  --pz-z-tooltip: 500;
}
```

### `src/styles/base.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700&family=JetBrains+Mono:wght@400&display=swap');

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--pz-font-primary);
  font-size: var(--pz-text-body);
  line-height: var(--pz-leading-body);
  color: var(--pz-color-text-primary);
  background-color: var(--pz-color-background-primary);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--pz-font-display);
  font-weight: var(--pz-weight-bold);
  line-height: var(--pz-leading-snug);
  color: var(--pz-color-text-primary);
}

h1 { font-size: var(--pz-text-h1); }
h2 { font-size: var(--pz-text-h2); }
h3 { font-size: var(--pz-text-h3); }
h4 { font-size: var(--pz-text-h4); }

code, pre, kbd, samp {
  font-family: var(--pz-font-mono);
  font-size: var(--pz-text-small);
}

a {
  color: var(--pz-color-accent-tech);
  text-decoration: none;
  transition: color var(--pz-transition-fast);
}

a:hover {
  color: var(--pz-color-foundation-black);
}

:focus-visible {
  outline: 2px solid var(--pz-color-steel-blue);
  outline-offset: 2px;
}

::selection {
  background-color: var(--pz-color-earth-orange);
  color: var(--pz-color-limestone-white);
}
```

### `src/styles/utilities.css`

```css
.pz-u-text-mono { font-family: var(--pz-font-mono) !important; }
.pz-u-text-display { font-family: var(--pz-font-display) !important; }
.pz-u-text-uppercase { text-transform: uppercase !important; letter-spacing: 0.05em; }
.pz-u-text-center { text-align: center !important; }
.pz-u-text-right { text-align: right !important; }

.pz-u-color-earth { color: var(--pz-color-earth-orange) !important; }
.pz-u-color-copper { color: var(--pz-color-copper-circuit) !important; }
.pz-u-color-steel { color: var(--pz-color-steel-blue) !important; }
.pz-u-color-savanna { color: var(--pz-color-savanna-green) !important; }
.pz-u-color-violet { color: var(--pz-color-african-violet) !important; }

.pz-u-mb-1 { margin-bottom: var(--pz-space-1) !important; }
.pz-u-mb-2 { margin-bottom: var(--pz-space-2) !important; }
.pz-u-mb-3 { margin-bottom: var(--pz-space-3) !important; }
.pz-u-mb-4 { margin-bottom: var(--pz-space-4) !important; }

.pz-u-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

### `src/styles/main.css`

```css
@import 'variables.css';
@import 'base.css';
@import 'utilities.css';
```

---

## 3. Vue Components

### `PzButton.vue`

```vue
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
    validator: (v) => ['small', 'medium', 'large'].includes(v)
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
  font-family: var(--pz-font-primary);
  font-weight: var(--pz-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.0625em;
  border: var(--pz-border-width) solid transparent;
  border-radius: var(--pz-border-radius);
  cursor: pointer;
  transition: all var(--pz-transition-base);
  text-decoration: none;
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
}

.pz-button--primary:hover:not(:disabled) {
  background-color: #B8531F;
  border-color: #B8531F;
  transform: translateY(-2px);
}

.pz-button--secondary {
  background-color: transparent;
  color: var(--pz-color-steel-blue);
  border-color: var(--pz-color-steel-blue);
}

.pz-button--secondary:hover:not(:disabled) {
  background-color: rgba(37, 99, 235, 0.1);
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
  border-color: var(--pz-color-concrete-grey);
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
```

### `PzCard.vue`

```vue
<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="pz-card__header">
      <slot name="header"></slot>
    </div>
    <div class="pz-card__body">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="pz-card__footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  hoverable: Boolean,
  padding: {
    type: String,
    default: 'medium',
    validator: (v) => ['none', 'small', 'medium', 'large'].includes(v)
  }
})

const cardClasses = computed(() => ({
  'pz-card': true,
  'pz-card--hoverable': props.hoverable,
  [`pz-card--padding-${props.padding}`]: true
}))
</script>

<style scoped>
.pz-card {
  background-color: var(--pz-color-limestone-white);
  border: var(--pz-border-width) solid rgba(113, 128, 150, 0.2);
  border-radius: var(--pz-border-radius);
  transition: border-color var(--pz-transition-base);
}

.pz-card--hoverable:hover {
  border-color: var(--pz-color-earth-orange);
}

.pz-card--padding-none .pz-card__body {
  padding: 0;
}

.pz-card--padding-small .pz-card__body {
  padding: var(--pz-space-2);
}

.pz-card--padding-medium .pz-card__body {
  padding: var(--pz-space-3);
}

.pz-card--padding-large .pz-card__body {
  padding: var(--pz-space-4);
}

.pz-card__header {
  padding: var(--pz-space-3);
  border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
}

.pz-card__footer {
  padding: var(--pz-space-3);
  border-top: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
}
</style>
```

### `PzInput.vue`

```vue
<template>
  <div class="pz-input-wrapper">
    <label v-if="label" :for="inputId" class="pz-input__label">
      {{ label }}
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="inputClasses"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <span v-if="error" class="pz-input__error">{{ error }}</span>
    <span v-else-if="hint" class="pz-input__hint">{{ hint }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: String,
  label: String,
  type: {
    type: String,
    default: 'text'
  },
  placeholder: String,
  disabled: Boolean,
  error: String,
  hint: String,
  size: {
    type: String,
    default: 'medium'
  }
})

defineEmits(['update:modelValue'])

const inputId = computed(() => `pz-input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => ({
  'pz-input': true,
  'pz-input--error': props.error,
  [`pz-input--${props.size}`]: true
}))
</script>

<style scoped>
.pz-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-1);
}

.pz-input__label {
  font-size: var(--pz-text-caption);
  font-weight: var(--pz-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--pz-color-concrete-grey);
}

.pz-input {
  font-family: var(--pz-font-primary);
  font-size: var(--pz-text-body);
  color: var(--pz-color-text-primary);
  background-color: var(--pz-color-limestone-white);
  border: var(--pz-border-width) solid var(--pz-color-concrete-grey);
  border-radius: var(--pz-border-radius);
  padding: var(--pz-space-2);
  transition: all var(--pz-transition-fast);
}

.pz-input:focus {
  outline: none;
  border-width: var(--pz-border-width-thick);
  border-color: var(--pz-color-steel-blue);
}

.pz-input--error {
  border-color: var(--pz-color-earth-orange);
}

.pz-input--error:focus {
  border-color: var(--pz-color-earth-orange);
}

.pz-input:disabled {
  background-color: rgba(113, 128, 150, 0.1);
  cursor: not-allowed;
}

.pz-input__error {
  font-size: var(--pz-text-caption);
  color: var(--pz-color-earth-orange);
}

.pz-input__hint {
  font-size: var(--pz-text-caption);
  color: var(--pz-color-concrete-grey);
}
</style>
```

### `PzBadge.vue`

```vue
<template>
  <span :class="badgeClasses">
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'success', 'warning', 'error', 'info', 'finance'].includes(v)
  },
  size: {
    type: String,
    default: 'medium'
  }
})

const badgeClasses = computed(() => ({
  'pz-badge': true,
  [`pz-badge--${props.variant}`]: true,
  [`pz-badge--${props.size}`]: true
}))
</script>

<style scoped>
.pz-badge {
  display: inline-flex;
  align-items: center;
  font-family: var(--pz-font-primary);
  font-weight: var(--pz-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: var(--pz-border-radius);
}

.pz-badge--small {
  padding: 0.25rem 0.5rem;
  font-size: var(--pz-text-caption);
}

.pz-badge--medium {
  padding: 0.5rem 0.75rem;
  font-size: var(--pz-text-small);
}

.pz-badge--default {
  background-color: rgba(113, 128, 150, 0.1);
  color: var(--pz-color-structural-steel);
}

.pz-badge--success {
  background-color: rgba(5, 150, 105, 0.1);
  color: var(--pz-color-savanna-green);
}

.pz-badge--info {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--pz-color-steel-blue);
}

.pz-badge--finance {
  background-color: rgba(184, 115, 51, 0.1);
  color: var(--pz-color-copper-circuit);
}

.pz-badge--warning {
  background-color: rgba(212, 101, 42, 0.1);
  color: var(--pz-color-earth-orange);
}

.pz-badge--error {
  background-color: rgba(212, 101, 42, 0.15);
  color: #B8531F;
}
</style>
```

### `PzDataTable.vue`

```vue
<template>
  <div class="pz-table-wrapper">
    <table class="pz-table">
      <thead class="pz-table__head">
        <tr>
          <th 
            v-for="column in columns" 
            :key="column.key"
            class="pz-table__th"
            :class="{ 'pz-table__th--numeric': column.numeric }"
          >
            {{ column.label }}
          </th>
        </tr>
      </thead>
      <tbody class="pz-table__body">
        <tr 
          v-for="(row, index) in data" 
          :key="index"
          class="pz-table__tr"
        >
          <td 
            v-for="column in columns" 
            :key="column.key"
            class="pz-table__td"
            :class="{ 
              'pz-table__td--numeric': column.numeric,
              'pz-table__td--mono': column.numeric || column.mono
            }"
          >
            <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
              {{ row[column.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.pz-table-wrapper {
  overflow-x: auto;
  border: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
}

.pz-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--pz-text-small);
}

.pz-table__head {
  background-color: var(--pz-color-foundation-black);
}

.pz-table__th {
  padding: var(--pz-space-2) var(--pz-space-3);
  text-align: left;
  font-family: var(--pz-font-primary);
  font-weight: var(--pz-weight-semibold);
  color: var(--pz-color-limestone-white);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: var(--pz-text-caption);
  white-space: nowrap;
}

.pz-table__th--numeric {
  text-align: right;
}

.pz-table__tr:nth-child(even) {
  background-color: #F5F5F3;
}

.pz-table__td {
  padding: var(--pz-space-2) var(--pz-space-3);
  color: var(--pz-color-text-primary);
  border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
}

.pz-table__td--numeric {
  text-align: right;
}

.pz-table__td--mono {
  font-family: var(--pz-font-mono);
  font-variant-numeric: tabular-nums;
}
</style>
```

### `PzNavigation.vue`

```vue
<template>
  <nav class="pz-nav" :class="{ 'pz-nav--dark': dark }">
    <div class="pz-nav__brand">
      <router-link to="/" class="pz-nav__logo">
        <span class="pz-nav__logo-text">PAANGUZO</span>
        <span class="pz-nav__logo-line"></span>
      </router-link>
    </div>
    
    <div class="pz-nav__menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path"
        :to="item.path"
        class="pz-nav__link"
        :class="{ 'pz-nav__link--active': $route.path === item.path }"
      >
        {{ item.label }}
      </router-link>
    </div>
    
    <div class="pz-nav__actions">
      <slot name="actions"></slot>
    </div>
  </nav>
</template>

<script setup>
defineProps({
  dark: Boolean,
  menuItems: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.pz-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 var(--pz-space-4);
  background-color: var(--pz-color-limestone-white);
  border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.2);
}

.pz-nav--dark {
  background-color: var(--pz-color-foundation-black);
  border-bottom-color: rgba(250, 250, 248, 0.1);
}

.pz-nav__logo {
  display: flex;
  flex-direction: column;
  text-decoration: none;
}

.pz-nav__logo-text {
  font-family: var(--pz-font-display);
  font-size: var(--pz-text-h4);
  font-weight: var(--pz-weight-bold);
  color: var(--pz-color-foundation-black);
  letter-spacing: 0.02em;
}

.pz-nav--dark .pz-nav__logo-text {
  color: var(--pz-color-limestone-white);
}

.pz-nav__logo-line {
  display: block;
  height: 3px;
  background-color: var(--pz-color-earth-orange);
  margin-top: 2px;
}

.pz-nav__menu {
  display: flex;
  gap: var(--pz-space-4);
}

.pz-nav__link {
  font-family: var(--pz-font-primary);
  font-size: var(--pz-text-small);
  font-weight: var(--pz-weight-medium);
  color: var(--pz-color-text-secondary);
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: var(--pz-space-1) 0;
  border-bottom: 2px solid transparent;
  transition: all var(--pz-transition-fast);
}

.pz-nav__link:hover,
.pz-nav__link--active {
  color: var(--pz-color-earth-orange);
  border-bottom-color: var(--pz-color-earth-orange);
}

.pz-nav--dark .pz-nav__link {
  color: var(--pz-color-concrete-grey);
}

.pz-nav--dark .pz-nav__link:hover,
.pz-nav--dark .pz-nav__link--active {
  color: var(--pz-color-limestone-white);
  border-bottom-color: var(--pz-color-earth-orange);
}
</style>
```

### `PzPhaseIndicator.vue`

```vue
<template>
  <div :class="indicatorClasses">
    <span class="pz-phase__number">Phase {{ phase }}</span>
    <span class="pz-phase__name">{{ phaseName }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  phase: {
    type: Number,
    required: true,
    validator: (v) => v >= 1 && v <= 6
  },
  size: {
    type: String,
    default: 'medium'
  }
})

const phaseNames = {
  1: 'Materials',
  2: 'Contracts',
  3: 'Finance',
  4: 'Projects',
  5: 'Institutional',
  6: 'Infrastructure'
}

const phaseColors = {
  1: 'earth',
  2: 'steel',
  3: 'copper',
  4: 'violet',
  5: 'foundation',
  6: 'gradient'
}

const phaseName = computed(() => phaseNames[props.phase])

const indicatorClasses = computed(() => ({
  'pz-phase': true,
  [`pz-phase--${props.size}`]: true,
  [`pz-phase--color-${phaseColors[props.phase]}`]: true
}))
</script>

<style scoped>
.pz-phase {
  display: inline-flex;
  flex-direction: column;
  gap: 0.25rem;
}

.pz-phase__number {
  font-family: var(--pz-font-mono);
  font-size: var(--pz-text-caption);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.pz-phase__name {
  font-family: var(--pz-font-display);
  font-weight: var(--pz-weight-bold);
}

.pz-phase--small .pz-phase__name {
  font-size: var(--pz-text-small);
}

.pz-phase--medium .pz-phase__name {
  font-size: var(--pz-text-body);
}

.pz-phase--large .pz-phase__name {
  font-size: var(--pz-text-h3);
}

.pz-phase--color-earth { color: var(--pz-color-earth-orange); }
.pz-phase--color-steel { color: var(--pz-color-steel-blue); }
.pz-phase--color-copper { color: var(--pz-color-copper-circuit); }
.pz-phase--color-violet { color: var(--pz-color-african-violet); }
.pz-phase--color-foundation { color: var(--pz-color-foundation-black); }
</style>
```

---

## 4. Setup Instructions

### `index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Paanguzo - Global Construction Marketplace OS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700&family=JetBrains+Mono&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

### `main.js`

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
```

---

## 5. Usage Examples

### Basic Page Template

```vue
<template>
  <div class="pz-page">
    <PzNavigation :menuItems="menuItems" />
    
    <main class="pz-page__content">
      <header class="pz-page__header">
        <PzPhaseIndicator :phase="1" size="large" />
        <h1 class="pz-page__title">Materials Marketplace</h1>
        <p class="pz-page__subtitle">
          Source construction materials with verified suppliers
        </p>
      </header>
      
      <div class="pz-page__grid">
        <PzCard v-for="supplier in suppliers" :key="supplier.id" hoverable>
          <template #header>
            <h3 class="pz-card__title">{{ supplier.name }}</h3>
            <PzBadge variant="success">Verified</PzBadge>
          </template>
          <p>{{ supplier.description }}</p>
          <PzButton variant="primary" fullWidth>
            Request Quote
          </PzButton>
        </PzCard>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PzNavigation from '@/components/PzNavigation.vue'
import PzPhaseIndicator from '@/components/PzPhaseIndicator.vue'
import PzCard from '@/components/PzCard.vue'
import PzBadge from '@/components/PzBadge.vue'
import PzButton from '@/components/PzButton.vue'

const menuItems = ref([
  { path: '/materials', label: 'Materials' },
  { path: '/contracts', label: 'Contracts' },
  { path: '/finance', label: 'Finance' }
])

const suppliers = ref([
  { id: 1, name: 'SteelCorp Ltd', description: 'Structural steel supplier' }
])
</script>

<style scoped>
.pz-page {
  min-height: 100vh;
}

.pz-page__content {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--pz-space-6) var(--pz-space-4);
}

.pz-page__header {
  margin-bottom: var(--pz-space-6);
}

.pz-page__title {
  margin-top: var(--pz-space-2);
  margin-bottom: var(--pz-space-2);
}

.pz-page__subtitle {
  color: var(--pz-color-text-secondary);
  font-size: var(--pz-text-body-lg);
}

.pz-page__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--pz-space-4);
}

.pz-card__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: var(--pz-text-h4);
}
</style>
```

---

## 6. BEM Naming Conventions

| Pattern | Example | Usage |
| :--- | :--- | :--- |
| **Block** | `.pz-button` | Component root |
| **Element** | `.pz-button__spinner` | Child element |
| **Modifier** | `.pz-button--primary` | Variant |
| **State** | `.pz-button--loading` or `.is-active` | Conditional state |

---

## 7. Color Usage by Platform Phase

| Phase | Name | Primary Color | Usage |
| :--- | :--- | :--- | :--- |
| **1** | Materials | Earth Orange | CTAs, procurement actions |
| **2** | Contracts | Steel Blue | Contractor features, tech |
| **3** | Finance | Copper Circuit | Financial products, escrow |
| **4** | Projects | African Violet | Project pipeline, capital |
| **5** | Institutional | Foundation Black | Enterprise, government |
| **6** | Infrastructure | All colors | Global integration |

---

## 8. Critical Rules

- [ ] **Never use gradients** (flat colors only)
- [ ] **Never round corners on primary buttons** (radius: 0)
- [ ] **Never use hardcoded values** (always use CSS variables)
- [ ] **Never mix competing accent colors in single view**
- [ ] **Never use `!important`** except in utility classes
- [ ] **Always use BEM naming** (`block__element--modifier`)
- [ ] **Always use `tabular-nums`** for financial data
- [ ] **Always use monospace** for transaction IDs and codes
