<template>
  <div class="vendor-product-card" :class="`vendor-product-card--${cardType}`">
    <div class="vpc-image">
      <img :src="product.primary_image_url || placeholderImage" :alt="product.name">
      <div v-if="!product.images?.length" class="vpc-image__badge vpc-image__badge--missing">
        📸 No photo
      </div>
    </div>

    <div class="vpc-body">
      <div class="vpc-header">
        <h4 class="vpc-name">{{ product.name }}</h4>
        <Badge :variant="inventoryBadgeVariant(product.inventory_signal)">
          {{ formatInventorySignal(product.inventory_signal) }}
        </Badge>
      </div>

      <div class="vpc-meta">
        <span>{{ product.category_name || product.category?.name || 'Uncategorized' }}</span>
        <span v-if="product.brand">• {{ product.brand }}</span>
        <span>• {{ configStore.formatPrice(product.base_price, product.effective_currency || product.currency, displayCurrency) }}</span>
      </div>

      <!-- Readiness Mini-Bar -->
      <div class="vpc-readiness">
        <div class="vpc-readiness__bar">
          <div class="vpc-readiness__fill" :style="{ width: `${readiness}%` }" :class="`vpc-readiness__fill--${readinessColor}`"></div>
        </div>
        <span class="vpc-readiness__label">{{ readinessLabel }}</span>
      </div>

      <!-- Stock-out Prediction -->
      <div v-if="product.inventory_signal === 'LOW_STOCK' && product.days_until_stockout != null" class="vpc-stock-prediction">
        <span class="vpc-stock-prediction__icon">⏱️</span>
        <span class="vpc-stock-prediction__text">
          At current quote volume, you'll run out in ~{{ product.days_until_stockout }} days
        </span>
      </div>

      <!-- Status Flags -->
      <div class="vpc-flags">
        <span v-if="product.is_featured" class="vpc-flag vpc-flag--featured">Featured</span>
        <span v-if="product.is_new_arrival" class="vpc-flag vpc-flag--new">New</span>
        <span v-if="product.is_on_sale" class="vpc-flag vpc-flag--sale">On Sale</span>
        <span v-if="!product.certification_entries?.length" class="vpc-flag vpc-flag--warn">No certs</span>
        <span v-if="!product.description" class="vpc-flag vpc-flag--warn">No description</span>
      </div>
    </div>

    <div class="vpc-actions">
      <Button
        size="sm"
        :variant="primaryAction.variant"
        @click="primaryAction.handler"
      >
        {{ primaryAction.label }}
      </Button>
      <Button size="sm" variant="ghost" @click="$emit('edit', product)">
        Edit
      </Button>
      <Button size="sm" variant="ghost" @click="$emit('context', product)">⋯</Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Badge from '../ui/Badge.vue';
import Button from '../ui/Button.vue';

const props = defineProps({
  product: { type: Object, required: true },
  placeholderImage: { type: String, default: '/placeholder.png' },
  displayCurrency: { type: String, default: '' },
});

const emit = defineEmits(['edit', 'delete', 'adjust', 'history', 'duplicate', 'toggle-status', 'context']);



const configStore = {
  formatPrice(price, currency, targetCurrency) {
    const c = targetCurrency || currency || 'KES';
    const p = parseFloat(price || 0).toFixed(2);
    return `${c} ${p}`;
  },
};

function inventoryBadgeVariant(signal) {
  if (signal === 'LOW_STOCK') return 'warning';
  if (signal === 'OUT_OF_STOCK') return 'danger';
  return 'success';
}

function formatInventorySignal(signal) {
  if (!signal) return 'In Stock';
  return signal.replaceAll('_', ' ');
}

// ─── Card Type ───
const cardType = computed(() => {
  const p = props.product;
  if (p.status === 'DRAFT') return 'draft';
  if (p.status === 'DISABLED') return 'disabled';
  if (p.inventory_signal === 'OUT_OF_STOCK') return 'out-of-stock';
  if (p.inventory_signal === 'LOW_STOCK') return 'low-stock';
  if (!p.images?.length || !p.description) return 'incomplete';
  return 'healthy';
});

// ─── Readiness Score ───
const readiness = computed(() => {
  const p = props.product;
  let s = 0;
  if (p.name) s += 15;
  if (p.category) s += 10;
  if (p.base_price > 0) s += 15;
  if (p.description) s += 15;
  if (p.images?.length >= 3) s += 25;
  else if (p.images?.length > 0) s += 10;
  if (p.certification_entries?.length) s += 15;
  else if (p.certifications) s += 10;
  if (p.attribute_entries?.length) s += 5;
  return Math.min(s, 100);
});

const readinessColor = computed(() => {
  const r = readiness.value;
  if (r >= 80) return 'good';
  if (r >= 50) return 'warn';
  return 'bad';
});

const readinessLabel = computed(() => {
  const r = readiness.value;
  if (r >= 80) return 'Complete';
  if (r >= 50) return 'Needs polish';
  return 'Incomplete';
});

