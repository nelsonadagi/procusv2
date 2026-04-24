<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="steel"
    title="Asset Control"
    eyebrow="SECURE_IDENTITY: INSTITUTIONAL_INVESTOR // SESSION: ENCRYPTED"
    signal-text="INVESTOR COMMERCE GRID ONLINE"
    :quickstats="quickstats"
    :sidebar-groups="[
      {
        title: 'Capital Metrics',
        items: [
          { id: 'portfolio', label: 'Portfolio Vital', icon: '◰' },
          { id: 'agreements', label: 'Agreement Logs', icon: '◈' },
          { id: 'compliance', label: 'Compliance Vault', icon: '🛡' }
        ]
      },
      {
        title: 'System Cmd',
        items: [
          { id: 'exit', label: 'Exit Console', icon: '⇚', action: () => $router.push('/') }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
        <div class="pz-status-indicator pz-status-indicator--pulse"></div>
        <Badge variant="primary">ALPHA_TIER_ACCESS</Badge>
      </div>
    </template>

    <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--lg-cols-3 pz-l-grid--gap-8">
      <!-- Compliance Module -->
      <section class="u-lg-col-span-1">
        <div class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Identity Verification</h3>
            <Badge :variant="profile?.kyc_status === 'VERIFIED' ? 'success' : 'warning'">
              {{ profile?.kyc_status === 'VERIFIED' ? 'Secure' : 'Pending' }}
            </Badge>
          </div>
          <div class="pz-p-6">
            <div v-if="profile" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
              <div class="pz-u-border-b pz-pb-4">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">KYC Protocol</span>
                <div class="font-bold pz-u-text-mono">{{ profile.kyc_status }}</div>
              </div>
              <div class="pz-u-border-b pz-pb-4">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">Accreditation Level</span>
                <div class="font-bold pz-u-text-mono">{{ profile.accreditation_status }}</div>
              </div>
              <div class="pz-u-border-b pz-pb-4">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">Legal Jurisdiction</span>
                <div class="font-bold pz-u-text-mono">{{ profile.jurisdiction }}</div>
              </div>
            </div>
            <EmptyState
              v-else
              icon="🛡"
              title="Profile not initialized"
              description="Complete investor onboarding to unlock compliance features."
            >
              <template #action>
                <Button variant="primary" block @click="onboard">Initialize Onboarding</Button>
              </template>
            </EmptyState>
          </div>
        </div>
      </section>

      <!-- Investment Stream -->
      <section class="u-lg-col-span-2">
        <div class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Investment Agreement Stream</h3>
            <span v-if="loading" class="pz-u-text-mono text-xs pz-u-color-concrete">Syncing...</span>
          </div>
          <div class="pz-table-wrapper">
            <table class="pz-admin-table">
              <thead>
                <tr>
                  <th>Asset Node</th>
                  <th>Capital Allocation</th>
                  <th>Protocol Status</th>
                  <th class="u-text-right">Command</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="agr in agreements" :key="agr.id">
                  <td>
                    <div class="font-bold pz-u-text-mono">PROJECT_#{{ agr.project }}</div>
                  </td>
                  <td class="pz-u-text-mono font-bold">{{ configStore.formatPrice(agr.amount) }}</td>
                  <td>
                    <Badge :variant="agr.status === 'SIGNED' ? 'success' : 'secondary'">{{ agr.status }}</Badge>
                  </td>
                  <td>
                    <div class="pz-l-flex pz-l-flex--justify-end">
                      <Button v-if="agr.status === 'DRAFT'" variant="primary" size="sm" @click="sign(agr.id)">Execute Sign</Button>
                      <span v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Verified</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="agreements.length === 0">
                  <td colspan="4" class="u-text-center pz-u-color-concrete u-py-12 pz-u-text-mono text-xs">
                    No active agreements detected in ledger.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  </DashboardShell>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import { useConfigStore } from '../stores/config';

const profile = ref(null);
const configStore = useConfigStore();
const agreements = ref([]);
const loading = ref(false);
const activeSection = ref('portfolio');

const totalAmount = computed(() => {
  return agreements.value.reduce((sum, agr) => sum + (parseFloat(agr.amount) || 0), 0);
});

const quickstats = computed(() => [
  { label: 'Total Capital Committed', value: configStore.formatPrice(totalAmount.value) },
  { label: 'Active Project Nodes', value: agreements.value.length },
  { label: 'Compliance Status', value: profile.value?.kyc_status || 'NOT_FOUND' }
]);

onMounted(() => loadData());

async function loadData() {
  loading.value = true;
  try {
    const pRes = await api.get('/v5/investors/');
    if (pRes.data && pRes.data.length > 0) {
      profile.value = pRes.data[0];
    } else if (pRes.data.results && pRes.data.results.length > 0) {
      profile.value = pRes.data.results[0];
    }

    const aRes = await api.get('/v5/agreements/');
    agreements.value = aRes.data.results || aRes.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function onboard() {
  await api.post('/v5/investors/onboard/', { jurisdiction: 'KE' });
  loadData();
}

async function sign(id) {
  await api.post(`/v5/agreements/${id}/sign/`);
  loadData();
}
</script>

<style scoped>
.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-concrete-grey);
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid var(--pz-color-concrete-grey);
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-3);
  align-items: flex-start;
}

@media (min-width: 640px) {
  .pz-admin-card__header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.pz-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.pz-admin-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.pz-admin-table th {
  text-align: left;
  padding: var(--pz-space-3) var(--pz-space-6);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  color: var(--pz-color-concrete-grey);
  border-bottom: 1px solid var(--pz-color-concrete-grey);
  background: var(--pz-color-limestone-white);
}

.pz-admin-table td {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  vertical-align: middle;
}

.pz-status-indicator {
  width: 12px;
  height: 12px;
  background: var(--pz-color-savanna-green);
  border-radius: 50%;
  display: inline-block;
}

.pz-status-indicator--pulse {
  animation: pz-pulse 3s infinite;
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
}

@keyframes pz-pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@media (prefers-reduced-motion: reduce) {
  .pz-status-indicator--pulse {
    animation: none;
  }
}

.u-lg-col-span-1 {
  grid-column: span 1;
}

.u-lg-col-span-2 {
  grid-column: span 2;
}

@media (min-width: 1024px) {
  .pz-l-grid--lg-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>
