<template>
  <div class="buyer-dashboard-page">
    <DashboardShell
    v-model:active-section="activeSection"
    accent="earth"
    title="Buyer Dashboard"
    eyebrow="MANAGE ORDERS & QUOTES"
    signal-text="BUYER WORKFLOW ONLINE"
    :quickstats="[
      { label: 'Orders', value: orders.length },
      { label: 'Quotes', value: quotes.length },
      { label: 'Hubs', value: addresses.length }
    ]"
    :sidebar-groups="[
      {
        title: 'Shopping Operations',
        items: [
          { id: 'orders', label: 'My Orders', icon: '📦' },
          { id: 'quotes', label: 'Quote Requests', icon: '📝' },
          { id: 'addresses', label: 'Delivery Addresses', icon: '📍' },
          { id: 'profile', label: 'My Profile', icon: '👤' }
        ]
      }
    ]"
  >
    <template #headerActions>
      <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
        <div class="u-text-right u-hide-mobile">
          <div class="pz-u-text-mono font-bold">{{ buyerIdentityLabel }}</div>
          <div class="pz-u-text-uppercase text-xs pz-u-color-earth">{{ userRole }}</div>
        </div>
        <Badge variant="primary">{{ userRole }}</Badge>
      </div>
    </template>

    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="buyer-workflow-banner">
        <div class="buyer-workflow-banner__summary">
          <div class="buyer-workflow-banner__kicker">{{ workflowSummary.stage }}</div>
          <h2 class="buyer-workflow-banner__title">{{ workflowSummary.title }}</h2>
          <p class="buyer-workflow-banner__body">{{ workflowSummary.body }}</p>
        </div>
        <div class="buyer-workflow-banner__actions">
          <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
            {{ workflowSummary.primaryAction.label }}
          </Button>
          <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
            {{ workflowSummary.secondaryAction.label }}
          </Button>
        </div>
      </div>
      <div class="buyer-workflow-banner__steps">
        <div
          v-for="step in workflowSteps"
          :key="step.label"
          class="buyer-workflow-step"
          :class="{ 'buyer-workflow-step--done': step.done, 'buyer-workflow-step--active': step.active }"
        >
          <span class="buyer-workflow-step__index">{{ step.index }}</span>
          <div class="buyer-workflow-step__content">
            <strong>{{ step.label }}</strong>
            <span>{{ step.help }}</span>
          </div>
        </div>
      </div>
    

    <ModuleCTA
      eyebrow="Supplier Path"
      title="Buying today, but also have materials to sell?"
      body="Activate vendor onboarding from the same account, publish your catalog, and keep buyer orders separate from supplier quotes."
      primary-label="Become a Vendor"
      primary-to="/vendors/register"
      secondary-label="Open Vendor Workspace"
      secondary-to="/vendor/dashboard"
      tone="earth"
    />
