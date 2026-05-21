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

    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="pz-property-workflow-banner">
        <div class="pz-property-workflow-banner__summary">
          <div class="pz-property-workflow-banner__kicker">{{ searchWorkflowSummary.stage }}</div>
          <h2 class="pz-property-workflow-banner__title">{{ searchWorkflowSummary.title }}</h2>
          <p class="pz-property-workflow-banner__body">{{ searchWorkflowSummary.body }}</p>
        </div>
        <div class="pz-property-workflow-banner__actions">
          <Button v-if="searchWorkflowSummary.primaryAction" variant="primary" size="sm" @click="searchWorkflowSummary.primaryAction.handler">
            {{ searchWorkflowSummary.primaryAction.label }}
          </Button>
          <Button v-if="searchWorkflowSummary.secondaryAction" variant="outline" size="sm" @click="searchWorkflowSummary.secondaryAction.handler">
            {{ searchWorkflowSummary.secondaryAction.label }}
          </Button>
        </div>
      </div>
      <div class="pz-property-workflow-banner__steps">
        <div
          v-for="step in searchWorkflowSteps"
          :key="step.label"
          class="pz-property-workflow-step"
          :class="{ 'pz-property-workflow-step--done': step.done, 'pz-property-workflow-step--active': step.active }"
        >
          <span class="pz-property-workflow-step__index">{{ step.index }}</span>
          <div class="pz-property-workflow-step__content">
            <strong>{{ step.label }}</strong>
            <span>{{ step.help }}</span>
          </div>
        </div>
      </div>

      <ModuleCTA
        eyebrow="List Property"
        title="Own or manage a property that should be visible here?"
        body="Open the property workspace to publish availability, add media, and receive inquiries or viewing requests from buyers and developers."
        primary-label="Create Property Listing"
        primary-to="/property-manager/dashboard"
        secondary-label="Start a Project"
        secondary-to="/projects/new"
        tone="steel"
      />
    </WorkflowGuide>

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
            <div class="pz-results-header__state">
              <span class="pz-results-header__state-item">Shortlisted {{ shortlistedProperties.length }}</span>
              <span class="pz-results-header__state-item">Compare {{ selectedForComparison.length }}/4</span>
            </div>
          </div>
          <div class="pz-results-header__actions">
            <Button class="u-show-mobile" variant="outline" size="sm" @click="mobileFiltersOpen = true">Filters</Button>
            <Button variant="outline" size="sm" @click="mapView = !mapView">{{ mapView ? 'List View' : 'Map View' }}</Button>
            <Button variant="outline" size="sm" @click="saveSearch">Save Search</Button>
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

        <EmptyState
          v-else-if="filteredProperties.length === 0"
          icon="🏠"
          title="No properties match your filters"
          :description="emptyStateGuidance.description"
          :nextStep="emptyStateGuidance.nextStep"
          action-label="Reset Filters"
          action-variant="outline"
          @action="clearFilters"
        />

        <div v-else-if="mapView" class="pz-property-map-view">
          <button
            v-for="prop in filteredPropertiesWithCoords"
            :key="prop.id"
            type="button"
            class="pz-property-map-pin"
            :style="getPropertyPinStyle(prop)"
            @click="viewProperty(prop.id)"
          >
            <strong>{{ formatNumber(prop.pricing_profile?.asking_price || prop.price_estimate, prop.pricing_profile?.currency || prop.country?.default_currency || 'KES') }}</strong>
            <span>{{ readableValue(prop.asset_type) }}</span>
          </button>
          <div v-if="!filteredPropertiesWithCoords.length" class="pz-property-map-empty">
            Properties need latitude and longitude before they can appear as map pins.
          </div>
        </div>

        <div v-else class="pz-results-grid">
          <div
            v-for="prop in filteredProperties"
            :key="prop.id"
            class="pz-property-card"
            @click="viewProperty(prop.id)"
          >
            <div class="pz-property-card__image-wrap">
              <img
                v-if="resolveMediaUrl(prop.primary_media?.media_url) || prop.primary_media?.external_url"
                :src="resolveMediaUrl(prop.primary_media?.media_url) || prop.primary_media?.external_url"
                :alt="prop.primary_media?.alt_text || prop.title"
                class="pz-property-card__image"
                loading="lazy"
              >
              <div v-else class="pz-property-card__image-fallback">
                <span>{{ readableValue(prop.asset_type) }}</span>
              </div>

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
                :class="{ 'pz-property-card__fav--active': isShortlisted(prop.id) }"
                :aria-label="isShortlisted(prop.id) ? 'Remove from shortlist' : 'Save to shortlist'"
                :title="isShortlisted(prop.id) ? 'Remove from shortlist' : 'Save to shortlist'"
                @click.stop="togglePropertyShortlist(prop)"
              >
                <svg v-if="isShortlisted(prop.id)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              </button>
            </div>

            <div class="pz-property-card__body">
              <div class="pz-property-card__price-row">
                <div class="pz-property-card__price">
                  {{ formatNumber(prop.pricing_profile?.asking_price || prop.price_estimate, prop.pricing_profile?.currency || prop.country?.default_currency || 'KES') }}
                </div>
                <span v-if="prop.financing_allowed" class="pz-property-card__finance-tag">Finance Ready</span>
              </div>

              <h3 class="pz-property-card__title">{{ prop.title }}</h3>

              <div class="pz-property-card__location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>{{ prop.location_display || prop.location_text || prop.formatted_address || 'Location pending' }}</span>
              </div>

              <div v-if="prop.purpose_name" class="pz-property-card__purpose">
                {{ prop.purpose_name }}
              </div>

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

              <div v-if="prop.highlighted_features?.length" class="pz-property-card__features">
                <span v-for="feature in prop.highlighted_features.slice(0, 3)" :key="feature.id">{{ feature.name }}</span>
              </div>

              <div class="pz-property-card__footer">
                <div class="pz-property-card__agent">
                  <div class="pz-property-card__agent-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </div>
                  <span class="pz-property-card__agent-name">{{ prop.manager_name || prop.owner_name }}</span>
                </div>
                <div class="pz-property-card__actions">
                <Button size="sm" variant="outline" @click.stop="togglePropertyForComparison(prop)">
                    {{ isSelectedForComparison(prop.id) ? 'Remove Compare' : 'Compare' }}
                  </Button>
                  <Button size="sm" variant="outline" @click.stop="viewProperty(prop.id)">View Details</Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div v-if="selectedForComparison.length > 0" class="pz-compare-bar" :class="{ 'pz-compare-bar--active': selectedForComparison.length > 0 }">
      <div class="pz-l-container pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
          <span class="pz-u-text-mono text-xs">{{ selectedForComparison.length }} properties selected for comparison</span>
          <div class="pz-l-flex pz-l-flex--gap-2 u-hide-mobile">
            <button
              v-for="item in selectedForComparison"
              :key="item.id"
              type="button"
              class="pz-compare-chip"
              @click="togglePropertyForComparison(item)"
            >
              {{ item.title }} ×
            </button>
          </div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3">
          <Button variant="ghost" size="sm" @click="clearPropertyComparison">Clear</Button>
          <Button variant="primary" size="sm" :disabled="selectedForComparison.length < 2" @click="showPropertyComparisonModal = true">
            Compare Properties
          </Button>
        </div>
      </div>
    </div>

    <Button class="pz-mobile-filter-trigger u-show-mobile" variant="primary" size="lg" pill @click="mobileFiltersOpen = true">
      Filters
    </Button>

    <Modal :isOpen="showPropertyComparisonModal" title="Compare Properties" size="xl" @close="showPropertyComparisonModal = false">
      <div v-if="selectedForComparison.length < 2" class="pz-comparison-empty">
        Select at least two properties to compare them side by side.
      </div>
      <div v-else class="pz-compare-table-wrap">
        <table class="pz-compare-table">
          <thead>
            <tr>
              <th>Attribute</th>
              <th v-for="item in selectedForComparison" :key="item.id">{{ item.title }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Price</td>
              <td v-for="item in selectedForComparison" :key="item.id">
                {{ formatNumber(item.pricing_profile?.asking_price || item.price_estimate, item.pricing_profile?.currency || item.country?.default_currency || 'KES') }}
              </td>
            </tr>
            <tr>
              <td>Location</td>
              <td v-for="item in selectedForComparison" :key="item.id">
                {{ item.location_display || item.location_text || item.formatted_address || 'Location pending' }}
              </td>
            </tr>
            <tr>
              <td>Purpose</td>
              <td v-for="item in selectedForComparison" :key="item.id">{{ item.purpose_name || '—' }}</td>
            </tr>
            <tr>
              <td>Bedrooms</td>
              <td v-for="item in selectedForComparison" :key="item.id">{{ item.specification?.bedrooms || 0 }}</td>
            </tr>
            <tr>
              <td>Bathrooms</td>
              <td v-for="item in selectedForComparison" :key="item.id">{{ item.specification?.bathrooms || 0 }}</td>
            </tr>
            <tr>
              <td>Stage</td>
              <td v-for="item in selectedForComparison" :key="item.id">{{ readableValue(item.development_metadata?.development_stage || 'NO_STAGE') }}</td>
            </tr>
            <tr>
              <td>Finance Ready</td>
              <td v-for="item in selectedForComparison" :key="item.id">
                <Badge :variant="item.financing_allowed ? 'success' : 'secondary'">
                  {{ item.financing_allowed ? 'Yes' : 'No' }}
                </Badge>
              </td>
            </tr>
            <tr>
              <td>Inquiry / Visit</td>
              <td v-for="item in selectedForComparison" :key="item.id">
                <div class="pz-compare-flags">
                  <Badge :variant="item.inquiry_enabled !== false ? 'success' : 'secondary'">{{ item.inquiry_enabled !== false ? 'Inquiry open' : 'Inquiry closed' }}</Badge>
                  <Badge :variant="item.appointment_enabled !== false ? 'success' : 'secondary'">{{ item.appointment_enabled !== false ? 'Visits open' : 'Visits closed' }}</Badge>
                </div>
              </td>
            </tr>
            <tr>
              <td>Top Features</td>
              <td v-for="item in selectedForComparison" :key="item.id">
                {{ (item.highlighted_features || []).slice(0, 3).map((feature) => feature.name).join(', ') || '—' }}
              </td>
            </tr>
            <tr>
              <td></td>
              <td v-for="item in selectedForComparison" :key="item.id">
                <Button size="sm" variant="primary" @click="viewProperty(item.id)">Open Property</Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Modal>

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
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Badge from '../components/ui/Badge.vue';
import EntryHero from '../components/ui/EntryHero.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import Modal from '../components/ui/Modal.vue';
import { useConfigStore } from '../stores/config';
import { detectUserLocation, getStoredLocation } from '../utils/location';

const configStore = useConfigStore();
const router = useRouter();

const mediaBaseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/api\/?$/, '');
function resolveMediaUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `${mediaBaseUrl}${url}`;
}

