<template>
  <div class="vendor-orders-section">
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">Vendor Operations</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">Orders</h3>
          <div class="pz-section-shell__meta">Fulfillment, shipment, and buyer response control.</div>
        </div>
        <Button variant="ghost" size="sm" @click="fetchOrders">Refresh</Button>
      </div>

      <div v-if="loading" class="pz-section-shell__content">
        <div class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">Loading orders...</div>
        </div>
      </div>

      <div v-else-if="orders.length === 0" class="pz-section-shell__content">
        <div class="pz-empty-state">
          <div class="pz-empty-state__glyph">ORD</div>
          <div class="pz-empty-state__eyebrow">Order Stream</div>
          <h4 class="pz-empty-state__title">No orders detected in this deployment zone.</h4>
          <p class="pz-empty-state__body">New buyer orders will appear here as soon as procurement requests move into fulfillment.</p>
        </div>
      </div>

      <div v-else class="pz-order-stream pz-section-shell__content">
        <div v-for="order in orders" :key="order.id" class="pz-order-node pz-u-transition-base">
          <div class="pz-order-node__header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start u-mb-6">
            <div>
              <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-1 font-bold">Order #{{ order.id }}
              </div>
              <div class="pz-u-text-display text-sm">{{ order.buyer_name || 'Guest Buyer' }}</div>
              <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mt-1">
                {{ new Date(order.created_at).toLocaleString() }}
              </div>
            </div>
            <Badge :variant="getStatusVariant(order.status)" class="pz-u-text-mono">{{ order.status }}</Badge>
          </div>

          <!-- Items Manifest -->
          <div class="pz-u-bg-limestone pz-p-6 pz-u-border-l u-mb-6"
            style="border-left-color: var(--pz-color-foundation-black);">
            <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4" style="letter-spacing: 0.1em;">
              Items</div>
            <div v-for="item in order.items" :key="item.id"
              class="pz-l-flex pz-l-flex--justify-between u-py-2 pz-u-border-b" style="border-bottom-style: dashed;">
              <span class="pz-u-text-mono text-xs">{{ item.quantity }}x {{ item.product_name_snapshot }}</span>
              <span class="pz-u-text-mono text-xs font-bold">{{ configStore.formatPrice(item.unit_price_snapshot, order.currency || 'KES')
                }}</span>
            </div>
            <div class="u-mt-6 pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
              <span class="pz-u-text-mono text-xs font-bold">Total</span>
              <span class="pz-u-text-display text-xl pz-u-color-savanna">{{ configStore.formatPrice(order.total_amount, order.currency || 'KES')
                }}</span>
            </div>
          </div>

          <!-- Ops Control -->
          <div class="pz-l-flex pz-l-flex--justify-end pz-l-flex--gap-3">
            <template v-if="order.status !== 'COMPLETED' && order.status !== 'CANCELLED'">
              <Button v-if="order.status === 'PLACED'" size="sm" variant="primary"
                @click="openFulfillmentModal(order, 'CONFIRMED')">Confirm Order</Button>
              <Button v-if="order.status === 'CONFIRMED'" size="sm" variant="primary"
                @click="openFulfillmentModal(order, 'PACKING')">Start Packing</Button>
              <Button v-if="order.status === 'PACKING'" size="sm" variant="primary"
                @click="openFulfillmentModal(order, 'SHIPPED')">Mark Shipped</Button>
              <Button v-if="order.status === 'SHIPPED'" size="sm" variant="primary"
                @click="openFulfillmentModal(order, 'DELIVERED')">Mark Delivered</Button>
              <Button v-if="order.tracking_number" size="sm" variant="secondary"
                @click="openTracking(order.tracking_number)">Track Order</Button>
            </template>
            <Button variant="ghost" size="sm" @click="openChat(order.id)">Chat with Buyer</Button>
            <Button variant="ghost" size="sm">Print Invoice</Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Fulfillment Protocol Modal -->
    <Modal :isOpen="showFulfillmentModal" title="Update Order Status" size="md"
      @close="showFulfillmentModal = false">
      <form id="fulfillment-form" @submit.prevent="submitFulfillment"
        class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <div class="pz-u-bg-limestone pz-p-4 pz-u-border" style="border-left: 4px solid var(--pz-color-earth-orange);">
          <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-1">Changing status to:</div>
          <div class="pz-u-text-mono font-bold">{{ fulfillmentForm.status }}</div>
        </div>

        <div v-if="fulfillmentForm.status === 'CONFIRMED'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
          <PzInput type="date" v-model="fulfillmentForm.estimated_delivery_at" label="Estimated Delivery Date" required />
          <PzInput v-model="fulfillmentForm.notes" label="Notes for Buyer" />
        </div>

        <div v-if="fulfillmentForm.status === 'SHIPPED'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
          <div class="pz-input-wrapper">
            <label class="pz-input__label">Select Courier</label>
            <select v-model="fulfillmentForm.carrier_code" class="u-w-full pz-p-3 pz-u-border pz-u-text-mono text-sm"
              style="background: white;">
              <option v-for="carrier in carriers" :key="carrier.code" :value="carrier.code">
                {{ carrier.name.toUpperCase() }}
              </option>
            </select>
          </div>
          <div class="pz-u-text-mono text-xs pz-u-color-concrete">
            // Tracking ID will be generated automatically
          </div>
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="showFulfillmentModal = false">Cancel</Button>
        <Button type="submit" form="fulfillment-form" variant="primary" :loading="updating">Update Status</Button>
      </template>
    </Modal>

    <!-- Tracking Modal -->
    <Modal :isOpen="showTrackingModal" title="Track Shipment" size="xl" @close="showTrackingModal = false">
      <LogisticsTracker :trackingNumber="activeTrackingNumber" />
    </Modal>

    <!-- Chat Modal -->
    <Modal :isOpen="showChatModal" title="Chat with Buyer" size="lg" @close="showChatModal = false">
      <ChatWindow v-if="activeChatRoomId" :roomId="String(activeChatRoomId)" />
    </Modal>
  </div>