</WorkflowGuide>

    <!-- ORDERS SECTION -->
    <div v-if="activeSection === 'orders'">
      <Card title="My Orders">
        <template #header>
          <Button variant="outline" size="sm" @click="fetchData">Refresh</Button>
        </template>

        <div v-if="loading" class="u-py-8">
          <SkeletonTable :columns="5" :rows="4" />
        </div>
        <EmptyState
          v-else-if="orders.length === 0"
          icon="📦"
          title="No orders yet"
          description="No paid or confirmed orders exist yet."
          next-step="Browse the marketplace, request quotes, and accept a response to create your first order."
          action-label="Browse Marketplace"
          action-variant="primary"
          @action="$router.push('/')"
        >
        </EmptyState>
        <div v-else class="c-table-container pz-table-shell">
          <table class="c-table">
            <thead class="c-table__head">
              <tr>
                <th class="c-table__th">Order ID</th>
                <th class="c-table__th">Vendor</th>
                <th class="c-table__th">Amount</th>
                <th class="c-table__th">Status</th>
                <th class="c-table__th u-text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="c-table__tr c-table__tr--hover">
                <td class="c-table__td c-table__td--mono">#{{ order.id }}</td>
                <td class="c-table__td">{{ order.vendor_name }}</td>
                <td class="c-table__td c-table__td--bold">{{ configStore.formatPrice(order.total_amount, order.currency || 'KES') }}</td>
                <td class="c-table__td">
                  <div class="l-flex l-flex--gap-2">
                    <Badge :variant="getPaymentBadgeVariant(order.payment_status)">{{ order.payment_status }}</Badge>
                    <Badge :variant="getStatusBadgeVariant(order.status)">{{ order.status }}</Badge>
                  </div>
                </td>
                <td class="c-table__td">
                  <div class="c-table__actions">
                    <Button v-if="order.status === 'DELIVERED'" variant="success" size="sm" @click="confirmDelivery(order.id)">Confirm</Button>
                    <Button v-if="order.status === 'COMPLETED'" variant="secondary" size="sm" @click="openRateModal(order)">Rate</Button>
                    <Button v-if="['PLACED', 'CONFIRMED'].includes(order.status)" variant="danger" size="sm" @click="cancelOrder(order.id)">Cancel</Button>
                    <Button v-if="order.payment_status !== 'PAID' && order.status !== 'CANCELLED'" variant="primary" size="sm" @click="simulatePayment(order)">Simulate Payment</Button>
                    <Button v-if="order.status === 'SHIPPED' || (order.tracking_number && order.tracking_number !== '')" variant="primary" size="sm" @click="openTracking(order.tracking_number)">Track Delivery</Button>
                    <Button variant="outline" size="sm" @click="openChat('order', order.id)">Chat</Button>
                    <Button variant="outline" size="sm" @click="openDisputeModal(order)">Dispute</Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- QUOTES SECTION -->
    <div v-if="activeSection === 'quotes'">
      <Card title="Quote Requests">
        <div v-if="loading" class="u-py-8">
          <SkeletonCard v-for="n in 3" :key="n" />
        </div>
        <EmptyState
          v-else-if="quotes.length === 0"
          icon="📝"
          title="No quote requests"
          description="No quote requests have been sent from this account yet."
          next-step="Request a quote from the marketplace so vendors can respond with pricing and delivery terms."
          action-label="Find Materials"
          action-variant="primary"
          @action="$router.push('/')"
        >
        </EmptyState>
        <div v-else class="pz-quote-list">
          <div v-for="quote in quotes" :key="quote.id" class="pz-quote-card">
            <div class="pz-quote-card__header">
              <div class="pz-quote-card__id">Request #{{ quote.id }}</div>
              <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'">{{ quote.status }}</Badge>
            </div>
            <div class="pz-quote-card__items">
              <div v-for="item in quote.items" :key="item.id">• {{ item.quantity }}x {{ item.product_name || item.product_details?.name || 'Material item' }}</div>
            </div>
            <div v-if="quote.responses && quote.responses.length > 0">
              <h4 class="pz-quote-card__responses-title">Vendor Responses</h4>
              <div class="pz-quote-response-list">
                <div v-for="resp in quote.responses" :key="resp.id" class="pz-quote-response" :class="{ 'pz-quote-response--ordered': resp.has_order }">
                  <div>
                    <div class="pz-quote-response__vendor">{{ resp.vendor_name || `Vendor #${resp.vendor}` }}</div>
                    <div class="pz-quote-response__price">{{ configStore.formatPrice(resp.confirmed_price, resp.quote_currency || resp.currency || 'KES') }} + {{ configStore.formatPrice(resp.delivery_fee, resp.quote_currency || resp.currency || 'KES') }} delivery</div>
                  </div>
                  <div v-if="resp.has_order" class="pz-quote-response__ordered">
                    <Badge variant="success">✓ Order #{{ resp.order_id }} Placed</Badge>
                    <Button size="sm" variant="outline" @click="activeSection = 'orders'">View Order</Button>
                  </div>
                  <Button v-else size="sm" variant="primary" @click="openCheckoutModal(quote, resp)">Accept & Checkout</Button>
                </div>
              </div>
            </div>
            <div v-else class="pz-quote-card__waiting">Awaiting vendor responses...</div>
          </div>
        </div>
      </Card>
    </div>

    <!-- ADDRESSES SECTION -->
    <div v-if="activeSection === 'addresses'">
      <div class="pz-l-grid pz-l-grid--md-cols-12 pz-l-grid--gap-8">
        <div class="pz-l-grid__col-md-7">
          <div class="flex justify-between items-center mb-6">
            <h2 class="pz-u-text-display text-xl">Delivery Hubs</h2>
            <Button variant="primary" size="sm" @click="openAddressModal">+ Add Delivery Hub</Button>
          </div>
          <div v-if="loading" class="grid grid-cols-1 gap-4">
            <SkeletonCard v-for="n in 2" :key="n" />
          </div>
          <EmptyState
            v-else-if="addresses.length === 0"
            icon="📍"
            title="No delivery hubs"
            description="No delivery locations have been saved for this buyer profile."
            next-step="Add a construction site or warehouse so vendors can deliver materials without delay."
            action-label="Add First Hub"
            action-variant="primary"
            @action="openAddressModal"
          >
          </EmptyState>
          <div v-else class="grid grid-cols-1 gap-4">
            <Card v-for="addr in addresses" :key="addr.id" class="relative hover:shadow-md transition-shadow">
              <div v-if="addr.is_default" class="absolute top-4 right-4">
                <Badge variant="success">Default Address</Badge>
              </div>
              <h4 class="pz-u-text-mono font-bold mb-2">{{ addr.name.toUpperCase() }}</h4>
              <p class="pz-u-text-mono text-xs pz-u-color-concrete mb-4">{{ addr.address_line_1 }}<br />{{ addr.city.toUpperCase() }}, {{ addr.country.toUpperCase() }}</p>
              <Button variant="danger" size="sm" @click="deleteAddress(addr.id)">Delete</Button>
            </Card>
          </div>
        </div>
        <div class="pz-l-grid__col-md-5">
          <LogisticsCalculator />
        </div>
      </div>
    </div>

    <!-- PROFILE SECTION -->
    <div v-if="activeSection === 'profile' && !isGuest">
      <Card title="My Profile" class="max-w-2xl">
        <form @submit.prevent="updateProfile" class="l-grid l-grid--cols-1 l-grid--gap-4">
          <div class="l-grid l-grid--cols-2 l-grid--gap-4">
            <PzInput v-model="profile.first_name" label="First Name" required />
            <PzInput v-model="profile.last_name" label="Last Name" required />
          </div>
          <PzInput v-model="profile.phone" label="Phone Number" placeholder="+254..." />

          <div class="pz-input-wrapper">
            <label class="pz-input__label">Approved Workspace Access</label>
            <div class="pz-profile-role-panel">
              <div class="pz-profile-role-panel__row">
                <span class="pz-profile-role-panel__label">Primary role</span>
                <strong>{{ profile.role || 'PROJECT_OWNER' }}</strong>
              </div>
              <div class="pz-profile-role-panel__row">
                <span class="pz-profile-role-panel__label">Additional approved roles</span>
                <span>{{ approvedRoleSummary }}</span>
              </div>
            </div>
            <span class="pz-input__hint">Use the activation cards below to begin specialized onboarding. Admin approval grants additional roles when those workflows are approved.</span>
          </div>

          <div class="pz-input-wrapper">
            <label class="pz-input__label">Work Region</label>
            <select v-model="profile.profile.preferred_region" class="pz-input">
              <option value="NAIROBI">Nairobi Area</option>
              <option value="MOMBASA">Mombasa Area</option>
              <option value="KISUMU">Kisumu Area</option>
            </select>
          </div>

          <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pt-4">
            <p class="pz-u-text-mono text-xs pz-u-color-steel">LAST SYNCED: JUST NOW</p>
            <Button type="submit" variant="primary">Save Changes</Button>
          </div>
        </form>
      </Card>

      <Card title="Role Activation" class="max-w-2xl u-mt-6">
        <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
          <button v-for="hub in onboardingHubs" :key="hub.label" type="button" class="pz-role-launcher" @click="$router.push(hub.path)">
            <div class="pz-role-launcher__eyebrow">{{ hub.kicker }}</div>
            <div class="pz-role-launcher__title">{{ hub.label }}</div>
            <div class="pz-role-launcher__body">{{ hub.body }}</div>
          </button>
        </div>
      </Card>
    </div>

    <div v-else-if="activeSection === 'profile' && isGuest">
      <Card title="Buyer Access" class="max-w-2xl">
        <div class="pz-guest-panel">
          <div class="pz-guest-panel__title">You are browsing as a buyer.</div>
          <p class="pz-guest-panel__body">
            Sign in to save your profile, delivery hubs, quote requests, and order history. Until then, browse the marketplace and use the buyer dashboard as your main workspace.
          </p>
          <div class="pz-guest-panel__actions">
            <Button variant="primary" @click="$router.push('/login')">Sign In</Button>
            <Button variant="outline" @click="$router.push('/')">Browse Marketplace</Button>
          </div>
        </div>
      </Card>
    </div>
    </DashboardShell>

    <!-- Rate Modal -->
    <Modal :isOpen="showRateModal" title="Rate Vendor" size="md" @close="showRateModal = false">
    <div class="text-center mb-4">
      <p class="mb-2">How was your experience with order #{{ selectedOrder?.id }}?</p>
      <div class="flex justify-center gap-2">
        <button v-for="i in 5" :key="i" type="button" :class="['text-2xl focus:outline-none transition-colors', newRating.score >= i ? 'text-yellow-400' : 'text-gray-300']" @click="newRating.score = i">★</button>
      </div>
    </div>
    <textarea v-model="newRating.comment" class="form-input w-full" rows="3" placeholder="Leave a review..."></textarea>
    <template #footer>
      <Button variant="outline" @click="showRateModal = false">Cancel</Button>
      <Button @click="submitRating" variant="primary">Submit Review</Button>
    </template>
    </Modal>

    <!-- Address Modal -->
    <Modal :isOpen="showAddressModal" title="Add Delivery Hub" size="lg" @close="showAddressModal = false">
    <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
      <form id="addr-form" @submit.prevent="saveAddress" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
        <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Hub Identification</div>
        <PzInput v-model="newAddress.name" label="Hub Name" placeholder="e.g. Site Alpha / Warehouse" required />
        <PzInput v-model="newAddress.address_line_1" label="Street Address" required />
        <div class="pz-l-grid pz-l-grid--cols-2 pz-l-grid--gap-4">
          <PzInput v-model="newAddress.city" label="City" required />
          <PzInput v-model="newAddress.country" label="Country" required />
        </div>
        <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-border-radius-sm mt-4">
          <label class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 pz-u-text-mono text-sm cursor-pointer">
            <input v-model="newAddress.is_default" type="checkbox" class="pz-checkbox">
            <span>Set as default operational hub</span>
          </label>
        </div>
      </form>
      <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
        <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Map Location</div>
        <div class="pz-u-border pz-p-2 pz-u-bg-limestone" style="min-height: 380px;">
          <LocationInterface v-model="hubLocationState" @change="handleHubLocationChange" />
        </div>
        <div class="pz-u-text-mono text-[10px] pz-u-color-concrete">GPS: {{ newAddress.latitude || '0.0000' }}N, {{ newAddress.longitude || '0.0000' }}E</div>
      </div>
    </div>
    <template #footer>
      <Button variant="outline" @click="showAddressModal = false">Cancel</Button>
      <Button type="submit" form="addr-form" variant="primary">Save Hub</Button>
    </template>
    </Modal>

    <!-- Tracking Modal -->
    <Modal :isOpen="showTrackingModal" title="Tracking Details" size="xl" @close="showTrackingModal = false">
      <LogisticsTracker :trackingNumber="activeTrackingNumber" />
    </Modal>

    <!-- Chat Modal -->
    <Modal :isOpen="showChatModal" title="Message Vendor" size="lg" @close="showChatModal = false">
      <ChatWindow v-if="activeChatRoomId" :roomId="String(activeChatRoomId)" />
    </Modal>

    <!-- Confirm Modal -->
    <Modal :isOpen="showActionConfirm" :title="confirmActionTitle" size="sm" @close="closeActionConfirm">
    <div class="pz-confirm-panel">
      <p class="pz-confirm-panel__title">{{ confirmActionMessage }}</p>
      <p class="pz-confirm-panel__body">This action updates the order workflow immediately and may affect dispatch or fulfillment.</p>
    </div>
    <template #footer>
      <Button variant="outline" @click="closeActionConfirm">Cancel</Button>
      <Button variant="primary" :loading="confirmActionLoading" @click="confirmAction">Continue</Button>
    </template>
    </Modal>

    <!-- Checkout Modal -->
    <Modal :isOpen="showCheckoutModal" title="Choose Payment Method" size="lg" @close="closeCheckoutModal">
    <div class="pz-checkout-modal">
      <div class="pz-checkout-modal__summary">
        <div>
          <div class="pz-checkout-modal__eyebrow">Quote Response</div>
          <h3>Accept and place the order</h3>
          <p>Choose a configured gateway. This demo creates a simulated payment record for the selected method.</p>
        </div>
        <div class="pz-checkout-modal__amount">
          <span>Total</span>
          <strong>{{ selectedCheckoutResponse ? configStore.formatPrice(Number(selectedCheckoutResponse.confirmed_price || 0) + Number(selectedCheckoutResponse.delivery_fee || 0), selectedCheckoutResponse.quote_currency || selectedCheckoutResponse.currency || 'KES') : '—' }}</strong>
        </div>
      </div>

      <div class="pz-checkout-methods">
        <div v-if="paymentMethods.length === 0" class="pz-checkout-methods__empty">
          No active payment methods configured yet.
        </div>
        <button
          v-for="method in paymentMethods"
          :key="method.id"
          type="button"
          class="pz-checkout-method"
          :class="{ 'pz-checkout-method--active': selectedPaymentProvider === method.provider }"
          @click="selectedPaymentProvider = method.provider"
        >
          <div class="pz-checkout-method__top">
            <strong>{{ method.label }}</strong>
            <Badge :variant="method.is_test_mode ? 'warning' : 'success'">{{ method.is_test_mode ? 'Test' : 'Live' }}</Badge>
          </div>
          <div class="pz-checkout-method__meta">{{ method.provider }}</div>
          <div class="pz-checkout-method__copy">{{ method.instructions || 'No instructions configured.' }}</div>
          <div class="pz-checkout-method__meta">{{ (method.enabled_regions || []).join(', ') || 'All regions' }}</div>
        </button>
      </div>

      <div class="pz-checkout-modal__footnote">
        <span>Default method:</span>
        <strong>{{ defaultPaymentLabel || 'No default configured' }}</strong>
      </div>
    </div>
    <template #footer>
      <Button variant="outline" @click="closeCheckoutModal">Cancel</Button>
      <Button variant="primary" :loading="checkoutLoading" :disabled="!selectedPaymentProvider || paymentMethods.length === 0" @click="confirmCheckout">Place Order</Button>
    </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, provide } from 'vue';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import { useNotificationStore } from '../stores/notifications';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import Modal from '../components/ui/Modal.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import SkeletonCard from '../components/ui/SkeletonCard.vue';
