<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="earth"
    :title="dashboardTitle"
    :eyebrow="dashboardEyebrow"
    signal-text="PROPERTY GRID ONLINE"
    workspace-label="Operations"
    :sidebar-groups="navGroups"
    :quickstats="quickstats"
  >
    <template #headerActions>
      <Button v-if="canCreateListing" variant="primary" size="sm" @click="openPropertyModal">New Listing</Button>
      <Button v-if="canManageAppointments" variant="outline" size="sm" @click="openAvailabilityModal">Publish Availability</Button>
      <Button variant="ghost" size="sm" @click="loadDashboard">Refresh</Button>
    </template>

    <div v-if="activeSection === 'listings'" class="pz-manager-layout">
      <Card title="Listing Operations" class="u-xl-col-span-2">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Create structured property listings in a focused modal flow instead of inline page editing.</p>
          <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
            <Button type="button" variant="primary" @click="openPropertyModal">Create Listing</Button>
            <Button type="button" variant="outline" @click="openAvailabilityModal">Publish Availability</Button>
          </div>
        </div>
      </Card>

      <Card title="Availability">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Manage visitor booking windows in a modal so the live inventory grid stays visible.</p>
          <Button type="button" variant="outline" fullWidth @click="openAvailabilityModal">Open Availability Publisher</Button>
        </div>
      </Card>

      <Card title="Managed Properties" class="u-xl-col-span-3">
        <div v-if="properties.length" class="pz-manager-list">
          <div class="pz-manager-list__header">
            <span>Listing</span>
            <span>Availability</span>
            <span>Commercial</span>
            <span class="u-text-right">Action</span>
          </div>
          <router-link
            v-for="item in properties"
            :key="item.id"
            :to="`/properties/${item.id}`"
            class="pz-manager-list__row"
          >
            <div class="pz-manager-list__primary">
              <div class="pz-u-text-display text-sm">{{ item.title }}</div>
              <div class="pz-u-text-mono text-xs pz-u-color-steel">
                {{ item.asset_type }} // {{ item.location_display || 'Location pending' }}
              </div>
            </div>
            <div class="pz-manager-list__meta">
              <span class="pz-manager-pill">{{ item.appointment_enabled ? 'Appointments On' : 'Appointments Off' }}</span>
              <span class="pz-manager-pill">{{ item.inquiry_enabled ? 'Inquiries On' : 'Inquiries Off' }}</span>
            </div>
            <div class="pz-manager-list__commercial">
              <strong>{{ configStore.formatPrice(item.pricing_profile?.asking_price || item.price_estimate, item.pricing_profile?.currency || item.country?.default_currency || configStore.activeCurrencyCode) }}</strong>
              <span class="pz-u-text-mono text-xs pz-u-color-earth">{{ item.status }}</span>
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">
                {{ item.specification?.bedrooms || 0 }} bed / {{ item.specification?.bathrooms || 0 }} bath / {{ item.development_metadata?.development_stage || 'No stage' }}
              </span>
            </div>
            <div class="pz-manager-list__action">
              <span class="pz-manager-link">Open Listing ↳</span>
            </div>
          </router-link>
        </div>
        <EmptyState
          v-else
          icon="🏠"
          title="No properties yet"
          description="Create your first listing to start managing properties."
          action-label="Create Listing"
          action-variant="primary"
          @action="openPropertyModal"
        />
      </Card>
    </div>

    <div v-else-if="activeSection === 'availability'" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-8">
      <Card title="Publish Availability">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Open the availability modal to publish new slots without losing context.</p>
          <Button type="button" variant="primary" fullWidth @click="openAvailabilityModal">Publish Slots</Button>
        </div>
      </Card>

      <Card title="Current Appointments">
        <EmptyState
          v-if="!appointments.length"
          icon="🗓"
          title="No appointments yet"
          description="Published slots and visitor bookings will appear here."
        />
        <div v-else class="pz-space-y-3">
          <div v-for="appt in appointments.slice(0, 6)" :key="appt.id" class="pz-manager-feed">
            <strong>{{ appt.property_title }}</strong>
            <span>{{ formatDateTime(appt.scheduled_start) }}</span>
          </div>
        </div>
      </Card>
    </div>

    <div v-else-if="activeSection === 'leads'">
      <Card title="Incoming Leads">
        <div v-if="inquiries.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--lg-cols-3 pz-l-grid--gap-4">
          <div v-for="inquiry in inquiries" :key="inquiry.id" class="pz-manager-feed">
            <strong>{{ inquiry.full_name }}</strong>
            <span>{{ inquiry.property_title }}</span>
            <span class="pz-u-text-mono text-xs pz-u-color-earth">{{ inquiry.inquiry_type }}</span>
          </div>
        </div>
        <EmptyState
          v-else
          icon="📭"
          title="No inquiries yet"
          description="Leads will appear here when prospects express interest in your listings."
        />
      </Card>
    </div>

    <div v-else-if="activeSection === 'appointments'">
      <Card title="Appointments">
        <div v-if="appointments.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
          <div v-for="appointment in appointments" :key="appointment.id" class="pz-manager-feed">
            <strong>{{ appointment.full_name }}</strong>
            <span>{{ appointment.property_title }}</span>
            <span>{{ formatDateTime(appointment.scheduled_start) }}</span>
          </div>
        </div>
        <EmptyState
          v-else
          icon="🗓"
          title="No appointments scheduled"
          description="Appointments will appear here once prospects book available slots."
        />
      </Card>
    </div>

    <Modal :isOpen="showPropertyModal" title="PUBLISH_PROPERTY_LISTING" size="xl" @close="closePropertyModal">
      <form id="property-form" class="pz-space-y-6" @submit.prevent="createProperty">
        <div class="pz-manager-form-grid">
          <PzInput v-model="propertyForm.title" label="Title" required />
          <PzInput v-model="propertyForm.location_text" label="Searchable Location" />
          <select v-model="propertyForm.asset_type" class="pz-input">
            <option value="LAND">Land</option>
            <option value="RESIDENTIAL">Residential</option>
            <option value="COMMERCIAL">Commercial</option>
            <option value="INDUSTRIAL">Industrial</option>
            <option value="MIXED_USE">Mixed Use</option>
            <option value="HOSPITALITY">Hospitality</option>
            <option value="RENOVATION">Renovation</option>
            <option value="SPECIAL_PURPOSE">Special Purpose</option>
          </select>
          <select v-model="propertyForm.listing_type" class="pz-input">
            <option value="SALE">Sale</option>
            <option value="LEASE">Lease</option>
            <option value="DEVELOPMENT_OPPORTUNITY">Development Opportunity</option>
            <option value="COMPLETED_PROJECT">Completed Project</option>
          </select>
          <PzInput v-model="propertyForm.price_estimate" label="Estimated Value" type="number" required />
          <PzInput v-model="propertyForm.formatted_address" label="Formatted Address" />
        </div>

        <textarea
          v-model="propertyForm.description"
          class="pz-input"
          rows="4"
          placeholder="Describe the property, commercial positioning, and operating context"
        />

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Specifications</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Capture the facts users will compare quickly.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="specificationForm.bedrooms" label="Bedrooms" type="number" />
            <PzInput v-model="specificationForm.bathrooms" label="Bathrooms" type="number" />
            <PzInput v-model="specificationForm.parking_spaces" label="Parking Spaces" type="number" />
            <PzInput v-model="specificationForm.floors" label="Floors" type="number" />
            <PzInput v-model="specificationForm.internal_area" label="Internal Area" type="number" />
            <select v-model="specificationForm.internal_area_unit" class="pz-input">
              <option value="SQM">Square Meters</option>
              <option value="SQFT">Square Feet</option>
              <option value="ACRE">Acre</option>
              <option value="HECTARE">Hectare</option>
            </select>
            <PzInput v-model="specificationForm.lot_size" label="Lot Size" type="number" />
            <select v-model="specificationForm.lot_size_unit" class="pz-input">
              <option value="SQM">Square Meters</option>
              <option value="SQFT">Square Feet</option>
              <option value="ACRE">Acre</option>
              <option value="HECTARE">Hectare</option>
            </select>
            <select v-model="specificationForm.condition_rating" class="pz-input">
              <option value="">Condition Rating</option>
              <option value="SHELL">Shell</option>
              <option value="FAIR">Fair</option>
              <option value="GOOD">Good</option>
              <option value="EXCELLENT">Excellent</option>
            </select>
            <select v-model="specificationForm.occupancy_status" class="pz-input">
              <option value="">Occupancy Status</option>
              <option value="VACANT">Vacant</option>
              <option value="OCCUPIED">Occupied</option>
              <option value="OWNER_OCCUPIED">Owner Occupied</option>
              <option value="TENANTED">Tenanted</option>
              <option value="UNDER_CONSTRUCTION">Under Construction</option>
            </select>
          </div>
        </div>

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Pricing And Finance</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Expose commercial terms and financing posture.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="pricingForm.asking_price" label="Asking Price" type="number" />
            <PzInput v-model="pricingForm.rent_amount" label="Rent Amount" type="number" />
            <select v-model="pricingForm.currency" class="pz-input">
              <option v-for="currency in configStore.availableCurrencies" :key="currency.currency_code" :value="currency.currency_code">
                {{ currency.currency_code }}{{ currency.symbol ? ` (${currency.symbol})` : '' }}
              </option>
            </select>
            <select v-model="pricingForm.pricing_strategy" class="pz-input">
              <option value="FIXED">Fixed</option>
              <option value="NEGOTIABLE">Negotiable</option>
              <option value="PRICE_ON_APPLICATION">Price On Application</option>
              <option value="PER_UNIT">Per Unit</option>
            </select>
            <PzInput v-model="pricingForm.deposit_amount" label="Deposit Amount" type="number" />
            <label class="pz-checkbox-row">
              <input v-model="pricingForm.requires_deposit" type="checkbox" />
              <span>Requires deposit</span>
            </label>
            <label class="pz-checkbox-row">
              <input v-model="propertyForm.financing_allowed" type="checkbox" />
              <span>Financing allowed</span>
            </label>
            <label class="pz-checkbox-row">
              <input v-model="propertyForm.appointment_enabled" type="checkbox" />
              <span>Appointments enabled</span>
            </label>
          </div>
        </div>

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Development And Media</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Publish due-diligence context and visual assets.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="developmentForm.zoning_info" label="Zoning" />
            <select v-model="developmentForm.development_stage" class="pz-input">
              <option value="">Development Stage</option>
              <option value="RAW_LAND">Raw Land</option>
              <option value="SERVICED_SITE">Serviced Site</option>
              <option value="IN_DESIGN">In Design</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
            </select>
            <PzInput v-model="developmentForm.recommended_use" label="Recommended Use" />
            <PzInput v-model="developmentForm.utilities_text" label="Utilities" placeholder="Water, Power, Fiber" />
            <PzInput v-model="mediaForm.primary_image_url" label="Primary Image URL" />
            <PzInput v-model="mediaForm.virtual_tour_url" label="Virtual Tour URL" />
            <label class="pz-checkbox-row">
              <input v-model="developmentForm.build_ready" type="checkbox" />
              <span>Build ready</span>
            </label>
          </div>
          <textarea v-model="propertyForm.feature_tags" class="pz-input" rows="3" placeholder="Feature highlights, comma separated" />
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closePropertyModal">Cancel</Button>
        <Button type="submit" form="property-form" variant="primary" :loading="submittingProperty">Publish Listing</Button>
      </template>
    </Modal>

    <Modal :isOpen="showAvailabilityModal" title="PUBLISH_AVAILABILITY_WINDOWS" size="lg" @close="closeAvailabilityModal">
      <form id="availability-form" class="pz-space-y-4" @submit.prevent="createAvailability">
        <select v-model="availabilityForm.property" class="pz-input">
          <option disabled value="">Select property</option>
          <option v-for="item in properties" :key="item.id" :value="item.id">{{ item.title }}</option>
        </select>
        <PzInput v-model="availabilityForm.start_at" label="Start" type="datetime-local" required />
        <PzInput v-model="availabilityForm.end_at" label="End" type="datetime-local" required />
        <PzInput v-model="availabilityForm.slot_duration_minutes" label="Slot Duration (minutes)" type="number" required />
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeAvailabilityModal">Cancel</Button>
        <Button type="submit" form="availability-form" variant="primary" :loading="submittingAvailability">Publish Slots</Button>
      </template>
    </Modal>
  </DashboardShell>
