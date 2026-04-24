<template>
  <div class="pz-admin-properties">
    <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center u-mb-8">
      <div>
        <h2 class="pz-u-text-display pz-properties-title">Asset Registry</h2>
        <p class="pz-u-text-mono text-xs pz-u-color-concrete pz-properties-subtitle">Manage and track your verified land and properties.</p>
      </div>
      <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
        <Button
          v-if="scope === 'mine'"
          variant="outline"
          size="sm"
          class="pz-btn-interactive"
          @click="openPropertyConsole"
        >
          Property Console
        </Button>
        <Button variant="primary" size="sm" class="pz-btn-interactive" @click="createProperty">
          + Initialize Asset
        </Button>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6 u-mb-12">
      <div v-for="(stat, idx) in stats" :key="stat.label" class="pz-command-node pz-glass-surface pz-animate-enter" :style="{ animationDelay: `${idx * 0.1}s` }">
        <div class="pz-command-node__label">{{ stat.label }}</div>
        <div class="pz-command-node__value">{{ stat.value }}</div>
        <div class="pz-command-node__accent"></div>
      </div>
    </div>

    <!-- Assets Table -->
    <div class="pz-admin-card pz-glass-panel pz-animate-enter" style="animation-delay: 0.4s;">
      <div class="pz-table-header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pz-u-p-4">
        <div class="pz-search-wrapper">
          <span class="pz-search-icon">🔍</span>
          <input v-model="searchQuery" type="text" class="pz-search-input" placeholder="Search assets by ID, name, or location..." />
        </div>
      </div>
      <div class="pz-table-wrapper">
        <table class="pz-admin-table">
          <thead>
            <tr>
              <th>Asset ID</th>
              <th>Identifier</th>
              <th>Type</th>
              <th>Location</th>
              <th>Valuation</th>
              <th>Status</th>
              <th class="u-text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prop in filteredProperties" :key="prop.id" class="pz-table-row-interactive">
              <td class="pz-u-text-mono text-xs font-bold">PRP-{{ prop.id.toString().padStart(4, '0') }}</td>
              <td>
                <div class="font-bold pz-asset-title">{{ prop.title }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">Owner: {{ prop.owner_name || 'System' }}</div>
              </td>
              <td>
                <Badge variant="secondary" size="sm">{{ prop.asset_type }}</Badge>
              </td>
              <td class="pz-u-text-mono text-xs">{{ prop.location_display || prop.location_text || prop.formatted_address || 'Location pending' }}</td>
              <td class="pz-u-text-mono font-bold">{{ configStore.formatPrice(prop.price_estimate) }}</td>
              <td>
                <Badge :variant="getStatusVariant(prop.status)" size="sm">{{ prop.status }}</Badge>
              </td>
              <td class="u-text-right">
                <button class="pz-action-btn" @click="manageProperty(prop.id)">Manage ↳</button>
              </td>
            </tr>
            <tr v-if="filteredProperties.length === 0">
              <td colspan="7" class="pz-u-text-mono text-xs pz-u-color-concrete pz-u-p-6 u-text-center">
                {{ properties.length === 0 ? 'No assets found in the registry.' : 'No assets match your search.' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../services/api';
import { useConfigStore } from '../../stores/config';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';

const props = defineProps({
  scope: {
    type: String,
    default: 'all'
  }
});

const configStore = useConfigStore();
const router = useRouter();
const properties = ref([]);
const stats = ref([
  { label: 'Total Assets', value: '0' },
  { label: 'Land Units', value: '0' },
  { label: 'Commercial', value: '0' },
  { label: 'Total Valuation', value: '$0' }
]);

const searchQuery = ref('');

const filteredProperties = computed(() => {
  if (!searchQuery.value) return properties.value;
  const q = searchQuery.value.toLowerCase();
  return properties.value.filter(prop => {
    const title = (prop.title || '').toLowerCase();
    const owner = (prop.owner_name || '').toLowerCase();
    const id = (`prp-${prop.id}`).toLowerCase();
    const loc = (prop.location_display || prop.location_text || prop.formatted_address || '').toLowerCase();
    const type = (prop.asset_type || '').toLowerCase();
    return title.includes(q) || owner.includes(q) || id.includes(q) || loc.includes(q) || type.includes(q);
  });
});

async function fetchProperties() {
  try {
    const params = props.scope === 'mine' ? { owner: 'me' } : {};
    const res = await api.get('/property/', { params });
    properties.value = res.data.results || res.data;
    calculateStats();
  } catch (err) {
    console.error(err);
  }
}

function calculateStats() {
  const land = properties.value.filter(p => p.asset_type === 'LAND').length;
  const commercial = properties.value.filter(p => p.asset_type === 'COMMERCIAL').length;
  const totalVal = properties.value.reduce((acc, p) => acc + parseFloat(p.price_estimate || 0), 0);

  stats.value[0].value = properties.value.length.toString();
  stats.value[1].value = land.toString();
  stats.value[2].value = commercial.toString();
  stats.value[3].value = configStore.formatPrice(totalVal);
}

function getStatusVariant(status) {
  if (status === 'ACTIVE' || status === 'VERIFIED') return 'success';
  if (status === 'SOLD' || status === 'PENDING') return 'warning';
  return 'secondary';
}

function manageProperty(propertyId) {
  router.push(`/properties/${propertyId}`);
}

function openPropertyConsole() {
  router.push('/property-manager/dashboard');
}

function createProperty() {
  if (props.scope === 'mine') {
    openPropertyConsole();
    return;
  }
  router.push('/properties');
}

onMounted(fetchProperties);
</script>

<style scoped>
.pz-properties-title {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  background: var(--pz-gradient-premium);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem;
}

.pz-properties-subtitle {
  letter-spacing: 0.05em;
  color: var(--pz-color-structural-steel);
}

.pz-animate-enter {
  opacity: 0;
  animation: tabEnter 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes tabEnter {
  0% { opacity: 0; transform: translateY(12px) scale(0.98); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

.pz-glass-surface {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.pz-glass-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 10px 30px rgba(10, 10, 15, 0.08);
  border-radius: var(--pz-border-radius-lg, 12px);
  overflow: hidden;
}

.pz-command-node {
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  border-radius: var(--pz-border-radius-lg, 12px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pz-command-node:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(10, 10, 15, 0.1);
  border-color: var(--pz-color-earth-orange, #D4652A);
}

.pz-command-node__label {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey, #718096);
  margin-bottom: 0.5rem;
}

.pz-command-node__value {
  font-family: var(--pz-font-display);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.pz-command-node__accent {
  position: absolute;
  top: 0;
  right: 0;
  width: 6px;
  height: 100%;
  background: var(--pz-color-foundation-black, #0A0A0F);
  transition: width 0.3s ease, background 0.3s ease;
}

.pz-command-node:hover .pz-command-node__accent {
  width: 8px;
  background: var(--pz-color-earth-orange, #D4652A);
}

.pz-table-wrapper {
  overflow-x: auto;
}

.pz-admin-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 700px;
}

.pz-admin-table th {
  text-align: left;
  padding: 1rem 1.5rem;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey, #718096);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  background: rgba(10, 10, 15, 0.02);
}

.pz-admin-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  vertical-align: middle;
}

.pz-table-row-interactive {
  transition: background 0.3s ease;
}

.pz-table-row-interactive:hover {
  background: rgba(255, 255, 255, 0.6);
}

.pz-asset-title {
  color: var(--pz-color-foundation-black);
  transition: color 0.3s ease;
}

.pz-table-row-interactive:hover .pz-asset-title {
  color: var(--pz-color-earth-orange);
}

.pz-action-btn {
  background: none;
  border: none;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: #2563EB;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pz-action-btn:hover {
  color: #0A0A0F;
  transform: translateX(4px);
}

.pz-btn-interactive {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pz-btn-interactive:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 101, 42, 0.3);
}

.pz-table-header {
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  background: rgba(10, 10, 15, 0.02);
}

.pz-search-wrapper {
  position: relative;
  width: 100%;
  max-width: 320px;
}

.pz-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.85rem;
  opacity: 0.5;
  pointer-events: none;
}

.pz-search-input {
  width: 100%;
  padding: 0.6rem 1rem 0.6rem 2.25rem;
  border-radius: var(--pz-border-radius-lg, 12px);
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.6);
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  color: var(--pz-color-foundation-black);
  transition: all 0.3s ease;
  outline: none;
}

.pz-search-input:focus {
  background: rgba(255, 255, 255, 0.95);
  border-color: var(--pz-color-earth-orange);
  box-shadow: 0 0 0 3px rgba(212, 101, 42, 0.1);
}

.pz-search-input::placeholder {
  color: var(--pz-color-concrete-grey);
}
</style>
