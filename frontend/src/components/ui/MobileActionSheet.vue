<template>
  <Teleport to="body">
    <Transition name="mas-backdrop">
      <div v-if="isOpen" class="mas-backdrop" @click="close">
        <Transition name="mas-sheet">
          <div v-if="isOpen" class="mas-sheet" @click.stop>
            <div class="mas-sheet__handle"></div>
            <div class="mas-sheet__header">
              <h4 class="mas-sheet__title">{{ title }}</h4>
              <button class="mas-sheet__close" @click="close">✕</button>
            </div>
            <div class="mas-sheet__body">
              <slot />
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  isOpen: { type: Boolean, default: false },
  title: { type: String, default: 'Actions' },
});

const emit = defineEmits(['close']);

function close() {
  emit('close');
}
</script>

<style scoped>
.mas-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 100;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.mas-sheet {
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 1rem 1rem 0 0;
  padding: 0.75rem 1rem 1.5rem;
  max-height: 80vh;
  overflow-y: auto;
  animation: mas-slide-up 0.25s ease-out;
}

@keyframes mas-slide-up {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.mas-sheet__handle {
  width: 36px;
  height: 4px;
  background: #cbd5e1;
  border-radius: 2px;
  margin: 0 auto 0.75rem;
}

.mas-sheet__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.mas-sheet__title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.mas-sheet__close {
  background: none;
  border: none;
  font-size: 1.1rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
}

.mas-backdrop-enter-active,
.mas-backdrop-leave-active {
  transition: opacity 0.2s;
}

.mas-backdrop-enter-from,
.mas-backdrop-leave-to {
  opacity: 0;
}
</style>
