<template>
  <div class="vendor-inventory-section" :class="{ 'pz-field-ops': fieldOpsMode }">
    <!-- Celebration Overlay -->
    <Transition name="pz-celebration">
      <div v-if="showCelebration" class="pz-celebration-overlay" role="alert" aria-live="polite">
        <div class="pz-celebration__confetti">
          <div v-for="n in 30" :key="n" class="pz-confetti" :style="confettiStyle(n)"></div>
        </div>
        <div class="pz-celebration__content">
          <div class="pz-celebration__emoji">🎉</div>
          <h2 class="pz-celebration__title">Your material is live!</h2>
          <p class="pz-celebration__body">Buyers can now discover and request quotes for your product.</p>
          <Button variant="primary" @click="showCelebration = false">Start Selling</Button>
        </div>
      </div>
    </Transition>

    <!-- Screen reader live region for dynamic updates -->
    <div aria-live="polite" aria-atomic="true" class="u-sr-only">
      {{ liveRegionMessage }}
    </div>
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start">
        <div>
          <div class="pz-section-shell__eyebrow">Your Products</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">Product Catalog</h3>
          <div class="pz-section-shell__meta">Manage your inventory, pricing, and product details. Complete listings get more quotes from buyers.</div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
          <Button size="sm" variant="ghost" :loading="downloadingTemplate" @click="downloadTemplate">Download Template</Button>
          <Button v-if="isExperiencedVendor" size="sm" variant="secondary" @click="showCsvWizard = true">Import CSV</Button>
          <Button size="sm" variant="secondary" @click="openBulkAdjustModal">Bulk Adjust</Button>
          <Button size="sm" @click="openCreateModal">Add Product</Button>
          <Button
            size="sm"
            variant="ghost"
            :class="{ 'pz-field-ops-toggle--active': fieldOpsMode }"
            @click="fieldOpsMode = !fieldOpsMode"
          >
            {{ fieldOpsMode ? '🏭 Standard' : '🏭 Field Ops' }}
          </Button>
        </div>
      </div>

      <!-- Approval Blocker -->
    <div v-if="vendorStatus && vendorStatus !== 'APPROVED'" class="pz-approval-blocker">
      <div class="pz-approval-blocker__icon">⏳</div>
      <h4 class="pz-approval-blocker__title">
        {{ vendorStatus === 'PENDING' ? 'Your account is under review' : 'Account not approved' }}
      </h4>
      <p class="pz-approval-blocker__body">
        {{ vendorStatus === 'PENDING'
          ? 'You\'ll be able to publish products and receive quotes once your vendor profile is approved. Typical review time is 1–2 business days.'
          : 'Your vendor account needs to be approved before you can manage inventory. Please contact support for assistance.'
        }}
      </p>
      <div class="pz-approval-blocker__actions">
        <Button variant="primary" :loading="downloadingTemplate" @click="downloadTemplate">Download CSV Template</Button>
        <Button variant="ghost" @click="$emit('navigate', 'profile')">View Profile</Button>
      </div>
    </div>

    <div v-else class="pz-section-shell__content">
        <VendorWorkspaceHeader
          :products="products"
          :unresponded-quotes="unrespondedQuotes"
          :backend-recommendations="backendRecommendations"
          :avg-response-time-hours="vendorProfile?.avg_response_time_hours"
          :vendor-status="vendorProfile?.verified_status"
          :performance-metrics="{
            activeProducts: dashboardStats?.active_products || products.filter(p => p.status === 'ACTIVE').length,
            viewsThisWeek: dashboardStats?.views_this_week || 0,
            quotesThisMonth: dashboardStats?.quotes_this_month || 0,
            conversionRate: dashboardStats?.conversion_rate || 0,
          }"
          @restock="openAdjustmentModal"
          @edit="openEditModal"
          @respond-quote="$emit('show-alert', 'Quote response opens from the Quotes tab.', 'info')"
          @add-certs="$emit('show-alert', 'Select a product and edit its Compliance tab to add certifications.', 'info')"
        />
        <VendorPerformanceChart :data="dailyStats" class="u-mb-6" />

        <!-- Notification Panel -->
        <VendorNotificationPanel
          v-if="vendorNotifications.length"
          :notifications="vendorNotifications"
          class="u-mb-6"
          @action="handleNotificationAction"
        />

        <div class="pz-inventory-toolbar u-mb-6">
          <div class="pz-inventory-toolbar__search">
            <label class="pz-inventory-toolbar__label" for="vendor-inventory-search">Search inventory</label>
            <input
              id="vendor-inventory-search"
              v-model.trim="searchQuery"
              type="search"
              class="pz-inventory-toolbar__input"
              placeholder="Search by material, category, brand, SKU, origin, or description"
            >
          </div>
          <div class="pz-inventory-toolbar__meta">
            <span>{{ filteredProducts.length }} visible</span>
            <Button v-if="searchQuery" size="sm" variant="ghost" @click="searchQuery = ''">Clear Search</Button>
          </div>
        </div>

        <div v-if="loading" class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">Loading your products...</div>
        </div>

        <!-- Guided Empty State -->
        <div v-else-if="products.length === 0" class="pz-empty-state pz-empty-state--guided">
          <div class="pz-empty-state__glyph">🏗️</div>
          <div class="pz-empty-state__eyebrow">Your Catalog is Empty</div>
          <h4 class="pz-empty-state__title">Start selling construction materials</h4>
          <p class="pz-empty-state__body">Publish your first material to begin receiving quote requests from project owners.</p>
          <div class="pz-empty-state__actions">
            <Button variant="primary" @click="openCreateModal">🚀 Publish First Material</Button>
            <Button variant="secondary" :loading="downloadingTemplate" @click="downloadTemplate">📥 Download CSV Template</Button>
          </div>
          <div class="pz-empty-state__tips">
            <p>💡 Products with photos and certifications get 5× more quotes.</p>
            <p>⏱️ Setup time: ~5 minutes per product</p>
          </div>
        </div>

        <div v-else-if="filteredProducts.length === 0" class="pz-empty-state">
          <div class="pz-empty-state__glyph">🔍</div>
          <div class="pz-empty-state__eyebrow">Search Results</div>
          <h4 class="pz-empty-state__title">No inventory items match this search.</h4>
          <p class="pz-empty-state__body">Try a broader material name, category, brand, origin, or SKU term.</p>
        </div>

        <!-- Operational Card Groups -->
        <div v-else class="vpc-groups">
          <!-- Needs Attention -->
          <div v-if="attentionProducts.length" class="vpc-group">
            <div class="vpc-group__header">
              <span class="vpc-group__title">⚠️ Needs Attention</span>
              <span class="vpc-group__count">{{ attentionProducts.length }}</span>
            </div>
            <div class="vpc-group__list">
              <VendorProductCard
                v-for="product in attentionProducts"
                :key="product.id"
                :product="product"
                :placeholder-image="placeholderImage"
                :display-currency="configStore.activeCurrencyCode"
                @edit="openEditModal"
                @delete="deleteProduct"
                @adjust="openAdjustmentModal"
                @history="openHistoryModal"
                @toggle-status="toggleProductStatus"
                @context="openContextMenu"
              />
            </div>
          </div>

          <!-- Healthy -->
          <div v-if="healthyProducts.length" class="vpc-group">
            <div class="vpc-group__header">
              <span class="vpc-group__title">✅ Healthy Listings</span>
              <span class="vpc-group__count">{{ healthyProducts.length }}</span>
            </div>
            <div class="vpc-group__list">
              <VendorProductCard
                v-for="product in healthyProducts"
                :key="product.id"
                :product="product"
                :placeholder-image="placeholderImage"
                :display-currency="configStore.activeCurrencyCode"
                @edit="openEditModal"
                @delete="deleteProduct"
                @adjust="openAdjustmentModal"
                @history="openHistoryModal"
                @toggle-status="toggleProductStatus"
                @context="openContextMenu"
              />
            </div>
          </div>

          <!-- Drafts -->
          <div v-if="draftProducts.length" class="vpc-group">
            <div class="vpc-group__header">
              <span class="vpc-group__title">📝 Drafts</span>
              <span class="vpc-group__count">{{ draftProducts.length }}</span>
            </div>
            <div class="vpc-group__list">
              <VendorProductCard
                v-for="product in draftProducts"
                :key="product.id"
                :product="product"
                :placeholder-image="placeholderImage"
                :display-currency="configStore.activeCurrencyCode"
                @edit="openEditModal"
                @delete="deleteProduct"
                @adjust="openAdjustmentModal"
                @history="openHistoryModal"
                @toggle-status="toggleProductStatus"
                @context="openContextMenu"
              />
            </div>
          </div>

          <!-- Hidden / Disabled -->
          <div v-if="hiddenProducts.length" class="vpc-group">
            <div class="vpc-group__header">
              <span class="vpc-group__title">🚫 Hidden</span>
              <span class="vpc-group__count">{{ hiddenProducts.length }}</span>
            </div>
            <div class="vpc-group__list">
              <VendorProductCard
                v-for="product in hiddenProducts"
                :key="product.id"
                :product="product"
                :placeholder-image="placeholderImage"
                :display-currency="configStore.activeCurrencyCode"
                @edit="openEditModal"
                @delete="deleteProduct"
                @adjust="openAdjustmentModal"
                @history="openHistoryModal"
                @toggle-status="toggleProductStatus"
                @context="openContextMenu"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :isOpen="showProductModal" :title="editingProductId ? 'Edit Product' : 'Add New Product'" size="xl" @close="closeProductModal">
      <form id="product-form" class="pz-product-form" novalidate @submit.prevent="saveProduct" @keydown="handleWizardKeydown">
        <!-- Wizard Step Indicator (creation mode only) -->
        <div v-if="wizardMode && !editingProductId" class="pz-wizard-bar">
          <div class="pz-wizard-steps">
            <div
              v-for="n in totalSteps"
              :key="n"
              class="pz-wizard-step"
              :class="{
                'pz-wizard-step--active': currentStep === n,
                'pz-wizard-step--done': currentStep > n,
              }"
            >
              <div class="pz-wizard-step__bubble">{{ n < totalSteps ? n : '✓' }}</div>
              <div class="pz-wizard-step__label">
                {{ n === 1 ? 'Commercial' : n === 2 ? 'Technical' : n === 3 ? 'Compliance' : n === 4 ? 'Documents' : n === 5 ? 'Media' : 'Review' }}
              </div>
            </div>
          </div>
          <div class="pz-wizard-readiness">
            <div class="pz-wizard-readiness__bar">
              <div class="pz-wizard-readiness__fill" :style="{ width: `${readinessScore}%` }"></div>
            </div>
            <span class="pz-wizard-readiness__label">{{ readinessScore }}% — {{ readinessLabel }}</span>
          </div>
        </div>

        <!-- Tab Navigation (edit mode only) -->
        <div v-else class="pz-modal-tabs">
          <button
            v-for="tab in materialFormTabs"
            :key="tab.id"
            type="button"
            class="pz-modal-tab"
            :class="{ 'pz-modal-tab--active': activeProductTab === tab.id }"
            @click="activeProductTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <div v-show="activeProductTab === 'commercial'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Step 1 of 5</div>
              <h4>Pricing & Basics</h4>
            </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
            <div>
              <PzInput v-model="productForm.name" label="Material Name" required />
              <!-- Duplicate Detection Warning -->
              <div v-if="duplicateProductWarning" class="pvd-warning pvd-warning--duplicate">
                <span class="pvd-warning__icon">⚠️</span>
                <span class="pvd-warning__text">
                  You already have "{{ duplicateProductWarning.name }}". Are you sure you want to publish another?
                </span>
              </div>
              <!-- Smart Category Suggestion -->
              <div v-else-if="suggestedCategory && !productForm.category" class="pvd-suggestion">
                <span class="pvd-suggestion__icon">💡</span>
                <span class="pvd-suggestion__text">
                  Suggested category: <strong>{{ suggestedCategory.name }}</strong>
                </span>
                <Button size="xs" variant="ghost" @click="productForm.category = suggestedCategory.id">Use this</Button>
              </div>
            </div>
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Category</label>
              <select v-model="productForm.category" name="category" class="pz-input" required>
                <option disabled value="">Select category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </div>
            <PzInput v-model="productForm.unit" label="Unit of Sale" required />
            <div>
              <PzInput v-model.number="productForm.base_price" label="Base Price" type="number" required />
              <!-- Price Anomaly Warning -->
              <div v-if="priceAnomaly" class="pvd-warning" :class="`pvd-warning--${priceAnomaly.severity}`">
                <span class="pvd-warning__icon">{{ priceAnomaly.type === 'high' ? '🔺' : '🔻' }}</span>
                <span class="pvd-warning__text">{{ priceAnomaly.message }}</span>
              </div>
            </div>
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Currency</label>
              <select v-model="productForm.currency" name="currency" class="pz-input" required>
                <option v-for="currency in supportedCurrencies" :key="currency.currency_code" :value="currency.currency_code">
                  {{ currency.currency_code }}{{ currency.symbol ? ` (${currency.symbol})` : '' }}
                </option>
              </select>
            </div>
            <template v-if="isExperiencedVendor">
              <PzInput v-model.number="productForm.bulk_price" label="Bulk Price" type="number" />
              <PzInput v-model.number="productForm.bulk_threshold" label="Bulk Threshold" type="number" />
            </template>
            <PzInput v-model.number="productForm.stock_quantity" label="Stock Quantity" type="number" required />
            <PzInput v-model.number="productForm.reorder_level" label="Reorder Threshold" type="number" />
            <PzInput v-model.number="productForm.min_order_quantity" label="Min Order Qty" type="number" />
            <PzInput v-model.number="productForm.max_order_quantity" label="Max Order Qty" type="number" />
            <PzInput v-model="productForm.brand" label="Brand" />
            <PzInput v-model="productForm.model_number" label="Model / SKU" />
            <PzInput v-model="productForm.quality_grade" label="Quality Grade" />
            <PzInput v-model="productForm.country_of_origin" label="Country of Origin" />
            <PzInput v-model="productForm.packaging_details" label="Packaging Details" />
            <PzInput v-model.number="productForm.estimated_delivery_days" label="Lead Time (Days)" type="number" />
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Status</label>
              <select v-model="productForm.status" class="pz-input">
                <option value="ACTIVE">ACTIVE</option>
                <option value="DRAFT">DRAFT</option>
                <option value="OUT_OF_STOCK">OUT_OF_STOCK</option>
                <option value="DISABLED">DISABLED</option>
              </select>
            </div>
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Marketing Flags</label>
              <div class="pz-checkbox-row">
                <label class="pz-checkbox">
                  <input v-model="productForm.is_featured" type="checkbox">
                  <span>Featured</span>
                </label>
                <label v-if="isExperiencedVendor" class="pz-checkbox">
                  <input v-model="productForm.is_new_arrival" type="checkbox">
                  <span>New Arrival</span>
                </label>
                <label v-if="isExperiencedVendor" class="pz-checkbox">
                  <input v-model="productForm.is_on_sale" type="checkbox">
                  <span>On Sale</span>
                </label>
              </div>
              <p v-if="!isExperiencedVendor" class="pvd-progressive-hint">
                💡 New Arrival and On Sale unlock after your first 3 products.
              </p>
            </div>
          </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4 u-mt-4">
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.short_description" label="Short Description" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.description" label="Detailed Description" type="textarea" required />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.delivery_regions_text" label="Delivery Regions" help-text="Comma-separated, e.g. NAIROBI, MOMBASA, KISUMU" />
              <!-- Delivery Region Suggestions -->
              <div v-if="suggestedDeliveryRegions.length && !productForm.delivery_regions_text" class="pvd-suggestion pvd-suggestion--inline">
                <span class="pvd-suggestion__icon">🚚</span>
                <span class="pvd-suggestion__text">Popular regions:</span>
                <button
                  v-for="region in suggestedDeliveryRegions"
                  :key="region"
                  type="button"
                  class="pvd-suggestion__chip"
                  @click="addDeliveryRegion(region)"
                >
                  + {{ region }}
                </button>
              </div>
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.features_text" label="Feature Highlights" type="textarea" help-text="One feature per line" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.applications_text" label="Applications" type="textarea" help-text="One use case per line" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.handling_instructions" label="Handling Instructions" type="textarea" />
            </div>
          </div>
          </section>
        </div>

        <div v-show="activeProductTab === 'technical'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Technical Layer</div>
              <h4>Structured Attributes</h4>
              <Button size="sm" variant="ghost" type="button" @click="addAttribute">Add Attribute</Button>
            </div>
          <div v-if="productForm.attribute_entries.length" class="pz-repeaters">
            <div v-for="(attribute, index) in productForm.attribute_entries" :key="`attribute-${index}`" class="pz-repeater-row">
              <PzInput v-model="attribute.group" label="Group" />
              <PzInput v-model="attribute.name" label="Name" />
              <PzInput v-model="attribute.value" label="Value" />
              <PzInput v-model="attribute.unit" label="Unit" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Highlight</label>
                <select v-model="attribute.is_highlight" class="pz-input">
                  <option :value="false">No</option>
                  <option :value="true">Yes</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeAttribute(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No structured attributes added yet.</p>
          </section>
        </div>

        <div v-show="activeProductTab === 'compliance'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Step 3 of 5</div>
              <h4>Certifications</h4>
              <Button size="sm" variant="ghost" type="button" @click="addCertification">Add Certification</Button>
            </div>

            <!-- Certification Gap Suggestions -->
            <div v-if="suggestedCertifications.length" class="pvd-suggestion pvd-suggestion--block">
              <div class="pvd-suggestion__header">
                <span class="pvd-suggestion__icon">🏅</span>
                <span class="pvd-suggestion__text">
                  Common certifications for <strong>{{ currentCategoryName }}</strong>:
                </span>
              </div>
              <div class="pvd-suggestion__chips">
                <button
                  v-for="cert in suggestedCertifications"
                  :key="cert.name"
                  type="button"
                  class="pvd-suggestion__chip"
                  @click="addSuggestedCertification(cert)"
                >
                  + {{ cert.name }}
                </button>
              </div>
            </div>

          <div v-if="productForm.certification_entries.length" class="pz-repeaters">
            <div v-for="(certification, index) in productForm.certification_entries" :key="`certification-${index}`" class="pz-repeater-row">
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Registry</label>
                <select v-model="certification.registry" class="pz-input">
                  <option :value="null">Custom</option>
                  <option v-for="option in certificationOptions" :key="option.id" :value="option.id">{{ option.name }}</option>
                </select>
              </div>
              <PzInput v-model="certification.display_name" label="Display Name" />
              <PzInput v-model="certification.certification_number" label="Reference Number" />
              <PzInput v-model="certification.issuing_body" label="Issuing Body" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Status</label>
                <select v-model="certification.status" class="pz-input">
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="PENDING">PENDING</option>
                  <option value="EXPIRED">EXPIRED</option>
                  <option value="REVOKED">REVOKED</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeCertification(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No certification records added yet.</p>
          </section>
        </div>

        <div v-show="activeProductTab === 'documents'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Step 4 of 5</div>
              <h4>Documents</h4>
              <Button size="sm" variant="ghost" type="button" @click="addDocument">Add Document</Button>
            </div>
          <div v-if="productForm.documents.length" class="pz-repeaters">
            <div v-for="(document, index) in productForm.documents" :key="`document-${index}`" class="pz-repeater-row">
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Document Type</label>
                <select v-model="document.document_type" class="pz-input">
                  <option value="DATASHEET">DATASHEET</option>
                  <option value="SAFETY">SAFETY</option>
                  <option value="WARRANTY">WARRANTY</option>
                  <option value="BROCHURE">BROCHURE</option>
                  <option value="INSTALLATION">INSTALLATION</option>
                  <option value="OTHER">OTHER</option>
                </select>
              </div>
              <PzInput v-model="document.title" label="Title" />
              <PzInput v-model="document.external_url" label="External URL" />
              <PzInput v-model="document.description" label="Description" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Visibility</label>
                <select v-model="document.is_public" class="pz-input">
                  <option :value="true">Public</option>
                  <option :value="false">Internal</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeDocument(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No supporting documents added yet.</p>
          </section>
        </div>

        <div v-show="activeProductTab === 'media'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Step 5 of 5</div>
              <h4>Photos & Files</h4>
            </div>

          <div v-if="editingProduct?.images?.length || editingProduct?.documents?.length" class="pz-existing-assets">
            <div v-if="editingProduct?.images?.length" class="pz-existing-assets__group">
              <div class="pz-existing-assets__title">Existing Images</div>
              <div class="pz-chip-list">
                <span v-for="image in editingProduct.images" :key="image.id" class="pz-chip pz-chip--removable">
                  {{ image.alt_text || `Image ${image.display_order + 1}` }}
                  <button type="button" class="pz-chip__remove" title="Delete image" @click="deleteProductImage(image)">×</button>
                </span>
              </div>
            </div>
            <div v-if="editingProduct?.documents?.length" class="pz-existing-assets__group">
              <div class="pz-existing-assets__title">Existing Documents</div>
              <div class="pz-chip-list">
                <span v-for="document in editingProduct.documents" :key="document.id" class="pz-chip pz-chip--removable">
                  {{ document.title }}
                  <button type="button" class="pz-chip__remove" title="Delete document" @click="deleteProductDocument(document)">×</button>
                </span>
              </div>
            </div>
          </div>

          <div class="pz-upload-grid">
            <div class="pz-upload-card">
              <div class="pz-upload-card__title">Product Images</div>
              <p class="pz-u-color-steel text-sm">Upload one or multiple images for the same material.</p>
              <input
                ref="productImageInput"
                type="file"
                accept="image/*"
                multiple
                class="u-sr-only"
                @change="handleProductImagesSelected"
              >
              <input
                ref="cameraInput"
                type="file"
                accept="image/*"
                capture="environment"
                class="u-sr-only"
                @change="handleProductImagesSelected"
              >
              <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                <Button size="sm" variant="secondary" type="button" @click="triggerProductImageUpload">Upload Images</Button>
                <Button size="sm" variant="secondary" type="button" class="u-show-mobile" @click="triggerCameraCapture">📷 Take Photo</Button>
                <Button
                  v-if="selectedProductImageFiles.length"
                  size="sm"
                  variant="ghost"
                  type="button"
                  @click="clearSelectedProductImages"
                >
                  Clear Images
                </Button>
              </div>
              <div v-if="selectedProductImageFiles.length" class="pz-upload-selection">
                {{ selectedProductImageFiles.length }} image{{ selectedProductImageFiles.length === 1 ? '' : 's' }} queued for upload on save.
              </div>
              <div v-if="imageValidationWarnings.length" class="pvd-image-warnings">
                <div v-for="(warn, i) in imageValidationWarnings" :key="i" class="pvd-warning pvd-warning--warning">
                  <span class="pvd-warning__icon">📷</span>
                  <span class="pvd-warning__text">{{ warn }}</span>
                </div>
              </div>
            </div>

            <div class="pz-upload-card">
              <div class="pz-upload-card__title">Product Documents</div>
              <p class="pz-u-color-steel text-sm">Upload datasheets, brochures, warranties, or other supporting files.</p>
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Uploaded document type</label>
                <select v-model="uploadDocumentType" class="pz-input">
                  <option value="DATASHEET">DATASHEET</option>
                  <option value="SAFETY">SAFETY</option>
                  <option value="WARRANTY">WARRANTY</option>
                  <option value="BROCHURE">BROCHURE</option>
                  <option value="INSTALLATION">INSTALLATION</option>
                  <option value="OTHER">OTHER</option>
                </select>
              </div>
              <input
                ref="productDocumentInput"
                type="file"
                multiple
                class="u-sr-only"
                @change="handleProductDocumentsSelected"
              >
              <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                <Button size="sm" variant="secondary" type="button" @click="triggerProductDocumentUpload">Upload Documents</Button>
                <Button
                  v-if="selectedProductDocumentFiles.length"
                  size="sm"
                  variant="ghost"
                  type="button"
                  @click="clearSelectedProductDocuments"
                >
                  Clear Documents
                </Button>
              </div>
              <div v-if="selectedProductDocumentFiles.length" class="pz-upload-selection">
                {{ selectedProductDocumentFiles.length }} document{{ selectedProductDocumentFiles.length === 1 ? '' : 's' }} queued for upload on save.
              </div>
            </div>
          </div>
          </section>
        </div>

        <!-- Review Step -->
        <div v-show="activeProductTab === 'review'" class="pz-modal-panel">
          <section class="pz-form-section">
            <div class="pz-form-section__header">
              <div class="pz-form-section__eyebrow">Step 6 of 6</div>
              <h4>Review Before Publishing</h4>
            </div>
            <div class="pz-review-card">
              <div class="pz-review-card__preview">
                <div class="pz-review-card__image">
                  <img v-if="selectedProductImageFiles.length" :src="URL.createObjectURL(selectedProductImageFiles[0])" alt="Preview">
                  <div v-else class="pz-review-card__no-image">📸 No image uploaded</div>
                </div>
                <div class="pz-review-card__info">
                  <h3>{{ productForm.name || 'Untitled Material' }}</h3>
                  <p class="pz-review-card__price">
                    {{ configStore.formatPrice(productForm.base_price, productForm.currency, configStore.activeCurrencyCode) }}
                    <span v-if="productForm.bulk_price"> — Bulk: {{ configStore.formatPrice(productForm.bulk_price, productForm.currency, configStore.activeCurrencyCode) }}</span>
                  </p>
                  <p class="pz-review-card__desc">{{ productForm.short_description || productForm.description || 'No description provided.' }}</p>
                  <div class="pz-review-card__meta">
                    <span v-if="productForm.brand">Brand: {{ productForm.brand }}</span>
                    <span>Stock: {{ productForm.stock_quantity }} {{ productForm.unit }}</span>
                    <span>Min Order: {{ productForm.min_order_quantity }}</span>
                  </div>
                </div>
              </div>
              <div class="pz-review-checklist">
                <div class="pz-review-checklist__title">Readiness Checklist</div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': productForm.name }">
                  {{ productForm.name ? '✅' : '⬜' }} Material name
                </div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': productForm.category }">
                  {{ productForm.category ? '✅' : '⬜' }} Category selected
                </div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': productForm.base_price > 0 }">
                  {{ productForm.base_price > 0 ? '✅' : '⬜' }} Price set
                </div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': productForm.description }">
                  {{ productForm.description ? '✅' : '⬜' }} Description
                </div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': selectedProductImageFiles.length }">
                  {{ selectedProductImageFiles.length ? '✅' : '⚠️' }} Photos ({{ selectedProductImageFiles.length || 'none' }})
                </div>
                <div class="pz-review-checklist__item" :class="{ 'pz-review-checklist__item--ok': productForm.certification_entries?.length }">
                  {{ productForm.certification_entries?.length ? '✅' : '⚠️' }} Certifications ({{ productForm.certification_entries?.length || 'none' }})
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Wizard Gate Error -->
        <div v-if="wizardGateError" class="pz-wizard-gate-error">
          <span class="pz-wizard-gate-error__icon">⚠️</span>
          <span class="pz-wizard-gate-error__text">{{ wizardGateError }}</span>
        </div>

        <!-- Wizard Navigation -->
        <div v-if="wizardMode && !editingProductId" class="pz-wizard-nav">
          <Button
            type="button"
            variant="ghost"
            :disabled="currentStep <= 1"
            @click="prevStep"
          >
            ← Previous
          </Button>
          <Button
            v-if="currentStep < totalSteps"
            type="button"
            variant="secondary"
            :disabled="!canAdvanceFromStep(currentStep).valid"
            @click="nextStep"
          >
            Next Step →
          </Button>
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeProductModal">Cancel</Button>
        <Button
          v-if="wizardMode && !editingProductId && currentStep < totalSteps"
          type="button"
          variant="primary"
          :disabled="!canAdvanceFromStep(currentStep).valid"
          @click="nextStep"
        >
          Continue
        </Button>
        <Button
          v-else
          type="submit"
          form="product-form"
          variant="primary"
          :loading="saving"
        >
          {{ editingProductId ? 'Save Material' : 'Publish Material' }}
        </Button>
      </template>
    </Modal>

    <Modal :isOpen="showAdjustmentModal" title="Adjust Stock Level" size="md" @close="closeAdjustmentModal">
      <form id="inventory-adjustment-form" class="pz-product-form" @submit.prevent="submitInventoryAdjustment">
        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div>
              <div class="pz-form-section__eyebrow">Stock Ledger</div>
              <h4>{{ selectedInventoryProduct?.name || 'Selected Material' }}</h4>
            </div>
          </div>
          <div class="pz-inventory-adjustment__summary">
            <div>
              <span>On hand</span>
              <strong>{{ selectedInventoryProduct?.stock_quantity ?? 0 }}</strong>
            </div>
            <div>
              <span>Available</span>
              <strong>{{ selectedInventoryProduct?.available_quantity ?? selectedInventoryProduct?.stock_quantity ?? 0 }}</strong>
            </div>
            <div>
              <span>Reorder at</span>
              <strong>{{ selectedInventoryProduct?.reorder_level ?? 0 }}</strong>
            </div>
          </div>

          <!-- Stock-Out Prediction -->
          <div v-if="stockOutPrediction" class="pvd-stock-prediction" :class="`pvd-stock-prediction--${stockOutPrediction.severity}`">
            <span class="pvd-stock-prediction__icon">📊</span>
            <div class="pvd-stock-prediction__body">
              <div class="pvd-stock-prediction__message">{{ stockOutPrediction.message }}</div>
              <div v-if="stockOutPrediction.days_until_stockout" class="pvd-stock-prediction__meta">
                {{ stockOutPrediction.current_stock }} in stock • {{ stockOutPrediction.daily_quote_rate }} units/day quote rate
              </div>
            </div>
          </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
            <PzInput v-model.number="inventoryAdjustmentForm.quantity_delta" label="Quantity Delta" type="number" required help-text="Use positive values to restock and negative values to remove stock." />
            <PzInput v-model="inventoryAdjustmentForm.reference" label="Reference" help-text="e.g. GRN-448, cycle count, damaged batch" />
            <div class="pz-col-span-2">
              <PzInput v-model="inventoryAdjustmentForm.note" label="Adjustment Note" type="textarea" required />
            </div>
          </div>
        </section>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeAdjustmentModal">Cancel</Button>
        <Button type="submit" form="inventory-adjustment-form" variant="primary" :loading="adjustingInventory">
          Apply Adjustment
        </Button>
      </template>
    </Modal>

    <Modal :isOpen="showHistoryModal" title="Stock History" size="lg" @close="closeHistoryModal">
      <VendorProductTimeline :product-id="selectedInventoryProduct?.id" />
      <section class="pz-form-section">
        <div class="pz-form-section__header">
          <div>
            <div class="pz-form-section__eyebrow">Movement Ledger</div>
            <h4>{{ selectedInventoryProduct?.name || 'Selected Material' }}</h4>
          </div>
        </div>
        <div v-if="historyLoading" class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">Loading stock history...</div>
        </div>
        <div v-else-if="inventoryHistory.length === 0" class="pz-empty-state">
          <div class="pz-empty-state__glyph">LOG</div>
          <div class="pz-empty-state__eyebrow">Inventory Ledger</div>
          <h4 class="pz-empty-state__title">No movement records yet.</h4>
          <p class="pz-empty-state__body">Initial stock loads, manual adjustments, order commits, and restocks will appear here.</p>
        </div>
        <div v-else class="pz-ledger-list">
          <article v-for="movement in inventoryHistory" :key="movement.id" class="pz-ledger-row">
            <div class="pz-ledger-row__top">
              <Badge :variant="movement.quantity_delta < 0 ? 'danger' : 'success'">
                {{ movement.movement_type }}
              </Badge>
              <span class="pz-u-text-mono text-xs">{{ formatMovementDate(movement.created_at) }}</span>
            </div>
            <div class="pz-ledger-row__numbers">
              <span>Delta: {{ movement.quantity_delta > 0 ? `+${movement.quantity_delta}` : movement.quantity_delta }}</span>
              <span>{{ movement.quantity_before }} → {{ movement.quantity_after }}</span>
            </div>
            <p v-if="movement.note" class="pz-ledger-row__note">{{ movement.note }}</p>
            <div class="pz-ledger-row__meta">
              <span v-if="movement.reference">Ref: {{ movement.reference }}</span>
              <span v-if="movement.actor_name">By: {{ movement.actor_name }}</span>
            </div>
          </article>
        </div>
      </section>
    </Modal>

    <!-- Mobile Quick Actions Sheet -->
    <MobileActionSheet
      :isOpen="showContextSheet"
      :title="contextProduct?.name || 'Actions'"
      @close="closeContextMenu"
    >
      <div class="pms-context-actions">
        <button class="pms-context-btn" @click="handleContextAction('edit')">
          <span class="pms-context-btn__icon">✏️</span>
          <span class="pms-context-btn__label">Edit Product</span>
        </button>
        <button class="pms-context-btn" @click="handleContextAction('adjust')">
          <span class="pms-context-btn__icon">📦</span>
          <span class="pms-context-btn__label">Adjust Stock</span>
        </button>
        <button class="pms-context-btn" @click="handleContextAction('history')">
          <span class="pms-context-btn__icon">📜</span>
          <span class="pms-context-btn__label">View History</span>
        </button>
        <button
          class="pms-context-btn"
          :class="{ 'pms-context-btn--danger': contextProduct?.status === 'ACTIVE' }"
          @click="handleContextAction('toggle')"
        >
          <span class="pms-context-btn__icon">{{ contextProduct?.status === 'ACTIVE' ? '🚫' : '✅' }}</span>
          <span class="pms-context-btn__label">{{ contextProduct?.status === 'ACTIVE' ? 'Disable' : 'Activate' }}</span>
        </button>
        <button class="pms-context-btn pms-context-btn--danger" @click="handleContextAction('delete')">
          <span class="pms-context-btn__icon">🗑️</span>
          <span class="pms-context-btn__label">Delete</span>
        </button>
      </div>
    </MobileActionSheet>

    <!-- CSV Import Wizard -->
    <Modal :isOpen="showCsvWizard" title="Import Catalog" size="lg" @close="showCsvWizard = false">
      <VendorCsvImportWizard @close="showCsvWizard = false" @imported="fetchProducts" />
    </Modal>

    <!-- Bulk Adjust Modal -->
    <Modal :isOpen="showBulkAdjustModal" title="Bulk Stock Adjustment" size="lg" @close="closeBulkAdjustModal">
      <div class="pz-bulk-adjust">
        <div class="pz-bulk-adjust__form">
          <PzInput v-model.number="bulkAdjustForm.quantity_delta" label="Quantity Adjustment" type="number" placeholder="+50 or -20" />
          <PzInput v-model="bulkAdjustForm.note" label="Note" placeholder="Reason for adjustment" />
        </div>
        <div class="pz-bulk-adjust__subtitle">Select Products</div>
        <div v-if="!products.length" class="pz-bulk-adjust__empty">No products available.</div>
        <div v-else class="pz-bulk-adjust__list">
          <label
            v-for="product in products"
            :key="product.id"
            class="pz-bulk-adjust__item"
          >
            <input
              v-model="bulkAdjustSelected"
              type="checkbox"
              :value="product.id"
              class="pz-bulk-adjust__checkbox"
            >
            <div class="pz-bulk-adjust__item-body">
              <div class="pz-bulk-adjust__item-name">{{ product.name }}</div>
              <div class="pz-bulk-adjust__item-meta">
                Stock: {{ product.stock_quantity }} • {{ product.inventory_signal?.replace('_', ' ') || 'In Stock' }}
              </div>
            </div>
          </label>
        </div>
        <div class="pz-bulk-adjust__count">{{ bulkAdjustSelected.length }} selected</div>
      </div>
      <template #footer>
        <Button variant="ghost" @click="closeBulkAdjustModal">Cancel</Button>
        <Button variant="primary" :loading="bulkAdjusting" :disabled="!bulkAdjustSelected.length || !bulkAdjustForm.quantity_delta" @click="submitBulkAdjustment">
          Adjust {{ bulkAdjustSelected.length || '' }} Products
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';
import Modal from '../ui/Modal.vue';
import PzInput from '../PzInput.vue';
import { useConfigStore } from '../../stores/config';
import { useOfflineQueueStore } from '../../stores/offlineQueue';
import VendorInventoryList from './VendorInventoryList.vue';
import VendorWorkspaceHeader from './VendorWorkspaceHeader.vue';
import VendorProductCard from './VendorProductCard.vue';
import VendorPerformanceChart from './VendorPerformanceChart.vue';
import VendorNotificationPanel from './VendorNotificationPanel.vue';
import VendorProductTimeline from './VendorProductTimeline.vue';
import VendorCsvImportWizard from './VendorCsvImportWizard.vue';
import MobileActionSheet from '../ui/MobileActionSheet.vue';

const configStore = useConfigStore();
const offlineQueue = useOfflineQueueStore();
const showAlert = inject('showAlert');
defineProps({
  vendorStatus: { type: String, default: '' },
});

const placeholderImage = 'https://placehold.co/640x420?text=No+Image+Available';

const products = ref([]);
const categories = ref([]);
const categoryPriceStats = ref([]);
const certificationOptions = ref([]);
const loading = ref(true);
const saving = ref(false);
const downloadingTemplate = ref(false);
const deletingProductId = ref(null);
const showProductModal = ref(false);
const showCsvWizard = ref(false);
const showBulkAdjustModal = ref(false);
const editingProductId = ref(null);
const fieldOpsMode = ref(false);
const showCelebration = ref(false);
const showContextSheet = ref(false);
const contextProduct = ref(null);
const bulkAdjustSelected = ref([]);
const bulkAdjustForm = ref({ quantity_delta: 0, note: '' });
const bulkAdjusting = ref(false);
const productImageInput = ref(null);
const cameraInput = ref(null);
const productDocumentInput = ref(null);
const selectedInventoryProduct = ref(null);
const showAdjustmentModal = ref(false);
const adjustingInventory = ref(false);
const showHistoryModal = ref(false);
const stockOutPrediction = ref(null);
const liveRegionMessage = ref('');
const historyLoading = ref(false);
const inventoryHistory = ref([]);
const searchQuery = ref('');
const selectedProductImageFiles = ref([]);
const selectedProductDocumentFiles = ref([]);
const imageValidationWarnings = ref([]);
const uploadDocumentType = ref('DATASHEET');
const activeProductTab = ref('commercial');
const wizardMode = ref(false);
const dashboardStats = ref({
  total_products: 0,
  active_products: 0,
  draft_products: 0,
  disabled_products: 0,
  low_stock_count: 0,
  out_of_stock_count: 0,
  products_with_images: 0,
  products_with_certifications: 0,
});
const unrespondedQuotes = ref(0);
const vendorNotifications = ref([]);
const backendRecommendations = ref([]);
const vendorProfile = ref(null);
const dailyStats = ref([]);

const materialFormTabs = [
  { id: 'commercial', label: 'Commercial', step: 1 },
  { id: 'technical', label: 'Technical', step: 2 },
  { id: 'compliance', label: 'Compliance', step: 3 },
  { id: 'documents', label: 'Documents', step: 4 },
  { id: 'media', label: 'Media', step: 5 },
];

const currentStep = computed(() => {
  const tab = materialFormTabs.find((t) => t.id === activeProductTab.value);
  return tab?.step || 1;
});

const totalSteps = 6; // 5 tabs + review

const readinessScore = computed(() => {
  const f = productForm.value;
  let s = 0;
  if (f.name?.trim()) s += 15;
  if (f.category) s += 10;
  if (f.base_price > 0) s += 15;
  if (f.description?.trim()) s += 15;
  if (f.stock_quantity >= 0) s += 10;
  if (selectedProductImageFiles.value.length >= 3) s += 20;
  else if (selectedProductImageFiles.value.length > 0) s += 10;
  if (f.certification_entries?.length) s += 10;
  if (f.attribute_entries?.length) s += 5;
  return Math.min(s, 100);
});

const readinessLabel = computed(() => {
  const r = readinessScore.value;
  if (r >= 80) return 'Ready to publish';
  if (r >= 50) return 'Almost there';
  return 'Keep going';
});

const wizardGateError = ref('');

function canAdvanceFromStep(step) {
  const f = productForm.value;
  if (step === 1) {
    if (!f.name?.trim()) return { valid: false, message: 'Material Name is required before continuing.' };
    if (!f.category) return { valid: false, message: 'Category is required before continuing.' };
    if (!f.base_price || f.base_price <= 0) return { valid: false, message: 'Base Price must be greater than 0 before continuing.' };
  }
  if (step === 5) {
    const hasImages = selectedProductImageFiles.value.length > 0 || (editingProductId.value && products.value.find(p => p.id === editingProductId.value)?.images?.length);
    if (!hasImages) {
      return { valid: true, warning: 'You have not added any product images. Listings with images get 5× more views. You can still continue.' };
    }
  }
  return { valid: true };
}

function goToStep(step) {
  wizardGateError.value = '';
  if (step >= 1 && step <= 5) {
    activeProductTab.value = materialFormTabs[step - 1].id;
  } else if (step === 6) {
    activeProductTab.value = 'review';
  }
}

function nextStep() {
  const gate = canAdvanceFromStep(currentStep.value);
  if (!gate.valid) {
    wizardGateError.value = gate.message;
    return;
  }
  wizardGateError.value = gate.warning || '';
  const next = currentStep.value + 1;
  if (next <= totalSteps) goToStep(next);
}

function prevStep() {
  wizardGateError.value = '';
  const prev = currentStep.value - 1;
  if (prev >= 1) goToStep(prev);
}

function handleWizardKeydown(event) {
  if (!wizardMode.value) return;
  // ArrowRight / ArrowDown → next step
  if ((event.key === 'ArrowRight' || event.key === 'ArrowDown') && !event.shiftKey) {
    // Only navigate if focus is not in a text input/textarea
    const tag = event.target.tagName;
    const isTextField = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
    if (!isTextField || event.target.type === 'checkbox' || event.target.type === 'radio') {
      event.preventDefault();
      nextStep();
    }
  }
  // ArrowLeft / ArrowUp → previous step
  if ((event.key === 'ArrowLeft' || event.key === 'ArrowUp') && !event.shiftKey) {
    const tag = event.target.tagName;
    const isTextField = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
    if (!isTextField || event.target.type === 'checkbox' || event.target.type === 'radio') {
      event.preventDefault();
      prevStep();
    }
  }
}

const inventoryAdjustmentForm = ref({
  quantity_delta: 0,
  note: '',
  reference: '',
});

const emptyProductForm = () => ({
  name: '',
  category: '',
  unit: 'bag',
  base_price: 0,
  currency: 'KES',
  bulk_price: null,
  bulk_threshold: null,
  stock_quantity: 0,
  reorder_level: 0,
  min_order_quantity: 1,
  max_order_quantity: null,
  brand: '',
  model_number: '',
  quality_grade: '',
  country_of_origin: '',
  packaging_details: '',
  estimated_delivery_days: null,
  short_description: '',
  description: '',
  delivery_regions_text: '',
  features_text: '',
  applications_text: '',
  handling_instructions: '',
  status: 'ACTIVE',
  is_featured: false,
  is_new_arrival: false,
  is_on_sale: false,
  attribute_entries: [],
  certification_entries: [],
  documents: [],
});

const productForm = ref(emptyProductForm());
const supportedCurrencies = computed(() => configStore.availableCurrencies);

// ─── Auto-save Draft ───
const DRAFT_KEY = 'vendor_draft_product';
let draftSaveTimer = null;

function saveDraftToStorage() {
  if (!wizardMode.value || editingProductId.value) return;
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(productForm.value));
  } catch {
    // Ignore storage errors
  }
}

function loadDraftFromStorage() {
  try {
    const raw = localStorage.getItem(DRAFT_KEY);
    if (raw) {
      const draft = JSON.parse(raw);
      productForm.value = { ...emptyProductForm(), ...draft };
      return true;
    }
  } catch {
    // Ignore parse errors
  }
  return false;
}

function clearDraftStorage() {
  try {
    localStorage.removeItem(DRAFT_KEY);
  } catch {
    // Ignore
  }
}

watch(
  productForm,
  () => {
    if (draftSaveTimer) clearTimeout(draftSaveTimer);
    draftSaveTimer = setTimeout(saveDraftToStorage, 800);
  },
  { deep: true }
);

const lowStockCount = computed(() => products.value.filter((entry) => entry.inventory_signal === 'LOW_STOCK').length);
const featuredCount = computed(() => products.value.filter((entry) => entry.is_featured).length);
const certifiedCount = computed(() => products.value.filter((entry) => entry.certification_entries?.length).length);

// ─── Operational Card Groups ───
const attentionProducts = computed(() => filteredProducts.value.filter((p) => {
  if (p.status !== 'ACTIVE') return false;
  return p.inventory_signal === 'LOW_STOCK'
    || p.inventory_signal === 'OUT_OF_STOCK'
    || !p.images?.length
    || !p.description;
}));

const healthyProducts = computed(() => filteredProducts.value.filter((p) => {
  if (p.status !== 'ACTIVE') return false;
  return p.inventory_signal !== 'LOW_STOCK'
    && p.inventory_signal !== 'OUT_OF_STOCK'
    && p.images?.length
    && p.description;
}));

const draftProducts = computed(() => filteredProducts.value.filter((p) => p.status === 'DRAFT'));
const hiddenProducts = computed(() => filteredProducts.value.filter((p) => p.status === 'DISABLED' || (p.status === 'ACTIVE' && p.inventory_signal === 'OUT_OF_STOCK')));

// ─── AI-Assisted UX Computed ───

/** Suggest category based on product name keywords */
const suggestedCategory = computed(() => {
  const name = (productForm.value.name || '').toLowerCase();
  if (!name || productForm.value.category) return null;

  // Simple keyword → category mapping
  const keywordMap = {
    cement: ['Cement', 'Concrete', 'Mortar'],
    concrete: ['Cement', 'Concrete'],
    mortar: ['Cement', 'Mortar'],
    steel: ['Steel', 'Metal', 'Rebar'],
    rebar: ['Steel', 'Rebar'],
    iron: ['Steel', 'Metal'],
    timber: ['Timber', 'Wood'],
    wood: ['Timber', 'Wood'],
    plank: ['Timber', 'Wood'],
    board: ['Timber', 'Board'],
    plywood: ['Timber', 'Plywood'],
    nail: ['Hardware', 'Fasteners'],
    screw: ['Hardware', 'Fasteners'],
    bolt: ['Hardware', 'Fasteners'],
    pipe: ['Plumbing', 'Pipes'],
    pvc: ['Plumbing', 'Pipes'],
    wire: ['Electrical', 'Wiring'],
    cable: ['Electrical', 'Cabling'],
    switch: ['Electrical', 'Switches'],
    socket: ['Electrical', 'Switches'],
    tile: ['Tiles', 'Flooring'],
    floor: ['Tiles', 'Flooring'],
    roof: ['Roofing'],
    sheet: ['Roofing', 'Sheets'],
    paint: ['Paints', 'Coatings'],
    coating: ['Paints', 'Coatings'],
    glass: ['Glass', 'Glazing'],
    window: ['Glass', 'Windows'],
    door: ['Doors', 'Frames'],
    frame: ['Doors', 'Frames'],
    sand: ['Aggregates', 'Sand'],
    aggregate: ['Aggregates'],
    stone: ['Aggregates', 'Stone'],
    gravel: ['Aggregates', 'Gravel'],
    brick: ['Bricks', 'Blocks'],
    block: ['Bricks', 'Blocks'],
  };

  const matchedNames = new Set();
  for (const [keyword, catNames] of Object.entries(keywordMap)) {
    if (name.includes(keyword)) {
      catNames.forEach((n) => matchedNames.add(n));
    }
  }

  if (!matchedNames.size) return null;

  // Find the best matching category from available categories
  const available = categories.value;
  for (const catName of matchedNames) {
    const match = available.find((c) => c.name.toLowerCase().includes(catName.toLowerCase()));
    if (match) return match;
  }
  return null;
});

/** Warn if product name is similar to an existing one */
const duplicateProductWarning = computed(() => {
  const name = (productForm.value.name || '').trim().toLowerCase();
  if (!name || name.length < 4) return null;

  // Skip if editing an existing product with the same name
  if (editingProductId.value) {
    const current = products.value.find((p) => p.id === editingProductId.value);
    if (current && current.name.toLowerCase().trim() === name) return null;
  }

  const similar = products.value.find((p) => {
    const existing = (p.name || '').toLowerCase().trim();
    // Exact match or very close (contains the full name)
    return existing === name || existing.includes(name) || name.includes(existing);
  });

  return similar || null;
});

/** Warn if price is anomalous compared to category median */
const isExperiencedVendor = computed(() => products.value.length >= 3);

const priceAnomaly = computed(() => {
  const price = parseFloat(productForm.value.base_price);
  const categoryId = productForm.value.category;
  if (!price || price <= 0 || !categoryId || !categoryPriceStats.value.length) return null;

  const catUuid = categories.value.find((c) => c.id === categoryId || c.uuid === categoryId)?.uuid || categoryId;
  const stats = categoryPriceStats.value.find((s) => s.category_uuid === catUuid);
  if (!stats || !stats.median_price) return null;

  const median = parseFloat(stats.median_price);
  if (median <= 0) return null;

  const ratio = price / median;
  if (ratio > 2.5) {
    return { type: 'high', message: `Your price is ${Math.round(ratio * 100)}% above the category median (${configStore.formatPrice(median, productForm.value.currency)}). Buyers may filter you out.`, severity: 'warning' };
  }
  if (ratio < 0.4) {
    return { type: 'low', message: `Your price is ${Math.round((1 - ratio) * 100)}% below the category median (${configStore.formatPrice(median, productForm.value.currency)}). Make sure this is intentional.`, severity: 'info' };
  }
  return null;
});

// ─── Certification Gap Detection ───

const categoryCertMap = {
  cement: ['KEBS Certified', 'ISO 9001', 'CE Mark'],
  concrete: ['KEBS Certified', 'ISO 9001'],
  steel: ['KEBS Certified', 'ISO 9001', 'BS EN'],
  rebar: ['KEBS Certified', 'ISO 9001'],
  timber: ['FSC Certified', 'PEFC', 'KEBS'],
  wood: ['FSC Certified', 'PEFC'],
  plumbing: ['ISO 15874', 'DIN 8077'],
  electrical: ['KEBS', 'IEC 60898', 'UL Listed'],
  tile: ['ISO 13006', 'ANSI A137.1'],
  roofing: ['ASTM D3462', 'ISO 9001'],
  paint: ['ISO 9001', 'Green Seal'],
  glass: ['ISO 12543', 'ANSI Z97.1'],
  aggregate: ['BS EN 12620', 'ASTM C33'],
  brick: ['BS EN 771', 'ASTM C62'],
  block: ['BS EN 771', 'ASTM C90'],
  hardware: ['ISO 9001', 'DIN Standard'],
  door: ['BS EN 14351', 'ANSI/BHMA'],
  window: ['BS EN 14351', 'NFRC'],
};

const currentCategoryName = computed(() => {
  const catId = productForm.value.category;
  if (!catId) return '';
  const cat = categories.value.find((c) => c.id === catId || c.uuid === catId);
  return cat?.name || '';
});

const suggestedCertifications = computed(() => {
  const catName = currentCategoryName.value.toLowerCase();
  if (!catName) return [];

  // Find matching cert list
  let certNames = [];
  for (const [keyword, certs] of Object.entries(categoryCertMap)) {
    if (catName.includes(keyword)) {
      certNames = certs;
      break;
    }
  }
  if (!certNames.length) return [];

  // Filter out certs already added
  const existingNames = new Set(
    (productForm.value.certification_entries || [])
      .map((e) => (e.display_name || '').toLowerCase())
  );

  return certNames
    .filter((name) => !existingNames.has(name.toLowerCase()))
    .map((name) => ({ name }));
});

const suggestedDeliveryRegions = computed(() => {
  // Common delivery regions for construction materials in East Africa
  return ['NAIROBI', 'MOMBASA', 'KISUMU', 'NAKURU', 'ELDORET'];
});

function addDeliveryRegion(region) {
  const current = productForm.value.delivery_regions_text || '';
  const regions = current.split(',').map((r) => r.trim()).filter(Boolean);
  if (!regions.includes(region)) {
    regions.push(region);
  }
  productForm.value.delivery_regions_text = regions.join(', ');
}

function addSuggestedCertification(cert) {
  // Find matching registry option if available
  const registryOption = certificationOptions.value.find(
    (o) => o.name.toLowerCase() === cert.name.toLowerCase()
  );
  productForm.value.certification_entries.push({
    registry: registryOption ? registryOption.id : null,
    display_name: cert.name,
    certification_number: '',
    issuing_body: '',
    status: 'ACTIVE',
  });
}

const filteredProducts = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) {
    return products.value;
  }

  return products.value.filter((product) => {
    const haystack = [
      product.name,
      product.category_name,
      product.category?.name,
      product.brand,
      product.model_number,
      product.country_of_origin,
      product.short_description,
      product.description,
      product.quality_grade,
      product.unit,
      ...(product.certification_highlights || []),
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();

    return haystack.includes(query);
  });
});

