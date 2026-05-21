<template>
  <div class="pz-edit-page">
    <div class="pz-l-container u-py-8">
      <!-- Loading -->
      <div v-if="loading" class="pz-u-text-center u-py-20">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">Loading property data...</p>
      </div>

      <div v-else-if="property" class="pz-edit-layout">
        <!-- Header -->
        <div class="pz-edit-header">
          <nav class="pz-breadcrumb pz-u-text-mono text-xs">
            <router-link :to="`/properties/${route.params.id}`" class="pz-breadcrumb__item">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
              Property Details
            </router-link>
            <span class="pz-breadcrumb__separator">/</span>
            <span class="pz-breadcrumb__current pz-u-color-steel">Edit</span>
          </nav>

          <div class="pz-edit-header__title">
            <h1 class="pz-u-text-display">Edit Property</h1>
            <p class="pz-edit-header__subtitle">{{ property.title }}</p>
          </div>
        </div>

        <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
          <div class="pz-edit-workflow-banner">
            <div class="pz-edit-workflow-banner__summary">
              <div class="pz-edit-workflow-banner__kicker">{{ workflowSummary.stage }}</div>
              <h2 class="pz-edit-workflow-banner__title">{{ workflowSummary.title }}</h2>
              <p class="pz-edit-workflow-banner__body">{{ workflowSummary.body }}</p>
              <div class="pz-edit-workflow-banner__meta">
                <span class="pz-edit-workflow-banner__meta-item">Progress {{ workflowCompletion.completeCount }}/{{ workflowCompletion.totalCount }}</span>
                <span v-if="draftRestored" class="pz-edit-workflow-banner__meta-item">Draft restored</span>
                <span v-if="draftSavedAt" class="pz-edit-workflow-banner__meta-item">Autosaved</span>
              </div>
            </div>
            <div class="pz-edit-workflow-banner__actions">
              <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
                {{ workflowSummary.primaryAction.label }}
              </Button>
              <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
                {{ workflowSummary.secondaryAction.label }}
              </Button>
            </div>
          </div>
          <div v-if="workflowCompletion.blockers.length" class="pz-edit-workflow-blockers">
            <span class="pz-edit-workflow-blockers__label">Still needed</span>
            <div class="pz-edit-workflow-blockers__list">
              <span v-for="item in workflowCompletion.blockers" :key="item" class="pz-edit-workflow-blockers__item">{{ item }}</span>
            </div>
          </div>
          <div class="pz-edit-workflow-banner__steps">
            <div
              v-for="step in workflowSections"
              :key="step.label"
              class="pz-edit-workflow-step"
              :class="{ 'pz-edit-workflow-step--done': step.complete, 'pz-edit-workflow-step--active': step.active, 'pz-edit-workflow-step--locked': !canAdvanceToSection(step.id) }"
              @click="goToSection(step.id)"
            >
              <div class="pz-edit-workflow-step__index">{{ step.index }}</div>
              <div class="pz-edit-workflow-step__content">
                <div class="pz-edit-workflow-step__title-row">
                  <strong>{{ step.label }}</strong>
                  <span class="pz-edit-workflow-step__state">{{ step.complete ? 'Done' : step.active ? 'Now' : 'Next' }}</span>
                </div>
                <span>{{ step.help }}</span>
              </div>
            </div>
          </div>
        

        <ModuleCTA
          eyebrow="Asset Pipeline"
          title="Use this listing to generate the next project opportunity."
          body="Keep the property complete, then connect serious buyer or developer interest to project planning and procurement."
          primary-label="Preview Listing"
          primary-to="/properties"
          secondary-label="Start Project"
          secondary-to="/projects/new"
          tone="steel"
        />
