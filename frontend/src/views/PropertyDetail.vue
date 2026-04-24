<template>
  <div class="pz-property-page">
    <div class="pz-l-container u-py-8">
      <div v-if="loading" class="pz-u-text-center u-py-20">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">Loading property intelligence...</p>
      </div>

      <div v-else-if="property" class="pz-space-y-8">
        <nav class="pz-breadcrumb pz-u-text-mono text-xs">
          <router-link to="/properties" class="pz-breadcrumb__item">PROPERTY MARKETPLACE</router-link>
          <span class="pz-breadcrumb__separator">//</span>
          <span class="pz-breadcrumb__current pz-u-color-steel">{{ property.title }}</span>
        </nav>

        <section class="pz-property-hero">
          <div class="pz-property-hero__media">
            <img
              v-if="heroMediaUrl"
              :src="heroMediaUrl"
              :alt="property.primary_media?.alt_text || property.title"
              class="pz-property-hero__image"
            />
            <div v-else class="pz-property-hero__fallback">
              <span class="pz-u-text-mono text-xs">PROPERTY MEDIA</span>
              <strong>{{ property.asset_type }}</strong>
            </div>
          </div>

          <div class="pz-property-hero__content">
            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start pz-l-flex--gap-4 pz-l-flex--wrap">
              <div class="pz-space-y-3">
                <div class="pz-u-text-mono text-xs pz-u-color-earth">{{ property.listing_type }}</div>
                <h1 class="pz-u-text-display">{{ property.title }}</h1>
                <p class="pz-u-text-mono text-sm pz-u-color-steel pz-property-hero__description">{{ property.description }}</p>
              </div>
              <div class="pz-l-flex pz-l-flex--gap-2 pz-l-flex--wrap">
                <Badge variant="ghost">{{ property.asset_type }}</Badge>
                <Badge :variant="property.status === 'ACTIVE' ? 'success' : 'secondary'">{{ property.status }}</Badge>
              </div>
            </div>

            <div class="pz-property-hero__price">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Commercial Terms</span>
              <strong>{{ displayPrice }}</strong>
              <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ property.location_display || 'Location pending' }}</span>
            </div>

            <div v-if="summaryStats.length" class="pz-property-summary-grid">
              <div v-for="stat in summaryStats" :key="stat.label" class="pz-property-detail__metric">
                <span class="pz-property-detail__label">{{ stat.label }}</span>
                <span class="pz-property-detail__value">{{ stat.value }}</span>
              </div>
            </div>

            <div v-if="property.highlighted_features?.length" class="pz-property-chip-row">
              <span v-for="feature in property.highlighted_features" :key="feature.id" class="pz-property-chip">
                {{ feature.name }}
              </span>
            </div>
          </div>
        </section>

        <div class="pz-property-layout">
          <section class="pz-space-y-8">
            <Card v-if="canModifyProperty" title="Operator Console">
              <div class="pz-space-y-5">
                <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pz-l-flex--gap-4 pz-l-flex--wrap">
                  <div class="pz-space-y-1">
                    <div class="pz-u-text-mono text-xs pz-u-color-earth">EDITABLE WORKSPACE</div>
                    <p class="pz-u-text-mono text-xs pz-u-color-steel">
                      Update the listing, pricing, readiness, and ownership profile from the same page.
                    </p>
                  </div>
                  <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                    <Button variant="outline" @click="toggleEditMode">
                      {{ editMode ? 'Close Editor' : 'Modify Property' }}
                    </Button>
                  </div>
                </div>

                <div v-if="editMode" class="pz-space-y-6">
                  <div class="pz-editor-shell">
                    <div class="pz-editor-nav">
                      <button
                        v-for="section in editorSections"
                        :key="section.id"
                        type="button"
                        class="pz-editor-nav__item"
                        :class="{ 'is-active': activeEditorSection === section.id }"
                        @click="activeEditorSection = section.id"
                      >
                        <span class="pz-editor-nav__kicker">{{ section.kicker }}</span>
                        <strong>{{ section.label }}</strong>
                        <span>{{ section.description }}</span>
                      </button>
                    </div>
                    <div class="pz-operator-form-section">
                      <div class="pz-space-y-1">
                        <div class="pz-u-text-display text-sm">{{ activeEditorMeta.label }}</div>
                        <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ activeEditorMeta.description }}</div>
                      </div>

                      <div v-if="activeEditorSection === 'listing'" class="pz-space-y-4">
                        <div class="pz-operator-form-grid">
                          <PzInput v-model="operatorForm.title" label="Title" required />
                          <select v-model="operatorForm.asset_type" class="pz-input">
                            <option value="LAND">Land</option>
                            <option value="RESIDENTIAL">Residential</option>
                            <option value="COMMERCIAL">Commercial</option>
                            <option value="INDUSTRIAL">Industrial</option>
                            <option value="MIXED_USE">Mixed Use</option>
                            <option value="HOSPITALITY">Hospitality</option>
                            <option value="RENOVATION">Renovation</option>
                            <option value="SPECIAL_PURPOSE">Special Purpose</option>
                          </select>
                          <select v-model="operatorForm.listing_type" class="pz-input">
                            <option value="SALE">Sale</option>
                            <option value="LEASE">Lease</option>
                            <option value="DEVELOPMENT_OPPORTUNITY">Development Opportunity</option>
                            <option value="COMPLETED_PROJECT">Completed Project</option>
                          </select>
                          <select v-model="operatorForm.status" class="pz-input">
                            <option value="DRAFT">Draft</option>
                            <option value="ACTIVE">Active</option>
                            <option value="SOLD">Sold</option>
                            <option value="LEASED">Leased</option>
                            <option value="UNDER_OFFER">Under Offer</option>
                            <option value="INACTIVE">Inactive</option>
                          </select>
                          <PzInput v-model="operatorForm.location_text" label="Location Text" />
                          <PzInput v-model="operatorForm.formatted_address" label="Formatted Address" />
                          <PzInput v-model="operatorForm.price_estimate" label="Estimated Value" type="number" />
                        </div>
                        <textarea
                          v-model="operatorForm.description"
                          class="pz-input"
                          rows="4"
                          placeholder="Describe the property, market position, and operating context"
                        />
                        <div class="pz-operator-toggle-grid">
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.financing_allowed" type="checkbox" />
                            <span>Financing allowed</span>
                          </label>
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.inquiry_enabled" type="checkbox" />
                            <span>Inquiries enabled</span>
                          </label>
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.appointment_enabled" type="checkbox" />
                            <span>Appointments enabled</span>
                          </label>
                        </div>
                      </div>

                      <div v-else-if="activeEditorSection === 'specification'" class="pz-operator-form-grid">
                        <PzInput v-model="operatorForm.specification.bedrooms" label="Bedrooms" type="number" />
                        <PzInput v-model="operatorForm.specification.bathrooms" label="Bathrooms" type="number" />
                        <PzInput v-model="operatorForm.specification.floors" label="Floors" type="number" />
                        <PzInput v-model="operatorForm.specification.parking_spaces" label="Parking Spaces" type="number" />
                        <PzInput v-model="operatorForm.specification.internal_area" label="Internal Area" type="number" />
                        <select v-model="operatorForm.specification.internal_area_unit" class="pz-input">
                          <option value="SQM">Square Meters</option>
                          <option value="SQFT">Square Feet</option>
                          <option value="ACRE">Acre</option>
                          <option value="HECTARE">Hectare</option>
                        </select>
                        <PzInput v-model="operatorForm.specification.lot_size" label="Lot Size" type="number" />
                        <select v-model="operatorForm.specification.lot_size_unit" class="pz-input">
                          <option value="SQM">Square Meters</option>
                          <option value="SQFT">Square Feet</option>
                          <option value="ACRE">Acre</option>
                          <option value="HECTARE">Hectare</option>
                        </select>
                        <PzInput v-model="operatorForm.specification.year_built" label="Year Built" type="number" />
                        <PzInput v-model="operatorForm.specification.renovation_year" label="Renovation Year" type="number" />
                        <select v-model="operatorForm.specification.furnishing_state" class="pz-input">
                          <option value="">Furnishing State</option>
                          <option value="UNFURNISHED">Unfurnished</option>
                          <option value="PART_FURNISHED">Part Furnished</option>
                          <option value="FURNISHED">Furnished</option>
                          <option value="FITTED">Fitted</option>
                        </select>
                        <select v-model="operatorForm.specification.condition_rating" class="pz-input">
                          <option value="">Condition Rating</option>
                          <option value="SHELL">Shell</option>
                          <option value="FAIR">Fair</option>
                          <option value="GOOD">Good</option>
                          <option value="EXCELLENT">Excellent</option>
                        </select>
                        <PzInput v-model="operatorForm.specification.energy_rating" label="Energy Rating" />
                        <select v-model="operatorForm.specification.occupancy_status" class="pz-input">
                          <option value="">Occupancy Status</option>
                          <option value="VACANT">Vacant</option>
                          <option value="OCCUPIED">Occupied</option>
                          <option value="OWNER_OCCUPIED">Owner Occupied</option>
                          <option value="TENANTED">Tenanted</option>
                          <option value="UNDER_CONSTRUCTION">Under Construction</option>
                        </select>
                      </div>

                      <div v-else-if="activeEditorSection === 'commercial'" class="pz-space-y-4">
                        <div class="pz-operator-form-grid">
                          <PzInput v-model="operatorForm.pricing_profile.asking_price" label="Asking Price" type="number" />
                          <PzInput v-model="operatorForm.pricing_profile.rent_amount" label="Rent Amount" type="number" />
                          <select v-model="operatorForm.pricing_profile.currency" class="pz-input">
                            <option value="KES">KES</option>
                            <option value="USD">USD</option>
                            <option value="EUR">EUR</option>
                          </select>
                          <select v-model="operatorForm.pricing_profile.pricing_strategy" class="pz-input">
                            <option value="FIXED">Fixed</option>
                            <option value="NEGOTIABLE">Negotiable</option>
                            <option value="PRICE_ON_APPLICATION">Price On Application</option>
                            <option value="PER_UNIT">Per Unit</option>
                          </select>
                          <PzInput v-model="operatorForm.pricing_profile.deposit_amount" label="Deposit Amount" type="number" />
                          <PzInput v-model="operatorForm.pricing_profile.price_per_area_unit" label="Price Per Area Unit" type="number" />
                          <select v-model="operatorForm.pricing_profile.area_unit" class="pz-input">
                            <option value="SQM">Square Meters</option>
                            <option value="SQFT">Square Feet</option>
                            <option value="ACRE">Acre</option>
                            <option value="HECTARE">Hectare</option>
                          </select>
                          <PzInput v-model="operatorForm.pricing_profile.service_charge_amount" label="Service Charge" type="number" />
                          <PzInput v-model="operatorForm.pricing_profile.tax_percentage" label="Tax %" type="number" />
                          <PzInput v-model="operatorForm.pricing_profile.insurance_percentage" label="Insurance %" type="number" />
                        </div>
                        <div class="pz-operator-toggle-grid">
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.pricing_profile.requires_deposit" type="checkbox" />
                            <span>Requires deposit</span>
                          </label>
                        </div>
                        <textarea
                          v-model="operatorForm.pricing_profile.financing_notes"
                          class="pz-input"
                          rows="3"
                          placeholder="Financing notes, eligibility, or underwriting context"
                        />
                      </div>

                      <div v-else-if="activeEditorSection === 'readiness'" class="pz-space-y-4">
                        <div class="pz-operator-form-grid">
                          <PzInput v-model="operatorForm.development_metadata.zoning_info" label="Zoning" />
                          <select v-model="operatorForm.development_metadata.development_stage" class="pz-input">
                            <option value="">Development Stage</option>
                            <option value="RAW_LAND">Raw Land</option>
                            <option value="SERVICED_SITE">Serviced Site</option>
                            <option value="IN_DESIGN">In Design</option>
                            <option value="IN_PROGRESS">In Progress</option>
                            <option value="COMPLETED">Completed</option>
                          </select>
                          <PzInput v-model="operatorForm.development_metadata.recommended_use" label="Recommended Use" />
                          <PzInput v-model="operatorForm.development_metadata.estimated_completion_budget" label="Completion Budget" type="number" />
                          <PzInput v-model="operatorForm.development_metadata.expected_completion_date" label="Expected Completion Date" type="date" />
                          <PzInput v-model="operatorForm.development_metadata.utilities_text" label="Utilities" />
                        </div>
                        <div class="pz-operator-toggle-grid">
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.development_metadata.build_ready" type="checkbox" />
                            <span>Build ready</span>
                          </label>
                        </div>
                      </div>

                      <div v-else class="pz-space-y-4">
                        <div class="pz-operator-form-grid">
                          <PzInput v-model="operatorForm.ownership_profile.legal_owner_name" label="Legal Owner Name" />
                          <select v-model="operatorForm.ownership_profile.ownership_type" class="pz-input">
                            <option value="">Ownership Type</option>
                            <option value="INDIVIDUAL">Individual</option>
                            <option value="COMPANY">Company</option>
                            <option value="TRUST">Trust</option>
                            <option value="GOVERNMENT">Government</option>
                            <option value="OTHER">Other</option>
                          </select>
                          <PzInput v-model="operatorForm.ownership_profile.title_reference" label="Title Reference" />
                          <PzInput v-model="operatorForm.ownership_profile.deed_reference" label="Deed Reference" />
                        </div>
                        <div class="pz-operator-toggle-grid">
                          <label class="pz-checkbox-row">
                            <input v-model="operatorForm.ownership_profile.has_liens" type="checkbox" />
                            <span>Has liens</span>
                          </label>
                        </div>
                        <textarea
                          v-model="operatorForm.ownership_profile.lien_notes"
                          class="pz-input"
                          rows="3"
                          placeholder="Lien notes"
                        />
                        <textarea
                          v-model="operatorForm.ownership_profile.disclosure_notes"
                          class="pz-input"
                          rows="3"
                          placeholder="Disclosure notes"
                        />
                        <textarea
                          v-model="operatorForm.featureText"
                          class="pz-input"
                          rows="3"
                          placeholder="Feature highlights, comma separated"
                        />
                      </div>
                    </div>

                    <div class="pz-editor-actions">
                      <div class="pz-editor-actions__summary">
                        <span class="pz-editor-status">Editing: {{ activeEditorMeta.label }}</span>
                        <span class="pz-u-text-mono text-xs pz-u-color-steel">Changes save back to the live listing.</span>
                      </div>
                      <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                        <Button variant="ghost" @click="cancelEditing">Cancel</Button>
                        <Button variant="primary" :loading="savingProperty" @click="saveProperty">
                          Save Changes
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            <Card title="Overview">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Owner</span>
                  <span class="pz-property-detail__value">{{ property.owner_name }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Manager</span>
                  <span class="pz-property-detail__value">{{ property.manager_name || 'Owner-managed' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Address</span>
                  <span class="pz-property-detail__value">{{ property.formatted_address || property.location_display || 'Address pending' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Finance</span>
                  <span class="pz-property-detail__value">{{ property.financing_allowed ? 'Financing supported' : 'Direct purchase only' }}</span>
                </div>
              </div>
            </Card>

            <Card title="Market Positioning">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in marketStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <span class="pz-property-detail__value">{{ stat.value }}</span>
                </div>
              </div>
            </Card>

            <Card v-if="mediaGallery.length" title="Media">
              <div class="pz-property-gallery">
                <a
                  v-for="asset in mediaGallery"
                  :key="asset.id"
                  :href="asset.media_url || asset.external_url"
                  class="pz-property-gallery__item"
                  target="_blank"
                  rel="noreferrer"
                >
                  <div class="pz-property-gallery__preview">
                    <img
                      v-if="asset.media_type === 'IMAGE' && (asset.media_url || asset.external_url)"
                      :src="asset.media_url || asset.external_url"
                      :alt="asset.alt_text || asset.title"
                    />
                    <div v-else class="pz-property-gallery__placeholder">
                      {{ readableMediaType(asset.media_type) }}
                    </div>
                  </div>
                  <div class="pz-space-y-1">
                    <div class="pz-u-text-display text-sm">{{ asset.title || readableMediaType(asset.media_type) }}</div>
                    <div class="pz-u-text-mono text-xs pz-u-color-steel">{{ asset.caption || 'Open asset' }}</div>
                  </div>
                </a>
              </div>
            </Card>

            <Card title="Property Specification">
              <div v-if="specificationStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
                <div v-for="stat in specificationStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <span class="pz-property-detail__value">{{ stat.value }}</span>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No structured specification has been published yet.</p>
            </Card>

            <Card title="Development Readiness">
              <div v-if="property.development_metadata" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Zoning</span>
                  <span class="pz-property-detail__value">{{ property.development_metadata.zoning_info || 'Not specified' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Build Ready</span>
                  <span class="pz-property-detail__value">{{ property.development_metadata.build_ready ? 'Yes' : 'No' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Development Stage</span>
                  <span class="pz-property-detail__value">{{ property.development_metadata.development_stage || 'Not specified' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Utilities</span>
                  <span class="pz-property-detail__value">{{ formatUtilities(property.development_metadata.utilities_available) }}</span>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Development metadata has not been published for this property yet.</p>
            </Card>

            <Card title="Features And Amenities">
              <div v-if="property.features?.length" class="pz-property-feature-grid">
                <div v-for="feature in property.features" :key="feature.id" class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">{{ feature.category || 'Feature' }}</span>
                  <span class="pz-property-detail__value">{{ feature.name }}</span>
                  <span v-if="feature.description" class="pz-u-text-mono text-xs pz-u-color-steel">{{ feature.description }}</span>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No feature list published yet.</p>
            </Card>

            <Card title="Property Operations">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Ownership</span>
                  <span class="pz-property-detail__value">{{ ownershipSummary }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Verification</span>
                  <span class="pz-property-detail__value">{{ property.ownership_profile?.verification_status || 'UNVERIFIED' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Pricing Strategy</span>
                  <span class="pz-property-detail__value">{{ property.pricing_profile?.pricing_strategy || 'FIXED' }}</span>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">Deposit</span>
                  <span class="pz-property-detail__value">{{ depositSummary }}</span>
                </div>
              </div>
            </Card>

            <Card title="Financial Structure">
              <div v-if="financialStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in financialStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <span class="pz-property-detail__value">{{ stat.value }}</span>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Detailed pricing data has not been published yet.</p>
            </Card>

            <Card title="Ownership And Compliance">
              <div v-if="ownershipStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in ownershipStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <span class="pz-property-detail__value">{{ stat.value }}</span>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Ownership diligence notes have not been published yet.</p>
            </Card>

            <Card title="Linked Projects">
              <div v-if="property.linked_projects?.length" class="pz-space-y-3">
                <router-link v-for="link in property.linked_projects" :key="link.id" :to="`/projects/${link.project}`" class="pz-property-detail__link-card">
                  <span class="pz-u-text-display text-sm">{{ link.project_title }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-steel">Open project workspace</span>
                </router-link>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">This property is currently operating as a standalone asset.</p>
            </Card>

            <Card title="Suggested Materials">
              <div v-if="materials.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
                <router-link v-for="material in materials" :key="material.id" :to="`/products/${material.id}`" class="pz-property-detail__link-card">
                  <span class="pz-u-text-display text-sm">{{ material.name }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ configStore.formatPrice(material.base_price) }}</span>
                </router-link>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No material suggestions available yet.</p>
            </Card>
          </section>

          <aside class="pz-space-y-6">
            <Card title="Showings And Visits">
              <div v-if="property.showings?.length" class="pz-space-y-3 u-mb-4">
                <div v-for="showing in property.showings" :key="showing.id" class="pz-property-detail__feed">
                  <strong>{{ readableShowingType(showing.event_type) }}</strong>
                  <span>{{ formatDateTime(showing.start_at) }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ showing.instructions || readableOccurrenceType(showing.occurrence_type) }}</span>
                </div>
              </div>
              <div v-if="availableSlots.length" class="pz-space-y-3">
                <label v-for="slot in availableSlots" :key="slot.start_at" class="pz-property-detail__slot">
                  <input v-model="selectedSlot" type="radio" :value="slot" />
                  <span>{{ formatSlot(slot) }}</span>
                </label>
                <form class="pz-space-y-4 u-mt-4" @submit.prevent="submitAppointment">
                  <PzInput v-model="appointmentForm.full_name" label="Full Name" required />
                  <PzInput v-model="appointmentForm.email" label="Email" type="email" />
                  <PzInput v-model="appointmentForm.phone_number" label="Phone Number" />
                  <textarea v-model="appointmentForm.notes" class="pz-input" rows="3" placeholder="Add visit notes or questions" />
                  <Button type="submit" variant="outline" fullWidth :loading="submittingAppointment">Book Visit</Button>
                </form>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No public appointment slots are currently available.</p>
            </Card>

            <Card title="Availability Snapshot">
              <div class="pz-space-y-3">
                <div v-for="stat in availabilityStats" :key="stat.label" class="pz-property-detail__feed">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <strong>{{ stat.value }}</strong>
                </div>
              </div>
            </Card>

            <Card title="Inquiry">
              <form class="pz-space-y-4" @submit.prevent="submitInquiry">
                <PzInput v-model="inquiryForm.full_name" label="Full Name" required />
                <PzInput v-model="inquiryForm.email" label="Email" type="email" />
                <PzInput v-model="inquiryForm.phone_number" label="Phone Number" />
                <select v-model="inquiryForm.inquiry_type" class="pz-input">
                  <option value="GENERAL">General</option>
                  <option value="VIEWING">Viewing</option>
                  <option value="FINANCING">Financing</option>
                  <option value="MATERIALS">Materials</option>
                  <option value="SERVICE">Service</option>
                </select>
                <textarea v-model="inquiryForm.message" class="pz-input" rows="4" placeholder="How can the owner or manager help?" />
                <Button type="submit" variant="primary" fullWidth :loading="submittingInquiry">Send Inquiry</Button>
              </form>
            </Card>

            <Card title="Financing">
              <div v-if="financeProducts.length" class="pz-space-y-4">
                <div class="pz-property-side-note">
                  <span class="pz-u-text-mono text-xs pz-u-color-concrete">Finance target</span>
                  <strong>{{ property.financing_allowed ? 'Property-ready application' : 'Project-linked finance only' }}</strong>
                </div>
                <select v-model="financeForm.product" class="pz-input">
                  <option disabled value="">Select financing product</option>
                  <option v-for="product in financeProducts" :key="product.id" :value="product.id">{{ product.name }}</option>
                </select>
                <select v-model="financeForm.purpose_category" class="pz-input">
                  <option value="ACQUISITION">Acquisition</option>
                  <option value="COMPLETION">Completion</option>
                  <option value="RENOVATION">Renovation</option>
                </select>
                <PzInput v-model="financeForm.requested_amount" type="number" label="Requested Amount" />
                <textarea v-model="financeForm.purpose" class="pz-input" rows="3" placeholder="Describe what the financing will support" />
                <Button variant="primary" fullWidth :loading="submittingFinance" @click="submitFinance">Apply For Financing</Button>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Financing products are not available at the moment.</p>
            </Card>

            <Card v-if="operatorView" title="Operator Feed">
              <div class="pz-space-y-4">
                <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                  <div v-for="stat in operatorStats" :key="stat.label" class="pz-property-detail__metric">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
                <div>
                  <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Recent Inquiries</div>
                  <div v-if="operatorInquiries.length" class="pz-space-y-2">
                    <div v-for="inquiry in operatorInquiries.slice(0, 4)" :key="inquiry.id" class="pz-property-detail__feed">
                      <strong>{{ inquiry.full_name }}</strong>
                      <span>{{ inquiry.inquiry_type }}</span>
                      <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ inquiry.email || inquiry.phone_number || 'No contact provided' }}</span>
                    </div>
                  </div>
                  <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No inquiries yet.</p>
                </div>
                <div>
                  <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Upcoming Appointments</div>
                  <div v-if="operatorAppointments.length" class="pz-space-y-2">
                    <div v-for="appointment in operatorAppointments.slice(0, 4)" :key="appointment.id" class="pz-property-detail__feed">
                      <strong>{{ appointment.full_name }}</strong>
                      <span>{{ formatDateTime(appointment.scheduled_start) }}</span>
                      <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ appointment.email || appointment.phone_number || 'No contact provided' }}</span>
                    </div>
                  </div>
                  <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No appointments scheduled.</p>
                </div>
              </div>
            </Card>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Card from '../components/ui/Card.vue';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import PzInput from '../components/PzInput.vue';

const route = useRoute();
const authStore = useAuthStore();
const configStore = useConfigStore();
const showAlert = inject('showAlert');

const property = ref(null);
const availableSlots = ref([]);
const financeProducts = ref([]);
const materials = ref([]);
const operatorInquiries = ref([]);
const operatorAppointments = ref([]);
const selectedSlot = ref(null);
const loading = ref(true);
const editMode = ref(false);
const savingProperty = ref(false);
const activeEditorSection = ref('listing');
const submittingInquiry = ref(false);
const submittingAppointment = ref(false);
const submittingFinance = ref(false);
const operatorForm = ref(createDefaultOperatorForm());

const inquiryForm = ref({
  full_name: '',
  email: '',
  phone_number: '',
  inquiry_type: 'GENERAL',
  message: '',
});

const appointmentForm = ref({
  full_name: '',
  email: '',
  phone_number: '',
  notes: '',
});

const financeForm = ref({
  product: '',
  requested_amount: '',
  purpose_category: 'ACQUISITION',
  purpose: '',
});

const operatorView = computed(() => {
  if (!property.value || !authStore.user) return false;
  return authStore.isAdmin || authStore.user.id === property.value.owner || authStore.user.id === property.value.manager;
});

const canModifyProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  return authStore.user.id === property.value.owner;
});

const heroMediaUrl = computed(() => property.value?.primary_media?.media_url || property.value?.primary_media?.external_url || '');

const mediaGallery = computed(() => property.value?.media_assets || []);

const displayPrice = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (pricing?.asking_price) {
    return `${configStore.formatPrice(pricing.asking_price)} ${pricing.pricing_strategy || ''}`.trim();
  }
  if (property.value?.price_estimate) {
    return configStore.formatPrice(property.value.price_estimate);
  }
  return 'Price on request';
});

const marketStats = computed(() => {
  if (!property.value) return [];
  const items = [
    { label: 'Listing Type', value: property.value.listing_type },
    { label: 'Asset Type', value: property.value.asset_type },
    { label: 'Listing Status', value: property.value.status },
    { label: 'Purpose', value: property.value.purpose_name || property.value.purpose_slug || 'Not classified' },
    { label: 'Location', value: property.value.location_display || property.value.location_text || 'Location pending' },
    { label: 'Published', value: formatDate(property.value.created_at) },
    { label: 'Last Updated', value: formatDate(property.value.updated_at) },
    { label: 'Public Inquiry', value: property.value.inquiry_enabled ? 'Open' : 'Closed' },
    { label: 'Appointment Booking', value: property.value.appointment_enabled ? 'Open' : 'Closed' },
  ];
  return items.filter((item) => item.value);
});

const summaryStats = computed(() => {
  if (!property.value) return [];
  const specification = property.value.specification || {};
  const stats = [
    { label: 'Bedrooms', value: specification.bedrooms },
    { label: 'Bathrooms', value: specification.bathrooms },
    { label: 'Parking', value: specification.parking_spaces },
    {
      label: 'Internal Area',
      value: specification.internal_area ? `${specification.internal_area} ${specification.internal_area_unit}` : '',
    },
  ];
  return stats.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const specificationStats = computed(() => {
  const specification = property.value?.specification;
  if (!specification) return [];
  const stats = [
    { label: 'Bedrooms', value: specification.bedrooms },
    { label: 'Bathrooms', value: specification.bathrooms },
    { label: 'Floors', value: specification.floors },
    { label: 'Parking Spaces', value: specification.parking_spaces },
    {
      label: 'Internal Area',
      value: specification.internal_area ? `${specification.internal_area} ${specification.internal_area_unit}` : '',
    },
    {
      label: 'Lot Size',
      value: specification.lot_size ? `${specification.lot_size} ${specification.lot_size_unit}` : '',
    },
    { label: 'Year Built', value: specification.year_built },
    { label: 'Renovation Year', value: specification.renovation_year },
    { label: 'Furnishing', value: specification.furnishing_state },
    { label: 'Condition', value: specification.condition_rating },
    { label: 'Energy Rating', value: specification.energy_rating },
    { label: 'Occupancy', value: specification.occupancy_status },
  ];
  return stats.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const ownershipSummary = computed(() => {
  const ownership = property.value?.ownership_profile;
  if (!ownership) return 'Ownership profile not published';
  return ownership.legal_owner_name || ownership.ownership_type || 'Ownership profile available';
});

const depositSummary = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (!pricing?.requires_deposit) return 'No deposit requirement published';
  if (pricing.deposit_amount) return configStore.formatPrice(pricing.deposit_amount);
  return 'Deposit required';
});

const financialStats = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (!pricing) return [];
  const items = [
    { label: 'Currency', value: pricing.currency },
    { label: 'Asking Price', value: formatMoney(pricing.asking_price) },
    { label: 'Rent Amount', value: formatMoney(pricing.rent_amount) },
    { label: 'Pricing Strategy', value: pricing.pricing_strategy },
    {
      label: 'Price Per Unit',
      value: pricing.price_per_area_unit ? `${configStore.formatPrice(pricing.price_per_area_unit)} / ${pricing.area_unit}` : '',
    },
    { label: 'Service Charge', value: formatMoney(pricing.service_charge_amount) },
    { label: 'Tax Percentage', value: pricing.tax_percentage ? `${pricing.tax_percentage}%` : '' },
    { label: 'Insurance Percentage', value: pricing.insurance_percentage ? `${pricing.insurance_percentage}%` : '' },
    { label: 'Financing Notes', value: pricing.financing_notes },
  ];
  return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const ownershipStats = computed(() => {
  const ownership = property.value?.ownership_profile;
  if (!ownership) return [];
  const items = [
    { label: 'Legal Owner', value: ownership.legal_owner_name },
    { label: 'Ownership Type', value: ownership.ownership_type },
    { label: 'Title Reference', value: ownership.title_reference },
    { label: 'Deed Reference', value: ownership.deed_reference },
    { label: 'Verification Status', value: ownership.verification_status },
    { label: 'Lien Position', value: ownership.has_liens ? 'Liens declared' : 'No liens declared' },
    { label: 'Lien Notes', value: ownership.lien_notes },
    { label: 'Disclosure Notes', value: ownership.disclosure_notes },
  ];
  return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const availabilityStats = computed(() => {
  const nextSlot = availableSlots.value[0];
  return [
    { label: 'Open Slots', value: availableSlots.value.length ? `${availableSlots.value.length} available` : 'No open slots' },
    { label: 'Next Available Slot', value: nextSlot ? formatSlot(nextSlot) : 'Not scheduled' },
    { label: 'Published Showings', value: property.value?.showings?.length ? `${property.value.showings.length} scheduled` : 'No showings' },
  ];
});

const operatorStats = computed(() => [
  { label: 'Open Leads', value: operatorInquiries.value.length },
  { label: 'Scheduled Appointments', value: operatorAppointments.value.length },
  { label: 'Open Slots', value: availableSlots.value.length },
  { label: 'Linked Projects', value: property.value?.linked_projects?.length || 0 },
]);

const editorSections = [
  { id: 'listing', kicker: '01', label: 'Listing Basics', description: 'Identity, status, and visibility controls.' },
  { id: 'specification', kicker: '02', label: 'Specification', description: 'Beds, area, fit-out, and occupancy data.' },
  { id: 'commercial', kicker: '03', label: 'Commercials', description: 'Pricing, deposit, and finance posture.' },
  { id: 'readiness', kicker: '04', label: 'Readiness', description: 'Development stage, utilities, and delivery context.' },
  { id: 'ownership', kicker: '05', label: 'Ownership', description: 'Title references, disclosures, and highlights.' },
];

const activeEditorMeta = computed(() =>
  editorSections.find((section) => section.id === activeEditorSection.value) || editorSections[0]
);

function formatUtilities(items) {
  if (!items?.length) return 'Not specified';
  return items.join(', ');
}

function formatMoney(value) {
  if (value === null || value === undefined || value === '') return '';
  return configStore.formatPrice(value);
}

function formatDate(value) {
  if (!value) return '';
  return new Date(value).toLocaleDateString();
}

function formatDateTime(value) {
  return new Date(value).toLocaleString();
}

function formatSlot(slot) {
  return `${formatDateTime(slot.start_at)} - ${new Date(slot.end_at).toLocaleTimeString()}`;
}

function readableMediaType(type) {
  return (type || '').replaceAll('_', ' ');
}

function readableShowingType(type) {
  return (type || '').replaceAll('_', ' ');
}

function readableOccurrenceType(type) {
  return (type || '').replaceAll('_', ' ');
}

function createDefaultOperatorForm() {
  return {
    title: '',
    description: '',
    asset_type: 'RESIDENTIAL',
    listing_type: 'SALE',
    status: 'ACTIVE',
    location_text: '',
    formatted_address: '',
    price_estimate: '',
    financing_allowed: false,
    inquiry_enabled: true,
    appointment_enabled: true,
    featureText: '',
    specification: {
      bedrooms: '',
      bathrooms: '',
      floors: '',
      parking_spaces: '',
      internal_area: '',
      internal_area_unit: 'SQM',
      lot_size: '',
      lot_size_unit: 'SQM',
      year_built: '',
      renovation_year: '',
      furnishing_state: '',
      condition_rating: '',
      energy_rating: '',
      occupancy_status: '',
    },
    development_metadata: {
      zoning_info: '',
      build_ready: false,
      development_stage: '',
      estimated_completion_budget: '',
      expected_completion_date: '',
      recommended_use: '',
      utilities_text: '',
    },
    pricing_profile: {
      currency: 'KES',
      asking_price: '',
      rent_amount: '',
      pricing_strategy: 'FIXED',
      requires_deposit: false,
      deposit_amount: '',
      price_per_area_unit: '',
      area_unit: 'SQM',
      service_charge_amount: '',
      tax_percentage: '',
      insurance_percentage: '',
      financing_notes: '',
    },
    ownership_profile: {
      legal_owner_name: '',
      ownership_type: '',
      title_reference: '',
      deed_reference: '',
      has_liens: false,
      lien_notes: '',
      disclosure_notes: '',
    },
  };
}

function numberOrNull(value) {
  return value === '' || value === null || value === undefined ? null : Number(value);
}

function hydrateOperatorForm(source) {
  const spec = source?.specification || {};
  const development = source?.development_metadata || {};
  const pricing = source?.pricing_profile || {};
  const ownership = source?.ownership_profile || {};

  operatorForm.value = {
    title: source?.title || '',
    description: source?.description || '',
    asset_type: source?.asset_type || 'RESIDENTIAL',
    listing_type: source?.listing_type || 'SALE',
    status: source?.status || 'ACTIVE',
    location_text: source?.location_text || '',
    formatted_address: source?.formatted_address || '',
    price_estimate: source?.price_estimate || '',
    financing_allowed: Boolean(source?.financing_allowed),
    inquiry_enabled: source?.inquiry_enabled !== false,
    appointment_enabled: source?.appointment_enabled !== false,
    featureText: (source?.features || []).map((feature) => feature.name).filter(Boolean).join(', '),
    specification: {
      bedrooms: spec.bedrooms ?? '',
      bathrooms: spec.bathrooms ?? '',
      floors: spec.floors ?? '',
      parking_spaces: spec.parking_spaces ?? '',
      internal_area: spec.internal_area ?? '',
      internal_area_unit: spec.internal_area_unit || 'SQM',
      lot_size: spec.lot_size ?? '',
      lot_size_unit: spec.lot_size_unit || 'SQM',
      year_built: spec.year_built ?? '',
      renovation_year: spec.renovation_year ?? '',
      furnishing_state: spec.furnishing_state || '',
      condition_rating: spec.condition_rating || '',
      energy_rating: spec.energy_rating || '',
      occupancy_status: spec.occupancy_status || '',
    },
    development_metadata: {
      zoning_info: development.zoning_info || '',
      build_ready: Boolean(development.build_ready),
      development_stage: development.development_stage || '',
      estimated_completion_budget: development.estimated_completion_budget ?? '',
      expected_completion_date: development.expected_completion_date || '',
      recommended_use: development.recommended_use || '',
      utilities_text: (development.utilities_available || []).join(', '),
    },
    pricing_profile: {
      currency: pricing.currency || 'KES',
      asking_price: pricing.asking_price ?? '',
      rent_amount: pricing.rent_amount ?? '',
      pricing_strategy: pricing.pricing_strategy || 'FIXED',
      requires_deposit: Boolean(pricing.requires_deposit),
      deposit_amount: pricing.deposit_amount ?? '',
      price_per_area_unit: pricing.price_per_area_unit ?? '',
      area_unit: pricing.area_unit || 'SQM',
      service_charge_amount: pricing.service_charge_amount ?? '',
      tax_percentage: pricing.tax_percentage ?? '',
      insurance_percentage: pricing.insurance_percentage ?? '',
      financing_notes: pricing.financing_notes || '',
    },
    ownership_profile: {
      legal_owner_name: ownership.legal_owner_name || '',
      ownership_type: ownership.ownership_type || '',
      title_reference: ownership.title_reference || '',
      deed_reference: ownership.deed_reference || '',
      has_liens: Boolean(ownership.has_liens),
      lien_notes: ownership.lien_notes || '',
      disclosure_notes: ownership.disclosure_notes || '',
    },
  };
}

function buildPropertyPayload() {
  const featureNames = operatorForm.value.featureText
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);

  return {
    title: operatorForm.value.title,
    description: operatorForm.value.description,
    asset_type: operatorForm.value.asset_type,
    listing_type: operatorForm.value.listing_type,
    status: operatorForm.value.status,
    location_text: operatorForm.value.location_text,
    formatted_address: operatorForm.value.formatted_address,
    price_estimate: numberOrNull(operatorForm.value.price_estimate),
    financing_allowed: operatorForm.value.financing_allowed,
    inquiry_enabled: operatorForm.value.inquiry_enabled,
    appointment_enabled: operatorForm.value.appointment_enabled,
    specification: {
      bedrooms: numberOrNull(operatorForm.value.specification.bedrooms),
      bathrooms: numberOrNull(operatorForm.value.specification.bathrooms),
      floors: numberOrNull(operatorForm.value.specification.floors),
      parking_spaces: numberOrNull(operatorForm.value.specification.parking_spaces),
      internal_area: numberOrNull(operatorForm.value.specification.internal_area),
      internal_area_unit: operatorForm.value.specification.internal_area_unit,
      lot_size: numberOrNull(operatorForm.value.specification.lot_size),
      lot_size_unit: operatorForm.value.specification.lot_size_unit,
      year_built: numberOrNull(operatorForm.value.specification.year_built),
      renovation_year: numberOrNull(operatorForm.value.specification.renovation_year),
      furnishing_state: operatorForm.value.specification.furnishing_state,
      condition_rating: operatorForm.value.specification.condition_rating,
      energy_rating: operatorForm.value.specification.energy_rating,
      occupancy_status: operatorForm.value.specification.occupancy_status,
    },
    development_metadata: {
      zoning_info: operatorForm.value.development_metadata.zoning_info,
      build_ready: operatorForm.value.development_metadata.build_ready,
      development_stage: operatorForm.value.development_metadata.development_stage,
      estimated_completion_budget: numberOrNull(operatorForm.value.development_metadata.estimated_completion_budget),
      expected_completion_date: operatorForm.value.development_metadata.expected_completion_date || null,
      recommended_use: operatorForm.value.development_metadata.recommended_use,
      utilities_available: operatorForm.value.development_metadata.utilities_text
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
    },
    pricing_profile: {
      currency: operatorForm.value.pricing_profile.currency,
      asking_price: numberOrNull(operatorForm.value.pricing_profile.asking_price),
      rent_amount: numberOrNull(operatorForm.value.pricing_profile.rent_amount),
      pricing_strategy: operatorForm.value.pricing_profile.pricing_strategy,
      requires_deposit: operatorForm.value.pricing_profile.requires_deposit,
      deposit_amount: numberOrNull(operatorForm.value.pricing_profile.deposit_amount),
      price_per_area_unit: numberOrNull(operatorForm.value.pricing_profile.price_per_area_unit),
      area_unit: operatorForm.value.pricing_profile.area_unit,
      service_charge_amount: numberOrNull(operatorForm.value.pricing_profile.service_charge_amount),
      tax_percentage: numberOrNull(operatorForm.value.pricing_profile.tax_percentage),
      insurance_percentage: numberOrNull(operatorForm.value.pricing_profile.insurance_percentage),
      financing_notes: operatorForm.value.pricing_profile.financing_notes,
    },
    ownership_profile: {
      legal_owner_name: operatorForm.value.ownership_profile.legal_owner_name,
      ownership_type: operatorForm.value.ownership_profile.ownership_type,
      title_reference: operatorForm.value.ownership_profile.title_reference,
      deed_reference: operatorForm.value.ownership_profile.deed_reference,
      has_liens: operatorForm.value.ownership_profile.has_liens,
      lien_notes: operatorForm.value.ownership_profile.lien_notes,
      disclosure_notes: operatorForm.value.ownership_profile.disclosure_notes,
    },
    features: featureNames.map((name, index) => ({
      name,
      category: 'Highlight',
      is_highlighted: index < 6,
      sort_order: index + 1,
    })),
  };
}

function toggleEditMode() {
  editMode.value = !editMode.value;
  if (editMode.value && property.value) {
    activeEditorSection.value = 'listing';
    hydrateOperatorForm(property.value);
  }
}

function cancelEditing() {
  if (property.value) {
    hydrateOperatorForm(property.value);
  }
  activeEditorSection.value = 'listing';
  editMode.value = false;
}

async function loadProperty() {
  loading.value = true;
  try {
    const [propertyRes, availabilityRes, financeRes, materialsRes] = await Promise.all([
      api.get(`/property/${route.params.id}/`),
      api.get(`/property/${route.params.id}/availability/`),
      api.get('/v3/finance/products/'),
      api.get('/v1/products/'),
    ]);

    property.value = propertyRes.data;
    hydrateOperatorForm(propertyRes.data);
    availableSlots.value = availabilityRes.data;
    financeProducts.value = financeRes.data.results || financeRes.data;
    materials.value = (materialsRes.data.results || materialsRes.data || []).slice(0, 3);

    if (operatorView.value) {
      const [inquiriesRes, appointmentsRes] = await Promise.all([
        api.get('/property/inquiries/', { params: { property: route.params.id } }),
        api.get('/property/appointments/', { params: { property: route.params.id } }),
      ]);
      operatorInquiries.value = inquiriesRes.data.results || inquiriesRes.data;
      operatorAppointments.value = appointmentsRes.data.results || appointmentsRes.data;
    }
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property details.', 'error');
  } finally {
    loading.value = false;
  }
}

async function saveProperty() {
  if (!canModifyProperty.value) return;
  savingProperty.value = true;
  try {
    await api.patch(`/property/${route.params.id}/`, buildPropertyPayload());
    showAlert?.('Property updated successfully.', 'success');
    editMode.value = false;
    await loadProperty();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to update property.', 'error');
  } finally {
    savingProperty.value = false;
  }
}

async function submitInquiry() {
  submittingInquiry.value = true;
  try {
    await api.post('/property/inquiries/', {
      property: route.params.id,
      ...inquiryForm.value,
    });
    showAlert?.('Inquiry submitted successfully.', 'success');
    inquiryForm.value = { full_name: '', email: '', phone_number: '', inquiry_type: 'GENERAL', message: '' };
    await loadProperty();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to submit inquiry.', 'error');
  } finally {
    submittingInquiry.value = false;
  }
}

async function submitAppointment() {
  if (!selectedSlot.value) {
    showAlert?.('Select an available slot first.', 'error');
    return;
  }

  submittingAppointment.value = true;
  try {
    await api.post('/property/appointments/', {
      property: route.params.id,
      availability_window: selectedSlot.value.window_id,
      scheduled_start: selectedSlot.value.start_at,
      scheduled_end: selectedSlot.value.end_at,
      ...appointmentForm.value,
    });
    showAlert?.('Appointment request submitted.', 'success');
    appointmentForm.value = { full_name: '', email: '', phone_number: '', notes: '' };
    selectedSlot.value = null;
    await loadProperty();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to book appointment.', 'error');
  } finally {
    submittingAppointment.value = false;
  }
}

async function submitFinance() {
  if (!authStore.isAuthenticated) {
    showAlert?.('Sign in to apply for financing.', 'error');
    return;
  }

  submittingFinance.value = true;
  try {
    await api.post('/v3/finance/applications/', {
      product: financeForm.value.product,
      target_type: 'PROPERTY',
      property: route.params.id,
      requested_amount: financeForm.value.requested_amount,
      purpose_category: financeForm.value.purpose_category,
      purpose: financeForm.value.purpose,
    });
    showAlert?.('Financing application submitted.', 'success');
    financeForm.value = { product: '', requested_amount: '', purpose_category: 'ACQUISITION', purpose: '' };
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to submit financing application.', 'error');
  } finally {
    submittingFinance.value = false;
  }
}

onMounted(loadProperty);
</script>

<style scoped>
.pz-property-page {
  /* Premium dynamic background using brand colors */
  background: 
    radial-gradient(circle at top left, rgba(212, 101, 42, 0.06), transparent 40%),
    radial-gradient(circle at bottom right, rgba(184, 115, 51, 0.05), transparent 40%),
    linear-gradient(180deg, var(--pz-color-limestone-white) 0%, #f4f1ea 100%);
  color: var(--pz-color-foundation-black);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: var(--pz-font-primary);
}

/* Decorative ambient background glows using brand colors */
.pz-property-page::before,
.pz-property-page::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
  pointer-events: none;
}
.pz-property-page::before {
  top: -10%; left: -10%; width: 600px; height: 600px;
  background: rgba(212, 101, 42, 0.12); /* Earth Orange */
}
.pz-property-page::after {
  bottom: 10%; right: -10%; width: 700px; height: 700px;
  background: rgba(184, 115, 51, 0.08); /* Copper Circuit */
}

/* Ensure content is above background blobs */
.pz-l-container {
  position: relative;
  z-index: 1;
}

/* No need to override deep card styles heavily if it defaults to light, 
   but we ensure glassmorphism is perfect */
:deep(.pz-card) {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(24px) !important;
  border: 1px solid rgba(10, 10, 15, 0.08) !important;
  box-shadow: 0 16px 32px -12px rgba(10, 10, 15, 0.08) !important;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease !important;
}
:deep(.pz-card:hover) {
  transform: translateY(-4px) !important;
  box-shadow: 0 24px 46px rgba(10, 10, 15, 0.12), 0 0 0 1px rgba(212, 101, 42, 0.12) !important;
  border-color: var(--pz-color-earth-orange) !important;
}

/* Hero Section */
.pz-property-hero {
  display: grid;
  gap: 2.5rem;
  grid-template-columns: 1.3fr 1fr;
  padding: 2.5rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow: 0 25px 50px -12px rgba(10, 10, 15, 0.1);
  margin-bottom: 2rem;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-property-hero:hover {
  transform: translateY(-6px);
  box-shadow: 0 35px 60px -15px rgba(10, 10, 15, 0.15);
  border-color: rgba(212, 101, 42, 0.3);
}

.pz-property-hero__media {
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 10px 30px rgba(10, 10, 15, 0.15);
  min-height: 28rem;
}
.pz-property-hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.pz-property-hero__media:hover .pz-property-hero__image {
  transform: scale(1.06);
}
.pz-property-hero__fallback {
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, var(--pz-color-structural-steel), var(--pz-color-foundation-black));
  color: var(--pz-color-limestone-white);
  min-height: 28rem;
  flex-direction: column;
}

.pz-property-hero__content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.5rem;
}

.pz-u-text-display {
  font-family: var(--pz-font-display);
  font-size: 2.75rem;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--pz-color-foundation-black) 0%, var(--pz-color-structural-steel) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.pz-property-hero__description {
  line-height: 1.7;
  color: var(--pz-color-structural-steel);
  font-size: 1.05rem;
}

.pz-property-hero__price {
  padding: 1.5rem;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(212, 101, 42, 0.05), rgba(212, 101, 42, 0.01));
  border: 1px solid rgba(212, 101, 42, 0.15);
  border-left: 4px solid var(--pz-color-earth-orange);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  box-shadow: inset 0 2px 10px rgba(255, 255, 255, 0.5);
}
.pz-property-hero__price strong {
  font-family: var(--pz-font-display);
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--pz-color-earth-orange);
}

/* Feature Grids */
.pz-property-summary-grid,
.pz-property-feature-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
}

.pz-property-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}
.pz-property-chip {
  padding: 0.4rem 1rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.1);
  border: 1px solid rgba(212, 101, 42, 0.2);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: all 0.3s ease;
}
.pz-property-chip:hover {
  background: rgba(212, 101, 42, 0.15);
  border-color: rgba(212, 101, 42, 0.3);
  transform: translateY(-2px);
}

/* Media Gallery */
.pz-property-gallery {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}
.pz-property-gallery__item,
.pz-property-detail__link-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.08);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-property-gallery__item:hover,
.pz-property-detail__link-card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(212, 101, 42, 0.3);
  box-shadow: 0 15px 30px -5px rgba(10, 10, 15, 0.1);
}