import SkeletonTable from '../components/ui/SkeletonTable.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import PzInput from '../components/PzInput.vue';
import LogisticsCalculator from '../components/logistics/LogisticsCalculator.vue';
import LogisticsTracker from '../components/logistics/LogisticsTracker.vue';
import LocationInterface from '../components/ui/LocationInterface.vue';
import ChatWindow from '../components/chat/ChatWindow.vue';

const authStore = useAuthStore();
const configStore = useConfigStore();
const notificationStore = useNotificationStore();

const activeSection = ref('orders');
const orders = ref([]);
const quotes = ref([]);
const paymentMethods = ref([]);
const addresses = ref([]);
const profile = ref({ profile: {} });
const loading = ref(true);
const checkoutLoading = ref(false);
const showCheckoutModal = ref(false);
const selectedCheckoutQuote = ref(null);
const selectedCheckoutResponse = ref(null);
const selectedPaymentProvider = ref('');

const isGuest = computed(() => !authStore.isAuthenticated);
const userRole = computed(() => (isGuest.value ? 'Buyer' : authStore.user?.role || 'User'));
const buyerIdentityLabel = computed(() => {
  if (isGuest.value) return 'Guest Buyer';
  const first = authStore.user?.first_name || '';
  const last = authStore.user?.last_name || '';
  return `${first} ${last}`.trim() || authStore.user?.email || 'Buyer Account';
});
const approvedRoleSummary = computed(() => {
  if (profile.value.role === 'ADMIN') return 'Admin accounts do not carry additional non-admin roles.';
  const roles = profile.value.roles || [];
  return roles.length ? roles.join(', ') : 'No additional approved roles yet.';
});
const defaultPaymentLabel = computed(() => {
  const method = paymentMethods.value.find((item) => item.provider === selectedPaymentProvider.value)
    || paymentMethods.value.find((item) => item.is_default)
    || paymentMethods.value[0];
  return method ? method.label : '';
});

