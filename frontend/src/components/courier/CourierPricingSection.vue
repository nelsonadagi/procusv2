<template>
  <div class="pz-pricing-section">
    <div class="pz-admin-card pz-u-border-thick">
      <div class="pz-admin-card__header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
        <h3 class="pz-admin-card__title">PRICING_ZONE_MATRIX</h3>
        <Button variant="primary" size="sm" @click="openAddZone">ADD_ZONE</Button>
      </div>

      <div class="pz-p-6">
        <div v-if="loading" class="pz-state-shell">
          <div class="pz-state-shell__kicker">NETWORK_LOADING</div>
          <div class="pz-state-shell__title">Hydrating corridor matrix</div>
          <div class="pz-state-shell__body">Pricing zones are loading from the logistics service.</div>
        </div>

        <div v-else-if="loadError" class="pz-state-shell pz-state-shell--error">
          <div class="pz-state-shell__kicker">LOAD_FAILURE</div>
          <div class="pz-state-shell__title">Unable to load pricing zones</div>
          <div class="pz-state-shell__body">{{ loadError }}</div>
          <Button variant="outline" size="sm" @click="fetchZones">RETRY_SYNC</Button>
        </div>

        <div v-else-if="zones.length === 0" class="u-text-center u-py-12 pz-u-text-mono text-xs pz-u-color-concrete">
          // NO_ZONES_DEFINED_IN_CATALOG
        </div>

        <div v-else class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div v-for="zone in zones" :key="zone.id" class="pz-zone-card u-hover-shift">
            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start u-mb-6">
              <div class="font-bold text-lg">{{ zone.name }}</div>
              <Badge variant="secondary" class="pz-badge--tactical">{{ zone.zone_type }}</Badge>
            </div>

            <div class="pz-zone-rules">
              <div v-for="rule in zone.rules" :key="rule.id" class="pz-rule-display">
                <span class="pz-u-text-mono text-xs">Base: {{ configStore.formatPrice(rule.base_cost, rule.currency || 'KES') }}</span>
                <span class="pz-u-text-mono text-xs">+ {{ configStore.formatPrice(rule.per_kg_cost, rule.currency || 'KES') }}/kg</span>
              </div>
            </div>

            <div class="u-mt-6 pz-l-flex pz-l-flex--gap-4 pz-u-border-t pz-pt-4 pz-zone-card__actions">
              <button class="pz-link-btn" @click="editZone(zone)">EDIT</button>
              <button class="pz-link-btn pz-link-btn--danger" @click="promptDelete(zone)">DELETE</button>
            </div>

            <div class="pz-zone-card__accent"></div>
          </div>
        </div>
      </div>
    </div>

    <Modal :isOpen="showModal" :title="editMode ? 'RECONFIGURE_ZONE' : 'DEPLOY_NEW_ZONE'" size="lg" @close="showModal = false">
      <div class="pz-p-4 pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">CORE_PARAMETERS</div>
            <PzInput v-model="form.name" label="ZONE_IDENTIFIER" placeholder="e.g. Nairobi Central" required />

            <div class="pz-input-wrapper">
              <label class="pz-input__label">GEOLOCATION_TYPE</label>
              <select v-model="form.zone_type" class="pz-input">
                <option value="RADIUS">RADIAL_CIRCLE (Standard)</option>
                <option value="POLYGON">POLYGON_AREA (Advanced)</option>
              </select>
            </div>

            <div v-if="form.zone_type === 'RADIUS'" class="u-mt-2">
              <PzInput v-model="form.radius_km" label="OPERATIONAL_RADIUS (KM)" type="number" step="0.1" required />
            </div>

            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mt-4 u-mb-2">TARIFF_STRUCTURE</div>
            <div class="pz-l-grid pz-l-grid--cols-2 pz-l-grid--gap-4">
              <PzInput v-model="form.base_cost" label="BASE_COST" type="number" step="0.01" required />
              <PzInput v-model="form.per_kg_rate" label="PER_KG_RATE" type="number" step="0.01" required />
            </div>
          </div>

          <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">INTERSPACIAL_BOUNDARIES</div>
            <div class="pz-u-border pz-p-2 pz-u-bg-limestone" style="min-height: 350px;">
              <LocationInterface v-model="locationState" @change="handleLocationChange" />
            </div>
            <div class="pz-u-text-mono text-[10px] pz-u-color-concrete">
              LAT: {{ form.center_lat }} // LNG: {{ form.center_lng }}
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button variant="ghost" @click="showModal = false">ABORT</Button>
        <Button variant="primary" :loading="saving" @click="saveZone">SYNCHRONIZE_RULES</Button>
      </template>
    </Modal>

    <Modal :isOpen="showDeleteModal" title="DECOMMISSION_CORRIDOR" size="sm" @close="showDeleteModal = false">
      <div class="pz-delete-prompt">
        <p class="pz-delete-prompt__title">
          Remove <strong>{{ zoneToDelete?.name }}</strong> from the courier pricing network?
        </p>
        <p class="pz-delete-prompt__body">
          This removes the zone and its tariff configuration from the active operational matrix.
        </p>
      </div>
      <template #footer>
        <Button variant="ghost" @click="showDeleteModal = false">CANCEL</Button>
        <Button variant="danger" :loading="deleting" @click="confirmDelete">REMOVE_ZONE</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';
