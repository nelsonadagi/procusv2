<template>
  <div class="pz-property-list">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Search property"
      placeholder="Search by title, place, feature, or development profile"
      search-label="Search Properties"
      @submit="fetchProperties"
    >
      <template #actions>
        <Button variant="outline" size="sm" @click="scrollToMarket">Filters</Button>
      </template>
    </EntryHero>

    <div id="property-market" class="pz-market-shell">
      <aside class="pz-market-sidebar u-hide-mobile">
        <div class="pz-filter-rail">
        <div class="pz-filter-rail__header">
            <div>
              <div class="pz-filter-rail__eyebrow">Filter Results</div>
              <h3 class="pz-filter-rail__title">Refine Properties</h3>
            </div>
            <Button v-if="activeFiltersCount" variant="ghost" size="sm" @click="clearFilters">Reset</Button>
          </div>

          <div class="pz-filter-section">
            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Country</span>
              <select v-model="filters.country" class="pz-filter-bar__control">
                <option value="">All countries</option>
                <option v-for="country in configStore.countries" :key="country.id" :value="country.id">
                  {{ country.flag_emoji }} {{ country.name }}
                </option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Location Search</span>
              <input v-model="filters.location" type="text" placeholder="City, district, or address" class="pz-filter-bar__input">
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Asset Type</span>
              <select v-model="filters.asset_type" class="pz-filter-bar__control">
                <option value="">All asset types</option>
                <option v-for="option in assetTypes" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Property Purpose</span>
              <select v-model="filters.purpose" class="pz-filter-bar__control">
                <option value="">All purposes</option>
                <option v-for="option in purposeOptions" :key="option.id" :value="option.slug">{{ option.name }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Listing Type</span>
              <select v-model="filters.listing_type" class="pz-filter-bar__control">
                <option value="">All listing types</option>
                <option v-for="option in listingTypes" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Development Stage</span>
              <select v-model="filters.development_stage" class="pz-filter-bar__control">
                <option value="">Any stage</option>
                <option v-for="option in developmentStages" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Status</span>
              <select v-model="filters.status" class="pz-filter-bar__control">
                <option value="">Any status</option>
                <option v-for="option in statuses" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>
          </div>

          <div class="pz-filter-section">
            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Bedrooms</span>
              <select v-model="filters.min_bedrooms" class="pz-filter-bar__control">
                <option value="">Any</option>
                <option v-for="count in [1,2,3,4,5]" :key="count" :value="count">{{ count }}+</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Bathrooms</span>
              <select v-model="filters.min_bathrooms" class="pz-filter-bar__control">
                <option value="">Any</option>
                <option v-for="count in [1,2,3,4]" :key="count" :value="count">{{ count }}+</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Occupancy</span>
              <select v-model="filters.occupancy_status" class="pz-filter-bar__control">
                <option value="">Any occupancy</option>
                <option v-for="option in occupancyStatuses" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Condition</span>
              <select v-model="filters.condition_rating" class="pz-filter-bar__control">
                <option value="">Any condition</option>
                <option v-for="option in conditionRatings" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>
          </div>

          <div class="pz-filter-section">
            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Budget Range</span>
              <div class="pz-filter-range">
                <input v-model.number="filters.min_price" type="number" placeholder="Min" class="pz-filter-bar__input">
                <input v-model.number="filters.max_price" type="number" placeholder="Max" class="pz-filter-bar__input">
              </div>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Pricing Strategy</span>
              <select v-model="filters.pricing_strategy" class="pz-filter-bar__control">
                <option value="">Any strategy</option>
                <option v-for="option in pricingStrategies" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Feature Search</span>
              <input v-model="filters.feature" type="text" placeholder="e.g. rooftop, truck access" class="pz-filter-bar__input">
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Sort By</span>
              <select v-model="filters.sort_by" class="pz-filter-bar__control">
                <option value="">Default</option>
                <option value="price">Lowest price</option>
                <option value="-price">Highest price</option>
                <option value="-created_at">Newest listings</option>
                <option value="-bedrooms">Most bedrooms</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Radius (KM)</span>
              <select v-model="filters.radius_km" class="pz-filter-bar__control">
                <option value="">Any distance</option>
                <option value="5">5 KM</option>
                <option value="10">10 KM</option>
                <option value="25">25 KM</option>
                <option value="50">50 KM</option>
              </select>
            </div>
          </div>

          <div class="pz-filter-rail__toggles">
            <label class="pz-filter-toggle">
              <input v-model="onlyFinanceReady" type="checkbox">
              <span>Financing ready</span>
            </label>
            <label class="pz-filter-toggle">
              <input v-model="onlyBuildReady" type="checkbox">
              <span>Build ready</span>
            </label>
            <Button variant="ghost" size="sm" @click="useMyLocation">Use My Location</Button>
          </div>
        </div>
      </aside>

      <section class="pz-market-results">
        <div class="pz-results-header">
          <div>
            <div class="pz-u-text-display text-lg">Property discovery</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">
              {{ filteredProperties.length }} listings • {{ activeFiltersCount }} active filters
            </div>
          </div>
          <div class="pz-results-header__actions">
            <Button class="u-show-mobile" variant="outline" size="sm" @click="mobileFiltersOpen = true">Filters</Button>
            <div class="pz-quick-chips">
              <button
                v-for="type in quickAssetTypes"
                :key="type.value"
                class="pz-nav__pill"
                :class="{ 'pz-nav__pill--active': filters.asset_type === type.value }"
                @click="toggleQuickAssetType(type.value)"
              >
                {{ type.label }}
              </button>
              <button
                v-if="userCoords"
                class="pz-nav__pill"
                :class="{ 'pz-nav__pill--active': !!filters.radius_km }"
                @click="toggleNearby"
              >
                Near Me
              </button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="pz-u-text-center u-py-20">
          <div class="pz-status-indicator pz-status-indicator--pulse"></div>
          <p class="pz-u-text-mono text-xs u-mt-4">Loading properties...</p>
        </div>

        <div v-else-if="filteredProperties.length === 0" class="pz-empty-state">
          <p class="pz-u-text-display text-lg">No properties found</p>
          <p class="pz-u-text-mono text-xs pz-u-color-concrete">Try widening your search or resetting filters.</p>
          <Button variant="outline" @click="clearFilters">Reset Filters</Button>
        </div>

        <div v-else class="pz-results-grid">
          <div
            v-for="prop in filteredProperties"
            :key="prop.id"
            class="pz-admin-card pz-u-transition-spring u-hover-spring"
            @click="viewProperty(prop.id)"
          >
            <div class="pz-admin-card__media">
              <img
                v-if="prop.primary_media?.media_url || prop.primary_media?.external_url"
                :src="prop.primary_media?.media_url || prop.primary_media?.external_url"
                :alt="prop.primary_media?.alt_text || prop.title"
              >
              <div v-else class="pz-admin-card__media-fallback">
                <span>{{ prop.asset_type }}</span>
              </div>
            </div>

            <div class="pz-admin-card__header">
              <Badge variant="ghost" size="sm" class="pz-u-text-mono">{{ readableValue(prop.asset_type) }}</Badge>
              <Badge :variant="prop.status === 'ACTIVE' ? 'success' : 'secondary'">{{ readableValue(prop.status) }}</Badge>
            </div>

            <div class="pz-p-8">
              <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--gap-3 pz-l-flex--align-start">
                <h3 class="pz-u-text-display pz-property-card__title">{{ prop.title }}</h3>
                <span v-if="prop.financing_allowed" class="pz-property-card__finance">Finance Ready</span>
              </div>

              <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-5">
                {{ prop.location_display || prop.location_text || prop.formatted_address || 'Location pending' }}
              </div>

              <div v-if="prop.purpose_name" class="pz-u-text-mono text-xs pz-u-color-earth u-mb-4">
                {{ prop.purpose_name }}
              </div>

              <div class="pz-property-card__price">
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">Commercial Terms</div>
                <div class="pz-u-text-display text-xl">{{ formatNumber(prop.pricing_profile?.asking_price || prop.price_estimate) }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-steel">
                  {{ readableValue(prop.pricing_profile?.pricing_strategy || 'FIXED') }}
                </div>
              </div>

              <div class="pz-property-card__specs">
                <span>{{ prop.specification?.bedrooms || 0 }} bed</span>
                <span>{{ prop.specification?.bathrooms || 0 }} bath</span>
                <span>{{ readableValue(prop.development_metadata?.development_stage || 'NO_STAGE') }}</span>
              </div>

              <div v-if="prop.highlighted_features?.length" class="pz-property-card__features">
                <span v-for="feature in prop.highlighted_features.slice(0, 3)" :key="feature.id">{{ feature.name }}</span>
              </div>

              <div class="pz-property-card__footer">
                <span class="pz-u-text-mono text-xs pz-u-color-savanna">{{ prop.manager_name || prop.owner_name }}</span>
                <Button size="sm" variant="ghost">View Details</Button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <Button class="pz-mobile-filter-trigger u-show-mobile" variant="primary" size="lg" pill @click="mobileFiltersOpen = true">
      Filters
    </Button>

    <Modal :isOpen="mobileFiltersOpen" title="Refine Properties" size="lg" @close="mobileFiltersOpen = false">
      <div class="pz-mobile-filter-sheet">
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Country</span>
          <select v-model="filters.country" class="pz-filter-bar__control">
            <option value="">All countries</option>
            <option v-for="country in configStore.countries" :key="country.id" :value="country.id">
              {{ country.flag_emoji }} {{ country.name }}
            </option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Location Search</span>
          <input v-model="filters.location" type="text" placeholder="City, district, or address" class="pz-filter-bar__input">
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Asset Type</span>
          <select v-model="filters.asset_type" class="pz-filter-bar__control">
            <option value="">All asset types</option>
            <option v-for="option in assetTypes" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Property Purpose</span>
          <select v-model="filters.purpose" class="pz-filter-bar__control">
            <option value="">All purposes</option>
            <option v-for="option in purposeOptions" :key="option.id" :value="option.slug">{{ option.name }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Listing Type</span>
          <select v-model="filters.listing_type" class="pz-filter-bar__control">
            <option value="">All listing types</option>
            <option v-for="option in listingTypes" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Development Stage</span>
          <select v-model="filters.development_stage" class="pz-filter-bar__control">
            <option value="">Any stage</option>
            <option v-for="option in developmentStages" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Budget Range</span>
          <div class="pz-filter-range">
            <input v-model.number="filters.min_price" type="number" placeholder="Min" class="pz-filter-bar__input">
            <input v-model.number="filters.max_price" type="number" placeholder="Max" class="pz-filter-bar__input">
          </div>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Bedrooms</span>
          <select v-model="filters.min_bedrooms" class="pz-filter-bar__control">
            <option value="">Any</option>
            <option v-for="count in [1,2,3,4,5]" :key="count" :value="count">{{ count }}+</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Bathrooms</span>
          <select v-model="filters.min_bathrooms" class="pz-filter-bar__control">
            <option value="">Any</option>
            <option v-for="count in [1,2,3,4]" :key="count" :value="count">{{ count }}+</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Occupancy</span>
          <select v-model="filters.occupancy_status" class="pz-filter-bar__control">
            <option value="">Any occupancy</option>
            <option v-for="option in occupancyStatuses" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Condition</span>
          <select v-model="filters.condition_rating" class="pz-filter-bar__control">
            <option value="">Any condition</option>
            <option v-for="option in conditionRatings" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Pricing Strategy</span>
          <select v-model="filters.pricing_strategy" class="pz-filter-bar__control">
            <option value="">Any strategy</option>
            <option v-for="option in pricingStrategies" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Feature Search</span>
          <input v-model="filters.feature" type="text" placeholder="e.g. terrace, truck access" class="pz-filter-bar__input">
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Sort By</span>
          <select v-model="filters.sort_by" class="pz-filter-bar__control">
            <option value="">Default</option>
            <option value="price">Lowest price</option>
            <option value="-price">Highest price</option>
            <option value="-created_at">Newest listings</option>
            <option value="-bedrooms">Most bedrooms</option>
          </select>
        </div>
        <div class="pz-filter-bar__item">
          <span class="pz-filter-bar__label">Radius (KM)</span>
          <select v-model="filters.radius_km" class="pz-filter-bar__control">
            <option value="">Any distance</option>
            <option value="5">5 KM</option>
            <option value="10">10 KM</option>
            <option value="25">25 KM</option>
            <option value="50">50 KM</option>
          </select>
        </div>
        <div class="pz-filter-rail__toggles">
          <label class="pz-filter-toggle">
            <input v-model="onlyFinanceReady" type="checkbox">
            <span>Financing ready</span>
          </label>
          <label class="pz-filter-toggle">
            <input v-model="onlyBuildReady" type="checkbox">
            <span>Build ready</span>
          </label>
          <Button variant="ghost" size="sm" @click="useMyLocation">Use My Location</Button>
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
import { computed, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import EntryHero from '../components/ui/EntryHero.vue';
import Modal from '../components/ui/Modal.vue';
import { useConfigStore } from '../stores/config';
import { detectUserLocation, getStoredLocation } from '../utils/location';

const configStore = useConfigStore();
const router = useRouter();

const properties = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const mobileFiltersOpen = ref(false);
const onlyFinanceReady = ref(false);
const onlyBuildReady = ref(false);
const lastRequestId = ref(0);
const userCoords = ref(getStoredLocation());
const purposeTree = ref([]);

const filters = ref({
  asset_type: '',
  purpose: '',
  country: '',
  location: '',
  listing_type: '',
  development_stage: '',
  status: '',
  min_bedrooms: '',
  min_bathrooms: '',
  occupancy_status: '',
  condition_rating: '',
  min_price: '',
  max_price: '',
  pricing_strategy: '',
  feature: '',
  sort_by: '',
  radius_km: '',
});

const assetTypes = [
  { label: 'Land', value: 'LAND' },
  { label: 'Residential', value: 'RESIDENTIAL' },
  { label: 'Commercial', value: 'COMMERCIAL' },
  { label: 'Industrial', value: 'INDUSTRIAL' },
  { label: 'Mixed Use', value: 'MIXED_USE' },
  { label: 'Hospitality', value: 'HOSPITALITY' },
  { label: 'Renovation', value: 'RENOVATION' },
  { label: 'Special Purpose', value: 'SPECIAL_PURPOSE' },
];

const quickAssetTypes = assetTypes.slice(0, 5);
const purposeOptions = computed(() => purposeTree.value.flatMap((node) => [node, ...(node.children || [])]));

const listingTypes = [
  { label: 'Sale', value: 'SALE' },
  { label: 'Lease', value: 'LEASE' },
  { label: 'Development Opportunity', value: 'DEVELOPMENT_OPPORTUNITY' },
  { label: 'Completed Project', value: 'COMPLETED_PROJECT' },
];

const developmentStages = [
  { label: 'Raw Land', value: 'RAW_LAND' },
  { label: 'Serviced Site', value: 'SERVICED_SITE' },
  { label: 'In Design', value: 'IN_DESIGN' },
  { label: 'In Progress', value: 'IN_PROGRESS' },
  { label: 'Completed', value: 'COMPLETED' },
];

const statuses = [
  { label: 'Active', value: 'ACTIVE' },
  { label: 'Draft', value: 'DRAFT' },
  { label: 'Under Offer', value: 'UNDER_OFFER' },
  { label: 'Sold', value: 'SOLD' },
  { label: 'Leased', value: 'LEASED' },
  { label: 'Inactive', value: 'INACTIVE' },
];

const occupancyStatuses = [
  { label: 'Vacant', value: 'VACANT' },
  { label: 'Occupied', value: 'OCCUPIED' },
  { label: 'Owner Occupied', value: 'OWNER_OCCUPIED' },
  { label: 'Tenanted', value: 'TENANTED' },
  { label: 'Under Construction', value: 'UNDER_CONSTRUCTION' },
];

const conditionRatings = [
  { label: 'Shell', value: 'SHELL' },
  { label: 'Fair', value: 'FAIR' },
  { label: 'Good', value: 'GOOD' },
  { label: 'Excellent', value: 'EXCELLENT' },
];

const pricingStrategies = [
  { label: 'Fixed', value: 'FIXED' },
  { label: 'Negotiable', value: 'NEGOTIABLE' },
  { label: 'Price On Application', value: 'PRICE_ON_APPLICATION' },
  { label: 'Per Unit', value: 'PER_UNIT' },
];

const filteredProperties = computed(() => properties.value);

const activeFiltersCount = computed(() => {
  let count = searchQuery.value ? 1 : 0;
  Object.values(filters.value).forEach((value) => {
    if (value !== '' && value !== null && value !== undefined) count += 1;
  });
  if (onlyFinanceReady.value) count += 1;
  if (onlyBuildReady.value) count += 1;
  return count;
});

function formatNumber(num) {
  return configStore.formatPrice(num);
}

function readableValue(value) {
  return String(value || '').replaceAll('_', ' ');
}

function buildParams() {
  const params = {};
  if (searchQuery.value) params.search = searchQuery.value;
  Object.entries(filters.value).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      params[key] = value;
    }
  });
  if (onlyFinanceReady.value) params.financing_allowed = true;
  if (onlyBuildReady.value) params.build_ready = true;
  if (filters.value.radius_km && userCoords.value?.lat && userCoords.value?.lng) {
    params.latitude = userCoords.value.lat;
    params.longitude = userCoords.value.lng;
  }
  return params;
}

async function fetchProperties() {
  const requestId = ++lastRequestId.value;
  loading.value = true;
  try {
    const response = await api.get('/property/', { params: buildParams() });
    if (requestId !== lastRequestId.value) return;
    properties.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to fetch properties', err);
  } finally {
    if (requestId === lastRequestId.value) {
      loading.value = false;
    }
  }
}

async function fetchPurposes() {
  try {
    const response = await api.get('/taxonomy/categories/', {
      params: { taxonomy_type: 'PROPERTY', tree: true },
    });
    const all = response.data.results || response.data || [];
    purposeTree.value = all.filter((item) => item.slug !== 'property-listing-types');
  } catch (error) {
    console.error('Failed to fetch property taxonomy', error);
  }
}

function clearFilters() {
  searchQuery.value = '';
  onlyFinanceReady.value = false;
  onlyBuildReady.value = false;
  filters.value = {
    asset_type: '',
    purpose: '',
    country: '',
    location: '',
    listing_type: '',
    development_stage: '',
    status: '',
    min_bedrooms: '',
    min_bathrooms: '',
    occupancy_status: '',
    condition_rating: '',
    min_price: '',
    max_price: '',
    pricing_strategy: '',
    feature: '',
    sort_by: '',
    radius_km: '',
  };
}

function viewProperty(id) {
  router.push(`/properties/${id}`);
}

function toggleQuickAssetType(value) {
  filters.value.asset_type = filters.value.asset_type === value ? '' : value;
}

function toggleNearby() {
  filters.value.radius_km = filters.value.radius_km ? '' : '25';
}

function scrollToMarket() {
  document.getElementById('property-market')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function useMyLocation() {
  try {
    userCoords.value = await detectUserLocation();
    if (!filters.value.radius_km) {
      filters.value.radius_km = '25';
    }
  } catch (error) {
    console.error('Failed to detect location', error);
  }
}

let debounceHandle = null;
watch(
  [searchQuery, filters, onlyFinanceReady, onlyBuildReady],
  () => {
    if (debounceHandle) window.clearTimeout(debounceHandle);
    debounceHandle = window.setTimeout(() => {
      fetchProperties();
    }, 250);
  },
  { deep: true }
);

onMounted(async () => {
  if (!configStore.countries.length) {
    await configStore.fetchConfig();
  }
  await Promise.all([fetchPurposes(), fetchProperties()]);
});
</script>

<style scoped>
.pz-property-list {
  background-color: var(--pz-color-limestone-white);
  min-height: 100vh;
}

.pz-market-shell {
  display: grid;
  gap: 2rem;
  grid-template-columns: minmax(17rem, 21rem) minmax(0, 1fr);
  width: 100%;
  margin: 2rem 0 0;
  padding: 0 clamp(1rem, 2vw, 2rem) 4rem;
}

.pz-market-sidebar {
  position: sticky;
  top: 1rem;
  align-self: start;
}

.pz-filter-rail {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(12px);
}

.pz-filter-rail__header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: start;
}

.pz-filter-rail__eyebrow,
.pz-filter-bar__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-filter-rail__title {
  margin: 0.25rem 0 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

.pz-filter-section,
.pz-mobile-filter-sheet {
  display: grid;
  gap: 0.9rem;
}

.pz-filter-bar__item {
  display: grid;
  gap: 0.45rem;
}

.pz-filter-bar__control,
.pz-filter-bar__input {
  min-height: 2.85rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: white;
  padding: 0 0.85rem;
  width: 100%;
}

.pz-filter-range {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pz-filter-rail__toggles {
  display: grid;
  gap: 0.7rem;
}

.pz-filter-toggle {
  display: flex;
  gap: 0.7rem;
  align-items: center;
  min-height: 2.85rem;
  padding: 0 0.85rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.pz-market-results {
  display: grid;
  gap: 1.5rem;
}

.pz-results-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  padding: 0.25rem 0;
}

.pz-results-header__actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pz-quick-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.pz-results-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
}

.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.pz-admin-card:hover {
  box-shadow: 12px 12px 0 var(--pz-color-foundation-black);
  transform: translate(-4px, -4px);
}

.pz-admin-card__media {
  height: 13rem;
  background: #ece7de;
}

.pz-admin-card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.pz-admin-card__media-fallback {
  height: 100%;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #1f1f1c, #5b5148);
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pz-property-card__title {
  font-size: 1.3rem;
  line-height: 1.1;
  margin: 0 0 0.25rem;
}

.pz-property-card__finance {
  padding: 0.35rem 0.5rem;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.2);
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  white-space: nowrap;
}

.pz-property-card__price {
  display: grid;
  gap: 0.2rem;
  padding: 0.9rem 1rem;
  background: var(--pz-color-limestone-white);
  border-left: 3px solid var(--pz-color-earth-orange);
  margin-bottom: 1rem;
}

.pz-property-card__features,
.pz-property-card__specs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.pz-property-card__features span,
.pz-property-card__specs span {
  padding: 0.35rem 0.55rem;
  background: rgba(199, 134, 74, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.06);
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.pz-property-card__footer {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: center;
}

.pz-empty-state {
  display: grid;
  gap: 0.85rem;
  place-items: center;
  padding: 4rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  text-align: center;
}

.pz-mobile-filter-trigger {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  z-index: 30;
}

@media (max-width: 1024px) {
  .pz-market-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .pz-results-header,
  .pz-results-header__actions,
  .pz-property-card__footer {
    flex-direction: column;
    align-items: stretch;
  }

  .pz-filter-range {
    grid-template-columns: 1fr;
  }
}
</style>