const properties = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const mobileFiltersOpen = ref(false);
const mapView = ref(false);
const onlyFinanceReady = ref(false);
const onlyBuildReady = ref(false);
const lastRequestId = ref(0);
const userCoords = ref(getStoredLocation());
const purposeTree = ref([]);
const shortlistedProperties = ref([]);
const selectedForComparison = ref([]);
const showPropertyComparisonModal = ref(false);
const shortlistStorageKey = 'pz-property-shortlist';
const compareStorageKey = 'pz-property-compare';

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
const filteredPropertiesWithCoords = computed(() =>
  filteredProperties.value.filter((item) => item.latitude !== null && item.latitude !== undefined && item.longitude !== null && item.longitude !== undefined)
);

const activeFiltersCount = computed(() => {
  let count = searchQuery.value ? 1 : 0;
  Object.values(filters.value).forEach((value) => {
    if (value !== '' && value !== null && value !== undefined) count += 1;
  });
  if (onlyFinanceReady.value) count += 1;
  if (onlyBuildReady.value) count += 1;
  return count;
});

const emptyStateGuidance = computed(() => {
  const suggestions = [];
  if (filters.value.condition_rating) suggestions.push('remove the condition filter');
  if (filters.value.radius_km && Number(filters.value.radius_km) < 50) suggestions.push('expand the radius to 50 KM');
  if (filters.value.max_price) suggestions.push('raise the maximum budget');
  if (filters.value.asset_type) suggestions.push('include all asset types');
  if (filters.value.development_stage) suggestions.push('remove the development stage filter');
  const nextStep = suggestions.length
    ? `Try to ${suggestions.slice(0, 2).join(' or ')}.`
    : 'Clear one or two filters, or change the purpose and development stage to widen the results.';
  return {
    description: 'The current filters are too narrow for the available property set.',
    nextStep,
  };
});

