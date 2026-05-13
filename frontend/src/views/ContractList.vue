<template>
  <div class="pz-contract-list-page">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Search tenders"
      placeholder="Search by scope, title, location, or owner"
      search-label="Search Tenders"
      @submit="fetchContracts"
    >
      <template #actions>
        <Button variant="outline" size="sm" @click="mobileFiltersOpen = true">Filters</Button>
      </template>
    </EntryHero>

    <main id="contract-market" class="pz-contract-market-shell">
      <aside class="pz-market-sidebar u-hide-mobile">
        <div class="pz-filter-rail">
          <div class="pz-filter-rail__header">
            <div>
              <div class="pz-filter-rail__eyebrow">Filter Results</div>
              <h3 class="pz-filter-rail__title">Refine Contracts</h3>
            </div>
            <Button v-if="hasActiveFilters" variant="ghost" size="sm" @click="clearFilters">Reset</Button>
          </div>

          <div class="pz-filter-section">
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
              <span class="pz-filter-bar__label">Country</span>
              <select v-model="selectedCountry" @change="fetchContracts" class="pz-filter-bar__control">
                <option value="">All Countries</option>
                <option v-for="c in configStore.countries" :key="c.id" :value="c.iso_code">{{ c.flag_emoji }} {{ c.name }}</option>
              </select>
            </div>
          </div>

          <div class="pz-filter-section">
            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">CapEx Range ({{ configStore.activeCurrency.symbol || '$' }})</span>
              <div class="pz-filter-range">
                <input v-model.number="budgetMin" type="number" placeholder="Min" class="pz-filter-bar__input" @change="fetchContracts">
                <input v-model.number="budgetMax" type="number" placeholder="Max" class="pz-filter-bar__input" @change="fetchContracts">
              </div>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Sort By</span>
              <select v-model="sortBy" @change="fetchContracts" class="pz-filter-bar__control">
                <option value="">Latest</option>
                <option value="budget_max">High Budget</option>
                <option value="-budget_max">Low Budget</option>
              </select>
            </div>
          </div>

          <div class="pz-filter-rail__toggles">
            <div class="pz-filter-chip-shelf">
              <button type="button" class="pz-nav__pill" :class="{ 'pz-nav__pill--active': viewMode === 'grid' }" @click="viewMode = 'grid'">Grid</button>
              <button type="button" class="pz-nav__pill" :class="{ 'pz-nav__pill--active': viewMode === 'list' }" @click="viewMode = 'list'">List</button>
            </div>
            <Button variant="ghost" size="sm" @click="clearFilters">Clear Filters</Button>
          </div>
        </div>
      </aside>

      <section class="pz-market-results">
        <div class="pz-results-header">
          <div>
            <div class="pz-u-text-display text-lg">Contract discovery</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">
              {{ contracts.length }} tenders • {{ activeFilterCount }} active filters
            </div>
          </div>
          <div class="pz-results-header__actions">
            <Button class="u-show-mobile" variant="outline" size="sm" @click="mobileFiltersOpen = true">Filters</Button>
            <div class="pz-view-switcher u-hide-mobile">
              <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }" @click="viewMode = 'grid'">⣿</button>
              <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }" @click="viewMode = 'list'">≡</button>
            </div>
          </div>
        </div>

        <div v-if="activeFilterChips.length" class="pz-filter-chips">
          <div class="pz-filter-chips__scroll">
            <button
              v-for="chip in activeFilterChips"
              :key="`${chip.key}-${chip.value}`"
              type="button"
              class="pz-filter-chip"
              @click="removeFilterChip(chip)"
            >
              <span class="pz-filter-chip__label">{{ chip.label }}</span>
              <span class="pz-filter-chip__value">{{ chip.value }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>
        </div>

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
            <span class="pz-results-strip__label">MARKET_SEGMENT</span>
            <span class="pz-results-strip__value">Construction procurement</span>
          </div>
        </div>

        <div v-if="loading" class="pz-empty-state">
          <div class="pz-status-indicator pz-status-indicator--pulse"></div>
          <p class="pz-u-text-mono text-xs">Loading tenders...</p>
        </div>

        <div v-else-if="error" class="pz-empty-state">
          <p class="pz-u-text-display text-lg">Unable to load tenders</p>
          <p class="pz-u-text-mono text-xs pz-u-color-concrete">{{ error }}</p>
          <Button variant="outline" @click="fetchContracts">Retry</Button>
        </div>

        <div v-else-if="contracts.length === 0" class="pz-empty-state">
          <p class="pz-u-text-display text-lg">No contracts found</p>
          <p class="pz-u-text-mono text-xs pz-u-color-concrete">Try widening your region, status, or budget filters.</p>
          <Button variant="outline" @click="clearFilters">Reset Filters</Button>
        </div>

        <div v-else :class="viewMode === 'grid' ? 'pz-contract-grid' : 'pz-contract-list'">
          <article
            v-for="contract in contracts"
            :key="contract.id"
            class="pz-contract-card"
            :class="{ 'pz-contract-card--list': viewMode === 'list' }"
            @click="$router.push(`/contracts/${contract.id}`)"
          >
            <div class="pz-contract-card__image-wrap">
              <img :src="contract.featured_image_url || '/placeholder.png'" :alt="contract.title || 'Contract brief'" class="pz-contract-card__image" loading="lazy">
              <div class="pz-contract-card__image-badges">
                <span class="pz-contract-card__badge" :class="'pz-contract-card__badge--' + getContractStatusVariant(contract.status)">{{ contract.status || 'POSTED' }}</span>
                <span v-if="contract.category?.name" class="pz-contract-card__badge pz-contract-card__badge--category">{{ contract.category.name }}</span>
              </div>
            </div>

            <div class="pz-contract-card__body">
              <div class="pz-contract-card__eyebrow">{{ contract.location || 'Undisclosed region' }}</div>
              <h3 class="pz-contract-card__title">{{ contract.title || 'Untitled procurement brief' }}</h3>
              <p class="pz-contract-card__lead">{{ contract.description_scope }}</p>

              <div class="pz-contract-card__meta">
                <span class="pz-contract-card__meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  {{ contract.owner_username || 'Project Owner' }}
                </span>
                <span class="pz-contract-card__meta-item">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                  {{ formatDate(contract.created_at) }}
                </span>
              </div>

              <div class="pz-contract-card__details">
                <div class="pz-contract-card__detail">
                  <span>Budget</span>
                  <strong>{{ formatBudget(contract) }}</strong>
                </div>
                <div class="pz-contract-card__detail">
                  <span>Deadline</span>
                  <strong>{{ deadlineLabel(contract.bid_deadline) }}</strong>
                </div>
                <div class="pz-contract-card__detail">
                  <span>Timeline</span>
                  <strong>{{ formatOptionalDate(contract.project_start_date) }} to {{ formatOptionalDate(contract.project_end_date) }}</strong>
                </div>
              </div>

              <div class="pz-contract-card__footer">
                <Button variant="outline" size="sm" @click.stop="$router.push(`/contracts/${contract.id}`)">View Details</Button>
                <Button
                  v-if="contract.status === 'POSTED' || contract.status === 'BIDDING'"
                  variant="primary"
                  size="sm"
                  @click.stop="$router.push(`/contracts/${contract.id}`)"
                >
                  Submit Bid
                </Button>
                <Button
                  v-else
                  variant="outline"
                  size="sm"
                  disabled
                  @click.stop
                >
                  {{ contract.status === 'AWARDED' ? 'Awarded' : 'Closed' }}
                </Button>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>

    <Modal :isOpen="mobileFiltersOpen" title="Refine Contracts" size="lg" @close="mobileFiltersOpen = false">
      <div class="pz-mobile-filter-sheet">
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Tender Status</span>
          <select v-model="selectedStatus" class="pz-filter-bar__control" @change="fetchContracts">
            <option value="">All Visible</option>
            <option value="POSTED">Posted</option>
            <option value="BIDDING">Bidding</option>
            <option value="AWARDED">Awarded</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Country</span>
          <select v-model="selectedCountry" class="pz-filter-bar__control" @change="fetchContracts">
            <option value="">All Countries</option>
            <option v-for="c in configStore.countries" :key="c.id" :value="c.iso_code">{{ c.flag_emoji }} {{ c.name }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">CapEx Range</span>
          <div class="pz-filter-range">
            <input v-model.number="budgetMin" type="number" placeholder="Min" class="pz-filter-bar__input" @change="fetchContracts">
            <input v-model.number="budgetMax" type="number" placeholder="Max" class="pz-filter-bar__input" @change="fetchContracts">
          </div>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Sort By</span>
          <select v-model="sortBy" class="pz-filter-bar__control" @change="fetchContracts">
            <option value="">Latest</option>
            <option value="budget_max">High Budget</option>
            <option value="-budget_max">Low Budget</option>
          </select>
        </div>
      </div>
      <template #footer>
        <Button variant="ghost" @click="clearFilters">Reset</Button>
        <Button variant="primary" @click="mobileFiltersOpen = false">Show Results</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import ContractsService from '../services/contracts';
import Button from '../components/ui/Button.vue';
import EntryHero from '../components/ui/EntryHero.vue';
import Modal from '../components/ui/Modal.vue';
import { useConfigStore } from '../stores/config';

const configStore = useConfigStore();
const contracts = ref([]);
const loading = ref(true);
const error = ref('');
const viewMode = ref('grid');
const mobileFiltersOpen = ref(false);
const showAlert = inject('showAlert', null);

const searchQuery = ref('');
const selectedCountry = ref('');
const selectedStatus = ref('');
const budgetMin = ref(null);
const budgetMax = ref(null);
const sortBy = ref('');

const hasActiveFilters = computed(() => {
  return searchQuery.value || selectedCountry.value || selectedStatus.value || budgetMin.value || budgetMax.value || sortBy.value;
});

const activeFilterCount = computed(() => {
  return [
    searchQuery.value,
    selectedCountry.value,
    selectedStatus.value,
    budgetMin.value,
    budgetMax.value,
    sortBy.value
  ].filter((value) => value !== '' && value !== null && value !== undefined).length;
});

const activeFilterChips = computed(() => {
  const chips = [];
  if (searchQuery.value) chips.push({ key: 'search', label: 'Search', value: searchQuery.value });
  if (selectedStatus.value) chips.push({ key: 'status', label: 'Status', value: selectedStatus.value });
  if (selectedCountry.value) {
    const c = configStore.countries.find(x => String(x.iso_code).toUpperCase() === String(selectedCountry.value).toUpperCase());
    chips.push({ key: 'country', label: 'Country', value: c?.name || selectedCountry.value });
  }
  if (budgetMin.value) chips.push({ key: 'budgetMin', label: 'Min Budget', value: configStore.formatPrice(budgetMin.value, configStore.activeCurrencyCode || 'KES') });
  if (budgetMax.value) chips.push({ key: 'budgetMax', label: 'Max Budget', value: configStore.formatPrice(budgetMax.value, configStore.activeCurrencyCode || 'KES') });
  if (sortBy.value) {
    const label = sortBy.value === 'budget_max' ? 'High Budget' : sortBy.value === '-budget_max' ? 'Low Budget' : sortBy.value;
    chips.push({ key: 'sortBy', label: 'Sort', value: label });
  }
  return chips;
});

async function fetchContracts() {
  loading.value = true;
  error.value = '';
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    params.country = selectedCountry.value || '';
    if (selectedStatus.value) params.status = selectedStatus.value;
    if (budgetMin.value) params.budget_min = budgetMin.value;
    if (budgetMax.value) params.budget_max = budgetMax.value;
    if (sortBy.value) params.sort_by = sortBy.value;

    console.log('[ContractList] fetching with params:', JSON.stringify(params));
    const res = await ContractsService.list(params);
    console.log('[ContractList] received', (res.data.results || res.data || []).length, 'contracts');
    contracts.value = res.data.results || res.data;
  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.detail || 'The procurement marketplace is temporarily unavailable.';
    showAlert?.('Unable to load contracts right now.', 'error');
  } finally {
    loading.value = false;
  }
}

function clearFilters() {
  searchQuery.value = '';
  selectedCountry.value = '';
  selectedStatus.value = '';
  budgetMin.value = null;
  budgetMax.value = null;
  sortBy.value = '';
  fetchContracts();
}

function removeFilterChip(chip) {
  if (chip.key === 'search') searchQuery.value = '';
  if (chip.key === 'status') selectedStatus.value = '';
  if (chip.key === 'country') selectedCountry.value = '';
  if (chip.key === 'budgetMin') budgetMin.value = null;
  if (chip.key === 'budgetMax') budgetMax.value = null;
  if (chip.key === 'sortBy') sortBy.value = '';
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

function formatOptionalDate(dateStr) {
  if (!dateStr) return 'TBD';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatBudget(contract) {
  const currency = contract.currency || 'KES';
  if (contract.budget_min && contract.budget_max) {
    return `${configStore.formatPrice(contract.budget_min, currency)} - ${configStore.formatPrice(contract.budget_max, currency)}`;
  }
  if (contract.budget_max) return `Up to ${configStore.formatPrice(contract.budget_max, currency)}`;
  if (contract.budget_min) return `From ${configStore.formatPrice(contract.budget_min, currency)}`;
  return 'Budget on request';
}

function formatNumber(amount) {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return '0.00';
  return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function deadlineLabel(value) {
  if (!value) return 'Deadline TBD';
  const now = new Date();
  const deadline = new Date(value);
  const diffDays = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
  if (diffDays > 1) return `Closes in ${diffDays} days`;
  if (diffDays === 1) return 'Closes tomorrow';
  if (diffDays === 0) return 'Closes today';
  return `Closed ${Math.abs(diffDays)} days ago`;
}

onMounted(() => {
  fetchContracts();
});
</script>

<style scoped>
.pz-contract-list-page {
  min-height: 100vh;
  background: linear-gradient(180deg, rgba(247, 244, 239, 0.55), rgba(255, 255, 255, 0));
}

.pz-contract-market-shell {
  display: grid;
  grid-template-columns: minmax(18rem, 22rem) minmax(0, 1fr);
  gap: 1.5rem;
  max-width: 92rem;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.pz-market-sidebar {
  position: sticky;
  top: 1.25rem;
  align-self: start;
}

.pz-market-results {
  min-width: 0;
}

.pz-filter-rail {
  display: grid;
  gap: 1rem;
  padding: 1.15rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 10px 28px rgba(10, 10, 15, 0.05);
}

.pz-filter-rail__header,
.pz-results-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
}

.pz-filter-rail__eyebrow,
.pz-filter-bar__label,
.pz-contract-card__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-filter-rail__title {
  margin: 0.3rem 0 0;
  font-family: var(--pz-font-display);
  font-size: 1.2rem;
}

.pz-filter-section {
  display: grid;
  gap: 0.85rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-filter-bar__item {
  display: grid;
  gap: 0.45rem;
}

.pz-filter-bar__control,
.pz-filter-bar__input {
  width: 100%;
  padding: 0.9rem 1rem;
  border-radius: 14px;
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.84);
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
  color: var(--pz-color-foundation-black);
  transition: all 0.2s ease;
}

.pz-filter-bar__control:focus,
.pz-filter-bar__input:focus {
  outline: none;
  border-color: rgba(212, 101, 42, 0.4);
  box-shadow: 0 0 0 2px rgba(212, 101, 42, 0.12);
}

.pz-filter-range {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
}

.pz-filter-rail__toggles {
  display: grid;
  gap: 0.8rem;
  padding-top: 0.25rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-filter-chip-shelf {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pz-nav__pill {
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(250, 249, 245, 0.85);
  border-radius: 999px;
  padding: 0.55rem 0.95rem;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
  cursor: pointer;
}

.pz-nav__pill--active {
  background: rgba(212, 101, 42, 0.12);
  border-color: rgba(212, 101, 42, 0.22);
  color: var(--pz-color-earth-orange);
}

.pz-results-header {
  margin-bottom: 1rem;
}

.pz-results-header__actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.pz-filter-chips {
  margin-bottom: 1rem;
}

.pz-filter-chips__scroll {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.2rem;
  scrollbar-width: none;
}

.pz-filter-chips__scroll::-webkit-scrollbar {
  display: none;
}

.pz-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.65rem 0.85rem;
  border-radius: 999px;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.84);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-structural-steel);
  cursor: pointer;
}

.pz-filter-chip__label {
  color: var(--pz-color-concrete-grey);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.pz-filter-chip__value {
  color: var(--pz-color-foundation-black);
  font-weight: 600;
}

.pz-filter-chip svg {
  width: 0.75rem;
  height: 0.75rem;
}

.pz-results-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  margin-bottom: 1.25rem;
}

.pz-results-strip__metric {
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.84);
  border-radius: 16px;
  box-shadow: 0 1px 2px rgba(10, 10, 15, 0.02);
}

.pz-results-strip__label {
  display: block;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
}

.pz-results-strip__value {
  display: block;
  margin-top: 0.45rem;
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

.pz-empty-state {
  padding: 2rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.88);
  display: grid;
  gap: 0.75rem;
  place-items: start;
}

.pz-status-indicator {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  background: rgba(212, 101, 42, 0.08);
  border: 1px solid rgba(212, 101, 42, 0.18);
}

.pz-status-indicator--pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.08); opacity: 1; }
}

