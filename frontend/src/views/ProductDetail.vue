<template>
    <div class="l-product-detail u-mb-20">
        <div v-if="loading" class="l-flex l-flex--center u-p-20 l-flex--column">
            <div class="c-loader u-mb-4"></div>
            <p>Loading construction materials...</p>
        </div>

        <div v-else-if="error" class="l-container u-p-20 u-text-center">
            <div class="c-alert c-alert--danger u-mb-6">{{ error }}</div>
            <Button variant="primary" @click="$router.push('/')">Back to Marketplace</Button>
        </div>

        <div v-if="product" class="pz-l-container u-py-8">
            <!-- Premium Breadcrumb -->
            <nav class="pz-breadcrumb u-mb-8 pz-u-text-mono text-xs">
                <router-link to="/" class="pz-breadcrumb__item">MARKETPLACE</router-link>
                <span class="pz-breadcrumb__separator">//</span>
                <span class="pz-breadcrumb__current pz-u-color-steel">{{ product.name }}</span>
            </nav>

            <div class="pz-l-dashboard">
                <!-- Left: Image Gallery Module -->
                <div class="pz-gallery">
                    <div class="pz-gallery__main pz-u-border">
                        <img :src="selectedImage || product.primary_image_url || '/placeholder.png'" :alt="product.name"
                            class="pz-gallery__image">
                        <div class="pz-gallery__badges">
                            <Badge v-if="product.is_featured" variant="earth" size="large">FEATURED ASSET</Badge>
                            <Badge v-if="product.is_on_sale" variant="finance" size="large">EFFICIENCY YIELD</Badge>
                        </div>
                    </div>

                    <div v-if="product.images && product.images.length > 1"
                        class="c-gallery__thumbs l-grid l-grid--cols-4 l-grid--gap-4 u-mt-4">
                        <div v-for="img in product.images" :key="img.id"
                            class="c-gallery__thumb c-card c-card--interactive"
                            :class="{ 'c-gallery__thumb--active': selectedImage === img.image_url }"
                            @click="selectedImage = img.image_url">
                            <img :src="img.image_url" :alt="img.alt_text">
                        </div>
                    </div>
                </div>

                <!-- Right: Product Information Module -->
                <div class="pz-product-details">
                    <div class="u-mb-4">
                        <Badge variant="savanna">{{ product.category?.name || 'MATERIAL' }}</Badge>
                    </div>
                    <h1 class="pz-u-text-display text-4xl u-mb-2">{{ product.name }}</h1>
                    <p class="pz-u-text-mono text-sm pz-u-color-steel u-mb-8">ASSET IDENTIFIER: {{ product.model_number
                        || 'N/A' }}</p>

                    <div class="pz-l-flex pz-l-flex--gap-6 u-mb-10 pz-u-text-mono text-xs pz-u-color-concrete">
                        <span v-if="product.brand">BRAND: {{ product.brand }}</span>
                        <span>VENDOR: {{ product.vendor_business_name }}</span>
                    </div>

                    <!-- Pricing Card -->
                    <div class="pz-p-6 pz-u-bg-limestone pz-u-border u-mb-8">
                        <div class="pz-l-flex pz-l-flex--align-end pz-l-flex--gap-2 u-mb-2">
                            <span class="pz-u-text-display text-5xl pz-u-color-earth">${{ product.base_price }}</span>
                            <span class="pz-u-text-mono text-lg pz-u-color-steel">/ {{ product.unit }}</span>
                        </div>

                        <div v-if="product.bulk_price" class="pz-u-border-t u-mt-4 u-pt-4">
                            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-2">
                                <Badge variant="finance" size="small">BULK SCALE AVAILABLE</Badge>
                                <span class="pz-u-text-mono text-xs">${{ product.bulk_price }} @ {{
                                    product.bulk_threshold }}+ UNITS</span>
                            </div>
                        </div>
                    </div>

                    <!-- Availability & Logistics -->
                    <div class="c-card u-mb-8">
                        <div class="c-card__body l-grid l-grid--cols-1 l-grid--gap-4">
                            <div class="l-flex l-flex--align-center l-flex--gap-3">
                                <span :class="product.is_in_stock ? 'u-color-success' : 'u-color-danger'">●</span>
                                <span class="font-medium">{{ product.is_in_stock ? 'In Stock' : 'Out of Stock' }}</span>
                                <span class="u-color-muted text-sm" v-if="product.is_in_stock">({{
                                    product.stock_quantity }} {{ product.unit }}s available)</span>
                            </div>

                            <div class="l-flex l-flex--align-center l-flex--gap-3 text-sm u-color-muted">
                                <span>🚚</span>
                                <span>Est. Delivery: {{ product.estimated_delivery_days || '3-5' }} days</span>
                            </div>
                        </div>
                    </div>

                    <!-- Main Actions -->
                    <div class="l-flex l-flex--gap-4">
                        <Button variant="primary" size="lg" block @click="requestQuote"
                            :disabled="!product.is_in_stock">
                            Request Professional Quote
                        </Button>
                        <Button variant="outline" size="lg" @click="contactVendor">Contact</Button>
                    </div>
                </div>
            </div>

            <!-- Extended Details Tabs -->
            <div class="pz-tabs pz-p-6 pz-u-border pz-u-bg-limestone u-mt-16">
                <div class="pz-tabs__nav">
                    <button v-for="tab in detailTabs" :key="tab" class="pz-tabs__btn"
                        :class="{ 'pz-tabs__btn--active': activeTab === tab }" @click="activeTab = tab">
                        {{ tab }}
                    </button>
                </div>

                <div class="c-card__body">
                    <div v-if="activeTab === 'Description'" class="u-fade-in">
                        <h3 class="u-mb-4">Description</h3>
                        <p class="u-line-height-relaxed u-color-muted">{{ product.description }}</p>
                    </div>

                    <div v-if="activeTab === 'Specifications'" class="u-fade-in">
                        <table class="c-table u-w-full">
                            <tr v-if="product.brand">
                                <td class="u-font-bold u-p-4 u-border-b">Brand</td>
                                <td class="u-p-4 u-border-b">{{ product.brand }}</td>
                            </tr>
                            <tr v-if="product.quality_grade">
                                <td class="u-font-bold u-p-4 u-border-b">Grade</td>
                                <td class="u-p-4 u-border-b">{{ product.quality_grade }}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import api from '../services/api';
    import { useAuthStore } from '../stores/auth';

    // UI Components
    import Button from '../components/ui/Button.vue';
    import Badge from '../components/ui/Badge.vue';

    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    const product = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const selectedImage = ref(null);
    const activeTab = ref('Description');
    const relatedProducts = ref([]);

    const detailTabs = ['Description', 'Specifications', 'Logistics', 'Compliance'];

    const fetchProduct = async () => {
        loading.value = true;
        error.value = null;
        try {
            const productId = route.params.id;
            const response = await api.get(`/v1/products/${productId}/`);
            product.value = response.data;
            if (product.value.primary_image_url) selectedImage.value = product.value.primary_image_url;
        } catch (err) {
            error.value = 'Product not found or unavailable.';
        } finally {
            loading.value = false;
        }
    };

    const requestQuote = async () => {
        if (!authStore.isAuthenticated) {
            alert('Please login to request a quote');
            router.push('/login');
            return;
        }
        try {
            await api.post('/orders/quote-requests/', {
                items: [{ product: product.value.id, quantity: product.value.min_order_quantity || 1 }]
            });
            alert('Quote request sent successfully!');
            router.push('/buyer/dashboard');
        } catch (err) {
            alert('Failed to request quote.');
        }
    };

    const contactVendor = () => alert('Contact feature coming soon!');

    onMounted(fetchProduct);