const onboardingHubs = [
  { label: 'Owner Workspace', path: '/owner/dashboard', kicker: 'PROJECT_OWNER', body: 'Create projects, track updates, and manage owner-side execution.' },
  { label: 'Vendor Workspace', path: '/vendor/dashboard', kicker: 'VENDOR', body: 'Complete supplier onboarding, then manage inventory, quotes, and orders.' },
  { label: 'Contractor Workspace', path: '/contractor/dashboard', kicker: 'CONTRACTOR', body: 'Submit your contractor profile, then bid on tenders and track jobs.' },
  { label: 'Investor Workspace', path: '/investor/dashboard', kicker: 'INVESTOR', body: 'Initialize investor compliance onboarding and review agreements.' },
  { label: 'Property Manager Workspace', path: '/property-manager/dashboard', kicker: 'PROPERTY_MANAGER', body: 'Manage property listings, availability, and visitor appointments.' },
  { label: 'Agent Workspace', path: '/agent/dashboard', kicker: 'REAL_ESTATE_AGENT', body: 'List and sell properties, manage inquiries, and coordinate viewings.' },
  { label: 'Surveyor Workspace', path: '/surveyor/dashboard', kicker: 'SURVEYOR', body: 'Conduct property valuations, verify ownership, and assess condition.' },
  { label: 'Courier Workspace', path: '/courier/dashboard', kicker: 'COURIER', body: 'Register your courier company profile and activate logistics operations.' },
  { label: 'Government Workspace', path: '/government/dashboard', kicker: 'GOVERNMENT', body: 'Review public tender access and government procurement guidance.' }
];