</template>

<script setup>
import { inject, onMounted, ref, computed } from 'vue';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Card from '../components/ui/Card.vue';
import Button from '../components/ui/Button.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import PzInput from '../components/PzInput.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import Modal from '../components/ui/Modal.vue';

const configStore = useConfigStore();
const authStore = useAuthStore();
const showAlert = inject('showAlert');

const activeSection = ref('listings');

const properties = ref([]);
const inquiries = ref([]);
const appointments = ref([]);
const submittingProperty = ref(false);
const submittingAvailability = ref(false);
const showPropertyModal = ref(false);
const showAvailabilityModal = ref(false);

const dashboardProfile = computed(() => {
  if (authStore.hasRole('SURVEYOR')) {
    return {
      title: 'Surveyor Hub',
      eyebrow: 'VALUATION & VERIFICATION',
      canCreateListing: false,
      canManageAppointments: false,
      canVerify: true,
    };
  }
  if (authStore.hasRole('REAL_ESTATE_AGENT')) {
    return {
      title: 'Agent Hub',
      eyebrow: 'SALES & LISTING OPERATIONS',
      canCreateListing: true,
      canManageAppointments: true,
      canVerify: false,
    };
  }
  return {
    title: 'Property Manager Hub',
    eyebrow: 'PROPERTY OPERATIONS',
    canCreateListing: true,
    canManageAppointments: true,
    canVerify: false,
  };
});

