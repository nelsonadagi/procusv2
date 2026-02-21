<template>
  <div class="pz-marketplace">
    <!-- Premium Global Hero -->
    <section class="pz-hero-premium">
      <div class="pz-hero-premium__mesh"></div>
      <div class="pz-l-container pz-hero-premium__content">
        <h1 class="pz-u-text-display pz-hero-premium__title">The Operating System for Construction</h1>
        <p class="pz-hero-premium__subtitle pz-u-text-mono">
          UNIFIED COMMERCE • INDUSTRIAL LOGISTICS • PROJECT COMMAND
        </p>

        <!-- Glassmorphism Discovery -->
        <div class="pz-discovery-glass">
          <div class="pz-discovery-glass__input-group">
            <span class="pz-discovery-glass__icon">🔍</span>
            <input v-model="searchQuery" @input="debouncedSearch" type="text" :placeholder="searchPlaceholder"
              class="pz-discovery-glass__input">
          </div>
          <Button variant="primary" size="lg" @click="fetchProducts" class="u-hide-mobile">EXECUTE DISCOVERY</Button>
        </div>

        <div class="pz-hero-premium__stats pz-u-text-mono">
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">50K+</span>
            <span class="pz-stat-premium__label">ASSETS</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">2.5K+</span>
            <span class="pz-stat-premium__label">VENDORS</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">15+</span>
            <span class="pz-stat-premium__label">REGIONS</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Unified Discovery Filters -->
    <div id="marketplace" class="pz-l-container u-mt-12">
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Asset Category</span>
            <select v-model="selectedCategory" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">All Materials</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Deployment Region</span>
            <select v-model="selectedRegion" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">All Regions</option>
              <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Cost Parameters ($)</span>
            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-2">
              <input v-model.number="priceMin" type="number" placeholder="MIN" class="pz-filter-bar__input"
                @change="fetchProducts">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">/</span>
              <input v-model.number="priceMax" type="number" placeholder="MAX" class="pz-filter-bar__input"
                @change="fetchProducts">
            </div>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Asset Sequence</span>
            <select v-model="sortBy" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">Standard</option>
              <option value="base_price">Alpha Cost</option>
              <option value="-base_price">Omega Cost</option>
              <option value="-created_at">Latest Intake</option>
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
          <Button v-if="activeFiltersCount > 0" variant="ghost" size="sm" @click="clearFilters">RESET ({{
            activeFiltersCount }})</Button>
        </div>
      </div>

      <!-- Quote Status Ticker (Social Proof) -->
      <div class="quote-ticker u-mb-8">
        <span class="quote-ticker__label">LATEST ACTIVITY:</span>
        <span class="quote-ticker__text">15 quotes confirmed in the last hour • 85% Vendor response rate today •
          Nairobi
          Depot restocked 500 tons of Simba Cement</span>
      </div>

      <!-- 4. Marketplace Main Panel -->
      <main class="marketplace-main">
        <!-- Controls Bar -->
        <div class="marketplace-controls" v-if="totalProducts > 0">
          <div class="u-text-sm color-muted">
            Found <span class="u-font-bold color-main">{{ totalProducts }}</span> professional-grade materials
          </div>
        </div>

        <!-- Skeletons -->
        <div v-if="loading" class="material-grid">
          <div v-for="n in 6" :key="n" class="material-card material-card--skeleton"></div>
        </div>

        <!-- Material Grid Redesign -->
        <div v-else :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
          <article v-for="product in productList" :key="product.id"
            class="pz-premium-card pz-card--interactive u-hover-spring"
            :class="{ 'pz-premium-card--featured': product.is_featured, 'pz-premium-card--list': viewMode === 'list' }"
            @click="handleProductClick(product)">

            <div class="pz-premium-card__media">
              <img :src="product.primary_image_url || '/placeholder.png'" :alt="product.name"
                class="pz-premium-card__img" loading="lazy">
              <div class="pz-premium-card__badges">
                <Badge v-if="product.certifications" variant="success">CERTIFIED</Badge>
                <Badge v-if="product.is_on_sale" variant="finance">BULK RATE</Badge>
              </div>
            </div>

            <div class="pz-premium-card__content">
              <div class="pz-premium-card__top">
                <span class="pz-premium-card__vendor">{{ product.vendor_business_name }}</span>
                <div class="pz-premium-card__rating">⭐ {{ product.average_rating || '5.0' }}</div>
              </div>

              <h4 class="pz-premium-card__title">{{ product.name }}</h4>

              <div class="pz-premium-card__specs">
                <span class="pz-spec-dot">GRADE: {{ product.quality_grade || 'A+' }}</span>
                <span class="pz-spec-dot">STOCK: {{ product.stock_quantity > 0 ? 'READY' : 'PRE' }}</span>
                <span v-if="product.origin" class="pz-spec-dot">ORIGIN: {{ product.origin }}</span>
              </div>

              <div class="pz-premium-card__pricing">
                <div class="pz-price-display">
                  <span class="pz-price-display__val">${{ product.base_price }}</span>
                  <span class="pz-price-display__unit">/{{ product.unit }}</span>
                </div>
                <Button variant="primary" size="sm" @click.stop="requestQuote(product)">
                  QUICK QUOTE
                </Button>
              </div>
            </div>
          </article>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && productList.length === 0" class="pz-card pz-p-12 pz-u-text-center">
          <div class="u-text-4xl u-mb-4">🔍</div>
          <h3 class="pz-u-text-display text-lg">NO MATCHING ASSETS FOUND</h3>
          <p class="pz-u-text-mono text-xs pz-u-color-steel u-mb-8">RECONFIGURE DISCOVERY PARAMETERS</p>
          <Button variant="outline" @click="clearFilters">RESET ALL FILTERS</Button>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pz-l-flex pz-l-flex--center pz-l-flex--gap-4 u-mt-12">
          <Button variant="outline" size="sm" :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)">PREV</Button>
          <span class="pz-u-text-mono text-sm">SEC {{ currentPage }} / {{ totalPages }}</span>
          <Button variant="outline" size="sm" :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)">NEXT</Button>
        </div>
      </main>
    </div>

    <!-- Mobile Filter Trigger -->
    <Button class="marketplace-filters__toggle" variant="primary" size="lg" pill @click="mobileFiltersOpen = true">
      ⚙️ Filters
    </Button>

    <!-- Comparison Sticky Bar -->
    <div class="pz-compare-bar" :class="{ 'pz-compare-bar--active': selectedForComparison.length > 0 }">
      <div class="pz-l-container pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
          <span class="pz-u-text-mono text-xs">{{ selectedForComparison.length }} ASSETS STAGED</span>
          <div class="pz-l-flex pz-l-flex--gap-2 u-hide-mobile">
            <Badge v-for="p in selectedForComparison" :key="p.id" variant="finance"
              @click="toggleProductForComparison(p)">{{ p.name }} ✕</Badge>
          </div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3">
          <Button variant="ghost" size="sm" @click="selectedForComparison = []">DISCARD</Button>
          <Button variant="primary" size="sm">COMPARE ASSETS</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';

  const viewMode = ref('grid');
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';

  // UI Components
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';

  const router = useRouter();
  const authStore = useAuthStore();

  // Platform Local States
  const searchQuery = ref('');
  const searchMode = ref('materials'); // 'materials', 'vendors', 'categories'
  const selectedCategory = ref('');
  const selectedRegion = ref('');
  const sortBy = ref('');
  const priceMin = ref(null);
  const priceMax = ref(null);
  const inStockOnly = ref(false);
  const verifiedOnly = ref(false);

  const loading = ref(true);
  const productList = ref([]); // Replaced products with productList to avoid confusion with the reactive 'products' ref
  const categories = ref([]);
  const totalProducts = ref(0);
  const currentPage = ref(1);
  const pageSize = 12;
  const mobileFiltersOpen = ref(false);
  const selectedForComparison = ref([]);

  const regions = ['NAIROBI', 'MOMBASA', 'KISUMU', 'NAKURU', 'ELDORET', 'CENTRAL', 'COAST', 'RIFT VALLEY'];

  // Computed Context
  const totalPages = computed(() => Math.ceil(totalProducts.value / pageSize));
  const activeFiltersCount = computed(() => {
    let count = 0;
    if (selectedCategory.value) count++;
    if (selectedRegion.value) count++;
    if (priceMin.value !== null) count++;
    if (priceMax.value !== null) count++;
    if (inStockOnly.value) count++;
    if (verifiedOnly.value) count++;
    return count;
  });

  const searchPlaceholder = computed(() => {
    if (searchMode.value === 'vendors') return "Search for verified vendors (e.g. 'Bamburi Cement')...";
    if (searchMode.value === 'categories') return "Search for material categories (e.g. 'Steel')...";
    return "Search materials (e.g. 'TMT Bars', 'Simba Cement')...";
  });

  const isSelectedForComparison = (id) => selectedForComparison.value.some(p => p.id === id);

  // Business Logic
  const fetchCategories = async () => {
    try {
      const response = await api.get('/taxonomy/categories/');
      const data = response.data?.results || response.data || [];
      // Filter out any null/undefined items to prevent render crashes
      categories.value = (Array.isArray(data) ? data : []).filter(Boolean);
    } catch (err) { console.error(err); }
  };

  const fetchProducts = async () => {
    loading.value = true;
    console.log("Initiating product discovery...");
    try {
      const params = {
        page: currentPage.value,
        page_size: pageSize,
        search: searchQuery.value || undefined,
        category: selectedCategory.value || undefined,
        region: selectedRegion.value || undefined,
        ordering: sortBy.value || undefined,
        base_price__gte: priceMin.value || undefined,
        base_price__lte: priceMax.value || undefined,
        is_in_stock: inStockOnly.value || undefined,
        is_verified: verifiedOnly.value || undefined
      };
      const response = await api.get('/v1/products/', { params });

      // Technical mapping: extract results from DRF paginated response or direct list
      const data = response.data.results || response.data || [];
      const rawList = Array.isArray(data) ? data : (data.results || []);
      // Filter out any null/undefined items to prevent render crashes
      productList.value = rawList.filter(Boolean);
      totalProducts.value = response.data.count || productList.value.length;

      console.log(`Discovery successful. Staged ${productList.value.length} assets.`);
    } catch (err) {
      console.error("Discovery failed critically:", err);
      productList.value = [];
      totalProducts.value = 0;
    }
    finally { loading.value = false; }
  };

  const handleProductClick = (product) => {
    router.push(`/products/${product.id}`);
  };

  const requestQuote = async (product) => {
    if (!authStore.isAuthenticated) {
      alert('Please login to request a quote');
      router.push('/login');
      return;
    }
    try {
      await api.post('/orders/quote-requests/', {
        items: [{ product: product.id, quantity: product.min_order_quantity || 1 }]
      });
      alert('Quote request sent successfully!');
      router.push('/buyer/dashboard');
    } catch (err) {
      alert('Failed to request quote.');
    }
  };

  const scrollToMarket = () => {
    document.getElementById('marketplace')?.scrollIntoView({ behavior: 'smooth' });
  };

  const clearFilters = () => {
    selectedCategory.value = '';
    selectedRegion.value = '';
    priceMin.value = null;
    priceMax.value = null;
    inStockOnly.value = false;
    verifiedOnly.value = false;
    fetchProducts();
  };

  const toggleProductForComparison = (product) => {
    const idx = selectedForComparison.value.findIndex(p => p.id === product.id);
    if (idx === -1) {
      if (selectedForComparison.value.length < 4) selectedForComparison.value.push(product);
      else alert("Maximum 4 products can be compared.");
    } else {
      selectedForComparison.value.splice(idx, 1);
    }
  };

  const changePage = (page) => {
    currentPage.value = page;
    window.scrollTo({ top: 400, behavior: 'smooth' });
    fetchProducts();
  };

  let searchTimeout = null;
  const debouncedSearch = () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      currentPage.value = 1;
      fetchProducts();
    }, 400);
  };

  onMounted(() => {
    fetchCategories();
    fetchProducts();
  });
</script>

<style scoped>

  /* Marketplace Specific */
  .pz-marketplace {
    background-color: #F8FAFC;
    min-height: 100vh;
  }

  .pz-premium-card__rating {
    font-size: 0.75rem;
    font-weight: 700;
  }

  .pz-premium-card__specs {
    display: flex;
    gap: var(--pz-space-4);
    margin-bottom: var(--pz-space-6);
  }

  .pz-spec-dot {
    font-size: 0.65rem;
    padding: var(--pz-space-1) var(--pz-space-2);
    background: #F1F5F9;
    border-radius: 4px;
    color: var(--pz-color-structural-steel);
  }

  .pz-price-display__unit {
    font-size: 0.875rem;
    color: var(--pz-color-concrete-grey);
  }

  .pz-mobile-filter-trigger {
    position: fixed;
    bottom: var(--pz-space-6);
    right: var(--pz-space-6);
    box-shadow: 8px 8px 0 var(--pz-color-foundation-black);
    z-index: 50;
  }
</style>
