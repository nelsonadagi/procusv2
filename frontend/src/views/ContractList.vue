<template>
  <div class="pz-marketplace">
    <!-- Premium Global Hero -->
    <section class="pz-hero-premium">
      <div class="pz-hero-premium__mesh"></div>
      <div class="pz-l-container pz-hero-premium__content">
        <h1 class="pz-u-text-display pz-hero-premium__title">Procure Major Works & Tenders</h1>
        <p class="pz-hero-premium__subtitle pz-u-text-mono">
          UNIFIED PROCUREMENT • VERIFIED BIDDING • STRATEGIC COMMAND
        </p>

        <!-- Glassmorphism Discovery -->
        <div class="pz-discovery-glass">
          <div class="pz-discovery-glass__input-group">
            <span class="pz-discovery-glass__icon">🔍</span>
            <input v-model="searchQuery" @input="debouncedSearch" type="text" placeholder="DISCOVER OPPORTUNITIES..."
              class="pz-discovery-glass__input">
          </div>
          <Button variant="primary" size="lg" @click="fetchContracts" class="u-hide-mobile">EXECUTE SEARCH</Button>
        </div>

        <div class="pz-hero-premium__stats pz-u-text-mono">
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">{{ contracts.length }}</span>
            <span class="pz-stat-premium__label">ACTIVE TENDERS</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">VERIFIED</span>
            <span class="pz-stat-premium__label">COMMAND</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">{{ selectedLocation || 'GLOBAL' }}</span>
            <span class="pz-stat-premium__label">LOCATION</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content Area -->
    <main class="pz-l-container u-py-12">
      <!-- Unified Discovery Filters -->
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Strategic Sector</span>
            <select v-model="selectedSector" @change="fetchContracts" class="pz-filter-bar__control">
              <option value="">All Sectors</option>
              <option value="Residential">Residential</option>
              <option value="Commercial">Commercial</option>
              <option value="Infrastructure">Infrastructure</option>
              <option value="Industrial">Industrial</option>
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
            <span class="pz-filter-bar__label">CapEx Range ($)</span>
            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-2">
              <input v-model.number="budgetMin" type="number" placeholder="MIN" class="pz-filter-bar__input"
                @change="fetchContracts">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">/</span>
              <input v-model.number="budgetMax" type="number" placeholder="MAX" class="pz-filter-bar__input"
                @change="fetchContracts">
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
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }"
              @click="viewMode = 'grid'">
              ⣿
            </button>
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }"
              @click="viewMode = 'list'">
              ≡
            </button>
          </div>
          <Button v-if="hasActiveFilters" variant="ghost" size="sm" @click="clearFilters">RESET PORTFOLIO</Button>
        </div>
      </div>

      <div class="content-layout">
        <div v-if="loading" class="u-text-center u-py-12">
          <div class="loading-spinner"></div>
          <p class="u-mt-4 u-color-muted">Searching the market...</p>
        </div>

        <div v-else>
          <div v-if="contracts.length === 0" class="empty-state">
            <span class="empty-icon">📂</span>
            <h3>No contracts found</h3>
            <p>Try adjusting your search or filters to see more opportunities.</p>
            <Button variant="outline" @click="clearFilters" class="u-mt-4">Reset All Filters</Button>
          </div>

          <!-- Contracts Listing -->
          <div v-else :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
            <article v-for="contract in contracts" :key="contract.id"
              class="pz-premium-card pz-card--interactive u-hover-spring"
              :class="{ 'pz-premium-card--list': viewMode === 'list' }"
              @click="$router.push(`/contracts/${contract.id}`)">

              <div class="pz-premium-card__media">
                <img :src="contract.featured_image_url || '/placeholder.png'" :alt="contract.title"
                  class="pz-premium-card__img">
                <div class="pz-premium-card__badges">
                  <Badge :variant="getContractStatusVariant(contract.status)">{{ contract.status }}</Badge>
                </div>
              </div>

              <div class="pz-premium-card__content">
                <div class="pz-premium-card__top">
                  <span class="pz-premium-card__vendor">{{ contract.location }}</span>
                  <div class="pz-premium-card__rating">{{ formatDate(contract.created_at) }}</div>
                </div>

                <h3 class="pz-premium-card__title">{{ contract.title }}</h3>

                <div class="pz-premium-card__specs">
                  <span class="pz-spec-dot">ARCHITECT: {{ contract.owner_username }}</span>
                  <span class="pz-spec-dot">SECTOR: {{ contract.sector || 'GENERAL' }}</span>
                </div>

                <div class="pz-premium-card__pricing">
                  <div class="pz-price-display">
                    <span class="pz-price-display__unit">EST. BUDGET</span>
                    <div class="pz-price-display__val">${{ contract.budget_min }} - ${{ contract.budget_max }}</div>
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
  import { ref, computed, onMounted } from 'vue';
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';

  const authStore = useAuthStore();
  const contracts = ref([]);
  const loading = ref(true);
  const viewMode = ref('grid');

  // Search & Filters
  const searchQuery = ref('');
  const selectedLocation = ref('');
  const selectedStatus = ref('');
  const selectedSector = ref(''); // New filter
  const budgetMin = ref(null);
  const budgetMax = ref(null);
  const sortBy = ref(''); // New filter

  let searchTimeout = null;

  const hasActiveFilters = computed(() => {
    return searchQuery.value || selectedLocation.value || selectedStatus.value || selectedSector.value || budgetMin.value || budgetMax.value || sortBy.value;
  });

  async function fetchContracts() {
    loading.value = true;
    try {
      const params = {};
      if (searchQuery.value) params.search = searchQuery.value;
      if (selectedLocation.value) params.location = selectedLocation.value;
      if (selectedStatus.value) params.status = selectedStatus.value;
      if (selectedSector.value) params.sector = selectedSector.value; // Add sector to params
      if (budgetMin.value) params.budget_min = budgetMin.value;
      if (budgetMax.value) params.budget_max = budgetMax.value;
      if (sortBy.value) params.sort_by = sortBy.value; // Add sort_by to params

      const res = await api.get('/v2/contracts/', { params });
      contracts.value = res.data.results || res.data;
    } catch (err) {
      console.error(err);
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
    selectedSector.value = ''; // Reset new filter
    budgetMin.value = null;
    budgetMax.value = null;
    sortBy.value = ''; // Reset new filter
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

  onMounted(() => {
    fetchContracts();
  });
</script>

<style scoped>

  /* Marketplace Specific */
  .pz-marketplace {
    background-color: var(--pz-color-limestone-white);
    min-height: 100vh;
  }
</style>