import Modal from '../ui/Modal.vue';
import PzInput from '../PzInput.vue';
import LocationInterface from '../ui/LocationInterface.vue';
import { useConfigStore } from '../../stores/config';

const configStore = useConfigStore();
const zones = ref([]);
const showModal = ref(false);
const showDeleteModal = ref(false);
const editMode = ref(false);
const saving = ref(false);
const deleting = ref(false);
const loading = ref(false);
const loadError = ref('');
const zoneToDelete = ref(null);
const showAlert = inject('showAlert');

const locationState = ref({ lat: null, lng: null, city: '', country_id: null });

const form = ref({
  id: null,
  name: '',
  zone_type: 'RADIUS',
  base_cost: 0,
  per_kg_rate: 0,
  center_lat: null,
  center_lng: null,
  radius_km: 10.0
});

async function fetchZones() {
  loading.value = true;
  loadError.value = '';
  try {
    const res = await api.get('/logistics/pricing-zones/');
    zones.value = res.data.results || res.data;
  } catch (err) {
    console.error('Fetch zones error', err);
    loadError.value = err.response?.data?.detail || 'The courier pricing service did not respond.';
  } finally {
    loading.value = false;
  }
}

function handleLocationChange(loc) {
  form.value.center_lat = loc.lat;
  form.value.center_lng = loc.lng;
}

function openAddZone() {
  editMode.value = false;
  form.value = {
    id: null,
    name: '',
    zone_type: 'RADIUS',
    base_cost: 0,
    per_kg_rate: 0,
    center_lat: null,
    center_lng: null,
    radius_km: 10.0
  };
  locationState.value = { lat: null, lng: null, city: '', country_id: null };
  showModal.value = true;
}

function editZone(zone) {
  editMode.value = true;
  const rule = zone.rules?.[0] || {};
  form.value = {
    id: zone.id,
    name: zone.name,
    zone_type: zone.zone_type,
    base_cost: rule.base_cost || 0,
    per_kg_rate: rule.per_kg_cost || 0,
    center_lat: zone.center_lat,
    center_lng: zone.center_lng,
    radius_km: zone.radius_km || 10.0
  };
  locationState.value = {
    lat: zone.center_lat,
    lng: zone.center_lng,
    city: '',
    country_id: null
  };
  showModal.value = true;
}