</WorkflowGuide>

        <!-- Editor -->
        <div class="pz-editor-shell">
          <div class="pz-editor-nav">
            <button
              v-for="section in workflowSections"
              :key="section.id"
              type="button"
              class="pz-editor-nav__item"
              :class="{ 'is-active': activeEditorSection === section.id, 'is-locked': !canAdvanceToSection(section.id) }"
              :disabled="!canAdvanceToSection(section.id)"
              @click="goToSection(section.id)"
            >
              <span class="pz-editor-nav__icon" v-html="editorSectionIcons[section.id]"></span>
              <div class="pz-editor-nav__text">
                <strong>{{ section.label }}</strong>
                <span class="pz-editor-nav__state" :class="{ 'is-done': section.complete }">{{ section.complete ? 'Done' : section.active ? 'Next up' : 'Needs work' }}</span>
                <span>{{ section.description }}</span>
              </div>
            </button>
          </div>

          <div class="pz-operator-form-section">
            <div class="pz-operator-form-header">
              <span class="pz-operator-form__kicker">{{ activeEditorMeta.kicker }}</span>
              <strong>{{ activeEditorMeta.label }}</strong>
              <span class="pz-operator-form__desc">{{ activeEditorMeta.description }}</span>
            </div>

            <div v-if="activeEditorSection === 'listing'" class="pz-operator-form-body">
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
                  <option value="PENDING_REVIEW">Pending Review</option>
                  <option value="ACTIVE">Active</option>
                  <option value="SOLD">Sold</option>
                  <option value="LEASED">Leased</option>
                  <option value="UNDER_OFFER">Under Offer</option>
                  <option value="INACTIVE">Inactive</option>
                </select>
                <PzInput v-model="operatorForm.location_text" label="Location Text" />
                <PzInput v-model="operatorForm.formatted_address" label="Formatted Address" />
                <PzInput v-model="operatorForm.latitude" label="Latitude" type="number" />
                <PzInput v-model="operatorForm.longitude" label="Longitude" type="number" />
                <PzInput v-model="operatorForm.price_estimate" label="Estimated Value" type="number" />
              </div>
              <div class="pz-map-picker">
                <div>
                  <strong>Location Picker</strong>
                  <span>Click the pad to approximate the pin, then refine latitude and longitude if needed.</span>
                </div>
                <button type="button" class="pz-map-picker__pad" @click="setApproximateLocation">
                  <span class="pz-map-picker__pin" :style="mapPinStyle"></span>
                </button>
              </div>
              <textarea
                v-model="operatorForm.description"
                class="pz-input"
                rows="3"
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

            <div v-else-if="activeEditorSection === 'specification'" class="pz-operator-form-body">
              <div class="pz-operator-form-grid">
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
            </div>

            <div v-else-if="activeEditorSection === 'commercial'" class="pz-operator-form-body">
              <div class="pz-operator-form-grid">
                <PzInput v-model="operatorForm.pricing_profile.asking_price" label="Asking Price" type="number" />
                <PzInput v-model="operatorForm.pricing_profile.rent_amount" label="Rent Amount" type="number" />
                <select v-model="operatorForm.pricing_profile.currency" class="pz-input">
                  <option v-for="currency in configStore.availableCurrencies" :key="currency.currency_code" :value="currency.currency_code">
                    {{ currency.currency_code }}{{ currency.symbol ? ` (${currency.symbol})` : '' }}
                  </option>
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
                rows="2"
                placeholder="Financing notes, eligibility, or underwriting context"
              />
            </div>

            <div v-else-if="activeEditorSection === 'readiness'" class="pz-operator-form-body">
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

            <div v-else-if="activeEditorSection === 'media'" class="pz-operator-form-body">
              <div v-if="property?.media_assets?.length" class="pz-existing-assets">
                <div class="pz-existing-assets__title">Current Media And Documents</div>
                <div class="pz-existing-assets__grid">
                  <div v-for="asset in property.media_assets" :key="asset.id" class="pz-existing-asset">
                    <img
                      v-if="asset.media_type === 'IMAGE' && (resolveMediaUrl(asset.media_url) || asset.external_url)"
                      :src="resolveMediaUrl(asset.media_url) || asset.external_url"
                      :alt="asset.alt_text || asset.title || 'Property image'"
                      class="pz-existing-asset__thumb"
                    />
                    <div v-else class="pz-existing-asset__doc">
                      <span class="pz-existing-asset__doc-icon">📄</span>
                      <span class="pz-existing-asset__doc-name">{{ asset.title || asset.alt_text || 'Document' }}</span>
                    </div>
                    <div class="pz-existing-asset__meta">{{ asset.media_type }}</div>
                  </div>
                </div>
              </div>

              <div class="pz-upload-grid">
                <div class="pz-upload-card">
                  <div class="pz-upload-card__title">Images</div>
                  <p class="pz-u-color-steel text-sm">Upload one or more images for this property.</p>
                  <input ref="propertyImageInput" type="file" accept="image/*" multiple class="u-sr-only" @change="handlePropertyImagesSelected">
                  <input ref="propertyCameraInput" type="file" accept="image/*" capture="environment" class="u-sr-only" @change="handlePropertyImagesSelected">
                  <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                    <Button type="button" variant="secondary" size="sm" @click="triggerPropertyImageUpload">UPLOAD_IMAGES</Button>
                    <Button type="button" variant="outline" size="sm" @click="triggerPropertyCameraUpload">CAMERA_CAPTURE</Button>
                    <Button v-if="selectedPropertyImageFiles.length" type="button" variant="ghost" size="sm" @click="clearSelectedPropertyImages">CLEAR_IMAGES</Button>
                  </div>
                  <div v-if="selectedPropertyImageFiles.length" class="pz-upload-selection">
                    {{ selectedPropertyImageFiles.length }} image{{ selectedPropertyImageFiles.length === 1 ? '' : 's' }} selected.
                  </div>
                  <div v-if="selectedPropertyImagePreviews.length" class="pz-upload-preview-grid">
                    <img
                      v-for="(preview, idx) in selectedPropertyImagePreviews"
                      :key="idx"
                      :src="preview"
                      class="pz-upload-preview-thumb"
                      alt="Selected preview"
                    />
                  </div>
                </div>

                <div class="pz-upload-card">
                  <div class="pz-upload-card__title">Documents</div>
                  <p class="pz-u-color-steel text-sm">Upload documents or floor plans with a clear update action.</p>
                  <div class="pz-input-wrapper">
                    <label class="pz-input__label">Upload type</label>
                    <select v-model="propertyUploadDocumentType" class="pz-input">
                      <option value="DOCUMENT">Document</option>
                      <option value="FLOOR_PLAN">Floor Plan</option>
                    </select>
                  </div>
                  <input ref="propertyDocumentInput" type="file" multiple class="u-sr-only" @change="handlePropertyDocumentsSelected">
                  <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                    <Button type="button" variant="secondary" size="sm" @click="triggerPropertyDocumentUpload">UPLOAD_DOCUMENTS</Button>
                    <Button v-if="selectedPropertyDocumentFiles.length" type="button" variant="ghost" size="sm" @click="clearSelectedPropertyDocuments">CLEAR_DOCUMENTS</Button>
                  </div>
                  <div v-if="selectedPropertyDocumentFiles.length" class="pz-upload-selection">
                    <div
                      v-for="(file, idx) in selectedPropertyDocumentFiles"
                      :key="`${file.name}-${idx}`"
                      class="pz-document-category-row"
                    >
                      <span>{{ file.name }}</span>
                      <select v-model="selectedPropertyDocumentCategories[idx]" class="pz-input">
                        <option value="GENERAL">General</option>
                        <option value="DEED">Title Deed</option>
                        <option value="FLOOR_PLAN">Floor Plan</option>
                        <option value="COMPLIANCE">Compliance</option>
                        <option value="SURVEY">Survey</option>
                        <option value="VALUATION">Valuation</option>
                        <option value="BROCHURE">Brochure</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                <Button
                  type="button"
                  variant="primary"
                  size="sm"
                  :loading="uploadingMedia"
                  :disabled="!selectedPropertyImageFiles.length && !selectedPropertyDocumentFiles.length"
                  @click="uploadPropertyFiles"
                >
                  UPDATE_UPLOADS
                </Button>
              </div>
            </div>

            <div v-else class="pz-operator-form-body">
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
                rows="2"
                placeholder="Lien notes"
              />
              <textarea
                v-model="operatorForm.ownership_profile.disclosure_notes"
                class="pz-input"
                rows="2"
                placeholder="Disclosure notes"
              />
              <textarea
                v-model="operatorForm.featureText"
                class="pz-input"
                rows="2"
                placeholder="Feature highlights, comma separated"
              />
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="pz-editor-actions">
          <div class="pz-editor-actions__summary">
            <span class="pz-editor-status">{{ activeEditorMeta.label }}</span>
            <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ workflowSummary.footer }}</span>
          </div>
          <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
            <Button variant="ghost" size="sm" @click="cancelEdit">Cancel</Button>
            <Button variant="outline" size="sm" :loading="saving" @click="saveProperty({ stayOnPage: true })">
              Save &amp; Continue
            </Button>
            <Button variant="primary" size="sm" :loading="saving" :disabled="!canPublishProperty" @click="saveProperty()">
              Save &amp; Exit
            </Button>
          </div>
        </div>
        <div class="pz-mobile-sticky-actions">
          <span>{{ offlineDraftMessage }}</span>
          <Button variant="primary" size="sm" :loading="saving" :disabled="!canPublishProperty" @click="saveProperty()">
            Save
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Button from '../components/ui/Button.vue';
import PzInput from '../components/PzInput.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const configStore = useConfigStore();
const showAlert = inject('showAlert');

