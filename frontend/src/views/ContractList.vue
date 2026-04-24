<template>
  <div class="pz-marketplace">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Search contracts"
      placeholder="Search contracts by scope, title, or location"
      search-label="Search Contracts"
      @submit="fetchContracts"
    />

    <main class="pz-l-container u-py-12">
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Tender Status</span>
            <select v-model="selectedStatus" @change="fetchContracts" class="pz-filter-bar__control">
              <option value="">All Visible</option>
              <option value="POSTED">Posted</option>
              <option value="BIDDING">Bidding</option>
              <option value="AWARDED">Awarded</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Operations Region</span>
            <select v-model="selectedLocation" @change="fetchContracts" class="pz-filter-bar__control">
              <option value="">All Regions</option>
              <option value="Nairobi">Nairobi</option>
              <option value="Mombasa">Mombasa</option>
              <option value="Kisumu">Kisumu</option>
              <option value="Nakuru">Nakuru</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">CapEx Range ({{ configStore.activeCurrency.symbol || '$' }})</span>
            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-2">
              <input v-model.number="budgetMin" type="number" placeholder="MIN" class="pz-filter-bar__input" @change="fetchContracts">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">/</span>
              <input v-model.number="budgetMax" type="number" placeholder="MAX" class="pz-filter-bar__input" @change="fetchContracts">
            </div>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Command Sequence</span>
            <select v-model="sortBy" @change="fetchContracts" class="pz-filter-bar__control">
              <option value="">Latest</option>
              <option value="budget_max">High Budget</option>
              <option value="-budget_max">Low Budget</option>
            </select>
          </div>
        </div>

        <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
          <div class="pz-view-switcher u-hide-mobile">
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }" @click="viewMode = 'grid'">
              ⣿
            </button>
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }" @click="viewMode = 'list'">
              ≡
            </button>
          </div>
          <Button v-if="hasActiveFilters" variant="ghost" size="sm" @click="clearFilters">RESET PORTFOLIO</Button>
        </div>
      </div>

      <div class="content-layout">
        <div class="pz-results-strip">
          <div class="pz-results-strip__metric">
            <span class="pz-results-strip__label">VISIBLE_TENDERS</span>
            <span class="pz-results-strip__value">{{ contracts.length }}</span>
          </div>
          <div class="pz-results-strip__metric">
            <span class="pz-results-strip__label">SEARCH_STATE</span>
            <span class="pz-results-strip__value">{{ loading ? 'SYNCING' : (error ? 'INTERRUPTED' : 'READY') }}</span>
          </div>
          <div class="pz-results-strip__metric">
            <span class="pz-results-strip__label">ACTIVE_FILTERS</span>
            <span class="pz-results-strip__value">{{ activeFilterCount }}</span>
          </div>
        </div>

        <div v-if="loading" class="pz-state-panel">
          <div class="pz-state-panel__kicker">PROCUREMENT_SCAN</div>
          <h3 class="pz-state-panel__title">Searching the contract network</h3>
          <p class="pz-state-panel__body">Matching tenders, status filters, and budget corridors against the live marketplace.</p>
        </div>

        <div v-else>
          <div v-if="error" class="pz-state-panel pz-state-panel--error">
            <div class="pz-state-panel__kicker">NETWORK_ERROR</div>
            <h3 class="pz-state-panel__title">Unable to load tenders right now</h3>
            <p class="pz-state-panel__body">{{ error }}</p>
            <Button variant="outline" @click="fetchContracts" class="u-mt-4">RETRY_SYNC</Button>
          </div>

          <div v-else-if="contracts.length === 0" class="pz-state-panel">
            <div class="pz-state-panel__kicker">EMPTY_RESULT_SET</div>
            <h3 class="pz-state-panel__title">No contracts matched this portfolio</h3>
            <p class="pz-state-panel__body">Try widening your region, status, or budget filters to see more tenders.</p>
            <Button variant="outline" @click="clearFilters" class="u-mt-4">RESET_ALL_FILTERS</Button>
          </div>

          <div v-else :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
            <article
              v-for="contract in contracts"
              :key="contract.id"
              class="pz-premium-card pz-card--interactive u-hover-spring"
              :class="{ 'pz-premium-card--list': viewMode === 'list' }"
              @click="$router.push(`/contracts/${contract.id}`)"
            >
              <div class="pz-premium-card__media">
                <img :src="contract.featured_image_url || '/placeholder.png'" :alt="contract.title || 'Contract brief'" class="pz-premium-card__img">
                <div class="pz-premium-card__badges">
                  <Badge :variant="getContractStatusVariant(contract.status)">{{ contract.status || 'POSTED' }}</Badge>
                </div>
              </div>

              <div class="pz-premium-card__content">
                <div class="pz-premium-card__top">
                  <span class="pz-premium-card__vendor">{{ contract.location || 'Undisclosed region' }}</span>
                  <div class="pz-premium-card__rating">{{ formatDate(contract.created_at) }}</div>
                </div>

                <h3 class="pz-premium-card__title">{{ contract.title || 'Untitled procurement brief' }}</h3>

                <div class="pz-premium-card__specs">
                  <span class="pz-spec-dot">ARCHITECT: {{ contract.owner_username || 'Platform owner' }}</span>
                  <span class="pz-spec-dot">SECTOR: {{ contract.sector || 'GENERAL' }}</span>
                </div>

                <div class="pz-premium-card__pricing">
                  <div class="pz-price-display">
                    <span class="pz-price-display__unit">EST. BUDGET</span>
                    <div class="pz-price-display__val">{{ formatBudget(contract) }}</div>
                  </div>
                  <Button variant="primary" size="sm">SUBMIT SPEC</Button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import api from '../services/api';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import EntryHero from '../components/ui/EntryHero.vue';