.pz-property-gallery__preview {
  height: 12rem;
  border-radius: 8px;
  overflow: hidden;
  background: var(--pz-color-concrete-grey);
}
.pz-property-gallery__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.pz-property-gallery__item:hover .pz-property-gallery__preview img {
  transform: scale(1.08);
}

/* Metrics and Cards inside Grid */
.pz-property-detail__metric,
.pz-property-detail__slot,
.pz-property-detail__feed,
.pz-property-side-note {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.05);
  transition: all 0.3s ease;
}
.pz-property-detail__metric:hover,
.pz-property-detail__feed:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(10, 10, 15, 0.1);
}

.pz-property-detail__label {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}
.pz-property-detail__value {
  color: var(--pz-color-structural-steel);
  font-size: 1rem;
  font-weight: 500;
}

.pz-operator-form-section {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.72);
  border-radius: 16px;
}

.pz-editor-shell {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(14rem, 17rem) minmax(0, 1fr);
}

.pz-editor-nav {
  display: grid;
  gap: 0.75rem;
  align-content: start;
}

.pz-editor-nav__item {
  display: grid;
  gap: 0.2rem;
  padding: 0.95rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.75);
  text-align: left;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.pz-editor-nav__item:hover,
.pz-editor-nav__item.is-active {
  border-color: rgba(212, 101, 42, 0.35);
  box-shadow: 0 10px 24px rgba(10, 10, 15, 0.06);
  transform: translateY(-1px);
}