const property = ref(null);
const loading = ref(true);
const saving = ref(false);
const uploadingMedia = ref(false);
const activeEditorSection = ref('listing');
const propertyImageInput = ref(null);
const propertyCameraInput = ref(null);
const propertyDocumentInput = ref(null);
const selectedPropertyImageFiles = ref([]);
const selectedPropertyImagePreviews = ref([]);
const selectedPropertyDocumentFiles = ref([]);
const selectedPropertyDocumentCategories = ref([]);
const propertyUploadDocumentType = ref('DOCUMENT');
const draftSavedAt = ref(null);
const draftRestored = ref(false);
const defaultCurrencyCode = computed(() => configStore.activeCurrencyCode || 'KES');
const operatorForm = ref(createDefaultOperatorForm());
const propertyDraftStorageKey = computed(() => `pz-property-edit-draft:${route.params.id}`);
const isOnline = ref(typeof navigator === 'undefined' ? true : navigator.onLine);
const offlineDraftMessage = computed(() => (isOnline.value ? 'Draft autosaved locally' : 'Saved locally - will sync when online'));

const mediaBaseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/api\/?$/, '');
function resolveMediaUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  return `${mediaBaseUrl}${url}`;
}

const editorSectionIcons = {
  listing: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
  specification: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 6H3"/><path d="M10 12H3"/><path d="M10 18H3"/><path d="M14 9h.01"/><path d="M18 9h.01"/><path d="M14 15h.01"/><path d="M18 15h.01"/></svg>',
  commercial: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
  readiness: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
  media: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>',
  ownership: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
};

