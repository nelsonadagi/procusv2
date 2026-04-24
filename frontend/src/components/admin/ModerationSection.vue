<template>
  <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">Dispute Control</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">DISPUTE_ARBITRATION_QUEUE</h3>
          <div class="pz-section-shell__meta">Review open disputes and execute refund or release outcomes.</div>
        </div>
        <Badge :variant="openDisputes.length ? 'warning' : 'success'">{{ openDisputes.length ? `${openDisputes.length} OPEN` : 'ALL_CLEAR' }}</Badge>
      </div>

      <div v-if="loading" class="pz-section-shell__content">
        <div class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">QUERYING_DISPUTE_LEDGER</div>
        </div>
      </div>

      <div v-else-if="disputes.length === 0" class="pz-section-shell__content">
        <div class="pz-empty-state">
          <div class="pz-empty-state__glyph">DSP</div>
          <div class="pz-empty-state__eyebrow">Arbitration Queue</div>
          <h4 class="pz-empty-state__title">No disputes are currently recorded.</h4>
          <p class="pz-empty-state__body">Buyer and contract disputes will appear here when they require operator review.</p>
        </div>
      </div>

      <div v-else class="pz-table-wrapper pz-section-shell__content pz-data-table-shell">
        <table class="pz-admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>CHANNEL</th>
              <th>REASON</th>
              <th>STATUS</th>
              <th>EVIDENCE</th>
              <th class="u-text-right">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dispute in disputes" :key="dispute.id">
              <td class="pz-u-text-mono text-xs">DSP-{{ dispute.id }}</td>
              <td class="pz-u-text-mono text-xs">{{ dispute.contract ? 'CONTRACT' : dispute.order ? 'ORDER' : 'GENERAL' }}</td>
              <td>
                <div class="u-font-bold">{{ dispute.reason }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">Opened {{ formatDate(dispute.created_at) }}</div>
              </td>
              <td><Badge :variant="getStatusVariant(dispute.status)">{{ dispute.status }}</Badge></td>
              <td class="pz-u-text-mono text-xs">{{ dispute.evidence?.length || 0 }} item(s)</td>
              <td>
                <div class="pz-l-flex pz-l-flex--justify-end pz-l-flex--gap-3">
                  <Button
                    v-if="isResolvable(dispute)"
                    size="sm"
                    variant="primary"
                    :loading="actionState.id === dispute.id && actionState.outcome === 'RELEASE'"
                    @click="resolveDispute(dispute.id, 'RELEASE')"
                  >
                    RELEASE
                  </Button>
                  <Button
                    v-if="isResolvable(dispute)"
                    size="sm"
                    variant="danger"
                    :loading="actionState.id === dispute.id && actionState.outcome === 'REFUND'"
                    @click="resolveDispute(dispute.id, 'REFUND')"
                  >
                    REFUND
                  </Button>
                  <Badge v-else variant="ghost">RESOLVED</Badge>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';

const disputes = ref([]);
const loading = ref(true);
const actionState = ref({ id: null, outcome: null });
const showAlert = inject('showAlert', null);

const openDisputes = computed(() => disputes.value.filter((entry) =>
  ['OPENED', 'UNDER_REVIEW'].includes(entry.status)
));

function isResolvable(dispute) {
  return ['OPENED', 'UNDER_REVIEW'].includes(dispute.status);
}

function getStatusVariant(status) {
  if (status === 'RESOLVED_RELEASE') return 'success';
  if (status === 'RESOLVED_REFUND') return 'danger';
  if (status === 'UNDER_REVIEW') return 'info';
  return 'warning';
}

function formatDate(value) {
  return new Date(value).toLocaleString();
}

async function fetchDisputes() {
  loading.value = true;
  try {
    const res = await api.get('/v3/disputes/');
    disputes.value = res.data.results || res.data || [];
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to load dispute queue.', 'error');
  } finally {
    loading.value = false;
  }
}

async function resolveDispute(id, outcome) {
  actionState.value = { id, outcome };
  try {
    await api.post(`/v3/disputes/${id}/resolve/`, { outcome });
    await fetchDisputes();
    showAlert?.(`Dispute ${outcome === 'RELEASE' ? 'released' : 'refunded'} successfully.`, 'success');
  } catch (err) {
    showAlert?.(err.response?.data?.error || 'Failed to resolve dispute.', 'error');
  } finally {
    actionState.value = { id: null, outcome: null };
  }
}

onMounted(fetchDisputes);
</script>

<style scoped>
.pz-admin-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

.pz-admin-table th {
  text-align: left;
  padding: var(--pz-space-3) var(--pz-space-6);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  color: var(--pz-color-concrete-grey);
  border-bottom: 1px solid var(--pz-color-foundation-black);
  background: var(--pz-color-limestone-white);
}

.pz-admin-table td {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  vertical-align: top;
}
</style>
