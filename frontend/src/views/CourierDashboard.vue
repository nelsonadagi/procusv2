<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="copper"
    title="Courier Command Hub"
    eyebrow="SECURE_IDENTITY: COURIER_NODE // SESSION: ACTIVE"
    signal-text="COURIER NETWORK ONLINE"
    :quickstats="[
      { label: 'Sections', value: navSections.length },
      { label: 'Status', value: courierProfile?.status || 'UNKNOWN' },
      { label: 'Mode', value: 'Carrier Ops' }
    ]"
    :sidebar-groups="[
      {
        title: 'Courier Capability',
        items: navSections.map(s => ({ id: s.id, label: s.label, icon: s.icon }))
      },
      {
        title: 'System Actions',
        items: [
          { id: 'exit', label: 'Exit Console', icon: '⇚', action: () => $router.push('/') }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div v-if="courierProfile" class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
        <div class="u-text-right u-hide-mobile">
          <div class="pz-u-text-mono font-bold text-sm">{{ courierProfile.company_name }}</div>
          <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ courierProfile.registration_number }}</div>
        </div>
        <Badge :variant="getStatusVariant(courierProfile.status)">{{ courierProfile.status }}</Badge>
      </div>
    </template>

    <div v-if="needsOnboarding" class="pz-onboarding-state">
      <div class="pz-onboarding-state__kicker">COURIER_PROFILE_REQUIRED</div>
      <h3 class="pz-onboarding-state__title">Your courier workspace needs a registry profile before dispatch can start.</h3>
      <p class="pz-onboarding-state__body">
        Begin with your company registration data. Once saved, pricing zones, API settings, and shipments will activate in this console.
      </p>
      <Badge variant="warning">PROFILE_SETUP_PENDING</Badge>
      <div class="u-mt-6">
        <CourierProfileSection @profile-updated="handleProfileUpdate" @show-alert="showAlert" />
      </div>
    </div>
    <component v-else :is="activeComponent" @profile-updated="handleProfileUpdate" @show-alert="showAlert" />
  </DashboardShell>
</template>

<script setup>
import { ref, onMounted, computed, defineAsyncComponent, provide } from 'vue';
import api from '../services/api';
import Badge from '../components/ui/Badge.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import { useNotificationStore } from '../stores/notifications';

const notificationStore = useNotificationStore();

const CourierProfileSection = defineAsyncComponent(() => import('../components/courier/CourierProfileSection.vue'));
const CourierPricingSection = defineAsyncComponent(() => import('../components/courier/CourierPricingSection.vue'));
const CourierApiSection = defineAsyncComponent(() => import('../components/courier/CourierApiSection.vue'));
const CourierShipmentsSection = defineAsyncComponent(() => import('../components/courier/CourierShipmentsSection.vue'));

const activeSection = ref('profile');
const courierProfile = ref(null);
const needsOnboarding = ref(false);

const navSections = [
  { id: 'profile', label: 'Company Profile', icon: '🏢' },
  { id: 'pricing', label: 'Pricing Zones', icon: '💲' },
  { id: 'api', label: 'API Configuration', icon: '🔌' },
  { id: 'shipments', label: 'Active Shipments', icon: '🚚' }
];

const activeComponent = computed(() => {
  switch (activeSection.value) {
    case 'profile': return CourierProfileSection;
    case 'pricing': return CourierPricingSection;
    case 'api': return CourierApiSection;
    case 'shipments': return CourierShipmentsSection;
    default: return CourierProfileSection;
  }
});

const showAlert = (message, type = 'info') => {
  const mappedType = type === 'error' ? 'ERROR' : (type === 'success' ? 'PAYMENT' : 'BID');
  notificationStore.addNotification({
    message,
    type: mappedType,
    timestamp: new Date().toISOString()
  });
};

provide('showAlert', showAlert);

async function fetchCourierProfile() {
  try {
    const res = await api.get('/logistics/couriers/me/');
    courierProfile.value = res.data;
    needsOnboarding.value = false;
  } catch (err) {
    if (err.response?.status === 404) {
      needsOnboarding.value = true;
      courierProfile.value = null;
      return;
    }
    console.error('Courier profile fetch error', err);
    showAlert('Courier profile could not be synchronized. Complete courier registration to activate this console.', 'error');
    courierProfile.value = null;
  }
}

function handleProfileUpdate(profile) {
  courierProfile.value = profile;
  needsOnboarding.value = false;
  showAlert('Profile updated successfully', 'success');
}

function getStatusVariant(status) {
  switch (status) {
    case 'APPROVED': return 'success';
    case 'PENDING': return 'warning';
    case 'REJECTED': return 'danger';
    default: return 'secondary';
  }
}

onMounted(() => {
  fetchCourierProfile();
});
</script>

<style scoped>
.pz-onboarding-state {
  display: grid;
  gap: 1rem;
  padding: clamp(1.5rem, 4vw, 2.5rem);
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(10, 10, 15, 0.12);
  box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.06);
}

.pz-onboarding-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-earth-orange);
}

.pz-onboarding-state__title {
  font-size: 1.35rem;
}

.pz-onboarding-state__body {
  max-width: 44rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
