<template>
    <div class="vendor-quotes-section">
        <div class="pz-admin-card pz-section-shell">
            <div class="pz-admin-card__header pz-section-shell__header">
                <div>
                    <div class="pz-section-shell__eyebrow">Commercial Response</div>
                    <h3 class="pz-admin-card__title pz-section-shell__title">INBOUND_PROCUREMENT_REQUESTS</h3>
                    <div class="pz-section-shell__meta">Review requests, price line items, and issue proposals.</div>
                </div>
                <Button variant="ghost" size="sm" @click="fetchQuotes">REFRESH_STREAM</Button>
            </div>

            <div class="pz-section-shell__content">
                <div v-if="loading" class="pz-loading-state">
                    <div class="pz-loading-state__indicator"></div>
                    <div class="pz-loading-state__label">STREAMING_QUOTE_REQUESTS</div>
                </div>
                <div v-else-if="quotes.length === 0" class="pz-empty-state">
                    <div class="pz-empty-state__glyph">QTE</div>
                    <div class="pz-empty-state__eyebrow">Quote Stream</div>
                    <h4 class="pz-empty-state__title">No active procurement requests are waiting.</h4>
                    <p class="pz-empty-state__body">When buyers request pricing, their commercial briefs will appear here for response.</p>
                </div>
                <div v-else class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
                    <div v-for="quote in quotes" :key="quote.id" class="pz-quote-card">
                        <div class="pz-l-flex pz-l-flex--justify-between u-mb-4">
                            <div>
                                <div class="pz-u-text-mono font-bold text-sm">REQ #{{ quote.id }}</div>
                                <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ quote.buyer_name }}</div>
                            </div>
                            <Badge :variant="quote.status === 'REQUESTED' ? 'warning' : 'success'">{{ quote.status }}
                            </Badge>
                        </div>

                        <div class="pz-u-bg-limestone pz-p-4 u-mb-4">
                            <div v-for="item in quote.items" :key="item.id"
                                class="pz-l-flex pz-l-flex--justify-between text-xs u-mb-1">
                                <span>{{ item.quantity }}x {{ item.product_details?.name || 'Unknown Item' }}</span>
                                <span class="pz-u-text-mono font-bold">{{
                                    configStore.formatPrice(item.product_details?.base_price) }} (Base)</span>
                            </div>
                        </div>

                        <div class="pz-l-flex pz-l-flex--justify-end" v-if="quote.status === 'REQUESTED'">
                            <Button size="sm" variant="primary"
                                @click="openResponseModal(quote)">PREPARE_RESPONSE</Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Response Modal -->
        <Modal :isOpen="showResponseModal" title="GENERATE_COMMERCIAL_PROPOSAL" size="lg"
            @close="showResponseModal = false">
            <form id="quote-response-form" @submit.prevent="submitQuoteResponse">
                <div class="pz-u-bg-limestone pz-p-4 u-mb-6 pz-u-border">
                    <div class="pz-u-text-mono text-xs font-bold u-mb-2">LINE_ITEM_PRICING</div>
                    <div v-for="(item, idx) in responseForm.items" :key="item.id"
                        class="pz-l-grid pz-l-grid--cols-12 pz-l-grid--gap-4 pz-l-grid--align-center u-mb-2">
                        <div class="pz-l-grid__col-span-4 text-xs">{{ item.product_name }} (x{{ item.quantity }})</div>
                        <div class="pz-l-grid__col-span-3">
                            <input type="number" v-model="item.unit_price" class="pz-input pz-input--sm"
                                placeholder="Unit Price" required>
                        </div>
                        <div class="pz-l-grid__col-span-5">
                            <input type="text" v-model="item.availability_notes" class="pz-input pz-input--sm"
                                placeholder="Notes (e.g. In Stock)">
                        </div>
                    </div>
                </div>

                <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
                    <PzInput v-model="responseForm.delivery_fee"
                        :label="`LOGISTICS_SURCHARGE (${configStore.activeCurrency.symbol})`" type="number" />
                    <PzInput type="date" v-model="responseForm.valid_until" label="PROPOSAL_EXPIRY_DATE" />
                </div>
            </form>
            <template #footer>
                <Button variant="ghost" @click="showResponseModal = false">CANCEL</Button>
                <Button type="submit" form="quote-response-form" variant="primary"
                    :loading="submitting">TRANSMIT_PROPOSAL</Button>
            </template>
        </Modal>
    </div>
</template>

<script setup>
    import { ref, onMounted, inject } from 'vue';
    import api from '../../services/api';
    import Button from '../ui/Button.vue';
    import Badge from '../ui/Badge.vue';
    import Modal from '../ui/Modal.vue';
    import PzInput from '../PzInput.vue';
    import { useConfigStore } from '../../stores/config';

    const configStore = useConfigStore();
    const quotes = ref([]);
    const loading = ref(true);
    const showResponseModal = ref(false);
    const submitting = ref(false);
    const selectedQuote = ref(null);
    const showAlert = inject('showAlert');

    const responseForm = ref({
        items: [],
        delivery_fee: 0,
        valid_until: ''
    });

    async function fetchQuotes() {
        loading.value = true;
        try {
            const res = await api.get('/orders/quote-requests/vendor_quotes/');
            quotes.value = res.data.results || res.data;
        } catch (err) {
            console.error("Fetch quotes error", err);
        } finally {
            loading.value = false;
        }
    }

    function openResponseModal(quote) {
        selectedQuote.value = quote;
        responseForm.value = {
            items: quote.items.map(item => ({
                id: item.id,
                product_name: item.product_details?.name,
                quantity: item.quantity,
                unit_price: item.product_details?.base_price,
                availability_notes: 'In Stock'
            })),
            delivery_fee: 50,
            valid_until: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        };
        showResponseModal.value = true;
    }

    async function submitQuoteResponse() {
        submitting.value = true;
        try {
            await api.post(`/orders/quote-requests/${selectedQuote.value.id}/respond/`, {
                items: responseForm.value.items.map(i => ({
                    id: i.id,
                    unit_price: i.unit_price,
                    availability_notes: i.availability_notes
                })),
                delivery_fee: responseForm.value.delivery_fee,
                valid_until: responseForm.value.valid_until
            });
            if (showAlert) showAlert("Proposal transmitted securely", "success");
            showResponseModal.value = false;
            fetchQuotes();
        } catch (err) {
            if (showAlert) showAlert("Failed to transmit proposal", "error");
        } finally {
            submitting.value = false;
        }
    }

    onMounted(fetchQuotes);
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

    .pz-quote-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(10, 10, 15, 0.08);
        padding: var(--pz-space-6);
        transition: border-color 0.2s, transform 0.2s;
        box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
    }

    .pz-quote-card:hover {
        border-color: var(--pz-color-primary);
        transform: translate(-2px, -2px);
    }
</style>
