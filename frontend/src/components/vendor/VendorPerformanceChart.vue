<template>
  <div class="vendor-performance-chart">
    <div class="vpc-chart__header">
      <h4 class="vpc-chart__title">📊 30-Day Activity</h4>
      <div class="vpc-chart__legend">
        <span class="vpc-legend__item"><span class="vpc-legend__dot vpc-legend__dot--views"></span> Views</span>
        <span class="vpc-legend__item"><span class="vpc-legend__dot vpc-legend__dot--quotes"></span> Quotes</span>
      </div>
    </div>
    <div v-if="!data?.length" class="vpc-chart__empty">No activity data yet.</div>
    <div v-else class="vpc-chart__canvas">
      <svg :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="none" class="vpc-chart__svg">
        <!-- Grid lines -->
        <line v-for="n in 5" :key="`grid-${n}`"
          x1="0" :y1="(height / 5) * n" :x2="width" :y2="(height / 5) * n"
          stroke="rgba(10,10,15,0.06)" stroke-width="1"
        />
        <!-- Views area -->
        <path :d="viewsAreaPath" fill="rgba(37, 99, 235, 0.08)" />
        <path :d="viewsLinePath" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        <!-- Quotes line -->
        <path :d="quotesLinePath" fill="none" stroke="#d4652a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        <!-- Data points -->
        <circle v-for="(d, i) in data" :key="`v-${i}`"
          :cx="xScale(i)" :cy="yScale(d.views)" r="3" fill="#2563eb"
        />
        <circle v-for="(d, i) in data" :key="`q-${i}`"
          :cx="xScale(i)" :cy="yScale(d.quotes)" r="3" fill="#d4652a"
        />
      </svg>
      <!-- Hover tooltip -->
      <div v-if="hoverIndex !== null" class="vpc-chart__tooltip" :style="tooltipStyle">
        <div class="vpc-tooltip__date">{{ data[hoverIndex].date }}</div>
        <div class="vpc-tooltip__row"><span class="vpc-tooltip__dot vpc-tooltip__dot--views"></span> Views: {{ data[hoverIndex].views }}</div>
        <div class="vpc-tooltip__row"><span class="vpc-tooltip__dot vpc-tooltip__dot--quotes"></span> Quotes: {{ data[hoverIndex].quotes }}</div>
      </div>
      <!-- Hover overlay for interaction -->
      <div class="vpc-chart__overlay">
        <div
          v-for="(d, i) in data"
          :key="`hover-${i}`"
          class="vpc-chart__hover-col"
          @mouseenter="hoverIndex = i"
          @mouseleave="hoverIndex = null"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  data: { type: Array, default: () => [] },
});

const width = 600;
const height = 180;
const padding = { top: 10, bottom: 10 };
const hoverIndex = ref(null);

const maxValue = computed(() => {
  if (!props.data.length) return 1;
  const max = Math.max(...props.data.map((d) => Math.max(d.views || 0, d.quotes || 0)));
  return max > 0 ? max : 1;
});

function xScale(i) {
  if (props.data.length <= 1) return width / 2;
  return (i / (props.data.length - 1)) * width;
}

function yScale(val) {
  const chartHeight = height - padding.top - padding.bottom;
  const ratio = (val || 0) / maxValue.value;
  return height - padding.bottom - ratio * chartHeight;
}

function pathPoints(key) {
  return props.data.map((d, i) => `${xScale(i)},${yScale(d[key])}`).join(' ');
}

const viewsLinePath = computed(() => {
  const pts = pathPoints('views');
  return pts ? `M ${pts}` : '';
});

const quotesLinePath = computed(() => {
  const pts = pathPoints('quotes');
  return pts ? `M ${pts}` : '';
});

const viewsAreaPath = computed(() => {
  if (!props.data.length) return '';
  const pts = pathPoints('views');
  const firstX = xScale(0);
  const lastX = xScale(props.data.length - 1);
  const bottomY = height - padding.bottom;
  return `M ${firstX},${bottomY} L ${pts} L ${lastX},${bottomY} Z`;
});

const tooltipStyle = computed(() => {
  if (hoverIndex.value === null) return {};
  const x = xScale(hoverIndex.value);
  const leftPct = (x / width) * 100;
  return {
    left: `${Math.min(Math.max(leftPct, 10), 90)}%`,
    transform: 'translateX(-50%)',
  };
});
</script>

<style scoped>
.vendor-performance-chart {
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(10, 10, 15, 0.04);
}

.vpc-chart__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.vpc-chart__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 600;
}

.vpc-chart__legend {
  display: flex;
  gap: 0.75rem;
  font-size: 0.78rem;
}

.vpc-legend__item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.vpc-legend__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.vpc-legend__dot--views { background: #2563eb; }
.vpc-legend__dot--quotes { background: #d4652a; }

.vpc-chart__empty {
  text-align: center;
  padding: 2rem;
  color: var(--pz-color-concrete-grey);
  font-size: 0.9rem;
}

.vpc-chart__canvas {
  position: relative;
  height: 180px;
}

.vpc-chart__svg {
  width: 100%;
  height: 100%;
  display: block;
}

.vpc-chart__overlay {
  position: absolute;
  inset: 0;
  display: flex;
}

.vpc-chart__hover-col {
  flex: 1;
  cursor: crosshair;
}

.vpc-chart__tooltip {
  position: absolute;
  bottom: 100%;
  margin-bottom: 0.5rem;
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.1);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  box-shadow: 0 4px 12px rgba(10, 10, 15, 0.1);
  font-size: 0.78rem;
  pointer-events: none;
  white-space: nowrap;
  z-index: 10;
}

.vpc-tooltip__date {
  font-weight: 600;
  margin-bottom: 0.2rem;
  color: var(--pz-color-foundation-black);
}

.vpc-tooltip__row {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--pz-color-text-secondary);
}

.vpc-tooltip__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.vpc-tooltip__dot--views { background: #2563eb; }
.vpc-tooltip__dot--quotes { background: #d4652a; }
</style>