const dashboardTitle = computed(() => dashboardProfile.value.title);
const dashboardEyebrow = computed(() => dashboardProfile.value.eyebrow);
const canCreateListing = computed(() => dashboardProfile.value.canCreateListing);
const canManageAppointments = computed(() => dashboardProfile.value.canManageAppointments);
const canVerify = computed(() => dashboardProfile.value.canVerify);

const quickstats = computed(() => [
  { label: 'Listings', value: properties.value.length },
  { label: 'Leads', value: inquiries.value.length },
  { label: 'Appointments', value: appointments.value.length },
]);

const navGroups = computed(() => {
  const items = [
    { id: 'listings', label: 'Listings & Availability', icon: '🏠' },
  ];
  if (canManageAppointments.value) {
    items.push({ id: 'availability', label: 'Availability Windows', icon: '🗓' });
  }
  items.push({ id: 'leads', label: 'Incoming Leads', icon: '📭' });
  if (canManageAppointments.value) {
    items.push({ id: 'appointments', label: 'Appointments', icon: '⏰' });
  }
  if (canVerify.value) {
    items.push({ id: 'verification', label: 'Verification Queue', icon: '✓' });
  }
  return [
    {
      title: 'Property Operations',
      items,
    },
    {
      title: 'System',
      items: [
        { id: 'exit', label: 'Exit Console', icon: '⇚', action: () => { window.location.href = '/'; } },
      ],
    },
  ];
});

