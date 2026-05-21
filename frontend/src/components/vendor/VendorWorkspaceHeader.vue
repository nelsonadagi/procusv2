<template>
  <div class="vendor-workspace-header">
    <!-- Priority Strip -->
    <div v-if="urgentItems.length" class="pz-priority-strip">
      <div class="pz-priority-strip__label">
        <span class="pz-priority-strip__dot" aria-hidden="true"></span>
        {{ urgentItems.length }} urgent action{{ urgentItems.length === 1 ? '' : 's' }}
      </div>
      <div class="pz-priority-strip__items">
        <button
          v-for="item in urgentItems.slice(0, 3)"
          :key="item.id"
          type="button"
          class="pz-priority-strip__item"
          @click="item.action"
        >
          <span class="pz-priority-strip__icon">{{ item.icon }}</span>
          <span class="pz-priority-strip__text">{{ item.label }}</span>
        </button>
      </div>
    </div>

    <!-- Health Score + Stats -->
    <div class="pz-health-bar">
      <div class="pz-health-score">
        <div class="pz-health-score__ring" :style="ringStyle" @click="showBreakdown = !showBreakdown">
          <div class="pz-health-score__value">{{ healthScore }}</div>
          <div class="pz-health-score__label">{{ healthLabel }}</div>
        </div>
        <div class="pz-health-score__factors">
          <div class="pz-health-factor" :class="`pz-health-factor--${listingHealth >= 70 ? 'good' : listingHealth >= 40 ? 'warn' : 'bad'}`">
            <span>Listings</span>
            <strong>{{ listingHealth }}%</strong>
          </div>
          <div class="pz-health-factor" :class="`pz-health-factor--${stockHealth >= 70 ? 'good' : stockHealth >= 40 ? 'warn' : 'bad'}`">
            <span>Stock</span>
            <strong>{{ stockHealth }}%</strong>
          </div>
          <div class="pz-health-factor" :class="`pz-health-factor--${certHealth >= 70 ? 'good' : certHealth >= 40 ? 'warn' : 'bad'}`">
            <span>Certs</span>
            <strong>{{ certHealth }}%</strong>
          </div>
          <div class="pz-health-factor" :class="`pz-health-factor--${responseHealth >= 70 ? 'good' : responseHealth >= 40 ? 'warn' : 'bad'}`">
            <span>Response</span>
            <strong>{{ responseHealth }}%</strong>
          </div>
          <div class="pz-health-factor" :class="`pz-health-factor--${freshnessHealth >= 70 ? 'good' : freshnessHealth >= 40 ? 'warn' : 'bad'}`">
            <span>Fresh</span>
            <strong>{{ freshnessHealth }}%</strong>
          </div>
          <button class="pz-health-score__toggle" @click="showBreakdown = !showBreakdown">
            {{ showBreakdown ? 'Hide details' : 'View details' }}
          </button>
        </div>
      </div>

      <!-- Expandable Health Breakdown -->
      <Transition name="pz-breakdown">
        <div v-if="showBreakdown" class="pz-health-breakdown">
          <div class="pz-breakdown-grid">
            <div class="pz-breakdown-card">
              <div class="pz-breakdown-card__header">
                <span class="pz-breakdown-card__icon">📋</span>
                <span class="pz-breakdown-card__title">Listing Completeness</span>
                <Badge size="xs" :variant="listingHealth >= 70 ? 'success' : listingHealth >= 40 ? 'warning' : 'danger'">{{ listingHealth }}%</Badge>
              </div>
              <div class="pz-breakdown-card__body">
                <div class="pz-breakdown-row">
                  <span>With photos</span>
                  <strong>{{ productsWithImages }} / {{ activeProducts.length }}</strong>
                </div>
                <div class="pz-breakdown-row">
                  <span>With description</span>
                  <strong>{{ productsWithDesc }} / {{ activeProducts.length }}</strong>
                </div>
                <div class="pz-breakdown-row">
                  <span>With specs</span>
                  <strong>{{ productsWithSpecs }} / {{ activeProducts.length }}</strong>
                </div>
              </div>
            </div>

            <div class="pz-breakdown-card">
              <div class="pz-breakdown-card__header">
                <span class="pz-breakdown-card__icon">📦</span>
                <span class="pz-breakdown-card__title">Stock Health</span>
                <Badge size="xs" :variant="stockHealth >= 70 ? 'success' : stockHealth >= 40 ? 'warning' : 'danger'">{{ stockHealth }}%</Badge>
              </div>
              <div class="pz-breakdown-card__body">
                <div class="pz-breakdown-row pz-breakdown-row--good">
                  <span>Healthy</span>
                  <strong>{{ healthyStockCount }}</strong>
                </div>
                <div class="pz-breakdown-row pz-breakdown-row--warn">
                  <span>Low stock</span>
                  <strong>{{ lowStockCount }}</strong>
                </div>
                <div class="pz-breakdown-row pz-breakdown-row--bad">
                  <span>Out of stock</span>
                  <strong>{{ outOfStockCount }}</strong>
                </div>
              </div>
            </div>

            <div class="pz-breakdown-card">
              <div class="pz-breakdown-card__header">
                <span class="pz-breakdown-card__icon">🏅</span>
                <span class="pz-breakdown-card__title">Certifications</span>
                <Badge size="xs" :variant="certHealth >= 70 ? 'success' : certHealth >= 40 ? 'warning' : 'danger'">{{ certHealth }}%</Badge>
              </div>
              <div class="pz-breakdown-card__body">
                <div class="pz-breakdown-row pz-breakdown-row--good">
                  <span>Certified products</span>
                  <strong>{{ productsWithCerts }}</strong>
                </div>
                <div class="pz-breakdown-row pz-breakdown-row--warn">
                  <span>Missing certs</span>
                  <strong>{{ activeProducts.length - productsWithCerts }}</strong>
                </div>
              </div>
            </div>

            <div class="pz-breakdown-card">
              <div class="pz-breakdown-card__header">
                <span class="pz-breakdown-card__icon">⏱️</span>
                <span class="pz-breakdown-card__title">Response Time</span>
                <Badge size="xs" :variant="responseHealth >= 70 ? 'success' : responseHealth >= 40 ? 'warning' : 'danger'">{{ responseHealth }}%</Badge>
              </div>
              <div class="pz-breakdown-card__body">
                <div class="pz-breakdown-row">
                  <span>Avg response time</span>
                  <strong>{{ avgResponseTimeHours != null ? `${avgResponseTimeHours}h` : 'No data' }}</strong>
                </div>
                <div class="pz-breakdown-row pz-breakdown-row--good">
                  <span>Target</span>
                  <strong>&lt; 4h</strong>
                </div>
              </div>
            </div>

            <div class="pz-breakdown-card">
              <div class="pz-breakdown-card__header">
                <span class="pz-breakdown-card__icon">🔄</span>
                <span class="pz-breakdown-card__title">Freshness</span>
                <Badge size="xs" :variant="freshnessHealth >= 70 ? 'success' : freshnessHealth >= 40 ? 'warning' : 'danger'">{{ freshnessHealth }}%</Badge>
              </div>
              <div class="pz-breakdown-card__body">
                <div class="pz-breakdown-row">
                  <span>Avg days since update</span>
                  <strong>{{ freshnessDays }}d</strong>
                </div>
                <div class="pz-breakdown-row pz-breakdown-row--good">
                  <span>Target</span>
                  <strong>&lt; 7d</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Performance Metrics Strip -->
      <div v-if="performanceMetrics" class="pz-metrics-strip">
        <div class="pz-metric">
          <div class="pz-metric__value">{{ performanceMetrics.activeProducts }}</div>
          <div class="pz-metric__label">Active Products</div>
        </div>
        <div class="pz-metric">
          <div class="pz-metric__value">{{ performanceMetrics.viewsThisWeek }}</div>
          <div class="pz-metric__label">Views This Week</div>
        </div>
        <div class="pz-metric">
          <div class="pz-metric__value">{{ performanceMetrics.quotesThisMonth }}</div>
          <div class="pz-metric__label">Quotes This Month</div>
        </div>
        <div class="pz-metric">
          <div class="pz-metric__value">{{ performanceMetrics.conversionRate }}%</div>
          <div class="pz-metric__label">Conversion Rate</div>
        </div>
      </div>

      <!-- Waiting on You vs Waiting on Others -->
      <div class="pz-waiting-grid">
        <div class="pz-waiting-col">
          <div class="pz-waiting-col__header">
            <span class="pz-waiting-col__dot pz-waiting-col__dot--you"></span>
            <span class="pz-waiting-col__title">Waiting on You</span>
          </div>
          <div v-if="waitingOnYou.length" class="pz-waiting-col__list">
            <div v-for="rec in waitingOnYou.slice(0, 3)" :key="rec.id" class="pz-health-action" @click="rec.action">
              <span class="pz-health-action__icon">{{ rec.icon }}</span>
              <div class="pz-health-action__body">
                <div class="pz-health-action__title">{{ rec.title }}</div>
                <div class="pz-health-action__meta">{{ rec.meta }}</div>
              </div>
              <span class="pz-health-action__cta">{{ rec.cta }}</span>
            </div>
          </div>
          <div v-else class="pz-waiting-col__empty">You're all caught up 🎉</div>
        </div>

        <div class="pz-waiting-col">
          <div class="pz-waiting-col__header">
            <span class="pz-waiting-col__dot pz-waiting-col__dot--others"></span>
            <span class="pz-waiting-col__title">Waiting on Others</span>
          </div>
          <div v-if="waitingOnOthers.length" class="pz-waiting-col__list">
            <div v-for="item in waitingOnOthers.slice(0, 2)" :key="item.id" class="pz-health-action pz-health-action--blocked">
              <span class="pz-health-action__icon">{{ item.icon }}</span>
              <div class="pz-health-action__body">
                <div class="pz-health-action__title">{{ item.title }}</div>
                <div class="pz-health-action__meta">{{ item.meta }}</div>
              </div>
            </div>
          </div>
          <div v-else class="pz-waiting-col__empty">Nothing blocked externally</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import Badge from '../ui/Badge.vue';

