<template>
  <div class="pz-unified-hub">
    <div class="pz-l-container">
      <header class="pz-unified-hub__header">
        <div class="pz-unified-hub__signal">
          <span class="pz-unified-hub__signal-dot"></span>
          <span>UNIFIED CONTROL NODE ONLINE</span>
        </div>
        <h1 class="pz-u-text-display pz-unified-hub__title">Workspace Hub</h1>
        <p class="pz-u-text-mono text-xs pz-u-color-steel">
          Select an active workspace to continue operations.
        </p>
      </header>

      <section class="pz-unified-hub__grid">
        <router-link
          v-for="ws in activeWorkspaces"
          :key="ws.id"
          :to="ws.path"
          class="pz-hub-card"
          :class="`pz-hub-card--accent-${ws.accent}`"
        >
          <div class="pz-hub-card__meta">
            <span class="pz-hub-card__icon" aria-hidden="true">{{ ws.icon }}</span>
            <Badge v-if="ws.badge" :variant="ws.badgeVariant">{{ ws.badge }}</Badge>
          </div>
          <h3 class="pz-hub-card__title">{{ ws.label }}</h3>
          <p class="pz-hub-card__desc">{{ ws.description }}</p>
          <div class="pz-hub-card__action">
            <span>Open Workspace</span>
            <span aria-hidden="true">→</span>
          </div>
        </router-link>
      </section>

      <section v-if="activationWorkspaces.length" class="pz-unified-hub__activation">
        <h2 class="pz-u-text-mono text-sm pz-u-color-concrete u-mb-6">Activate Additional Workspaces</h2>
        <div class="pz-unified-hub__grid pz-unified-hub__grid--compact">
          <router-link
            v-for="ws in activationWorkspaces"
            :key="ws.id"
            :to="ws.path"
            class="pz-hub-card pz-hub-card--dim"
          >
            <div class="pz-hub-card__meta">
              <span class="pz-hub-card__icon" aria-hidden="true">🔒</span>
            </div>
            <h3 class="pz-hub-card__title">{{ ws.label }}</h3>
            <p class="pz-hub-card__desc">{{ ws.description }}</p>
            <div class="pz-hub-card__action">
              <span>Begin Activation</span>
              <span aria-hidden="true">→</span>
            </div>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import Badge from '../components/ui/Badge.vue';

const authStore = useAuthStore();

