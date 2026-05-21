<template>
  <section class="pz-module-cta" :class="[`pz-module-cta--${tone}`]">
    <div class="pz-module-cta__copy">
      <span class="pz-module-cta__eyebrow">{{ eyebrow }}</span>
      <h3>{{ resolvedTitle }}</h3>
      <p>{{ resolvedBody }}</p>
    </div>
    <div class="pz-module-cta__actions">
      <router-link v-if="resolvedPrimaryTo" :to="resolvedPrimaryTo" class="pz-module-cta__link">
        <Button variant="primary" size="sm">{{ resolvedPrimaryLabel }}</Button>
      </router-link>
      <router-link v-if="resolvedSecondaryTo" :to="resolvedSecondaryTo" class="pz-module-cta__link">
        <Button variant="outline" size="sm">{{ resolvedSecondaryLabel }}</Button>
      </router-link>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import Button from './Button.vue';
import { useAuthStore } from '../../stores/auth';

const props = defineProps({
  eyebrow: { type: String, default: 'Next Step' },
  title: { type: String, required: true },
  body: { type: String, required: true },
  primaryLabel: { type: String, required: true },
  primaryTo: { type: [String, Object], required: true },
  secondaryLabel: { type: String, default: '' },
  secondaryTo: { type: [String, Object], default: null },
  tone: { type: String, default: 'earth' }
});

const authStore = useAuthStore();

const roleDestinations = [
  {
    role: 'VENDOR',
    paths: ['/vendors/register', '/vendor/dashboard'],
    title: 'Ready to manage your vendor workspace?',
    body: 'Your account already has vendor access. Open the vendor workspace to list products, manage stock, and respond to buyer quote requests.',
    primaryLabel: 'Open Vendor Workspace',
    primaryTo: '/vendor/dashboard',
    secondaryLabel: 'View Marketplace',
    secondaryTo: '/products',
  },
  {
    role: 'CONTRACTOR',
    paths: ['/contractors/register', '/contractor/dashboard'],
    title: 'Ready to manage contractor opportunities?',
    body: 'Your contractor access is active. Open the contractor workspace to review tenders, manage bids, and track awarded work.',
    primaryLabel: 'Open Contractor Workspace',
    primaryTo: '/contractor/dashboard',
    secondaryLabel: 'Find Tenders',
    secondaryTo: '/contracts',
  },
  {
    role: 'PROPERTY_MANAGER',
    paths: ['/property-manager/dashboard', '/agent/dashboard', '/surveyor/dashboard'],
    title: 'Ready to manage your property workspace?',
    body: 'Your property workspace is available. Open it to update listings, manage inquiries, publish availability, and follow up on appointments.',
    primaryLabel: 'Open Property Workspace',
    primaryTo: '/property-manager/dashboard',
    secondaryLabel: 'Browse Properties',
    secondaryTo: '/properties',
  },
  {
    role: 'COURIER',
    paths: ['/courier/dashboard'],
    title: 'Ready to manage delivery operations?',
    body: 'Your courier workspace is available. Open it to manage courier profile, pricing zones, dispatch settings, and shipment activity.',
    primaryLabel: 'Open Courier Workspace',
    primaryTo: '/courier/dashboard',
    secondaryLabel: 'Browse Materials',
    secondaryTo: '/products',
  },
  {
    role: 'INVESTOR',
    paths: ['/investor/dashboard', '/finance/apply', '/market/secondary'],
    title: 'Ready to manage capital workflows?',
    body: 'Your investor access is active. Open the investor workspace to review opportunities, applications, agreements, and portfolio activity.',
    primaryLabel: 'Open Investor Workspace',
    primaryTo: '/investor/dashboard',
    secondaryLabel: 'Discover Projects',
    secondaryTo: '/projects',
  },
  {
    role: 'GOVERNMENT',
    paths: ['/government/dashboard'],
    title: 'Ready to review public procurement?',
    body: 'Your government workspace is available. Open it to review tender access, procurement guidance, and public opportunity workflows.',
    primaryLabel: 'Open Government Workspace',
    primaryTo: '/government/dashboard',
    secondaryLabel: 'View Tenders',
    secondaryTo: '/tenders',
  },
];

function pathOf(value) {
  return typeof value === 'string' ? value : value?.path || '';
}

const activeOverride = computed(() => {
  if (!authStore.isAuthenticated) return null;
  const routePaths = [pathOf(props.primaryTo), pathOf(props.secondaryTo)].filter(Boolean);
  return roleDestinations.find((item) => (
    authStore.hasRole(item.role) && routePaths.some((path) => item.paths.includes(path))
  )) || null;
});

