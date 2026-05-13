<template>
  <div class="pz-material-detail">
    <div v-if="loading" class="pz-detail-state">
      <div class="c-loader u-mb-4"></div>
      <p>Loading material intelligence...</p>
    </div>

    <div v-else-if="error" class="pz-detail-state">
      <div class="c-alert c-alert--danger u-mb-6">{{ error }}</div>
      <Button variant="primary" @click="$router.push('/products')">Back to Materials</Button>
    </div>

    <div v-else-if="product" class="pz-l-container u-py-8">
      <nav class="pz-breadcrumb u-mb-8">
        <router-link to="/products" class="pz-breadcrumb__item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
          Materials
        </router-link>
        <span class="pz-breadcrumb__separator">/</span>
        <span class="pz-breadcrumb__current">{{ product.name }}</span>
      </nav>

      <section class="pz-detail-hero">
        <div class="pz-detail-gallery">
          <div class="pz-detail-gallery__main">
            <img :src="selectedImage || product.primary_image_url || '/placeholder.png'" :alt="product.name">
            <div class="pz-detail-gallery__badges">
              <Badge v-if="product.is_featured" variant="earth">Featured</Badge>
              <Badge v-if="product.inventory_signal === 'LOW_STOCK'" variant="warning">Low Stock</Badge>
              <Badge v-else-if="product.inventory_signal === 'OUT_OF_STOCK'" variant="danger">Out of Stock</Badge>
              <Badge v-else variant="success">In Stock</Badge>
            </div>
          </div>
          <div v-if="product.images?.length > 1" class="pz-detail-gallery__thumbs">
            <button
              v-for="img in product.images"
              :key="img.id"
              type="button"
              class="pz-detail-gallery__thumb"
              :class="{ 'pz-detail-gallery__thumb--active': selectedImage === img.image_url }"
              @click="selectedImage = img.image_url"
            >
              <img :src="img.image_url" :alt="img.alt_text || product.name">
            </button>
          </div>
        </div>

        <div class="pz-detail-summary">
          <div class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-3 u-mb-3">
            <Badge variant="savanna">{{ product.category?.name || 'Material' }}</Badge>
            <Badge v-if="product.brand" variant="secondary">{{ product.brand }}</Badge>
            <Badge v-for="cert in certificationHighlights" :key="cert" variant="success">{{ cert }}</Badge>
          </div>

          <h1 class="pz-u-text-display text-4xl u-mb-3">{{ product.name }}</h1>
          <p class="pz-u-color-steel u-mb-6">{{ product.short_description || product.description }}</p>

          <div class="pz-detail-meta">
            <div><span>Vendor</span><strong>{{ product.vendor_business_name || 'Marketplace Vendor' }}</strong></div>
            <div><span>Location</span><strong>{{ product.vendor_location || product.vendor_formatted_address || 'Location on request' }}</strong></div>
            <div><span>Origin</span><strong>{{ product.country_of_origin || 'Not specified' }}</strong></div>
            <div><span>Packaging</span><strong>{{ product.packaging_details || 'Standard packaging' }}</strong></div>
          </div>

          <div class="pz-detail-price">
            <div>
              <div class="pz-detail-price__amount">{{ configStore.formatPrice(product.base_price, product.effective_currency || product.currency, targetCurrencyCode) }}</div>
              <div class="pz-detail-price__unit">per {{ product.unit }}</div>
              <div class="pz-detail-price__unit">Stored in {{ product.effective_currency || product.currency || 'KES' }}</div>
            </div>
            <div v-if="product.bulk_price" class="pz-detail-price__bulk">
              <div>Bulk: {{ configStore.formatPrice(product.bulk_price, product.effective_currency || product.currency, targetCurrencyCode) }}</div>
              <small>{{ product.bulk_threshold }}+ {{ product.unit }}</small>
            </div>
          </div>

          <div class="pz-detail-panels">
            <div class="pz-detail-panel">
              <span>Inventory</span>
              <strong>{{ product.stock_quantity }} {{ product.unit }}</strong>
              <small>Reorder at {{ product.reorder_level || 0 }}</small>
            </div>
            <div class="pz-detail-panel">
              <span>Lead Time</span>
              <strong>{{ product.estimated_delivery_days || '3-5' }} days</strong>
              <small>{{ product.delivery_regions?.length ? product.delivery_regions.join(', ') : 'Delivery regions on request' }}</small>
            </div>
            <div class="pz-detail-panel">
              <span>Minimum Order</span>
              <strong>{{ product.min_order_quantity || 1 }} {{ product.unit }}</strong>
              <small>{{ product.max_order_quantity ? `Max ${product.max_order_quantity}` : 'No max limit set' }}</small>
            </div>
          </div>

          <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
            <Button variant="primary" size="lg" :disabled="product.inventory_signal === 'OUT_OF_STOCK'" @click="requestQuote(product)">
              Request Quote
            </Button>
            <Button variant="outline" size="lg" @click="contactVendor">Contact Vendor</Button>
          </div>
        </div>
      </section>

      <section class="pz-detail-grid u-mt-10">
        <div class="pz-detail-main">
          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Material Brief</div>
                <h3>Description</h3>
              </div>
            </div>
            <p class="pz-u-color-steel">{{ product.description }}</p>
          </div>

          <div v-if="highlightAttributes.length" class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Fast Scan</div>
                <h3>Key Attributes</h3>
              </div>
            </div>
            <div class="pz-detail-chip-grid">
              <div v-for="attribute in highlightAttributes" :key="attribute.name" class="pz-detail-chip">
                <span>{{ attribute.name }}</span>
                <strong>{{ attribute.value }}{{ attribute.unit ? ` ${attribute.unit}` : '' }}</strong>
              </div>
            </div>
          </div>

          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Technical Layer</div>
                <h3>Specifications</h3>
              </div>
            </div>
            <table class="pz-detail-table">
              <tbody>
                <tr v-for="spec in specificationRows" :key="spec.label">
                  <td>{{ spec.label }}</td>
                  <td>{{ spec.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="groupedAttributes.length" class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Structured Attributes</div>
                <h3>Performance & Physical Data</h3>
              </div>
            </div>
            <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
              <div v-for="group in groupedAttributes" :key="group.name" class="pz-detail-subcard">
                <h4>{{ group.name }}</h4>
                <ul class="pz-detail-list">
                  <li v-for="item in group.items" :key="`${group.name}-${item.name}`">
                    <span>{{ item.name }}</span>
                    <strong>{{ item.value }}{{ item.unit ? ` ${item.unit}` : '' }}</strong>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <aside class="pz-detail-side">
          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Compliance</div>
                <h3>Certifications</h3>
              </div>
            </div>
            <div v-if="product.certification_entries?.length" class="pz-detail-stack">
              <div v-for="cert in product.certification_entries" :key="cert.id" class="pz-detail-subcard">
                <h4>{{ cert.display_name || cert.registry_name || 'Certification' }}</h4>
                <p>{{ cert.issuing_body || 'Issuing body not specified' }}</p>
                <small v-if="cert.certification_number">Ref: {{ cert.certification_number }}</small>
              </div>
            </div>
            <p v-else class="pz-u-color-steel">No structured certification records published yet.</p>
          </div>

          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Procurement Pack</div>
                <h3>Documents</h3>
              </div>
            </div>
            <div v-if="publicDocuments.length" class="pz-detail-stack">
              <a v-for="doc in publicDocuments" :key="doc.id" :href="doc.external_url || doc.file_url" target="_blank" rel="noopener" class="pz-detail-doc">
                <strong>{{ doc.title }}</strong>
                <span>{{ doc.document_type }}</span>
              </a>
            </div>
            <p v-else class="pz-u-color-steel">Datasheets and brochures will appear here once published.</p>
          </div>

          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Handling</div>
                <h3>Logistics & Usage</h3>
              </div>
            </div>
            <ul class="pz-detail-list">
              <li><span>Special handling</span><strong>{{ product.requires_special_handling ? 'Required' : 'Standard' }}</strong></li>
              <li><span>Weight</span><strong>{{ product.shipping_weight || product.weight || 'N/A' }}{{ product.shipping_weight || product.weight ? ' kg' : '' }}</strong></li>
              <li><span>Warranty</span><strong>{{ product.warranty_period || 'Not specified' }}</strong></li>
            </ul>
            <p v-if="product.handling_instructions" class="pz-u-color-steel u-mt-4">{{ product.handling_instructions }}</p>
          </div>

          <div class="pz-detail-card">
            <div class="pz-detail-card__header">
              <div>
                <div class="pz-detail-card__eyebrow">Recommended Use</div>
                <h3>Applications</h3>
              </div>
            </div>
            <ul class="pz-detail-tag-list">
              <li v-for="item in applicationList" :key="item">{{ item }}</li>
            </ul>
          </div>
        </aside>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const configStore = useConfigStore();
const showAlert = inject('showAlert');

const product = ref(null);
const loading = ref(true);
const error = ref(null);
const selectedImage = ref(null);
const targetCurrencyCode = computed(() => {
  const routeCurrency = (route.query.currency || route.query.target_currency || '').toString().trim().toUpperCase();
  return routeCurrency || configStore.activeCurrencyCode || 'KES';
});

const certificationHighlights = computed(() =>
  (product.value?.certification_entries || [])
    .slice(0, 3)
    .map((entry) => entry.display_name || entry.registry_name)
    .filter(Boolean)
);

const highlightAttributes = computed(() =>
  (product.value?.attribute_entries || []).filter((entry) => entry.is_highlight).slice(0, 6)
);

const groupedAttributes = computed(() => {
  const grouped = new Map();
  for (const entry of product.value?.attribute_entries || []) {
    const groupName = entry.group || 'General';
    if (!grouped.has(groupName)) {
      grouped.set(groupName, []);
    }
    grouped.get(groupName).push(entry);
  }
  return Array.from(grouped.entries()).map(([name, items]) => ({ name, items }));
});

const publicDocuments = computed(() =>
  (product.value?.documents || []).filter((entry) => entry.is_public && (entry.external_url || entry.file_url))
);

const applicationList = computed(() => {
  const raw = `${product.value?.applications || ''}\n${product.value?.features || ''}`;
  return raw
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 8);
});

const specificationRows = computed(() => {
  if (!product.value) {
    return [];
  }
  const rows = [
    ['Brand', product.value.brand],
    ['Model / SKU', product.value.model_number],
    ['Quality Grade', product.value.quality_grade],
    ['Dimensions', product.value.dimensions],
    ['Color / Finish', product.value.color],
    ['Composition', product.value.material_composition],
  ]
    .filter(([, value]) => value)
    .map(([label, value]) => ({ label, value }));

  for (const [label, value] of Object.entries(product.value.technical_specifications || {})) {
    rows.push({ label, value });
  }
  return rows;
});

const fetchProduct = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.get(`/v1/products/${route.params.id}/`);
    product.value = response.data;
    selectedImage.value = response.data.primary_image_url || response.data.images?.[0]?.image_url || null;
  } catch (err) {
    error.value = 'Material not found or unavailable.';
  } finally {
    loading.value = false;
  }
};

