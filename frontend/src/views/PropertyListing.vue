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
                <option v-for="country in configStore.countries" :key="country.id" :value="country.iso_code">
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
              <span class="pz-filter-bar__label">Budget Range ({{ configStore.activeCurrencyCode || 'KES' }})</span>
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
            <div class="pz-u-text-mono text-[10px] pz-u-color-steel">
              Prices are shown in {{ configStore.activeCurrencyCode || 'KES' }} for the selected country.
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
            class="pz-property-card"
            @click="viewProperty(prop.id)"
          >
            <!-- Image Section -->
            <div class="pz-property-card__image-wrap">
              <img
                v-if="prop.primary_media?.media_url || prop.primary_media?.external_url"
                :src="prop.primary_media?.media_url || prop.primary_media?.external_url"
                :alt="prop.primary_media?.alt_text || prop.title"
                class="pz-property-card__image"
                loading="lazy"
              >
              <div v-else class="pz-property-card__image-fallback">
                <span>{{ readableValue(prop.asset_type) }}</span>
              </div>

              <!-- Image Overlays -->
              <div class="pz-property-card__image-badges">
                <span class="pz-property-card__badge pz-property-card__badge--type">{{ readableValue(prop.asset_type) }}</span>
                <span
                  class="pz-property-card__badge"
                  :class="prop.status === 'ACTIVE' ? 'pz-property-card__badge--active' : 'pz-property-card__badge--status'"
                >
                  {{ readableValue(prop.status) }}
                </span>
              </div>

              <button
                type="button"
                class="pz-property-card__fav"
                @click.stop
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              </button>
            </div>

            <!-- Content Section -->
            <div class="pz-property-card__body">
              <!-- Price Row -->
              <div class="pz-property-card__price-row">
                <div class="pz-property-card__price">
                  {{ formatNumber(prop.pricing_profile?.asking_price || prop.price_estimate, prop.pricing_profile?.currency || prop.country?.default_currency || 'KES') }}
                </div>
                <span v-if="prop.financing_allowed" class="pz-property-card__finance-tag">Finance Ready</span>
              </div>

              <!-- Title -->
              <h3 class="pz-property-card__title">{{ prop.title }}</h3>

              <!-- Location -->
              <div class="pz-property-card__location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>{{ prop.location_display || prop.location_text || prop.formatted_address || 'Location pending' }}</span>
              </div>

              <!-- Purpose -->
              <div v-if="prop.purpose_name" class="pz-property-card__purpose">
                {{ prop.purpose_name }}
              </div>

              <!-- Specs Row -->
              <div class="pz-property-card__specs">
                <div class="pz-property-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>
                  <span>{{ prop.specification?.bedrooms || 0 }} <span class="pz-property-card__spec-label">bed</span></span>
                </div>
                <div class="pz-property-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6"/><path d="M12 21v-7"/><path d="M8 14a4 4 0 0 1 8 0v7H8z"/><path d="M4 14h16"/></svg>
                  <span>{{ prop.specification?.bathrooms || 0 }} <span class="pz-property-card__spec-label">bath</span></span>
                </div>
                <div class="pz-property-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
                  <span>{{ readableValue(prop.development_metadata?.development_stage || 'NO_STAGE') }}</span>
                </div>
              </div>

              <!-- Features -->
              <div v-if="prop.highlighted_features?.length" class="pz-property-card__features">
                <span v-for="feature in prop.highlighted_features.slice(0, 3)" :key="feature.id">{{ feature.name }}</span>
              </div>

              <!-- Footer -->
              <div class="pz-property-card__footer">
                <div class="pz-property-card__agent">
                  <div class="pz-property-card__agent-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </div>
                  <span class="pz-property-card__agent-name">{{ prop.manager_name || prop.owner_name }}</span>
                </div>
                <Button size="sm" variant="outline">View Details</Button>
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
            <option v-for="country in configStore.countries" :key="country.id" :value="country.iso_code">
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
          <span class="pz-filter-bar__label">Budget Range ({{ configStore.activeCurrencyCode || 'KES' }})</span>
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

function formatNumber(num, sourceCurrency = 'KES') {
  return configStore.formatPrice(num, sourceCurrency);
}

function readableValue(value) {
  return String(value || '').replaceAll('_', ' ');
}