const editorSections = [
  { id: 'listing', kicker: '01', label: 'Listing Basics', description: 'Identity, status, and visibility controls.' },
  { id: 'specification', kicker: '02', label: 'Specification', description: 'Beds, area, fit-out, and occupancy data.' },
  { id: 'commercial', kicker: '03', label: 'Commercials', description: 'Pricing, deposit, and finance posture.' },
  { id: 'readiness', kicker: '04', label: 'Readiness', description: 'Development stage, utilities, and delivery context.' },
  { id: 'media', kicker: '05', label: 'Media & Documents', description: 'Images, floor plans, and property files.' },
  { id: 'ownership', kicker: '06', label: 'Ownership', description: 'Title references, disclosures, and highlights.' },
];

const activeEditorMeta = computed(() =>
  editorSections.find((section) => section.id === activeEditorSection.value) || editorSections[0]
);

function getDraftSnapshot() {
  return {
    activeEditorSection: activeEditorSection.value,
    operatorForm: operatorForm.value,
  };
}

function restoreDraftSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== 'object') return;
  if (snapshot.activeEditorSection && editorSections.some((section) => section.id === snapshot.activeEditorSection)) {
    activeEditorSection.value = snapshot.activeEditorSection;
  }
  if (snapshot.operatorForm && typeof snapshot.operatorForm === 'object') {
    operatorForm.value = {
      ...operatorForm.value,
      ...snapshot.operatorForm,
      specification: {
        ...operatorForm.value.specification,
        ...(snapshot.operatorForm.specification || {}),
      },
      development_metadata: {
        ...operatorForm.value.development_metadata,
        ...(snapshot.operatorForm.development_metadata || {}),
      },
      pricing_profile: {
        ...operatorForm.value.pricing_profile,
        ...(snapshot.operatorForm.pricing_profile || {}),
      },
      ownership_profile: {
        ...operatorForm.value.ownership_profile,
        ...(snapshot.operatorForm.ownership_profile || {}),
      },
    };
  }
}

function loadStoredDraft() {
  if (typeof window === 'undefined') return null;
  try {
    const stored = window.localStorage.getItem(propertyDraftStorageKey.value);
    return stored ? JSON.parse(stored) : null;
  } catch (error) {
    console.error('Failed to load property edit draft', error);
    return null;
  }
}

function saveStoredDraft() {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(propertyDraftStorageKey.value, JSON.stringify(getDraftSnapshot()));
    draftSavedAt.value = new Date().toISOString();
  } catch (error) {
    console.error('Failed to save property edit draft', error);
  }
}

function clearStoredDraft() {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.removeItem(propertyDraftStorageKey.value);
  } catch (error) {
    console.error('Failed to clear property edit draft', error);
  }
}

function sectionNeedsAttention(sectionId) {
  switch (sectionId) {
    case 'listing':
      return {
        complete: Boolean(
          operatorForm.value.title?.trim() &&
          (operatorForm.value.location_text?.trim() || operatorForm.value.formatted_address?.trim()) &&
          numberOrNull(operatorForm.value.price_estimate) !== null
        ),
        missing: [
          !operatorForm.value.title?.trim() ? 'Title' : null,
          !(operatorForm.value.location_text?.trim() || operatorForm.value.formatted_address?.trim()) ? 'Location' : null,
          numberOrNull(operatorForm.value.price_estimate) === null ? 'Value' : null,
        ].filter(Boolean),
      };
    case 'specification':
      return {
        complete: Boolean(
          operatorForm.value.specification.bedrooms ||
          operatorForm.value.specification.bathrooms ||
          operatorForm.value.specification.internal_area ||
          operatorForm.value.specification.lot_size
        ),
        missing: [
          !operatorForm.value.specification.bedrooms ? 'Bedrooms' : null,
          !operatorForm.value.specification.bathrooms ? 'Bathrooms' : null,
          !operatorForm.value.specification.internal_area ? 'Area' : null,
        ].filter(Boolean),
      };
    case 'commercial':
      return {
        complete: Boolean(
          numberOrNull(operatorForm.value.pricing_profile.asking_price) !== null ||
          numberOrNull(operatorForm.value.pricing_profile.rent_amount) !== null
        ),
        missing: [
          numberOrNull(operatorForm.value.pricing_profile.asking_price) === null &&
          numberOrNull(operatorForm.value.pricing_profile.rent_amount) === null
            ? 'Price'
            : null,
          !operatorForm.value.pricing_profile.currency ? 'Currency' : null,
        ].filter(Boolean),
      };
    case 'readiness':
      return {
        complete: Boolean(operatorForm.value.development_metadata.development_stage || operatorForm.value.development_metadata.build_ready),
        missing: [
          !operatorForm.value.development_metadata.development_stage ? 'Stage' : null,
          !operatorForm.value.development_metadata.zoning_info?.trim() ? 'Zoning' : null,
        ].filter(Boolean),
      };
    case 'media':
      return {
        complete: Boolean(property.value?.media_assets?.length || selectedPropertyImageFiles.value.length || selectedPropertyDocumentFiles.value.length),
        missing: [
          !property.value?.media_assets?.length && !selectedPropertyImageFiles.value.length ? 'Images' : null,
          !property.value?.media_assets?.length && !selectedPropertyDocumentFiles.value.length ? 'Documents' : null,
        ].filter(Boolean),
      };
    case 'ownership':
      return {
        complete: Boolean(
          operatorForm.value.ownership_profile.legal_owner_name?.trim() ||
          operatorForm.value.ownership_profile.title_reference?.trim()
        ),
        missing: [
          !operatorForm.value.ownership_profile.legal_owner_name?.trim() ? 'Owner' : null,
          !operatorForm.value.ownership_profile.title_reference?.trim() ? 'Title ref' : null,
        ].filter(Boolean),
      };
    default:
      return { complete: false, missing: [] };
  }
}