const props = defineProps({
  products: { type: Array, default: () => [] },
  unrespondedQuotes: { type: Number, default: 0 },
  backendRecommendations: { type: Array, default: () => [] },
  avgResponseTimeHours: { type: Number, default: null },
  vendorStatus: { type: String, default: '' },
  performanceMetrics: {
    type: Object,
    default: () => ({
      activeProducts: 0,
      viewsThisWeek: 0,
      quotesThisMonth: 0,
      conversionRate: 0,
    }),
  },
});

const emit = defineEmits(['restock', 'edit', 'respond-quote', 'add-photos', 'add-certs']);

const showBreakdown = ref(false);

// ─── Health Score Computation ───

const activeProducts = computed(() => props.products.filter((p) => p.status === 'ACTIVE'));

const listingHealth = computed(() => {
  if (!activeProducts.value.length) return 0;
  const scored = activeProducts.value.map((p) => {
    let s = 0;
    if (p.name) s += 15;
    if (p.category) s += 10;
    if (p.base_price > 0) s += 15;
    if (p.description) s += 15;
    if (p.images?.length >= 3) s += 25;
    else if (p.images?.length > 0) s += 10;
    if (p.certification_entries?.length) s += 15;
    if (p.attribute_entries?.length) s += 5;
    return Math.min(s, 100);
  });
  return Math.round(scored.reduce((a, b) => a + b, 0) / scored.length);
});