const editingProduct = computed(() => (
  editingProductId.value
    ? products.value.find((entry) => entry.id === editingProductId.value) || null
    : null
));

function normalizeListPayload(data) {
  return data?.results || data || [];
}

function splitLines(value) {
  return (value || '')
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
    .join('\n');
}

function parseDeliveryRegions(value) {
  return (value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function inventoryBadgeVariant(signal) {
  if (signal === 'LOW_STOCK') return 'warning';
  if (signal === 'OUT_OF_STOCK') return 'danger';
  return 'success';
}

function formatInventorySignal(signal) {
  if (!signal) return 'In Stock';
  return signal.replaceAll('_', ' ');
}

async function fetchCategories() {
  try {
    const res = await api.get('/taxonomy/categories/?taxonomy_type=MATERIAL');
    categories.value = normalizeListPayload(res.data);
  } catch (err) {
    showAlert?.('Failed to load material categories.', 'error');
  }
}

async function fetchCertificationOptions() {
  try {
    const res = await api.get('/v1/products/certification-options/');
    certificationOptions.value = normalizeListPayload(res.data);
  } catch (err) {
    certificationOptions.value = [];
  }
}

async function fetchProducts() {
  loading.value = true;
  try {
    const res = await api.get('/v1/products/me/');
    products.value = normalizeListPayload(res.data);
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to load vendor inventory.', 'error');
  } finally {
    loading.value = false;
  }
}

async function fetchDashboardStats() {
  try {
    const [statsRes, quotesRes, recsRes, meRes, dailyRes] = await Promise.allSettled([
      api.get('/v1/products/dashboard-stats/'),
      api.get('/orders/quote-requests/unresponded-count/'),
      api.get('/vendors/me/recommendations/'),
      api.get('/vendors/me/'),
      api.get('/v1/products/daily-stats/'),
    ]);
    dashboardStats.value = statsRes.status === 'fulfilled' ? statsRes.value.data : dashboardStats.value;
    unrespondedQuotes.value = quotesRes.status === 'fulfilled' ? (quotesRes.value.data.count || 0) : 0;
    backendRecommendations.value = recsRes.status === 'fulfilled' ? (recsRes.value.data.recommendations || []) : [];
    vendorProfile.value = meRes.status === 'fulfilled' ? (meRes.value.data || null) : null;
    dailyStats.value = dailyRes.status === 'fulfilled' ? (dailyRes.value.data || []) : [];
  } catch (err) {
    // Silent fail — workspace should still function without stats
  }
}

async function fetchCategoryPriceStats() {
  try {
    const res = await api.get('/v1/products/category-price-stats/');
    categoryPriceStats.value = normalizeListPayload(res.data);
  } catch (err) {
    categoryPriceStats.value = [];
  }
}

async function fetchVendorNotifications() {
  try {
    const res = await api.get('/notifications/');
    const items = res.data?.results || res.data || [];
    vendorNotifications.value = items.slice(0, 10).map((n) => ({
      id: n.id,
      title: n.subject || 'Notification',
      message: n.message || '',
      timestamp: n.created_at,
      read: n.status === 'SENT',
      icon: notificationIcon(n.type),
      actionLabel: actionLabel(n.data),
      data: n.data,
    }));
  } catch (err) {
    // Silent fail
  }
}

function notificationIcon(type) {
  const map = {
    BID: '🏗️',
    MILESTONE: '📅',
    PAYMENT: '💰',
    ESCROW: '🔒',
    DISPUTE: '⚠️',
    SYSTEM: '🔔',
    CHAT: '💬',
  };
  return map[type] || '🔔';
}

function actionLabel(data) {
  if (data?.product_uuid) return 'View';
  if (data?.quote_request_id) return 'Respond';
  if (data?.order_id) return 'Track';
  return null;
}

function handleNotificationAction(n) {
  if (n.data?.product_uuid) {
    const product = products.value.find((p) => p.uuid === n.data.product_uuid);
    if (product) openEditModal(product);
  } else if (n.data?.quote_request_id) {
    emit('navigate', 'quotes');
  }
}

function addAttribute() {
  productForm.value.attribute_entries.push({
    group: '',
    name: '',
    value: '',
    unit: '',
    is_highlight: false,
    sort_order: productForm.value.attribute_entries.length + 1,
  });
}

function removeAttribute(index) {
  productForm.value.attribute_entries.splice(index, 1);
}

function addCertification() {
  productForm.value.certification_entries.push({
    registry: null,
    display_name: '',
    certification_number: '',
    issuing_body: '',
    status: 'ACTIVE',
  });
}

function removeCertification(index) {
  productForm.value.certification_entries.splice(index, 1);
}

function addDocument() {
  productForm.value.documents.push({
    document_type: 'DATASHEET',
    title: '',
    external_url: '',
    description: '',
    is_public: true,
  });
}

function removeDocument(index) {
  productForm.value.documents.splice(index, 1);
}

function openCreateModal() {
  editingProductId.value = null;
  activeProductTab.value = 'commercial';
  wizardMode.value = true;
  selectedProductImageFiles.value = [];
  selectedProductDocumentFiles.value = [];
  uploadDocumentType.value = 'DATASHEET';
  const hasDraft = loadDraftFromStorage();
  if (!hasDraft) {
    productForm.value = {
      ...emptyProductForm(),
      currency: configStore.activeCurrencyCode || 'KES',
    };
  }
  showProductModal.value = true;
}

function openEditModal(product) {
  editingProductId.value = product.id;
  activeProductTab.value = 'commercial';
  wizardMode.value = false;
  selectedProductImageFiles.value = [];
  selectedProductDocumentFiles.value = [];
  uploadDocumentType.value = 'DATASHEET';
  productForm.value = {
    name: product.name || '',
    category: product.category?.id || product.category_id || '',
    unit: product.unit || 'unit',
    base_price: Number(product.base_price || 0),
    currency: product.currency || configStore.activeCurrencyCode || 'KES',
    bulk_price: product.bulk_price ? Number(product.bulk_price) : null,
    bulk_threshold: product.bulk_threshold ?? null,
    stock_quantity: Number(product.stock_quantity || 0),
    reorder_level: product.reorder_level ?? 0,
    min_order_quantity: product.min_order_quantity ?? 1,
    max_order_quantity: product.max_order_quantity ?? null,
    brand: product.brand || '',
    model_number: product.model_number || '',
    quality_grade: product.quality_grade || '',
    country_of_origin: product.country_of_origin || '',
    packaging_details: product.packaging_details || '',
    estimated_delivery_days: product.estimated_delivery_days ?? null,
    short_description: product.short_description || '',
    description: product.description || '',
    delivery_regions_text: (product.delivery_regions || []).join(', '),
    features_text: product.features || '',
    applications_text: product.applications || '',
    handling_instructions: product.handling_instructions || '',
    status: product.status || 'ACTIVE',
    is_featured: Boolean(product.is_featured),
    is_new_arrival: Boolean(product.is_new_arrival),
    is_on_sale: Boolean(product.is_on_sale),
    attribute_entries: (product.attribute_entries || []).map((entry) => ({
      group: entry.group || '',
      name: entry.name || '',
      value: entry.value || '',
      unit: entry.unit || '',
      is_highlight: Boolean(entry.is_highlight),
      sort_order: entry.sort_order || 0,
    })),
    certification_entries: (product.certification_entries || []).map((entry) => ({
      registry: entry.registry || null,
      display_name: entry.display_name || '',
      certification_number: entry.certification_number || '',
      issuing_body: entry.issuing_body || '',
      status: entry.status || 'ACTIVE',
    })),
    documents: (product.documents || []).map((entry) => ({
      document_type: entry.document_type || 'DATASHEET',
      title: entry.title || '',
      external_url: entry.external_url || '',
      description: entry.description || '',
      is_public: entry.is_public !== false,
    })),
  };
  showProductModal.value = true;
}

function openBulkAdjustModal() {
  bulkAdjustSelected.value = [];
  bulkAdjustForm.value = { quantity_delta: 0, note: '' };
  showBulkAdjustModal.value = true;
}

function closeBulkAdjustModal() {
  showBulkAdjustModal.value = false;
  bulkAdjustSelected.value = [];
  bulkAdjustForm.value = { quantity_delta: 0, note: '' };
}

async function submitBulkAdjustment() {
  if (!bulkAdjustSelected.value.length) {
    showAlert?.('Select at least one product.', 'warning');
    return;
  }
  if (!bulkAdjustForm.value.quantity_delta) {
    showAlert?.('Enter a quantity adjustment.', 'warning');
    return;
  }

  bulkAdjusting.value = true;
  const errors = [];
  let successCount = 0;

  for (const productId of bulkAdjustSelected.value) {
    try {
      await api.post(`/v1/products/${productId}/adjust-inventory/`, {
        quantity_delta: bulkAdjustForm.value.quantity_delta,
        note: bulkAdjustForm.value.note || 'Bulk adjustment',
      });
      successCount++;
    } catch (err) {
      const product = products.value.find((p) => p.id === productId);
      errors.push(product?.name || productId);
    }
  }

  if (errors.length) {
    showAlert?.(`Updated ${successCount} products. Failed: ${errors.join(', ')}`, 'warning');
  } else {
    showAlert?.(`Updated ${successCount} products successfully.`, 'success');
  }

  bulkAdjusting.value = false;
  closeBulkAdjustModal();
  await fetchProducts();
}

function confettiStyle(n) {
  const colors = ['#d4652a', '#16a34a', '#2563eb', '#dc2626', '#f59e0b', '#8b5cf6'];
  const left = Math.random() * 100;
  const delay = Math.random() * 2;
  const duration = 2 + Math.random() * 2;
  const color = colors[n % colors.length];
  return {
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    backgroundColor: color,
  };
}

function closeProductModal() {
  showProductModal.value = false;
  editingProductId.value = null;
  activeProductTab.value = 'commercial';
  selectedProductImageFiles.value = [];
  selectedProductDocumentFiles.value = [];
  uploadDocumentType.value = 'DATASHEET';
  productForm.value = {
    ...emptyProductForm(),
    currency: configStore.activeCurrencyCode || 'KES',
  };
}

function triggerProductImageUpload() {
  productImageInput.value?.click();
}

function triggerCameraCapture() {
  cameraInput.value?.click();
}

function triggerProductDocumentUpload() {
  productDocumentInput.value?.click();
}

async function handleProductImagesSelected(event) {
  const files = Array.from(event.target.files || []);
  selectedProductImageFiles.value = files;
  imageValidationWarnings.value = [];

  for (const file of files) {
    if (!file.type.startsWith('image/')) continue;
    try {
      const dims = await getImageDimensions(file);
      if (dims.width < 500 || dims.height < 500) {
        imageValidationWarnings.value.push(`"${file.name}" is only ${dims.width}×${dims.height}px. For best results, use images at least 500×500px.`);
      }
    } catch {
      // ignore
    }
  }
}

function getImageDimensions(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      URL.revokeObjectURL(url);
      resolve({ width: img.naturalWidth, height: img.naturalHeight });
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('Failed to load image'));
    };
    img.src = url;
  });
}