const requestQuote = async (material) => {
  if (!authStore.isAuthenticated) {
    showAlert?.('Please sign in to request a quote.', 'info');
    router.push('/login');
    return;
  }
  try {
    await api.post('/orders/quote-requests/', {
      items: [{ product: material.id, quantity: material.min_order_quantity || 1 }],
    });
    showAlert?.('Quote request sent successfully.', 'success');
    router.push('/buyer/dashboard');
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to request quote.', 'error');
  }
};

const contactVendor = () => {
  showAlert?.('Vendor messaging will open from this detail page once chat routing is enabled for materials.', 'info');
};

onMounted(fetchProduct);
</script>

<style scoped>
.pz-material-detail {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(246, 242, 236, 0.96)),
    radial-gradient(circle at top left, rgba(212, 101, 42, 0.12), transparent 28%);
}

.pz-detail-state {
  min-height: 60vh;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 2rem;
}

.pz-detail-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 2rem;
}

.pz-detail-gallery__main {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: #ffffff;
  border-radius: 20px;
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 8px 24px rgba(10, 10, 15, 0.06);
  aspect-ratio: 1 / 1;
}

.pz-detail-gallery__main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-detail-gallery__main:hover img {
  transform: scale(1.03);
}
.pz-detail-gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pz-detail-gallery__badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pz-detail-gallery__thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  gap: 0.75rem;
  margin-top: 0.9rem;
}

