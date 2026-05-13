<template>
  <div class="pz-investor-page">
    <div v-if="loading" class="pz-u-text-center u-py-20">
      <div class="c-loader u-mb-4"></div>
      <p class="pz-u-text-mono text-xs">Loading portfolio...</p>
    </div>

    <div v-else class="pz-l-container u-py-8">
      <!-- Breadcrumb -->
      <nav class="pz-breadcrumb u-mb-6">
        <span class="pz-breadcrumb__current pz-u-color-steel">Investor Workspace</span>
      </nav>

      <!-- Hero -->
      <section class="pz-investor-hero">
        <div class="pz-investor-hero__content">
          <div class="pz-space-y-3">
            <div class="pz-u-text-mono text-xs pz-u-color-earth">Capital Partner</div>
            <h1 class="pz-u-text-display">Investment Portfolio</h1>
            <p class="pz-u-text-mono text-sm pz-u-color-steel">
              Track your commitments, agreements, financing applications, and returns across the construction ecosystem.
            </p>
          </div>

          <div class="pz-investor-hero__stats">
            <div class="pz-investor-stat">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Total Committed</span>
              <strong>{{ formatPrice(totalCommitted, 'KES') }}</strong>
            </div>
            <div class="pz-investor-stat">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Active Projects</span>
              <strong>{{ agreements.length }}</strong>
            </div>
            <div class="pz-investor-stat">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Pending Pledges</span>
              <strong>{{ pendingPledges }}</strong>
            </div>
            <div class="pz-investor-stat">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Open Applications</span>
              <strong>{{ openApplications }}</strong>
            </div>
          </div>
        </div>
      </section>

      <!-- Layout -->
      <div class="pz-investor-layout">
        <section class="pz-space-y-6">
          <!-- Tabs -->
          <div class="pz-investor-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="pz-investor-tab"
              :class="{ 'pz-investor-tab--active': activeTab === tab.id }"
              @click="activeTab = tab.id"
            >
              <span class="pz-investor-tab__label">{{ tab.label }}</span>
              <span v-if="tab.count !== null" class="pz-investor-tab__badge">{{ tab.count }}</span>
            </button>
          </div>

          <!-- Portfolio Tab -->
          <div v-show="activeTab === 'portfolio'" class="pz-tab-panel pz-space-y-6">
            <Card title="Investment Summary" variant="premium" eyebrow="Overview">
              <div v-if="agreements.length === 0" class="pz-investor-empty">
                <div class="pz-investor-empty__kicker">NO ACTIVE INVESTMENTS</div>
                <p>Browse projects seeking funding to start building your portfolio.</p>
                <Button variant="primary" class="u-mt-4" @click="$router.push('/projects')">Discover Projects</Button>
              </div>
              <div v-else class="pz-detail-stack">
                <div v-for="agr in agreements" :key="agr.id" class="pz-agreement-card">
                  <div class="pz-agreement-card__top">
                    <div>
                      <div class="pz-agreement-card__project">Project #{{ agr.project }}</div>
                      <div class="pz-agreement-card__meta">Signed {{ formatDate(agr.signed_at) || 'Pending' }}</div>
                    </div>
                    <div class="pz-agreement-card__amount">{{ formatPrice(agr.amount, agr.currency || 'KES') }}</div>
                  </div>
                  <div class="pz-agreement-card__footer">
                    <Badge :variant="getAgreementVariant(agr.status)">{{ agr.status }}</Badge>
                    <Button v-if="agr.status === 'DRAFT'" size="sm" variant="primary" @click="sign(agr.id)">Sign Agreement</Button>
                    <span v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Verified</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card title="Recent Activity" variant="premium" eyebrow="Timeline">
              <div v-if="agreements.length === 0 && financeApps.length === 0" class="pz-investor-empty">
                <p>No recent activity to display.</p>
              </div>
              <div v-else class="pz-activity-list">
                <div v-for="agr in agreements.slice(0, 5)" :key="`agr-${agr.id}`" class="pz-activity-item">
                  <span class="pz-activity-item__icon">📄</span>
                  <div class="pz-activity-item__content">
                    <strong>Agreement {{ agr.status === 'SIGNED' ? 'signed' : 'created' }}</strong>
                    <span>Project #{{ agr.project }} — {{ formatPrice(agr.amount, agr.currency || 'KES') }}</span>
                  </div>
                  <span class="pz-activity-item__date">{{ formatDate(agr.created_at) }}</span>
                </div>
              </div>
            </Card>
          </div>

          <!-- Agreements Tab -->
          <div v-show="activeTab === 'agreements'" class="pz-tab-panel pz-space-y-6">
            <Card title="Investment Agreements" variant="premium" eyebrow="Legal">
              <div v-if="agreements.length === 0" class="pz-investor-empty">
                <div class="pz-investor-empty__kicker">NO AGREEMENTS</div>
                <p>Agreements are created after you pledge to a project and the owner initiates terms.</p>
              </div>
              <div v-else class="pz-detail-stack">
                <div v-for="agr in agreements" :key="agr.id" class="pz-agreement-card">
                  <div class="pz-agreement-card__top">
                    <div>
                      <div class="pz-agreement-card__project">Project #{{ agr.project }}</div>
                      <div class="pz-agreement-card__meta">
                        Status: {{ agr.status }} &bull; Created {{ formatDate(agr.created_at) }}
                      </div>
                    </div>
                    <div class="pz-agreement-card__amount">{{ formatPrice(agr.amount, agr.currency || 'KES') }}</div>
                  </div>
                  <p v-if="agr.agreement_terms_url" class="pz-agreement-card__terms">
                    <a :href="agr.agreement_terms_url" target="_blank" rel="noreferrer">View Terms Document</a>
                  </p>
                  <div class="pz-agreement-card__footer">
                    <Badge :variant="getAgreementVariant(agr.status)">{{ agr.status }}</Badge>
                    <Button v-if="agr.status === 'DRAFT'" size="sm" variant="primary" @click="sign(agr.id)">Execute Sign</Button>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          <!-- Applications Tab -->
          <div v-show="activeTab === 'applications'" class="pz-tab-panel pz-space-y-6">
            <Card title="Finance Applications" variant="premium" eyebrow="Credit">
              <div v-if="financeApps.length === 0" class="pz-investor-empty">
                <div class="pz-investor-empty__kicker">NO APPLICATIONS</div>
                <p>Apply for material credit, working capital, or project financing.</p>
                <Button variant="primary" class="u-mt-4" @click="$router.push('/finance/apply')">Apply for Financing</Button>
              </div>
              <div v-else class="pz-detail-stack">
                <div v-for="app in financeApps" :key="app.id" class="pz-agreement-card">
                  <div class="pz-agreement-card__top">
                    <div>
                      <div class="pz-agreement-card__project">{{ app.product_details?.name || 'Finance Product' }}</div>
                      <div class="pz-agreement-card__meta">
                        {{ app.target_type }} &bull; {{ app.purpose_category }} &bull; {{ formatDate(app.created_at) }}
                      </div>
                    </div>
                    <div class="pz-agreement-card__amount">{{ formatPrice(app.requested_amount, app.currency || 'KES') }}</div>
                  </div>
                  <div class="pz-agreement-card__footer">
                    <Badge :variant="getAppVariant(app.status)">{{ app.status }}</Badge>
                  </div>
                </div>
              </div>
            </Card>
            <div class="pz-l-flex pz-l-flex--justify-end">
              <Button variant="outline" @click="$router.push('/finance/apply')">New Application</Button>
            </div>
          </div>

          <!-- Accounts Tab -->
          <div v-show="activeTab === 'accounts'" class="pz-tab-panel pz-space-y-6">
            <BankAccountManager />
          </div>
        </section>

        <!-- Sidebar -->
        <aside class="pz-investor-sidebar">
          <Card title="Compliance Status" variant="elevated">
            <div v-if="profile" class="pz-detail-stack">
              <div class="pz-detail-subcard">
                <span>KYC Status</span>
                <strong>{{ profile.kyc_status }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Accreditation</span>
                <strong>{{ profile.accreditation_status }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Jurisdiction</span>
                <strong>{{ profile.jurisdiction }}</strong>
              </div>
            </div>
            <EmptyState
              v-else
              icon="🛡"
              title="Profile not initialized"
              description="Complete onboarding to unlock all features."
            >
              <template #action>
                <Button variant="primary" block @click="onboard">Initialize</Button>
              </template>
            </EmptyState>
          </Card>

          <Card title="Quick Actions" variant="glass">
            <div class="pz-detail-stack">
              <Button block variant="primary" @click="$router.push('/projects')">Find Projects</Button>
              <Button block variant="outline" @click="$router.push('/finance/apply')">Apply for Credit</Button>
              <Button block variant="outline" @click="$router.push('/market/secondary')">Secondary Market</Button>
            </div>
          </Card>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import FinanceService from '../services/finance';
import api from '../services/api';
import { useConfigStore } from '../stores/config';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import Card from '../components/ui/Card.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import BankAccountManager from '../components/finance/BankAccountManager.vue';

const configStore = useConfigStore();
const profile = ref(null);
const agreements = ref([]);
const financeApps = ref([]);
const loading = ref(false);
const activeTab = ref('portfolio');

const tabs = computed(() => [
  { id: 'portfolio', label: 'Portfolio', count: agreements.value.length || null },
  { id: 'agreements', label: 'Agreements', count: agreements.value.length || null },
  { id: 'applications', label: 'Applications', count: financeApps.value.length || null },
  { id: 'accounts', label: 'Accounts', count: null },
]);

const totalCommitted = computed(() => {
  return agreements.value.reduce((sum, agr) => sum + (parseFloat(agr.amount) || 0), 0);
});

const pendingPledges = computed(() => {
  return agreements.value.filter(a => a.status === 'DRAFT').length;
});

const openApplications = computed(() => {
  return financeApps.value.filter(a => a.status === 'SUBMITTED').length;
});

onMounted(() => loadData());

async function loadData() {
  loading.value = true;
  try {
    const pRes = await FinanceService.getInvestorProfile();
    if (pRes.data && pRes.data.length > 0) {
      profile.value = pRes.data[0];
    } else if (pRes.data.results && pRes.data.results.length > 0) {
      profile.value = pRes.data.results[0];
    }

    const aRes = await FinanceService.listAgreements();
    agreements.value = aRes.data.results || aRes.data || [];

    const fRes = await FinanceService.listApplications();
    financeApps.value = fRes.data.results || fRes.data || [];
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function onboard() {
  try {
    await FinanceService.onboardInvestor({ jurisdiction: 'KE' });
    loadData();
  } catch (e) {
    console.error(e);
  }
}

async function sign(id) {
  try {
    await FinanceService.signAgreement(id);
    loadData();
  } catch (e) {
    console.error(e);
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatPrice(amount, sourceCurrency = 'KES') {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return 'KES 0.00';
  return configStore.formatPrice ? configStore.formatPrice(value, sourceCurrency) : `KES ${value.toLocaleString()}`;
}

function getAgreementVariant(s) {
  if (s === 'FUNDED') return 'success';
  if (s === 'SIGNED') return 'primary';
  if (s === 'DRAFT') return 'warning';
  return 'secondary';
}

function getAppVariant(s) {
  if (s === 'APPROVED' || s === 'DISBURSED') return 'success';
  if (s === 'SUBMITTED') return 'warning';
  if (s === 'REJECTED') return 'danger';
  return 'secondary';
}
</script>

<style scoped>
.pz-investor-page {
  min-height: 100vh;
  background-color: var(--pz-color-limestone-white);
}

.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--pz-color-concrete-grey);
}

.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
}

/* Hero */
.pz-investor-hero {
  background: #ffffff;
  border-radius: 24px;
  padding: 2rem 2.5rem;
  box-shadow:
    0 2px 4px rgba(10, 10, 15, 0.02),
    0 8px 16px rgba(10, 10, 15, 0.04),
    0 20px 40px rgba(10, 10, 15, 0.06);
  margin-bottom: 2rem;
}

.pz-investor-hero__content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pz-investor-hero__stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.pz-investor-stat {
  padding: 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(10, 10, 15, 0.06);
  display: grid;
  gap: 0.35rem;
}

.pz-investor-stat strong {
  font-family: var(--pz-font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

/* Layout */
.pz-investor-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.75rem;
}

.pz-investor-sidebar {
  position: sticky;
  top: 2rem;
  align-self: start;
  height: fit-content;
  display: grid;
  gap: 1rem;
}

/* Tabs */
.pz-investor-tabs {
  display: flex;
  gap: 0.4rem;
  overflow-x: auto;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  border: 1px solid rgba(10, 10, 15, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  width: fit-content;
  max-width: 100%;
}

.pz-investor-tabs::-webkit-scrollbar {
  display: none;
}

.pz-investor-tab {
  position: relative;
  padding: 0.7rem 1.1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pz-investor-tab:hover {
  color: var(--pz-color-structural-steel);
  background: rgba(10, 10, 15, 0.03);
}

.pz-investor-tab--active {
  background: white;
  color: var(--pz-color-earth-orange);
  box-shadow: 0 2px 8px rgba(10, 10, 15, 0.08);
}

.pz-investor-tab__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.4rem;
  height: 1.4rem;
  padding: 0 0.35rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
}

.pz-tab-panel {
  animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Detail components */
.pz-detail-stack {
  display: grid;
  gap: 0.75rem;
}

.pz-detail-subcard {
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-detail-subcard span:first-child {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-detail-subcard strong {
  display: block;
  margin-top: 0.15rem;
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

/* Agreement card */
.pz-agreement-card {
  padding: 1rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-agreement-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.pz-agreement-card__project {
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pz-agreement-card__meta {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.15rem;
}

.pz-agreement-card__amount {
  font-family: var(--pz-font-display);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--pz-color-earth-orange);
  white-space: nowrap;
}

.pz-agreement-card__terms {
  margin: 0.5rem 0 0;
  font-size: 0.85rem;
}

.pz-agreement-card__terms a {
  color: var(--pz-color-earth-orange);
  text-decoration: none;
}

.pz-agreement-card__terms a:hover {
  text-decoration: underline;
}

.pz-agreement-card__footer {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  align-items: center;
}

/* Empty state */
.pz-investor-empty {
  padding: 1.5rem 0;
  text-align: center;
}

.pz-investor-empty__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.5rem;
}

.pz-investor-empty p {
  margin: 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
}

/* Activity */
.pz-activity-list {
  display: grid;
  gap: 0.75rem;
}

.pz-activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-activity-item__icon {
  font-size: 1.2rem;
}

.pz-activity-item__content {
  flex: 1;
  display: grid;
  gap: 0.1rem;
}

.pz-activity-item__content strong {
  font-family: var(--pz-font-display);
  font-size: 0.9rem;
  font-weight: 600;
}

.pz-activity-item__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
}

.pz-activity-item__date {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

/* Utilities */
.pz-l-flex { display: flex; }
.pz-l-flex--justify-end { justify-content: flex-end; }
.pz-space-y-3 > * + * { margin-top: 0.75rem; }
.pz-space-y-6 > * + * { margin-top: 1.5rem; }
.pz-u-text-center { text-align: center; }
.pz-u-text-display { font-family: var(--pz-font-display); font-weight: 700; color: var(--pz-color-foundation-black); letter-spacing: -0.02em; line-height: 1.2; margin: 0; }
.pz-u-text-mono { font-family: var(--pz-font-mono); }
.pz-u-color-earth { color: var(--pz-color-earth-orange); }
.pz-u-color-steel { color: var(--pz-color-structural-steel); }
.pz-u-color-concrete { color: var(--pz-color-concrete-grey); }
.u-mt-4 { margin-top: 1rem; }
.u-py-20 { padding-top: 5rem; padding-bottom: 5rem; }
.u-mb-6 { margin-bottom: 1.5rem; }

.c-loader {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 2px solid rgba(10, 10, 15, 0.08);
  border-top-color: var(--pz-color-earth-orange);
  margin: 0 auto;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .pz-investor-hero__stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .pz-investor-layout {
    grid-template-columns: 1fr;
  }
  .pz-investor-sidebar {
    position: static;
  }
}

@media (max-width: 640px) {
  .pz-investor-hero {
    padding: 1.5rem;
  }
  .pz-investor-hero__stats {
    grid-template-columns: 1fr;
  }
}
</style>