const propertyForm = ref({
  title: '',
  description: '',
  asset_type: 'RESIDENTIAL',
  listing_type: 'SALE',
  price_estimate: '',
  location_text: '',
  formatted_address: '',
  financing_allowed: false,
  appointment_enabled: true,
  inquiry_enabled: true,
  manager: '',
  feature_tags: '',
});

const specificationForm = ref({
  bedrooms: '',
  bathrooms: '',
  floors: '',
  parking_spaces: '',
  internal_area: '',
  internal_area_unit: 'SQM',
  lot_size: '',
  lot_size_unit: 'SQM',
  condition_rating: '',
  occupancy_status: '',
});

const pricingForm = ref({
  currency: configStore.activeCurrencyCode || 'KES',
  asking_price: '',
  rent_amount: '',
  pricing_strategy: 'FIXED',
  requires_deposit: false,
  deposit_amount: '',
});

const developmentForm = ref({
  zoning_info: '',
  build_ready: false,
  development_stage: '',
  recommended_use: '',
  utilities_text: '',
});

const mediaForm = ref({
  primary_image_url: '',
  virtual_tour_url: '',
});

const availabilityForm = ref({
  property: '',
  start_at: '',
  end_at: '',
  slot_duration_minutes: 60,
});

function formatDateTime(value) {
  return new Date(value).toLocaleString();
}

function numberOrNull(value) {
  return value === '' || value === null || value === undefined ? null : Number(value);
}