function handleProductDocumentsSelected(event) {
  selectedProductDocumentFiles.value = Array.from(event.target.files || []);
}

function clearSelectedProductImages() {
  selectedProductImageFiles.value = [];
  imageValidationWarnings.value = [];
  if (productImageInput.value) {
    productImageInput.value.value = '';
  }
}

function clearSelectedProductDocuments() {
  selectedProductDocumentFiles.value = [];
  if (productDocumentInput.value) {
    productDocumentInput.value.value = '';
  }
}

async function openAdjustmentModal(product) {
  selectedInventoryProduct.value = product;
  inventoryAdjustmentForm.value = {
    quantity_delta: 0,
    note: '',
    reference: '',
  };
  stockOutPrediction.value = null;
  showAdjustmentModal.value = true;

  // Fetch stock-out prediction
  try {
    const res = await api.get(`/v1/products/${product.uuid || product.id}/stock-out-prediction/`);
    const data = res.data;
    if (data.days_until_stockout !== null && data.days_until_stockout <= 14) {
      data.severity = 'urgent';
    } else if (data.days_until_stockout !== null && data.days_until_stockout <= 30) {
      data.severity = 'warning';
    } else {
      data.severity = 'ok';
    }
    stockOutPrediction.value = data;
  } catch {
    stockOutPrediction.value = null;
  }
}

