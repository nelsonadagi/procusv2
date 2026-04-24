<template>
  <div class="pz-api-section">
    <div class="pz-admin-card">
      <div class="pz-admin-card__header">
        <div>
          <h3 class="pz-admin-card__title">EXTERNAL_INTEGRATION_ADAPTER</h3>
          <p class="pz-admin-card__meta">
            Draft courier connector settings here, then wire a live backend adapter when the integration endpoint is available.
          </p>
        </div>
      </div>
      <div class="pz-p-6">
        <div class="pz-status-banner" :class="statusClass">
          <div>
            <div class="pz-status-banner__eyebrow">ADAPTER_STATUS</div>
            <div class="pz-status-banner__value">{{ adapterStatus }}</div>
          </div>
          <div class="pz-status-banner__detail">
            {{ adapterMessage }}
          </div>
        </div>

        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-8">
          <div>
            <h4 class="pz-u-text-mono text-xs font-bold u-mb-4">CONNECTION_PARAMETERS</h4>
            <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
              <PzInput v-model="config.base_url" label="API_BASE_URL" placeholder="https://api.your-logistics.com/v1" />
              <PzInput v-model="config.api_key" label="API_KEY_HEADER" type="password" />
              <PzInput v-model="config.webhook_url" label="INCOMING_WEBHOOK_URL" placeholder="https://..." />
            </div>
            <div class="u-mt-6">
              <Button :loading="testing" @click="testConnection">VALIDATE_DRAFT</Button>
            </div>
          </div>

          <div class="pz-u-bg-limestone pz-p-6">
            <h4 class="pz-u-text-mono text-xs font-bold u-mb-4">ENDPOINT_MAPPING</h4>
            <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
              <PzInput v-model="config.create_order_endpoint" label="POST /orders" />
              <PzInput v-model="config.track_order_endpoint" label="GET /track" />
              <PzInput v-model="config.cancel_order_endpoint" label="POST /cancel" />
            </div>
          </div>
        </div>

        <div class="u-mt-8 pz-u-border-t pz-pt-6 pz-l-flex pz-l-flex--justify-between">
          <div class="pz-u-text-mono text-xs pz-u-color-concrete">
            // LAST_DRAFT_SAVE: {{ lastSync || 'NEVER' }}
          </div>
          <Button variant="primary" @click="saveConfig" :loading="saving">SAVE_CONFIGURATION_DRAFT</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import PzInput from '../PzInput.vue';
import Button from '../ui/Button.vue';

const STORAGE_KEY = 'pz_courier_api_config_draft';

const config = ref({
  base_url: '',
  api_key: '',
  webhook_url: '',
  create_order_endpoint: '/orders',
  track_order_endpoint: '/track',
  cancel_order_endpoint: '/orders/cancel'
});
const testing = ref(false);
const saving = ref(false);
const lastSync = ref(null);
const showAlert = inject('showAlert');

const adapterStatus = computed(() => {
  if (config.value.base_url && config.value.api_key && config.value.webhook_url) {
    return 'READY_FOR_BACKEND_WIRING';
  }

  if (config.value.base_url || config.value.api_key || config.value.webhook_url) {
    return 'PARTIAL_DRAFT';
  }

  return 'NOT_CONFIGURED';
});

const adapterMessage = computed(() => {
  if (adapterStatus.value === 'READY_FOR_BACKEND_WIRING') {
    return 'Core parameters are present. Live connectivity still requires a backend integration endpoint.';
  }

  if (adapterStatus.value === 'PARTIAL_DRAFT') {
    return 'Some parameters are in place, but the draft is incomplete and cannot be promoted yet.';
  }

  return 'No courier integration has been configured yet. Start with the base URL, API key, and webhook destination.';
});

const statusClass = computed(() => ({
  'pz-status-banner--success': adapterStatus.value === 'READY_FOR_BACKEND_WIRING',
  'pz-status-banner--warning': adapterStatus.value === 'PARTIAL_DRAFT',
  'pz-status-banner--neutral': adapterStatus.value === 'NOT_CONFIGURED'
}));

function persistDraft() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    config: config.value,
    lastSync: lastSync.value
  }));
}

function hydrateDraft() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return;

    const parsed = JSON.parse(stored);
    if (parsed?.config) {
      config.value = {
        ...config.value,
        ...parsed.config
      };
    }
    lastSync.value = parsed?.lastSync || null;
  } catch (error) {
    console.error('Failed to hydrate courier API draft', error);
  }
}

async function testConnection() {
  if (!config.value.base_url || !config.value.api_key) {
    showAlert('Base URL and API key are required before validating the adapter draft.', 'error');
    return;
  }

  testing.value = true;
  try {
    await new Promise((resolve) => setTimeout(resolve, 700));
    showAlert('Draft validated locally. Live connectivity tests need a backend connector endpoint.', 'info');
  } finally {
    testing.value = false;
  }
}

async function saveConfig() {
  if (!config.value.base_url) {
    showAlert('API base URL is required before saving the adapter draft.', 'error');
    return;
  }

  saving.value = true;
  try {
    await new Promise((resolve) => setTimeout(resolve, 400));
    lastSync.value = new Date().toLocaleString();
    persistDraft();
    showAlert('Courier adapter draft saved locally. Wire a backend endpoint to make it live.', 'success');
  } finally {
    saving.value = false;
  }
}

onMounted(hydrateDraft);
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
  color: var(--pz-color-text-secondary);
  max-width: 42rem;
  line-height: 1.55;
}

.pz-status-banner {
  display: grid;
  grid-template-columns: minmax(0, 16rem) minmax(0, 1fr);
  gap: var(--pz-space-4);
  padding: var(--pz-space-4);
  margin-bottom: var(--pz-space-6);
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(248, 246, 240, 0.78);
}

.pz-status-banner--success {
  border-left: 4px solid var(--pz-color-savanna-green);
}

.pz-status-banner--warning {
  border-left: 4px solid var(--pz-color-earth-orange);
}

.pz-status-banner--neutral {
  border-left: 4px solid var(--pz-color-concrete-grey);
}

.pz-status-banner__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
}

.pz-status-banner__value {
  margin-top: 0.35rem;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  letter-spacing: -0.02em;
}

.pz-status-banner__detail {
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .pz-status-banner {
    grid-template-columns: 1fr;
  }
}
</style>
