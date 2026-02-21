<template>
  <div class="pz-marketplace">
    <!-- Premium Global Hero -->
    <section class="pz-hero-premium">
      <div class="pz-hero-premium__mesh"></div>
      <div class="pz-l-container pz-hero-premium__content">
        <h1 class="pz-u-text-display pz-hero-premium__title">Construction Tenders</h1>
        <p class="pz-hero-premium__subtitle pz-u-text-mono">
          STRATEGIC PROCUREMENT GATEWAY • GOVERNMENT & PRIVATE DEPLOYMENTS
        </p>

        <!-- Glassmorphism Discovery -->
        <div class="pz-discovery-glass">
          <div class="pz-discovery-glass__input-group">
            <span class="pz-discovery-glass__icon">🔍</span>
            <input v-model="searchQuery" type="text" placeholder="PROSPECT TENDER OPPORTUNITIES..."
              class="pz-discovery-glass__input">
          </div>
          <Button variant="primary" size="lg" class="u-hide-mobile">EXECUTE DISCOVERY</Button>
        </div>

        <div class="pz-hero-premium__stats pz-u-text-mono">
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">{{ tenders.length }}</span>
            <span class="pz-stat-premium__label">ACTIVE TENDERS</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">VERIFIED</span>
            <span class="pz-stat-premium__label">COMMAND</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">PAN-REGIONAL</span>
            <span class="pz-stat-premium__label">COVERAGE</span>
          </div>
        </div>
      </div>
    </section>

    <main class="pz-l-container u-py-12">
      <!-- Unified Discovery Filters -->
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Tender Status</span>
            <select v-model="selectedStatus" class="pz-filter-bar__control">
              <option value="">All Tenders</option>
              <option value="OPEN">Open</option>
              <option value="CLOSED">Closed/Bidding</option>
              <option value="AWARDED">Awarded</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Deployment Zone</span>
            <select v-model="selectedLocation" class="pz-filter-bar__control">
              <option value="">All Regions</option>
              <option value="Nairobi">Nairobi</option>
              <option value="Mombasa">Mombasa</option>
              <option value="Kisumu">Kisumu</option>
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
          <Button variant="ghost" size="sm" @click="clearFilters">RESET PARAMETERS</Button>
        </div>
      </div>

      <div v-if="loading" class="pz-l-flex pz-l-flex--center u-py-20 pz-l-flex--column">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">SYNCHRONIZING TENDER REGISTRY...</p>
      </div>

      <div v-else-if="tenders.length > 0" :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
        <div v-for="tender in tenders" :key="tender.id" class="pz-premium-card">
          <div class="pz-premium-card__media">
            <img :src="tender.featured_image_url || '/placeholder.png'" :alt="tender.title"
              class="pz-premium-card__img">
            <div class="pz-premium-card__badges">
              <Badge variant="savanna">{{ tender.status }}</Badge>
            </div>
          </div>
          <div class="pz-premium-card__content">
            <div class="pz-premium-card__top">
              <span class="pz-premium-card__vendor">{{ tender.location }}</span>
              <div class="pz-premium-card__rating">ID_#{{ tender.id }}</div>
            </div>

            <h3 class="pz-premium-card__title">{{ tender.title }}</h3>

            <div class="pz-premium-card__specs">
              <span class="pz-spec-dot">SECTOR: {{ tender.sector || 'INFRA' }}</span>
              <span class="pz-spec-dot">DUE: 48H</span>
            </div>

            <p class="pz-u-text-mono text-xs pz-u-color-concrete u-line-clamp-2 u-mb-6" style="height: 3em;">
              {{ tender.description_scope }}
            </p>

            <div class="pz-premium-card__pricing">
              <div class="pz-price-display">
                <span class="pz-price-display__unit">BUDGET RANGE</span>
                <div class="pz-price-display__val">${{ tender.budget_min }} - ${{ tender.budget_max }}</div>
              </div>
              <Button @click="bid(tender.id)" variant="primary" size="sm">EXECUTE BID</Button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 text-muted">
        No active tenders found matching your criteria.
      </div>
    </main>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  const viewMode = ref('grid');
  import api from '../services/api';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import { useAuthStore } from '../stores/auth';

  const router = useRouter();
  const authStore = useAuthStore();
  const tenders = ref([]);
  const loading = ref(true);
  const searchQuery = ref('');
  const selectedStatus = ref('');
  const selectedLocation = ref('');
  const budgetMin = ref(null);
  const budgetMax = ref(null);

  const clearFilters = () => {
    searchQuery.value = '';
    selectedStatus.value = '';
    selectedLocation.value = '';
    budgetMin.value = null;
    budgetMax.value = null;
  };

  onMounted(async () => {
    try {
      // Fetch contracts with status POSTED or BIDDING
      // Backend ContractViewSet allows listing. 
      // We might need to filter status=POSTED in query params if it returns all.
      const res = await api.get('/contracts/?status=POSTED');
      tenders.value = res.data.results || res.data;
    } catch (err) {
      console.error("Failed to load tenders", err);
    } finally {
      loading.value = false;
    }
  });

  const bid = (id) => {
    if (!authStore.isAuthenticated) {
      router.push('/login?redirect=/tenders');
      return;
    }
    router.push(`/contracts/${id}`);
  };
</script>

<style scoped>
  .u-line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