function closeAdjustmentModal() {
  showAdjustmentModal.value = false;
  selectedInventoryProduct.value = null;
  inventoryAdjustmentForm.value = {
    quantity_delta: 0,
    note: '',
    reference: '',
  };
}

async function submitInventoryAdjustment() {
  if (!selectedInventoryProduct.value) return;

  if (!navigator.onLine) {
    offlineQueue.add({
      type: 'STOCK_ADJUST',
      productId: selectedInventoryProduct.value.id,
      payload: { ...inventoryAdjustmentForm.value },
    });
    showAlertMessage('You appear to be offline. Stock adjustment saved and will sync when connection returns.', 'warning');
    closeAdjustmentModal();
    return;
  }

  adjustingInventory.value = true;
  try {
    const response = await api.post(
      `/v1/products/${selectedInventoryProduct.value.id}/adjust-inventory/`,
      inventoryAdjustmentForm.value,
    );
    const updatedProduct = response.data.product;
    products.value = products.value.map((entry) => (
      entry.id === updatedProduct.id ? updatedProduct : entry
    ));
    selectedInventoryProduct.value = updatedProduct;
    showAlertMessage('Stock updated. Your listing is back in search results.', 'success');
    closeAdjustmentModal();
  } catch (err) {
    showAlert?.(err.response?.data?.error || 'Failed to adjust inventory.', 'error');
  } finally {
    adjustingInventory.value = false;
  }
}