const resolvedTitle = computed(() => activeOverride.value?.title || props.title);
const resolvedBody = computed(() => activeOverride.value?.body || props.body);
const resolvedPrimaryLabel = computed(() => activeOverride.value?.primaryLabel || props.primaryLabel);
const resolvedPrimaryTo = computed(() => activeOverride.value?.primaryTo || props.primaryTo);
const resolvedSecondaryLabel = computed(() => activeOverride.value?.secondaryLabel || props.secondaryLabel);
const resolvedSecondaryTo = computed(() => activeOverride.value?.secondaryTo || props.secondaryTo);
</script>

<style scoped>
.pz-module-cta {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0 0;
  padding: 1rem 1.05rem;
  border: 1px solid rgba(212, 101, 42, 0.34);
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(255, 249, 239, 0.98), rgba(255, 255, 255, 0.94)),
    var(--color-white, #fff);
  box-shadow: 0 12px 28px rgba(212, 101, 42, 0.16);
}

.pz-module-cta::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 0.28rem;
  background: var(--pz-color-earth-orange);
}

.pz-module-cta::after {
  content: "";
  position: absolute;
  top: -2.2rem;
  right: -2rem;
  width: 5.4rem;
  height: 5.4rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.12);
  pointer-events: none;
}

.pz-module-cta--steel {
  border-color: rgba(71, 91, 112, 0.34);
}

.pz-module-cta--steel::before {
  background: var(--pz-color-structural-steel, #52616b);
}

.pz-module-cta--savanna {
  border-color: rgba(178, 116, 48, 0.38);
}

.pz-module-cta--savanna::before {
  background: var(--pz-color-savanna-green, #7f8b52);
}

.pz-module-cta--copper {
  border-color: rgba(151, 94, 62, 0.38);
}

.pz-module-cta--copper::before {
  background: #975e3e;
}

.pz-module-cta__copy {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.pz-module-cta__eyebrow {
  display: block;
  margin-bottom: 0.25rem;
  color: #9a3f17;
  font-family: var(--pz-font-mono, monospace);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

.pz-module-cta h3 {
  margin: 0;
  color: var(--pz-color-foundation-black, #1f261f);
  font-size: 1.08rem;
  line-height: 1.25;
}

.pz-module-cta p {
  margin: 0.35rem 0 0;
  max-width: 58rem;
  color: #374151;
  font-size: 0.9rem;
  line-height: 1.5;
}

.pz-module-cta__actions {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.pz-module-cta__link {
  position: relative;
  display: inline-flex;
  text-decoration: none;
}

.pz-module-cta__link:first-child {
  filter: drop-shadow(0 10px 18px rgba(212, 101, 42, 0.26));
}

.pz-module-cta__link:first-child::after {
  content: "";
  position: absolute;
  inset: -0.35rem;
  z-index: -1;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.18);
  opacity: 0.75;
  transform: scale(0.92);
  animation: pz-cta-pulse 2.6s ease-in-out infinite;
}

.pz-module-cta__link :deep(button) {
  min-height: 2.45rem;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0;
  transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
}

.pz-module-cta__link:first-child :deep(button) {
  border-color: rgba(212, 101, 42, 0.82);
  background:
    linear-gradient(135deg, #f47a37 0%, #d4652a 52%, #9b4d22 100%) !important;
  color: #fff !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.24),
    0 12px 22px rgba(212, 101, 42, 0.28);
}

.pz-module-cta__link:first-child :deep(button)::after {
  content: " ->";
  font-weight: 900;
}

.pz-module-cta__link:hover :deep(button),
.pz-module-cta__link:focus-visible :deep(button) {
  transform: translateY(-2px);
  filter: saturate(1.08);
}

.pz-module-cta__link:first-child:hover :deep(button),
.pz-module-cta__link:first-child:focus-visible :deep(button) {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.28),
    0 16px 28px rgba(212, 101, 42, 0.36);
}

.pz-module-cta__link:focus-visible {
  outline: 3px solid rgba(212, 101, 42, 0.36);
  outline-offset: 4px;
  border-radius: 999px;
}

@keyframes pz-cta-pulse {
  0%,
  100% {
    opacity: 0.45;
    transform: scale(0.92);
  }

  50% {
    opacity: 0.9;
    transform: scale(1.04);
  }
}

@media (max-width: 720px) {
  .pz-module-cta {
    grid-template-columns: 1fr;
  }

  .pz-module-cta__actions {
    justify-content: flex-start;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pz-module-cta__link:first-child::after,
  .pz-module-cta__link :deep(button) {
    animation: none;
    transition: none;
  }
}
</style>