// ─── Primary Action ───
const primaryAction = computed(() => {
  const p = props.product;

  if (p.inventory_signal === 'LOW_STOCK') {
    return { label: 'Restock', variant: 'warning', handler: () => emit('adjust', p) };
  }
  if (p.inventory_signal === 'OUT_OF_STOCK') {
    return { label: 'Restock', variant: 'danger', handler: () => emit('adjust', p) };
  }
  if (p.status === 'DRAFT') {
    return { label: 'Publish', variant: 'primary', handler: () => emit('edit', p) };
  }
  if (!p.images?.length) {
    return { label: 'Add Photos', variant: 'secondary', handler: () => emit('edit', p) };
  }
  if (!p.description) {
    return { label: 'Complete', variant: 'secondary', handler: () => emit('edit', p) };
  }
  return { label: 'Edit', variant: 'ghost', handler: () => emit('edit', p) };
});

function confirmDelete() {
  if (confirm(`Delete "${props.product.name}"? This cannot be undone.`)) {
    emit('delete', props.product);
  }
}

function toggleStatus() {
  emit('toggle-status', props.product);
}
</script>

<style scoped>
.vendor-product-card {
  display: grid;
  grid-template-columns: 5rem 1fr auto;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 12px;
  transition: all 0.2s ease;
  align-items: start;
}

.vendor-product-card:hover {
  border-color: rgba(10, 10, 15, 0.14);
  box-shadow: 0 6px 24px rgba(10, 10, 15, 0.06);
}

.vendor-product-card--draft {
  border-left: 3px solid var(--pz-color-concrete-grey);
  background: rgba(120, 120, 130, 0.02);
}

.vendor-product-card--disabled {
  border-left: 3px solid #9ca3af;
  opacity: 0.7;
}

.vendor-product-card--out-of-stock {
  border-left: 3px solid #dc2626;
  background: rgba(220, 38, 38, 0.02);
}

.vendor-product-card--low-stock {
  border-left: 3px solid #d97706;
  background: rgba(217, 119, 6, 0.02);
}

.vendor-product-card--incomplete {
  border-left: 3px solid #ea580c;
}

.vendor-product-card--healthy {
  border-left: 3px solid #16a34a;
}

/* Image */
.vpc-image {
  width: 5rem;
  height: 5rem;
  border-radius: 10px;
  overflow: hidden;
  background: #f4f4f5;
  position: relative;
  flex-shrink: 0;
}

.vpc-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.vpc-image__badge {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-size: 0.65rem;
  font-family: var(--pz-font-mono);
  text-align: center;
  padding: 0.3rem;
}

.vpc-image__badge--missing {
  background: rgba(10, 10, 15, 0.5);
  color: white;
}

/* Body */
.vpc-body {
  display: grid;
  gap: 0.35rem;
  min-width: 0;
}

.vpc-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.vpc-name {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--pz-color-foundation-black);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vpc-meta {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Readiness */
.vpc-readiness {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.2rem;
}

.vpc-readiness__bar {
  flex: 1;
  max-width: 8rem;
  height: 0.35rem;
  background: rgba(10, 10, 15, 0.06);
  border-radius: 99px;
  overflow: hidden;
}

.vpc-readiness__fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.4s ease;
}

.vpc-readiness__fill--good { background: #16a34a; }
.vpc-readiness__fill--warn { background: #d97706; }
.vpc-readiness__fill--bad  { background: #dc2626; }

.vpc-readiness__label {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

/* Stock-out Prediction */
.vpc-stock-prediction {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.6rem;
  background: rgba(217, 119, 6, 0.06);
  border: 1px solid rgba(217, 119, 6, 0.12);
  border-radius: 8px;
  font-size: 0.78rem;
  color: #92400e;
  margin-top: 0.3rem;
}

.vpc-stock-prediction__icon {
  font-size: 0.9rem;
}

/* Flags */
.vpc-flags {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.2rem;
}

.vpc-flag {
  font-size: 0.68rem;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  font-weight: 500;
}

.vpc-flag--featured { background: rgba(212, 101, 42, 0.1); color: var(--pz-color-earth-orange); }
.vpc-flag--new      { background: rgba(22, 163, 74, 0.1); color: #166534; }
.vpc-flag--sale     { background: rgba(220, 38, 38, 0.1); color: #991b1b; }
.vpc-flag--warn     { background: rgba(234, 88, 12, 0.08); color: #9a3412; }

/* Actions */
.vpc-actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.vpc-actions__more {
  position: relative;
}

.vpc-actions__menu {
  position: absolute;
  top: calc(100% + 0.3rem);
  right: 0;
  min-width: 9rem;
  background: white;
  border: 1px solid rgba(10, 10, 15, 0.1);
  border-radius: 10px;
  box-shadow: 0 12px 32px rgba(10, 10, 15, 0.1);
  z-index: 20;
  overflow: hidden;
  display: grid;
}

.vpc-actions__menu button {
  padding: 0.55rem 0.9rem;
  text-align: left;
  font-size: 0.82rem;
  background: none;
  border: none;
  color: var(--pz-color-foundation-black);
  cursor: pointer;
  transition: background 0.12s;
}

.vpc-actions__menu button:hover {
  background: rgba(10, 10, 15, 0.04);
}

.vpc-actions__danger {
  color: #dc2626 !important;
}

@media (max-width: 640px) {
  .vendor-product-card {
    grid-template-columns: 1fr;
  }
  .vpc-image {
    width: 100%;
    height: 10rem;
  }
  .vpc-actions {
    justify-content: flex-start;
  }
}
</style>
