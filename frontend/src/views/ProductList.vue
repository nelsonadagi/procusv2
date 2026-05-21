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

    <div class="pz-l-container u-mt-6">
      <WorkflowGuide title="Materials Workflow" :eyebrow="workflowSummary.stage">
          <div class="pz-product-workflow">
            <div class="pz-product-workflow__summary">
              <div class="pz-product-workflow__kicker">{{ workflowSummary.stage }}</div>
              <h3 class="pz-product-workflow__title">{{ workflowSummary.title }}</h3>
              <p class="pz-product-workflow__body">{{ workflowSummary.body }}</p>
              <div class="pz-product-workflow__actions">
                <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
                  {{ workflowSummary.primaryAction.label }}
                </Button>
                <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
                  {{ workflowSummary.secondaryAction.label }}
                </Button>
              </div>
            </div>
            <div class="pz-product-workflow__metrics">
              <div class="pz-product-workflow__metric">
                <span>Visible Products</span>
                <strong>{{ totalProducts }}</strong>
              </div>
              <div class="pz-product-workflow__metric">
                <span>Compare Queue</span>
                <strong>{{ selectedForComparison.length }}</strong>
              </div>
              <div class="pz-product-workflow__metric">
                <span>Active Filters</span>
                <strong>{{ activeFiltersCount }}</strong>
              </div>
            </div>
          </div>
          <div class="pz-product-workflow__steps">
            <div
              v-for="step in workflowSteps"
              :key="step.label"
              class="pz-product-workflow-step"
              :class="{ 'pz-product-workflow-step--done': step.done, 'pz-product-workflow-step--active': step.active }"
            >
              <span class="pz-product-workflow-step__index">{{ step.index }}</span>
              <div class="pz-product-workflow-step__content">
                <strong>{{ step.label }}</strong>
                <span>{{ step.help }}</span>
              </div>
            </div>
          </div>

          <ModuleCTA
            eyebrow="Sell Materials"
            title="Have materials to sell on the marketplace?"
            body="Activate a vendor workspace, list your first product, and start receiving quote requests from buyers who are already comparing suppliers."
            primary-label="Become a Vendor"
            primary-to="/vendors/register"
            secondary-label="List a Product"
            secondary-to="/vendor/dashboard"
            tone="earth"
          />
      </WorkflowGuide>
    </div>

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

          <!-- Location -->
          <div class="pz-filter-section">
            <button type="button" class="pz-filter-section__trigger" @click="toggleSection('location')">
              <span>Location</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.location }"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div v-show="expandedSections.location" class="pz-filter-section__body">
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Country</span>
                <select v-model="selectedCountry" @change="handleHubChange" class="pz-filter-field__control">
                  <option value="">Global Marketplace</option>
                  <option v-for="c in configStore.countries" :key="c.id" :value="c.iso_code">{{ c.flag_emoji }} {{ c.name }}</option>
                </select>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">County / State</span>
                <select v-model="selectedCounty" @change="handleCountyChange" class="pz-filter-field__control">
                  <option value="">All Counties</option>
                  <option v-for="c in availableCounties" :key="c" :value="c">{{ c }}</option>
                </select>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Subcounty / City</span>
                <select v-model="selectedSubcounty" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">All Areas</option>
                  <option v-for="s in availableSubcounties" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Radius (KM)</span>
                <select v-model="selectedRadius" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">Any distance</option>
                  <option value="5">5 KM</option>
                  <option value="10">10 KM</option>
                  <option value="25">25 KM</option>
                  <option value="50">50 KM</option>
                  <option value="100">100 KM</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Product Details -->
          <div class="pz-filter-section">
            <button type="button" class="pz-filter-section__trigger" @click="toggleSection('product')">
              <span>Product Details</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.product }"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div v-show="expandedSections.product" class="pz-filter-section__body">
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Material Category</span>
                <select v-model="selectedCategory" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">All Industrial Materials</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Certification</span>
                <input v-model.trim="certificationQuery" type="text" placeholder="KEBS, ISO 9001, CE" class="pz-filter-field__control" @input="debouncedSearch">
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Country of Origin</span>
                <input v-model.trim="originQuery" type="text" placeholder="Kenya, Tanzania, China" class="pz-filter-field__control" @input="debouncedSearch">
              </div>
            </div>
          </div>

          <!-- Pricing -->
          <div class="pz-filter-section">
            <button type="button" class="pz-filter-section__trigger" @click="toggleSection('pricing')">
              <span>Pricing & Sort</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.pricing }"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div v-show="expandedSections.pricing" class="pz-filter-section__body">
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Price Range</span>
                <div class="pz-filter-range">
                  <input v-model.number="priceMin" type="number" placeholder="Min" class="pz-filter-field__control" @change="fetchProducts">
                  <span class="pz-filter-range__sep">—</span>
                  <input v-model.number="priceMax" type="number" placeholder="Max" class="pz-filter-field__control" @change="fetchProducts">
                </div>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Sort By</span>
                <select v-model="sortBy" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">Standard</option>
                  <option value="base_price">Lowest Price</option>
                  <option value="-base_price">Highest Price</option>
                  <option value="-created_at">Newest Arrivals</option>
                  <option value="distance" v-if="userCoords">Nearest To Me</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Availability -->
          <div class="pz-filter-section">
            <button type="button" class="pz-filter-section__trigger" @click="toggleSection('availability')">
              <span>Availability</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.availability }"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div v-show="expandedSections.availability" class="pz-filter-section__body">
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Inventory Status</span>
                <select v-model="inventorySignal" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">All stock states</option>
                  <option value="IN_STOCK">In Stock</option>
                  <option value="LOW_STOCK">Low Stock</option>
                  <option value="OUT_OF_STOCK">Out of Stock</option>
                </select>
              </div>
              <div class="pz-filter-field">
                <span class="pz-filter-field__label">Delivery Region</span>
                <select v-model="deliveryRegion" @change="fetchProducts" class="pz-filter-field__control">
                  <option value="">Any delivery region</option>
                  <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
                </select>
              </div>
              <div class="pz-filter-toggles">
                <label class="pz-filter-toggle">
                  <input v-model="inStockOnly" type="checkbox" @change="fetchProducts">
                  <span class="pz-toggle-check"></span>
                  <span>In Stock Only</span>
                </label>
                <label class="pz-filter-toggle">
                  <input v-model="verifiedOnly" type="checkbox" @change="fetchProducts">
                  <span class="pz-toggle-check"></span>
                  <span>Verified Suppliers</span>
                </label>
              </div>
            </div>
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
        <!-- Active Filter Chips -->
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
            <button v-if="activeFiltersCount > 1" type="button" class="pz-filter-chip pz-filter-chip--clear" @click="clearFilters">
              Clear all
            </button>
          </div>
        </div>

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
        <div v-else :class="viewMode === 'grid' ? 'pz-product-grid' : 'pz-product-list'">
          <article
            v-for="product in productList"
            :key="product.id"
            class="pz-product-card"
            :class="{ 'pz-product-card--featured': product.is_featured, 'pz-product-card--list': viewMode === 'list' }"
            @click="handleProductClick(product)"
          >
            <div class="pz-product-card__media">
              <img
                :src="product.primary_image_url || '/placeholder.png'"
                :alt="product.name"
                class="pz-product-card__img"
                loading="lazy"
              />
              <div class="pz-product-card__badges">
                <span v-if="product.is_featured" class="pz-product-card__badge pz-product-card__badge--featured">Featured</span>
                <span v-if="product.is_new_arrival" class="pz-product-card__badge pz-product-card__badge--new">New</span>
                <span v-if="product.is_on_sale" class="pz-product-card__badge pz-product-card__badge--sale">Bulk Rate</span>
                <span
                  v-if="product.inventory_signal === 'LOW_STOCK'"
                  class="pz-product-card__badge pz-product-card__badge--warning"
                >Low Stock</span>
                <span
                  v-else-if="product.inventory_signal === 'OUT_OF_STOCK'"
                  class="pz-product-card__badge pz-product-card__badge--danger"
                >Out of Stock</span>
                <span v-else class="pz-product-card__badge pz-product-card__badge--success">In Stock</span>
              </div>
            </div>

            <div class="pz-product-card__body">
              <div class="pz-product-card__eyebrow">{{ product.vendor_business_name }}</div>
              <h4 class="pz-product-card__title">{{ product.name }}</h4>

              <div class="pz-product-card__location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                {{ product.vendor_location }}{{ product.vendor_country_name ? ', ' + product.vendor_country_name : '' }}
              </div>

              <div class="pz-product-card__specs">
                <span class="pz-product-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                  {{ product.quality_grade || 'A+' }}
                </span>
                <span class="pz-product-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
                  {{ product.stock_quantity }} {{ product.unit }}
                </span>
                <span v-if="product.country_of_origin" class="pz-product-card__spec">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                  {{ product.country_of_origin }}
                </span>
              </div>

              <div v-if="product.attribute_highlights?.length" class="pz-product-card__attribute">
                {{ product.attribute_highlights[0]?.name }}: {{ product.attribute_highlights[0]?.value }}{{ product.attribute_highlights[0]?.unit ? ` ${product.attribute_highlights[0].unit}` : '' }}
              </div>

              <div v-if="product.certification_highlights?.length" class="pz-product-card__features">
                <span v-for="cert in product.certification_highlights" :key="cert">{{ cert }}</span>
              </div>

              <div class="pz-product-card__price-row">
                <div>
                  <span class="pz-product-card__price">{{ configStore.formatPrice(product.base_price, product.effective_currency || product.currency, displayCurrencyCode) }}</span>
                  <span class="pz-product-card__unit">/{{ product.unit }}</span>
                </div>
                <Button variant="primary" size="sm" @click.stop="requestQuote(product)">Get Quote</Button>
              </div>

              <div class="pz-product-card__footer">
                <div class="pz-product-card__vendor">
                  <div class="pz-product-card__vendor-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </div>
                  <span>{{ product.vendor_business_name }}</span>
                </div>
                <Button variant="outline" size="sm" @click.stop="handleProductClick(product)">View Details</Button>
              </div>
            </div>
          </article>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && productList.length === 0" class="pz-card pz-p-12 pz-u-text-center">
          <div class="u-text-4xl u-mb-4">🔍</div>
          <h3 class="pz-u-text-display text-lg">No Products Found</h3>
          <p class="pz-u-text-mono text-xs pz-u-color-steel u-mb-8">Try changing your search filters</p>
          <Button variant="outline" @click="clearFilters">Reset All Filters</Button>
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
        <!-- Location -->
        <div class="pz-filter-section">
          <button type="button" class="pz-filter-section__trigger" @click="toggleSection('location')">
            <span>Location</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.location }"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div v-show="expandedSections.location" class="pz-filter-section__body">
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Country</span>
              <select v-model="selectedCountry" @change="handleHubChange" class="pz-filter-field__control">
                <option value="">Global Marketplace</option>
                <option v-for="c in configStore.countries" :key="c.id" :value="c.iso_code">{{ c.flag_emoji }} {{ c.name }}</option>
              </select>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">County / State</span>
              <select v-model="selectedCounty" @change="handleCountyChange" class="pz-filter-field__control">
                <option value="">All Counties</option>
                <option v-for="c in availableCounties" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Subcounty / City</span>
              <select v-model="selectedSubcounty" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">All Areas</option>
                <option v-for="s in availableSubcounties" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Radius (KM)</span>
              <select v-model="selectedRadius" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">Any distance</option>
                <option value="5">5 KM</option>
                <option value="10">10 KM</option>
                <option value="25">25 KM</option>
                <option value="50">50 KM</option>
                <option value="100">100 KM</option>
              </select>
            </div>
          </div>
        </div>
        <!-- Product Details -->
        <div class="pz-filter-section">
          <button type="button" class="pz-filter-section__trigger" @click="toggleSection('product')">
            <span>Product Details</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.product }"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div v-show="expandedSections.product" class="pz-filter-section__body">
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Material Category</span>
              <select v-model="selectedCategory" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">All Industrial Materials</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Certification</span>
              <input v-model.trim="certificationQuery" type="text" placeholder="KEBS, ISO 9001, CE" class="pz-filter-field__control" @input="debouncedSearch">
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Country of Origin</span>
              <input v-model.trim="originQuery" type="text" placeholder="Kenya, Tanzania, China" class="pz-filter-field__control" @input="debouncedSearch">
            </div>
          </div>
        </div>
        <!-- Pricing -->
        <div class="pz-filter-section">
          <button type="button" class="pz-filter-section__trigger" @click="toggleSection('pricing')">
            <span>Pricing & Sort</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.pricing }"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div v-show="expandedSections.pricing" class="pz-filter-section__body">
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Price Range</span>
              <div class="pz-filter-range">
                <input v-model.number="priceMin" type="number" placeholder="Min" class="pz-filter-field__control" @change="fetchProducts">
                <span class="pz-filter-range__sep">—</span>
                <input v-model.number="priceMax" type="number" placeholder="Max" class="pz-filter-field__control" @change="fetchProducts">
              </div>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Sort By</span>
              <select v-model="sortBy" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">Standard</option>
                <option value="base_price">Lowest Price</option>
                <option value="-base_price">Highest Price</option>
                <option value="-created_at">Newest Arrivals</option>
                <option value="distance" v-if="userCoords">Nearest To Me</option>
              </select>
            </div>
          </div>
        </div>
        <!-- Availability -->
        <div class="pz-filter-section">
          <button type="button" class="pz-filter-section__trigger" @click="toggleSection('availability')">
            <span>Availability</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="pz-filter-section__icon" :class="{ 'is-open': expandedSections.availability }"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div v-show="expandedSections.availability" class="pz-filter-section__body">
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Inventory Status</span>
              <select v-model="inventorySignal" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">All stock states</option>
                <option value="IN_STOCK">In Stock</option>
                <option value="LOW_STOCK">Low Stock</option>
                <option value="OUT_OF_STOCK">Out of Stock</option>
              </select>
            </div>
            <div class="pz-filter-field">
              <span class="pz-filter-field__label">Delivery Region</span>
              <select v-model="deliveryRegion" @change="fetchProducts" class="pz-filter-field__control">
                <option value="">Any delivery region</option>
                <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
            <div class="pz-filter-toggles">
              <label class="pz-filter-toggle">
                <input v-model="inStockOnly" type="checkbox" @change="fetchProducts">
                <span class="pz-toggle-check"></span>
                <span>In Stock Only</span>
              </label>
              <label class="pz-filter-toggle">
                <input v-model="verifiedOnly" type="checkbox" @change="fetchProducts">
                <span class="pz-toggle-check"></span>
                <span>Verified Suppliers</span>
              </label>
            </div>
          </div>
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
          <span class="pz-u-text-mono text-xs">{{ selectedForComparison.length }} selected</span>
          <div class="pz-l-flex pz-l-flex--gap-2 u-hide-mobile">
            <Badge v-for="p in selectedForComparison" :key="p.id" variant="finance"
              @click="toggleProductForComparison(p)">{{ p.name }} ✕</Badge>
          </div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3">
          <Button variant="ghost" size="sm" @click="selectedForComparison = []">Discard</Button>
          <Button variant="primary" size="sm" @click="showComparisonModal = true">Compare Products</Button>
        </div>
      </div>
    </div>

    <!-- Comparison Modal -->
    <Modal :isOpen="showComparisonModal" title="Compare Materials" size="xl" @close="showComparisonModal = false">
      <div v-if="selectedForComparison.length" class="pz-compare-table-wrap">
        <table class="pz-compare-table">
          <thead>
            <tr>
              <th>Attribute</th>
              <th v-for="p in selectedForComparison" :key="p.id">{{ p.name }}</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Price</td><td v-for="p in selectedForComparison" :key="p.id">{{ configStore.formatPrice(p.base_price, p.effective_currency || p.currency, displayCurrencyCode) }}</td></tr>
            <tr><td>Bulk Price</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.bulk_price ? configStore.formatPrice(p.bulk_price, p.effective_currency || p.currency, displayCurrencyCode) : '—' }}</td></tr>
            <tr><td>Brand</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.brand || '—' }}</td></tr>
            <tr><td>Stock</td><td v-for="p in selectedForComparison" :key="p.id"><Badge :variant="inventoryBadgeVariant(p.inventory_signal)">{{ formatInventorySignal(p.inventory_signal) }}</Badge></td></tr>
            <tr><td>Min Order</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.min_order_quantity || 1 }} {{ p.unit }}</td></tr>
            <tr><td>Quality</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.quality_grade || '—' }}</td></tr>
            <tr><td>Origin</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.country_of_origin || '—' }}</td></tr>
            <tr><td>Certifications</td><td v-for="p in selectedForComparison" :key="p.id">{{ p.certification_highlights?.join(', ') || '—' }}</td></tr>
            <tr>
              <td></td>
              <td v-for="p in selectedForComparison" :key="p.id">
                <Button size="sm" variant="primary" @click="requestQuote(p); showComparisonModal = false">Quote</Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Modal>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, inject, watch } from 'vue';
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
  import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
  import ModuleCTA from '../components/ui/ModuleCTA.vue';
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
  const showComparisonModal = ref(false);

  const regions = ['NAIROBI', 'MOMBASA', 'KISUMU', 'NAKURU', 'ELDORET', 'CENTRAL', 'COAST', 'RIFT VALLEY'];

  // Computed Context
  const totalPages = computed(() => Math.ceil(totalProducts.value / pageSize));
  const regionalDefaultCountryCode = computed(() => {
    const country = configStore.activeCountry;
    return country?.iso_code ? String(country.iso_code) : '';
  });
  const displayCurrencyCode = computed(() => {
    if (selectedCountry.value) {
      const country = configStore.countries.find((item) => String(item.iso_code).toUpperCase() === String(selectedCountry.value).toUpperCase());
      return country?.default_currency || configStore.activeCurrencyCode || 'KES';
    }
    return configStore.activeCurrencyCode || 'KES';
  });
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
    if (selectedRadius.value) count++;
    if (sortBy.value) count++;
    return count;
  });

  const expandedSections = ref({ location: true, product: true, pricing: true, availability: true });
  const toggleSection = (section) => { expandedSections.value[section] = !expandedSections.value[section]; };

  const activeFilterChips = computed(() => {
    const chips = [];
    if (selectedCountry.value) {
      const c = configStore.countries.find(x => String(x.iso_code).toUpperCase() === String(selectedCountry.value).toUpperCase());
      chips.push({ key: 'country', label: 'Country', value: c?.name || selectedCountry.value });
    }
    if (selectedCategory.value) {
      const c = categories.value.find(x => x.id === selectedCategory.value);
      chips.push({ key: 'category', label: 'Category', value: c?.name || 'Category' });
    }
    if (selectedCounty.value) chips.push({ key: 'county', label: 'County', value: selectedCounty.value });
    if (selectedSubcounty.value) chips.push({ key: 'subcounty', label: 'City', value: selectedSubcounty.value });
    if (certificationQuery.value) chips.push({ key: 'certification', label: 'Cert', value: certificationQuery.value });
    if (originQuery.value) chips.push({ key: 'origin', label: 'Origin', value: originQuery.value });
    if (priceMin.value !== null) chips.push({ key: 'priceMin', label: 'Min', value: configStore.formatPrice(priceMin.value, configStore.activeCurrencyCode, displayCurrencyCode.value) });
    if (priceMax.value !== null) chips.push({ key: 'priceMax', label: 'Max', value: configStore.formatPrice(priceMax.value, configStore.activeCurrencyCode, displayCurrencyCode.value) });
    if (inventorySignal.value) chips.push({ key: 'inventory', label: 'Stock', value: inventorySignal.value.replace('_', ' ') });
    if (deliveryRegion.value) chips.push({ key: 'delivery', label: 'Delivery', value: deliveryRegion.value });
    if (inStockOnly.value) chips.push({ key: 'inStock', label: 'Stock', value: 'In Stock Only' });
    if (verifiedOnly.value) chips.push({ key: 'verified', label: 'Supplier', value: 'Verified' });
    if (selectedRadius.value) chips.push({ key: 'radius', label: 'Radius', value: `${selectedRadius.value}km` });
    if (sortBy.value) {
      const labels = { base_price: 'Lowest Price', '-base_price': 'Highest Price', '-created_at': 'Newest', distance: 'Nearest' };
      chips.push({ key: 'sort', label: 'Sort', value: labels[sortBy.value] || sortBy.value });
    }
    return chips;
  });

  const removeFilterChip = (chip) => {
    switch (chip.key) {
      case 'country': selectedCountry.value = regionalDefaultCountryCode.value; handleHubChange(); break;
      case 'category': selectedCategory.value = ''; fetchProducts(); break;
      case 'county': selectedCounty.value = ''; handleCountyChange(); break;
      case 'subcounty': selectedSubcounty.value = ''; fetchProducts(); break;
      case 'certification': certificationQuery.value = ''; debouncedSearch(); break;
      case 'origin': originQuery.value = ''; debouncedSearch(); break;
      case 'priceMin': priceMin.value = null; fetchProducts(); break;
      case 'priceMax': priceMax.value = null; fetchProducts(); break;
      case 'inventory': inventorySignal.value = ''; fetchProducts(); break;
      case 'delivery': deliveryRegion.value = ''; fetchProducts(); break;
      case 'inStock': inStockOnly.value = false; fetchProducts(); break;
      case 'verified': verifiedOnly.value = false; fetchProducts(); break;
      case 'radius': selectedRadius.value = ''; fetchProducts(); break;
      case 'sort': sortBy.value = ''; fetchProducts(); break;
    }
  };

  const searchPlaceholder = computed(() => {
    return "Search materials (e.g. 'TMT Bars', 'Simba Cement')...";
  });

  const workflowSummary = computed(() => {
    if (loading.value) {
      return {
        stage: 'SYNCING',
        title: 'Loading the material marketplace',
        body: 'Fetching filters, materials, and location context so the next step is visible immediately.',
        primaryAction: null,
        secondaryAction: null,
      };
    }

    if (!productList.value.length) {
      return {
        stage: 'DISCOVER',
        title: 'Widen the search and reset filters',
        body: 'No products match the current search state. Reset filters or broaden the category, region, or price range to recover results.',
        primaryAction: { label: 'Reset Filters', handler: clearFilters },
        secondaryAction: { label: 'Search Again', handler: submitSearch },
      };
    }

    if (selectedForComparison.value.length) {
      return {
        stage: 'COMPARE',
        title: 'Compare shortlisted materials',
        body: 'Use the compare queue to review price, stock, certifications, and origin before requesting a quote.',
        primaryAction: { label: 'Compare Products', handler: () => { showComparisonModal.value = true; } },
        secondaryAction: { label: 'Request Quote', handler: () => { const first = selectedForComparison.value[0]; if (first) requestQuote(first); } },
      };
    }

    if (activeFiltersCount.value > 0) {
      return {
        stage: 'REFINE',
        title: 'Refine results and shortlist the best match',
        body: 'Your filters are narrowing the catalog. Compare a few candidates, then request a quote from the strongest supplier.',
        primaryAction: { label: 'Clear Filters', handler: clearFilters },
        secondaryAction: { label: 'Compare Selected', handler: () => { if (selectedForComparison.value.length) showComparisonModal.value = true; } },
      };
    }

    return {
      stage: 'BROWSE',
      title: 'Browse, compare, and request a quote',
      body: 'Start with the strongest match, compare suppliers, then use the quote path to move into checkout or delivery planning.',
      primaryAction: { label: 'Compare Products', handler: () => { if (selectedForComparison.value.length) showComparisonModal.value = true; } },
      secondaryAction: { label: 'Reset Filters', handler: clearFilters },
    };
  });

  const workflowSteps = computed(() => [
    {
      index: '01',
      label: 'Filter or search',
      help: 'Narrow by location, category, stock, or price.',
      done: activeFiltersCount.value > 0,
      active: activeFiltersCount.value === 0,
    },
    {
      index: '02',
      label: 'Compare suppliers',
      help: 'Use the compare queue to review viable options side by side.',
      done: selectedForComparison.value.length > 1,
      active: selectedForComparison.value.length === 1,
    },
    {
      index: '03',
      label: 'Request quote',
      help: 'Send the chosen product into the buyer quote workflow.',
      done: false,
      active: Boolean(selectedForComparison.value.length),
    },
    {
      index: '04',
      label: 'Track response',
      help: 'Move from quote request into order and delivery tracking.',
      done: false,
      active: false,
    },
  ]);

  const isSelectedForComparison = (id) => selectedForComparison.value.some(p => p.id === id);

  const syncCountryFilterFromStore = () => {
    const country = configStore.activeCountry;
    selectedCountry.value = country?.iso_code ? String(country.iso_code) : '';
  };

  const syncStoreFromCountryFilter = () => {
    if (!selectedCountry.value) return;
    const country = configStore.countries.find((item) => String(item.iso_code).toUpperCase() === String(selectedCountry.value).toUpperCase());
    if (country && country.iso_code !== configStore.activeCountryCode) {
      configStore.setCountry(country.iso_code);
    }
  };

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
        country: selectedCountry.value || '',
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
      console.log('[ProductList] fetching with params:', JSON.stringify(params));
      const response = await api.get('/v1/products/', { params });
      console.log('[ProductList] received', (response.data.results || response.data || []).length, 'products');

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
    router.push({ path: `/products/${product.id}`, query: { currency: displayCurrencyCode.value } });
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

  const inventoryBadgeVariant = (signal) => {
    if (signal === 'OUT_OF_STOCK') return 'danger';
    if (signal === 'LOW_STOCK') return 'warning';
    return 'success';
  };

  const formatInventorySignal = (signal) => {
    if (signal === 'OUT_OF_STOCK') return 'Out of Stock';
    if (signal === 'LOW_STOCK') return 'Low Stock';
    return 'In Stock';
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
    selectedCountry.value = regionalDefaultCountryCode.value;
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
    syncStoreFromCountryFilter();
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
    syncCountryFilterFromStore();
    fetchCategories();
    fetchLocations();
    fetchProducts();
  });

  watch(
    () => configStore.activeCountryCode,
    () => {
      syncCountryFilterFromStore();
      fetchLocations();
      fetchProducts();
    }
  );

  watch(
    selectedCountry,
    () => {
      syncStoreFromCountryFilter();
    }
  );

  watch(searchQuery, () => {
    debouncedSearch();
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

  /* Filter Rail */
  .pz-filter-rail {
    position: sticky;
    top: 6.5rem;
    display: grid;
    gap: 0.5rem;
    padding: 1.25rem;
    background: #ffffff;
    border: 1px solid rgba(10, 10, 15, 0.06);
    border-radius: 20px;
    box-shadow:
      0 1px 2px rgba(10, 10, 15, 0.02),
      0 4px 16px rgba(10, 10, 15, 0.04);
  }

  .pz-filter-rail__header {
    display: flex;
    align-items: start;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.5rem;
    margin-bottom: 0.25rem;
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

  /* Filter Section (collapsible) */
  .pz-filter-section {
    border-bottom: 1px solid rgba(10, 10, 15, 0.06);
  }

  .pz-filter-section__trigger {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.65rem 0;
    background: none;
    border: none;
    font-family: var(--pz-font-display);
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--pz-color-foundation-black);
    cursor: pointer;
    text-align: left;
  }

  .pz-filter-section__icon {
    width: 1rem;
    height: 1rem;
    color: var(--pz-color-concrete-grey);
    transition: transform 0.2s ease;
    flex-shrink: 0;
  }

  .pz-filter-section__icon.is-open {
    transform: rotate(180deg);
  }

  .pz-filter-section__body {
    display: grid;
    gap: 0.65rem;
    padding-bottom: 0.75rem;
  }

  /* Filter Field */
  .pz-filter-field {
    display: grid;
    gap: 0.35rem;
  }

  .pz-filter-field__label {
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--pz-color-concrete-grey);
  }

  .pz-filter-field__control {
    min-height: 40px;
    padding: 0.55rem 0.75rem;
    border: 1px solid rgba(10, 10, 15, 0.1);
    border-radius: 10px;
    background: rgba(250, 249, 245, 0.6);
    color: var(--pz-color-foundation-black);
    font-size: 0.9rem;
    width: 100%;
    transition: all 0.2s ease;
  }

  .pz-filter-field__control:focus {
    outline: none;
    border-color: var(--pz-color-earth-orange);
    box-shadow: 0 0 0 3px rgba(212, 101, 42, 0.1);
    background: white;
  }

  /* Price Range */
  .pz-filter-range {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 0.5rem;
    align-items: center;
  }

  .pz-filter-range__sep {
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    color: var(--pz-color-concrete-grey);
  }

  /* Filter Toggles (checkboxes) */
  .pz-filter-toggles {
    display: grid;
    gap: 0.6rem;
  }

  .pz-filter-toggle {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.88rem;
    color: var(--pz-color-foundation-black);
    cursor: pointer;
  }

  .pz-filter-toggle input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  .pz-toggle-check {
    width: 1.15rem;
    height: 1.15rem;
    border: 2px solid rgba(10, 10, 15, 0.15);
    border-radius: 5px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    transition: all 0.2s ease;
  }

  .pz-filter-toggle input:checked + .pz-toggle-check {
    background: var(--pz-color-earth-orange);
    border-color: var(--pz-color-earth-orange);
  }

  .pz-filter-toggle input:checked + .pz-toggle-check::after {
    content: '';
    width: 5px;
    height: 8px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg) translate(-1px, -1px);
  }

  .pz-filter-toggle input:focus + .pz-toggle-check {
    box-shadow: 0 0 0 3px rgba(212, 101, 42, 0.15);
  }

  /* Active Filter Chips */
  .pz-filter-chips {
    margin-bottom: 0.75rem;
  }

  .pz-filter-chips__scroll {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .pz-filter-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.7rem;
    background: rgba(212, 101, 42, 0.08);
    border: 1px solid rgba(212, 101, 42, 0.18);
    border-radius: 10px;
    font-size: 0.78rem;
    color: var(--pz-color-earth-orange);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .pz-filter-chip:hover {
    background: rgba(212, 101, 42, 0.14);
    border-color: rgba(212, 101, 42, 0.3);
  }

  .pz-filter-chip svg {
    width: 0.75rem;
    height: 0.75rem;
    flex-shrink: 0;
  }

  .pz-filter-chip__label {
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.75;
  }

  .pz-filter-chip__value {
    font-weight: 600;
  }

  .pz-filter-chip--clear {
    background: rgba(10, 10, 15, 0.05);
    border-color: rgba(10, 10, 15, 0.1);
    color: var(--pz-color-concrete-grey);
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .pz-filter-chip--clear:hover {
    background: rgba(10, 10, 15, 0.08);
    border-color: rgba(10, 10, 15, 0.15);
    color: var(--pz-color-foundation-black);
  }

  .pz-product-workflow-popover {
    position: relative;
    display: inline-block;
    z-index: 20;
  }

  .pz-product-workflow-trigger {
    position: relative;
    display: inline-grid;
    grid-template-columns: auto 1fr;
    column-gap: 0.75rem;
    row-gap: 0.08rem;
    min-width: 13.5rem;
    padding: 0.9rem 1.05rem;
    border: 1px solid rgba(212, 101, 42, 0.64);
    border-radius: 999px;
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 236, 213, 0.98)),
      #fff;
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.45),
      0 14px 30px rgba(212, 101, 42, 0.24);
    text-align: left;
    cursor: help;
    animation: pz-product-start-breathe 2.8s ease-in-out infinite;
    transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, filter 0.16s ease;
  }

  .pz-product-workflow-trigger::before {
    content: ">";
    grid-row: 1 / span 3;
    display: inline-flex;
    width: 2.35rem;
    height: 2.35rem;
    align-items: center;
    justify-content: center;
    align-self: center;
    border-radius: 999px;
    background: var(--pz-color-earth-orange);
    color: white;
    font-family: var(--pz-font-mono);
    font-size: 1.08rem;
    font-weight: 900;
    box-shadow: 0 8px 18px rgba(212, 101, 42, 0.3);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
  }

  .pz-product-workflow-trigger::after {
    content: "Open";
    position: absolute;
    top: -0.55rem;
    right: 1.1rem;
    display: inline-flex;
    align-items: center;
    min-height: 1.05rem;
    padding: 0 0.42rem;
    border-radius: 999px;
    background: #111827;
    color: white;
    font-family: var(--pz-font-mono);
    font-size: 0.58rem;
    font-weight: 800;
    letter-spacing: 0;
  }

  .pz-product-workflow-trigger:hover,
  .pz-product-workflow-popover:focus-within .pz-product-workflow-trigger {
    transform: translateY(-2px);
    border-color: rgba(212, 101, 42, 0.9);
    filter: saturate(1.08);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.5),
      0 18px 34px rgba(212, 101, 42, 0.34);
  }

  .pz-product-workflow-trigger:hover::before,
  .pz-product-workflow-popover:focus-within .pz-product-workflow-trigger::before {
    transform: translateX(2px) scale(1.04);
    box-shadow: 0 10px 22px rgba(212, 101, 42, 0.38);
  }

  .pz-product-workflow-trigger span {
    grid-column: 2;
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--pz-color-concrete-grey);
  }

  .pz-product-workflow-trigger strong {
    grid-column: 2;
    font-family: var(--pz-font-display);
    font-size: 1.08rem;
    color: var(--pz-color-foundation-black);
  }

  .pz-product-workflow-trigger em {
    grid-column: 2;
    color: var(--pz-color-structural-steel);
    font-family: var(--pz-font-mono);
    font-size: 0.66rem;
    font-style: normal;
    line-height: 1.25;
  }

  @keyframes pz-product-start-breathe {
    0%,
    100% {
      box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.45),
        0 12px 26px rgba(212, 101, 42, 0.2);
    }

    50% {
      box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.5),
        0 18px 36px rgba(212, 101, 42, 0.34);
    }
  }

  .pz-product-workflow-panel {
    position: absolute;
    top: calc(100% + 0.65rem);
    left: 0;
    width: min(62rem, calc(100vw - 2rem));
    padding: 1.1rem;
    border: 1px solid rgba(212, 101, 42, 0.18);
    border-radius: 14px;
    background:
      linear-gradient(145deg, rgba(255, 255, 255, 0.99), rgba(255, 247, 237, 0.98)),
      #fff;
    box-shadow:
      0 24px 60px rgba(10, 10, 15, 0.16),
      0 12px 30px rgba(212, 101, 42, 0.1);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-0.35rem);
    transition: opacity 0.16s ease, transform 0.16s ease, visibility 0.16s ease;
    pointer-events: none;
  }

  .pz-product-workflow-panel::before {
    content: "";
    position: absolute;
    top: -0.45rem;
    left: 1.6rem;
    width: 0.9rem;
    height: 0.9rem;
    transform: rotate(45deg);
    border-left: 1px solid rgba(212, 101, 42, 0.18);
    border-top: 1px solid rgba(212, 101, 42, 0.18);
    background: rgba(255, 255, 255, 0.99);
  }

  .pz-product-workflow-popover:hover .pz-product-workflow-panel,
  .pz-product-workflow-popover:focus-within .pz-product-workflow-panel {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
    pointer-events: auto;
  }

  .pz-product-workflow {
    display: grid;
    gap: 1rem;
    grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.95fr);
    align-items: start;
  }

  .pz-product-workflow__summary {
    display: grid;
    gap: 0.6rem;
  }

  .pz-product-workflow__kicker {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pz-color-concrete-grey);
  }

  .pz-product-workflow__title {
    margin: 0;
    font-family: var(--pz-font-display);
    font-size: 1.25rem;
  }

  .pz-product-workflow__body {
    max-width: 58ch;
    margin: 0;
    color: var(--pz-color-text-secondary);
    line-height: 1.55;
  }

  .pz-product-workflow__actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .pz-product-workflow__metrics {
    display: grid;
    gap: 0.75rem;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .pz-product-workflow__metric {
    display: grid;
    gap: 0.2rem;
    padding: 0.85rem 0.95rem;
    border: 1px solid rgba(10, 10, 15, 0.08);
    background: rgba(255, 255, 255, 0.8);
  }

  .pz-product-workflow__metric span {
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--pz-color-concrete-grey);
  }

  .pz-product-workflow__metric strong {
    font-family: var(--pz-font-display);
    font-size: 1rem;
  }

  .pz-product-workflow__steps {
    display: grid;
    gap: 0.75rem;
    margin-top: 1rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .pz-product-workflow-step {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.75rem;
    padding: 0.85rem 0.9rem;
    border: 1px solid rgba(10, 10, 15, 0.08);
    background: rgba(255, 255, 255, 0.9);
  }

  .pz-product-workflow-step__index {
    display: inline-grid;
    place-items: center;
    width: 1.9rem;
    height: 1.9rem;
    border: 1px solid rgba(10, 10, 15, 0.12);
    background: rgba(247, 244, 239, 0.95);
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    font-weight: 700;
  }

  .pz-product-workflow-step__content {
    display: grid;
    gap: 0.2rem;
  }

  .pz-product-workflow-step__content strong {
    font-size: 0.82rem;
  }

  .pz-product-workflow-step__content span {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    color: var(--pz-color-concrete-grey);
    line-height: 1.5;
  }

  .pz-product-workflow-step--done {
    border-color: rgba(5, 150, 105, 0.25);
  }

  .pz-product-workflow-step--active {
    border-color: rgba(212, 101, 42, 0.35);
    box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
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

  /* Product Grid & List */
  .pz-product-grid {
    display: grid;
    gap: 1.75rem;
    grid-template-columns: repeat(auto-fill, minmax(22rem, 1fr));
  }

  .pz-product-list {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr;
  }

  /* Product Card */
  .pz-product-card {
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

  .pz-product-card:hover {
    transform: translateY(-6px);
    box-shadow:
      0 8px 24px rgba(10, 10, 15, 0.06),
      0 24px 48px rgba(10, 10, 15, 0.08);
  }

  .pz-product-card:hover .pz-product-card__img {
    transform: scale(1.05);
  }

  .pz-product-card--featured {
    box-shadow:
      0 1px 2px rgba(10, 10, 15, 0.02),
      0 4px 12px rgba(10, 10, 15, 0.06),
      0 0 0 1px rgba(212, 101, 42, 0.15);
  }

  .pz-product-card--featured:hover {
    box-shadow:
      0 8px 24px rgba(10, 10, 15, 0.08),
      0 24px 48px rgba(10, 10, 15, 0.1),
      0 0 0 1px rgba(212, 101, 42, 0.25);
  }

  /* List View */
  .pz-product-card--list {
    flex-direction: row;
    align-items: stretch;
  }

  .pz-product-card--list .pz-product-card__media {
    width: 280px;
    flex-shrink: 0;
    aspect-ratio: 4 / 3;
  }

  .pz-product-card--list .pz-product-card__body {
    flex: 1;
    justify-content: center;
  }

  @media (max-width: 767px) {
    .pz-product-card--list {
      flex-direction: column;
    }
    .pz-product-card--list .pz-product-card__media {
      width: 100%;
      aspect-ratio: 3 / 2;
    }
  }

  /* Image Area */
  .pz-product-card__media {
    position: relative;
    aspect-ratio: 3 / 2;
    overflow: hidden;
    background: linear-gradient(135deg, #e8e4db, #d4cfc5);
  }

  .pz-product-card__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Badges */
  .pz-product-card__badges {
    position: absolute;
    top: 0.85rem;
    left: 0.85rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    z-index: 2;
  }

  .pz-product-card__badge {
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

  .pz-product-card__badge--featured {
    background: rgba(212, 101, 42, 0.9);
    color: white;
    border: 1px solid rgba(212, 101, 42, 0.3);
  }

  .pz-product-card__badge--new {
    background: rgba(59, 130, 246, 0.9);
    color: white;
    border: 1px solid rgba(59, 130, 246, 0.3);
  }

  .pz-product-card__badge--sale {
    background: rgba(16, 185, 129, 0.9);
    color: white;
    border: 1px solid rgba(16, 185, 129, 0.3);
  }

  .pz-product-card__badge--success {
    background: rgba(34, 139, 34, 0.9);
    color: white;
    border: 1px solid rgba(34, 139, 34, 0.3);
  }

  .pz-product-card__badge--warning {
    background: rgba(217, 119, 6, 0.9);
    color: white;
    border: 1px solid rgba(217, 119, 6, 0.3);
  }

  .pz-product-card__badge--danger {
    background: rgba(220, 38, 38, 0.9);
    color: white;
    border: 1px solid rgba(220, 38, 38, 0.3);
  }

  /* Card Body */
  .pz-product-card__body {
    padding: 1.25rem 1.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
  }

  .pz-product-card__eyebrow {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--pz-color-earth-orange);
  }

  .pz-product-card__title {
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

  .pz-product-card__location {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--pz-color-concrete-grey);
    font-size: 0.85rem;
    line-height: 1.4;
    margin-top: 0.1rem;
  }

  .pz-product-card__location svg {
    width: 0.85rem;
    height: 0.85rem;
    flex-shrink: 0;
    color: var(--pz-color-earth-orange);
  }

  /* Specs Row */
  .pz-product-card__specs {
    display: flex;
    gap: 1rem;
    padding: 0.5rem 0;
    border-top: 1px solid rgba(10, 10, 15, 0.06);
    border-bottom: 1px solid rgba(10, 10, 15, 0.06);
    margin-top: 0.2rem;
  }

  .pz-product-card__spec {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    color: var(--pz-color-structural-steel);
    font-size: 0.82rem;
    font-weight: 500;
  }

  .pz-product-card__spec svg {
    width: 0.9rem;
    height: 0.9rem;
    color: var(--pz-color-concrete-grey);
    flex-shrink: 0;
  }

  /* Attribute line */
  .pz-product-card__attribute {
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    color: var(--pz-color-concrete-grey);
    letter-spacing: 0.02em;
  }

  /* Feature Pills */
  .pz-product-card__features {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.1rem;
  }

  .pz-product-card__features span {
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

  /* Price Row */
  .pz-product-card__price-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-top: auto;
    padding-top: 0.75rem;
  }

  .pz-product-card__price {
    font-family: var(--pz-font-display);
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--pz-color-foundation-black);
    letter-spacing: -0.02em;
    line-height: 1.1;
  }

  .pz-product-card__unit {
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    color: var(--pz-color-concrete-grey);
    font-weight: 600;
  }

  /* Footer */
  .pz-product-card__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(10, 10, 15, 0.06);
    margin-top: 0.5rem;
  }

  .pz-product-card__vendor {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 0;
  }

  .pz-product-card__vendor-avatar {
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 50%;
    background: rgba(10, 10, 15, 0.06);
    display: grid;
    place-items: center;
    flex-shrink: 0;
  }

  .pz-product-card__vendor-avatar svg {
    width: 0.9rem;
    height: 0.9rem;
    color: var(--pz-color-concrete-grey);
  }

  .pz-product-card__vendor span {
    font-size: 0.85rem;
    color: var(--pz-color-structural-steel);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    gap: 0.5rem;
  }

  .pz-mobile-filter-sheet .pz-filter-section {
    border-bottom: 1px solid rgba(10, 10, 15, 0.08);
  }

  .pz-mobile-filter-sheet .pz-filter-section__trigger {
    padding: 0.75rem 0;
    font-size: 1rem;
  }

  .pz-mobile-filter-sheet .pz-filter-section__body {
    padding-bottom: 1rem;
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

  @media (max-width: 1024px) {
    .pz-product-workflow-panel {
      left: 50%;
      width: min(34rem, calc(100vw - 2rem));
      transform: translate(-50%, -0.35rem);
    }

    .pz-product-workflow-popover:hover .pz-product-workflow-panel,
    .pz-product-workflow-popover:focus-within .pz-product-workflow-panel {
      transform: translate(-50%, 0);
    }

    .pz-product-workflow,
    .pz-product-workflow__metrics,
    .pz-product-workflow__steps {
      grid-template-columns: 1fr;
    }

    .pz-product-grid {
      grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
    }
  }

  @media (max-width: 767px) {
    .pz-marketplace-shell {
      padding: 0 1rem;
    }

    .pz-product-workflow {
      gap: 0.75rem;
    }

    .quote-ticker {
      margin-bottom: 1rem;
    }

    .marketplace-controls {
      align-items: flex-start;
    }

    .pz-product-grid {
      grid-template-columns: 1fr;
    }

    .pz-product-card__footer {
      flex-direction: column;
      align-items: stretch;
    }

    .pz-mobile-filter-trigger {
      bottom: 1rem;
      right: 1rem;
    }
  }

  /* Comparison Table */
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
</style>
