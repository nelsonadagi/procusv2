<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="savanna"
    title="Project Control Center"
    :eyebrow="`Registered Company: ${profile?.company_name || 'Authenticating'} // Verification Status: ${profile?.verified_status || 'Pending'}`"
    signal-text="PROJECT CONTROL GRID ONLINE"
    :quickstats="[
      { label: 'Bids', value: pendingBids.length },
      { label: 'Jobs', value: activeJobs.length },
      { label: 'Tenders', value: myContracts.length }
    ]"
    :sidebar-groups="[
      {
        title: 'Management',
        items: [
          { id: 'bids', label: 'Active Bids', icon: '📜' },
          { id: 'jobs', label: 'Active Jobs', icon: '🏗️' },
          { id: 'my-tenders', label: 'Posted Tenders', icon: '📝' },
          { id: 'profile', label: 'Business Profile', icon: '👤' }
        ]
      },
      {
        title: 'Actions',
        items: [
          { id: 'find-tenders', label: 'Find Tenders', icon: '🔍', action: () => $router.push('/tenders') },
          { id: 'exit', label: 'Exit Dashboard', icon: '⇚', action: () => $router.push('/') }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
        <div class="pz-status-indicator pz-status-indicator--pulse"></div>
        <Badge :variant="profile?.verified_status === 'APPROVED' ? 'success' : 'warning'">
          {{ profile?.verified_status === 'APPROVED' ? 'Verified' : 'Pending Verification' }}
        </Badge>
      </div>
    </template>

    <div v-if="needsOnboarding" class="pz-onboarding-state">
      <div class="pz-onboarding-state__kicker">CONTRACTOR_PROFILE_REQUIRED</div>
      <h3 class="pz-onboarding-state__title">Your contractor workspace needs a verified company profile.</h3>
      <p class="pz-onboarding-state__body">
        Submit your contractor registration to unlock bids, jobs, and tender management in this console.
      </p>
      <Button variant="primary" @click="$router.push('/contractors/register')">Complete Contractor Onboarding</Button>
    </div>

    <!-- Command Nodes (Stats) -->
    <div v-else class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6 u-mb-8">
      <div class="pz-command-node">
        <div class="pz-command-node__label">Active Proposals</div>
        <div class="pz-command-node__value">{{ pendingBids.length }}</div>
        <div class="pz-command-node__accent"></div>
      </div>
      <div class="pz-command-node">
        <div class="pz-command-node__label">Awarded Jobs</div>
        <div class="pz-command-node__value pz-u-color-savanna">{{ activeJobs.length }}</div>
        <div class="pz-command-node__accent"></div>
      </div>
      <div class="pz-command-node">
        <div class="pz-command-node__label">Bid Success Rate</div>
        <div class="pz-command-node__value pz-u-color-earth">74%</div>
        <div class="pz-command-node__accent"></div>
      </div>
      <div class="pz-command-node">
        <div class="pz-command-node__label">System Rating</div>
        <div class="pz-command-node__value">4.9</div>
        <div class="pz-command-node__accent"></div>
      </div>
    </div>

    <div v-if="!needsOnboarding" class="pz-admin-console__content">
      <!-- ACTIVE BIDS -->
      <div v-if="activeSection === 'bids'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <div class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Submitted Proposals</h3>
            <Button size="sm" variant="outline" @click="fetchData">Refresh</Button>
          </div>
          <div class="pz-table-wrapper">
            <table class="pz-admin-table">
              <thead>
                <tr>
                  <th>Project</th>
                  <th>Submission Date</th>
                  <th>Price</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bid in pendingBids" :key="bid.id">
                  <td>
                    <div class="font-bold">{{ bid.contract_title || 'NODE_#00' + bid.contract }}</div>
                  </td>
                  <td class="pz-u-text-mono text-xs">{{ new Date(bid.created_at).toLocaleDateString() }}</td>
                  <td class="pz-u-text-mono font-bold">{{ configStore.formatPrice(bid.proposed_cost, bid.contract_currency || 'KES') }}</td>
                  <td>
                    <Badge :variant="getBidStatusVariant(bid.status)">{{ bid.status }}</Badge>
                  </td>
                </tr>
                <tr v-if="pendingBids.length === 0">
                  <td colspan="4" class="u-text-center pz-u-color-concrete u-py-12 pz-u-text-mono text-xs">
                    No active proposals found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ACTIVE JOBS -->
      <div v-if="activeSection === 'jobs'" class="pz-l-grid pz-l-grid--columns-1 pz-l-grid--gap-6">
        <div v-for="job in activeJobs" :key="job.id" class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Active Job: {{ job.contract_title || 'Job #' + job.id }}</h3>
            <Badge variant="success">In Progress</Badge>
          </div>
          <div class="pz-p-6">
            <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-12 pz-l-flex--align-center">
              <div>
                <h4 class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4">Job Details</h4>
                <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                  <div class="pz-l-flex pz-l-flex--justify-between">
                    <span class="pz-u-text-mono text-xs">Value:</span>
                    <span class="pz-u-text-mono text-xs font-bold">{{ configStore.formatPrice(job.proposed_cost, job.contract_currency || 'KES') }}</span>
                  </div>
                  <div class="pz-l-flex pz-l-flex--justify-between">
                    <span class="pz-u-text-mono text-xs">Timeline:</span>
                    <span class="pz-u-text-mono text-xs font-bold">{{ job.proposed_timeline_days }} days</span>
                  </div>
                </div>
              </div>
              <div class="pz-u-bg-limestone pz-p-4 pz-u-border u-text-center">
                <p class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2">Completion</p>
                <div class="pz-u-text-display text-2xl">45%</div>
                <Button size="sm" variant="secondary" class="u-mt-4" @click="viewJobDetails(job)">View Details</Button>
              </div>
            </div>
          </div>
        </div>
        <EmptyState
          v-if="activeJobs.length === 0"
          icon="🏗️"
          title="No active jobs"
          description="Win bids on tenders to see your active jobs here."
        >
          <template #action>
            <Button variant="primary" @click="activeSection = 'bids'">View My Bids</Button>
          </template>
        </EmptyState>
      </div>

      <!-- POSTED TENDERS -->
      <div v-if="activeSection === 'my-tenders'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <div class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Posted Tenders</h3>
          </div>
          <div class="pz-table-wrapper">
            <table class="pz-admin-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Location</th>
                  <th>Budget Range</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in myContracts" :key="c.id" class="u-cursor-pointer" @click="$router.push(`/contracts/${c.id}`)">
                  <td class="font-bold">{{ c.title }}</td>
                  <td class="pz-u-text-mono text-xs">{{ c.location }}</td>
                  <td class="pz-u-text-mono text-xs">{{ configStore.formatPrice(c.budget_min, c.currency || 'KES') }} - {{ configStore.formatPrice(c.budget_max, c.currency || 'KES') }}</td>
                  <td>
                    <Badge :variant="c.status === 'POSTED' ? 'success' : 'warning'">{{ c.status }}</Badge>
                  </td>
                </tr>
                <tr v-if="myContracts.length === 0">
                  <td colspan="4" class="u-text-center pz-u-color-concrete u-py-12 pz-u-text-mono text-xs">
                    No posted tenders yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- PROFILE SECTION -->
      <div v-if="activeSection === 'profile'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <div class="pz-admin-card">
          <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">Business Registration Data</h3>
          </div>
          <div class="pz-p-8">
            <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-8">
              <div>
                <div class="u-mb-6">
                  <label class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2 u-block">Company Name</label>
                  <div class="font-bold text-lg pz-u-border-b pz-pb-2">{{ profile?.company_name }}</div>
                </div>
                <div class="u-mb-6">
                  <label class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2 u-block">Location</label>
                  <div class="font-bold text-lg pz-u-border-b pz-pb-2">{{ profile?.operating_region }}</div>
                </div>
              </div>
              <div>
                <label class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4 u-block">Services Offered</label>
                <div class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-3">
                  <span v-for="s in profile?.service_categories" :key="s" class="pz-spec-dot">{{ s }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardShell>
</template>

<script setup>
import { ref, onMounted, computed, provide } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import { useNotificationStore } from '../stores/notifications';

const router = useRouter();
const authStore = useAuthStore();
const configStore = useConfigStore();
const notificationStore = useNotificationStore();

const activeSection = ref('bids');
const loading = ref(true);
const profile = ref(null);
const needsOnboarding = ref(false);
const bids = ref([]);
const myContracts = ref([]);

const showAlert = (message, type = 'info') => {
  const mappedType = type === 'error' ? 'ERROR' : (type === 'success' ? 'PAYMENT' : 'BID');
  notificationStore.addNotification({
    message,
    type: mappedType,
    timestamp: new Date().toISOString()
  });
};

provide('showAlert', showAlert);

const pendingBids = computed(() => bids.value.filter(b => b.status !== 'AWARDED'));
const activeJobs = computed(() => bids.value.filter(b => b.status === 'AWARDED'));

const fetchData = async () => {
  loading.value = true;
  try {
    const [profRes, bidsRes, contRes] = await Promise.all([
      api.get('/contractors/me/'),
      api.get('/bids/'),
      api.get('/v2/contracts/')
    ]);
    profile.value = profRes.data;
    needsOnboarding.value = false;
    bids.value = bidsRes.data.results || bidsRes.data;
    const allContracts = contRes.data.results || contRes.data;
    myContracts.value = allContracts.filter(c => c.owner_username === authStore.user?.username);
  } catch (err) {
    if (err.response?.status === 404 || err.response?.status === 403) {
      needsOnboarding.value = true;
      profile.value = null;
      bids.value = [];
      myContracts.value = [];
    } else {
      console.error('Fetch error', err);
    }
  } finally {
    loading.value = false;
  }
};

const getBidStatusVariant = (status) => {
  if (status === 'SHORTLISTED') return 'info';
  if (status === 'AWARDED') return 'success';
  if (status === 'REJECTED') return 'danger';
  return 'warning';
};

const viewJobDetails = (job) => {
  router.push(`/contracts/${job.contract}`);
};

onMounted(() => fetchData());
</script>

<style scoped>
.pz-onboarding-state {
  margin-bottom: var(--pz-space-8);
  padding: var(--pz-space-6);
  border: 1px solid var(--pz-color-foundation-black);
  background: white;
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.06);
}

.pz-onboarding-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-earth-orange);
  margin-bottom: 0.75rem;
}

.pz-onboarding-state__title {
  font-size: 1.35rem;
  margin-bottom: 0.75rem;
}

.pz-onboarding-state__body {
  max-width: 42rem;
  margin-bottom: 1rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

.pz-command-node {
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(10, 10, 15, 0.08);
  padding: var(--pz-space-4);
  position: relative;
  overflow: hidden;
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
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

.pz-admin-console__content {
  padding: clamp(1rem, 2.5vw, 1.5rem);
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

.pz-admin-card {
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(10, 10, 15, 0.08);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
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

.pz-admin-table tr:hover {
  background: rgba(0, 0, 0, 0.02);
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

.pz-spec-dot {
  font-size: 0.65rem;
  padding: var(--pz-space-1) var(--pz-space-2);
  background: rgba(10, 10, 15, 0.05);
  border-radius: 4px;
  color: var(--pz-color-structural-steel);
}
</style>