async function saveZone() {
  if (!form.value.name) return showAlert('Identity required for deployment', 'error');
  if (!form.value.center_lat) return showAlert('Interspacial coordinates are missing. Select a point on the map.', 'error');

  saving.value = true;
  try {
    let zoneId = form.value.id;

    const zoneData = {
      name: form.value.name,
      zone_type: form.value.zone_type,
      center_lat: form.value.center_lat,
      center_lng: form.value.center_lng,
      radius_km: form.value.radius_km
    };

    if (editMode.value) {
      await api.patch(`/logistics/pricing-zones/${zoneId}/`, zoneData);
    } else {
      const zoneRes = await api.post('/logistics/pricing-zones/', zoneData);
      zoneId = zoneRes.data.id;
    }

    const ruleData = {
      zone: zoneId,
      base_cost: form.value.base_cost,
      per_kg_cost: form.value.per_kg_rate,
      express_multiplier: 1.5,
      same_day_multiplier: 2.0
    };

    const zone = zones.value.find((item) => item.id === zoneId);
    if (zone && zone.rules?.[0]) {
      await api.patch(`/logistics/pricing-rules/${zone.rules[0].id}/`, ruleData);
    } else {
      await api.post('/logistics/pricing-rules/', ruleData);
    }

    showAlert('Pricing corridor updated successfully.', 'success');
    showModal.value = false;
    fetchZones();
  } catch (err) {
    console.error('Save error', err.response?.data);
    showAlert('Sync failed: schema validation error.', 'error');
  } finally {
    saving.value = false;
  }
}

function promptDelete(zone) {
  zoneToDelete.value = zone;
  showDeleteModal.value = true;
}

async function confirmDelete() {
  if (!zoneToDelete.value) return;

  deleting.value = true;
  try {
    await api.delete(`/logistics/pricing-zones/${zoneToDelete.value.id}/`);
    showAlert('Pricing corridor removed from the active network.', 'success');
    showDeleteModal.value = false;
    zoneToDelete.value = null;
    fetchZones();
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Unable to remove this pricing zone.', 'error');
  } finally {
    deleting.value = false;
  }
}

onMounted(fetchZones);
</script>

<style scoped>
.pz-u-border-thick {
  border: 1px solid var(--pz-color-foundation-black);
}

.pz-admin-card {
  background: white;
}

.pz-admin-card__header {
  padding: var(--pz-space-6);
  border-bottom: 2px solid var(--pz-color-foundation-black);
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.pz-state-shell {
  display: grid;
  gap: 0.4rem;
  padding: var(--pz-space-6);
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(248, 246, 240, 0.8);
}

.pz-state-shell--error {
  border-left: 4px solid var(--pz-color-danger);
}

.pz-state-shell__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
}

.pz-state-shell__title {
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

.pz-state-shell__body {
  color: var(--pz-color-text-secondary);
  line-height: 1.5;
}

.pz-zone-card {
  background: #F8FAFC;
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: var(--pz-space-6);
  position: relative;
  overflow: hidden;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.pz-zone-card:hover {
  border-color: var(--pz-color-foundation-black);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.pz-zone-card__actions {
  border-top-style: dotted;
}

.pz-badge--tactical {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  background: #E2E8F0;
  color: #3182CE;
  border-radius: 8px;
  padding: 2px 12px;
}

.pz-rule-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #4A5568;
}

.pz-link-btn {
  background: none;
  border: none;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 4px;
  transition: color 0.2s;
}

.pz-link-btn:hover {
  color: var(--pz-color-earth-orange);
}

.pz-link-btn--danger:hover {
  color: #E53E3E;
}

.pz-zone-card__accent {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 2px;
  background: transparent;
  transition: background 0.2s;
}

.pz-zone-card:hover .pz-zone-card__accent {
  background: var(--pz-color-earth-orange);
}

.pz-delete-prompt__title {
  margin: 0;
  font-weight: 600;
  line-height: 1.5;
}

.pz-delete-prompt__body {
  margin: 0.75rem 0 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}
</style>