.pz-detail-gallery__thumb {
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  cursor: pointer;
  border-radius: 12px;
  transition: all 0.2s ease;
}
.pz-detail-gallery__thumb:hover {
  border-color: rgba(212, 101, 42, 0.3);
  box-shadow: 0 4px 12px rgba(10, 10, 15, 0.08);
}

.pz-detail-gallery__thumb--active {
  border-color: var(--pz-color-earth-orange);
}

.pz-detail-summary,
.pz-detail-card {
  background: #ffffff;
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 20px;
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 4px 16px rgba(10, 10, 15, 0.04);
  position: relative;
  overflow: hidden;
}
.pz-detail-summary::before,
.pz-detail-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, rgba(212, 101, 42, 0), rgba(212, 101, 42, 0.7), rgba(212, 101, 42, 0));
  opacity: 0;
  transition: opacity 0.3s ease;
}
.pz-detail-summary:hover::before,
.pz-detail-card:hover::before {
  opacity: 1;
}

.pz-detail-summary {
  padding: 1.75rem;
}

.pz-detail-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.9rem;
  margin-bottom: 1.25rem;
}

.pz-detail-meta div,
.pz-detail-panel {
  display: grid;
  gap: 0.2rem;
}

.pz-detail-meta span,
.pz-detail-panel span,
.pz-detail-card__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--pz-color-earth-orange);
}