function buildParams() {
  const params = {};
  if (searchQuery.value) params.search = searchQuery.value;
  // Always include country so the backend knows the filter was explicitly set
  // (even when empty, meaning "show all countries" instead of falling back to header)
  params.country = filters.value.country || '';
  Object.entries(filters.value).forEach(([key, value]) => {
    if (key === 'country') return; // already handled above
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

function syncCountryFilterFromStore() {
  filters.value.country = configStore.activeCountryCode || '';
}

function syncStoreFromCountryFilter() {
  if (!filters.value.country) return;
  if (filters.value.country !== configStore.activeCountryCode) {
    configStore.setCountry(filters.value.country);
  }
}

async function fetchProperties() {
  const requestId = ++lastRequestId.value;
  loading.value = true;
  try {
    const builtParams = buildParams();
    console.log('[PropertyListing] fetching with params:', JSON.stringify(builtParams));
    const response = await api.get('/property/', { params: builtParams });
    if (requestId !== lastRequestId.value) return;
    console.log('[PropertyListing] received', (response.data.results || response.data || []).length, 'properties');
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
    country: configStore.activeCountryCode || '',
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
  syncCountryFilterFromStore();
  await Promise.all([fetchPurposes(), fetchProperties()]);
});

watch(
  () => configStore.activeCountryCode,
  () => {
    syncCountryFilterFromStore();
    fetchProperties();
  }
);

watch(
  () => filters.value.country,
  () => {
    syncStoreFromCountryFilter();
  }
);
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
  gap: 1.75rem;
  grid-template-columns: repeat(auto-fill, minmax(22rem, 1fr));
}

/* Modern Property Card */
.pz-property-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  border: 1px solid rgba(10, 10, 15, 0.06);
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 4px 12px rgba(10, 10, 15, 0.04);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.pz-property-card:hover {
  transform: translateY(-6px);
  box-shadow:
    0 8px 24px rgba(10, 10, 15, 0.06),
    0 24px 48px rgba(10, 10, 15, 0.08);
}

.pz-property-card:hover .pz-property-card__image {
  transform: scale(1.05);
}

/* Image Area */
.pz-property-card__image-wrap {
  position: relative;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background: linear-gradient(135deg, #e8e4db, #d4cfc5);
}

.pz-property-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.pz-property-card__image-fallback {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #2a2825, #5b5148);
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

/* Image Badges */
.pz-property-card__image-badges {
  position: absolute;
  top: 0.85rem;
  left: 0.85rem;
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.pz-property-card__badge {
  padding: 0.35rem 0.65rem;
  border-radius: 8px;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.pz-property-card__badge--type {
  background: rgba(255, 255, 255, 0.92);
  color: var(--pz-color-foundation-black);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.pz-property-card__badge--active {
  background: rgba(34, 139, 34, 0.9);
  color: white;
  border: 1px solid rgba(34, 139, 34, 0.3);
}

.pz-property-card__badge--status {
  background: rgba(10, 10, 15, 0.75);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Favorite Button */
.pz-property-card__fav {
  position: absolute;
  top: 0.85rem;
  right: 0.85rem;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: grid;
  place-items: center;
  cursor: pointer;
  transition: all 0.25s ease;
  color: var(--pz-color-concrete-grey);
  z-index: 2;
}

.pz-property-card__fav:hover {
  background: white;
  color: var(--pz-color-earth-orange);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(10, 10, 15, 0.15);
}

.pz-property-card__fav svg {
  width: 1.05rem;
  height: 1.05rem;
}

/* Card Body */
.pz-property-card__body {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}

/* Price Row */
.pz-property-card__price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.pz-property-card__price {
  font-family: var(--pz-font-display);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--pz-color-foundation-black);
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.pz-property-card__finance-tag {
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.18);
  color: #15803d;
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}

/* Title */
.pz-property-card__title {
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

/* Location */
.pz-property-card__location {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--pz-color-concrete-grey);
  font-size: 0.88rem;
  line-height: 1.4;
}

.pz-property-card__location svg {
  width: 0.9rem;
  height: 0.9rem;
  flex-shrink: 0;
  color: var(--pz-color-earth-orange);
}

/* Purpose */
.pz-property-card__purpose {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

/* Specs Row */
.pz-property-card__specs {
  display: flex;
  gap: 1.25rem;
  padding: 0.6rem 0;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
  margin-top: 0.2rem;
}

.pz-property-card__spec {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
  font-weight: 500;
}

.pz-property-card__spec svg {
  width: 1rem;
  height: 1rem;
  color: var(--pz-color-concrete-grey);
}

.pz-property-card__spec-label {
  color: var(--pz-color-concrete-grey);
  font-weight: 400;
}

/* Features */
.pz-property-card__features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.pz-property-card__features span {
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  background: rgba(212, 101, 42, 0.06);
  border: 1px solid rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.04em;
}

/* Footer */
.pz-property-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 0.75rem;
}

.pz-property-card__agent {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.pz-property-card__agent-avatar {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: rgba(10, 10, 15, 0.06);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.pz-property-card__agent-avatar svg {
  width: 0.9rem;
  height: 0.9rem;
  color: var(--pz-color-concrete-grey);
}

.pz-property-card__agent-name {
  font-size: 0.85rem;
  color: var(--pz-color-structural-steel);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
  .pz-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
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

  .pz-results-grid {
    grid-template-columns: 1fr;
  }
}
</style>
