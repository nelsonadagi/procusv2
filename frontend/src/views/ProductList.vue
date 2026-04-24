<template>
  <div class="pz-marketplace">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Find materials fast"
      :placeholder="searchPlaceholder"
      search-label="Search Materials"
      @submit="submitSearch"
    >
      <template #actions>
        <Button variant="outline" size="sm" @click="scrollToMarket">Filters</Button>
      </template>
    </EntryHero>

    <div id="marketplace" class="pz-marketplace-shell u-mt-12">
      <aside class="pz-marketplace-sidebar u-hide-mobile">
        <div class="pz-filter-rail">
          <div class="pz-filter-rail__header">
            <div>
              <div class="pz-filter-rail__eyebrow">Filter Results</div>
              <h3 class="pz-filter-rail__title">Refine Materials</h3>
            </div>
            <Button v-if="activeFiltersCount > 0" variant="ghost" size="sm" @click="clearFilters">Reset</Button>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Country</span>
            <select v-model="selectedCountry" @change="handleHubChange" class="pz-filter-bar__control">
              <option value="">Global Marketplace</option>
              <option v-for="c in configStore.countries" :key="c.id" :value="c.id">{{ c.flag_emoji }} {{ c.name }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Material Category</span>
            <select v-model="selectedCategory" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">All Industrial Materials</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Certification</span>
            <input v-model.trim="certificationQuery" type="text" placeholder="KEBS, ISO 9001, CE" class="pz-filter-bar__input" @input="debouncedSearch">
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Country of Origin</span>
            <input v-model.trim="originQuery" type="text" placeholder="Kenya, Tanzania, China" class="pz-filter-bar__input" @input="debouncedSearch">
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">County / State</span>
            <select v-model="selectedCounty" @change="handleCountyChange" class="pz-filter-bar__control">
              <option value="">All Counties</option>
              <option v-for="c in availableCounties" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Subcounty / City</span>
            <select v-model="selectedSubcounty" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">All Areas</option>
              <option v-for="s in availableSubcounties" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Price Range ($)</span>
            <div class="pz-filter-range">
              <input v-model.number="priceMin" type="number" placeholder="Min" class="pz-filter-bar__input" @change="fetchProducts">
              <input v-model.number="priceMax" type="number" placeholder="Max" class="pz-filter-bar__input" @change="fetchProducts">
            </div>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Sort By</span>
            <select v-model="sortBy" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">Standard</option>
              <option value="base_price">Lowest Price</option>
              <option value="-base_price">Highest Price</option>
              <option value="-created_at">Newest Arrivals</option>
              <option value="distance" v-if="userCoords">Nearest To Me</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Radius (KM)</span>
            <select v-model="selectedRadius" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">Any distance</option>
              <option value="5">5 KM</option>
              <option value="10">10 KM</option>
              <option value="25">25 KM</option>
              <option value="50">50 KM</option>
              <option value="100">100 KM</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Inventory Status</span>
            <select v-model="inventorySignal" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">All stock states</option>
              <option value="IN_STOCK">In Stock</option>
              <option value="LOW_STOCK">Low Stock</option>
              <option value="OUT_OF_STOCK">Out of Stock</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Delivery Region</span>
            <select v-model="deliveryRegion" @change="fetchProducts" class="pz-filter-bar__control">
              <option value="">Any delivery region</option>
              <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
            </select>
          </div>

          <div class="pz-filter-rail__toggles">
            <label class="pz-filter-toggle">
              <input v-model="inStockOnly" type="checkbox" @change="fetchProducts">
              <span>In Stock Only</span>
            </label>
            <label class="pz-filter-toggle">
              <input v-model="verifiedOnly" type="checkbox" @change="fetchProducts">
              <span>Verified Suppliers</span>
            </label>
          </div>
        </div>
      </aside>

      <section class="pz-marketplace-results">
        <div class="quote-ticker u-mb-8">
        <span class="quote-ticker__label">LATEST ACTIVITY:</span>
        <span class="quote-ticker__text">15 quotes confirmed in the last hour • 85% Vendor response rate today •
          Nairobi
          Depot restocked 500 tons of Simba Cement</span>
        </div>

        <main class="marketplace-main">
        <!-- Controls Bar -->
        <div class="marketplace-controls" v-if="totalProducts > 0">
          <div class="marketplace-controls__summary">
            <div class="u-text-sm color-muted">
              Found <span class="u-font-bold color-main">{{ totalProducts }}</span> products
            </div>
            <div class="pz-marketplace-results__meta">
              <span>{{ activeFiltersCount }} active filters</span>
            </div>
          </div>
          <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
            <Button class="u-show-mobile" variant="outline" size="sm" @click="mobileFiltersOpen = true">Filters</Button>
            <div class="pz-view-switcher u-hide-mobile">
              <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }" @click="viewMode = 'grid'">⣿</button>
              <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }" @click="viewMode = 'list'">≡</button>
            </div>
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

              <div class="pz-premium-card__location u-mb-2">
                <span class="pz-u-text-mono text-xs pz-u-color-steel">
                  📍 {{ product.vendor_location }}, {{ product.vendor_country_name }}
                </span>
              </div>

              <h4 class="pz-premium-card__title">{{ product.name }}</h4>

              <div class="pz-premium-card__specs">
                <span class="pz-spec-dot">GRADE: {{ product.quality_grade || 'A+' }}</span>
                <span class="pz-spec-dot">STOCK: {{ product.inventory_signal === 'LOW_STOCK' ? 'LOW' : product.stock_quantity > 0 ? 'READY' : 'PRE' }}</span>
                <span v-if="product.country_of_origin" class="pz-spec-dot">ORIGIN: {{ product.country_of_origin }}</span>
              </div>

              <div v-if="product.attribute_highlights?.length" class="pz-u-text-mono text-xs pz-u-color-steel u-mb-3">
                {{ product.attribute_highlights[0]?.name }}: {{ product.attribute_highlights[0]?.value }}{{ product.attribute_highlights[0]?.unit ? ` ${product.attribute_highlights[0].unit}` : '' }}
              </div>

              <div v-if="product.certification_highlights?.length" class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-2 u-mb-3">
                <Badge v-for="cert in product.certification_highlights" :key="cert" variant="success" size="small">{{ cert }}</Badge>
              </div>

              <div class="pz-premium-card__pricing">
                <div class="pz-price-display">
                  <span class="pz-price-display__val">{{ configStore.formatPrice(product.base_price) }}</span>
                  <span class="pz-price-display__unit">/{{ product.unit }}</span>
                </div>
                <Button variant="primary" size="sm" @click.stop="requestQuote(product)">
                  GET QUOTE
                </Button>
              </div>
            </div>
          </article>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && productList.length === 0" class="pz-card pz-p-12 pz-u-text-center">
          <div class="u-text-4xl u-mb-4">🔍</div>
          <h3 class="pz-u-text-display text-lg">NO PRODUCTS FOUND</h3>
          <p class="pz-u-text-mono text-xs pz-u-color-steel u-mb-8">TRY CHANGING YOUR SEARCH FILTERS</p>
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
      </section>
    </div>

    <Button class="pz-mobile-filter-trigger u-show-mobile" variant="primary" size="lg" pill @click="mobileFiltersOpen = true">
      Filters
    </Button>

    <Modal :isOpen="mobileFiltersOpen" title="Refine Materials" size="lg" @close="mobileFiltersOpen = false">
      <div class="pz-mobile-filter-sheet">
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Country</span>
          <select v-model="selectedCountry" @change="handleHubChange" class="pz-filter-bar__control">
            <option value="">Global Marketplace</option>
            <option v-for="c in configStore.countries" :key="c.id" :value="c.id">{{ c.flag_emoji }} {{ c.name }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Material Category</span>
          <select v-model="selectedCategory" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">All Industrial Materials</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Certification</span>
          <input v-model.trim="certificationQuery" type="text" placeholder="KEBS, ISO 9001, CE" class="pz-filter-bar__input" @input="debouncedSearch">
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Country of Origin</span>
          <input v-model.trim="originQuery" type="text" placeholder="Kenya, Tanzania, China" class="pz-filter-bar__input" @input="debouncedSearch">
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">County / State</span>
          <select v-model="selectedCounty" @change="handleCountyChange" class="pz-filter-bar__control">
            <option value="">All Counties</option>
            <option v-for="c in availableCounties" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Subcounty / City</span>
          <select v-model="selectedSubcounty" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">All Areas</option>
            <option v-for="s in availableSubcounties" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Price Range ($)</span>
          <div class="pz-filter-range">
            <input v-model.number="priceMin" type="number" placeholder="Min" class="pz-filter-bar__input" @change="fetchProducts">
            <input v-model.number="priceMax" type="number" placeholder="Max" class="pz-filter-bar__input" @change="fetchProducts">
          </div>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Sort By</span>
          <select v-model="sortBy" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">Standard</option>
            <option value="base_price">Lowest Price</option>
            <option value="-base_price">Highest Price</option>
            <option value="-created_at">Newest Arrivals</option>
            <option value="distance" v-if="userCoords">Nearest To Me</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Radius (KM)</span>
          <select v-model="selectedRadius" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">Any distance</option>
            <option value="5">5 KM</option>
            <option value="10">10 KM</option>
            <option value="25">25 KM</option>
            <option value="50">50 KM</option>
            <option value="100">100 KM</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Inventory Status</span>
          <select v-model="inventorySignal" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">All stock states</option>
            <option value="IN_STOCK">In Stock</option>
            <option value="LOW_STOCK">Low Stock</option>
            <option value="OUT_OF_STOCK">Out of Stock</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Delivery Region</span>
          <select v-model="deliveryRegion" @change="fetchProducts" class="pz-filter-bar__control">
            <option value="">Any delivery region</option>
            <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
          </select>
        </div>
        <div class="pz-filter-rail__toggles">
          <label class="pz-filter-toggle">
            <input v-model="inStockOnly" type="checkbox" @change="fetchProducts">
            <span>In Stock Only</span>
          </label>
          <label class="pz-filter-toggle">
            <input v-model="verifiedOnly" type="checkbox" @change="fetchProducts">
            <span>Verified Suppliers</span>
          </label>
        </div>
      </div>
      <template #footer>
        <Button variant="ghost" @click="clearFilters">Reset</Button>
        <Button variant="primary" @click="mobileFiltersOpen = false">Show Results</Button>
      </template>
    </Modal>

    <!-- Comparison Sticky Bar -->
    <div class="pz-compare-bar" :class="{ 'pz-compare-bar--active': selectedForComparison.length > 0 }">
      <div class="pz-l-container pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
          <span class="pz-u-text-mono text-xs">{{ selectedForComparison.length }} SELECTED</span>
          <div class="pz-l-flex pz-l-flex--gap-2 u-hide-mobile">
            <Badge v-for="p in selectedForComparison" :key="p.id" variant="finance"
              @click="toggleProductForComparison(p)">{{ p.name }} ✕</Badge>
          </div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3">
          <Button variant="ghost" size="sm" @click="selectedForComparison = []">DISCARD</Button>
          <Button variant="primary" size="sm">COMPARE PRODUCTS</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, inject } from 'vue';
  import { useRouter } from 'vue-router';
  import { detectUserLocation, getStoredLocation } from '../utils/location';

  const viewMode = ref('grid');
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';
  import { useConfigStore } from '../stores/config';

  // UI Components
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import EntryHero from '../components/ui/EntryHero.vue';
  import Modal from '../components/ui/Modal.vue';

  const router = useRouter();
  const authStore = useAuthStore();
  const configStore = useConfigStore();
  const showAlert = inject('showAlert');

  // Platform Local States
  const searchQuery = ref('');
  const searchMode = ref('materials'); // 'materials', 'vendors', 'categories'
  const selectedCountry = ref('');
  const selectedCounty = ref('');
  const selectedSubcounty = ref('');
  const selectedCategory = ref('');
  const certificationQuery = ref('');
  const originQuery = ref('');
  const inventorySignal = ref('');
  const deliveryRegion = ref('');

  const availableCounties = ref([]);
  const availableSubcounties = ref([]);
  const sortBy = ref('');
  const priceMin = ref(null);
  const priceMax = ref(null);
  const inStockOnly = ref(false);
  const verifiedOnly = ref(false);
  const selectedRadius = ref('');
  const userCoords = ref(getStoredLocation());

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
    if (selectedCountry.value) count++;
    if (selectedCategory.value) count++;
    if (selectedCounty.value) count++;
    if (selectedSubcounty.value) count++;
    if (certificationQuery.value) count++;
    if (originQuery.value) count++;
    if (priceMin.value !== null) count++;
    if (priceMax.value !== null) count++;
    if (inventorySignal.value) count++;
    if (deliveryRegion.value) count++;
    if (inStockOnly.value) count++;
    if (verifiedOnly.value) count++;
    return count;
  });

  const searchPlaceholder = computed(() => {
    return "Search materials (e.g. 'TMT Bars', 'Simba Cement')...";
  });

  const isSelectedForComparison = (id) => selectedForComparison.value.some(p => p.id === id);

  // Business Logic
  const fetchCategories = async () => {
    try {
      const response = await api.get('/taxonomy/categories/', {
        params: { taxonomy_type: 'MATERIAL' }
      });
      const data = response.data?.results || response.data || [];
      // Filter out any null/undefined items to prevent render crashes
      categories.value = (Array.isArray(data) ? data : []).filter(Boolean);
    } catch (err) { console.error(err); }
  };

  const fetchLocations = async () => {
    try {
      const params = { country: selectedCountry.value || undefined };
      const res = await api.get('/v1/products/locations/', { params });
      availableCounties.value = res.data.counties || [];
      availableSubcounties.value = res.data.subcounties || [];
    } catch (err) {
      console.error("Failed to fetch location hierarchy", err);
    }
  };

  const fetchProducts = async () => {
    loading.value = true;
    console.log("Initiating product discovery...");
    try {
      const useDistanceAwareSearch = Boolean(selectedRadius.value || sortBy.value === 'distance');
      const params = {
        page: currentPage.value,
        page_size: pageSize,
        search: searchQuery.value || undefined,
        country: selectedCountry.value || undefined,
        category: selectedCategory.value || undefined,
        county: selectedCounty.value || undefined,
        subcounty: selectedSubcounty.value || undefined,
        certification: certificationQuery.value || undefined,
        country_of_origin: originQuery.value || undefined,
        inventory_signal: inventorySignal.value || undefined,
        delivery_region: deliveryRegion.value || undefined,
        ordering: sortBy.value || undefined,
        base_price__gte: priceMin.value || undefined,
        base_price__lte: priceMax.value || undefined,
        is_in_stock: inStockOnly.value || undefined,
        is_verified: verifiedOnly.value || undefined,
        latitude: useDistanceAwareSearch ? userCoords.value?.lat : undefined,
        longitude: useDistanceAwareSearch ? userCoords.value?.lng : undefined,
        radius_km: selectedRadius.value || undefined
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

  const submitSearch = () => {
    currentPage.value = 1;
    fetchProducts();
  };

  const handleProductClick = (product) => {
    router.push(`/products/${product.id}`);
  };

  const requestQuote = async (product) => {
    if (!authStore.isAuthenticated) {
      showAlert('Please sign in to request a quote.', 'info');
      router.push('/login');
      return;
    }
    try {
      await api.post('/orders/quote-requests/', {
        items: [{ product: product.id, quantity: product.min_order_quantity || 1 }]
      });
      showAlert('Quote request sent successfully.', 'success');
      router.push('/buyer/dashboard');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to request quote.', 'error');
    }
  };

  const scrollToMarket = () => {
    document.getElementById('marketplace')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleDetectLocation = async () => {
    try {
      const coords = await detectUserLocation();
      userCoords.value = coords;
      showAlert('Location detected. Distance-aware discovery is now enabled.', 'success');
      fetchProducts();
    } catch (err) {
      showAlert('Please enable location services in your browser to use distance-aware discovery.', 'info');
    }
  };

  const clearFilters = () => {
    searchQuery.value = '';
    selectedCountry.value = '';
    selectedCategory.value = '';
    selectedCounty.value = '';
    selectedSubcounty.value = '';
    certificationQuery.value = '';
    originQuery.value = '';
    priceMin.value = null;
    priceMax.value = null;
    inventorySignal.value = '';
    deliveryRegion.value = '';
    inStockOnly.value = false;
    verifiedOnly.value = false;
    currentPage.value = 1;
    fetchProducts();
  };

  const handleHubChange = () => {
    selectedCounty.value = '';
    selectedSubcounty.value = '';
    currentPage.value = 1;
    fetchLocations();
    fetchProducts();
  };

  const handleCountyChange = () => {
    selectedSubcounty.value = '';
    currentPage.value = 1;
    fetchProducts();
  };

  const toggleProductForComparison = (product) => {
    const idx = selectedForComparison.value.findIndex(p => p.id === product.id);
    if (idx === -1) {
      if (selectedForComparison.value.length < 4) selectedForComparison.value.push(product);
      else showAlert('A maximum of 4 products can be compared at once.', 'info');
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

  onMounted(async () => {
    await configStore.fetchConfig();
    selectedCountry.value = '';
    fetchCategories();
    fetchLocations();
    fetchProducts();
  });
</script>

<style scoped>

  /* Marketplace Specific */
  .pz-marketplace {
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.64), rgba(248, 246, 240, 0.92)),
      radial-gradient(circle at top left, rgba(212, 101, 42, 0.08), transparent 28%);
    min-height: 100vh;
  }

  .pz-marketplace-shell {
    width: 100%;
    margin: 0;
    padding-inline: clamp(1rem, 2vw, 2rem);
  }

  .pz-marketplace-sidebar {
    display: none;
  }

  .pz-marketplace-results {
    min-width: 0;
  }

  .pz-filter-rail {
    position: sticky;
    top: 6.5rem;
    display: grid;
    gap: 1rem;
    padding: 1.15rem;
    background: rgba(255, 255, 255, 0.84);
    border: 1px solid rgba(10, 10, 15, 0.08);
    box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.05);
    backdrop-filter: blur(12px);
  }

  .pz-filter-rail__header {
    display: flex;
    align-items: start;
    justify-content: space-between;
    gap: 1rem;
  }

  .pz-filter-rail__eyebrow,
  .quote-ticker__label {
    font-family: var(--pz-font-mono);
    text-transform: uppercase;
    letter-spacing: 0.18em;
  }

  .pz-filter-rail__eyebrow {
    font-size: 0.64rem;
    color: var(--pz-color-earth-orange);
  }

  .pz-filter-rail__title {
    margin: 0.25rem 0 0;
    font-family: var(--pz-font-display);
    font-size: 1.35rem;
    letter-spacing: -0.04em;
  }

  .pz-filter-range {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.5rem;
  }

  .pz-filter-rail__toggles {
    display: grid;
    gap: 0.75rem;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(10, 10, 15, 0.08);
  }

  .pz-filter-toggle {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.92rem;
    color: var(--pz-color-foundation-black);
  }

  .pz-filter-toggle input {
    width: 18px;
    height: 18px;
    accent-color: var(--pz-color-earth-orange);
  }

  .pz-filter-bar {
    display: grid;
    gap: 1rem;
    padding: 1.15rem;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(10, 10, 15, 0.08);
    box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.06);
    backdrop-filter: blur(10px);
  }

  .pz-filter-bar__item {
    display: grid;
    gap: 0.4rem;
  }

  .pz-filter-bar__label {
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--pz-color-concrete-grey);
  }

  .pz-filter-bar__control,
  .pz-filter-bar__input {
    min-height: 44px;
    padding: 0.7rem 0.85rem;
    border: 1px solid rgba(10, 10, 15, 0.12);
    background: rgba(255, 255, 255, 0.92);
    color: var(--pz-color-foundation-black);
  }

  .pz-filter-bar__control:focus,
  .pz-filter-bar__input:focus {
    outline: 2px solid rgba(212, 101, 42, 0.2);
    border-color: var(--pz-color-earth-orange);
  }

  .quote-ticker {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.95rem 1rem;
    border-left: 3px solid var(--pz-color-earth-orange);
    background: rgba(10, 10, 15, 0.92);
    color: white;
  }

  .quote-ticker__label {
    font-size: 0.64rem;
    color: var(--pz-color-earth-orange);
  }

  .quote-ticker__text {
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.72);
  }

  .marketplace-main {
    padding-bottom: 5rem;
  }

  .marketplace-controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0 0 1rem;
  }

  .marketplace-controls__summary {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
  }

  .pz-marketplace-results__meta {
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--pz-color-concrete-grey);
  }

  .pz-premium-card__rating {
    font-size: 0.75rem;
    font-weight: 700;
  }

  .pz-premium-card__specs {
    display: flex;
    flex-wrap: wrap;
    gap: var(--pz-space-4);
    margin-bottom: var(--pz-space-6);
  }

  .pz-premium-card {
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid rgba(10, 10, 15, 0.08);
    box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
  }

  .pz-premium-card__content {
    padding: 1.15rem;
  }

  .pz-spec-dot {
    font-size: 0.65rem;
    padding: var(--pz-space-1) var(--pz-space-2);
    background: rgba(10, 10, 15, 0.05);
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

  .pz-mobile-filter-sheet {
    display: grid;
    gap: 1rem;
  }

  @media (min-width: 1024px) {
    .pz-marketplace-shell {
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 1.5rem;
      align-items: start;
    }

    .pz-marketplace-sidebar {
      display: block !important;
    }

    .marketplace-main {
      padding-bottom: 3rem;
    }
  }

  @media (max-width: 767px) {
    .pz-marketplace-shell {
      padding: 0 1rem;
    }

    .quote-ticker {
      margin-bottom: 1rem;
    }

    .marketplace-controls {
      align-items: flex-start;
    }

    .pz-mobile-filter-trigger {
      bottom: 1rem;
      right: 1rem;
    }
  }
</style>