import { useConfigStore } from '../stores/config';

const configStore = useConfigStore();
const contracts = ref([]);
const loading = ref(true);
const error = ref('');
const viewMode = ref('grid');
const showAlert = inject('showAlert', null);

const searchQuery = ref('');
const selectedLocation = ref('');
const selectedStatus = ref('');
const budgetMin = ref(null);
const budgetMax = ref(null);
const sortBy = ref('');

let searchTimeout = null;

const hasActiveFilters = computed(() => {
  return searchQuery.value || selectedLocation.value || selectedStatus.value || budgetMin.value || budgetMax.value || sortBy.value;
});

const activeFilterCount = computed(() => {
  return [
    searchQuery.value,
    selectedLocation.value,
    selectedStatus.value,
    budgetMin.value,
    budgetMax.value,
    sortBy.value
  ].filter((value) => value !== '' && value !== null && value !== undefined).length;
});

async function fetchContracts() {
  loading.value = true;
  error.value = '';
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    if (selectedLocation.value) params.location = selectedLocation.value;
    if (selectedStatus.value) params.status = selectedStatus.value;
    if (budgetMin.value) params.budget_min = budgetMin.value;
    if (budgetMax.value) params.budget_max = budgetMax.value;
    if (sortBy.value) params.sort_by = sortBy.value;

    const res = await api.get('/v2/contracts/', { params });
    contracts.value = res.data.results || res.data;
  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.detail || 'The procurement marketplace is temporarily unavailable.';
    showAlert?.('Unable to load contracts right now.', 'error');
  } finally {
    loading.value = false;
  }
}

function debouncedSearch() {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchContracts();
  }, 500);
}

function clearFilters() {
  searchQuery.value = '';
  selectedLocation.value = '';
  selectedStatus.value = '';
  budgetMin.value = null;
  budgetMax.value = null;
  sortBy.value = '';
  fetchContracts();
}

function getContractStatusVariant(status) {
  if (status === 'POSTED') return 'info';
  if (status === 'BIDDING') return 'warning';
  if (status === 'AWARDED') return 'success';
  if (status === 'COMPLETED') return 'success';
  return 'secondary';
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatBudget(contract) {
  if (contract.budget_min && contract.budget_max) {
    return `${configStore.formatPrice(contract.budget_min)} - ${configStore.formatPrice(contract.budget_max)}`;
  }
  if (contract.budget_max) return `Up to ${configStore.formatPrice(contract.budget_max)}`;
  if (contract.budget_min) return `From ${configStore.formatPrice(contract.budget_min)}`;
  return 'Budget on request';
}

onMounted(() => {
  fetchContracts();
});
</script>

<style scoped>
.pz-marketplace {
  background-color: var(--pz-color-limestone-white);
  min-height: 100vh;
}

.pz-results-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--pz-space-4);
  margin-bottom: var(--pz-space-6);
}

.pz-results-strip__metric {
  padding: var(--pz-space-4);
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--pz-shadow-offset-sm);
}

.pz-results-strip__label {
  display: block;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
}

.pz-results-strip__value {
  display: block;
  margin-top: 0.45rem;
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

.pz-state-panel {
  padding: var(--pz-space-8);
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--pz-shadow-offset-md);
}

.pz-state-panel--error {
  border-left: 4px solid var(--pz-color-danger);
}

.pz-state-panel__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
  text-transform: uppercase;
}

.pz-state-panel__title {
  margin: 0.65rem 0 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.3rem, 2vw, 1.7rem);
  letter-spacing: -0.03em;
}

.pz-state-panel__body {
  max-width: 44rem;
  margin: 0.75rem 0 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .pz-results-strip {
    grid-template-columns: 1fr;
  }
}
</style>
