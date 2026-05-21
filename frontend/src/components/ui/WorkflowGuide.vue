<template>
  <div
    class="pz-workflow-guide"
    :class="{ 'pz-workflow-guide--open': isOpen, 'pz-workflow-guide--dismissed': isDismissed }"
    @keydown.escape="closePanel"
    @mouseleave="restoreHover"
    @focusout="handleFocusOut"
  >
    <button
      type="button"
      class="pz-workflow-guide__trigger"
      :aria-controls="panelId"
      :aria-expanded="isOpen ? 'true' : 'false'"
      :aria-label="`Start here: ${title}`"
      @click="togglePanel"
    >
      <span>{{ eyebrow }}</span>
      <strong>Start Here</strong>
      <em>{{ title }}</em>
    </button>
    <div
      :id="panelId"
      class="pz-workflow-guide__panel"
      role="dialog"
      :aria-label="`${title} actions`"
      @click.capture="handlePanelClick"
    >
      <div class="pz-workflow-guide__header">
        <div>
          <span>{{ eyebrow }}</span>
          <strong>{{ title }}</strong>
        </div>
        <small>Pick the next action</small>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from 'vue';

const props = defineProps({
  title: { type: String, default: 'Workflow Path' },
  eyebrow: { type: String, default: 'Start Here' },
});

const instance = getCurrentInstance();
const isOpen = ref(false);
const isDismissed = ref(false);
const panelId = computed(() => `workflow-guide-${instance?.uid || 'panel'}-${props.title.replace(/\W+/g, '-').toLowerCase()}`);

function togglePanel() {
  isDismissed.value = false;
  isOpen.value = !isOpen.value;
}

function closePanel({ dismiss = false } = {}) {
  isOpen.value = false;
  isDismissed.value = dismiss;
  if (dismiss && typeof document !== 'undefined') {
    document.activeElement?.blur?.();
  }
}

function restoreHover() {
  isDismissed.value = false;
}

function handleFocusOut(event) {
  if (!event.currentTarget.contains(event.relatedTarget)) {
    restoreHover();
  }
}

function handlePanelClick(event) {
  const action = event.target.closest('a, button, [role="button"], input[type="submit"], input[type="button"]');
  if (action) {
    closePanel({ dismiss: true });
  }
}
</script>

<style scoped>
.pz-workflow-guide {
  position: relative;
  display: inline-block;
  z-index: 30;
}

.pz-workflow-guide__trigger {
  position: relative;
  display: inline-grid;
  grid-template-columns: auto 1fr;
  column-gap: 0.75rem;
  row-gap: 0.08rem;
  min-width: 13.5rem;
  padding: 0.9rem 1.05rem 0.9rem 1.05rem;
  border: 2px solid rgba(169, 77, 28, 0.76);
  border-radius: 999px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 236, 213, 0.98)),
    #fff;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.45),
    0 14px 30px rgba(212, 101, 42, 0.24);
  text-align: left;
  cursor: pointer;
  animation: pz-start-here-breathe 2.8s ease-in-out infinite;
  transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, filter 0.16s ease;
}

.pz-workflow-guide__trigger::before {
  content: ">";
  grid-row: 1 / span 2;
  display: inline-flex;
  width: 2.35rem;
  height: 2.35rem;
  align-items: center;
  justify-content: center;
  align-self: center;
  border-radius: 999px;
  background: #b84f1f;
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 1.08rem;
  font-weight: 900;
  box-shadow: 0 8px 18px rgba(212, 101, 42, 0.3);
  transition: transform 0.16s ease, box-shadow 0.16s ease;
}

.pz-workflow-guide__trigger::after {
  content: "Open";
  position: absolute;
  top: -0.55rem;
  right: 1.1rem;
  display: inline-flex;
  align-items: center;
  min-height: 1.05rem;
  padding: 0 0.42rem;
  border-radius: 999px;
  background: #111827;
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.58rem;
  font-weight: 800;
  letter-spacing: 0;
}

.pz-workflow-guide__trigger:hover,
.pz-workflow-guide:focus-within .pz-workflow-guide__trigger,
.pz-workflow-guide--open .pz-workflow-guide__trigger {
  transform: translateY(-2px);
  border-color: rgba(212, 101, 42, 0.9);
  filter: saturate(1.08);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    0 18px 34px rgba(212, 101, 42, 0.34);
}

.pz-workflow-guide__trigger:hover::before,
.pz-workflow-guide:focus-within .pz-workflow-guide__trigger::before,
.pz-workflow-guide--open .pz-workflow-guide__trigger::before {
  transform: translateX(2px) scale(1.04);
  box-shadow: 0 10px 22px rgba(212, 101, 42, 0.38);
}