.pz-editor-nav__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-editor-nav__item strong {
  font-size: 0.95rem;
}

.pz-editor-nav__item span:last-child {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
}

.pz-operator-form-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}

.pz-operator-toggle-grid {
  display: grid;
  gap: 0.8rem;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}

.pz-checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 2.8rem;
  padding: 0 0.75rem;
  border: 1px solid rgba(10, 10, 15, 0.1);
  border-radius: 12px;
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.pz-editor-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.1rem;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.92);
  position: sticky;
  bottom: 0;
  border-radius: 0 0 16px 16px;
}

.pz-editor-actions__summary {
  display: grid;
  gap: 0.2rem;
}

.pz-editor-status {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

/* Slots for appointments */
.pz-property-detail__slot {
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}
.pz-property-detail__slot:hover {
  background: rgba(255, 255, 255, 0.9);
}
.pz-property-detail__slot:has(input:checked) {
  background: rgba(212, 101, 42, 0.08);
  border-color: rgba(212, 101, 42, 0.4);
  box-shadow: inset 0 0 0 1px rgba(212, 101, 42, 0.2);
}

/* Breadcrumbs */
.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-family: var(--pz-font-mono);
}
.pz-breadcrumb__item {
  color: var(--pz-color-concrete-grey);
  text-decoration: none;
  transition: color 0.2s;
}
.pz-breadcrumb__item:hover {
  color: var(--pz-color-earth-orange);
}
.pz-breadcrumb__separator {
  color: rgba(10, 10, 15, 0.2);
}
.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-weight: 500;
}

/* Ensure inputs look clean */
:deep(.pz-input),
:deep(select.pz-input),
:deep(textarea.pz-input) {
  background: rgba(255, 255, 255, 0.8) !important;
  border: 1px solid rgba(10, 10, 15, 0.1) !important;
  color: var(--pz-color-foundation-black) !important;
  transition: all 0.3s ease !important;
}
:deep(.pz-input:focus),
:deep(select.pz-input:focus),
:deep(textarea.pz-input:focus) {
  border-color: var(--pz-color-earth-orange) !important;
  box-shadow: 0 0 0 2px rgba(212, 101, 42, 0.15) !important;
  background: white !important;
  outline: none;
}

/* Layout */
.pz-property-layout {
  display: grid;
  gap: 2.5rem;
  grid-template-columns: minmax(0, 1.6fr) minmax(22rem, 1fr);
}

@media (max-width: 1024px) {
  .pz-property-layout {
    grid-template-columns: 1fr;
  }

  .pz-editor-shell {
    grid-template-columns: 1fr;
  }

  .pz-editor-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .pz-property-hero {
    grid-template-columns: 1fr;
  }
  .pz-property-hero__media,
  .pz-property-hero__fallback {
    min-height: 20rem;
  }
}
</style>