.pz-detail-price {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
  border-bottom: 1px solid rgba(10, 10, 15, 0.08);
  margin-bottom: 1rem;
}

.pz-detail-price__amount {
  font-family: var(--pz-font-display);
  font-size: clamp(2rem, 3.8vw, 3.4rem);
  line-height: 1;
}

.pz-detail-price__unit,
.pz-detail-price__bulk small {
  color: var(--pz-color-steel-grey);
}

.pz-detail-panels {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  margin-bottom: 1.25rem;
}

.pz-detail-panel {
  padding: 1rem;
  background: rgba(250, 249, 245, 0.8);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 14px;
  display: grid;
  gap: 0.25rem;
}

.pz-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 1.5rem;
}

.pz-detail-main,
.pz-detail-side,
.pz-detail-stack {
  display: grid;
  gap: 1rem;
}

.pz-detail-card {
  padding: 1.5rem;
}

.pz-detail-card__header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.pz-detail-card h3,
.pz-detail-subcard h4 {
  margin: 0.15rem 0 0;
}

.pz-detail-chip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.8rem;
}

.pz-detail-chip,
.pz-detail-subcard,
.pz-detail-doc {
  display: grid;
  gap: 0.2rem;
  padding: 0.9rem;
  background: rgba(250, 249, 245, 0.7);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 12px;
  transition: all 0.2s ease;
}
.pz-detail-doc:hover {
  background: rgba(250, 249, 245, 0.9);
  border-color: rgba(212, 101, 42, 0.2);
}

.pz-detail-doc {
  text-decoration: none;
  color: inherit;
}

.pz-detail-table {
  width: 100%;
  border-collapse: collapse;
}

.pz-detail-table td {
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-detail-table td:first-child {
  width: 40%;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
}

.pz-detail-list,
.pz-detail-tag-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.8rem;
}

.pz-detail-list li {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.pz-detail-tag-list {
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
}

.pz-detail-tag-list li {
  padding: 0.5rem 0.75rem;
  background: rgba(212, 101, 42, 0.05);
  border: 1px solid rgba(212, 101, 42, 0.1);
  border-radius: 10px;
  font-size: 0.85rem;
  color: var(--pz-color-earth-orange);
  font-weight: 500;
  text-align: center;
}

.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
}
.pz-breadcrumb__item {
  color: var(--pz-color-concrete-grey);
  text-decoration: none;
  transition: color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.pz-breadcrumb__item:hover {
  color: var(--pz-color-earth-orange);
}
.pz-breadcrumb__separator {
  color: rgba(10, 10, 15, 0.15);
  font-size: 0.65rem;
}
.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-weight: 500;
}

@media (max-width: 980px) {
  .pz-detail-hero,
  .pz-detail-grid {
    grid-template-columns: 1fr;
  }

  .pz-detail-meta,
  .pz-detail-panels {
    grid-template-columns: 1fr;
  }
}
</style>
