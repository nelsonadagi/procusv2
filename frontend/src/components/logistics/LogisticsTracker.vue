<template>
    <div class="pz-logistics-tracker">
        <div class="pz-l-grid pz-l-grid--md-cols-12 pz-l-grid--gap-8">

            <!-- 01: Tracking Manifest -->
            <div class="pz-l-grid__col-md-5">
                <div class="pz-admin-card" style="height: 100%;">
                    <div class="pz-admin-card__header">
                        <h3 class="pz-admin-card__title">SHIPMENT_MANIFEST_ID: {{ trackingNumber }}</h3>
                        <Badge v-if="shipment" :variant="getStatusVariant(shipment.status)" size="sm">{{ shipment.status }}</Badge>
                    </div>

                    <div v-if="loading" class="pz-loading-state pz-p-6">
                        <div class="pz-loading-state__indicator"></div>
                        <div class="pz-loading-state__label">POLLING_CARRIER_NODE</div>
                    </div>

                    <div v-else-if="shipment" class="pz-p-6">
                        <div class="pz-l-flex pz-l-flex--justify-between u-mb-8">
                            <div>
                                <div class="pz-u-text-mono text-xs pz-u-color-concrete">CARRIER_RESOURCE</div>
                                <div class="pz-u-text-display">{{ shipment.carrier_name?.toUpperCase() || 'EXTERNAL_PARTNER' }}</div>
                            </div>
                            <div class="text-right">
                                <div class="pz-u-text-mono text-xs pz-u-color-concrete">ETA</div>
                                <div class="pz-u-text-mono font-bold">{{ shipment.expected_delivery ? new Date(shipment.expected_delivery).toLocaleDateString() : 'TBD' }}</div>
                            </div>
                        </div>

                        <div class="pz-u-bg-limestone pz-p-4 pz-u-border u-mb-6">
                            <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2">LOGISTICS_ROUTE</div>
                            <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
                                <div style="flex: 1;">
                                    <div class="pz-u-text-mono text-xs font-bold">ORIGIN</div>
                                    <div class="text-xs">{{ shipment.origin_address }}</div>
                                </div>
                                <div class="pz-u-text-mono" style="font-size: 1.5rem;">➔</div>
                                <div style="flex: 1;">
                                    <div class="pz-u-text-mono text-xs font-bold">DESTINATION</div>
                                    <div class="text-xs">{{ shipment.destination_address }}</div>
                                </div>
                            </div>
                        </div>

                        <div class="pz-tracking-stream">
                            <div class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4">REALTIME_EVENT_LOG</div>
                            <div v-if="shipment.events && shipment.events.length > 0">
                                <div v-for="event in shipment.events" :key="event.id" class="pz-tracking-event">
                                    <div class="pz-tracking-event__marker"></div>
                                    <div class="pz-tracking-event__content">
                                        <div class="pz-l-flex pz-l-flex--justify-between">
                                            <span class="pz-u-text-mono text-xs font-bold">{{ event.status }}</span>
                                            <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ formatDate(event.timestamp) }}</span>
                                        </div>
                                        <div class="text-xs u-mt-1">{{ event.description }}</div>
                                        <div class="pz-u-text-mono text-xs pz-u-color-earth u-mt-1">// LOC: {{ event.location }}</div>
                                    </div>
                                </div>
                            </div>
                             <div v-else class="text-xs pz-u-color-concrete">No tracking events recorded.</div>
                        </div>
                    </div>

                    <div v-else class="pz-empty-state pz-m-6">
                        <div class="pz-empty-state__glyph">TRK</div>
                        <div class="pz-empty-state__eyebrow">Tracking Feed</div>
                        <h4 class="pz-empty-state__title">No shipment telemetry is available for this tracking number.</h4>
                        <p class="pz-empty-state__body">Check that the shipment exists and that the carrier has started pushing status updates.</p>
                    </div>
                </div>
            </div>

            <!-- 02: Interactive Map View -->
            <div class="pz-l-grid__col-md-7">
                <div class="pz-admin-card pz-map-card">
                    <div class="pz-admin-card__header">
                        <h3 class="pz-admin-card__title">TACTICAL_LOCATION_INTEL</h3>
                        <Badge variant="success" size="sm" class="pulse-badge">LIVE_INTEL_ACTIVE</Badge>
                    </div>
                    
                    <div id="logistics-map" class="pz-map-container"></div>
                    
                    <div class="pz-map-overlay pz-u-text-mono text-xs" v-if="currentLocation">
                         <div>LAT: {{ currentLocation.lat.toFixed(4) }}</div>
                         <div>LNG: {{ currentLocation.lng.toFixed(4) }}</div>
                         <div class="u-mt-2 pz-u-color-earth">EN_ROUTE: {{ shipment?.destination_address }}</div>
                    </div>
                </div>
                
                 <!-- Rate Calculator (Zone Pricing) -->
                <div class="pz-admin-card u-mt-6">
                    <div class="pz-admin-card__header">
                        <h3 class="pz-admin-card__title">ZONE_PRICING_CALCULATOR</h3>
                    </div>
                    <div class="pz-p-6">
                         <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-end">
                            <div class="pz-input-wrapper" style="flex: 1;">
                                <label class="pz-input__label">DELIVERY_ZONE</label>
                                <select v-model="calcZone" class="pz-input pz-input--sm">
                                    <option v-for="zone in zones" :key="zone.id" :value="zone.id">{{ zone.name }}</option>
                                </select>
                            </div>
                             <div class="pz-input-wrapper" style="width: 100px;">
                                <label class="pz-input__label">WEIGHT (KG)</label>
                                <input v-model="calcWeight" type="number" class="pz-input pz-input--sm" />
                            </div>
                            <Button @click="calculateRate" :loading="calculating" size="sm">ESTIMATE_COST</Button>
                         </div>
                         
                         <div v-if="calcResult" class="u-mt-4 pz-u-bg-limestone pz-p-4">
                            <div class="pz-l-flex pz-l-flex--justify-between u-mb-2">
                                <span class="pz-u-text-mono text-xs">ESTIMATED_BASE_COST:</span>
                                <span class="font-bold">{{ formatCurrency(calcResult.base_cost) }}</span>
                            </div>
                            <div v-if="calcResult.quotes && calcResult.quotes.length > 0">
                                <div class="pz-u-text-mono text-xs u-mb-2 font-bold">CARRIER_QUOTES:</div>
                                <div v-for="quote in calcResult.quotes" :key="quote.carrier" class="pz-l-flex pz-l-flex--justify-between text-xs u-mb-1">
                                    <span>{{ quote.carrier }} ({{ quote.service_level }})</span>
                                    <span>{{ formatCurrency(quote.price) }}</span>
                                </div>
                            </div>
                         </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, onUnmounted, watch, nextTick, inject } from 'vue';
    import api from '../../services/api';
    import Badge from '../ui/Badge.vue';
    import Button from '../ui/Button.vue';

    const showAlert = inject('showAlert');
    const props = defineProps({
        trackingNumber: {
            type: String,
            required: true
        }
    });

    const shipment = ref(null);
    const loading = ref(true);
    const map = ref(null);
    const marker = ref(null);
    const currentLocation = ref(null);
    const pollInterval = ref(null);
    
    // Calculator
    const zones = ref([]);
    const calcZone = ref(null);
    const calcWeight = ref(1);
    const calculating = ref(false);
    const calcResult = ref(null);

    async function fetchTrackingData() {
        try {
            // Get mock tracking data directly if specific endpoint exists, else simulate
            // In real world: GET /api/logistics/shipments/track/{id}/
            // But we use filter by tracking number then get details
            
            // First get the shipment details from our DB
            const res = await api.get(`/logistics/shipments/?tracking_number=${props.trackingNumber}`);
            const results = res.data.results || res.data;
            
            if (results.length > 0) {
                shipment.value = results[0];
                
                // Now get simulated live update
                if (shipment.value.id) {
                     const trackRes = await api.get(`/logistics/shipments/${shipment.value.id}/track/`);
                     const liveData = trackRes.data.live_update;
                     
                     if (liveData && liveData.lat && liveData.lng) {
                         updateMap(liveData.lat, liveData.lng);
                     }
                }
            }
        } catch (err) {
            console.error("Tracking fetch error", err);
            if (showAlert && loading.value) showAlert("Network Error: Carrier telemetry lost", "error");
        } finally {
            loading.value = false;
        }
    }
    
    function updateMap(lat, lng) {
        currentLocation.value = { lat, lng };
        
        if (!map.value) {
            // Initialize Map
            nextTick(() => {
                const mapEl = document.getElementById('logistics-map');
                const leaflet = window.L;
                if (mapEl && leaflet) {
                    map.value = leaflet.map('logistics-map').setView([lat, lng], 13);
                    
                    leaflet.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                        subdomains: 'abcd',
                        maxZoom: 20
                    }).addTo(map.value);
                    
                    const icon = leaflet.divIcon({
                        className: 'custom-div-icon',
                        html: "<div style='background-color:#c30;width:12px;height:12px;border-radius:50%;box-shadow:0 0 10px #c30;'></div>",
                        iconSize: [12, 12],
                        iconAnchor: [6, 6]
                    });

                    marker.value = leaflet.marker([lat, lng], { icon: icon }).addTo(map.value);
                } else if (showAlert) {
                    showAlert("Map layer unavailable. Tracking data is still available in manifest mode.", "error");
                }
            });
        } else {
            // Update Marker
            if (marker.value) {
                marker.value.setLatLng([lat, lng]);
                map.value.panTo([lat, lng]);
            }
        }
    }

    async function fetchZones() {
        try {
            const res = await api.get('/logistics/pricing-zones/');
            zones.value = res.data.results || res.data;
            if (zones.value.length > 0) calcZone.value = zones.value[0].id;
        } catch (err) {
            console.error(err);
            if (showAlert) showAlert("Sync Error: Zone Matrix unavailable", "error");
        }
    }

    async function calculateRate() {
        if (!calcZone.value) return;
        calculating.value = true;
        try {
            const res = await api.get(`/logistics/pricing-zones/calculate/?zone_id=${calcZone.value}&weight=${calcWeight.value}`);
            calcResult.value = res.data;
            if (showAlert) showAlert("Tariff calculation synchronized", "success");
        } catch (err) {
            if (showAlert) showAlert("Calculation Error: Pricing logic failure", "error");
        } finally {
            calculating.value = false;
        }
    }

    function getStatusVariant(status) {
        if (status === 'DELIVERED') return 'success';
        if (status === 'IN_TRANSIT' || status === 'OUT_FOR_DELIVERY') return 'primary';
        if (status === 'FAILED') return 'danger';
        return 'warning';
    }

    function formatDate(dateStr) {
        return new Date(dateStr).toLocaleTimeString('en-GB', { hour12: false });
    }
    
    function formatCurrency(val) {
        return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(val);
    }

    onMounted(() => {
        fetchTrackingData();
        fetchZones();
        
        // Poll for updates every 5 seconds
        pollInterval.value = setInterval(fetchTrackingData, 5000);
    });
    
    onUnmounted(() => {
        if (pollInterval.value) clearInterval(pollInterval.value);
        if (map.value) {
            map.value.remove();
            map.value = null;
        }
    });