async function syncOfflineQueue() {
  if (!offlineQueue.queue.length || !navigator.onLine) return;
  await offlineQueue.sync(async (item) => {
    if (item.type === 'STOCK_ADJUST') {
      await api.post(`/v1/products/${item.productId}/adjust-inventory/`, item.payload);
    }
  });
  if (!offlineQueue.queue.length) {
    showAlertMessage('Offline adjustments synced successfully.', 'success');
    await fetchProducts();
  }
}

function formatMovementDate(value) {
  if (!value) return 'Unknown';
  return new Date(value).toLocaleString();
}

async function openHistoryModal(product) {
  selectedInventoryProduct.value = product;
  showHistoryModal.value = true;
  historyLoading.value = true;
  try {
    const response = await api.get(`/v1/products/${product.id}/inventory-history/`);
    inventoryHistory.value = normalizeListPayload(response.data);
  } catch (err) {
    inventoryHistory.value = [];
    showAlert?.(err.response?.data?.detail || 'Failed to load inventory history.', 'error');
  } finally {
    historyLoading.value = false;
  }
}

function closeHistoryModal() {
  showHistoryModal.value = false;
  selectedInventoryProduct.value = null;
  inventoryHistory.value = [];
}

function openContextMenu(product) {
  contextProduct.value = product;
  showContextSheet.value = true;
}

