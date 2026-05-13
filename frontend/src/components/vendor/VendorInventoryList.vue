<template>
  <div class="pz-inventory-list">
    <div class="pz-inventory-list__desktop">
      <PzDataTable :columns="columns" :data="products">
        <template #cell-material="{ row }">
          <div class="pz-inventory-list__material">
            <img
              class="pz-inventory-list__thumb"
              :src="row.primary_image_url || placeholderImage"
              :alt="row.name"
            >
            <div class="pz-inventory-list__material-copy">
              <div class="pz-inventory-list__name">{{ row.name }}</div>
              <div class="pz-inventory-list__category">
                {{ row.category_name || row.category?.name || 'Unclassified Material' }}
              </div>
            </div>
          </div>
        </template>

        <template #cell-pricing="{ row }">
          <div class="pz-inventory-list__stack">
            <strong>{{ formatPrice(row.base_price, row.effective_currency || row.currency) }}</strong>
            <span>Unit: {{ row.unit || 'unit' }}</span>
          </div>
        </template>

        <template #cell-inventory="{ row }">
          <div class="pz-inventory-list__stack">
            <Badge :variant="inventoryBadgeVariant(row.inventory_signal)">
              {{ formatInventorySignal(row.inventory_signal) }}
            </Badge>
            <span>On hand: {{ row.stock_quantity }}</span>
            <span>Available: {{ row.available_quantity ?? row.stock_quantity }}</span>
            <span>Reorder at: {{ row.reorder_level ?? 0 }}</span>
          </div>
        </template>

        <template #cell-compliance="{ row }">
          <div class="pz-inventory-list__stack">
            <span v-if="row.brand">Brand: {{ row.brand }}</span>
            <span v-if="row.country_of_origin">Origin: {{ row.country_of_origin }}</span>
            <span v-if="row.certification_highlights?.length">
              {{ row.certification_highlights.join(', ') }}
            </span>
            <span v-else class="pz-inventory-list__muted">No certification tags</span>
          </div>
        </template>

        <template #cell-status="{ row }">
          <Badge :variant="row.status === 'ACTIVE' ? 'earth' : 'secondary'">
            {{ row.status }}
          </Badge>
        </template>

        <template #cell-actions="{ row }">
          <div class="pz-inventory-list__actions">
            <Button size="sm" variant="outline" @click="$emit('adjust', row)">ADJUST</Button>
            <Button size="sm" variant="secondary" @click="$emit('history', row)">HISTORY</Button>
            <Button size="sm" variant="ghost" @click="$emit('edit', row)">EDIT</Button>
            <Button
              size="sm"
              variant="danger"
              :loading="deletingProductId === row.id"
              @click="$emit('delete', row)"
            >
              DELETE
            </Button>
          </div>
        </template>
      </PzDataTable>
    </div>

    <div class="pz-inventory-list__mobile">
      <article v-for="product in products" :key="product.id" class="pz-inventory-list__row">
        <div class="pz-inventory-list__row-top">
          <div class="pz-inventory-list__material">
            <img
              class="pz-inventory-list__thumb"
              :src="product.primary_image_url || placeholderImage"
              :alt="product.name"
            >
            <div class="pz-inventory-list__material-copy">
              <div class="pz-inventory-list__name">{{ product.name }}</div>
              <div class="pz-inventory-list__category">
                {{ product.category_name || product.category?.name || 'Unclassified Material' }}
              </div>
            </div>
          </div>
          <Badge :variant="product.status === 'ACTIVE' ? 'earth' : 'secondary'">
            {{ product.status }}
          </Badge>
        </div>

        <div class="pz-inventory-list__meta-grid">
          <div class="pz-inventory-list__meta-cell">
            <span class="pz-inventory-list__meta-label">Price</span>
            <strong>{{ formatPrice(product.base_price, product.effective_currency || product.currency) }}</strong>
          </div>
          <div class="pz-inventory-list__meta-cell">
            <span class="pz-inventory-list__meta-label">Inventory</span>
            <Badge :variant="inventoryBadgeVariant(product.inventory_signal)">
              {{ product.inventory_signal }}
            </Badge>
            <span>On hand: {{ product.stock_quantity }}</span>
            <span>Available: {{ product.available_quantity ?? product.stock_quantity }}</span>
          </div>
          <div class="pz-inventory-list__meta-cell">
            <span class="pz-inventory-list__meta-label">Brand</span>
            <span>{{ product.brand || 'Not set' }}</span>
          </div>
          <div class="pz-inventory-list__meta-cell">
            <span class="pz-inventory-list__meta-label">Origin</span>
            <span>{{ product.country_of_origin || 'Not set' }}</span>
          </div>
        </div>

        <div v-if="product.certification_highlights?.length" class="pz-inventory-list__certs">
          {{ product.certification_highlights.join(', ') }}
        </div>

        <div class="pz-inventory-list__actions">
          <Button size="sm" variant="outline" @click="$emit('adjust', product)">ADJUST</Button>
          <Button size="sm" variant="secondary" @click="$emit('history', product)">HISTORY</Button>
          <Button size="sm" variant="ghost" @click="$emit('edit', product)">EDIT</Button>
          <Button
            size="sm"
            variant="danger"
            :loading="deletingProductId === product.id"
            @click="$emit('delete', product)"
          >
            DELETE
          </Button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import PzDataTable from '../PzDataTable.vue';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';

