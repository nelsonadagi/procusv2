<template>
  <div v-if="materialRequirements.length > 0" class="pms-suggestions">
    <div class="pms-header">
      <div class="pms-header__icon">🔎</div>
      <div class="pms-header__text">
        <h4 class="pms-header__title">Find Suppliers</h4>
        <p class="pms-header__subtitle">
          {{ materialRequirements.length }} material requirement{{ materialRequirements.length === 1 ? '' : 's' }} — 
          <button class="pms-header__action" @click="fetchSuggestions">{{ loading ? 'Searching…' : 'Search catalog' }}</button>
        </p>
      </div>
    </div>

    <div v-if="loading" class="pms-loading">
      <div class="pms-loading__spinner"></div>
      <span>Finding matching products…</span>
    </div>

    <div v-else-if="matches.length > 0" class="pms-grid">
      <div
        v-for="product in matches"
        :key="product.uuid"
        class="pms-card"
        @click="goToProduct(product)"
      >
        <div class="pms-card__image">
          <img
            :src="product.primary_image_url || placeholderImage"
            :alt="product.name"
            loading="lazy"
          />
          <Badge v-if="product.vendor_verified_status === 'APPROVED'" size="xs" variant="success" class="pms-card__badge">
            Verified
          </Badge>
        </div>
        <div class="pms-card__body">
          <div class="pms-card__name">{{ product.name }}</div>
          <div class="pms-card__vendor">{{ product.vendor_name }}</div>
          <div class="pms-card__price">{{ formatPrice(product) }}</div>
        </div>
        <div class="pms-card__actions">
          <Button size="xs" variant="primary" @click.stop="requestQuote(product)">
            Request Quote
          </Button>
        </div>
      </div>
    </div>

    <div v-else-if="searched" class="pms-empty">
      <p>No matching products found in the catalog.</p>
      <p class="pms-empty__hint">Try refining your requirement description or browse all products.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../services/api';
import { useConfigStore } from '../../stores/config';
import Badge from '../ui/Badge.vue';
import Button from '../ui/Button.vue';

const props = defineProps({
  project: { type: Object, required: true },
});

const emit = defineEmits(['show-alert']);

const router = useRouter();
const configStore = useConfigStore();

const loading = ref(false);
const searched = ref(false);
const matches = ref([]);

const placeholderImage = 'https://placehold.co/320x240?text=No+Image';

const materialRequirements = computed(() => {
  return (props.project.requirements || []).filter((r) => r.type === 'MATERIAL');
});

async function fetchSuggestions() {
  loading.value = true;
  searched.value = false;
  try {
    const res = await api.get(`/projects/${props.project.id}/suggest-products/`);
    matches.value = res.data.matches || [];
  } catch (err) {
    emit('show-alert', 'Could not load product suggestions. Please try again.', 'error');
  } finally {
    loading.value = false;
    searched.value = true;
  }
}

function formatPrice(product) {
  const price = product.effective_price || product.base_price;
  if (!price) return 'Price on request';
  return configStore.formatPrice(price, product.currency || 'KES');
}

function goToProduct(product) {
  router.push(`/products/${product.slug}`);
}

async function requestQuote(product) {
  try {
    const qty = Math.max(product.min_order_quantity || 1, 1);
    await api.post('/orders/quote-requests/', {
      items: [{ product: product.uuid || product.id, quantity: qty }],
    });
    emit('show-alert', `Quote request sent for ${product.name}`, 'success');
  } catch (err) {
    const msg = err.response?.data?.detail || err.response?.data?.error || 'Failed to send quote request';
    emit('show-alert', msg, 'error');
  }
}
</script>

<style scoped>
.pms-suggestions {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
}

.pms-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.pms-header__icon {
  font-size: 1.5rem;
}

.pms-header__title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: #0f172a;
}

.pms-header__subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.pms-header__action {
  background: none;
  border: none;
  color: #2563eb;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}

.pms-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.85rem;
  padding: 1rem 0;
}

.pms-loading__spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: pms-spin 0.8s linear infinite;
}

@keyframes pms-spin {
  to { transform: rotate(360deg); }
}

.pms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.75rem;
}

.pms-card {
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.15s;
}

.pms-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.pms-card__image {
  position: relative;
  height: 100px;
  background: #f1f5f9;
}

.pms-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pms-card__badge {
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
}

.pms-card__body {
  padding: 0.5rem;
}

.pms-card__name {
  font-size: 0.8rem;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pms-card__vendor {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.15rem;
}

.pms-card__price {
  font-size: 0.8rem;
  font-weight: 700;
  color: #059669;
  margin-top: 0.25rem;
}

.pms-card__actions {
  padding: 0 0.5rem 0.5rem;
}

.pms-empty {
  text-align: center;
  color: #64748b;
  font-size: 0.85rem;
  padding: 1rem 0;
}

.pms-empty__hint {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}
</style>
