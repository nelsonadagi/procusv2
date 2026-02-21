<template>
    <div class="pz-l-container u-py-8">
        <!-- Breadcrumbs/Phase -->
        <PzPhaseIndicator :phase="1" size="small" class="u-mb-6" />

        <!-- Header -->
        <header class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center u-mb-8">
            <div>
                <h1 class="pz-u-text-display">Vendor Command Hub</h1>
                <p class="pz-u-text-mono text-xs pz-u-color-copper">STRATEGIC MERCHANT OPERATIONS</p>
            </div>
            <div v-if="vendorProfile" class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
                <div class="u-text-right u-hide-mobile">
                    <div class="pz-u-text-mono font-bold">{{ vendorProfile.business_name }}</div>
                    <div class="pz-u-text-uppercase text-xs pz-u-color-savanna">{{ vendorProfile.location }}</div>
                </div>
                <Badge :variant="vendorProfile.verified_status === 'APPROVED' ? 'success' : 'warning'">
                    {{ vendorProfile.verified_status }}
                </Badge>
            </div>
        </header>

        <!-- Layout Grid -->
        <div class="pz-l-dashboard">
            <!-- Sidebar Navigation -->
            <aside class="u-sticky u-top-24">
                <nav class="pz-side-nav">
                    <div class="pz-side-nav__group">
                        <h3 class="pz-side-nav__title">Merchant Capability</h3>
                        <button @click="activeSection = 'profile'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'profile' }">
                            <span class="pz-side-nav__icon">👤</span> Operational Profile
                        </button>
                        <button @click="activeSection = 'inventory'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'inventory' }">
                            <span class="pz-side-nav__icon">📦</span> Supply Inventory
                        </button>
                        <button @click="activeSection = 'orders'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'orders' }">
                            <span class="pz-side-nav__icon">📋</span> Logistics Orders
                        </button>
                        <button @click="activeSection = 'quotes'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'quotes' }">
                            <span class="pz-side-nav__icon">📝</span> Procurement Quotes
                        </button>
                    </div>
                </nav>
            </aside>

            <!-- Main Content -->
            <main class="content-area flex-1 min-w-0">

                <!-- PROFILE SECTION -->
                <div v-if="activeSection === 'profile'">
                    <Card title="Business Profile">
                        <template #header>
                            <Button v-if="!editingProfile" variant="secondary" size="sm" @click="editingProfile = true">
                                Edit Profile
                            </Button>
                        </template>

                        <div v-if="loadingProfile" class="flex justify-center p-8">
                            <div class="spinner"></div>
                        </div>

                        <div v-else-if="vendorProfile">
                            <form @submit.prevent="saveProfile" class="l-grid l-grid--cols-1 l-grid--gap-6">
                                <div class="pz-l-grid pz-l-grid--cols-2 pz-l-grid--gap-6">
                                    <PzInput label="Registered Entity Name" v-model="profileForm.business_name"
                                        :disabled="!editingProfile" required />
                                    <PzInput label="Tax/Reg Certification" v-model="profileForm.registration_number"
                                        :disabled="!editingProfile" required />
                                    <PzInput label="Primary Logistics Hub" v-model="profileForm.location"
                                        :disabled="!editingProfile" required />

                                    <div class="pz-input-wrapper">
                                        <label class="pz-input__label">Strategic Categories</label>
                                        <PzInput v-if="editingProfile" v-model="categoriesInput"
                                            placeholder="Cement, Steel..." hideLabel />
                                        <div v-else class="pz-l-flex pz-l-flex--gap-2 pt-2">
                                            <Badge v-for="cat in profileForm.categories_served" :key="cat"
                                                variant="finance">{{ cat }}</Badge>
                                        </div>
                                    </div>
                                </div>

                                <!-- Metrics -->
                                <div class="pz-u-border-t pt-6 mt-6">
                                    <h4 class="pz-u-text-display text-sm u-mb-4">Operational Performance</h4>
                                    <div class="pz-l-grid pz-l-grid--cols-4 pz-l-grid--gap-4">
                                        <div class="pz-u-bg-limestone pz-u-border pz-p-4 pz-u-text-center">
                                            <div class="pz-u-text-mono text-xs pz-u-color-steel">FULFILLMENT</div>
                                            <div class="pz-u-text-display text-xl pz-u-color-savanna">{{
                                                vendorProfile.fulfillment_rate }}%
                                            </div>
                                        </div>
                                        <div class="pz-u-bg-limestone pz-u-border pz-p-4 pz-u-text-center">
                                            <div class="pz-u-text-mono text-xs pz-u-color-steel">TRUST RATING</div>
                                            <div class="pz-u-text-display text-xl pz-u-color-earth">{{
                                                vendorProfile.average_rating.toFixed(1)
                                            }} ★</div>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="editingProfile"
                                    class="pz-l-flex pz-l-flex--justify-between pt-4 pz-u-border-t">
                                    <p class="pz-u-text-mono text-xs pz-u-color-steel">SECURITY VERIFIED IDENTITY</p>
                                    <div class="pz-l-flex pz-l-flex--gap-2">
                                        <Button variant="ghost" @click="cancelEditProfile">Discard</Button>
                                        <Button variant="primary" type="submit">Commit Changes</Button>
                                    </div>
                                </div>
                            </form>
                        </div>

                        <!-- Empty State / Reg Form -->
                        <div v-else class="text-center py-12">
                            <div v-if="!showRegistrationForm">
                                <h3 class="text-xl font-bold mb-2">Become a Vendor</h3>
                                <p class="mb-4">Start selling your construction materials today.</p>
                                <Button variant="primary" size="lg" @click="showRegistrationForm = true">Register
                                    Now</Button>
                            </div>
                            <div v-else class="max-w-md mx-auto text-left">
                                <h3 class="text-lg font-bold mb-4">Vendor Registration</h3>
                                <form @submit.prevent="registerAsVendor"
                                    class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                                    <PzInput v-model="registrationForm.business_name" placeholder="Business Name"
                                        required />
                                    <PzInput v-model="registrationForm.registration_number"
                                        placeholder="Registration Number" required />
                                    <PzInput v-model="registrationForm.location" placeholder="Location" required />
                                    <PzInput v-model="registrationCategoriesInput"
                                        placeholder="Categories (comma separated)" />
                                    <div class="pz-l-flex pz-l-flex--gap-2 u-mt-4">
                                        <Button variant="outline" class="flex-1"
                                            @click="showRegistrationForm = false">Cancel</Button>
                                        <Button variant="primary" class="flex-1" type="submit"
                                            :loading="registering">Register</Button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </Card>
                </div>

                <!-- INVENTORY SECTION -->
                <div v-if="activeSection === 'inventory'">
                    <!-- Stats -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <Card>
                            <div class="u-text-center">
                                <div class="u-text-sm u-color-muted">Active Products</div>
                                <div class="u-text-2xl u-font-bold">{{ products.length }}</div>
                            </div>
                        </Card>
                        <Card>
                            <div class="u-text-center">
                                <div class="u-text-sm u-color-muted">Low Stock</div>
                                <div class="u-text-2xl u-font-bold u-color-warning">{{ lowStockCount }}</div>
                            </div>
                        </Card>
                        <Card>
                            <div class="u-text-center">
                                <div class="u-text-sm u-color-muted">Total Value</div>
                                <div class="u-text-2xl u-font-bold u-color-success">$--</div>
                            </div>
                        </Card>
                    </div>

                    <Card title="Product Inventory">
                        <template #header>
                            <div class="flex gap-2 flex-wrap">
                                <Button variant="outline" size="sm" @click="downloadTemplate">Template</Button>
                                <Button variant="outline" size="sm" @click="triggerImport">Import CSV</Button>
                                <input type="file" ref="fileInput" accept=".csv" class="hidden"
                                    @change="handleFileUpload">
                                <Button variant="primary" size="sm" @click="openAddModal">Add Product</Button>
                            </div>
                        </template>

                        <div v-if="loading" class="u-text-center u-py-12">
                            <div class="spinner"></div>
                        </div>
                        <div v-else class="c-table-container">
                            <table class="c-table">
                                <thead class="c-table__head">
                                    <tr>
                                        <th class="c-table__th">Product</th>
                                        <th class="c-table__th">Price</th>
                                        <th class="c-table__th">Stock</th>
                                        <th class="c-table__th u-text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="product in products" :key="product.id"
                                        class="c-table__tr c-table__tr--hover">
                                        <td class="c-table__td">
                                            <div class="u-font-bold">{{ product.name }}</div>
                                            <div class="u-text-xs u-color-muted">{{ product.brand || 'No Brand' }}
                                            </div>
                                        </td>
                                        <td class="c-table__td c-table__td--bold">
                                            ${{ product.base_price }}
                                        </td>
                                        <td class="c-table__td">
                                            <Badge :variant="product.stock_quantity < 10 ? 'danger' : 'success'">
                                                {{ product.stock_quantity }} {{ product.unit }}
                                            </Badge>
                                        </td>
                                        <td class="c-table__td">
                                            <div class="c-table__actions">
                                                <Button variant="secondary" size="sm"
                                                    @click="editProduct(product)">Edit</Button>
                                                <Button variant="danger" size="sm"
                                                    @click="deleteProduct(product.id)">Del</Button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <!-- Pagination -->
                        <div v-if="inventoryTotalPages > 1" class="flex justify-center gap-4 mt-6">
                            <Button variant="outline" size="sm" :disabled="inventoryPage === 1"
                                @click="changeInventoryPage(inventoryPage - 1)">Previous</Button>
                            <span class="text-sm self-center">Page {{ inventoryPage }} of {{ inventoryTotalPages
                                }}</span>
                            <Button variant="outline" size="sm" :disabled="inventoryPage === inventoryTotalPages"
                                @click="changeInventoryPage(inventoryPage + 1)">Next</Button>
                        </div>
                    </Card>
                </div>

                <!-- ORDERS SECTION -->
                <div v-if="activeSection === 'orders'">
                    <Card title="Order Management">
                        <template #header><Button variant="outline" size="sm"
                                @click="fetchOrders">Refresh</Button></template>
                        <div v-if="loadingOrders" class="p-8 text-center">Loading orders...</div>
                        <div v-else-if="orders.length === 0" class="p-8 text-center text-muted">No orders found.
                        </div>

                        <div v-else class="space-y-4">
                            <div v-for="order in orders" :key="order.id" class="border border-gray-200 rounded-lg p-4">
                                <div class="flex justify-between items-start mb-4">
                                    <div>
                                        <div class="font-bold">Order #{{ order.id }}</div>
                                        <div class="text-sm text-muted">{{ formatOrderDate(order.created_at) }} • {{
                                            order.buyer_name }}
                                        </div>
                                    </div>
                                    <Badge :variant="order.status === 'COMPLETED' ? 'success' : 'warning'">{{
                                        order.status }}</Badge>
                                </div>

                                <!-- Items -->
                                <div class="bg-gray-50 p-3 rounded mb-3 text-sm">
                                    <div v-for="item in order.items" :key="item.id" class="flex justify-between py-1">
                                        <span>{{ item.quantity }}x {{ item.product_name_snapshot }}</span>
                                        <span>${{ item.unit_price_snapshot }}</span>
                                    </div>
                                    <div class="border-t border-gray-200 mt-2 pt-2 flex justify-between font-bold">
                                        <span>Total</span>
                                        <span>${{ order.total_amount }}</span>
                                    </div>
                                </div>

                                <!-- Actions -->
                                <div class="flex gap-2 justify-end"
                                    v-if="order.status !== 'COMPLETED' && order.status !== 'CANCELLED'">
                                    <Button v-if="order.status === 'PLACED'" size="sm"
                                        @click="openFulfillmentModal(order, 'CONFIRMED')">Confirm</Button>
                                    <Button v-if="order.status === 'CONFIRMED'" size="sm"
                                        @click="openFulfillmentModal(order, 'PACKING')">Start Packing</Button>
                                    <Button v-if="order.status === 'PACKING'" size="sm"
                                        @click="openFulfillmentModal(order, 'SHIPPED')">Ship</Button>
                                    <Button v-if="order.status === 'SHIPPED'" size="sm"
                                        @click="openFulfillmentModal(order, 'DELIVERED')">Deliver</Button>
                                </div>
                            </div>
                        </div>
                    </Card>
                </div>

                <!-- QUOTES SECTION -->
                <div v-if="activeSection === 'quotes'">
                    <Card title="Quote Requests">
                        <template #header><Button variant="outline" size="sm"
                                @click="fetchQuoteRequests">Refresh</Button></template>
                        <div v-if="loadingQuotes" class="p-8 text-center">Loading quotes...</div>
                        <div v-else class="space-y-4">
                            <div v-for="quote in quoteRequests" :key="quote.id"
                                class="border border-gray-200 rounded-lg p-4">
                                <div class="flex justify-between mb-2">
                                    <div class="font-bold">#{{ quote.id }} - {{ quote.buyer_name }}</div>
                                    <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'">{{
                                        quote.status }}</Badge>
                                </div>
                                <div class="text-sm text-muted mb-4">
                                    <div v-for="item in quote.items" :key="item.id">{{ item.quantity }}x {{
                                        item.product_details?.name
                                        }}</div>
                                </div>
                                <Button v-if="quote.status === 'REQUESTED'" size="sm"
                                    @click="openQuoteResponseModal(quote)">Respond</Button>
                            </div>
                        </div>
                    </Card>
                </div>

            </main>
        </div>
    </div>

    <!-- Add Product Modal -->
    <Modal :isOpen="showAddModal" :title="editingProduct ? 'Edit Product' : 'Add Product'" size="xl"
        @close="closeModal">
        <form id="product-form" @submit.prevent="saveProduct" class="h-full flex flex-col">

            <!-- Tabs -->
            <div class="pz-tabs__nav">
                <button type="button" v-for="tab in tabs" :key="tab" @click="activeTab = tab" class="pz-tabs__btn"
                    :class="{ 'pz-tabs__btn--active': activeTab === tab }">
                    {{ tab }}
                </button>
            </div>

            <!-- Tab Content -->
            <div class="flex-1 overflow-y-auto pr-2">
                <div v-show="activeTab === 'Basic Info'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                    <PzInput v-model="formData.name" label="Name" required />

                    <div class="pz-input-wrapper">
                        <label class="pz-input__label">Category</label>
                        <select v-model="formData.category" class="pz-input">
                            <option v-for="c in categories" :value="c.id" :key="c.id">{{ c.name }}</option>
                        </select>
                    </div>

                    <div class="pz-input-wrapper">
                        <label class="pz-input__label">Description</label>
                        <textarea v-model="formData.description" class="pz-input" rows="4"></textarea>
                    </div>
                </div>

                <div v-show="activeTab === 'Pricing & Stock'"
                    class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4 mt-4">
                    <PzInput type="number" v-model="formData.base_price" label="Price" step="0.01" />
                    <PzInput v-model="formData.unit" label="Unit" />
                    <PzInput type="number" v-model="formData.stock_quantity" label="Stock" />
                </div>

                <div v-show="activeTab === 'Specifications'"
                    class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4 mt-4">
                    <PzInput v-model="formData.brand" label="Brand" />
                    <PzInput v-model="formData.model_number" label="Model" />
                </div>

                <div v-show="activeTab === 'Quality'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4 mt-4">
                    <div class="pz-input-wrapper">
                        <label class="pz-input__label">Certifications</label>
                        <textarea v-model="formData.certifications" class="pz-input" rows="2"></textarea>
                    </div>
                </div>

                <div v-show="activeTab === 'Images'">
                    <div class="border-2 border-dashed border-gray-300 p-8 text-center rounded cursor-pointer hover:bg-gray-50"
                        @click="$refs.imageInput.click()">
                        <p>Click to upload images</p>
                        <input ref="imageInput" type="file" multiple class="hidden" @change="handleImageUpload">
                    </div>
                    <div class="grid grid-cols-4 gap-4 mt-4">
                        <div v-for="(img, idx) in selectedImages" :key="idx"
                            class="relative aspect-square border-2 border-gray-200 rounded overflow-hidden">
                            <img :src="img.preview" class="w-full h-full object-cover">
                            <button type="button"
                                class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6"
                                @click="removeImage(idx)">×</button>
                        </div>
                    </div>
                </div>
            </div>
        </form>
        <template #footer>
            <Button variant="outline" @click="closeModal">Cancel</Button>
            <Button type="submit" form="product-form" variant="primary" :loading="saving">Save Product</Button>
        </template>
    </Modal>

    <!-- Fulfillment Modal -->
    <Modal :isOpen="showFulfillmentModal" title="Update Order" size="md" @close="closeFulfillmentModal">
        <form id="fulfillment-form" @submit.prevent="submitFulfillment"
            class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
            <div class="pz-alert pz-alert--info">
                <span>Updating sequence status to: <strong>{{ fulfillmentForm.status }}</strong></span>
            </div>

            <PzInput v-if="fulfillmentForm.status === 'CONFIRMED'" type="date"
                v-model="fulfillmentForm.estimated_delivery_at" label="Est. Delivery Date" required />

            <PzInput v-if="fulfillmentForm.status === 'SHIPPED'" v-model="fulfillmentForm.tracking_number"
                label="Tracking Information" required />
        </form>
        <template #footer>
            <Button variant="outline" @click="closeFulfillmentModal">Cancel</Button>
            <Button type="submit" form="fulfillment-form" :loading="submittingFulfillment">Update</Button>
        </template>
    </Modal>

    <!-- Quote Modal -->
    <Modal :isOpen="showQuoteModal" title="Send Quote" size="md" @close="closeQuoteModal">
        <form id="quote-form" @submit.prevent="submitQuoteResponse"
            class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
            <PzInput type="number" v-model="quoteForm.confirmed_price" label="Confirmed Price Valuation ($)" required />
            <PzInput type="number" v-model="quoteForm.delivery_fee" label="Logistics Surcharge ($)" required />
            <PzInput type="date" v-model="quoteForm.expires_at" label="Validity Window (Date)" required />
        </form>
        <template #footer>
            <Button variant="outline" @click="closeQuoteModal">Cancel</Button>
            <Button type="submit" form="quote-form" :loading="submittingQuote">Send</Button>
        </template>
    </Modal>

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
    const userRole = computed(() => authStore.user?.role || 'Vendor');
    const lowStockCount = computed(() => products.value.filter(p => p.stock_quantity < 10).length);
    const activeSection = ref('profile');


    const products = ref([]);
    const categories = ref([]);
    const loading = ref(true);
    const saving = ref(false);
    const importing = ref(false);
    const fileInput = ref(null);
    const showAddModal = ref(false);
    const editingProduct = ref(null);
    const activeTab = ref('Basic Info');
    const selectedImages = ref([]);
    const primaryImageIndex = ref(0);
    const inventoryPage = ref(1);
    const inventoryPageSize = 10;
    const inventoryTotal = ref(0);
    const inventoryTotalPages = computed(() => Math.ceil(inventoryTotal.value / inventoryPageSize));
    const changeInventoryPage = (page) => {
        if (page < 1 || page > inventoryTotalPages.value) return;
        inventoryPage.value = page;
        fetchMyProducts();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    const orders = ref([]);
    const loadingOrders = ref(false);
    const showFulfillmentModal = ref(false);
    const submittingFulfillment = ref(false);
    const selectedOrder = ref(null);
    const fulfillmentForm = ref({ status: '', tracking_number: '', estimated_delivery_at: '' });
    const fetchOrders = async () => {
        loadingOrders.value = true;
        try {
            const res = await api.get('/orders/orders/');
            orders.value = res.data.results || res.data;
        } catch (err) { console.error('Failed to fetch orders', err); }
        finally { loadingOrders.value = false; }
    };
    const formatOrderDate = (dateStr) => {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString();
    };
    const openFulfillmentModal = (order, newStatus) => {
        selectedOrder.value = order;
        fulfillmentForm.value = {
            status: newStatus,
            tracking_number: order.tracking_number || '',
            estimated_delivery_at: ''
        };
        showFulfillmentModal.value = true;
    };
    const closeFulfillmentModal = () => { showFulfillmentModal.value = false; selectedOrder.value = null; };
    const submitFulfillment = async () => {
        submittingFulfillment.value = true;
        try {
            await api.post(`/orders/orders/${selectedOrder.value.id}/update_fulfillment/`, fulfillmentForm.value);
            alert('Order updated!');
            closeFulfillmentModal();
            fetchOrders();
        } catch (err) {
            console.error('Update failed:', err);
            alert('Update failed: ' + (err.response?.data?.error || err.message));
        } finally {
            submittingFulfillment.value = false;
        }
    };
    const quoteRequests = ref([]);
    const loadingQuotes = ref(false);
    const showQuoteModal = ref(false);
    const submittingQuote = ref(false);
    const selectedQuote = ref(null);
    const quoteForm = ref({
        confirmed_price: 0,
        delivery_fee: 0,
        expires_at: ''
    });
    const fetchQuoteRequests = async () => {
        try {
            const res = await api.get('/orders/quote-requests/');
            quoteRequests.value = res.data.results || res.data;
        } catch (err) {
            console.error('Failed to fetch quotes:', err);
        } finally {
            loadingQuotes.value = false;
        }
    };
    const openQuoteResponseModal = (quote) => {
        selectedQuote.value = quote;
        let total = 0;
        quote.items.forEach(item => {
            total += (item.product_details?.base_price || 0) * item.quantity;
        });
        const nextWeek = new Date();
        nextWeek.setDate(nextWeek.getDate() + 7);
        quoteForm.value = {
            confirmed_price: total,
            delivery_fee: 0,
            expires_at: nextWeek.toISOString().split('T')[0]
        };
        showQuoteModal.value = true;
    };
    const closeQuoteModal = () => {
        showQuoteModal.value = false;
        selectedQuote.value = null;
    };
    const submitQuoteResponse = async () => {
        submittingQuote.value = true;
        try {
            await api.post(`/orders/quote-requests/${selectedQuote.value.id}/respond/`, quoteForm.value);
            alert('Quote sent successfully!');
            closeQuoteModal();
            fetchQuoteRequests();
        } catch (err) {
            console.error('Failed to send quote:', err);
            alert('Failed to send quote.');
        } finally {
            submittingQuote.value = false;
        }
    };
    const vendorProfile = ref(null);
    const loadingProfile = ref(true);
    const editingProfile = ref(false);
    const profileForm = ref({
        business_name: '',
        registration_number: '',
        location: '',
        categories_served: []
    });
    const categoriesInput = ref('');
    const showRegistrationForm = ref(false);
    const registering = ref(false);
    const registrationForm = ref({
        business_name: '',
        registration_number: '',
        location: '',
        categories_served: []
    });
    const registrationCategoriesInput = ref('');
    const tabs = ['Basic Info', 'Pricing & Stock', 'Specifications', 'Quality', 'Delivery', 'Images', 'Marketing'];
    const regions = ['NAIROBI', 'MOMBASA', 'KISUMU', 'NAKURU', 'ELDORET'];
    const formData = ref({
        name: '', category: '', short_description: '', description: '', unit: '',
        base_price: null, bulk_price: null, bulk_threshold: null, stock_quantity: 0,
        min_order_quantity: 1, max_order_quantity: null, brand: '', model_number: '',
        weight: null, dimensions: '', color: '', material_composition: '',
        quality_grade: '', certifications: '', warranty_period: '', manufacturing_date: null,
        expiry_date: null, features: '', applications: '', delivery_regions: [],
        estimated_delivery_days: null, shipping_weight: null, requires_special_handling: false,
        handling_instructions: '', meta_keywords: '', is_featured: false,
        is_new_arrival: false, is_on_sale: false, status: 'ACTIVE'
    });
    const fetchMyProducts = async () => {
        if (!vendorProfile.value?.id) {
            products.value = [];
            loading.value = false;
            return;
        }
        loading.value = true;
        try {
            const res = await api.get(`/v1/products/?vendor=${vendorProfile.value.id}&page=${inventoryPage.value}&page_size=${inventoryPageSize}`);
            products.value = res.data.results || res.data;
            inventoryTotal.value = res.data.count || products.value.length;
        } catch (err) {
            console.error('Failed to fetch products:', err);
        } finally {
            loading.value = false;
        }
    };
    const fetchCategories = async () => {
        try {
            const res = await api.get('/taxonomy/categories/?taxonomy_type=MATERIAL');
            categories.value = res.data.results || res.data;
        } catch (err) {
            console.error('Failed to fetch categories:', err);
        }
    };
    const fetchVendorProfile = async () => {
        loadingProfile.value = true;
        try {
            const res = await api.get('/vendors/profiles/me/');
            vendorProfile.value = res.data;
            profileForm.value = {
                business_name: res.data.business_name,
                registration_number: res.data.registration_number,
                location: res.data.location,
                categories_served: res.data.categories_served || []
            };
            categoriesInput.value = (res.data.categories_served || []).join(', ');
        } catch (err) {
            if (err.response?.status !== 404) {
                console.error('Failed to fetch vendor profile:', err);
            }
        } finally {
            loadingProfile.value = false;
        }
    };
    const saveProfile = async () => {
        try {
            if (categoriesInput.value) {
                profileForm.value.categories_served = categoriesInput.value.split(',').map(cat => cat.trim()).filter(cat => cat.length > 0);
            }
            await api.patch(`/vendors/profiles/${vendorProfile.value.id}/`, profileForm.value);
            alert('Profile updated successfully!');
            editingProfile.value = false;
            fetchVendorProfile();
        } catch (err) {
            console.error('Failed to update profile:', err);
            alert('Failed to update profile. Please try again.');
        }
    };
    const cancelEditProfile = () => {
        editingProfile.value = false;
        profileForm.value = {
            business_name: vendorProfile.value.business_name,
            registration_number: vendorProfile.value.registration_number,
            location: vendorProfile.value.location,
            categories_served: vendorProfile.value.categories_served || []
        };
        categoriesInput.value = (vendorProfile.value.categories_served || []).join(', ');
    };
    const registerAsVendor = async () => {
        registering.value = true;
        try {
            if (registrationCategoriesInput.value) {
                registrationForm.value.categories_served = registrationCategoriesInput.value.split(',').map(cat => cat.trim()).filter(cat => cat.length > 0);
            }
            await api.post('/vendors/profiles/', registrationForm.value);
            alert('Vendor registration successful! Your application is pending approval.');
            showRegistrationForm.value = false;
            registrationForm.value = { business_name: '', registration_number: '', location: '', categories_served: [] };
            registrationCategoriesInput.value = '';
            fetchVendorProfile();
        } catch (err) {
            console.error('Failed to register as vendor:', err);
            alert('Failed to register as vendor. ' + (err.response?.data?.detail || 'Please try again.'));
        } finally {
            registering.value = false;
        }
    };
    const downloadTemplate = async () => {
        try {
            const res = await api.get('/v1/products/download_template/', { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'product_import_template.csv');
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error('Failed to download template:', err);
            alert('Failed to download template. Please try again.');
        }
    };
    const triggerImport = () => { if (fileInput.value) { fileInput.value.click(); } };
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        importing.value = true;
        const formData = new FormData();
        formData.append('file', file);
        try {
            const res = await api.post('/v1/products/import_products/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
            let message = res.data.message || 'Import successful';
            if (res.data.errors && res.data.errors.length > 0) {
                const warnings = res.data.errors.slice(0, 5).join('\n');
                message += `\n\nWarnings:\n${warnings}`;
                if (res.data.errors.length > 5) {
                    message += `\n...and ${res.data.errors.length - 5} more warnings (check console)`;
                }
            }
            alert(message);
            event.target.value = '';
            fetchMyProducts();
        } catch (err) {
            console.error('Import failed:', err);
            alert('Import failed: ' + (err.response?.data?.error || err.message));
            event.target.value = '';
        } finally {
            importing.value = false;
        }
    };
    onMounted(async () => {
        await fetchVendorProfile();
        if (vendorProfile.value) { fetchMyProducts(); } else { loading.value = false; }
        fetchCategories();
        fetchQuoteRequests();
        fetchOrders();
    });
    const openAddModal = () => {
        editingProduct.value = null;
        resetForm();
        showAddModal.value = true;
        activeTab.value = 'Basic Info';
    };
    const editProduct = (product) => {
        editingProduct.value = product;
        Object.keys(formData.value).forEach(key => {
            formData.value[key] = product[key] || formData.value[key];
        });
        showAddModal.value = true;
        activeTab.value = 'Basic Info';
    };
    const closeModal = () => {
        showAddModal.value = false;
        resetForm();
        selectedImages.value = [];
        primaryImageIndex.value = 0;
    };
    const resetForm = () => {
        formData.value = {
            name: '', category: '', short_description: '', description: '', unit: '',
            base_price: null, bulk_price: null, bulk_threshold: null, stock_quantity: 0,
            min_order_quantity: 1, max_order_quantity: null, brand: '', model_number: '',
            weight: null, dimensions: '', color: '', material_composition: '',
            quality_grade: '', certifications: '', warranty_period: '', manufacturing_date: null,
            expiry_date: null, features: '', applications: '', delivery_regions: [],
            estimated_delivery_days: null, shipping_weight: null, requires_special_handling: false,
            handling_instructions: '', meta_keywords: '', is_featured: false,
            is_new_arrival: false, is_on_sale: false, status: 'ACTIVE'
        };
    };
    const handleImageUpload = (event) => {
        const files = Array.from(event.target.files);
        files.forEach(file => {
            if (file.size > 5 * 1024 * 1024) { alert(`${file.name} is too large. Max size is 5MB.`); return; }
            const reader = new FileReader();
            reader.onload = (e) => {
                selectedImages.value.push({ file: file, preview: e.target.result, name: file.name });
            };
            reader.readAsDataURL(file);
        });
    };
    const removeImage = (index) => {
        selectedImages.value.splice(index, 1);
        if (primaryImageIndex.value === index) { primaryImageIndex.value = 0; }
        else if (primaryImageIndex.value > index) { primaryImageIndex.value--; }
    };
    const saveProduct = async () => {
        saving.value = true;
        try {
            const productData = { ...formData.value };
            let response;
            if (editingProduct.value) { response = await api.patch(`/v1/products/${editingProduct.value.id}/`, productData); }
            else { response = await api.post('/v1/products/', productData); }
            if (selectedImages.value.length > 0) {
                const formDataImages = new FormData();
                selectedImages.value.forEach((img, idx) => {
                    formDataImages.append('images', img.file);
                    formDataImages.append(`alt_text_${idx}`, `${formData.value.name} - Image ${idx + 1}`);
                });
                await api.post(`/v1/products/${response.data.id}/upload_images/`, formDataImages, { headers: { 'Content-Type': 'multipart/form-data' } });
                if (primaryImageIndex.value !== 0) {
                    const images = await api.get(`/v1/product-images/?product=${response.data.id}`);
                    const primaryImage = images.data.results[primaryImageIndex.value];
                    if (primaryImage) { await api.post(`/v1/product-images/${primaryImage.id}/set_primary/`); }
                }
            }
            alert(editingProduct.value ? 'Product updated successfully!' : 'Product created successfully!');
            closeModal();
            fetchMyProducts();
        } catch (err) {
            console.error('Failed to save product:', err);
            alert('Failed to save product. Please check all required fields.');
        } finally { saving.value = false; }
    };
    const deleteProduct = async (id) => {
        if (!confirm("Delete this product?")) return;
        try {
            await api.delete(`/v1/products/${id}/`);
            products.value = products.value.filter(p => p.id !== id);
            alert('Product deleted successfully!');
        } catch (err) {
            console.error('Failed to delete product:', err);
            alert('Failed to delete product.');
        }
    };
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
</style>