const workflowSummary = computed(() => {
  if (loading.value) {
    return {
      stage: 'SYNCING',
      title: 'Loading buyer activity',
      body: 'Fetching your orders, quote requests, delivery hubs, and payment methods so the next action is visible right away.',
      primaryAction: null,
      secondaryAction: null,
    };
  }

  if (isGuest.value) {
    return {
      stage: 'BROWSE',
      title: 'Start as a buyer',
      body: 'Browse materials and properties as a buyer. Sign in when you want to save delivery hubs, quote requests, and order history.',
      primaryAction: { label: 'Sign In', handler: () => { window.location.href = '/login'; } },
      secondaryAction: { label: 'Browse Marketplace', handler: () => { window.location.href = '/'; } },
    };
  }

  if (!addresses.value.length) {
    return {
      stage: 'SETUP',
      title: 'Add a delivery hub first',
      body: 'Saved addresses unlock checkout, vendor delivery, and shipping tracking. Add one site or warehouse before placing your next order.',
      primaryAction: { label: 'Add Delivery Hub', handler: openAddressModal },
      secondaryAction: { label: 'Browse Marketplace', handler: () => { window.location.href = '/'; } },
    };
  }

  if (!quotes.value.length) {
    return {
      stage: 'REQUESTS',
      title: 'Request quotes before placing orders',
      body: 'Quote requests let vendors respond with pricing and delivery terms. Accept a quote to create the order and start payment.',
      primaryAction: { label: 'Browse Marketplace', handler: () => { window.location.href = '/'; } },
      secondaryAction: { label: 'Add Delivery Hub', handler: openAddressModal },
    };
  }

  const pendingOrder = orders.value.find((order) => order.payment_status !== 'PAID' || order.status === 'PLACED' || order.status === 'CONFIRMED');
  if (pendingOrder) {
    return {
      stage: 'ACTION',
      title: 'Complete payment or confirm delivery',
      body: 'There is at least one active order that needs attention. Finish payment, track delivery, or confirm receipt so the workflow can close cleanly.',
      primaryAction: { label: 'View Orders', handler: () => { activeSection.value = 'orders'; } },
      secondaryAction: { label: 'View Quotes', handler: () => { activeSection.value = 'quotes'; } },
    };
  }

  return {
    stage: 'READY',
    title: 'Keep your purchasing workflow moving',
    body: 'Your buyer workspace is ready. Use quote requests for comparison, orders for fulfillment, and delivery hubs for dispatch visibility.',
    primaryAction: { label: 'View Orders', handler: () => { activeSection.value = 'orders'; } },
    secondaryAction: { label: 'View Quotes', handler: () => { activeSection.value = 'quotes'; } },
  };
});

const workflowSteps = computed(() => {
  if (isGuest.value) {
    return [
      {
        index: '01',
        label: 'Browse marketplace',
        help: 'Explore materials and property listings before you sign in.',
        done: true,
        active: true,
      },
      {
        index: '02',
        label: 'Sign in',
        help: 'Sign in to save orders, quotes, and delivery hubs.',
        done: false,
        active: false,
      },
      {
        index: '03',
        label: 'Save delivery hubs',
        help: 'Checkout and delivery routing unlock after sign-in.',
        done: false,
        active: false,
      },
      {
        index: '04',
        label: 'Request quotes',
        help: 'Send quote requests once your buyer account is active.',
        done: false,
        active: false,
      },
    ];
  }

  return [
    {
      index: '01',
      label: 'Set delivery hubs',
      help: 'Addresses unlock checkout and delivery routing.',
      done: Boolean(addresses.value.length),
      active: !addresses.value.length,
    },
    {
      index: '02',
      label: 'Request quotes',
      help: 'Ask vendors to price the items or materials you need.',
      done: Boolean(quotes.value.length),
      active: activeSection.value === 'quotes',
    },
    {
      index: '03',
      label: 'Place and pay orders',
      help: 'Accept a response, place the order, and complete payment.',
      done: Boolean(orders.value.some((order) => order.payment_status === 'PAID')),
      active: activeSection.value === 'orders',
    },
    {
      index: '04',
      label: 'Track delivery and close out',
      help: 'Use tracking, chat, confirmation, and disputes to finish the workflow.',
      done: Boolean(orders.value.some((order) => order.status === 'COMPLETED')),
      active: Boolean(orders.value.some((order) => order.status === 'SHIPPED' || order.tracking_number)),
    },
  ];
});