const workflowSections = computed(() =>
  editorSections.map((section) => ({
    ...section,
    ...sectionNeedsAttention(section.id),
    active: activeEditorSection.value === section.id,
  }))
);

const workflowCompletion = computed(() => {
  const completeCount = workflowSections.value.filter((section) => section.complete).length;
  const nextMissing = workflowSections.value.find((section) => !section.complete) || workflowSections.value[0];
  return {
    completeCount,
    totalCount: workflowSections.value.length,
    percent: Math.round((completeCount / workflowSections.value.length) * 100),
    nextSectionId: nextMissing?.id || 'listing',
    nextLabel: nextMissing?.label || 'Listing Basics',
    blockers: workflowSections.value
      .filter((section) => !section.complete)
      .flatMap((section) => section.missing.slice(0, 2).map((item) => `${section.label}: ${item}`))
      .slice(0, 4),
  };
});

function goToSection(sectionId) {
  if (!canAdvanceToSection(sectionId)) {
    const blocker = workflowSections.value.find((section) => !section.complete);
    showAlert?.(`Complete ${blocker?.label || 'the current section'} before moving forward.`, 'warning');
    return;
  }
  activeEditorSection.value = sectionId;
}

function goToNextSection() {
  goToSection(workflowCompletion.value.nextSectionId);
}

const workflowSummary = computed(() => {
  if (!property.value) {
    return {
      stage: 'LOADING',
      title: 'Preparing property editor',
      body: 'Loading the listing so you can review and update it in one place.',
      footer: 'Save becomes available once the listing data is loaded.',
      primaryAction: null,
      secondaryAction: null,
    };
  }

  const nextSection = workflowCompletion.value.nextSectionId;
  const nextLabel = workflowCompletion.value.nextLabel;
  const nextHelp =
    nextSection === 'listing'
      ? 'Complete the identity, location, and value fields so the listing can be understood quickly.'
      : nextSection === 'specification'
        ? 'Add the property facts buyers compare first.'
        : nextSection === 'commercial'
          ? 'Confirm price, currency, and deposit terms.'
          : nextSection === 'media'
            ? 'Add images and documents so the asset can be reviewed without guessing.'
            : 'Complete ownership details so the record is ready for approval and handoff.';

  return {
    stage: `${property.value.status || 'DRAFT'} • ${workflowCompletion.value.completeCount}/${workflowCompletion.value.totalCount} sections ready`,
    title:
      nextSection === 'listing'
        ? 'Finish the core listing details'
        : nextSection === 'specification'
          ? 'Add the property facts'
          : nextSection === 'commercial'
            ? 'Confirm the commercial terms'
            : nextSection === 'media'
              ? 'Attach the supporting media'
              : 'Confirm ownership and disclosure',
    body: `${nextHelp} You are editing the live listing, so each completed section reduces the chance of missed approvals or follow-up questions.`,
    footer: workflowCompletion.value.blockers.length
      ? `Still missing: ${workflowCompletion.value.blockers.join(' • ')}`
      : 'All core sections are complete. Save and exit when you are finished.',
    primaryAction: { label: `Open ${nextLabel}`, handler: () => goToSection(nextSection) },
    secondaryAction: { label: 'Save Draft', handler: () => saveProperty({ stayOnPage: true }) },
  };
});

const canModifyProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  if (authStore.isAdmin) return true;
  if (authStore.user.id === property.value.owner) return true;
  if (authStore.user.id === property.value.manager) return true;
  if (authStore.hasPermission('property:update_property')) return true;
  return false;
});

