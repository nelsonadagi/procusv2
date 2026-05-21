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

    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="courier-workflow-banner">
        <div class="courier-workflow-banner__summary">
          <div class="courier-workflow-banner__kicker">{{ workflowSummary.stage }}</div>
          <h2 class="courier-workflow-banner__title">{{ workflowSummary.title }}</h2>
          <p class="courier-workflow-banner__body">{{ workflowSummary.body }}</p>
        </div>
        <div class="courier-workflow-banner__actions">
          <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
            {{ workflowSummary.primaryAction.label }}
          </Button>
          <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
            {{ workflowSummary.secondaryAction.label }}
          </Button>
        </div>
      </div>
      <div class="courier-workflow-banner__steps">
        <div
          v-for="step in workflowSteps"
          :key="step.label"
          class="courier-workflow-step"
          :class="{ 'courier-workflow-step--done': step.done, 'courier-workflow-step--active': step.active }"
        >
          <span class="courier-workflow-step__index">{{ step.index }}</span>
          <div class="courier-workflow-step__content">
            <strong>{{ step.label }}</strong>
            <span>{{ step.help }}</span>
          </div>
        </div>
      </div>
    

    <ModuleCTA
      eyebrow="Delivery Services"
      title="Can your company handle site deliveries?"
      body="Register courier capacity, publish pricing zones, and connect delivery operations to material orders and site dispatch."
      primary-label="Set Up Courier Profile"
      primary-to="/courier/dashboard"
      secondary-label="Browse Materials"
      secondary-to="/products"
      tone="copper"
    />
</WorkflowGuide>

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
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
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

const workflowSummary = computed(() => {
  if (needsOnboarding.value) {
    return {
      stage: 'SETUP',
      title: 'Create the courier registry profile',
      body: 'Complete the company profile first. Until the registry is active, pricing, API, and shipments stay locked.',
      primaryAction: { label: 'Open Profile', handler: () => { activeSection.value = 'profile'; } },
      secondaryAction: null,
    };
  }

  if (!courierProfile.value || courierProfile.value.status !== 'APPROVED') {
    return {
      stage: courierProfile.value?.status || 'PENDING',
      title: 'Finish approval before dispatch work begins',
      body: 'The registry is present, but the account is not yet approved for live shipment handling.',
      primaryAction: { label: 'Open Profile', handler: () => { activeSection.value = 'profile'; } },
      secondaryAction: { label: 'View Shipments', handler: () => { activeSection.value = 'shipments'; } },
    };
  }

  return {
    stage: 'ACTIVE',
    title: 'Manage live courier operations',
    body: 'Use pricing zones, API settings, and the active shipment manifest to keep deliveries moving and visible.',
    primaryAction: { label: 'View Shipments', handler: () => { activeSection.value = 'shipments'; } },
    secondaryAction: { label: 'Open Pricing', handler: () => { activeSection.value = 'pricing'; } },
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Register the courier profile',
    help: 'Company identity and support contacts activate the console.',
    done: Boolean(courierProfile.value),
    active: needsOnboarding.value,
  },
  {
    index: '02',
    label: 'Get approved',
    help: 'Approval unlocks dispatch, pricing, and shipment handling.',
    done: courierProfile.value?.status === 'APPROVED',
    active: courierProfile.value?.status === 'PENDING',
  },
  {
    index: '03',
    label: 'Configure pricing and API',
    help: 'Set up zones and sync points before accepting active routes.',
    done: courierProfile.value?.status === 'APPROVED' && activeSection.value !== 'profile',
    active: activeSection.value === 'pricing' || activeSection.value === 'api',
  },
  {
    index: '04',
    label: 'Track active shipments',
    help: 'Use the shipment panel to monitor live delivery movement.',
    done: activeSection.value === 'shipments',
    active: activeSection.value === 'shipments',
  },
]);

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

.courier-workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.courier-workflow-banner__summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.courier-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.courier-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.courier-workflow-banner__body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.courier-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.courier-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.courier-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
}

.courier-workflow-step__index {
  display: inline-flex;
  width: 1.9rem;
  height: 1.9rem;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(247, 244, 239, 0.95);
  border: 1px solid rgba(10, 10, 15, 0.12);
  color: var(--pz-color-foundation-black);
  flex-shrink: 0;
}

.courier-workflow-step__content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.courier-workflow-step__content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.courier-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.courier-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.courier-workflow-step--done .courier-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.courier-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .courier-workflow-banner {
    grid-template-columns: 1fr;
  }

  .courier-workflow-banner__actions {
    justify-content: flex-start;
  }

  .courier-workflow-banner__steps {
    grid-template-columns: 1fr;
  }
}
</style>
