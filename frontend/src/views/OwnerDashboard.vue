<template>
  <DashboardShell
    v-model:active-section="activeTab"
    accent="steel"
    title="Project Control Center"
    eyebrow="Account: Project Owner // Status: Active"
    :sidebar-groups="[
      {
        title: 'Portfolio Management',
        items: [
          { id: 'projects', label: 'Overview', icon: '◰' },
          { id: 'properties', label: 'My Properties', icon: '◰' },
          { id: 'quotes', label: 'Quote Requests', icon: '□' },
          { id: 'escrow', label: 'Payments', icon: '◈' },
          { id: 'logs', label: 'Activity Logs', icon: '⧇' }
        ]
      },
      {
        title: 'Quick Actions',
        items: [
          { id: 'new-project', label: 'Start New Project', icon: '+', action: () => $router.push('/projects/new') },
          { id: 'new-contract', label: 'Post a Tender', icon: '⊕', action: () => $router.push('/contracts/new') },
          { id: 'exit', label: 'Exit Dashboard', icon: '⇚', action: () => $router.push('/') }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
        <div class="pz-status-indicator pz-status-indicator--pulse"></div>
        <Badge variant="success">Compliance: Verified</Badge>
      </div>
    </template>

    <div class="pz-owner-workflow-card pz-glass-panel">
      <div class="pz-owner-workflow-card__summary">
        <div class="pz-owner-workflow-card__kicker">START HERE</div>
        <h3 class="pz-owner-workflow-card__title">{{ ownerWorkflow.title }}</h3>
        <p class="pz-owner-workflow-card__body">{{ ownerWorkflow.body }}</p>
        <div class="pz-owner-workflow-card__actions">
          <button class="pz-btn-glass" @click="ownerWorkflow.primaryAction.handler">{{ ownerWorkflow.primaryAction.label }}</button>
          <button v-if="ownerWorkflow.secondaryAction" class="pz-btn-glass" @click="ownerWorkflow.secondaryAction.handler">{{ ownerWorkflow.secondaryAction.label }}</button>
        </div>
      </div>
      <div class="pz-owner-workflow-card__metrics">
        <div class="pz-owner-workflow-metric">
          <span>Projects</span>
          <strong>{{ projects.length }}</strong>
        </div>
        <div class="pz-owner-workflow-metric">
          <span>Quote Requests</span>
          <strong>{{ quotes.length }}</strong>
        </div>
        <div class="pz-owner-workflow-metric">
          <span>Portfolio Updates</span>
          <strong>{{ recentUpdates.length }}</strong>
        </div>
      </div>
    </div>

    <WorkflowGuide title="Owner CTA" eyebrow="Action">
      <ModuleCTA
        eyebrow="Asset Action"
        title="Have property, materials, or a brief that should become a project?"
        body="Start a project, publish a tender, or open the property workspace so the asset can move into procurement and delivery."
        primary-label="Start Project"
        primary-to="/projects/new"
        secondary-label="List Property"
        secondary-to="/property-manager/dashboard"
        tone="steel"
      />
    </WorkflowGuide>

    <div v-if="activeTab === 'projects'" class="pz-tab-enter-active">
      <!-- Command Nodes (Stats) -->
      <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6 u-mb-12">
        <div class="pz-command-node pz-card--interactive u-hover-spring pz-glass-surface">
          <div class="pz-command-node__label">Total Investment</div>
          <div class="pz-command-node__value pz-u-color-savanna">{{ configStore.formatPrice(totalBudget, 'KES') }}</div>
          <div class="pz-command-node__accent"></div>
        </div>
        <div class="pz-command-node pz-card--interactive u-hover-spring pz-glass-surface">
          <div class="pz-command-node__label">Active Projects</div>
          <div class="pz-command-node__value">{{ activeProjectCount }}</div>
          <div class="pz-command-node__accent"></div>
        </div>
        <div class="pz-command-node pz-card--interactive u-hover-spring pz-glass-surface">
          <div class="pz-command-node__label">Funding Projects</div>
          <div class="pz-command-node__value pz-u-color-earth">{{ fundingProjectCount }}</div>
          <div class="pz-command-node__accent"></div>
        </div>
      </div>

      <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--lg-cols-3 pz-l-grid--gap-8">
        <!-- Active Portfolio Node -->
        <section class="u-lg-col-span-1">
          <div class="pz-admin-card pz-glass-panel">
            <div class="pz-admin-card__header">
              <h3 class="pz-admin-card__title">Active Project Units</h3>
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ projects.length }} Units</span>
            </div>
            <div class="pz-l-flex pz-l-flex--column">
              <div
                v-for="project in projectPreview"
                :key="project.id"
                class="pz-project-item pz-u-p-6 pz-u-border-b u-cursor-pointer"
                @click="$router.push(`/projects/${project.id}`)"
              >
                <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start u-mb-3">
                  <strong class="pz-u-text-mono text-sm pz-project-item__title">{{ project.title }}</strong>
                  <Badge variant="secondary" size="sm">{{ project.status }}</Badge>
                </div>
                <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
                  <span class="pz-u-text-mono text-xs pz-u-color-concrete">
                    {{ project.formatted_address || project.location_text || project.location || 'Location pending' }}
                  </span>
                  <span class="pz-u-text-mono text-xs pz-color-action-link">↳ View Details</span>
                </div>
              </div>
              <div v-if="projectPreview.length === 0" class="pz-u-p-6 pz-u-color-concrete pz-u-text-mono text-xs">
                No owner projects found yet.
              </div>
            </div>
          </div>
        </section>

        <!-- Procurement Stream -->
        <section class="u-lg-col-span-2">
          <div class="pz-admin-card pz-glass-panel">
            <div class="pz-admin-card__header">
              <h3 class="pz-admin-card__title">Recent Project Updates</h3>
            </div>
            <div class="pz-table-wrapper">
              <table class="pz-admin-table">
                <thead>
                  <tr>
                    <th>Project</th>
                    <th>Update</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="update in recentUpdates" :key="update.id" class="pz-table-row-interactive">
                    <td class="font-bold">{{ update.projectTitle }}</td>
                    <td class="pz-u-text-mono text-xs">{{ update.update_text }}</td>
                    <td class="pz-u-text-mono text-xs">{{ formatDate(update.created_at) }}</td>
                  </tr>
                  <tr v-if="recentUpdates.length === 0">
                    <td colspan="3" class="pz-u-text-mono text-xs pz-u-color-concrete">
                      No project updates published yet.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Escrow Pulse -->
          <div class="pz-workspace-status-card u-mt-8 pz-p-6">
            <div class="pz-workspace-status-card__bg"></div>
            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pz-workspace-status-card__content">
              <div>
                <h4 class="pz-u-text-mono text-xs font-bold u-mb-1 text-white">Owner Workspace Status</h4>
                <p class="pz-u-text-mono text-xs pz-u-color-limestone">Projects and properties are now scoped to your account.</p>
              </div>
              <div class="u-text-right">
                <div class="pz-u-text-display text-xl text-white">{{ projectPreview.length }}</div>
                <span class="pz-u-text-mono text-xs pz-u-color-savanna">Visible In Workspace</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <div v-else-if="activeTab === 'properties'" class="pz-tab-enter-active">
      <PropertiesSection scope="mine" />
    </div>

    <div v-else-if="activeTab === 'quotes'" class="pz-tab-enter-active">
      <div class="pz-admin-card pz-glass-panel">
        <div class="pz-admin-card__header">
          <div>
            <h3 class="pz-admin-card__title">My Quote Requests</h3>
            <p class="pz-section-note">Material quotes you requested from the marketplace.</p>
          </div>
          <button class="pz-btn-glass pz-u-text-mono text-xs" @click="fetchOwnerData">Refresh</button>
        </div>

        <div v-if="quotes.length === 0" class="pz-empty-quote-state">
          <div class="pz-empty-quote-state__kicker">No quote requests</div>
          <p>Request material quotes from product pages and they will appear here for tracking and checkout.</p>
          <button class="pz-btn-glass" @click="$router.push('/')">Find Materials</button>
        </div>

        <div v-else class="pz-owner-quote-list">
          <article v-for="quote in quotes" :key="quote.id" class="pz-owner-quote-card">
            <div class="pz-owner-quote-card__header">
              <div>
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">REQUEST #{{ quote.id }}</div>
                <strong>{{ quote.items?.length || 0 }} material line{{ (quote.items?.length || 0) === 1 ? '' : 's' }}</strong>
              </div>
              <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'" size="sm">{{ quote.status }}</Badge>
            </div>

            <div class="pz-owner-quote-card__items">
              <div v-for="item in quote.items" :key="item.id">
                {{ item.quantity }}x {{ item.product_details?.name || item.product_name || 'Material item' }}
              </div>
            </div>

            <div v-if="quote.responses?.length" class="pz-owner-quote-card__responses">
              <div v-for="response in quote.responses" :key="response.id" class="pz-owner-quote-response">
                <div>
                  <strong>{{ response.vendor_name || `Vendor #${response.vendor}` }}</strong>
                  <span>{{ configStore.formatPrice(Number(response.confirmed_price || 0) + Number(response.delivery_fee || 0), response.quote_currency || 'KES') }}</span>
                </div>
                <Badge v-if="response.has_order" variant="success" size="sm">ORDER #{{ response.order_id }}</Badge>
                <button v-else class="pz-action-btn" @click="$router.push('/buyer/dashboard')">Checkout</button>
              </div>
            </div>
            <div v-else class="pz-owner-quote-card__waiting">Waiting for vendor response.</div>
          </article>
        </div>
      </div>
    </div>

    <div v-else-if="activeTab === 'escrow'" class="pz-tab-enter-active">
      <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6 u-mb-8">
        <div class="pz-finance-card pz-glass-surface">
          <div class="pz-finance-card__icon pz-u-bg-savanna-soft">◈</div>
          <div class="pz-finance-card__content">
            <div class="pz-finance-card__label">Total Escrow Balance</div>
            <div class="pz-finance-card__value">{{ formatMoney(12450000) }}</div>
          </div>
        </div>
        <div class="pz-finance-card pz-glass-surface">
          <div class="pz-finance-card__icon pz-u-bg-copper-soft">◷</div>
          <div class="pz-finance-card__content">
            <div class="pz-finance-card__label">Pending Releases</div>
            <div class="pz-finance-card__value">{{ formatMoney(3250000) }}</div>
          </div>
        </div>
        <div class="pz-finance-card pz-glass-surface">
          <div class="pz-finance-card__icon pz-u-bg-steel-soft">✓</div>
          <div class="pz-finance-card__content">
            <div class="pz-finance-card__label">Completed Payments</div>
            <div class="pz-finance-card__value">{{ formatMoney(45800000) }}</div>
          </div>
        </div>
      </div>
      
      <div class="pz-admin-card pz-glass-panel">
        <div class="pz-admin-card__header">
          <h3 class="pz-admin-card__title">Recent Escrow Transactions</h3>
          <button class="pz-btn-glass pz-u-text-mono text-xs">View All</button>
        </div>
        <div class="pz-table-wrapper">
          <table class="pz-admin-table">
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Project</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trx in escrowTransactions" :key="trx.id" class="pz-table-row-interactive">
                <td class="pz-u-text-mono text-xs font-bold">{{ trx.id }}</td>
                <td>{{ trx.project }}</td>
                <td class="font-bold">{{ trx.amount }}</td>
                <td>
                  <Badge :variant="trx.status === 'Released' ? 'success' : (trx.status === 'In Escrow' ? 'warning' : 'secondary')" size="sm">
                    {{ trx.status }}
                  </Badge>
                </td>
                <td class="pz-u-text-mono text-xs">{{ trx.date }}</td>
                <td><button class="pz-action-btn">Review ↳</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else-if="activeTab === 'logs'" class="pz-tab-enter-active">
      <div class="pz-admin-card pz-glass-panel">
        <div class="pz-admin-card__header">
          <h3 class="pz-admin-card__title">Activity Timeline</h3>
        </div>
        <div class="pz-timeline-container pz-u-p-6">
          <div v-for="(log, idx) in activityLogs" :key="log.id" class="pz-timeline-item" :style="{ animationDelay: `${idx * 0.1}s` }">
            <div class="pz-timeline-item__node" :class="`pz-timeline-item__node--${log.type}`"></div>
            <div class="pz-timeline-item__content">
              <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center u-mb-1">
                <strong class="pz-u-text-mono text-xs">{{ log.user }}</strong>
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ log.time }}</span>
              </div>
              <p class="pz-timeline-item__text">{{ log.action }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="pz-module-state pz-glass-panel pz-tab-enter-active">
      <div class="pz-module-state__visual">
        <div class="pz-module-state__ring pz-module-state__ring--1"></div>
        <div class="pz-module-state__ring pz-module-state__ring--2"></div>
        <div class="pz-module-state__icon">⧉</div>
      </div>
      <div class="pz-module-state__kicker">FEATURE_STANDBY</div>
      <h3 class="pz-module-state__title">{{ activeTab }} is coming soon</h3>
      <p class="pz-module-state__body">
        This section is currently under development. Connected data, actions, and review states will be deployed in the next platform update.
      </p>
      <button class="pz-btn-glass u-mt-6" @click="activeTab = 'projects'">Return to Overview ↳</button>
    </div>
  </DashboardShell>
</template>

<script setup>
import { computed, ref, onMounted, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import { useConfigStore } from '../stores/config';
import Badge from '../components/ui/Badge.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';

const PropertiesSection = defineAsyncComponent(() => import('../components/admin/PropertiesSection.vue'));

const configStore = useConfigStore();
const router = useRouter();
const activeTab = ref('projects');
const projects = ref([]);
const quotes = ref([]);

function formatMoney(value) {
  return configStore.formatPrice(Number(value || 0), 'KES');
}

const escrowTransactions = ref([
  { id: 'TRX-9982', project: 'Nairobi Heights', amount: formatMoney(2500000), status: 'Released', date: 'Oct 12, 2025' },
  { id: 'TRX-9981', project: 'Lavington Villas', amount: formatMoney(850000), status: 'In Escrow', date: 'Oct 10, 2025' },
  { id: 'TRX-9980', project: 'Westlands Commercial', amount: formatMoney(4200000), status: 'Pending Approval', date: 'Oct 05, 2025' }
]);

const activityLogs = ref([
  { id: 'LOG-01', user: 'System', action: 'Compliance verification completed for Lavington Villas', time: '2 hours ago', type: 'system' },
  { id: 'LOG-02', user: 'Owner', action: 'Approved milestone 2 payment for Nairobi Heights', time: '1 day ago', type: 'user' },
  { id: 'LOG-03', user: 'Contractor', action: 'Uploaded site survey report for Westlands Commercial', time: '2 days ago', type: 'external' },
  { id: 'LOG-04', user: 'System', action: 'Generated monthly portfolio performance report', time: '3 days ago', type: 'system' }
]);

const projectPreview = computed(() => projects.value.slice(0, 3));
const totalBudget = computed(() =>
  projects.value.reduce((sum, project) => sum + Number(project.estimated_budget || 0), 0)
);
const activeProjectCount = computed(() =>
  projects.value.filter((project) => project.status !== 'COMPLETED').length
);
const fundingProjectCount = computed(() =>
  projects.value.filter((project) => project.funding_required).length
);
const recentUpdates = computed(() =>
  projects.value
    .flatMap((project) =>
      (project.updates || []).map((update) => ({
        ...update,
        projectTitle: project.title
      }))
    )
    .sort((left, right) => new Date(right.created_at) - new Date(left.created_at))
    .slice(0, 5)
);

const ownerWorkflow = computed(() => {
  if (!projects.value.length) {
    return {
      title: 'Create your first project',
      body: 'Start a project or post a tender so the owner workspace has something to track.',
      primaryAction: { label: 'Start New Project', handler: () => { activeTab.value = 'projects'; router.push('/projects/new'); } },
      secondaryAction: { label: 'Post a Tender', handler: () => router.push('/contracts/new') },
    };
  }

  if (!quotes.value.length) {
    return {
      title: 'Review your properties and quote requests',
      body: 'Your portfolio is active. Check properties, then use quote requests and updates to keep work moving.',
      primaryAction: { label: 'Open Properties', handler: () => { activeTab.value = 'properties'; } },
      secondaryAction: { label: 'View Activity', handler: () => { activeTab.value = 'logs'; } },
    };
  }

  return {
    title: 'Portfolio operations are active',
    body: 'Use the dashboard to review updates, manage quote responses, and follow the work as it moves through escrow.',
    primaryAction: { label: 'View Quote Requests', handler: () => { activeTab.value = 'quotes'; } },
    secondaryAction: { label: 'View Escrow', handler: () => { activeTab.value = 'escrow'; } },
  };
});

function formatDate(value) {
  return new Date(value).toLocaleDateString();
}

async function fetchOwnerData() {
  try {
    const [projectRes, quoteRes] = await Promise.all([
      api.get('/v4/projects/', { params: { owner: 'me' } }),
      api.get('/orders/quote-requests/')
    ]);
    projects.value = projectRes.data.results || projectRes.data;
    quotes.value = quoteRes.data.results || quoteRes.data;
  } catch (e) {
    console.error(e);
  }
}

onMounted(async () => {
  await fetchOwnerData();
});
</script>

<style scoped>
/* Glassmorphism & Surface Utilities */
.pz-glass-surface {
  background: var(--pz-glass-bg);
  backdrop-filter: var(--pz-blur-md);
  -webkit-backdrop-filter: var(--pz-blur-md);
  border: 1px solid var(--pz-glass-border);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.pz-glass-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: var(--pz-blur-lg);
  -webkit-backdrop-filter: var(--pz-blur-lg);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: var(--pz-shadow-lg);
}

.pz-owner-workflow-card {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
}

.pz-owner-workflow-card__summary {
  display: grid;
  gap: 0.55rem;
}

.pz-owner-workflow-card__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-owner-workflow-card__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1.25rem;
}

.pz-owner-workflow-card__body {
  max-width: 58ch;
  margin: 0;
  color: var(--pz-color-concrete-grey);
  line-height: 1.55;
}

.pz-owner-workflow-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.pz-owner-workflow-card__metrics {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.pz-owner-workflow-metric {
  display: grid;
  gap: 0.2rem;
  padding: 0.85rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.75);
}

.pz-owner-workflow-metric span {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-owner-workflow-metric strong {
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

/* Animations */
@keyframes tabEnter {
  0% {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.pz-tab-enter-active {
  animation: tabEnter 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes pz-pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@keyframes gradientPan {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Commands & Stats */
.pz-command-node {
  padding: var(--pz-space-5);
  position: relative;
  overflow: hidden;
  border-radius: var(--pz-border-radius-lg);
  transition: all var(--pz-transition-spring);
}

.pz-command-node:hover {
  transform: translateY(-4px);
  box-shadow: var(--pz-shadow-xl);
  border-color: var(--pz-color-earth-orange);
}

.pz-command-node__label {
  font-family: var(--pz-font-mono);
  font-size: 0.685rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--pz-color-concrete-grey);
  margin-bottom: var(--pz-space-2);
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
  background: var(--pz-color-foundation-black);
  transition: width var(--pz-transition-spring), background var(--pz-transition-base);
}

.pz-command-node:hover .pz-command-node__accent {
  width: 8px;
  background: var(--pz-color-earth-orange);
}

/* Admin Card (Overridden for better look) */
.pz-admin-card {
  border-radius: var(--pz-border-radius-lg);
  overflow: hidden;
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.4);
}

.pz-admin-card__title {
  font-family: var(--pz-font-display);
  font-size: 1.1rem;
  font-weight: 700;
}

.pz-section-note {
  margin: 0.25rem 0 0;
  color: var(--pz-color-concrete-grey);
  font-size: 0.82rem;
}

.pz-empty-quote-state {
  padding: var(--pz-space-8);
  display: grid;
  gap: var(--pz-space-3);
  color: var(--pz-color-concrete-grey);
}

.pz-empty-quote-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  color: var(--pz-color-earth-orange);
  text-transform: uppercase;
}

.pz-owner-quote-list {
  display: grid;
  gap: var(--pz-space-4);
  padding: var(--pz-space-6);
}

.pz-owner-quote-card {
  display: grid;
  gap: var(--pz-space-4);
  padding: var(--pz-space-5);
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-owner-quote-card__header,
.pz-owner-quote-response {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--pz-space-4);
}

.pz-owner-quote-card__items {
  display: grid;
  gap: 0.35rem;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
}

.pz-owner-quote-card__responses {
  display: grid;
  gap: var(--pz-space-3);
  padding-top: var(--pz-space-3);
  border-top: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-owner-quote-response {
  padding: var(--pz-space-3);
  background: rgba(10, 10, 15, 0.03);
}

.pz-owner-quote-response div {
  display: grid;
  gap: 0.2rem;
}

.pz-owner-quote-response span,
.pz-owner-quote-card__waiting {
  color: var(--pz-color-concrete-grey);
  font-size: 0.82rem;
}

/* Projects Flow */
.pz-project-item {
  background: transparent;
  transition: all var(--pz-transition-base);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
}

.pz-project-item:hover {
  background: rgba(255, 255, 255, 0.9);
  padding-left: var(--pz-space-8);
}

.pz-project-item__title {
  transition: color var(--pz-transition-base);
}

.pz-project-item:hover .pz-project-item__title {
  color: var(--pz-color-earth-orange);
}

.pz-color-action-link {
  color: var(--pz-color-earth-orange);
  transition: transform var(--pz-transition-fast);
  display: inline-block;
}

.pz-project-item:hover .pz-color-action-link {
  transform: translateX(4px);
}

/* Tables */
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
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  background: rgba(10, 10, 15, 0.02);
}

.pz-admin-table td {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  vertical-align: middle;
}

.pz-table-row-interactive {
  transition: background var(--pz-transition-base);
}

.pz-table-row-interactive:hover {
  background: rgba(255, 255, 255, 0.6);
}

/* Escrow Dashboard specific */
.pz-finance-card {
  display: flex;
  align-items: center;
  gap: var(--pz-space-4);
  padding: var(--pz-space-5);
  border-radius: var(--pz-border-radius-lg);
  transition: all var(--pz-transition-spring);
}

.pz-finance-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--pz-shadow-lg);
}

.pz-finance-card__icon {
  width: 48px;
  height: 48px;
  border-radius: var(--pz-border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.pz-u-bg-savanna-soft { background: rgba(5, 150, 105, 0.15); color: var(--pz-color-savanna-green); }
.pz-u-bg-copper-soft { background: rgba(184, 115, 51, 0.15); color: var(--pz-color-copper-circuit); }
.pz-u-bg-steel-soft { background: rgba(37, 99, 235, 0.15); color: var(--pz-color-steel-blue); }

.pz-finance-card__label {
  font-family: var(--pz-font-mono);
  font-size: 0.685rem;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.25rem;
}

.pz-finance-card__value {
  font-family: var(--pz-font-display);
  font-size: 1.5rem;
  font-weight: 800;
}

.pz-action-btn {
  background: none;
  border: none;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--pz-color-steel-blue);
  cursor: pointer;
  transition: all var(--pz-transition-fast);
}

.pz-action-btn:hover {
  color: var(--pz-color-foundation-black);
  transform: translateX(4px);
}

/* Timeline */
.pz-timeline-container {
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-6);
  position: relative;
}

.pz-timeline-container::before {
  content: '';
  position: absolute;
  left: calc(var(--pz-space-6) + 5px);
  top: var(--pz-space-6);
  bottom: var(--pz-space-6);
  width: 2px;
  background: rgba(10, 10, 15, 0.05);
}

.pz-timeline-item {
  display: flex;
  gap: var(--pz-space-4);
  position: relative;
  z-index: 1;
  opacity: 0;
  animation: tabEnter 0.5s ease forwards;
}

.pz-timeline-item__node {
  flex-shrink: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 5px;
  background: var(--pz-color-foundation-black);
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.8);
}

.pz-timeline-item__node--system { background: var(--pz-color-steel-blue); }
.pz-timeline-item__node--user { background: var(--pz-color-savanna-green); }
.pz-timeline-item__node--external { background: var(--pz-color-copper-circuit); }

.pz-timeline-item__content {
  background: rgba(255, 255, 255, 0.6);
  padding: var(--pz-space-4);
  border-radius: var(--pz-border-radius-md);
  border: 1px solid rgba(10, 10, 15, 0.05);
  flex-grow: 1;
  transition: all var(--pz-transition-base);
}

.pz-timeline-item:hover .pz-timeline-item__content {
  background: white;
  box-shadow: var(--pz-shadow-md);
  transform: translateX(4px);
}

.pz-timeline-item__text {
  font-size: 0.95rem;
  color: var(--pz-color-structural-steel);
  margin: 0;
}

/* Buttons */
.pz-btn-glass {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.1);
  padding: var(--pz-space-2) var(--pz-space-4);
  border-radius: var(--pz-border-radius-lg);
  font-family: var(--pz-font-mono);
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  cursor: pointer;
  transition: all var(--pz-transition-spring);
  backdrop-filter: var(--pz-blur-sm);
}

