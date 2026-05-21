<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="copper"
    title="Vendor Dashboard"
    :eyebrow="vendorProfile?.business_name || 'Merchant Operations'"
    signal-text="Vendor Dashboard"
    :quickstats="[
      { label: 'Sections', value: navSections.length },
      { label: 'Status', value: statusLabel },
      { label: 'Products', value: vendorProfile?.product_count ?? '-' }
    ]"
    :sidebar-groups="[
      {
        title: 'Workspace',
        items: [
          { id: 'inventory', label: '📦 Catalog', icon: '' },
          { id: 'quotes', label: '💬 Quotes', icon: '' },
          { id: 'orders', label: '📋 Orders', icon: '' },
          { id: 'profile', label: '⚙️ Account', icon: '' }
        ]
      },
      {
        title: 'Quick Actions',
        items: [
          { id: 'launch', label: '🚀 Launch', icon: '', action: () => { activeSection = 'inventory'; } },
          { id: 'exit', label: '⇚ Exit Dashboard', icon: '', action: () => $router.push('/') }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div v-if="vendorProfile" class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
        <div class="u-text-right u-hide-mobile">
          <div class="pz-u-text-mono font-bold text-sm">{{ vendorProfile.business_name }}</div>
          <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ vendorProfile.location }}</div>
        </div>
        <Badge :variant="vendorProfile.verified_status === 'APPROVED' ? 'success' : 'warning'">
          {{ vendorProfile.verified_status }}
        </Badge>
      </div>
    </template>

    <WorkflowGuide title="Vendor CTA" eyebrow="Action">
      <ModuleCTA
        eyebrow="Product Catalog"
        title="Ready to sell more materials?"
        body="Keep your vendor profile active, add products to the catalog, and make your stock visible to buyers requesting quotes."
        primary-label="List Product"
        primary-to="/vendor/dashboard"
        secondary-label="View Marketplace"
        secondary-to="/products"
        tone="earth"
      />
    </WorkflowGuide>

    <div v-if="needsOnboarding" class="pz-onboarding-state">
      <div class="pz-onboarding-state__kicker">Step 1 of 2</div>
      <h3 class="pz-onboarding-state__title">Complete your vendor profile to start selling.</h3>
      <p class="pz-onboarding-state__body">
        Tell us about your business so we can verify you as a supplier. Once approved, you'll be able to publish products and receive quote requests.
      </p>
      <Button variant="primary" @click="$router.push('/vendors/register')">Set Up Vendor Profile</Button>
    </div>

    <div v-else-if="isPendingApproval" class="pz-onboarding-state">
      <div class="pz-onboarding-state__kicker">Step 2 of 2 — Under Review</div>
      <h3 class="pz-onboarding-state__title">Your profile is being reviewed.</h3>
      <p class="pz-onboarding-state__body">
        Typical approval time is 1–2 business days. While you wait, you can prepare your product catalog using the CSV template so you're ready to publish immediately after approval.
      </p>
      <!-- Queue Position -->
      <div v-if="vendorProfile?.queue_position" class="pz-queue-position">
        <div class="pz-queue-position__number">#{{ vendorProfile.queue_position }}</div>
        <div class="pz-queue-position__label">in review queue</div>
        <div v-if="vendorProfile?.pending_hours" class="pz-queue-position__meta">
          Submitted {{ Math.floor(vendorProfile.pending_hours / 24) }}d {{ vendorProfile.pending_hours % 24 }}h ago
        </div>
      </div>
      <div class="pz-onboarding-state__actions">
        <Button variant="primary" :loading="downloadingTemplate" @click="downloadTemplate">Download CSV Template</Button>
        <Button variant="ghost" @click="activeSection = 'profile'">View My Profile</Button>
      </div>
      <div class="pz-onboarding-state__tips">
        <p>📋 What happens next: Our team reviews your business registration and delivery capability. You'll be notified by email and dashboard when approved.</p>
      </div>
    </div>

    <div v-else-if="isSuspended" class="pz-onboarding-state pz-onboarding-state--warning">
      <div class="pz-onboarding-state__kicker">Account Suspended</div>
      <h3 class="pz-onboarding-state__title">Your vendor account has been suspended.</h3>
      <p class="pz-onboarding-state__body">
        Your products are temporarily hidden from buyers. Please contact support for more information about reinstating your account.
      </p>
      <Button variant="primary" @click="$router.push('/support')">Contact Support</Button>
    </div>

    <VendorProfileSection v-else-if="activeSection === 'profile'" @profile-updated="handleProfileUpdate" @show-alert="showAlert" />
    <VendorInventorySection v-else-if="activeSection === 'inventory'" :vendor-status="vendorProfile?.verified_status" @show-alert="showAlert" @navigate="activeSection = $event" />
    <VendorOrdersSection v-else-if="activeSection === 'orders'" @show-alert="showAlert" />
    <VendorQuotesSection v-else-if="activeSection === 'quotes'" @show-alert="showAlert" @navigate="activeSection = $event" />

    <!-- Mobile Bottom Tab Bar -->
    <nav v-if="!needsOnboarding && !isPendingApproval && !isSuspended" class="pz-mobile-tab-bar" aria-label="Mobile navigation">
      <button
        v-for="tab in mobileTabs"
        :key="tab.id"
        class="pz-mobile-tab"
        :class="{ 'pz-mobile-tab--active': activeSection === tab.section }"
        @click="activeSection = tab.section"
      >
        <span class="pz-mobile-tab__icon">{{ tab.icon }}</span>
        <span class="pz-mobile-tab__label">{{ tab.label }}</span>
      </button>
    </nav>
  </DashboardShell>