// Modals
const showRateModal = ref(false);
const showAddressModal = ref(false);
const showTrackingModal = ref(false);
const showChatModal = ref(false);
const showActionConfirm = ref(false);
const confirmActionTitle = ref('');
const confirmActionMessage = ref('');
const confirmActionLoading = ref(false);
const pendingAction = ref(null);
const activeTrackingNumber = ref('');
const activeChatRoomId = ref(null);
const selectedOrder = ref(null);
const newRating = ref({ score: 5, comment: '' });
const hubLocationState = ref({ lat: null, lng: null, city: '', country_id: null });
const newAddress = ref({
  name: '',
  address_line_1: '',
  city: '',
  country: 'Kenya',
  is_default: false,
  latitude: null,
  longitude: null
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

const openActionConfirm = ({ title, message, action }) => {
  confirmActionTitle.value = title;
  confirmActionMessage.value = message;
  pendingAction.value = action;
  showActionConfirm.value = true;
};

const closeActionConfirm = () => {
  showActionConfirm.value = false;
  confirmActionTitle.value = '';
  confirmActionMessage.value = '';
  confirmActionLoading.value = false;
  pendingAction.value = null;
};

const confirmAction = async () => {
  if (!pendingAction.value) return;
  confirmActionLoading.value = true;
  try {
    await pendingAction.value();
    closeActionConfirm();
  } catch (err) {
    confirmActionLoading.value = false;
  }
};

const fetchData = async () => {
  loading.value = true;
  try {
    if (isGuest.value) {
      orders.value = [];
      quotes.value = [];
      addresses.value = [];
      profile.value = { profile: {} };
      paymentMethods.value = [];
      selectedPaymentProvider.value = '';
      return;
    }
    const [ordRes, quoteRes, addrRes, profRes, paymentMethodsRes] = await Promise.all([
      api.get('/orders/'),
      api.get('/orders/quote-requests/'),
      api.get('/accounts/addresses/'),
      api.get('/accounts/profile/'),
      api.get('/platform_settings/payment-methods/')
    ]);
    orders.value = ordRes.data.results || ordRes.data;
    quotes.value = quoteRes.data.results || quoteRes.data;
    addresses.value = addrRes.data.results || addrRes.data;
    profile.value = profRes.data || { profile: {} };
    if (!profile.value.profile) profile.value.profile = {};
    paymentMethods.value = paymentMethodsRes.data.results || paymentMethodsRes.data || [];
    if (!selectedPaymentProvider.value) {
      const defaultMethod = paymentMethods.value.find((item) => item.is_default && item.active) || paymentMethods.value[0];
      selectedPaymentProvider.value = defaultMethod?.provider || '';
    }
  } catch (err) {
    console.error('Failed to fetch dashboard data', err);
    showAlert('Failed to synchronize dashboard data', 'error');
  } finally {
    loading.value = false;
  }
};

const getStatusBadgeVariant = (status) => {
  switch (status) {
    case 'DELIVERED': return 'success';
    case 'COMPLETED': return 'success';
    case 'PLACED': return 'info';
    case 'CANCELLED': return 'danger';
    default: return 'warning';
  }
};

const getPaymentBadgeVariant = (status) => {
  return status === 'PAID' ? 'success' : 'warning';
};

const confirmDelivery = async (id) => {
  try {
    await api.post(`/orders/${id}/confirm_delivery/`);
    fetchData();
    showAlert('Delivery confirmed! Vendor has been notified.', 'success');
  } catch (err) { showAlert('Failed to confirm delivery', 'error'); }
};

const cancelOrder = async (id) => {
  openActionConfirm({
    title: 'Cancel Order',
    message: 'Cancel this order and notify the vendor fulfillment workflow?',
    action: async () => {
      await api.post(`/orders/${id}/cancel_order/`);
      fetchData();
      showAlert('Order cancelled successfully.', 'success');
    }
  });
};

const openCheckoutModal = (quote, response) => {
  selectedCheckoutQuote.value = quote;
  selectedCheckoutResponse.value = response;
  if (!selectedPaymentProvider.value) {
    const defaultMethod = paymentMethods.value.find((item) => item.is_default && item.active) || paymentMethods.value[0];
    selectedPaymentProvider.value = defaultMethod?.provider || '';
  }
  showCheckoutModal.value = true;
};

const closeCheckoutModal = () => {
  showCheckoutModal.value = false;
  selectedCheckoutQuote.value = null;
  selectedCheckoutResponse.value = null;
};

const confirmCheckout = async () => {
  if (!selectedCheckoutQuote.value || !selectedCheckoutResponse.value) return;
  checkoutLoading.value = true;
  try {
    await api.post(`/orders/quote-requests/${selectedCheckoutQuote.value.id}/checkout/`, {
      response_id: selectedCheckoutResponse.value.id,
      payment_provider: selectedPaymentProvider.value
    });
    showAlert('Checkout successful! Order placed.', 'success');
    closeCheckoutModal();
    activeSection.value = 'orders';
    fetchData();
  } catch (err) {
    const msg = err.response?.data?.error || 'Checkout failed';
    showAlert(msg, 'error');
  } finally {
    checkoutLoading.value = false;
  }
};

const simulatePayment = async (order) => {
  try {
    await api.post(`/orders/${order.id}/simulate_payment/`, {});
    showAlert(`Payment simulated for order #${order.id}.`, 'success');
    fetchData();
  } catch (err) {
    showAlert(err.response?.data?.error || 'Failed to simulate payment', 'error');
  }
};

const openRateModal = (order) => {
  selectedOrder.value = order;
  newRating.value = { score: 5, comment: '' };
  showRateModal.value = true;
};

const submitRating = async () => {
  try {
    await api.post('/reviews/ratings/', {
      order: selectedOrder.value.id,
      score: newRating.value.score,
      comment: newRating.value.comment
    });
    showRateModal.value = false;
    showAlert('Thank you for your feedback!', 'success');
    fetchData();
  } catch (err) {
    const errData = err.response?.data;
    const msg = typeof errData === 'string'
      ? errData
      : (Array.isArray(errData) ? errData[0] : (errData?.detail || errData?.non_field_errors?.[0] || 'Failed to submit rating'));
    showAlert(msg, 'error');
  }
};

const updateProfile = async () => {
  if (isGuest.value) {
    showAlert('Sign in to save profile changes.', 'info');
    return;
  }
  try {
    const res = await api.patch('/accounts/profile/', {
      first_name: profile.value.first_name,
      last_name: profile.value.last_name,
      phone: profile.value.phone,
      bio: profile.value.bio,
      profile: profile.value.profile
    });
    profile.value = res.data || { profile: {} };
    if (!profile.value.profile) profile.value.profile = {};
    authStore.setUser(res.data);
    showAlert('Profile synchronized successfully!', 'success');
  } catch (err) { showAlert('Failed to update profile', 'error'); }
};

const openAddressModal = () => {
  if (isGuest.value) {
    showAlert('Sign in to save delivery hubs to your account.', 'info');
    return;
  }
  newAddress.value = {
    name: '',
    address_line_1: '',
    city: '',
    country: 'Kenya',
    is_default: false,
    latitude: null,
    longitude: null
  };
  hubLocationState.value = { lat: null, lng: null, city: '', country_id: null };
  showAddressModal.value = true;
};

const handleHubLocationChange = (loc) => {
  newAddress.value.latitude = loc.lat;
  newAddress.value.longitude = loc.lng;
  if (loc.city) newAddress.value.city = loc.city;
  if (loc.address) newAddress.value.address_line_1 = loc.address;
};

const saveAddress = async () => {
  if (isGuest.value) {
    showAlert('Sign in to save delivery hubs to your account.', 'info');
    return;
  }
  if (!newAddress.value.latitude) {
    return showAlert('Please select a location on the map.', 'error');
  }
  try {
    await api.post('/accounts/addresses/', newAddress.value);
    showAlert('Delivery hub saved successfully.', 'success');
    showAddressModal.value = false;
    fetchData();
  } catch (err) {
    console.error(err);
    showAlert('Failed to save delivery hub.', 'error');
  }
};

const deleteAddress = async (id) => {
  openActionConfirm({
    title: 'Delete Address',
    message: 'Remove this delivery hub from your profile?',
    action: async () => {
      await api.delete(`/accounts/addresses/${id}/`);
      fetchData();
      showAlert('Address removed.', 'success');
    }
  });
};

const openTracking = (trackingNumber) => {
  activeTrackingNumber.value = trackingNumber;
  showTrackingModal.value = true;
};

const openDisputeModal = (order) => {
  showAlert(`Dispute escalation for order #${order.id} is not self-service yet. Please contact support for manual resolution.`, 'info');
};

const openChat = async (type, id) => {
  try {
    const res = await api.post('/chat/rooms/get-or-create/', { [type]: id });
    activeChatRoomId.value = res.data.id;
    showChatModal.value = true;
  } catch (err) {
    showAlert(err.response?.data?.error || 'Failed to initiate secure channel', 'error');
  }
};

onMounted(fetchData);
</script>

<style scoped>
.pz-table-shell {
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.82);
  overflow-x: auto;
}

.pz-guest-panel {
  display: grid;
  gap: 0.85rem;
}

.pz-guest-panel__title {
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-guest-panel__body {
  margin: 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.pz-guest-panel__actions {
  display: flex;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.buyer-workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.buyer-workflow-banner__summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.buyer-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.buyer-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.buyer-workflow-banner__body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.buyer-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.buyer-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.buyer-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
}

.buyer-workflow-step__index {
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

.buyer-workflow-step__content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.buyer-workflow-step__content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.buyer-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.buyer-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.buyer-workflow-step--done .buyer-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.buyer-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.c-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 640px;
}

.c-table__head {
  background: rgba(10, 10, 15, 0.03);
}

.c-table__th {
  padding: var(--pz-space-3) var(--pz-space-4);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--pz-color-concrete-grey);
  text-align: left;
  border-bottom: 1px solid rgba(10, 10, 15, 0.1);
  white-space: nowrap;
}

.c-table__td {
  padding: var(--pz-space-3) var(--pz-space-4);
  border-bottom: 1px solid rgba(10, 10, 15, 0.05);
  font-size: 0.875rem;
  vertical-align: middle;
}

.c-table__td--mono {
  font-family: var(--pz-font-mono);
  font-size: 0.8rem;
}

.c-table__td--bold {
  font-weight: 600;
}

.c-table__tr--hover:hover {
  background: rgba(10, 10, 15, 0.02);
}

.c-table__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--pz-space-2);
  justify-content: flex-end;
}