</script>

<style scoped>
    .pz-breadcrumb__item {
        color: var(--pz-color-earth-orange);
        text-decoration: none;
    }

    .pz-breadcrumb__separator {
        color: var(--pz-color-concrete-grey);
    }

    .pz-gallery__main {
        position: relative;
        aspect-ratio: 1/1;
        background: var(--pz-color-limestone-white);
        overflow: hidden;
    }

    .pz-gallery__image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .pz-gallery__badges {
        position: absolute;
        top: var(--pz-space-4);
        left: var(--pz-space-4);
        display: flex;
        flex-direction: column;
        gap: var(--pz-space-2);
    }

    .pz-spec-table {
        width: 100%;
        border-collapse: collapse;
    }

    .pz-spec-table td {
        padding: var(--pz-space-4);
        border-bottom: 1px solid var(--pz-color-limestone-white);
        background: var(--pz-color-limestone-white);
    }

    .pz-spec-table tr:hover td {
        background: var(--pz-color-limestone-white);
        border-color: var(--pz-color-earth-orange);
    }

    .pz-spec-label {
        font-family: var(--pz-font-mono);
        font-size: 0.75rem;
        color: var(--pz-color-concrete-grey);
        width: 200px;
    }

    .pz-spec-value {
        font-family: var(--pz-font-primary);
        color: var(--pz-color-foundation-black);
    }
</style>