const canPublishProperty = computed(() => {
  const listingReady = sectionNeedsAttention('listing').complete;
  const commercialReady = sectionNeedsAttention('commercial').complete;
  if (operatorForm.value.status === 'ACTIVE' || operatorForm.value.status === 'PENDING_REVIEW') {
    return listingReady && commercialReady;
  }
  return listingReady;
});

const mapPinStyle = computed(() => {
  const lat = Number(operatorForm.value.latitude || 0);
  const lng = Number(operatorForm.value.longitude || 0);
  return {
    left: `${Math.min(92, Math.max(8, ((lng + 180) / 360) * 100))}%`,
    top: `${Math.min(92, Math.max(8, ((90 - lat) / 180) * 100))}%`,
  };
});

function canAdvanceToSection(sectionId) {
  const index = editorSections.findIndex((section) => section.id === sectionId);
  if (index <= 0) return true;
  const previousSections = editorSections.slice(0, index);
  return previousSections.every((section) => sectionNeedsAttention(section.id).complete);
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
    latitude: '',
    longitude: '',
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
      currency: defaultCurrencyCode.value,
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
    latitude: source?.latitude ?? '',
    longitude: source?.longitude ?? '',
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
      currency: pricing.currency || defaultCurrencyCode.value,
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
    latitude: numberOrNull(operatorForm.value.latitude),
    longitude: numberOrNull(operatorForm.value.longitude),
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

async function loadProperty() {
  loading.value = true;
  try {
    const res = await api.get(`/property/${route.params.id}/`);
    property.value = res.data;
    hydrateOperatorForm(res.data);
    const storedDraft = loadStoredDraft();
    if (storedDraft) {
      restoreDraftSnapshot(storedDraft);
      draftRestored.value = true;
    } else {
      draftRestored.value = false;
    }
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property.', 'error');
  } finally {
    loading.value = false;
  }
}

async function saveProperty(options = {}) {
  if (!canModifyProperty.value) return;
  saving.value = true;
  try {
    await api.patch(`/property/${route.params.id}/`, buildPropertyPayload());
    clearStoredDraft();
    draftSavedAt.value = null;
    showAlert?.('Property updated successfully.', 'success');
    if (options.stayOnPage) {
      draftRestored.value = false;
      await loadProperty();
      goToSection(workflowCompletion.value.nextSectionId);
      return;
    }
    router.push(`/properties/${route.params.id}`);
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to update property.', 'error');
  } finally {
    saving.value = false;
  }
}

function triggerPropertyImageUpload() {
  propertyImageInput.value?.click();
}

function triggerPropertyCameraUpload() {
  propertyCameraInput.value?.click();
}

function triggerPropertyDocumentUpload() {
  propertyDocumentInput.value?.click();
}

function handlePropertyImagesSelected(event) {
  selectedPropertyImageFiles.value = Array.from(event.target.files || []);
  selectedPropertyImagePreviews.value.forEach((url) => URL.revokeObjectURL(url));
  selectedPropertyImagePreviews.value = selectedPropertyImageFiles.value.map((file) => URL.createObjectURL(file));
}

function handlePropertyDocumentsSelected(event) {
  selectedPropertyDocumentFiles.value = Array.from(event.target.files || []);
  selectedPropertyDocumentCategories.value = selectedPropertyDocumentFiles.value.map(() => propertyUploadDocumentType.value === 'FLOOR_PLAN' ? 'FLOOR_PLAN' : 'GENERAL');
}

function clearSelectedPropertyImages() {
  selectedPropertyImagePreviews.value.forEach((url) => URL.revokeObjectURL(url));
  selectedPropertyImageFiles.value = [];
  selectedPropertyImagePreviews.value = [];
  if (propertyImageInput.value) propertyImageInput.value.value = '';
}

function clearSelectedPropertyDocuments() {
  selectedPropertyDocumentFiles.value = [];
  selectedPropertyDocumentCategories.value = [];
  if (propertyDocumentInput.value) propertyDocumentInput.value.value = '';
}

function setApproximateLocation(event) {
  const rect = event.currentTarget.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width;
  const y = (event.clientY - rect.top) / rect.height;
  operatorForm.value.longitude = Number((x * 360 - 180).toFixed(6));
  operatorForm.value.latitude = Number((90 - y * 180).toFixed(6));
}

async function uploadPropertyFiles() {
  if (!property.value?.id) return;
  uploadingMedia.value = true;
  try {
    if (selectedPropertyImageFiles.value.length) {
      const imageData = new FormData();
      imageData.append('media_type', 'IMAGE');
      selectedPropertyImageFiles.value.forEach((file) => imageData.append('files', file));
      await api.post(`/property/${property.value.id}/upload-media/`, imageData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    }

    if (selectedPropertyDocumentFiles.value.length) {
      const documentData = new FormData();
      documentData.append('media_type', propertyUploadDocumentType.value);
      selectedPropertyDocumentFiles.value.forEach((file, idx) => {
        documentData.append('files', file);
        documentData.append(`document_category_${idx}`, selectedPropertyDocumentCategories.value[idx] || 'GENERAL');
      });
      await api.post(`/property/${property.value.id}/upload-media/`, documentData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    }

    clearSelectedPropertyImages();
    clearSelectedPropertyDocuments();
    await loadProperty();
    showAlert?.('Property media updated successfully.', 'success');
  } catch (error) {
    showAlert?.(error.response?.data?.error || error.response?.data?.detail || 'Failed to upload property media.', 'error');
  } finally {
    uploadingMedia.value = false;
  }
}

function cancelEdit() {
  router.push(`/properties/${route.params.id}`);
}

let draftSaveTimer = null;
watch(
  [operatorForm, activeEditorSection],
  () => {
    if (loading.value || !property.value || saving.value || uploadingMedia.value) return;
    if (draftSaveTimer) window.clearTimeout(draftSaveTimer);
    draftSaveTimer = window.setTimeout(() => {
      saveStoredDraft();
    }, 300);
  },
  { deep: true }
);

onMounted(() => {
  window.addEventListener('online', () => { isOnline.value = true; });
  window.addEventListener('offline', () => { isOnline.value = false; });
  loadProperty();
});

onUnmounted(() => {
  if (draftSaveTimer) window.clearTimeout(draftSaveTimer);
});
</script>

<style scoped>
.pz-edit-page {
  background-color: var(--pz-color-limestone-white);
  min-height: 100vh;
}

.pz-edit-layout {
  display: grid;
  gap: 1.5rem;
}

.pz-edit-header {
  display: grid;
  gap: 0.5rem;
}

.pz-edit-header__title {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.pz-edit-header__title h1 {
  font-size: 1.75rem;
  line-height: 1.2;
  margin: 0;
}

.pz-edit-header__subtitle {
  font-size: 1rem;
  color: var(--pz-color-concrete-grey);
  margin: 0;
}

.pz-edit-workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.pz-edit-workflow-banner__summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.pz-edit-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-edit-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.pz-edit-workflow-banner__body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.pz-edit-workflow-banner__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 0.25rem;
}

.pz-edit-workflow-banner__meta-item {
  display: inline-flex;
  align-items: center;
  min-height: 1.8rem;
  padding: 0 0.65rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.92);
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

.pz-edit-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.pz-edit-workflow-blockers {
  display: grid;
  gap: 0.55rem;
  margin-top: 1rem;
  padding: 0.85rem 0.95rem;
  border: 1px solid rgba(212, 101, 42, 0.18);
  background: rgba(247, 244, 239, 0.7);
}

.pz-edit-workflow-blockers__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-edit-workflow-blockers__list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.pz-edit-workflow-blockers__item {
  display: inline-flex;
  align-items: center;
  min-height: 1.8rem;
  padding: 0 0.65rem;
  border: 1px solid rgba(212, 101, 42, 0.16);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

.pz-edit-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.pz-edit-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

.pz-edit-workflow-step__index {
  display: inline-flex;
  width: 1.9rem;
  height: 1.9rem;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(247, 244, 239, 0.95);
  border: 1px solid rgba(10, 10, 15, 0.12);
  color: var(--pz-color-foundation-black);
  flex-shrink: 0;
}

.pz-edit-workflow-step__content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.pz-edit-workflow-step__title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.pz-edit-workflow-step__content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.pz-edit-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pz-edit-workflow-step__state,
.pz-editor-nav__state {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-edit-workflow-step__state {
  white-space: nowrap;
}

.pz-edit-workflow-step--active .pz-edit-workflow-step__state,
.pz-editor-nav__state.is-done {
  color: var(--pz-color-earth-orange);
}

.pz-edit-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.pz-edit-workflow-step--done .pz-edit-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.pz-edit-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-edit-workflow-step--locked,
.pz-editor-nav__item.is-locked {
  opacity: 0.58;
  cursor: not-allowed;
}

.pz-map-picker {
  display: grid;
  gap: 0.8rem;
  padding: 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.72);
  border-radius: 8px;
}

.pz-map-picker > div {
  display: grid;
  gap: 0.25rem;
}

.pz-map-picker span,
.pz-document-category-row span,
.pz-mobile-sticky-actions span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
}

.pz-map-picker__pad {
  position: relative;
  min-height: 13rem;
  border: 1px solid rgba(10, 10, 15, 0.1);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(10, 10, 15, 0.05) 1px, transparent 1px),
    linear-gradient(rgba(10, 10, 15, 0.05) 1px, transparent 1px),
    rgba(255, 255, 255, 0.88);
  background-size: 20% 20%;
}

.pz-map-picker__pin {
  position: absolute;
  width: 1rem;
  height: 1rem;
  transform: translate(-50%, -50%);
  border-radius: 50% 50% 50% 0;
  rotate: -45deg;
  background: var(--pz-color-earth-orange);
  box-shadow: 0 0 0 0.35rem rgba(212, 101, 42, 0.16);
}

.pz-document-category-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(9rem, 12rem);
  gap: 0.65rem;
  align-items: center;
}

.pz-mobile-sticky-actions {
  display: none;
}

/* Breadcrumbs */
.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
}
.pz-breadcrumb__item {
  color: var(--pz-color-concrete-grey);
  text-decoration: none;
  transition: color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.pz-breadcrumb__item:hover {
  color: var(--pz-color-earth-orange);
}
.pz-breadcrumb__separator {
  color: rgba(10, 10, 15, 0.15);
  font-size: 0.65rem;
}
.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-weight: 500;
}

