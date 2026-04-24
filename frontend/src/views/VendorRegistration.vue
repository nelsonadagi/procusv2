<template>
  <div class="pz-auth-page">
    <div class="pz-auth-shell pz-auth-shell--vendor">
      <section class="pz-auth-shell__intro">
        <div class="pz-auth-shell__eyebrow">VENDOR ONBOARDING</div>
        <h1 class="pz-auth-shell__title">Activate your supplier profile.</h1>
        <p class="pz-auth-shell__copy">
          Register your business identity, operating location, and delivery capabilities so your inventory can enter the procurement network.
        </p>

        <div class="pz-auth-shell__steps">
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">01</span>
            <div>
              <h3>Business registry</h3>
              <p>Capture the supplier business name and registration number used for platform verification.</p>
            </div>
          </div>
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">02</span>
            <div>
              <h3>Geo operations</h3>
              <p>Pin your operating base and delivery radius so discovery and logistics can route correctly.</p>
            </div>
          </div>
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">03</span>
            <div>
              <h3>Approval queue</h3>
              <p>Your profile enters the admin verification queue and remains pending until approved.</p>
            </div>
          </div>
        </div>
      </section>

      <Card class="pz-auth-card">
        <template #header>
          <div class="pz-u-text-center u-w-full">
            <h1 class="pz-u-text-display u-mb-2">Supplier Activation</h1>
            <p class="pz-u-text-mono text-xs">REGISTER YOUR VENDOR PROFILE</p>
          </div>
        </template>

        <form @submit.prevent="submitVendorProfile" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
          <PzInput v-model="form.business_name" label="BUSINESS_NAME" required />
          <PzInput v-model="form.registration_number" label="REGISTRATION_NUMBER" required />

          <div class="pz-input-wrapper">
            <label class="pz-input__label u-mb-3">OPERATING_LOCATION</label>
            <div class="pz-location-guide" :class="{ 'pz-location-guide--ready': isLocationReady }">
              <div class="pz-location-guide__header">
                <span class="pz-location-guide__badge">{{ isLocationReady ? 'LOCATION_READY' : 'ACTION_REQUIRED' }}</span>
                <span class="pz-location-guide__summary">
                  {{ isLocationReady ? 'Operating location captured and ready for submission.' : 'Choose your operating point before submitting this profile.' }}
                </span>
              </div>
              <ol class="pz-location-guide__steps">
                <li>Click on the map at your operating base, or use <strong>DETECT_GPS</strong>.</li>
                <li>Wait for the form to resolve a country and formatted address.</li>
                <li>Confirm that all location checks below turn ready.</li>
              </ol>
              <div class="pz-location-guide__status">
                <span :class="statusClass(form.country)">Country: {{ form.country ? 'resolved' : 'missing' }}</span>
                <span :class="statusClass(form.location)">Locality: {{ form.location || 'missing' }}</span>
                <span :class="statusClass(form.formatted_address)">Address: {{ form.formatted_address ? 'resolved' : 'missing' }}</span>
              </div>
            </div>
            <LocationInterface v-model="locationState" @change="handleLocationChange" />
          </div>

          <div class="pz-u-bg-limestone pz-p-4 pz-u-border">
            <label class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 cursor-pointer">
              <input type="checkbox" v-model="form.provides_delivery">
              <span class="pz-input__label">ENABLE_VENDOR_DELIVERY</span>
            </label>
          </div>

          <PzInput
            v-if="form.provides_delivery"
            v-model.number="form.delivery_radius_km"
            label="DELIVERY_RADIUS_KM"
            type="number"
          />

          <div class="pz-input-wrapper">
            <label class="pz-input__label u-mb-3">CATEGORIES_SERVED</label>
            <div v-if="loadingCategories" class="pz-u-text-mono text-xs pz-u-color-concrete">Loading material categories...</div>
            <div v-else class="pz-category-grid">
              <label
                v-for="category in categories"
                :key="category.id"
                class="pz-category-chip"
                :class="{ 'pz-category-chip--active': form.categories_served.includes(category.name) }"
              >
                <input v-model="form.categories_served" type="checkbox" :value="category.name" class="u-sr-only">
                {{ category.name }}
              </label>
            </div>
          </div>

          <Button type="submit" variant="primary" size="large" fullWidth :loading="submitting">
            {{ submitting ? 'Submitting Vendor Profile...' : 'Submit Vendor Profile' }}
          </Button>
        </form>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import Card from '../components/ui/Card.vue';
import Button from '../components/ui/Button.vue';
import PzInput from '../components/PzInput.vue';
import LocationInterface from '../components/ui/LocationInterface.vue';

const router = useRouter();
const showAlert = inject('showAlert', null);

const submitting = ref(false);
const loadingCategories = ref(true);
const categories = ref([]);

const form = ref({
  business_name: '',
  registration_number: '',
  country: null,
  location: '',
  latitude: null,
  longitude: null,
  formatted_address: '',
  location_hierarchy: {},
  provides_delivery: false,
  delivery_radius_km: 0,
  categories_served: []
});

const locationState = ref({
  lat: -1.2921,
  lng: 36.8219,
  address: '',
  city: '',
  country_id: null
});