const stockHealth = computed(() => {
  if (!activeProducts.value.length) return 0;
  const healthy = activeProducts.value.filter((p) => p.inventory_signal !== 'OUT_OF_STOCK' && p.inventory_signal !== 'LOW_STOCK').length;
  return Math.round((healthy / activeProducts.value.length) * 100);
});

const certHealth = computed(() => {
  if (!activeProducts.value.length) return 0;
  const withCerts = activeProducts.value.filter((p) => p.certification_entries?.length > 0).length;
  return Math.round((withCerts / activeProducts.value.length) * 100);
});

// Breakdown detail counts
const productsWithImages = computed(() => activeProducts.value.filter((p) => p.images?.length > 0).length);
const productsWithDesc = computed(() => activeProducts.value.filter((p) => p.description?.length > 10).length);
const productsWithSpecs = computed(() => activeProducts.value.filter((p) => p.attribute_entries?.length > 0).length);
const healthyStockCount = computed(() => activeProducts.value.filter((p) => p.inventory_signal !== 'OUT_OF_STOCK' && p.inventory_signal !== 'LOW_STOCK').length);
const lowStockCount = computed(() => activeProducts.value.filter((p) => p.inventory_signal === 'LOW_STOCK').length);
const outOfStockCount = computed(() => activeProducts.value.filter((p) => p.inventory_signal === 'OUT_OF_STOCK').length);
const productsWithCerts = computed(() => activeProducts.value.filter((p) => p.certification_entries?.length > 0).length);