/* Editor Shell */
.pz-editor-shell {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: minmax(13rem, 16rem) minmax(0, 1fr);
}

.pz-editor-nav {
  display: grid;
  gap: 0.4rem;
  align-content: start;
}

.pz-editor-nav__item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 0.75rem;
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 12px;
  background: white;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}
.pz-editor-nav__item:hover {
  border-color: rgba(212, 101, 42, 0.2);
}
.pz-editor-nav__item.is-active {
  background: white;
  border-color: rgba(212, 101, 42, 0.35);
  box-shadow: 0 4px 12px rgba(10, 10, 15, 0.06);
}

.pz-editor-nav__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 8px;
  background: rgba(212, 101, 42, 0.08);
  color: var(--pz-color-earth-orange);
  flex-shrink: 0;
}
.pz-editor-nav__icon svg {
  width: 0.9rem;
  height: 0.9rem;
}
.pz-editor-nav__item.is-active .pz-editor-nav__icon {
  background: rgba(212, 101, 42, 0.14);
}

.pz-editor-nav__text {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
  min-width: 0;
}
.pz-editor-nav__text strong {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}
.pz-editor-nav__text span {
  font-size: 0.7rem;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pz-editor-nav__state {
  display: block;
  line-height: 1.2;
}

/* Form Section */
.pz-operator-form-section {
  display: grid;
  gap: 0.75rem;
  padding: 0.875rem;
  border: 1px solid rgba(10, 10, 15, 0.06);
  background: white;
  border-radius: 14px;
}

.pz-operator-form-header {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}
.pz-operator-form__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}
.pz-operator-form-header strong {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}
.pz-operator-form__desc {
  font-size: 0.75rem;
  color: var(--pz-color-concrete-grey);
}

