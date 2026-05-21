<template>
  <div class="vendor-quotes-section">
    <!-- Response Coaching Banner -->
    <div v-if="responseStats" class="pz-coaching-banner">
      <div class="pz-coaching-banner__icon">⏱️</div>
      <div class="pz-coaching-banner__body">
        <strong>You respond in {{ responseStats.avg_hours }}h on average.</strong>
        <span v-if="responseStats.avg_hours <= 2"> Great job — fast responses win more quotes.</span>
        <span v-else> Responding within 2h increases your win rate by 35%.</span>
      </div>
    </div>

    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">Commercial Response</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">Quote Requests</h3>
          <div class="pz-section-shell__meta">Review buyer requests and send your pricing.</div>
        </div>
        <Button variant="ghost" size="sm" @click="fetchQuotes">Refresh</Button>
      </div>

      <div class="pz-section-shell__content">
        <div v-if="loading" class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">Loading quote requests...</div>
        </div>

        <!-- Guided Empty State -->
        <div v-else-if="quotes.length === 0" class="pz-empty-state pz-empty-state--guided">
          <div class="pz-empty-state__glyph">📭</div>
          <div class="pz-empty-state__eyebrow">No Quotes Yet</div>
          <h4 class="pz-empty-state__title">Buyers are browsing your catalog.</h4>
          <p class="pz-empty-state__body">
            When a project owner requests pricing, it will appear here. Here's how to increase your chances:
          </p>
          <div class="pz-empty-state__tips pz-empty-state__tips--list">
            <p>1. Add photos to your materials — listings with images get 5× more views</p>
            <p>2. Set competitive bulk pricing to attract large project orders</p>
            <p>3. Enable delivery to more regions</p>
          </div>
          <div class="pz-empty-state__actions">
            <Button variant="primary" @click="$emit('navigate', 'inventory')">Improve My Listings</Button>
          </div>
        </div>

        <div v-else class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div
            v-for="quote in quotes"
            :key="quote.id"
            class="pz-quote-card"
            :class="{ 'pz-quote-card--urgent': isUrgent(quote) }"
          >
            <div class="pz-l-flex pz-l-flex--justify-between u-mb-4">
              <div>
                <div class="pz-u-text-mono font-bold text-sm">Quote #{{ quote.id }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ quote.buyer_name || 'Guest Buyer' }}</div>
              </div>
              <div class="pz-l-flex pz-l-flex--gap-2">
                <Badge v-if="isUrgent(quote)" variant="error">URGENT &gt;12h</Badge>
                <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'">
                  {{ quote.status === 'REQUESTED' ? 'Awaiting Response' : quote.status }}
                </Badge>
              </div>
            </div>

            <div class="pz-u-bg-limestone pz-p-4 u-mb-4">
              <div
                v-for="item in quote.items" :key="item.id"
                class="pz-l-flex pz-l-flex--justify-between text-xs u-mb-1"
              >
                <span>{{ item.quantity }}× {{ item.product_details?.name || 'Unknown Item' }}</span>
                <span class="pz-u-text-mono font-bold">
                  {{ configStore.formatPrice(item.product_details?.base_price, item.product_details?.effective_currency || item.product_details?.currency) }}
                </span>
              </div>
            </div>

            <!-- One-Tap Quick Actions -->
            <div v-if="quote.status === 'REQUESTED'" class="pqq-quick-actions">
              <Button
                size="sm"
                variant="primary"
                class="pqq-quick-actions__btn"
                @click="acceptAtListedPrice(quote)"
              >
                ✅ Accept at Listed Price
              </Button>
              <Button
                size="sm"
                variant="secondary"
                class="pqq-quick-actions__btn"
                @click="openResponseModal(quote)"
              >
                💬 Counter Offer
              </Button>
              <Button
                size="sm"
                variant="ghost"
                class="pqq-quick-actions__btn"
                @click="declineQuote(quote)"
              >
                ❌ Decline
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Response Modal (for Counter Offer) -->
    <Modal :isOpen="showResponseModal" title="Send Counter Offer" size="lg" @close="showResponseModal = false">
      <form id="quote-response-form" @submit.prevent="submitQuoteResponse">
        <div class="pz-u-bg-limestone pz-p-4 u-mb-6 pz-u-border">
          <div class="pz-u-text-mono text-xs font-bold u-mb-2">Line Item Pricing</div>
          <div
            v-for="(item, idx) in responseForm.items" :key="item.id"
            class="pz-l-grid pz-l-grid--cols-12 pz-l-grid--gap-4 pz-l-grid--align-center u-mb-2"
          >
            <div class="pz-l-grid__col-span-4 text-xs">{{ item.product_name }} (×{{ item.quantity }})</div>
            <div class="pz-l-grid__col-span-3">
              <input
                v-model="item.unit_price" type="number" class="pz-input pz-input--sm"
                placeholder="Unit Price" required
              >
            </div>
            <div class="pz-l-grid__col-span-5">
              <input
                v-model="item.availability_notes" type="text" class="pz-input pz-input--sm"
                placeholder="Notes (e.g. In Stock)"
              >
            </div>
          </div>
        </div>

        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <PzInput
            v-model="responseForm.delivery_fee"
            :label="`Delivery Fee (${configStore.activeCurrency.symbol})`" type="number"
          />
          <PzInput v-model="responseForm.valid_until" type="date" label="Quote Valid Until" />
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="showResponseModal = false">Cancel</Button>
        <Button type="submit" form="quote-response-form" variant="primary" :loading="submitting">
          Send Quote
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';
import Modal from '../ui/Modal.vue';
import PzInput from '../PzInput.vue';
import { useConfigStore } from '../../stores/config';

