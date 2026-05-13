<template>
  <div class="pz-finance-page">
    <div class="pz-l-container u-py-8">
      <!-- Breadcrumb -->
      <nav class="pz-breadcrumb u-mb-6">
        <router-link to="/investor/dashboard" class="pz-breadcrumb__item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
          Investor Dashboard
        </router-link>
        <span class="pz-breadcrumb__separator">/</span>
        <span class="pz-breadcrumb__current pz-u-color-steel">Apply for Financing</span>
      </nav>

      <div class="pz-finance-layout">
        <!-- Form -->
        <section class="pz-space-y-6">
          <Card title="Finance Application" variant="premium" eyebrow="Credit Request">
            <form @submit.prevent="submitApplication" class="pz-finance-form">
              <div class="pz-finance-grid pz-finance-grid--two">
                <div class="pz-input-wrapper">
                  <label class="pz-input__label">Finance Product <span class="pz-input__required">*</span></label>
                  <select v-model="form.product_id" class="pz-input" required @change="onProductChange">
                    <option disabled value="">Select product</option>
                    <option v-for="p in products" :key="p.id" :value="p.id">
                      {{ p.name }} — {{ formatPrice(p.max_amount, p.currency || 'KES') }} max @ {{ p.interest_rate }}%
                    </option>
                  </select>
                </div>

                <div class="pz-input-wrapper">
                  <label class="pz-input__label">Target Type <span class="pz-input__required">*</span></label>
                  <select v-model="form.target_type" class="pz-input" required>
                    <option value="PROJECT">Project</option>
                    <option value="PROPERTY">Property</option>
                    <option value="MATERIAL_ORDER">Material Order</option>
                    <option value="CONTRACT">Contract</option>
                    <option value="GENERAL_WORKING_CAPITAL">Working Capital</option>
                  </select>
                </div>

                <PzInput v-model="form.requested_amount" :label="`Requested Amount (${configStore.activeCurrencyCode || 'KES'})`" type="number" required min="1" />

                <div class="pz-input-wrapper">
                  <label class="pz-input__label">Purpose Category <span class="pz-input__required">*</span></label>
                  <select v-model="form.purpose_category" class="pz-input" required>
                    <option value="ACQUISITION">Acquisition</option>
                    <option value="COMPLETION">Completion</option>
                    <option value="RENOVATION">Renovation</option>
                    <option value="MATERIALS_PROCUREMENT">Materials Procurement</option>
                    <option value="WORKING_CAPITAL">Working Capital</option>
                  </select>
                </div>
              </div>

              <div class="pz-input-wrapper">
                <label class="pz-input__label">Purpose Description <span class="pz-input__required">*</span></label>
                <textarea
                  v-model="form.purpose"
                  class="pz-input pz-finance-textarea"
                  rows="4"
                  required
                  placeholder="Describe how the funds will be used, timeline, and expected outcomes."
                ></textarea>
              </div>

              <div class="pz-finance-actions">
                <Button variant="outline" @click="$router.back()">Cancel</Button>
                <Button type="submit" variant="primary" :loading="submitting">Submit Application</Button>
              </div>
            </form>
          </Card>
        </section>

        <!-- Sidebar -->
        <aside class="pz-finance-sidebar">
          <Card title="Product Summary" variant="elevated">
            <div v-if="selectedProduct" class="pz-space-y-4">
              <div class="pz-detail-subcard">
                <span>Provider</span>
                <strong>{{ selectedProduct.provider_name }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Maximum Amount</span>
                <strong>{{ formatPrice(selectedProduct.max_amount, selectedProduct.currency || 'KES') }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Interest Rate</span>
                <strong>{{ selectedProduct.interest_rate }}%</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Status</span>
                <Badge :variant="selectedProduct.active ? 'success' : 'secondary'">
                  {{ selectedProduct.active ? 'Active' : 'Inactive' }}
                </Badge>
              </div>
            </div>
            <div v-else class="pz-finance-empty">
              <p>Select a finance product to see details.</p>
            </div>
          </Card>

          <Card title="Eligibility Checklist" variant="glass">
            <div class="pz-checklist">
              <div class="pz-checklist__item">
                <span class="pz-checklist__dot"></span>
                <span>Verified platform account</span>
              </div>
              <div class="pz-checklist__item">
                <span class="pz-checklist__dot"></span>
                <span>Minimum transaction history</span>
              </div>
              <div class="pz-checklist__item">
                <span class="pz-checklist__dot"></span>
                <span>No open disputes</span>
              </div>
              <div class="pz-checklist__item">
                <span class="pz-checklist__dot"></span>
                <span>Completion rate > 60%</span>
              </div>
            </div>
          </Card>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';
import FinanceService from '../services/finance';
import { useConfigStore } from '../stores/config';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import Card from '../components/ui/Card.vue';
import PzInput from '../components/PzInput.vue';

const router = useRouter();
const configStore = useConfigStore();
const showAlert = inject('showAlert');
const products = ref([]);
const submitting = ref(false);
const form = ref({
  product_id: '',
  target_type: 'PROJECT',
  requested_amount: '',
  purpose_category: 'WORKING_CAPITAL',
  purpose: '',
});

const selectedProduct = computed(() => {
  return products.value.find(p => p.id === form.value.product_id) || null;
});

onMounted(async () => {
  try {
    const res = await FinanceService.listProducts();
    products.value = res.data.results || res.data || [];
  } catch (e) {
    console.error(e);
  }
});

function onProductChange() {
  // Reset amount if it exceeds new product max
  const product = selectedProduct.value;
  if (product && form.value.requested_amount > parseFloat(product.max_amount)) {
    form.value.requested_amount = parseFloat(product.max_amount);
  }
}

async function submitApplication() {
  submitting.value = true;
  try {
    await FinanceService.createApplication({
      product: form.value.product_id,
      target_type: form.value.target_type,
      requested_amount: form.value.requested_amount,
      purpose_category: form.value.purpose_category,
      purpose: form.value.purpose,
    });
    showAlert?.('Application submitted successfully.', 'success');
    router.push('/investor/dashboard');
  } catch (err) {
    const detail = err.response?.data?.detail || err.response?.data?.error || 'Application failed. Please check your inputs.';
    showAlert?.(detail, 'error');
  } finally {
    submitting.value = false;
  }
}

function formatPrice(amount, sourceCurrency = 'KES') {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return 'KES 0.00';
  return configStore.formatPrice ? configStore.formatPrice(value, sourceCurrency) : `KES ${value.toLocaleString()}`;
}
</script>

<style scoped>
.pz-finance-page {
  min-height: 100vh;
  background-color: var(--pz-color-limestone-white);
}

.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--pz-color-concrete-grey);
}