.pz-operator-form-body {
  display: grid;
  gap: 0.6rem;
}

.pz-existing-assets,
.pz-upload-card {
  display: grid;
  gap: 0.75rem;
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
  border: 1px dashed rgba(10, 10, 15, 0.16);
  background: rgba(255, 255, 255, 0.96);
  border-radius: 12px;
}

.pz-upload-selection {
  font-size: 0.8rem;
  color: var(--pz-color-earth-orange);
}

.pz-operator-form-grid {
  display: grid;
  gap: 0.6rem;
  grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
}

.pz-operator-toggle-grid {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
}

.pz-checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 2.4rem;
  padding: 0 0.65rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 10px;
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

/* Actions */
.pz-editor-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.06);
  background: white;
  border-radius: 12px;
}

.pz-editor-actions__summary {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.pz-editor-status {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

@media (max-width: 1024px) {
  .pz-editor-shell {
    grid-template-columns: 1fr;
  }

  .pz-edit-workflow-banner {
    grid-template-columns: 1fr;
  }

  .pz-edit-workflow-banner__actions {
    justify-content: flex-start;
  }

  .pz-edit-workflow-banner__steps {
    grid-template-columns: 1fr;
  }

  .pz-editor-actions {
    padding-bottom: 4.5rem;
  }

  .pz-mobile-sticky-actions {
    position: sticky;
    bottom: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.75rem;
    border: 1px solid rgba(10, 10, 15, 0.08);
    border-radius: 8px 8px 0 0;
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 -8px 24px rgba(10, 10, 15, 0.08);
  }

  .pz-document-category-row {
    grid-template-columns: 1fr;
  }
}

.pz-existing-assets__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.pz-existing-asset {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.pz-existing-asset__thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-existing-asset__doc {
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  border-radius: 8px;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: #f8f9fb;
  padding: 0.5rem;
  text-align: center;
}

.pz-existing-asset__doc-icon {
  font-size: 1.25rem;
}

.pz-existing-asset__doc-name {
  font-size: 0.65rem;
  color: var(--pz-color-structural-steel);
  word-break: break-word;
}

.pz-existing-asset__meta {
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--pz-color-concrete-grey);
  text-align: center;
}

.pz-upload-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.pz-upload-preview-thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(10, 10, 15, 0.1);
}
</style>