const searchWorkflowSummary = computed(() => {
  if (loading.value) {
    return {
      stage: 'LOADING',
      title: 'Preparing the property workspace',
      body: 'Loading listings and filter options so you can compare properties without guessing.',
      primaryAction: null,
      secondaryAction: null,
    };
  }

  if (filteredProperties.value.length === 0) {
    return {
      stage: 'NO_MATCHES',
      title: 'Your filters are too narrow',
      body: 'Widen the search or change the purpose, stage, or budget so more properties appear.',
      primaryAction: { label: 'Reset Filters', handler: clearFilters },
      secondaryAction: { label: 'Use My Location', handler: useMyLocation },
    };
  }

  return {
    stage: 'DISCOVERY_READY',
    title: 'Find, compare, and act on the right property',
    body: 'Start with location and purpose, compare the strongest listings, then move to the property detail page to contact the owner or book a visit.',
    primaryAction: { label: 'Open Filters', handler: scrollToMarket },
    secondaryAction: { label: 'Clear Filters', handler: clearFilters },
  };
});

const searchWorkflowSteps = computed(() => [
  {
    index: '01',
    label: 'Narrow the search',
    help: 'Use filters to find the properties that match the current buying goal.',
    done: activeFiltersCount.value > 0,
    active: true,
  },
  {
    index: '02',
    label: 'Compare the results',
    help: 'Review price, location, and property readiness before opening a listing.',
    done: filteredProperties.value.length > 1,
    active: filteredProperties.value.length > 0,
  },
  {
    index: '03',
    label: 'Open the property',
    help: 'Move to the detail page to contact the owner, book a visit, or review finance paths.',
    done: filteredProperties.value.length > 0,
    active: filteredProperties.value.length > 0,
  },
]);