.pz-breadcrumb__item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--pz-color-earth-orange);
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.pz-breadcrumb__item:hover {
  opacity: 0.8;
}

.pz-breadcrumb__separator {
  color: var(--pz-color-concrete-grey);
  opacity: 0.5;
}

.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
}

/* Layout */
.pz-finance-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.75rem;
}

.pz-finance-sidebar {
  display: grid;
  gap: 1rem;
  height: fit-content;
}

/* Form */
.pz-finance-form {
  display: grid;
  gap: 1.25rem;
}

.pz-finance-grid {
  display: grid;
  gap: 1rem;
}

.pz-finance-grid--two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pz-finance-textarea {
  resize: vertical;
  min-height: 6rem;
}

.pz-finance-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

/* Detail cards */
.pz-detail-subcard {
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-detail-subcard span:first-child {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-detail-subcard strong {
  display: block;
  margin-top: 0.15rem;
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-finance-empty {
  padding: 1rem 0;
  text-align: center;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
}

/* Checklist */
.pz-checklist {
  display: grid;
  gap: 0.6rem;
}

.pz-checklist__item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.85rem;
  color: var(--pz-color-structural-steel);
}

.pz-checklist__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--pz-color-earth-orange);
  flex-shrink: 0;
}

/* Utilities */
.pz-space-y-4 > * + * { margin-top: 1rem; }
.pz-space-y-6 > * + * { margin-top: 1.5rem; }
.u-py-8 { padding-top: 2rem; padding-bottom: 2rem; }
.u-mb-6 { margin-bottom: 1.5rem; }

/* Responsive */
@media (max-width: 1024px) {
  .pz-finance-layout {
    grid-template-columns: 1fr;
  }
  .pz-finance-sidebar {
    position: static;
  }
}

@media (max-width: 640px) {
  .pz-finance-grid--two {
    grid-template-columns: 1fr;
  }
  .pz-finance-actions {
    flex-direction: column-reverse;
  }
}
</style>
