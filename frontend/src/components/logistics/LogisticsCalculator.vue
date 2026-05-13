<template>
    <div class="pz-admin-card pz-u-border-thick u-h-full">
        <div class="pz-admin-card__header">
            <h3 class="pz-admin-card__title">DELIVERY_QUOTATION_ENGINE</h3>
        </div>

        <div class="pz-p-6 pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">LOGISTICS_PARAMETERS</div>
            
            <div class="pz-input-wrapper">
                <label class="pz-input__label">TARGET_DELIVERY_ZONE</label>
                <select v-model="selectedZone" class="pz-input">
                    <option disabled value="">SELECT_ZONE...</option>
                    <option v-for="zone in zones" :key="zone.id" :value="zone.id">
                        {{ zone.name.toUpperCase() }}
                    </option>
                </select>
            </div>

            <PzInput v-model="weight" label="ESTIMATED_PAYLOAD_WEIGHT (KG)" type="number" step="0.1" placeholder="0.00" />

            <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center mt-4" style="border-style: dashed;">
                <div>
                    <div class="pz-u-text-mono text-[10px] pz-u-color-concrete">ESTIMATED_FULFILLMENT_COST</div>
                    <div class="pz-u-text-display text-2xl">{{ displayCost }}</div>
                </div>
                <div class="u-text-right">
                    <div class="pz-u-text-mono text-[10px] pz-u-color-concrete">SLA_LEAD_TIME</div>
                    <div class="pz-u-text-mono font-bold text-xs">{{ estimatedDays }} BUSINESS_DAYS</div>
                </div>
            </div>

            <Button variant="primary" block @click="performCalculation" :loading="loading" style="background: var(--pz-color-earth-orange); border: none;">
                GENERATE_LOGISTICS_QUOTE
            </Button>
            
            <div class="pz-u-text-mono text-[10px] pz-u-color-concrete text-center">
                // DATA_SOURCE: PROCUS_LOGISTICS_NODE_V1.2
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed, inject } from 'vue';
    import api from '../../services/api';
    import { useConfigStore } from '../../stores/config';
    import Button from '../ui/Button.vue';
    import PzInput from '../PzInput.vue';

    const showAlert = inject('showAlert');
    const configStore = useConfigStore();
    const zones = ref([]);
    const selectedZone = ref('');
    const weight = ref(0);
    const loading = ref(false);
    const calculatedCost = ref(0);
    const displayCost = computed(() => configStore.formatPrice ? configStore.formatPrice(calculatedCost.value, 'KES') : `KES ${Number(calculatedCost.value || 0).toLocaleString()}`);

    async function fetchZones() {
        try {
            const res = await api.get('/logistics/pricing-zones/');
            zones.value = res.data.results || res.data;
        } catch (err) {
            console.error("Failed to fetch zones", err);
            if (showAlert) showAlert("Sync Error: Logistics Hub registry unreachable", "error");
        }
    }

    async function performCalculation() {
        if (!selectedZone.value) return;

        loading.value = true;
        try {
            const res = await api.get(`/logistics/pricing-zones/calculate/`, {
                params: { zone_id: selectedZone.value, weight: weight.value }
            });
            const quotes = Array.isArray(res.data.quotes) ? res.data.quotes : [];
            const cheapestQuote = quotes.reduce((lowest, quote) => {
                if (!lowest) return quote;
                return Number(quote.price) < Number(lowest.price) ? quote : lowest;
            }, null);
            const amount = cheapestQuote?.price ?? res.data.base_cost ?? 0;
            calculatedCost.value = Number(amount || 0);
            if (showAlert) showAlert("Logistics quotation recalculated successfully", "info");
        } catch (err) {
            console.error("Calculation error", err);
            if (showAlert) showAlert("Tariff Engine Error: Calculation failed", "error");
        } finally {
            loading.value = false;
        }
    }

    const estimatedDays = computed(() => {
        const zone = zones.value.find(z => z.id === selectedZone.value);
        if (!zone) return '--';
        if (zone.radius_km <= 10) return 1;
        if (zone.radius_km <= 25) return 2;
        return 3;
    });

    onMounted(fetchZones);
</script>

<style scoped>
    .pz-u-border-thick {
        border-width: 2px;
    }
</style>