</script>

<style scoped>
    .pz-admin-card {
        background: white;
        border: 1px solid var(--pz-color-foundation-black);
        overflow: hidden;
    }

    .pz-m-6 {
        margin: 1.5rem;
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
        font-size: 0.825rem;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    .pz-tracking-stream {
        position: relative;
        padding-left: var(--pz-space-6);
    }

    .pz-tracking-event {
        position: relative;
        padding-bottom: var(--pz-space-8);
    }

    .pz-tracking-event__marker {
        position: absolute;
        left: -24px;
        top: 4px;
        width: 10px;
        height: 10px;
        background: var(--pz-color-foundation-black);
        border-radius: 50%;
        z-index: 2;
    }

    .pz-tracking-event::before {
        content: '';
        position: absolute;
        left: -20px;
        top: 14px;
        width: 1px;
        height: 100%;
        background: rgba(0, 0, 0, 0.1);
        z-index: 1;
    }

    .pz-tracking-event:last-child {
        padding-bottom: 0;
    }

    .pz-tracking-event:last-child::before {
        display: none;
    }

    /* Tactical Map Styling */
    .pz-map-card {
        height: 400px;
        background: #1e1e1e;
        color: #fff;
        position: relative;
    }
    
    .pz-map-container {
        width: 100%;
        height: 100%;
        z-index: 1;
    }

    .pz-map-overlay {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(0, 255, 0, 0.3);
        padding: 12px;
        pointer-events: none;
        z-index: 1000;
        color: #00ff00;
    }
    
    .pulse-badge {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