function formatNumber(num, sourceCurrency = 'KES') {
  return configStore.formatPrice(num, sourceCurrency);
}

function readableValue(value) {
  return String(value || '').replaceAll('_', ' ');
}

function loadStoredPropertySelection(storageKey) {
  if (typeof window === 'undefined') return [];
  try {
    const stored = window.localStorage.getItem(storageKey);
    const parsed = stored ? JSON.parse(stored) : [];
    return Array.isArray(parsed) ? parsed.filter(Boolean) : [];
  } catch (error) {
    console.error(`Failed to load ${storageKey}`, error);
    return [];
  }
}

function saveStoredPropertySelection(storageKey, items) {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(storageKey, JSON.stringify(items));
  } catch (error) {
    console.error(`Failed to save ${storageKey}`, error);
  }
}

function persistPropertySelection(storageKey, items) {
  saveStoredPropertySelection(storageKey, items);
}

function hydratePropertySelection(storageKey, fallback = []) {
  const stored = loadStoredPropertySelection(storageKey);
  return stored.length ? stored : fallback;
}

function reconcileSavedSelection(savedItems, freshItems) {
  const freshById = new Map((freshItems || []).map((item) => [String(item.id), item]));
  return savedItems
    .map((item) => freshById.get(String(item.id)) || item)
    .filter(Boolean)
    .filter((item, index, array) => array.findIndex((candidate) => String(candidate.id) === String(item.id)) === index);
}