.spinner {
  box-sizing: border-box;
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
    border: 4px solid var(--color-border);
    border-top: 4px solid var(--color-primary);
    border-radius: 50%;
  }
}

.pz-quote-list {
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-4);
}

.pz-quote-card {
  border: 1px solid rgba(10, 10, 15, 0.08);
  padding: var(--pz-space-5);
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

.pz-quote-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--pz-space-4);
  padding-bottom: var(--pz-space-3);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.pz-quote-card__id {
  font-family: var(--pz-font-mono);
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
}

.pz-quote-card__items {
  font-size: 0.85rem;
  color: var(--pz-color-text-secondary);
  background: #F8FAFC;
  padding: var(--pz-space-3);
  border-radius: 8px;
  margin-bottom: var(--pz-space-4);
}

.pz-quote-card__responses-title {
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--pz-color-earth-orange);
  margin-bottom: var(--pz-space-2);
}

.pz-quote-card__waiting {
  font-size: 0.85rem;
  color: var(--pz-color-text-secondary);
  font-style: italic;
}

.pz-quote-response-list {
  display: flex;
  flex-direction: column;
  gap: var(--pz-space-2);
}

.pz-quote-response {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--pz-space-3);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  transition: background 0.2s;
  gap: var(--pz-space-4);
  flex-wrap: wrap;
}