const responseHealth = computed(() => {
  const avg = props.avgResponseTimeHours;
  if (avg === null) return 100; // no data yet = perfect
  if (avg <= 2) return 100;
  if (avg <= 4) return 80;
  if (avg <= 8) return 60;
  if (avg <= 24) return 40;
  return 20;
});

const freshnessHealth = computed(() => {
  if (!activeProducts.value.length) return 0;
  const now = Date.now();
  const daysSinceUpdate = activeProducts.value.map((p) => {
    const updated = new Date(p.updated_at || p.created_at).getTime();
    return (now - updated) / 86400000;
  });
  const avgDays = daysSinceUpdate.reduce((a, b) => a + b, 0) / daysSinceUpdate.length;
  if (avgDays <= 7) return 100;
  if (avgDays <= 14) return 80;
  if (avgDays <= 30) return 60;
  if (avgDays <= 60) return 40;
  return 20;
});

const healthScore = computed(() => {
  const raw = (listingHealth.value * 0.25) + (stockHealth.value * 0.25) + (responseHealth.value * 0.20) + (certHealth.value * 0.15) + (freshnessHealth.value * 0.15);
  return Math.round(raw);
});

const healthLabel = computed(() => {
  const s = healthScore.value;
  if (s >= 90) return 'Excellent';
  if (s >= 70) return 'Good';
  if (s >= 50) return 'Fair';
  if (s >= 30) return 'Needs Work';
  return 'At Risk';
});

const ringStyle = computed(() => {
  const s = healthScore.value;
  let color = '#dc2626';
  if (s >= 90) color = '#16a34a';
  else if (s >= 70) color = '#65a30d';
  else if (s >= 50) color = '#d97706';
  else if (s >= 30) color = '#ea580c';
  return {
    background: `conic-gradient(${color} ${s * 3.6}deg, rgba(10,10,15,0.06) 0deg)`,
  };
});

// ─── Priority Strip ───

const urgentItems = computed(() => {
  const items = [];

  const lowStock = props.products.filter((p) => p.inventory_signal === 'LOW_STOCK');
  lowStock.forEach((p) => {
    items.push({
      id: `restock-${p.id}`,
      icon: '🔴',
      label: `${p.name} — ${p.stock_quantity} left`,
      action: () => emit('restock', p),
    });
  });

  const outOfStock = props.products.filter((p) => p.inventory_signal === 'OUT_OF_STOCK' && p.status === 'ACTIVE');
  outOfStock.forEach((p) => {
    items.push({
      id: `oos-${p.id}`,
      icon: '🚫',
      label: `${p.name} — out of stock`,
      action: () => emit('restock', p),
    });
  });

  if (props.unrespondedQuotes > 0) {
    items.push({
      id: 'quotes',
      icon: '💬',
      label: `${props.unrespondedQuotes} unresponded quote${props.unrespondedQuotes === 1 ? '' : 's'}`,
      action: () => emit('respond-quote'),
    });
  }

  return items;
});

// ─── Recommendations ───

const iconMap = {
  RESTOCK: '🔴',
  INCOMPLETE_LISTING: '📸',
  RESPOND_QUOTE: '💬',
  PUBLISH: '🚀',
  COMPLIANCE: '📋',
  PRICE: '💰',
};

const waitingOnYou = computed(() => recommendations.value.filter((r) => !r.blocked));

