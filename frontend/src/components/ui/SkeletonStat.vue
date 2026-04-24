<template>
  <div class="pz-skeleton-stat">
    <div class="pz-skeleton-stat__label"></div>
    <div class="pz-skeleton-stat__value"></div>
  </div>
</template>

<style scoped>
.pz-skeleton-stat {
  min-width: 120px;
  display: grid;
  gap: 0.5rem;
  padding: 0.7rem 0.85rem;
  background: rgba(10, 10, 15, 0.04);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-skeleton-stat__label {
  height: 8px;
  width: 50%;
  background: linear-gradient(90deg, rgba(10,10,15,0.04) 25%, rgba(10,10,15,0.08) 50%, rgba(10,10,15,0.04) 75%);
  background-size: 200% 100%;
  animation: pz-skeleton-shimmer 1.5s infinite;
  border-radius: 2px;
}

.pz-skeleton-stat__value {
  height: 16px;
  width: 30%;
  background: linear-gradient(90deg, rgba(10,10,15,0.04) 25%, rgba(10,10,15,0.08) 50%, rgba(10,10,15,0.04) 75%);
  background-size: 200% 100%;
  animation: pz-skeleton-shimmer 1.5s infinite;
  border-radius: 2px;
}

@keyframes pz-skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .pz-skeleton-stat__label,
  .pz-skeleton-stat__value {
    animation: none;
    background: rgba(10, 10, 15, 0.06);
  }
}
</style>