.pz-quote-response:hover {
  background: #F8FAFC;
}

.pz-quote-response--ordered {
  background: rgba(34, 197, 94, 0.04);
  border-color: rgba(34, 197, 94, 0.2);
}

.pz-quote-response__vendor {
  font-weight: 700;
  font-size: 0.875rem;
}

.pz-quote-response__price {
  font-size: 0.75rem;
  color: var(--pz-color-text-secondary);
  margin-top: 2px;
}

.pz-quote-response__ordered {
  display: flex;
  align-items: center;
  gap: var(--pz-space-2);
}

.pz-checkout-modal {
  display: grid;
  gap: 1rem;
}

.pz-checkout-modal__summary {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(10, 10, 15, 0.02);
}

.pz-checkout-modal__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.35rem;
}

.pz-checkout-modal__summary h3 {
  margin: 0 0 0.35rem;
  font-size: 1.05rem;
}

.pz-checkout-modal__summary p {
  margin: 0;
  color: var(--pz-color-steel-grey);
  max-width: 56ch;
}

.pz-checkout-modal__amount {
  display: grid;
  gap: 0.25rem;
  justify-items: end;
  align-content: start;
}

.pz-checkout-modal__amount span,
.pz-checkout-modal__footnote span,
.pz-checkout-method__meta {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-checkout-modal__amount strong {
  font-size: 1.5rem;
}

.pz-checkout-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
}

.pz-checkout-methods__empty {
  grid-column: 1 / -1;
  padding: 1rem;
  border: 1px dashed rgba(10, 10, 15, 0.16);
  background: rgba(10, 10, 15, 0.02);
  color: var(--pz-color-steel-grey);
}

.pz-checkout-method {
  display: grid;
  gap: 0.45rem;
  padding: 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: #fff;
  text-align: left;
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.pz-checkout-method:hover {
  transform: translateY(-1px);
  border-color: rgba(212, 101, 42, 0.35);
  box-shadow: 0 10px 30px rgba(10, 10, 15, 0.06);
}

.pz-checkout-method--active {
  border-color: rgba(212, 101, 42, 0.55);
  box-shadow: 0 0 0 2px rgba(212, 101, 42, 0.08);
}

.pz-checkout-method__top {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: start;
}

.pz-checkout-method__copy {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--pz-color-slate-grey);
}

.pz-checkout-modal__footnote {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  padding-top: 0.35rem;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-role-launcher {
  text-align: left;
  padding: 1rem;
  border: 1px solid var(--pz-color-foundation-black);
  background: white;
  transition: transform 160ms ease, box-shadow 160ms ease;
  cursor: pointer;
}

.pz-role-launcher:hover {
  transform: translateY(-2px);
  box-shadow: 8px 8px 0 rgba(10, 10, 15, 0.08);
}

.pz-role-launcher__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-earth-orange);
  margin-bottom: 0.5rem;
}

.pz-role-launcher__title {
  font-weight: 700;
  margin-bottom: 0.35rem;
}

.pz-role-launcher__body {
  font-size: 0.85rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.5;
}

.pz-profile-role-panel {
  display: grid;
  gap: 0.85rem;
  padding: 0.95rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(10, 10, 15, 0.03);
}

.pz-profile-role-panel__row {
  display: grid;
  gap: 0.2rem;
}

.pz-profile-role-panel__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-confirm-panel__title {
  margin: 0;
  font-weight: 700;
  line-height: 1.5;
}

.pz-confirm-panel__body {
  margin: 0.75rem 0 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

@media (min-width: 768px) {
  .pz-l-grid--md-cols-12 {
    grid-template-columns: repeat(12, minmax(0, 1fr));
  }
  .pz-l-grid__col-md-7 {
    grid-column: span 7 / span 7;
  }
  .pz-l-grid__col-md-5 {
    grid-column: span 5 / span 5;
  }
}

@media (max-width: 768px) {
  .buyer-workflow-banner {
    grid-template-columns: 1fr;
  }

  .buyer-workflow-banner__actions {
    justify-content: flex-start;
  }

  .buyer-workflow-banner__steps {
    grid-template-columns: 1fr;
  }
}
</style>
