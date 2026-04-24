<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="copper"
    title="Vendor Dashboard"
    :eyebrow="vendorProfile?.business_name || 'Merchant Operations'"
    signal-text="VENDOR COMMERCE GRID ONLINE"
    :quickstats="[
      { label: 'Sections', value: navSections.length },
      { label: 'Status', value: vendorProfile?.verified_status || (needsOnboarding ? 'ONBOARDING_REQUIRED' : 'PENDING') },
      { label: 'Mode', value: 'Supply Ops' }
    ]"
    :sidebar-groups="[
      {
        title: 'Merchant Dashboard',
        items: navSections.map(s => ({ id: s.id, label: s.label, icon: s.icon }))
      },
      {
        title: 'Actions',
        items: [
          { id: 'exit', label: 'Exit Dashboard', icon: '⇚', action: () => $router.push('/') }
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

    <div v-if="needsOnboarding" class="pz-onboarding-state">
      <div class="pz-onboarding-state__kicker">VENDOR_PROFILE_REQUIRED</div>
      <h3 class="pz-onboarding-state__title">Your vendor account still needs a supplier profile.</h3>
      <p class="pz-onboarding-state__body">
        Complete supplier onboarding before inventory, quote response, and fulfillment controls can be activated.
      </p>
      <Button variant="primary" @click="$router.push('/vendors/register')">Complete Vendor Onboarding</Button>
    </div>

    <VendorProfileSection v-else-if="activeSection === 'profile'" @profile-updated="handleProfileUpdate" @show-alert="showAlert" />
    <VendorInventorySection v-else-if="activeSection === 'inventory'" @show-alert="showAlert" />
    <VendorOrdersSection v-else-if="activeSection === 'orders'" @show-alert="showAlert" />
    <VendorQuotesSection v-else-if="activeSection === 'quotes'" @show-alert="showAlert" />
  </DashboardShell>
</template>

<script setup>
import { ref, onMounted, defineAsyncComponent, provide } from 'vue';
import api from '../services/api';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
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

const navSections = [
  { id: 'inventory', label: 'Supply Inventory', icon: '📦' },
  { id: 'orders', label: 'Logistics Orders', icon: '📋' },
  { id: 'quotes', label: 'Procurement Quotes', icon: '📝' },
  { id: 'profile', label: 'Operational Profile', icon: '👤' }
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
</style>