const waitingOnOthers = computed(() => {
  const items = [];
  if (props.vendorStatus === 'PENDING') {
    items.push({
      id: 'admin-approval',
      icon: '⏳',
      title: 'Admin approval pending',
      meta: 'Your vendor profile is under review. Typical time: 1–2 business days.',
      blocked: true,
    });
  }
  return items;
});

const recommendations = computed(() => {
  // Prefer backend-driven recommendations when available
  if (props.backendRecommendations.length) {
    return props.backendRecommendations.slice(0, 5).map((r) => ({
      id: r.id,
      icon: iconMap[r.type] || '🔔',
      title: r.title,
      meta: r.message,
      cta: r.cta,
      action: () => {
        if (r.cta_url) window.location.href = r.cta_url;
        else if (r.type === 'RESTOCK' && r.product_uuid) emit('restock', { uuid: r.product_uuid });
        else if (r.type === 'RESPOND_QUOTE') emit('respond-quote');
        else if (r.type === 'COMPLIANCE') emit('add-certs');
      },
    }));
  }

  // Fallback to local heuristics
  const recs = [];

  const noImages = activeProducts.value.filter((p) => !p.images?.length);
  if (noImages.length) {
    recs.push({
      id: 'photos',
      icon: '📸',
      title: `Add photos to ${noImages.length} product${noImages.length === 1 ? '' : 's'}`,
      meta: 'Products with images get 5× more views',
      cta: 'Fix',
      action: () => emit('edit', noImages[0]),
    });
  }

  const noDesc = activeProducts.value.filter((p) => !p.description);
  if (noDesc.length && !noImages.length) {
    recs.push({
      id: 'desc',
      icon: '📝',
      title: `Add descriptions to ${noDesc.length} product${noDesc.length === 1 ? '' : 's'}`,
      meta: 'Buyers need details to request quotes',
      cta: 'Fix',
      action: () => emit('edit', noDesc[0]),
    });
  }

  const noCerts = activeProducts.value.filter((p) => !p.certification_entries?.length);
  if (noCerts.length && !noImages.length && !noDesc.length) {
    recs.push({
      id: 'certs',
      icon: '📋',
      title: `Add certifications to ${noCerts.length} product${noCerts.length === 1 ? '' : 's'}`,
      meta: 'Enterprise buyers filter by compliance',
      cta: 'Fix',
      action: () => emit('add-certs'),
    });
  }

  return recs;
});

const freshnessDays = computed(() => {
  if (!activeProducts.value.length) return 0;
  const now = Date.now();
  const days = activeProducts.value.map((p) => {
    const updated = new Date(p.updated_at || p.created_at).getTime();
    return (now - updated) / 86400000;
  });
  return Math.round(days.reduce((a, b) => a + b, 0) / days.length);
});
</script>

<style scoped>
.vendor-workspace-header {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

/* Priority Strip */
.pz-priority-strip {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.6rem 1rem;
  background: linear-gradient(90deg, rgba(220, 38, 38, 0.06), rgba(220, 38, 38, 0.02));
  border: 1px solid rgba(220, 38, 38, 0.12);
  border-radius: 12px;
  overflow-x: auto;
}

.pz-priority-strip__label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #dc2626;
  white-space: nowrap;
  flex-shrink: 0;
}

.pz-priority-strip__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: #dc2626;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.pz-priority-strip__items {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pz-priority-strip__item {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.7rem;
  background: white;
  border: 1px solid rgba(220, 38, 38, 0.15);
  border-radius: 8px;
  font-size: 0.82rem;
  color: var(--pz-color-foundation-black);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.pz-priority-strip__item:hover {
  background: rgba(220, 38, 38, 0.04);
  border-color: rgba(220, 38, 38, 0.25);
}

/* Health Bar */
.pz-health-bar {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.5rem;
  padding: 1.25rem;
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  box-shadow: 0 4px 20px rgba(10, 10, 15, 0.04);
}

