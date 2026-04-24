<template>
  <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-8">
    <!-- Command Nodes (Stats) -->
    <div class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6">
      <div v-for="stat in stats" :key="stat.label" class="pz-command-node pz-card--interactive u-hover-spring">
        <div class="pz-command-node__label u-text-glitch" :data-text="stat.label">{{ stat.label }}</div>
        <div class="pz-command-node__value" :class="stat.class">{{ stat.value }}</div>
        <div class="pz-command-node__accent"></div>
      </div>
    </div>

    <!-- Audit Log Terminal -->
    <div class="pz-terminal-wrapper pz-elevation-lg u-hover-glow">
      <div class="pz-terminal__header">
        <span class="pz-terminal__title">AUDIT_LOG_STREAM</span>
        <div class="pz-terminal__controls">
          <span>●</span> <span>●</span> <span>●</span>
        </div>
      </div>
      <div class="pz-terminal">
        <div class="pz-terminal__scanline"></div>
        <div v-for="log in auditLogs" :key="log.id" class="pz-terminal__line">
          <span class="pz-terminal__timestamp">[{{ new Date(log.timestamp).toLocaleTimeString() }}]</span>
          <span class="pz-terminal__actor">{{ log.actor_name }}</span>
          <span class="pz-terminal__action">{{ log.action }}</span>
          <span class="pz-terminal__resource">({RESOURCE: {{ log.resource_type }} #{{ log.resource_id }}})</span>
        </div>
        <div v-if="loading" class="pz-terminal__line pz-u-color-concrete">// STREAMING_DATA...</div>
        <div v-else-if="auditLogs.length === 0" class="pz-terminal__line pz-u-color-concrete">// NO_AUDIT_EVENTS_FOUND</div>
        <div class="pz-terminal__cursor">_</div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, inject, onMounted, ref } from 'vue';
  import api from '../../services/api';

  const auditLogs = ref([]);
  const contractors = ref([]);
  const vendors = ref([]);
  const kycRecords = ref([]);
  const pendingContracts = ref([]);
  const disputes = ref([]);
  const operators = ref([]);
  const loading = ref(true);
  const showAlert = inject('showAlert', null);

  const stats = computed(() => {
    const pendingCount =
      contractors.value.filter((c) => c.verified_status === 'PENDING').length +
      vendors.value.filter((v) => v.verified_status === 'PENDING').length +
      kycRecords.value.filter((record) => ['PENDING', 'SUBMITTED'].includes(record.status)).length +
      pendingContracts.value.length;
    const openDisputes = disputes.value.filter((entry) => ['OPENED', 'UNDER_REVIEW'].includes(entry.status)).length;
    const activeOperators = operators.value.filter((user) => user.is_active).length;
    return [
      { label: 'ACTIVE_OPERATORS', value: activeOperators, class: 'pz-u-color-savanna' },
      { label: 'AUDIT_EVENTS', value: auditLogs.value.length, class: '' },
      { label: 'PENDING_NODES', value: pendingCount, class: 'pz-u-color-earth' },
      { label: 'OPEN_DISPUTES', value: openDisputes, class: 'u-color-error' }
    ];
  });

  async function fetchData() {
    loading.value = true;
    try {
      const [logsRes, contractorsRes, vendorsRes, kycRes, contractsRes, disputesRes, operatorsRes] = await Promise.all([
        api.get('/rbac/audit-logs/'),
        api.get('/contractors/'),
        api.get('/vendors/'),
        api.get('/compliance/kyc-verifications/'),
        api.get('/contracts/?status=PENDING'),
        api.get('/v3/disputes/'),
        api.get('/platform_settings/admin-users/')
      ]);
      auditLogs.value = logsRes.data.results || logsRes.data;
      contractors.value = contractorsRes.data.results || contractorsRes.data;
      vendors.value = vendorsRes.data.results || vendorsRes.data;
      kycRecords.value = kycRes.data.results || kycRes.data;
      pendingContracts.value = contractsRes.data.results || contractsRes.data;
      disputes.value = disputesRes.data.results || disputesRes.data;
      operators.value = operatorsRes.data.results || operatorsRes.data;
    } catch (err) {
      console.error("Failed to fetch admin overview data", err);
      showAlert?.('Failed to load admin overview telemetry.', 'error');
    } finally {
      loading.value = false;
    }
  }

  onMounted(() => {
    fetchData();
  });
</script>

<style scoped>

  /* Local styles for Terminal and Command Nodes for better encapsulation */
  .pz-command-node {
    background: white;
    border: 1px solid var(--pz-color-foundation-black);
    padding: var(--pz-space-4);
    position: relative;
    overflow: hidden;
  }

  .pz-command-node__label {
    font-family: var(--pz-font-mono);
    font-size: 0.625rem;
    font-weight: 700;
    color: var(--pz-color-concrete-grey);
    margin-bottom: var(--pz-space-2);
  }

  .pz-command-node__value {
    font-family: var(--pz-font-display);
    font-size: 1.75rem;
    font-weight: 800;
  }

  .pz-command-node__accent {
    position: absolute;
    top: 0;
    right: 0;
    width: 4px;
    height: 100%;
    background: var(--pz-color-foundation-black);
  }

  .pz-command-node:hover .pz-command-node__accent {
    background: var(--pz-color-earth-orange);
  }

  .pz-terminal-wrapper {
    background: var(--pz-color-foundation-black);
    border-radius: var(--pz-border-radius-sm);
    overflow: hidden;
    box-shadow: var(--pz-shadow-lg);
  }

  .pz-terminal__header {
    background: #1A1A24;
    padding: var(--pz-space-2) var(--pz-space-4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .pz-terminal__title {
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    color: var(--pz-color-concrete-grey);
  }

  .pz-terminal__controls {
    display: flex;
    gap: 6px;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.2);
  }

  .pz-terminal {
    padding: var(--pz-space-4);
    height: 320px;
    overflow-y: auto;
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    color: #00FF9C;
    position: relative;
  }

  .pz-terminal__scanline {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
      linear-gradient(to right, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 4px, 3px 100%;
    pointer-events: none;
    z-index: 5;
  }

  .pz-terminal__line {
    margin-bottom: 4px;
    line-height: 1.4;
  }

  .pz-terminal__timestamp {
    color: var(--pz-color-concrete-grey);
    margin-right: 8px;
  }

  .pz-terminal__actor {
    color: var(--pz-color-earth-orange);
    margin-right: 8px;
    font-weight: 700;
  }

  .pz-terminal__action {
    color: white;
    margin-right: 8px;
  }

  .pz-terminal__resource {
    color: #4cc9f0;
    opacity: 0.8;
  }

  .pz-terminal__cursor {
    display: inline-block;
    animation: blink 1s infinite;
  }

  @keyframes blink {
    50% {
      opacity: 0;
    }
  }
</style>
