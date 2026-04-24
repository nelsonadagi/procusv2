<template>
  <div class="pz-profile-section">
    <div class="pz-admin-card">
      <div class="pz-admin-card__header">
        <div>
          <h3 class="pz-admin-card__title">OFFICIAL_REGISTRATION_DATA</h3>
          <p class="pz-admin-card__meta">
            Keep the courier registry current so dispatch, support, and compliance workflows stay aligned.
          </p>
        </div>
      </div>
      <form @submit.prevent="saveProfile" class="pz-p-6">
        <div v-if="loading" class="pz-inline-state">
          <span class="pz-inline-state__label">PROFILE_SYNC</span>
          <span>Loading courier registry data...</span>
        </div>

        <div v-else-if="loadError" class="pz-inline-state pz-inline-state--error">
          <span class="pz-inline-state__label">REGISTRY_WARNING</span>
          <span>{{ loadError }}</span>
        </div>

        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <PzInput v-model="form.company_name" label="COMPANY_NAME" required />
          <PzInput v-model="form.registration_number" label="REGISTRATION_NO" required />
          <PzInput v-model="form.tax_pin" label="TAX_PIN / VAT_ID" />
          <PzInput v-model="form.website" label="WEBSITE_URL" />
          <PzInput v-model="form.support_email" label="SUPPORT_EMAIL" type="email" required />
          <PzInput v-model="form.support_phone" label="SUPPORT_HOTLINE" required />
        </div>

        <div class="u-mt-8">
          <LocationInterface v-model="locationState" @change="handleLocationChange" />
        </div>

        <div class="u-mt-8 pz-l-flex pz-l-flex--justify-end">
          <Button type="submit" variant="primary" :loading="saving">UPDATE_REGISTRY</Button>
        </div>
      </form>
    </div>

    <div class="pz-admin-card u-mt-8">
      <div class="pz-admin-card__header">
        <h3 class="pz-admin-card__title">COMPLIANCE_DOCUMENTS</h3>
      </div>
      <div class="pz-p-6">
        <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6">
          <div v-for="docType in documentTypes" :key="docType.code" class="pz-doc-upload">
            <div class="pz-u-text-mono text-xs font-bold u-mb-2">{{ docType.label }}</div>
            <div class="pz-doc-dropzone">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">SELECT_DOCUMENT</span>
              <input type="file" class="pz-doc-input" @change="uploadDocument($event, docType.code)">
            </div>
            <div v-if="documents[docType.code]" class="pz-doc-status">
              <span class="pz-doc-status__name">{{ documents[docType.code].name }}</span>
              <span class="pz-doc-status__meta">{{ documents[docType.code].sizeLabel }} • queued</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import PzInput from '../PzInput.vue';
import Button from '../ui/Button.vue';
import LocationInterface from '../ui/LocationInterface.vue';

const form = ref({
  company_name: '',
  registration_number: '',
  support_email: '',
  support_phone: '',
  country: null,
  location: '',
  latitude: null,
  longitude: null,
  formatted_address: ''
});

const locationState = ref({
  lat: -1.2921,
  lng: 36.8219,
  address: '',
  city: '',
  country_id: null
});

const saving = ref(false);
const loading = ref(false);
const loadError = ref('');
const documents = ref({});
const showAlert = inject('showAlert');

const documentTypes = [
  { code: 'LICENSE', label: 'TRANSPORT_LICENSE' },
  { code: 'INSURANCE', label: 'INSURANCE_CERT' },
  { code: 'REGISTRATION', label: 'BUSINESS_REG_CERT' }
];

async function fetchProfile() {
  loading.value = true;
  loadError.value = '';
  try {
    const res = await api.get('/logistics/couriers/me/');
    form.value = res.data;
    locationState.value = {
      lat: parseFloat(res.data.latitude) || -1.2921,
      lng: parseFloat(res.data.longitude) || 36.8219,
      address: res.data.formatted_address || '',
      city: res.data.location || '',
      country_id: res.data.country
    };
  } catch (err) {
    console.error('Profile fetch error', err);
    loadError.value = err.response?.data?.detail || 'No courier registry profile was returned.';
  } finally {
    loading.value = false;
  }
}

function handleLocationChange(loc) {
  form.value.latitude = loc.lat;
  form.value.longitude = loc.lng;
  form.value.formatted_address = loc.address;
  form.value.location = loc.city;
  form.value.country = loc.country_id;
}

async function saveProfile() {
  saving.value = true;
  try {
    let res;
    if (form.value.id) {
      res = await api.patch(`/logistics/couriers/${form.value.id}/`, form.value);
    } else {
      res = await api.post('/logistics/couriers/', form.value);
    }
    form.value = res.data;
    showAlert('Courier profile and operating base synchronized with the registry.', 'success');
  } catch (err) {
    console.error('Profile save error', err.response?.data);
    showAlert('Failed to update the official registry record.', 'error');
  } finally {
    saving.value = false;
  }
}

function uploadDocument(event, type) {
  const [file] = event.target.files || [];
  if (!file) return;

  if (file.size > 10 * 1024 * 1024) {
    showAlert(`${type} exceeds the 10MB upload limit.`, 'error');
    event.target.value = '';
    return;
  }

  documents.value[type] = {
    name: file.name,
    sizeLabel: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
    lastUpdated: new Date().toLocaleString()
  };
  showAlert(`${type} document queued for compliance upload.`, 'info');
  event.target.value = '';
}

onMounted(fetchProfile);
</script>

<style scoped>
.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 2px solid var(--pz-color-foundation-black);
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.pz-admin-card__meta {
  margin: 0.45rem 0 0;
  max-width: 44rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.5;
}

.pz-inline-state {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: var(--pz-space-5);
  padding: var(--pz-space-3) var(--pz-space-4);
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(248, 246, 240, 0.75);
  color: var(--pz-color-text-secondary);
}

.pz-inline-state--error {
  border-left: 4px solid var(--pz-color-danger);
}

.pz-inline-state__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
}

.pz-doc-dropzone {
  border: 2px dashed var(--pz-color-concrete-grey);
  padding: var(--pz-space-6);
  text-align: center;
  position: relative;
  cursor: pointer;
  background: var(--pz-color-limestone-white);
}

.pz-doc-dropzone:hover {
  border-color: var(--pz-color-earth-orange);
}

.pz-doc-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.pz-doc-status {
  display: grid;
  gap: 0.2rem;
  margin-top: 0.75rem;
  padding: 0.65rem 0.8rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(248, 246, 240, 0.65);
}

.pz-doc-status__name {
  font-size: 0.82rem;
  font-weight: 600;
}

.pz-doc-status__meta {
  font-size: 0.7rem;
  color: var(--pz-color-concrete-grey);
  font-family: var(--pz-font-mono);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
</style>