.pz-health-score {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.pz-health-score__ring {
  width: 5.5rem;
  height: 5.5rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  position: relative;
  flex-shrink: 0;
}

.pz-health-score__ring::before {
  content: '';
  position: absolute;
  inset: 0.4rem;
  border-radius: 50%;
  background: white;
}

.pz-health-score__value {
  position: relative;
  font-family: var(--pz-font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  line-height: 1;
}

.pz-health-score__label {
  position: relative;
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-health-score__factors {
  display: grid;
  gap: 0.4rem;
}

.pz-health-factor {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.78rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  min-width: 7rem;
}

.pz-health-factor--good { background: rgba(22, 163, 74, 0.08); color: #166534; }
.pz-health-factor--warn { background: rgba(217, 119, 6, 0.08); color: #92400e; }
.pz-health-factor--bad  { background: rgba(220, 38, 38, 0.08); color: #991b1b; }

.pz-health-factor strong {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
}

/* Recommendations */
.pz-health-actions {
  display: grid;
  gap: 0.5rem;
  align-content: center;
}

.pz-health-action {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.9rem;
  background: rgba(247, 244, 239, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.pz-health-action:hover {
  background: rgba(247, 244, 239, 0.9);
  border-color: rgba(10, 10, 15, 0.1);
}

.pz-health-action__icon {
  font-size: 1.1rem;
}

.pz-health-action__title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
  line-height: 1.3;
}

.pz-health-action__meta {
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
}

.pz-health-action__cta {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
  white-space: nowrap;
}

/* Expandable Breakdown */
.pz-health-score__toggle {
  background: none;
  border: none;
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  cursor: pointer;
  padding: 0.2rem 0;
  text-align: left;
  text-decoration: underline;
}

.pz-health-breakdown {
  grid-column: 1 / -1;
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-breakdown-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.pz-breakdown-card {
  background: rgba(247, 244, 239, 0.4);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 10px;
  padding: 0.9rem;
}

.pz-breakdown-card__header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.6rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.pz-breakdown-card__icon {
  font-size: 1rem;
}

.pz-breakdown-card__title {
  flex: 1;
}

.pz-breakdown-card__body {
  display: grid;
  gap: 0.35rem;
}

.pz-breakdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.78rem;
  padding: 0.25rem 0;
  border-bottom: 1px solid rgba(10, 10, 15, 0.04);
}

.pz-breakdown-row:last-child {
  border-bottom: none;
}

.pz-breakdown-row strong {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
}

.pz-breakdown-row--good strong { color: #166534; }
.pz-breakdown-row--warn strong { color: #92400e; }
.pz-breakdown-row--bad strong { color: #991b1b; }

/* Performance Metrics Strip */
.pz-metrics-strip {
  display: flex;
  gap: 1.5rem;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 10px;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.pz-metric {
  text-align: center;
  min-width: 80px;
}

.pz-metric__value {
  font-family: var(--pz-font-mono);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-metric__label {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.15rem;
}

/* Waiting on You / Waiting on Others */
.pz-waiting-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 0.75rem;
}

.pz-waiting-col {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 12px;
  padding: 0.75rem;
}

.pz-waiting-col__header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.6rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.pz-waiting-col__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

.pz-waiting-col__dot--you { background: #16a34a; }
.pz-waiting-col__dot--others { background: #d97706; }

.pz-waiting-col__list {
  display: grid;
  gap: 0.4rem;
}

.pz-waiting-col__empty {
  font-size: 0.82rem;
  color: var(--pz-color-concrete-grey);
  text-align: center;
  padding: 1rem 0;
}

.pz-health-action--blocked {
  opacity: 0.7;
  cursor: default;
}

.pz-health-action--blocked:hover {
  background: rgba(247, 244, 239, 0.6);
  border-color: rgba(10, 10, 15, 0.06);
}

/* Transition */
.pz-breakdown-enter-active,
.pz-breakdown-leave-active {
  transition: all 0.25s ease;
  max-height: 400px;
  opacity: 1;
  overflow: hidden;
}

.pz-breakdown-enter-from,
.pz-breakdown-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  margin-top: 0;
}

@media (max-width: 800px) {
  .pz-health-bar {
    grid-template-columns: 1fr;
  }
  .pz-priority-strip {
    flex-direction: column;
    align-items: flex-start;
  }
  .pz-breakdown-grid {
    grid-template-columns: 1fr;
  }
}
</style>