function closeContextMenu() {
  showContextSheet.value = false;
  contextProduct.value = null;
}

function handleContextAction(action) {
  const p = contextProduct.value;
  if (!p) return;
  closeContextMenu();
  switch (action) {
    case 'edit': openEditModal(p); break;
    case 'adjust': openAdjustmentModal(p); break;
    case 'history': openHistoryModal(p); break;
    case 'toggle': toggleProductStatus(p); break;
    case 'delete': deleteProduct(p); break;
  }
}

function buildPayload() {
  return {
    name: productForm.value.name,
    category: productForm.value.category,
    unit: productForm.value.unit,
    base_price: productForm.value.base_price,
    currency: productForm.value.currency || configStore.activeCurrencyCode || 'KES',
    bulk_price: productForm.value.bulk_price || null,
    bulk_threshold: productForm.value.bulk_threshold || null,
    stock_quantity: productForm.value.stock_quantity,
    reorder_level: productForm.value.reorder_level || 0,
    min_order_quantity: productForm.value.min_order_quantity || 1,
    max_order_quantity: productForm.value.max_order_quantity || null,
    brand: productForm.value.brand,
    model_number: productForm.value.model_number,
    quality_grade: productForm.value.quality_grade,
    country_of_origin: productForm.value.country_of_origin,
    packaging_details: productForm.value.packaging_details,
    estimated_delivery_days: productForm.value.estimated_delivery_days || null,
    short_description: productForm.value.short_description,
    description: productForm.value.description,
    delivery_regions: parseDeliveryRegions(productForm.value.delivery_regions_text),
    features: splitLines(productForm.value.features_text),
    applications: splitLines(productForm.value.applications_text),
    handling_instructions: productForm.value.handling_instructions,
    status: productForm.value.status,
    is_featured: productForm.value.is_featured,
    is_new_arrival: productForm.value.is_new_arrival,
    is_on_sale: productForm.value.is_on_sale,
    attribute_entries: productForm.value.attribute_entries.filter((entry) => entry.name && entry.value),
    certification_entries: productForm.value.certification_entries.filter((entry) => entry.display_name || entry.registry),
    documents: productForm.value.documents.filter((entry) => entry.title && entry.external_url),
  };
}