.pz-contract-grid {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(auto-fill, minmax(20.5rem, 1fr));
}

.pz-contract-list {
  display: grid;
  gap: 1rem;
}

.pz-contract-card {
  background: #ffffff;
  border-radius: 22px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(10, 10, 15, 0.06);
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 4px 14px rgba(10, 10, 15, 0.04);
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.pz-contract-card:hover {
  transform: translateY(-5px);
  box-shadow:
    0 10px 26px rgba(10, 10, 15, 0.06),
    0 24px 50px rgba(10, 10, 15, 0.08);
}

.pz-contract-card:hover .pz-contract-card__image {
  transform: scale(1.05);
}

.pz-contract-card--list {
  flex-direction: row;
  align-items: stretch;
}

.pz-contract-card--list .pz-contract-card__image-wrap {
  width: 290px;
  flex-shrink: 0;
  aspect-ratio: 4 / 3;
}

.pz-contract-card--list .pz-contract-card__body {
  flex: 1;
}

.pz-contract-card__image-wrap {
  position: relative;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background: linear-gradient(135deg, #e8e4db, #d4cfc5);
}

.pz-contract-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.55s cubic-bezier(0.4, 0, 0.2, 1);
}

.pz-contract-card__image-badges {
  position: absolute;
  top: 0.85rem;
  left: 0.85rem;
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.pz-contract-card__badge {
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.pz-contract-card__badge--info {
  background: rgba(59, 130, 246, 0.9);
  color: white;
}

.pz-contract-card__badge--warning {
  background: rgba(217, 119, 6, 0.9);
  color: white;
}

.pz-contract-card__badge--success {
  background: rgba(34, 139, 34, 0.9);
  color: white;
}

.pz-contract-card__badge--secondary {
  background: rgba(10, 10, 15, 0.7);
  color: white;
}

.pz-contract-card__badge--category {
  background: rgba(255, 255, 255, 0.88);
  color: var(--pz-color-foundation-black);
}

.pz-contract-card__body {
  padding: 1.25rem 1.5rem 1.5rem;
  display: grid;
  gap: 0.7rem;
  flex: 1;
}

.pz-contract-card__title {
  font-family: var(--pz-font-display);
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--pz-color-foundation-black);
  margin: 0;
  letter-spacing: -0.01em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pz-contract-card__lead {
  margin: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  line-height: 1.6;
  color: var(--pz-color-structural-steel);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pz-contract-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-contract-card__meta-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--pz-color-structural-steel);
  font-size: 0.82rem;
  font-weight: 500;
}

.pz-contract-card__meta-item svg {
  width: 0.9rem;
  height: 0.9rem;
  color: var(--pz-color-concrete-grey);
  flex-shrink: 0;
}

.pz-contract-card__details {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}

.pz-contract-card__detail {
  padding: 0.85rem 0.9rem;
  border-radius: 14px;
  background: rgba(250, 249, 245, 0.78);
  border: 1px solid rgba(10, 10, 15, 0.06);
  display: grid;
  gap: 0.2rem;
}

.pz-contract-card__detail span {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-card__detail strong {
  font-family: var(--pz-font-display);
  font-size: 0.92rem;
}

.pz-contract-card__footer {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: auto;
  padding-top: 0.75rem;
}

.pz-mobile-filter-sheet {
  display: grid;
  gap: 1rem;
}

@media (max-width: 1024px) {
  .pz-contract-market-shell {
    grid-template-columns: 1fr;
  }

  .pz-market-sidebar {
    position: static;
  }

  .pz-contract-grid {
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  }
}

@media (max-width: 768px) {
  .pz-contract-market-shell {
    padding: 1.25rem 1rem 3rem;
  }

  .pz-results-strip,
  .pz-contract-card__details {
    grid-template-columns: 1fr;
  }

  .pz-results-header {
    flex-direction: column;
  }

  .pz-contract-card--list {
    flex-direction: column;
  }

  .pz-contract-card--list .pz-contract-card__image-wrap {
    width: 100%;
    aspect-ratio: 3 / 2;
  }
}
</style>