</template>

<script setup>
import { ref, computed, onMounted, defineAsyncComponent, provide } from 'vue';
import api from '../services/api';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import { useNotificationStore } from '../stores/notifications';

const notificationStore = useNotificationStore();

const VendorProfileSection = defineAsyncComponent(() => import('../components/vendor/VendorProfileSection.vue'));
const VendorInventorySection = defineAsyncComponent(() => import('../components/vendor/VendorInventorySection.vue'));
const VendorOrdersSection = defineAsyncComponent(() => import('../components/vendor/VendorOrdersSection.vue'));
const VendorQuotesSection = defineAsyncComponent(() => import('../components/vendor/VendorQuotesSection.vue'));

const activeSection = ref('inventory');
const vendorProfile = ref(null);
const needsOnboarding = ref(false);
const downloadingTemplate = ref(false);

const statusLabel = computed(() => {
  const s = vendorProfile.value?.verified_status;
  if (s === 'APPROVED') return 'Verified';
  if (s === 'PENDING') return 'Under Review';
  if (s === 'REJECTED') return 'Not Approved';
  if (s === 'SUSPENDED') return 'Suspended';
  return needsOnboarding.value ? 'Not Registered' : 'Pending';
});

const isPendingApproval = computed(() => {
  return vendorProfile.value && vendorProfile.value.verified_status === 'PENDING';
});

const isSuspended = computed(() => {
  return vendorProfile.value && vendorProfile.value.verified_status === 'SUSPENDED';
});

const navSections = [
  { id: 'inventory', label: 'Supply Inventory', icon: '📦' },
  { id: 'orders', label: 'Logistics Orders', icon: '📋' },
  { id: 'quotes', label: 'Procurement Quotes', icon: '📝' },
  { id: 'profile', label: 'Operational Profile', icon: '👤' }
];

const mobileTabs = [
  { id: 'catalog', label: 'Catalog', icon: '📦', section: 'inventory' },
  { id: 'launch', label: 'Launch', icon: '🚀', section: 'inventory' },
  { id: 'quotes', label: 'Quotes', icon: '💬', section: 'quotes' },
  { id: 'insights', label: 'Insights', icon: '📊', section: 'inventory' },
  { id: 'account', label: 'Account', icon: '👤', section: 'profile' },
];

const showAlert = (message, type = 'info') => {
  const mappedType = type === 'error' ? 'ERROR' : (type === 'success' ? 'PAYMENT' : 'BID');
  notificationStore.addNotification({
    message,
    type: mappedType,
    timestamp: new Date().toISOString()
  });
};

provide('showAlert', showAlert);

async function fetchHeaderProfile() {
  try {
    const res = await api.get('/vendors/me/');
    vendorProfile.value = res.data;
    needsOnboarding.value = false;
  } catch (err) {
    if (err.response?.status === 403 || err.response?.status === 404) {
      vendorProfile.value = null;
      needsOnboarding.value = true;
      return;
    }
    console.error('Header profile fetch error', err);
  }
}

function handleProfileUpdate(profile) {
  vendorProfile.value = profile;
  showAlert('Profile updated successfully', 'success');
}

async function downloadTemplate() {
  downloadingTemplate.value = true;
  try {
    const res = await api.get('/v1/products/import-template/', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'product_import_template.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    showAlert('Failed to download template. Please try again.', 'error');
  } finally {
    downloadingTemplate.value = false;
  }
}

onMounted(() => {
  fetchHeaderProfile();
});
</script>

<style scoped>
.pz-onboarding-state {
  padding: clamp(1.5rem, 4vw, 2.5rem);
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(10, 10, 15, 0.12);
  box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.06);
}

.pz-onboarding-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-concrete-grey);
  text-transform: uppercase;
}

.pz-onboarding-state__title {
  margin: 0.7rem 0 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.4rem, 2.5vw, 2rem);
}

.pz-onboarding-state__body {
  max-width: 42rem;
  margin: 0.8rem 0 1.25rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.65;
}

.pz-onboarding-state__actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.pz-onboarding-state__tips {
  font-size: 0.8rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.6;
}

.pz-onboarding-state__tips p {
  margin: 0;
}

.pz-onboarding-state--warning {
  background: rgba(217, 119, 6, 0.06);
  border-color: rgba(217, 119, 6, 0.2);
}

/* Queue Position */
.pz-queue-position {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  padding: 0.75rem 1.25rem;
  background: rgba(247, 244, 239, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 12px;
  margin-bottom: 1rem;
}

.pz-queue-position__number {
  font-family: var(--pz-font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--pz-color-earth-orange);
}

.pz-queue-position__label {
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-queue-position__meta {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
}

/* Mobile Bottom Tab Bar */
.pz-mobile-tab-bar {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: white;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
  padding-bottom: env(safe-area-inset-bottom);
}

.pz-mobile-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  padding: 0.5rem 0.25rem;
  background: none;
  border: none;
  font-size: 0.65rem;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  transition: color 0.15s;
}

.pz-mobile-tab__icon {
  font-size: 1.25rem;
}

.pz-mobile-tab--active {
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

@media (max-width: 768px) {
  .pz-mobile-tab-bar {
    display: flex;
    justify-content: space-around;
  }
}
</style>