.pz-btn-glass:hover {
  background: white;
  box-shadow: var(--pz-shadow-md);
  transform: translateY(-2px);
  border-color: var(--pz-color-earth-orange);
}

/* Banners & Empty States */
.pz-workspace-status-card {
  position: relative;
  overflow: hidden;
  border-radius: var(--pz-border-radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.pz-workspace-status-card__bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--pz-color-foundation-black) 0%, #1A1A24 100%);
  z-index: 0;
}

.pz-workspace-status-card__bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(212, 101, 42, 0.4), transparent 50%);
  opacity: 0.8;
  animation: pz-pulse 4s infinite alternate;
}

.pz-workspace-status-card__content {
  position: relative;
  z-index: 1;
}

.pz-module-state {
  border-radius: var(--pz-border-radius-lg);
  padding: clamp(2rem, 5vw, 4rem);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pz-module-state__visual {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--pz-space-6);
}

.pz-module-state__ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1px solid var(--pz-color-earth-orange);
  opacity: 0.2;
}

.pz-module-state__ring--1 {
  animation: pz-pulse 3s infinite;
}

.pz-module-state__ring--2 {
  inset: -10px;
  border-color: var(--pz-color-copper-circuit);
  animation: pz-pulse 3s infinite;
  animation-delay: 1.5s;
}

.pz-module-state__icon {
  font-size: 2rem;
  color: var(--pz-color-earth-orange);
  z-index: 1;
}

.pz-module-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-concrete-grey);
  text-transform: uppercase;
}

.pz-module-state__title {
  margin: 0.7rem 0 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.4rem, 2.5vw, 2rem);
  color: var(--pz-color-foundation-black);
}

.pz-module-state__body {
  max-width: 32rem;
  margin: 0.8rem 0 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

/* Utilities */
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

.u-lg-col-span-1 { grid-column: span 1; }
.u-lg-col-span-2 { grid-column: span 2; }

@media (min-width: 1024px) {
  .pz-l-grid--lg-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (prefers-reduced-motion: reduce) {
  .pz-status-indicator--pulse, .pz-tab-enter-active, .pz-workspace-status-card__bg::after, .pz-module-state__ring--1, .pz-module-state__ring--2 {
    animation: none;
  }
}
</style>
