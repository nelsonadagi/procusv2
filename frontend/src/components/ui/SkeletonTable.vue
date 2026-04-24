<template>
  <div class="pz-skeleton-table">
    <div class="pz-skeleton-table__head">
      <div
        v-for="n in columns"
        :key="n"
        class="pz-skeleton-table__cell pz-skeleton-table__cell--head"
      ></div>
    </div>
    <div
      v-for="row in rows"
      :key="row"
      class="pz-skeleton-table__row"
    >
      <div
        v-for="n in columns"
        :key="n"
        class="pz-skeleton-table__cell"
      ></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  columns: { type: Number, default: 5 },
  rows: { type: Number, default: 4 }
});
</script>

<style scoped>
.pz-skeleton-table {
  width: 100%;
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-skeleton-table__head {
  display: grid;
  grid-template-columns: repeat(v-bind(columns), 1fr);
  gap: var(--pz-space-4);
  padding: var(--pz-space-3) var(--pz-space-4);
  background: rgba(10, 10, 15, 0.03);
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-skeleton-table__row {
  display: grid;
  grid-template-columns: repeat(v-bind(columns), 1fr);
  gap: var(--pz-space-4);
  padding: var(--pz-space-3) var(--pz-space-4);
  border-bottom: 1px solid rgba(10, 10, 15, 0.04);
}

.pz-skeleton-table__cell {
  height: 12px;
  background: linear-gradient(90deg, rgba(10,10,15,0.04) 25%, rgba(10,10,15,0.08) 50%, rgba(10,10,15,0.04) 75%);
  background-size: 200% 100%;
  animation: pz-skeleton-shimmer 1.5s infinite;
  border-radius: 2px;
}

.pz-skeleton-table__cell--head {
  height: 10px;
  width: 60%;
}

@keyframes pz-skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .pz-skeleton-table__cell {
    animation: none;
    background: rgba(10, 10, 15, 0.06);
  }
}
</style>