defineEmits(['edit', 'delete', 'adjust', 'history']);

const props = defineProps({
  products: {
    type: Array,
    required: true,
  },
  deletingProductId: {
    type: [String, Number, null],
    default: null,
  },
  placeholderImage: {
    type: String,
    required: true,
  },
  formatPrice: {
    type: Function,
    required: true,
  },
  inventoryBadgeVariant: {
    type: Function,
    required: true,
  },
  formatInventorySignal: {
    type: Function,
    required: true,
  },
});

const columns = computed(() => ([
  { key: 'material', label: 'Material' },
  { key: 'pricing', label: 'Pricing' },
  { key: 'inventory', label: 'Inventory' },
  { key: 'compliance', label: 'Brand / Origin / Certs' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' },
]));
</script>

<style scoped>
.pz-inventory-list {
  display: grid;
  gap: 1rem;
}

.pz-inventory-list__material {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  min-width: 0;
}

.pz-inventory-list__thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: #e2e8f0;
  flex-shrink: 0;
}

.pz-inventory-list__material-copy,
.pz-inventory-list__stack {
  display: grid;
  gap: 0.2rem;
  min-width: 0;
}

.pz-inventory-list__name {
  font-family: var(--pz-font-mono);
  font-weight: 700;
  font-size: 0.82rem;
}

.pz-inventory-list__category,
.pz-inventory-list__stack,
.pz-inventory-list__muted {
  font-size: 0.74rem;
  color: var(--pz-color-steel-grey);
}

.pz-inventory-list__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pz-inventory-list__mobile {
  display: none;
}

.pz-inventory-list__row {
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
  padding: 1rem;
  display: grid;
  gap: 1rem;
}

.pz-inventory-list__row-top {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 1rem;
}

.pz-inventory-list__meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.85rem;
}

.pz-inventory-list__meta-cell {
  display: grid;
  gap: 0.25rem;
  font-size: 0.78rem;
}

.pz-inventory-list__meta-label {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-inventory-list__certs {
  font-size: 0.74rem;
  color: var(--pz-color-steel-grey);
}

@media (max-width: 900px) {
  .pz-inventory-list__desktop {
    display: none;
  }

  .pz-inventory-list__mobile {
    display: grid;
    gap: 1rem;
  }
}

@media (max-width: 640px) {
  .pz-inventory-list__meta-grid {
    grid-template-columns: 1fr;
  }
}
</style>
