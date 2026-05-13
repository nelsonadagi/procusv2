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

        <!-- Editor -->
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
              <span class="pz-editor-nav__icon" v-html="editorSectionIcons[section.id]"></span>
              <div class="pz-editor-nav__text">
                <strong>{{ section.label }}</strong>
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
            <span class="pz-u-text-mono text-xs pz-u-color-steel">Changes save to the live listing.</span>
          </div>
          <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
            <Button variant="ghost" size="sm" @click="cancelEdit">Cancel</Button>
            <Button variant="primary" size="sm" :loading="saving" @click="saveProperty">
              Save Changes
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
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
const activeEditorSection = ref('listing');
const defaultCurrencyCode = computed(() => configStore.activeCurrencyCode || 'KES');
const operatorForm = ref(createDefaultOperatorForm());

const editorSectionIcons = {
  listing: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
  specification: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 6H3"/><path d="M10 12H3"/><path d="M10 18H3"/><path d="M14 9h.01"/><path d="M18 9h.01"/><path d="M14 15h.01"/><path d="M18 15h.01"/></svg>',
  commercial: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
  readiness: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
  ownership: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
};

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

const canModifyProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  if (authStore.isAdmin) return true;
  if (authStore.user.id === property.value.owner) return true;
  if (authStore.user.id === property.value.manager) return true;
  if (authStore.hasPermission('property:update_property')) return true;
  return false;
});

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
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property.', 'error');
  } finally {
    loading.value = false;
  }
}

async function saveProperty() {
  if (!canModifyProperty.value) return;
  saving.value = true;
  try {
    await api.patch(`/property/${route.params.id}/`, buildPropertyPayload());
    showAlert?.('Property updated successfully.', 'success');
    router.push(`/properties/${route.params.id}`);
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to update property.', 'error');
  } finally {
    saving.value = false;
  }
}

function cancelEdit() {
  router.push(`/properties/${route.params.id}`);
}

onMounted(() => {
  loadProperty();
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
}
</style>
