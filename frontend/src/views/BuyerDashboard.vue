<template>
    <div id="buyer-dashboard-root">
        <div class="pz-l-container u-py-8">
            <!-- Breadcrumbs/Phase -->
            <PzPhaseIndicator :phase="2" size="small" class="u-mb-6" />

            <!-- Header -->
            <header class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center u-mb-8">
                <div>
                    <h1 class="pz-u-text-display">Sovereign Dashboard</h1>
                    <p class="pz-u-text-mono text-xs pz-u-color-steel">TRADING OPERATIONS CONTROL CENTER</p>
                </div>
                <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
                    <div class="u-text-right u-hide-mobile">
                        <div class="pz-u-text-mono font-bold">{{ authStore.user?.first_name }} {{
                            authStore.user?.last_name
                        }}</div>
                        <div class="pz-u-text-uppercase text-xs pz-u-color-earth">{{ userRole }}</div>
                    </div>
                    <Badge variant="primary">{{ userRole }}</Badge>
                </div>
            </header>

            <!-- Layout Grid -->
            <div class="pz-l-dashboard">
                <!-- Sidebar Navigation -->
                <aside class="u-sticky u-top-24">
                    <nav class="pz-side-nav">
                        <div class="pz-side-nav__group">
                            <h3 class="pz-side-nav__title">Shopping Operations</h3>
                            <button @click="activeSection = 'orders'" class="pz-side-nav__item"
                                :class="{ 'pz-side-nav__item--active': activeSection === 'orders' }">
                                <span class="pz-side-nav__icon">📦</span> My Orders
                            </button>
                            <button @click="activeSection = 'quotes'" class="pz-side-nav__item"
                                :class="{ 'pz-side-nav__item--active': activeSection === 'quotes' }">
                                <span class="pz-side-nav__icon">📝</span> Quote Requests
                            </button>
                            <button @click="activeSection = 'addresses'" class="pz-side-nav__item"
                                :class="{ 'pz-side-nav__item--active': activeSection === 'addresses' }">
                                <span class="pz-side-nav__icon">📍</span> Logistics Hubs
                            </button>
                            <button @click="activeSection = 'profile'" class="pz-side-nav__item"
                                :class="{ 'pz-side-nav__item--active': activeSection === 'profile' }">
                                <span class="pz-side-nav__icon">👤</span> Identity Settings
                            </button>
                        </div>
                    </nav>
                </aside>

                <!-- Main Content -->
                <main class="content-area flex-1 min-w-0">

                    <!-- ORDERS SECTION -->
                    <div v-if="activeSection === 'orders'">
                        <Card title="My Orders">
                            <template #header><Button variant="outline" size="sm"
                                    @click="fetchData">Refresh</Button></template>

                            <div v-if="loading" class="u-text-center u-py-12">
                                <div class="spinner"></div>
                            </div>
                            <div v-else-if="orders.length === 0" class="u-text-center u-py-12 u-color-muted">
                                No orders found. Start shopping!
                            </div>
                            <div v-else class="c-table-container">
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
                                        <tr v-for="order in orders" :key="order.id"
                                            class="c-table__tr c-table__tr--hover">
                                            <td class="c-table__td c-table__td--mono">#{{ order.id }}</td>
                                            <td class="c-table__td">{{ order.vendor_name }}</td>
                                            <td class="c-table__td c-table__td--bold">${{ order.total_amount }}</td>
                                            <td class="c-table__td">
                                                <div class="l-flex l-flex--gap-2">
                                                    <Badge :variant="getPaymentBadgeVariant(order.payment_status)">{{
                                                        order.payment_status }}
                                                    </Badge>
                                                    <Badge :variant="getStatusBadgeVariant(order.status)">{{
                                                        order.status }}
                                                    </Badge>
                                                </div>
                                            </td>
                                            <td class="c-table__td">
                                                <div class="c-table__actions">
                                                    <Button v-if="order.status === 'DELIVERED'" variant="success"
                                                        size="sm" @click="confirmDelivery(order.id)">Confirm</Button>
                                                    <Button v-if="order.status === 'COMPLETED'" variant="secondary"
                                                        size="sm" @click="openRateModal(order)">Rate</Button>
                                                    <Button v-if="['PLACED', 'CONFIRMED'].includes(order.status)"
                                                        variant="danger" size="sm"
                                                        @click="cancelOrder(order.id)">Cancel</Button>
                                                    <Button variant="outline" size="sm"
                                                        @click="openDisputeModal(order)">Dispute</Button>
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
                            <div v-if="loading" class="p-8 text-center">
                                <div class="spinner"></div>
                            </div>
                            <div v-else-if="quotes.length === 0" class="p-8 text-center text-muted">No quote requests
                                found.</div>

                            <div v-else class="pz-quote-list">
                                <div v-for="quote in quotes" :key="quote.id" class="pz-quote-card">
                                    <div class="pz-quote-card__header">
                                        <div class="pz-quote-card__id">Request #{{ quote.id }}</div>
                                        <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'">
                                            {{ quote.status }}
                                        </Badge>
                                    </div>

                                    <div class="pz-quote-card__items">
                                        <div v-for="item in quote.items" :key="item.id">
                                            • {{ item.quantity }}x {{ item.product_name || 'Material item' }}
                                        </div>
                                    </div>

                                    <div v-if="quote.responses && quote.responses.length > 0">
                                        <h4 class="pz-quote-card__responses-title">Vendor Responses</h4>
                                        <div class="pz-quote-response-list">
                                            <div v-for="resp in quote.responses" :key="resp.id"
                                                class="pz-quote-response"
                                                :class="{ 'pz-quote-response--ordered': resp.has_order }">
                                                <div>
                                                    <div class="pz-quote-response__vendor">
                                                        {{ resp.vendor_name || `Vendor #${resp.vendor}` }}
                                                    </div>
                                                    <div class="pz-quote-response__price">
                                                        ${{ resp.confirmed_price }} + ${{ resp.delivery_fee }} delivery
                                                    </div>
                                                </div>
                                                <!-- Already checked out -->
                                                <div v-if="resp.has_order" class="pz-quote-response__ordered">
                                                    <Badge variant="success">✓ Order #{{ resp.order_id }} Placed</Badge>
                                                    <Button size="sm" variant="outline"
                                                        @click="activeSection = 'orders'">View
                                                        Order</Button>
                                                </div>
                                                <!-- Available to checkout -->
                                                <Button v-else size="sm" variant="primary"
                                                    @click="checkout(quote.id, resp.id)">
                                                    Accept & Checkout
                                                </Button>
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
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-xl font-bold">Delivery Locations</h2>
                            <Button variant="primary" size="sm" @click="openAddressModal">+ Add New</Button>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Card v-for="addr in addresses" :key="addr.id"
                                class="relative hover:shadow-md transition-shadow">
                                <div class="absolute top-4 right-4" v-if="addr.is_default">
                                    <Badge variant="success">Default</Badge>
                                </div>
                                <h4 class="font-bold mb-2">{{ addr.name }}</h4>
                                <p class="text-sm text-muted mb-4">{{ addr.address_line_1 }}<br />{{ addr.city }}, {{
                                    addr.country }}</p>
                                <Button variant="danger" size="sm" @click="deleteAddress(addr.id)">Delete</Button>
                            </Card>
                        </div>
                    </div>

                    <!-- PROFILE SECTION -->
                    <div v-if="activeSection === 'profile'">
                        <Card title="Identity Synchronization" class="max-w-2xl">
                            <form @submit.prevent="updateProfile" class="l-grid l-grid--cols-1 l-grid--gap-4">
                                <div class="l-grid l-grid--cols-2 l-grid--gap-4">
                                    <PzInput v-model="profile.first_name" label="Legal First Name" required />
                                    <PzInput v-model="profile.last_name" label="Legal Last Name" required />
                                </div>
                                <PzInput v-model="profile.phone" label="Communication Line (Phone)"
                                    placeholder="+254..." />

                                <div class="pz-input-wrapper">
                                    <label class="pz-input__label">Platform Operation Context</label>
                                    <select v-model="profile.role" class="pz-input">
                                        <option value="PROJECT_OWNER">Project Owner / Buyer</option>
                                        <option value="CONTRACTOR">Contractor</option>
                                        <option value="VENDOR">Vendor / Supplier</option>
                                        <option value="INVESTOR">Investor Hub</option>
                                        <option value="GOVERNMENT">Regulatory Body</option>
                                    </select>
                                    <span class="pz-input__hint">This determines your primary interface and
                                        analytics.</span>
                                </div>

                                <div class="pz-input-wrapper">
                                    <label class="pz-input__label">Preferred Economic Region</label>
                                    <select v-model="profile.profile.preferred_region" class="pz-input">
                                        <option value="NAIROBI">Nairobi Metropolitan</option>
                                        <option value="MOMBASA">Mombasa Coastal</option>
                                        <option value="KISUMU">Kisumu Lakeside</option>
                                    </select>
                                </div>

                                <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pt-4">
                                    <p class="pz-u-text-mono text-xs pz-u-color-steel">LAST SYNC: JUST NOW</p>
                                    <Button type="submit" variant="primary">Synchronize Profile</Button>
                                </div>
                            </form>
                        </Card>
                    </div>

                </main>
            </div>
        </div>

        <!-- Rate Modal -->
        <Modal :isOpen="showRateModal" title="Rate Vendor" size="md" @close="showRateModal = false">
            <div class="text-center mb-4">
                <p class="mb-2">How was your experience with order #{{ selectedOrder?.id }}?</p>
                <div class="flex justify-center gap-2">
                    <button v-for="i in 5" :key="i" @click="newRating.score = i" type="button"
                        :class="['text-2xl focus:outline-none transition-colors', newRating.score >= i ? 'text-yellow-400' : 'text-gray-300']">
                        ★
                    </button>
                </div>
            </div>
            <textarea v-model="newRating.comment" class="form-input w-full" rows="3"
                placeholder="Leave a review..."></textarea>
            <template #footer>
                <Button variant="outline" @click="showRateModal = false">Cancel</Button>
                <Button @click="submitRating" variant="primary">Submit Review</Button>
            </template>
        </Modal>

        <!-- Address Modal (Placeholder) -->
        <Modal :isOpen="showAddressModal" title="Add Address" size="md" @close="showAddressModal = false">
            <form id="addr-form" @submit.prevent="saveAddress" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                <PzInput v-model="newAddress.name" label="Address Name" placeholder="Home, Site A..." required />
                <PzInput v-model="newAddress.address_line_1" label="Address Line" required />
                <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                    <PzInput v-model="newAddress.city" label="City" required />
                    <PzInput v-model="newAddress.country" label="Country" required />
                </div>

                <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-border-radius-sm mt-2">
                    <label
                        class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 pz-u-text-mono text-sm cursor-pointer">
                        <input type="checkbox" v-model="newAddress.is_default">
                        <span>SET AS DEFAULT SHIPPING DESTINATION</span>
                    </label>
                </div>
            </form>
            <template #footer>
                <Button variant="outline" @click="showAddressModal = false">Cancel</Button>
                <Button type="submit" form="addr-form" variant="primary">Save Address</Button>
            </template>
        </Modal>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import api from '../services/api';
    import { useAuthStore } from '../stores/auth';
    import Card from '../components/ui/Card.vue';
    import Button from '../components/ui/Button.vue';
    import Badge from '../components/ui/Badge.vue';
    import Modal from '../components/ui/Modal.vue';
    import PzInput from '../components/PzInput.vue';
    import PzPhaseIndicator from '../components/PzPhaseIndicator.vue';

    const authStore = useAuthStore();
    const activeSection = ref('orders');
    const orders = ref([]);
    const quotes = ref([]);
    const addresses = ref([]);
    const profile = ref({ profile: {} });
    const loading = ref(true);

    const userRole = computed(() => authStore.user?.role || 'User');

    // Modals
    const showRateModal = ref(false);
    const showAddressModal = ref(false);
    const selectedOrder = ref(null);
    const newRating = ref({ score: 5, comment: '' });
    const newAddress = ref({ name: '', address_line_1: '', city: '', country: 'Kenya', is_default: false });

    const fetchData = async () => {
        loading.value = true;
        try {
            const [ordRes, quoteRes, addrRes, profRes] = await Promise.all([
                api.get('/orders/orders/'),
                api.get('/orders/quote-requests/'),
                api.get('/accounts/addresses/'),
                api.get('/accounts/profile/')
            ]);
            orders.value = ordRes.data.results || ordRes.data;
            quotes.value = quoteRes.data.results || quoteRes.data;
            addresses.value = addrRes.data.results || addrRes.data;
            profile.value = profRes.data || { profile: {} };
            if (!profile.value.profile) profile.value.profile = {};
        } catch (err) {
            console.error("Failed to fetch dashboard data", err);
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
            await api.post(`/orders/orders/${id}/confirm_delivery/`);
            fetchData();
        } catch (err) { alert("Failed to confirm delivery"); }
    };

    const cancelOrder = async (id) => {
        if (!confirm("Are you sure you want to cancel?")) return;
        try {
            await api.post(`/orders/orders/${id}/cancel_order/`);
            fetchData();
        } catch (err) { alert("Failed to cancel order"); }
    };

    const checkout = async (quoteId, responseId) => {
        try {
            await api.post(`/orders/quote-requests/${quoteId}/checkout/`, { response_id: responseId });
            alert("Checkout successful! Order placed.");
            activeSection.value = 'orders';
            fetchData();
        } catch (err) {
            const msg = err.response?.data?.error || "Checkout failed";
            alert(msg);
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
            alert("Thank you for your feedback!");
            fetchData();
        } catch (err) {
            const errData = err.response?.data;
            const msg = typeof errData === 'string'
                ? errData
                : (Array.isArray(errData) ? errData[0] : (errData?.detail || errData?.non_field_errors?.[0] || 'Failed to submit rating'));
            alert(msg);
        }
    };

    const updateProfile = async () => {
        try {
            await api.patch('/accounts/profile/', profile.value);
            alert("Profile updated!");
        } catch (err) { alert("Failed to update profile"); }
    };

    const openAddressModal = () => {
        newAddress.value = { name: '', address_line_1: '', city: 'Nairobi', country: 'Kenya', is_default: false };
        showAddressModal.value = true;
    };

    const saveAddress = async () => {
        try {
            await api.post('/accounts/addresses/', newAddress.value);
            alert("Address added!");
            showAddressModal.value = false;
            fetchData();
        } catch (err) { alert("Failed to add address"); }
    };

    const deleteAddress = async (id) => {
        if (!confirm("Delete address?")) return;
        try {
            await api.delete(`/accounts/addresses/${id}/`);
            fetchData();
        } catch (err) { alert("Failed to delete address"); }
    };

    const openDisputeModal = (order) => {
        alert("Dispute feature coming soon. Please contact support.");
    };

    onMounted(fetchData);