const activeWorkspaces = computed(() => {
  const items = [];
  items.push({
    id: 'buyer',
    label: 'Project Owner',
    description: 'Orders, quotes, addresses, and project oversight.',
    path: '/buyer/dashboard',
    icon: '🏗',
    accent: 'earth',
    badge: 'Base',
    badgeVariant: 'success'
  });
  if (authStore.hasRole('VENDOR')) {
    items.push({
      id: 'vendor',
      label: 'Vendor',
      description: 'Inventory, orders, quotes, and supply chain management.',
      path: '/vendor/dashboard',
      icon: '🏭',
      accent: 'copper',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.hasRole('CONTRACTOR')) {
    items.push({
      id: 'contractor',
      label: 'Contractor',
      description: 'Bids, contracts, crew management, and project execution.',
      path: '/contractor/dashboard',
      icon: '🔧',
      accent: 'steel',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.hasRole('PROPERTY_MANAGER')) {
    items.push({
      id: 'property',
      label: 'Property Manager',
      description: 'Listings, availability, leads, and appointments.',
      path: '/property-manager/dashboard',
      icon: '🏠',
      accent: 'earth',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.hasRole('INVESTOR')) {
    items.push({
      id: 'investor',
      label: 'Investor',
      description: 'Portfolio, agreements, and compliance vault.',
      path: '/investor/dashboard',
      icon: '◈',
      accent: 'savanna',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.hasRole('COURIER')) {
    items.push({
      id: 'courier',
      label: 'Courier',
      description: 'Shipments, pricing zones, and API configuration.',
      path: '/courier/dashboard',
      icon: '🚚',
      accent: 'copper',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.hasRole('GOVERNMENT')) {
    items.push({
      id: 'government',
      label: 'Government',
      description: 'Public tender access and procurement workflows.',
      path: '/government/dashboard',
      icon: '🏛',
      accent: 'earth',
      badge: 'Approved',
      badgeVariant: 'success'
    });
  }
  if (authStore.isAdmin) {
    items.push({
      id: 'admin',
      label: 'Admin',
      description: 'Platform control, verifications, and oversight.',
      path: '/admin',
      icon: '⚙',
      accent: 'earth',
      badge: 'Admin',
      badgeVariant: 'primary'
    });
  }
  return items;
});

const activationWorkspaces = computed(() => {
  const items = [];
  if (!authStore.hasRole('VENDOR')) {
    items.push({
      id: 'vendor-activation',
      label: 'Vendor Workspace',
      description: 'Sell materials and manage supply chain operations.',
      path: '/vendor/dashboard'
    });
  }
  if (!authStore.hasRole('CONTRACTOR')) {
    items.push({
      id: 'contractor-activation',
      label: 'Contractor Workspace',
      description: 'Bid on contracts and manage project execution.',
      path: '/contractor/dashboard'
    });
  }
  if (!authStore.hasRole('PROPERTY_MANAGER')) {
    items.push({
      id: 'property-activation',
      label: 'Property Manager Workspace',
      description: 'Manage property listings and appointments.',
      path: '/property-manager/dashboard'
    });
  }
  if (!authStore.hasRole('INVESTOR')) {
    items.push({
      id: 'investor-activation',
      label: 'Investor Workspace',
      description: 'Access investment agreements and portfolio tools.',
      path: '/investor/dashboard'
    });
  }
  if (!authStore.hasRole('COURIER')) {
    items.push({
      id: 'courier-activation',
      label: 'Courier Workspace',
      description: 'Manage shipments and delivery operations.',
      path: '/courier/dashboard'
    });
  }
  if (!authStore.hasRole('GOVERNMENT')) {
    items.push({
      id: 'government-activation',
      label: 'Government Workspace',
      description: 'Access public tenders and procurement tools.',
      path: '/government/dashboard'
    });
  }
  return items;
});
</script>

<style scoped>
.pz-unified-hub {
  min-height: 100vh;
  padding: var(--pz-space-8) 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(245, 243, 238, 0.9)),
    radial-gradient(circle at top right, rgba(212, 101, 42, 0.08), transparent 24%);
}

.pz-unified-hub__header {
  margin-bottom: var(--pz-space-8);
  padding: clamp(1.25rem, 3vw, 2rem);
  background: rgba(255, 255, 255, 0.78);
  border: 2px solid var(--pz-color-foundation-black);
  box-shadow: 14px 14px 0 rgba(10, 10, 15, 0.08);
}

.pz-unified-hub__signal {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
  margin-bottom: var(--pz-space-4);
}

.pz-unified-hub__signal-dot {
  width: 0.7rem;
  height: 0.7rem;
  background: var(--pz-color-earth-orange);
  border-radius: 999px;
  box-shadow: 0 0 0 4px rgba(212, 101, 42, 0.16);
}

.pz-unified-hub__title {
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 0.92;
  letter-spacing: -0.06em;
  margin: 0 0 var(--pz-space-2) 0;
}

.pz-unified-hub__grid {
  display: grid;
  gap: var(--pz-space-6);
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.pz-unified-hub__grid--compact {
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
}

.pz-unified-hub__activation {
  margin-top: var(--pz-space-12);
  padding-top: var(--pz-space-8);
  border-top: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-hub-card {
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-4);
  padding: var(--pz-space-6);
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.06);
  text-decoration: none;
  color: inherit;
  transition: all var(--pz-transition-spring);
}

.pz-hub-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 16px 16px 0 rgba(10, 10, 15, 0.1);
}

.pz-hub-card--dim {
  opacity: 0.75;
  border-style: dashed;
}

.pz-hub-card--dim:hover {
  opacity: 1;
  border-style: solid;
}

.pz-hub-card--accent-copper:hover {
  border-color: var(--pz-color-copper-circuit);
  box-shadow: 16px 16px 0 rgba(184, 115, 51, 0.15);
}

.pz-hub-card--accent-savanna:hover {
  border-color: var(--pz-color-savanna-green);
  box-shadow: 16px 16px 0 rgba(5, 150, 105, 0.15);
}

.pz-hub-card--accent-steel:hover {
  border-color: var(--pz-color-steel-blue);
  box-shadow: 16px 16px 0 rgba(37, 99, 235, 0.15);
}

.pz-hub-card__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pz-hub-card__icon {
  font-size: 1.5rem;
  line-height: 1;
}

.pz-hub-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.pz-hub-card__desc {
  font-size: 0.88rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
  flex: 1;
}

.pz-hub-card__action {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

@media (prefers-reduced-motion: reduce) {
  .pz-hub-card {
    transition: none;
  }
  .pz-hub-card:hover {
    transform: none;
  }
}
</style>