const emit = defineEmits(['navigate']);

const configStore = useConfigStore();
const quotes = ref([]);
const loading = ref(true);
const showResponseModal = ref(false);
const submitting = ref(false);
const selectedQuote = ref(null);
const showAlert = inject('showAlert');
const responseStats = ref(null);

function isUrgent(quote) {
  if (!quote.requested_at) return false;
  const hours = (Date.now() - new Date(quote.requested_at).getTime()) / 36e5;
  return hours > 12;
}

const responseForm = ref({
  items: [],
  delivery_fee: 0,
  valid_until: ''
});

async function fetchQuotes() {
  loading.value = true;
  try {
    const [quotesRes, statsRes] = await Promise.all([
      api.get('/orders/quote-requests/vendor_quotes/'),
      api.get('/vendors/me/').catch(() => null)
    ]);
    quotes.value = quotesRes.data.results || quotesRes.data;
    if (statsRes?.data?.avg_response_time_hours != null) {
      responseStats.value = { avg_hours: Math.round(statsRes.data.avg_response_time_hours) };
    }
  } catch (err) {
    console.error('Fetch quotes error', err);
  } finally {
    loading.value = false;
  }
}

function openResponseModal(quote) {
  selectedQuote.value = quote;
  responseForm.value = {
    items: quote.items.map(item => ({
      id: item.id,
      product_name: item.product_details?.name,
      quantity: item.quantity,
      unit_price: item.product_details?.base_price,
      availability_notes: 'In Stock'
    })),
    delivery_fee: 50,
    valid_until: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  };
  showResponseModal.value = true;
}

async function submitQuoteResponse() {
  submitting.value = true;
  try {
    await api.post(`/orders/quote-requests/${selectedQuote.value.id}/respond/`, {
      items: responseForm.value.items.map(i => ({
        id: i.id,
        unit_price: i.unit_price,
        availability_notes: i.availability_notes
      })),
      delivery_fee: responseForm.value.delivery_fee,
      valid_until: responseForm.value.valid_until
    });
    if (showAlert) showAlert('Quote sent to buyer successfully.', 'success');
    showResponseModal.value = false;
    fetchQuotes();
  } catch (err) {
    if (showAlert) showAlert('Failed to send quote. Please try again.', 'error');
  } finally {
    submitting.value = false;
  }
}

async function acceptAtListedPrice(quote) {
  try {
    await api.post(`/orders/quote-requests/${quote.id}/respond/`, {
      items: quote.items.map(item => ({
        id: item.id,
        unit_price: item.product_details?.base_price,
        availability_notes: 'In Stock'
      })),
      delivery_fee: 0,
      valid_until: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    });
    if (showAlert) showAlert('Quote accepted at listed price.', 'success');
    fetchQuotes();
  } catch (err) {
    if (showAlert) showAlert('Could not accept quote. Please try again.', 'error');
  }
}

async function declineQuote(quote) {
  if (!confirm('Decline this quote request? The buyer will be notified.')) return;
  try {
    await api.post(`/orders/quote-requests/${quote.id}/decline/`);
    if (showAlert) showAlert('Quote declined. Buyer has been notified.', 'info');
    fetchQuotes();
  } catch (err) {
    if (showAlert) showAlert('Could not decline quote. Please try again.', 'error');
  }
}

onMounted(fetchQuotes);
</script>

<style scoped>
.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 2px solid var(--pz-color-foundation-black);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.pz-quote-card {
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(10, 10, 15, 0.08);
  padding: var(--pz-space-6);
  transition: border-color 0.2s, transform 0.2s;
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

.pz-quote-card:hover {
  border-color: var(--pz-color-primary);
  transform: translate(-2px, -2px);
}

.pz-quote-card--urgent {
  border-color: #dc2626;
  border-width: 2px;
}

.pz-quote-card--urgent:hover {
  border-color: #991b1b;
}

/* Response coaching banner */
.pz-coaching-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #1e3a5f;
}

.pz-coaching-banner__icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

/* One-tap quick actions */
.pqq-quick-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pqq-quick-actions__btn {
  flex: 1 1 auto;
  min-width: 0;
  white-space: nowrap;
}

/* Empty state enhancements */
.pz-empty-state--guided {
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.pz-empty-state--guided .pz-empty-state__glyph {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.pz-empty-state--guided .pz-empty-state__title {
  font-size: 1.3rem;
  margin: 0.5rem 0;
}

.pz-empty-state__tips--list {
  text-align: left;
  display: inline-block;
  margin: 1rem 0;
}

.pz-empty-state__tips--list p {
  margin: 0.35rem 0;
}

.pz-empty-state__actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}
</style>