function resetPropertyForm() {
  propertyForm.value = {
    title: '',
    description: '',
    asset_type: 'RESIDENTIAL',
    listing_type: 'SALE',
    price_estimate: '',
    location_text: '',
    formatted_address: '',
    financing_allowed: false,
    appointment_enabled: true,
    inquiry_enabled: true,
    manager: '',
    feature_tags: '',
  };
  specificationForm.value = {
    bedrooms: '',
    bathrooms: '',
    floors: '',
    parking_spaces: '',
    internal_area: '',
    internal_area_unit: 'SQM',
    lot_size: '',
    lot_size_unit: 'SQM',
    condition_rating: '',
    occupancy_status: '',
  };
  pricingForm.value = {
    currency: configStore.activeCurrencyCode || 'KES',
    asking_price: '',
    rent_amount: '',
    pricing_strategy: 'FIXED',
    requires_deposit: false,
    deposit_amount: '',
  };
  developmentForm.value = {
    zoning_info: '',
    build_ready: false,
    development_stage: '',
    recommended_use: '',
    utilities_text: '',
  };
  mediaForm.value = {
    primary_image_url: '',
    virtual_tour_url: '',
  };
}

function resetAvailabilityForm() {
  availabilityForm.value = { property: '', start_at: '', end_at: '', slot_duration_minutes: 60 };
}

function openPropertyModal() {
  showPropertyModal.value = true;
}

function closePropertyModal() {
  showPropertyModal.value = false;
}

function openAvailabilityModal() {
  showAvailabilityModal.value = true;
}

function closeAvailabilityModal() {
  showAvailabilityModal.value = false;
}

async function loadDashboard() {
  try {
    const [propertiesRes, inquiriesRes, appointmentsRes] = await Promise.all([
      api.get('/property/mine/'),
      api.get('/property/inquiries/'),
      api.get('/property/appointments/'),
    ]);
    properties.value = propertiesRes.data.results || propertiesRes.data;
    inquiries.value = inquiriesRes.data.results || inquiriesRes.data;
    appointments.value = appointmentsRes.data.results || appointmentsRes.data;
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property manager dashboard.', 'error');
  }
}

async function createProperty() {
  submittingProperty.value = true;
  try {
    const featureNames = propertyForm.value.feature_tags
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);

    const mediaAssets = [
      mediaForm.value.primary_image_url
        ? {
            media_type: 'IMAGE',
            external_url: mediaForm.value.primary_image_url,
            title: 'Primary property image',
            is_primary: true,
            is_public: true,
          }
        : null,
      mediaForm.value.virtual_tour_url
        ? {
            media_type: 'VIRTUAL_TOUR',
            external_url: mediaForm.value.virtual_tour_url,
            title: 'Virtual tour',
            is_public: true,
          }
        : null,
    ].filter(Boolean);

    const specification = {
      bedrooms: numberOrNull(specificationForm.value.bedrooms),
      bathrooms: numberOrNull(specificationForm.value.bathrooms),
      floors: numberOrNull(specificationForm.value.floors),
      parking_spaces: numberOrNull(specificationForm.value.parking_spaces),
      internal_area: numberOrNull(specificationForm.value.internal_area),
      internal_area_unit: specificationForm.value.internal_area_unit,
      lot_size: numberOrNull(specificationForm.value.lot_size),
      lot_size_unit: specificationForm.value.lot_size_unit,
      condition_rating: specificationForm.value.condition_rating,
      occupancy_status: specificationForm.value.occupancy_status,
    };

    const pricingProfile = {
      currency: pricingForm.value.currency || configStore.activeCurrencyCode || 'KES',
      asking_price: numberOrNull(pricingForm.value.asking_price),
      rent_amount: numberOrNull(pricingForm.value.rent_amount),
      pricing_strategy: pricingForm.value.pricing_strategy,
      requires_deposit: pricingForm.value.requires_deposit,
      deposit_amount: numberOrNull(pricingForm.value.deposit_amount),
    };

    const hasDevelopmentData = Boolean(
      developmentForm.value.zoning_info
      || developmentForm.value.development_stage
      || developmentForm.value.recommended_use
      || developmentForm.value.utilities_text
      || developmentForm.value.build_ready
    );

    const payload = {
      title: propertyForm.value.title,
      description: propertyForm.value.description,
      asset_type: propertyForm.value.asset_type,
      listing_type: propertyForm.value.listing_type,
      price_estimate: numberOrNull(propertyForm.value.price_estimate),
      location_text: propertyForm.value.location_text,
      formatted_address: propertyForm.value.formatted_address,
      financing_allowed: propertyForm.value.financing_allowed,
      appointment_enabled: propertyForm.value.appointment_enabled,
      inquiry_enabled: propertyForm.value.inquiry_enabled,
      manager: authStore.hasRole('PROPERTY_MANAGER') ? authStore.user?.id : null,
      specification,
      pricing_profile: pricingProfile,
      features: featureNames.map((name, index) => ({
        name,
        category: 'Highlight',
        is_highlighted: index < 6,
        sort_order: index + 1,
      })),
      media_assets: mediaAssets,
    };

    if (hasDevelopmentData) {
      payload.development_metadata = {
        zoning_info: developmentForm.value.zoning_info,
        build_ready: developmentForm.value.build_ready,
        utilities_available: developmentForm.value.utilities_text.split(',').map((item) => item.trim()).filter(Boolean),
        development_stage: developmentForm.value.development_stage,
        recommended_use: developmentForm.value.recommended_use,
      };
    }

    await api.post('/property/', payload);
    showAlert?.('Property listing created.', 'success');
    resetPropertyForm();
    closePropertyModal();
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to create property listing.', 'error');
  } finally {
    submittingProperty.value = false;
  }
}