function isShortlisted(id) {
  return shortlistedProperties.value.some((item) => String(item.id) === String(id));
}

function isSelectedForComparison(id) {
  return selectedForComparison.value.some((item) => String(item.id) === String(id));
}

function togglePropertyShortlist(prop) {
  const exists = isShortlisted(prop.id);
  shortlistedProperties.value = exists
    ? shortlistedProperties.value.filter((item) => String(item.id) !== String(prop.id))
    : [...shortlistedProperties.value, prop];
  persistPropertySelection(shortlistStorageKey, shortlistedProperties.value);
}

function togglePropertyForComparison(prop) {
  const exists = isSelectedForComparison(prop.id);
  if (exists) {
    selectedForComparison.value = selectedForComparison.value.filter((item) => String(item.id) !== String(prop.id));
  } else if (selectedForComparison.value.length < 4) {
    selectedForComparison.value = [...selectedForComparison.value, prop];
  }
  persistPropertySelection(compareStorageKey, selectedForComparison.value);
}

function clearPropertyComparison() {
  selectedForComparison.value = [];
  showPropertyComparisonModal.value = false;
  persistPropertySelection(compareStorageKey, selectedForComparison.value);
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
    shortlistedProperties.value = reconcileSavedSelection(shortlistedProperties.value, properties.value);
    selectedForComparison.value = reconcileSavedSelection(selectedForComparison.value, properties.value).slice(0, 4);
    persistPropertySelection(shortlistStorageKey, shortlistedProperties.value);
    persistPropertySelection(compareStorageKey, selectedForComparison.value);
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

function getPropertyPinStyle(prop) {
  const lat = Number(prop.latitude || 0);
  const lng = Number(prop.longitude || 0);
  return {
    left: `${Math.min(94, Math.max(6, ((lng + 180) / 360) * 100))}%`,
    top: `${Math.min(94, Math.max(6, ((90 - lat) / 180) * 100))}%`,
  };
}

async function saveSearch() {
  const email = window.prompt('Email for new matching property alerts');
  if (!email) return;
  try {
    await api.post('/property/saved-searches/', {
      email,
      name: searchQuery.value || 'Saved property search',
      filters: {
        search: searchQuery.value,
        ...filters.value,
        financing_allowed: onlyFinanceReady.value,
        build_ready: onlyBuildReady.value,
      },
    });
    window.alert('Search saved.');
  } catch {
    window.alert('Could not save this search.');
  }
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
  shortlistedProperties.value = hydratePropertySelection(shortlistStorageKey);
  selectedForComparison.value = hydratePropertySelection(compareStorageKey).slice(0, 4);
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
  padding-bottom: 7rem;
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

.pz-results-header__state {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.pz-results-header__state-item {
  padding: 0.35rem 0.6rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.88);
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
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

.pz-property-card__fav--active {
  background: rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
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

.pz-property-card__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.5rem;
}

.pz-compare-bar {
  position: fixed;
  left: 1rem;
  right: 1rem;
  bottom: 1rem;
  z-index: 35;
}

.pz-compare-bar--active {
  box-shadow: 0 -8px 24px rgba(10, 10, 15, 0.08);
}

.pz-compare-bar .pz-l-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.96);
  backdrop-filter: blur(10px);
}

.pz-compare-chip {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: white;
  padding: 0 0.75rem;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

.pz-compare-chip:hover {
  border-color: rgba(212, 101, 42, 0.35);
  color: var(--pz-color-earth-orange);
}

.pz-comparison-empty {
  display: grid;
  place-items: center;
  min-height: 10rem;
  padding: 1.5rem;
  text-align: center;
  border: 1px dashed rgba(10, 10, 15, 0.14);
  background: rgba(247, 244, 239, 0.7);
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  line-height: 1.6;
  color: var(--pz-color-concrete-grey);
}

.pz-compare-flags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.pz-compare-table-wrap {
  overflow-x: auto;
}

.pz-compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.pz-compare-table th,
.pz-compare-table td {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  text-align: left;
  vertical-align: top;
}

.pz-compare-table th {
  background: rgba(10, 10, 15, 0.03);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

.pz-compare-table td:first-child {
  font-weight: 600;
  color: var(--pz-color-structural-steel);
  white-space: nowrap;
}

.pz-compare-table th:not(:first-child) {
  min-width: 10rem;
  color: var(--pz-color-foundation-black);
  font-size: 0.8rem;
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

.pz-property-workflow-banner {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) auto;
  gap: 1rem;
  align-items: start;
}

.pz-property-workflow-banner__summary {
  display: grid;
  gap: 0.5rem;
}

.pz-property-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-property-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-property-workflow-banner__body {
  margin: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  line-height: 1.6;
  color: var(--pz-color-concrete-grey);
  max-width: 72ch;
}

.pz-property-workflow-banner__actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.pz-property-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 1rem;
}

.pz-property-workflow-step {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 0.75rem;
  padding: 0.9rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.88);
}

.pz-property-workflow-step__index {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(247, 244, 239, 0.95);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
}

.pz-property-workflow-step__content {
  display: grid;
  gap: 0.2rem;
}

.pz-property-workflow-step__content strong {
  font-size: 0.85rem;
}

.pz-property-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  line-height: 1.5;
  color: var(--pz-color-concrete-grey);
}

