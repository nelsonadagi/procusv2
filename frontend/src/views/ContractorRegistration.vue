<template>
    <div class="page-container min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Card title="Join as a Contractor" class="w-full max-w-3xl">
            <template #header>
                <div class="pz-u-text-center">
                    <h2 class="pz-u-text-display text-2xl u-mb-2">Contractor Registration</h2>
                    <p class="pz-u-text-mono text-xs pz-u-color-steel">Join our network to access exclusive construction tenders and expand your business.</p>
                </div>
            </template>

            <form @submit.prevent="submitRegistration" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
                <!-- Basic Info -->
                <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
                    <PzInput v-model="form.company_name" label="Company Name" placeholder="e.g. Apex Builders Ltd"
                        required />

                <div class="pz-location-section">
                    <label class="pz-input__label u-mb-2">Business Location</label>
                    <LocationInterface v-model="locationState" @change="handleLocationChange" />
                </div>
                </div>

                <!-- Service Categories -->
                <div class="pz-input-wrapper">
                    <label class="pz-input__label">Select Services Offered</label>
                    <div v-if="loadingCategories" class="pz-u-text-mono text-xs pz-u-color-concrete">Loading services...
                    </div>
                    <div v-else class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-3"
                        style="max-height: 240px; overflow-y: auto;">
                        <div v-for="category in categories" :key="category.id" @click="toggleCategory(category.name)"
                            class="pz-u-border pz-p-3 pz-border-radius-sm cursor-pointer pz-l-flex pz-l-flex--align-center pz-l-flex--justify-between u-hover-spring"
                            :style="form.service_categories.includes(category.name) ? 'background: rgba(212, 101, 42, 0.05); border-color: var(--pz-color-earth-orange); color: var(--pz-color-earth-orange);' : 'background: white; border-color: var(--pz-color-concrete-grey);'">
                            <span class="pz-u-text-mono text-xs">{{ category.name }}</span>
                            <span v-if="form.service_categories.includes(category.name)">✓</span>
                        </div>
                    </div>
                    <p class="pz-u-text-mono text-xs pz-u-color-concrete u-mt-2">Selected: {{
                        form.service_categories.length }}
                        services</p>
                </div>

                <!-- Terms -->
                <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-border-radius-sm">
                    <label
                        class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 pz-u-text-mono text-sm cursor-pointer">
                        <input type="checkbox" v-model="agreedToTerms" required />
                        <span>I verify that my company is legally registered and I agree to the <a href="#"
                                class="pz-u-color-earth hover:underline">Terms of Service</a>.</span>
                    </label>
                </div>

                <div class="u-mt-4">
                    <Button type="submit" variant="primary" size="lg" fullWidth :loading="submitting"
                        :disabled="!isFormValid">
                        Submit Application
                    </Button>
                </div>
            </form>
        </Card>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed, inject } from 'vue';
    import { useRouter } from 'vue-router';
    import api from '../services/api';
    import Card from '../components/ui/Card.vue';
    import Button from '../components/ui/Button.vue';
    import PzInput from '../components/PzInput.vue';
    import LocationInterface from '../components/ui/LocationInterface.vue';

    const router = useRouter();
    const showAlert = inject('showAlert');
    const submitting = ref(false);
    const loadingCategories = ref(true);
    const agreedToTerms = ref(false);

    const form = ref({
        company_name: '',
        location_text: '',
        latitude: null,
        longitude: null,
        formatted_address: '',
        country: null,
        service_categories: [] // Stores 'name' strings
    });

    const locationState = ref({
        lat: -1.2921,
        lng: 36.8219,
        address: '',
        city: '',
        country_id: null
    });

    function handleLocationChange(loc) {
        form.value.latitude = loc.lat;
        form.value.longitude = loc.lng;
        form.value.formatted_address = loc.address;
        form.value.location_text = loc.city;
        form.value.country = loc.country_id;
    }
    const categories = ref([]);

    onMounted(async () => {
        try {
            const res = await api.get('/taxonomy/categories/?taxonomy_type=SERVICE');
            categories.value = res.data.results || res.data;
        } catch (err) {
            console.error("Failed to load categories:", err);
            // Fallback or Alert
        } finally {
            loadingCategories.value = false;
        }
    });

    const toggleCategory = (name) => {
        const index = form.value.service_categories.indexOf(name);
        if (index === -1) {
            form.value.service_categories.push(name);
        } else {
            form.value.service_categories.splice(index, 1);
        }
    };

    const isFormValid = computed(() => {
        return form.value.company_name &&
            form.value.location_text &&
            form.value.service_categories.length > 0 &&
            agreedToTerms.value;
    });

    const submitRegistration = async () => {
        submitting.value = true;
        try {
            await api.post('/contractors/register/', form.value);
            showAlert('Application submitted successfully. Pending admin approval.', 'success');
            router.push('/contractor/dashboard');
        } catch (err) {
            console.error('Registration failed:', err);
            const msg = err.response?.data?.detail || err.response?.data?.error || 'Registration failed.';
            showAlert(msg, 'error');
        } finally {
            submitting.value = false;
        }
    };
</script>

<style scoped>
    /* Additional specific styles if needed beyond layout.css */
</style>
