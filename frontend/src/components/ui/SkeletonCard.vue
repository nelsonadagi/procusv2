<template>
  <div class="pz-skeleton-card" :class="{ 'pz-skeleton-card--list': list }">
    <div v-if="!list" class="pz-skeleton-card__media"></div>
    <div class="pz-skeleton-card__body">
      <div class="pz-skeleton-card__line pz-skeleton-card__line--short"></div>
      <div class="pz-skeleton-card__line"></div>
      <div class="pz-skeleton-card__line pz-skeleton-card__line--half"></div>
      <div class="pz-skeleton-card__footer">
        <div class="pz-skeleton-card__line pz-skeleton-card__line--button"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  list: { type: Boolean, default: false }
});
</script>

<style scoped>
.pz-skeleton-card {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.04);
  overflow: hidden;
}

.pz-skeleton-card--list {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 0;
}

.pz-skeleton-card__media {
  height: 160px;
  background: linear-gradient(90deg, rgba(10,10,15,0.04) 25%, rgba(10,10,15,0.08) 50%, rgba(10,10,15,0.04) 75%);
  background-size: 200% 100%;
  animation: pz-skeleton-shimmer 1.5s infinite;
}

.pz-skeleton-card__body {
  padding: var(--pz-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-3);
}

.pz-skeleton-card__line {
  height: 12px;
  background: linear-gradient(90deg, rgba(10,10,15,0.04) 25%, rgba(10,10,15,0.08) 50%, rgba(10,10,15,0.04) 75%);
  background-size: 200% 100%;
  animation: pz-skeleton-shimmer 1.5s infinite;
  border-radius: 2px;
}

.pz-skeleton-card__line--short {
  width: 40%;
  height: 14px;
}

.pz-skeleton-card__line--half {
  width: 60%;
}

.pz-skeleton-card__line--button {
  width: 100px;
  height: 32px;
}

.pz-skeleton-card__footer {
  margin-top: auto;
  padding-top: var(--pz-space-3);
}

@keyframes pz-skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .pz-skeleton-card__media,
  .pz-skeleton-card__line {
    animation: none;
    background: rgba(10, 10, 15, 0.06);
  }
}
</style>