const isLocationReady = computed(() => (
  Boolean(form.value.country) &&
  Boolean(form.value.location) &&
  Boolean(form.value.formatted_address)
));

function statusClass(value) {
  return value
    ? 'pz-location-guide__status-item pz-location-guide__status-item--ok'
    : 'pz-location-guide__status-item';
}

function handleLocationChange(loc) {
  form.value.latitude = loc.lat;
  form.value.longitude = loc.lng;
  form.value.formatted_address = loc.address;
  form.value.location = loc.city;
  form.value.country = loc.country_id;
}

async function fetchCategories() {
  try {
    const res = await api.get('/taxonomy/categories/?taxonomy_type=MATERIAL');
    categories.value = res.data.results || res.data;
  } catch (err) {
    showAlert?.('Failed to load material categories for vendor onboarding.', 'error');
  } finally {
    loadingCategories.value = false;
  }
}

async function submitVendorProfile() {
  if (!isLocationReady.value) {
    showAlert?.('Set your operating location on the map, then wait for country and address resolution before submitting.', 'error');
    return;
  }

  submitting.value = true;
  try {
    await api.post('/vendors/', form.value);
    showAlert?.('Vendor profile submitted. Your account is now pending admin approval.', 'success');
    router.push('/vendor/dashboard');
  } catch (err) {
    const detail = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || 'Failed to submit vendor profile.';
    showAlert?.(detail, 'error');
  } finally {
    submitting.value = false;
  }
}

onMounted(fetchCategories);
</script>

<style scoped>
.pz-auth-page {
  min-height: calc(100vh - 88px);
  padding: clamp(1.5rem, 4vw, 3rem);
}

.pz-auth-shell {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  gap: 1.5rem;
}

.pz-auth-shell__intro {
  position: relative;
  overflow: hidden;
  padding: clamp(1.5rem, 4vw, 3rem);
  background:
    linear-gradient(155deg, rgba(10, 10, 15, 0.98), rgba(34, 24, 18, 0.94)),
    radial-gradient(circle at top right, rgba(212, 101, 42, 0.22), transparent 28%);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 18px 18px 0 rgba(10, 10, 15, 0.12);
}

.pz-auth-shell__intro::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent 0, transparent calc(100% - 1px), rgba(255, 255, 255, 0.06) calc(100% - 1px)),
    linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(255, 255, 255, 0.03) calc(100% - 1px));
  background-size: 88px 88px;
  pointer-events: none;
}

.pz-auth-shell__eyebrow,
.pz-auth-shell__step-index {
  font-family: var(--pz-font-mono);
  text-transform: uppercase;
  letter-spacing: 0.18em;
}

.pz-auth-shell__eyebrow {
  display: inline-flex;
  margin-bottom: 1rem;
  font-size: 0.72rem;
  color: var(--pz-color-earth-orange);
}

.pz-auth-shell__title {
  max-width: 10ch;
  font-size: clamp(2.4rem, 6vw, 4.6rem);
  line-height: 0.96;
  margin-bottom: 1rem;
  color: white;
}

.pz-auth-shell__copy {
  max-width: 46ch;
  color: rgba(255, 255, 255, 0.74);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 2rem;
}

.pz-auth-shell__steps {
  display: grid;
  gap: 0.95rem;
}

.pz-auth-shell__step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  align-items: start;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.pz-auth-shell__step-index {
  font-size: 0.68rem;
  color: var(--pz-color-savanna-green);
  padding-top: 0.2rem;
}

.pz-auth-shell__step h3 {
  font-size: 1.05rem;
  color: white;
  margin-bottom: 0.35rem;
}

.pz-auth-shell__step p {
  font-size: 0.88rem;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.68);
}

.pz-location-guide {
  display: grid;
  gap: 0.9rem;
  margin-bottom: 1rem;
  padding: 1rem 1.1rem;
  border: 1px solid rgba(10, 10, 15, 0.14);
  background: rgba(245, 239, 232, 0.72);
}

.pz-location-guide--ready {
  border-color: rgba(61, 122, 80, 0.35);
  background: rgba(232, 242, 235, 0.92);
}

.pz-location-guide__header {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

.pz-location-guide__badge {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.55rem;
  background: var(--pz-color-foundation-black);
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
}

.pz-location-guide__summary {
  font-size: 0.92rem;
  color: rgba(10, 10, 15, 0.78);
}

.pz-location-guide__steps {
  margin: 0;
  padding-left: 1.1rem;
  color: rgba(10, 10, 15, 0.76);
  line-height: 1.6;
}

.pz-location-guide__status {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.pz-location-guide__status-item {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.55rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  color: rgba(10, 10, 15, 0.64);
  text-transform: uppercase;
}

.pz-location-guide__status-item--ok {
  border-color: rgba(61, 122, 80, 0.45);
  color: var(--pz-color-savanna-green);
}

.pz-category-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.pz-category-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.55rem 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.16);
  background: rgba(248, 246, 240, 0.78);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  cursor: pointer;
}

.pz-category-chip--active {
  background: var(--pz-color-earth-orange);
  border-color: var(--pz-color-earth-orange);
  color: white;
}

@media (min-width: 1024px) {
  .pz-auth-shell {
    grid-template-columns: 1.05fr 0.95fr;
    align-items: stretch;
  }
}
</style>