function validateProductForm() {
  const requiredFields = [
    [productForm.value.name, 'Material Name'],
    [productForm.value.category, 'Category'],
    [productForm.value.unit, 'Unit of Sale'],
    [productForm.value.base_price, 'Base Price'],
    [productForm.value.stock_quantity, 'Stock Quantity'],
    [productForm.value.description, 'Detailed Description'],
  ];
  const missingField = requiredFields.find(([value]) => value === '' || value === null || value === undefined);
  if (missingField) {
    activeProductTab.value = 'commercial';
    showAlert?.(`${missingField[1]} is required before saving the material.`, 'warning');
    return false;
  }
  return true;
}

async function saveProduct() {
  if (!validateProductForm()) {
    return;
  }

  const isFirstPublish = !editingProductId.value && products.value.length === 0;
  saving.value = true;
  try {
    const payload = buildPayload();
    let response;
    if (editingProductId.value) {
      response = await api.patch(`/v1/products/${editingProductId.value}/`, payload);
      showAlertMessage('Your product has been saved.', 'success');
    } else {
      response = await api.post('/v1/products/', payload);
      showAlertMessage('Your material is live! Buyers can now find and request quotes.', 'success');
    }
    const productId = response?.data?.id || editingProductId.value;
    if (productId) {
      await uploadProductAssets(productId);
    }
    clearDraftStorage();
    closeProductModal();
    await fetchProducts();
    if (isFirstPublish) {
      showCelebration.value = true;
      setTimeout(() => { showCelebration.value = false; }, 4000);
    }
  } catch (err) {
    const detail = err.response?.data;
    let message = 'Failed to save material record.';
    if (typeof detail === 'string') {
      message = detail;
    } else if (detail && typeof detail === 'object') {
      // DRF returns field-level validation errors as objects
      const firstError = Object.values(detail).flat()[0];
      if (firstError) message = firstError;
    }
    showAlert?.(message, 'error');
  } finally {
    saving.value = false;
  }
}