.pz-property-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
}

.pz-property-workflow-step--done .pz-property-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
}

.pz-property-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.35);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-mobile-filter-trigger {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  z-index: 30;
}

.pz-property-map-view {
  position: relative;
  min-height: 32rem;
  overflow: hidden;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(10, 10, 15, 0.045) 1px, transparent 1px),
    linear-gradient(rgba(10, 10, 15, 0.045) 1px, transparent 1px),
    rgba(247, 244, 239, 0.8);
  background-size: 10% 10%;
}

.pz-property-map-pin {
  position: absolute;
  transform: translate(-50%, -50%);
  display: grid;
  gap: 0.15rem;
  min-width: 7rem;
  padding: 0.45rem 0.6rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  border-radius: 8px;
  background: white;
  box-shadow: 0 8px 18px rgba(10, 10, 15, 0.1);
  text-align: left;
}

.pz-property-map-pin strong {
  font-family: var(--pz-font-display);
  font-size: 0.78rem;
}

.pz-property-map-pin span,
.pz-property-map-empty {
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  color: var(--pz-color-concrete-grey);
}

.pz-property-map-empty {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 1rem;
  text-align: center;
}

@media (max-width: 1024px) {
  .pz-market-shell {
    grid-template-columns: 1fr;
  }
  .pz-property-workflow-banner {
    grid-template-columns: 1fr;
  }
  .pz-property-workflow-banner__actions {
    justify-content: flex-start;
  }
  .pz-property-workflow-banner__steps {
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

  .pz-results-header__state {
    gap: 0.4rem;
  }

  .pz-filter-range {
    grid-template-columns: 1fr;
  }

  .pz-results-grid {
    grid-template-columns: 1fr;
  }

  .pz-property-card__actions {
    justify-content: stretch;
  }

  .pz-property-card__actions :deep(button) {
    width: 100%;
  }

  .pz-compare-bar .pz-l-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .pz-compare-bar .pz-l-flex--gap-3 {
    width: 100%;
    justify-content: stretch;
  }

  .pz-compare-bar .pz-l-flex--gap-3 :deep(button) {
    flex: 1;
  }

  .pz-mobile-filter-trigger {
    bottom: 5rem;
  }
}
</style>