</script>

<style scoped>
    .u-sticky {
        position: sticky;
    }

    .u-top-24 {
        top: var(--space-24);
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
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }

    /* Quote Cards */
    .pz-quote-list {
        display: flex;
        flex-direction: column;
        gap: var(--pz-space-4, 16px);
    }

    .pz-quote-card {
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: var(--pz-border-radius-md, 12px);
        padding: var(--pz-space-5, 20px);
        background: #fff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .pz-quote-card__header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--pz-space-4, 16px);
        padding-bottom: var(--pz-space-3, 12px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }

    .pz-quote-card__id {
        font-weight: 700;
        font-size: 1rem;
    }

    .pz-quote-card__items {
        font-size: 0.85rem;
        color: var(--pz-color-text-secondary, #666);
        background: #F8FAFC;
        padding: var(--pz-space-3, 12px);
        border-radius: 8px;
        margin-bottom: var(--pz-space-4, 16px);
    }

    .pz-quote-card__responses-title {
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--pz-color-earth-orange, #FF6B2B);
        margin-bottom: var(--pz-space-2, 8px);
    }

    .pz-quote-card__waiting {
        font-size: 0.85rem;
        color: var(--pz-color-text-secondary, #999);
        font-style: italic;
    }

    .pz-quote-response-list {
        display: flex;
        flex-direction: column;
        gap: var(--pz-space-2, 8px);
    }

    .pz-quote-response {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--pz-space-3, 12px);
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 8px;
        transition: background 0.2s;
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
        color: var(--pz-color-text-secondary, #666);
        margin-top: 2px;
    }

    .pz-quote-response__ordered {
        display: flex;
        align-items: center;
        gap: var(--pz-space-2, 8px);
    }
</style>