async function uploadProductAssets(productId) {
  if (selectedProductImageFiles.value.length) {
    const imageData = new FormData();
    selectedProductImageFiles.value.forEach((file) => imageData.append('images', file));
    await api.post(`/v1/products/${productId}/upload_images/`, imageData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }

  if (selectedProductDocumentFiles.value.length) {
    const documentData = new FormData();
    documentData.append('document_type', uploadDocumentType.value);
    selectedProductDocumentFiles.value.forEach((file) => documentData.append('documents', file));
    await api.post(`/v1/products/${productId}/upload-documents/`, documentData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }
}

async function deleteProduct(product) {
  deletingProductId.value = product.id;
  try {
    await api.delete(`/v1/products/${product.id}/`);
    products.value = products.value.filter((entry) => entry.id !== product.id);
    showAlertMessage('Product deleted.', 'success');
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to delete material.', 'error');
  } finally {
    deletingProductId.value = null;
  }
}

async function toggleProductStatus(product) {
  const newStatus = product.status === 'ACTIVE' ? 'DISABLED' : 'ACTIVE';
  try {
    await api.patch(`/v1/products/${product.id}/`, { status: newStatus });
    product.status = newStatus;
    showAlertMessage(`Product ${newStatus === 'ACTIVE' ? 'is now live' : 'is now hidden'}.`, 'success');
  } catch (err) {
    showAlert?.('Failed to update status.', 'error');
  }
}

async function deleteProductImage(image) {
  if (!confirm(`Delete image "${image.alt_text || 'Image'}"?`)) return;
  try {
    await api.delete(`/v1/product-images/${image.uuid}/`);
    showAlertMessage('Image removed.', 'success');
    await fetchProducts();
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to delete image.', 'error');
  }
}

async function deleteProductDocument(document) {
  if (!confirm(`Delete document "${document.title}"?`)) return;
  try {
    await api.post(`/v1/products/${editingProductId.value}/remove-document/`, { document_uuid: document.uuid });
    showAlertMessage('Document removed.', 'success');
    await fetchProducts();
  } catch (err) {
    showAlert?.(err.response?.data?.detail || err.response?.data?.error || 'Failed to delete document.', 'error');
  }
}

async function downloadTemplate() {
  downloadingTemplate.value = true;
  try {
    const res = await api.get('/v1/products/download_template/', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'product_import_template.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    showAlertMessage('CSV template downloaded.', 'success');
  } catch (err) {
    showAlert?.('Failed to download inventory template.', 'error');
  } finally {
    downloadingTemplate.value = false;
  }
}

onMounted(async () => {
  await Promise.all([fetchCategories(), fetchCertificationOptions(), fetchProducts(), fetchDashboardStats(), fetchVendorNotifications(), fetchCategoryPriceStats()]);
  window.addEventListener('online', syncOfflineQueue);
});

onUnmounted(() => {
  window.removeEventListener('online', syncOfflineQueue);
});
</script>

<style scoped>
.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 2px solid var(--pz-color-foundation-black);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.pz-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.pz-summary-card,
.pz-form-section {
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

.pz-summary-card {
  padding: 1rem;
  display: grid;
  gap: 0.2rem;
}

.pz-summary-card span {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-summary-card strong {
  font-size: 1.5rem;
}

.pz-product-form,
.pz-repeaters {
  display: grid;
  gap: 1rem;
}

.pz-modal-tabs {
  display: flex;
  gap: 0.3rem;
  margin-bottom: 1rem;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 14px;
  border: 1px solid rgba(10, 10, 15, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.pz-modal-tabs::-webkit-scrollbar {
  display: none;
}

.pz-modal-tab {
  position: relative;
  flex: 1;
  padding: 0.55rem 0.75rem;
  background: transparent;
  border: none;
  border-radius: 10px;
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 0.82rem;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
}
.pz-modal-tab:hover {
  color: var(--pz-color-structural-steel);
  background: rgba(10, 10, 15, 0.03);
}
.pz-modal-tab--active {
  background: white;
  color: var(--pz-color-earth-orange);
  box-shadow: 0 2px 6px rgba(10, 10, 15, 0.08);
}

.pz-modal-panel {
  animation: fadeIn 0.25s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.pz-existing-assets,
.pz-existing-assets__group,
.pz-upload-card {
  display: grid;
  gap: 0.75rem;
}

.pz-existing-assets {
  margin-bottom: 1rem;
}

.pz-existing-assets__title,
.pz-upload-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pz-chip {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.2rem 0.7rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(247, 244, 239, 0.9);
  font-size: 0.76rem;
}

.pz-upload-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}

.pz-upload-card {
  padding: 1rem;
  border: 1px dashed rgba(10, 10, 15, 0.18);
  background: rgba(255, 255, 255, 0.96);
}

.pz-upload-selection {
  font-size: 0.8rem;
  color: var(--pz-color-earth-orange);
}

.pz-inventory-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1rem;
  flex-wrap: wrap;
}

.pz-inventory-toolbar__search {
  flex: 1 1 420px;
  display: grid;
  gap: 0.45rem;
}

.pz-inventory-toolbar__label {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-inventory-toolbar__input {
  width: 100%;
  min-height: 48px;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.18);
  background: rgba(255, 255, 255, 0.96);
  color: var(--pz-color-text-primary);
  font: inherit;
}

.pz-inventory-toolbar__input::placeholder {
  color: var(--pz-color-text-secondary);
}

.pz-inventory-toolbar__input:focus {
  outline: 2px solid rgba(212, 101, 42, 0.24);
  outline-offset: 2px;
  border-color: var(--pz-color-earth-orange);
}

.pz-inventory-toolbar__meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-inventory-adjustment__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.pz-inventory-adjustment__summary > div,
.pz-ledger-row {
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.95);
  padding: 0.9rem;
}

.pz-inventory-adjustment__summary span,
.pz-ledger-row__meta,
.pz-ledger-row__numbers {
  display: block;
  font-size: 0.78rem;
  color: var(--pz-color-steel-grey);
}

.pz-inventory-adjustment__summary strong {
  display: block;
  margin-top: 0.3rem;
  font-size: 1.1rem;
}

.pz-ledger-list {
  display: grid;
  gap: 0.75rem;
}

.pz-ledger-row__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.pz-ledger-row__numbers {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.pz-ledger-row__note {
  margin: 0.7rem 0 0.45rem;
  font-size: 0.88rem;
}

.pz-form-section {
  padding: 1rem;
}

.pz-form-section__header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.pz-form-section__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-repeater-row {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 0.75rem;
  align-items: end;
  padding: 0.9rem;
  background: rgba(247, 244, 239, 0.95);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

@media (max-width: 1200px) {
  .pz-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .pz-repeater-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .pz-summary-grid,
  .pz-repeater-row,
  .pz-inventory-adjustment__summary {
    grid-template-columns: 1fr;
  }

  .pz-ledger-row__top,
  .pz-ledger-row__numbers {
    flex-direction: column;
    align-items: start;
  }
}

.pz-checkbox-row {
  display: flex;
  gap: 1.25rem;
  flex-wrap: wrap;
  padding: 0.5rem 0;
}

.pz-checkbox {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  color: var(--pz-color-foundation-black);
  cursor: pointer;
}

.pz-checkbox input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--pz-color-earth-orange);
  cursor: pointer;
}

.pz-chip--removable {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding-right: 0.4rem;
}

.pz-chip__remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.1rem;
  height: 1.1rem;
  border: none;
  border-radius: 50%;
  background: rgba(10, 10, 15, 0.08);
  color: var(--pz-color-foundation-black);
  font-size: 0.85rem;
  line-height: 1;
  cursor: pointer;
  transition: background 0.15s ease;
}

.pz-chip__remove:hover {
  background: rgba(220, 38, 38, 0.15);
  color: #dc2626;
}

/* ─── Wizard ─── */
.pz-wizard-bar {
  padding: 1rem 1.25rem 0.75rem;
  background: rgba(247, 244, 239, 0.5);
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-wizard-steps {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.pz-wizard-step {
  display: grid;
  place-items: center;
  gap: 0.3rem;
  flex: 1;
  text-align: center;
}

.pz-wizard-step__bubble {
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(10, 10, 15, 0.06);
  color: var(--pz-color-concrete-grey);
  transition: all 0.25s ease;
}

.pz-wizard-step--active .pz-wizard-step__bubble {
  background: var(--pz-color-earth-orange);
  color: white;
  box-shadow: 0 0 0 4px rgba(212, 101, 42, 0.15);
}

.pz-wizard-step--done .pz-wizard-step__bubble {
  background: #16a34a;
  color: white;
}

.pz-wizard-step__label {
  font-size: 0.68rem;
  font-family: var(--pz-font-mono);
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

.pz-wizard-step--active .pz-wizard-step__label {
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

.pz-wizard-readiness {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.pz-wizard-readiness__bar {
  flex: 1;
  height: 0.4rem;
  background: rgba(10, 10, 15, 0.06);
  border-radius: 99px;
  overflow: hidden;
}

.pz-wizard-readiness__fill {
  height: 100%;
  background: linear-gradient(90deg, var(--pz-color-earth-orange), #d97706);
  border-radius: 99px;
  transition: width 0.4s ease;
}

.pz-wizard-readiness__label {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.06em;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

.pz-wizard-nav {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-wizard-gate-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: rgba(220, 38, 38, 0.06);
  border: 1px solid rgba(220, 38, 38, 0.12);
  border-radius: 8px;
  margin: 0.5rem 1.25rem;
  font-size: 0.85rem;
  color: #991b1b;
}

.pz-wizard-gate-error__icon {
  font-size: 1rem;
  flex-shrink: 0;
}

/* ─── Review Step ─── */
.pz-review-card {
  display: grid;
  gap: 1.25rem;
}

.pz-review-card__preview {
  display: grid;
  grid-template-columns: 8rem 1fr;
  gap: 1rem;
  padding: 1rem;
  background: rgba(247, 244, 239, 0.4);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 12px;
}

.pz-review-card__image {
  width: 8rem;
  height: 8rem;
  border-radius: 10px;
  overflow: hidden;
  background: #f4f4f5;
}

.pz-review-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pz-review-card__no-image {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  font-size: 0.75rem;
  color: var(--pz-color-concrete-grey);
}

.pz-review-card__info h3 {
  margin: 0 0 0.3rem;
  font-family: var(--pz-font-display);
  font-size: 1.1rem;
}

.pz-review-card__price {
  font-weight: 600;
  color: var(--pz-color-earth-orange);
  margin: 0 0 0.4rem;
}

.pz-review-card__desc {
  font-size: 0.85rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.5;
  margin: 0 0 0.5rem;
}

.pz-review-card__meta {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
}

.pz-review-checklist {
  display: grid;
  gap: 0.4rem;
}

.pz-review-checklist__title {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.3rem;
}

.pz-review-checklist__item {
  font-size: 0.85rem;
  padding: 0.35rem 0.6rem;
  border-radius: 8px;
  background: rgba(10, 10, 15, 0.03);
  color: var(--pz-color-concrete-grey);
}

.pz-review-checklist__item--ok {
  background: rgba(22, 163, 74, 0.08);
  color: #166534;
}

@media (max-width: 640px) {
  .pz-review-card__preview {
    grid-template-columns: 1fr;
  }
  .pz-review-card__image {
    width: 100%;
    height: 12rem;
  }
}

/* ─── Operational Card Groups ─── */
.vpc-groups {
  display: grid;
  gap: 1.5rem;
}

.vpc-group__header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
}

.vpc-group__title {
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.vpc-group__count {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  padding: 0.15rem 0.5rem;
  background: rgba(10, 10, 15, 0.06);
  border-radius: 99px;
  color: var(--pz-color-concrete-grey);
}

.vpc-group__list {
  display: grid;
  gap: 0.6rem;
}

/* ─── Guided Empty State ─── */
.pz-empty-state--guided {
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.pz-empty-state--guided .pz-empty-state__glyph {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.pz-empty-state--guided .pz-empty-state__title {
  font-size: 1.3rem;
  margin: 0.5rem 0;
}

.pz-empty-state__actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 1.25rem 0 0.75rem;
}

.pz-empty-state__tips {
  font-size: 0.8rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.7;
}

.pz-empty-state__tips p {
  margin: 0;
}

/* ─── Certification Suggestion Chips ─── */
.pvd-suggestion--block {
  display: block;
  margin-bottom: 0.75rem;
  padding: 0.6rem 0.75rem;
}

.pvd-suggestion__header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.4rem;
}

.pvd-suggestion__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.pvd-suggestion__chip {
  padding: 0.3rem 0.6rem;
  background: white;
  border: 1px solid rgba(37, 99, 235, 0.2);
  border-radius: 99px;
  font-size: 0.75rem;
  color: #2563eb;
  cursor: pointer;
  transition: all 0.12s;
}

.pvd-suggestion__chip:hover {
  background: rgba(37, 99, 235, 0.08);
  border-color: rgba(37, 99, 235, 0.35);
}

/* ─── Stock-Out Prediction ─── */
.pvd-stock-prediction {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.7rem 0.9rem;
  border-radius: 10px;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
}

.pvd-stock-prediction__icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.pvd-stock-prediction__message {
  font-weight: 600;
  line-height: 1.3;
}

.pvd-stock-prediction__meta {
  font-size: 0.75rem;
  opacity: 0.85;
  margin-top: 0.15rem;
}

.pvd-stock-prediction--urgent {
  background: rgba(220, 38, 38, 0.06);
  border: 1px solid rgba(220, 38, 38, 0.12);
  color: #991b1b;
}

.pvd-stock-prediction--warning {
  background: rgba(217, 119, 6, 0.06);
  border: 1px solid rgba(217, 119, 6, 0.12);
  color: #92400e;
}

.pvd-stock-prediction--ok {
  background: rgba(22, 163, 74, 0.06);
  border: 1px solid rgba(22, 163, 74, 0.12);
  color: #166534;
}

/* ─── Progressive Disclosure Hints ─── */
.pvd-progressive-hint {
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.3rem;
  font-style: italic;
}

.pvd-suggestion--inline {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.4rem;
  padding: 0.3rem 0.5rem;
  background: rgba(37, 99, 235, 0.04);
  border-radius: 8px;
  font-size: 0.75rem;
  color: #1e40af;
}

@media (max-width: 640px) {
  .pz-empty-state__actions {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (min-width: 641px) {
  .u-show-mobile {
    display: none !important;
  }
}

/* ─── Mobile Context Sheet Actions ─── */
.pms-context-actions {
  display: grid;
  gap: 0.25rem;
}

.pms-context-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 0.5rem;
  background: none;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.95rem;
  color: #0f172a;
  transition: background 0.12s;
}

.pms-context-btn:hover {
  background: #f1f5f9;
}

.pms-context-btn__icon {
  font-size: 1.25rem;
  width: 1.5rem;
  text-align: center;
}

.pms-context-btn__label {
  font-weight: 500;
}

.pms-context-btn--danger {
  color: #dc2626;
}

.pms-context-btn--danger:hover {
  background: rgba(220, 38, 38, 0.06);
}

/* ─── Smart Suggestions & Warnings ─── */
.pvd-suggestion {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.4rem;
  padding: 0.4rem 0.6rem;
  background: rgba(37, 99, 235, 0.06);
  border: 1px solid rgba(37, 99, 235, 0.15);
  border-radius: 8px;
  font-size: 0.78rem;
  color: #1e40af;
}

.pvd-suggestion__icon {
  font-size: 0.9rem;
}

.pvd-suggestion__text strong {
  font-weight: 600;
}

.pvd-warning {
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
  margin-top: 0.4rem;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  font-size: 0.78rem;
}

.pvd-warning__icon {
  font-size: 0.9rem;
  flex-shrink: 0;
  margin-top: 0.05rem;
}

.pvd-warning__text {
  line-height: 1.4;
}

.pvd-warning--duplicate {
  background: rgba(217, 119, 6, 0.06);
  border: 1px solid rgba(217, 119, 6, 0.15);
  color: #92400e;
}

.pvd-warning--warning {
  background: rgba(217, 119, 6, 0.06);
  border: 1px solid rgba(217, 119, 6, 0.15);
  color: #92400e;
}

.pvd-warning--info {
  background: rgba(37, 99, 235, 0.06);
  border: 1px solid rgba(37, 99, 235, 0.15);
  color: #1e40af;
}

/* ─── Approval Blocker ─── */
.pz-approval-blocker {
  text-align: center;
  padding: 2.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(10, 10, 15, 0.12);
  border-radius: 14px;
  margin: 1rem;
}

.pz-approval-blocker__icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.pz-approval-blocker__title {
  font-family: var(--pz-font-display);
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0.5rem 0;
}

.pz-approval-blocker__body {
  max-width: 36rem;
  margin: 0.6rem auto 1.25rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.65;
}

.pz-approval-blocker__actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* ─── Celebration Overlay ─── */
.pz-celebration-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: grid;
  place-items: center;
  background: rgba(10, 10, 15, 0.45);
  backdrop-filter: blur(4px);
}

.pz-celebration__confetti {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.pz-confetti {
  position: absolute;
  top: -10px;
  width: 8px;
  height: 8px;
  border-radius: 2px;
  animation-name: confetti-fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

@keyframes confetti-fall {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}

.pz-celebration__content {
  position: relative;
  z-index: 1;
  text-align: center;
  background: white;
  border: 2px solid var(--pz-color-foundation-black);
  padding: 2.5rem 2rem;
  border-radius: 16px;
  box-shadow: 0 24px 60px rgba(10, 10, 15, 0.25);
  max-width: 24rem;
  width: 90%;
}

.pz-celebration__emoji {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
  animation: bounce-in 0.6s ease;
}

.pz-celebration__title {
  font-family: var(--pz-font-display);
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: var(--pz-color-foundation-black);
}

.pz-celebration__body {
  color: var(--pz-color-text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.55;
}

@keyframes bounce-in {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); opacity: 1; }
}

.pz-celebration-enter-active,
.pz-celebration-leave-active {
  transition: opacity 0.4s ease;
}

.pz-celebration-enter-from,
.pz-celebration-leave-to {
  opacity: 0;
}

/* ─── Field Operations Mode ─── */
.pz-field-ops .pz-admin-card__title,
.pz-field-ops .pz-section-shell__title {
  font-size: 1.1rem;
}

.pz-field-ops .pz-section-shell__meta {
  font-size: 1rem;
}

.pz-field-ops button,
.pz-field-ops .pz-health-action,
.pz-field-ops .pz-quote-card {
  font-size: 1rem;
  padding: 0.75rem 1rem;
}

.pz-field-ops .pz-product-card {
  font-size: 1rem;
  border-width: 2px;
}

.pz-field-ops .pz-inventory-toolbar__input {
  font-size: 1.05rem;
  padding: 0.6rem 0.9rem;
}

.pz-field-ops .vpc-name {
  font-size: 1.05rem;
}

.pz-field-ops .vpc-meta {
  font-size: 0.95rem;
}

.pz-field-ops-toggle--active {
  background: rgba(22, 163, 74, 0.1);
  color: #166534;
  font-weight: 600;
}

/* ─── Bulk Adjust Modal ─── */
.pz-bulk-adjust__form {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.pz-bulk-adjust__subtitle {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.pz-bulk-adjust__list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 10px;
  padding: 0.5rem;
}

.pz-bulk-adjust__item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.12s;
}

.pz-bulk-adjust__item:hover {
  background: rgba(10, 10, 15, 0.03);
}

.pz-bulk-adjust__checkbox {
  width: 1.1rem;
  height: 1.1rem;
  flex-shrink: 0;
}

.pz-bulk-adjust__item-body {
  flex: 1;
}

.pz-bulk-adjust__item-name {
  font-size: 0.88rem;
  font-weight: 500;
}

.pz-bulk-adjust__item-meta {
  font-size: 0.75rem;
  color: var(--pz-color-concrete-grey);
}

.pz-bulk-adjust__count {
  font-size: 0.82rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.5rem;
  text-align: right;
}

.pz-bulk-adjust__empty {
  text-align: center;
  padding: 2rem;
  color: var(--pz-color-concrete-grey);
}

@media (max-width: 640px) {
  .pz-bulk-adjust__form {
    grid-template-columns: 1fr;
  }
}
</style>