async function createAvailability() {
  submittingAvailability.value = true;
  try {
    await api.post('/property/availability-windows/', availabilityForm.value);
    showAlert?.('Availability published.', 'success');
    resetAvailabilityForm();
    closeAvailabilityModal();
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to publish availability.', 'error');
  } finally {
    submittingAvailability.value = false;
  }
}

onMounted(loadDashboard);
</script>

<style scoped>
.pz-manager-form-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
}

.pz-manager-layout {
  display: grid;
  gap: 2rem;
  grid-template-columns: 1fr;
}

.pz-manager-section {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(20, 20, 20, 0.08);
  background: rgba(247, 244, 239, 0.8);
}

.pz-manager-feed {
  display: grid;
  gap: 0.9rem;
  padding: 1rem;
  border: 1px solid var(--pz-color-concrete-grey);
  background: white;
  text-decoration: none;
  color: inherit;
}

.pz-manager-list {
  display: grid;
  gap: 0.75rem;
}

.pz-manager-list__header,
.pz-manager-list__row {
  display: grid;
  gap: 1rem;
  align-items: center;
}

.pz-manager-list__header {
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1.2fr) minmax(0, 1.5fr) auto;
  padding: 0 0.25rem;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-manager-list__row {
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1.2fr) minmax(0, 1.5fr) auto;
  padding: 1rem 1.1rem;
  border: 1px solid var(--pz-color-concrete-grey);
  background: white;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.pz-manager-list__row:hover {
  transform: translateY(-1px);
  border-color: var(--pz-color-earth-orange);
  box-shadow: 0 10px 24px rgba(10, 10, 15, 0.08);
}

.pz-manager-list__primary,
.pz-manager-list__commercial {
  display: grid;
  gap: 0.35rem;
  min-width: 0;
}

.pz-manager-list__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pz-manager-pill {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.2rem 0.7rem;
  border: 1px solid rgba(20, 20, 20, 0.12);
  background: rgba(247, 244, 239, 0.9);
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.pz-manager-list__action {
  display: flex;
  justify-content: flex-end;
}

.pz-manager-link {
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--pz-color-earth-orange);
}

.pz-checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 2.8rem;
  padding: 0 0.75rem;
  border: 1px solid var(--pz-color-concrete-grey);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.u-xl-col-span-2,
.u-xl-col-span-3 {
  grid-column: span 1;
}

@media (min-width: 1280px) {
  .pz-manager-layout {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .u-xl-col-span-2 {
    grid-column: span 2;
  }

  .u-xl-col-span-3 {
    grid-column: span 3;
  }
}

@media (max-width: 920px) {
  .pz-manager-list__header {
    display: none;
  }

  .pz-manager-list__row {
    grid-template-columns: 1fr;
  }

  .pz-manager-list__action {
    justify-content: flex-start;
  }
}
</style>