.pz-workflow-guide__trigger span,
.pz-workflow-guide__header span {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #374151;
}

.pz-workflow-guide__trigger strong,
.pz-workflow-guide__header strong {
  font-family: var(--pz-font-display);
  font-size: 1.08rem;
  color: var(--pz-color-foundation-black);
}

.pz-workflow-guide__trigger span,
.pz-workflow-guide__trigger strong,
.pz-workflow-guide__trigger em {
  grid-column: 2;
}

.pz-workflow-guide__trigger em {
  margin-top: 0.02rem;
  color: #374151;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  font-style: normal;
  line-height: 1.25;
}

@keyframes pz-start-here-breathe {
  0%,
  100% {
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.45),
      0 12px 26px rgba(212, 101, 42, 0.2);
  }

  50% {
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.5),
      0 18px 36px rgba(212, 101, 42, 0.34);
  }
}

.pz-workflow-guide__panel {
  position: absolute;
  top: calc(100% + 0.65rem);
  left: 0;
  width: min(64rem, calc(100vw - 2rem));
  max-height: min(70vh, 42rem);
  overflow: auto;
  padding: 1.1rem;
  border: 1px solid rgba(212, 101, 42, 0.18);
  border-radius: 14px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.99), rgba(255, 247, 237, 0.98)),
    #fff;
  box-shadow:
    0 24px 60px rgba(10, 10, 15, 0.16),
    0 12px 30px rgba(212, 101, 42, 0.1);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-0.35rem);
  transition: opacity 0.16s ease, transform 0.16s ease, visibility 0.16s ease;
  pointer-events: none;
}

.pz-workflow-guide__panel::before {
  content: "";
  position: absolute;
  top: -0.45rem;
  left: 1.6rem;
  width: 0.9rem;
  height: 0.9rem;
  transform: rotate(45deg);
  border-left: 1px solid rgba(212, 101, 42, 0.18);
  border-top: 1px solid rgba(212, 101, 42, 0.18);
  background: rgba(255, 255, 255, 0.99);
}

.pz-workflow-guide:hover .pz-workflow-guide__panel,
.pz-workflow-guide:focus-within .pz-workflow-guide__panel,
.pz-workflow-guide--open .pz-workflow-guide__panel {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

.pz-workflow-guide--dismissed:hover .pz-workflow-guide__panel,
.pz-workflow-guide--dismissed:focus-within .pz-workflow-guide__panel,
.pz-workflow-guide--dismissed.pz-workflow-guide--open .pz-workflow-guide__panel {
  opacity: 0;
  visibility: hidden;
  transform: translateY(-0.35rem);
  pointer-events: none;
}

.pz-workflow-guide__header {
  position: sticky;
  top: -1.1rem;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin: -1.1rem -1.1rem 1rem;
  padding: 1rem 1.1rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.08);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 243, 226, 0.96)),
    #fff;
}

.pz-workflow-guide__header > div {
  display: grid;
  gap: 0.16rem;
}

.pz-workflow-guide__header small {
  display: inline-flex;
  align-items: center;
  min-height: 1.55rem;
  padding: 0 0.65rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.1);
  color: #9a3f17;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  font-weight: 800;
  text-transform: uppercase;
  white-space: nowrap;
}

.pz-workflow-guide__panel :deep(.pz-module-cta) {
  margin-top: 1rem;
}

.pz-workflow-guide__panel :deep([class*="workflow-step"]),
.pz-workflow-guide__panel :deep([class*="workflow__metric"]),
.pz-workflow-guide__panel :deep([class*="workflow-banner__metric"]) {
  border-radius: 10px;
}

@media (max-width: 1024px) {
  .pz-workflow-guide__panel {
    left: 50%;
    width: min(34rem, calc(100vw - 2rem));
    transform: translate(-50%, -0.35rem);
  }

  .pz-workflow-guide:hover .pz-workflow-guide__panel,
  .pz-workflow-guide:focus-within .pz-workflow-guide__panel,
  .pz-workflow-guide--open .pz-workflow-guide__panel {
    transform: translate(-50%, 0);
  }
}

.pz-workflow-guide__trigger:focus-visible {
  outline: 3px solid rgba(17, 24, 39, 0.78);
  outline-offset: 4px;
}

@media (prefers-reduced-motion: reduce) {
  .pz-workflow-guide__trigger,
  .pz-workflow-guide__trigger::before,
  .pz-workflow-guide__panel {
    animation: none;
    transition: none;
  }
}
</style>