</template>

<script setup>
  import { ref, onMounted, defineAsyncComponent, inject } from 'vue';
  import api from '../../services/api';
  import Button from '../ui/Button.vue';
  import Badge from '../ui/Badge.vue';
  import { useConfigStore } from '../../stores/config';
  import Modal from '../ui/Modal.vue';
  import PzInput from '../PzInput.vue';
  import ChatWindow from '../chat/ChatWindow.vue';

  const configStore = useConfigStore();
  const LogisticsTracker = defineAsyncComponent(() => import('../logistics/LogisticsTracker.vue'));

  const orders = ref([]);
  const carriers = ref([]);
  const loading = ref(true);
  const updating = ref(false);
  const showFulfillmentModal = ref(false);
  const showTrackingModal = ref(false);
  const showChatModal = ref(false);
  const selectedOrder = ref(null);
  const activeTrackingNumber = ref('');
  const activeChatRoomId = ref(null);
  const showAlert = inject('showAlert');

  const fulfillmentForm = ref({
    status: '',
    notes: '',
    carrier_code: 'G4S',
    estimated_delivery_at: ''
  });

  async function fetchOrders() {
    loading.value = true;
    try {
      const res = await api.get('/orders/vendor_orders/');
      orders.value = res.data.results || res.data;
    } catch (err) {
      console.error("Order fetch error", err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchCarriers() {
    try {
      const res = await api.get('/logistics/carriers/');
      carriers.value = res.data.results || res.data;
    } catch (err) {
      console.error("Carrier fetch error", err);
    }
  }

  function getStatusVariant(status) {
    switch (status) {
      case 'COMPLETED': return 'success';
      case 'CANCELLED': return 'danger';
      case 'PLACED': return 'warning';
      case 'SHIPPED': return 'primary';
      default: return 'secondary';
    }
  }

  function openFulfillmentModal(order, nextStatus) {
    selectedOrder.value = order;
    fulfillmentForm.value = {
      status: nextStatus,
      notes: '',
      carrier_code: 'G4S',
      estimated_delivery_at: ''
    };
    showFulfillmentModal.value = true;
  }

  function openTracking(trackingNumber) {
    activeTrackingNumber.value = trackingNumber;
    showTrackingModal.value = true;
  }

  async function submitFulfillment() {
    updating.value = true;
    try {
      await api.post(`/orders/${selectedOrder.value.id}/update_fulfillment/`, fulfillmentForm.value);
      showFulfillmentModal.value = false;
      fetchOrders();
      if (showAlert) showAlert("Order status updated via secure protocol", "success");
    } catch (err) {
      if (showAlert) showAlert("Failed to update order status", "error");
    } finally {
      updating.value = false;
    }
  }

  async function openChat(orderId) {
    try {
      const res = await api.post('/chat/rooms/get-or-create/', { order: orderId });
      activeChatRoomId.value = res.data.id;
      showChatModal.value = true;
    } catch (err) {
      if (showAlert) showAlert(err.response?.data?.error || "Failed to initiate chat session", "error");
    }
  }

  onMounted(() => {
    fetchOrders();
    fetchCarriers();
  });
</script>

<style scoped>
  .pz-admin-card {
    background: white;
    border: 1px solid var(--pz-color-foundation-black);
  }

  .pz-admin-card__header {
    padding: var(--pz-space-4) var(--pz-space-6);
    border-bottom: 2px solid var(--pz-color-foundation-black);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pz-admin-card__title {
    font-family: var(--pz-font-mono);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.1em;
  }

  .pz-order-stream {
    display: grid;
    gap: 1rem;
  }

  .pz-order-node {
    padding: 1.25rem;
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(10, 10, 15, 0.08);
    box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
  }

  .pz-order-node:hover {
    background: var(--pz-color-limestone-white);
  }
</style>
