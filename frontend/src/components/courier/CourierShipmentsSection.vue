<template>
  <div class="pz-shipments-section">
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">Shipment Control</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">ACTIVE_LOGISTICS_MANIFEST</h3>
          <div class="pz-section-shell__meta">Assigned shipments currently moving through the courier network.</div>
        </div>
      </div>
      <div v-if="shipments.length === 0" class="pz-section-shell__content">
        <div class="courier-workflow-empty">
          <div class="courier-workflow-empty__kicker">NO_ACTIVE_SHIPMENTS</div>
          <h4 class="courier-workflow-empty__title">No active shipments are currently assigned.</h4>
          <p class="courier-workflow-empty__body">Shipment manifests will appear here as soon as vendor orders are routed to your courier profile.</p>
          <div class="courier-workflow-empty__actions">
            <Button variant="outline" size="sm" @click="showAlert('Use the profile and pricing tabs to finish courier readiness before live shipments arrive.', 'info')">Review Readiness</Button>
          </div>
        </div>
      </div>
      <div v-else class="pz-section-shell__content">
        <div class="pz-table-container pz-data-table-shell">
            <table class="pz-table">
                <thead>
                    <tr>
                        <th>TRACKING_ID</th>
                        <th>DESTINATION</th>
                        <th>STATUS</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="shipment in shipments" :key="shipment.id">
                        <td class="pz-u-text-mono font-bold">{{ shipment.tracking_number }}</td>
                        <td class="text-sm">{{ shipment.destination_address }}</td>
                        <td><Badge :variant="getStatusVariant(shipment.status)">{{ shipment.status }}</Badge></td>
                        <td>
                            <Button size="xs" variant="ghost" @click="viewDetails(shipment)">DETAILS</Button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue';
import api from '../../services/api';
import Badge from '../ui/Badge.vue';
import Button from '../ui/Button.vue';

const shipments = ref([]);
const showAlert = inject('showAlert');

async function fetchShipments() {
    try {
        const res = await api.get('/logistics/shipments/');
        shipments.value = res.data.results || res.data;
    } catch (err) {
        console.error("Fetch shipments error", err);
    }
}

function getStatusVariant(status) {
    if (status === 'DELIVERED') return 'success';
    if (status === 'IN_TRANSIT') return 'primary';
    return 'secondary';
}

function viewDetails(shipment) {
    showAlert(`Tracking node ${shipment.tracking_number} selected. Open shipment telemetry from the linked workflow panel.`, "info");
}

onMounted(fetchShipments);
</script>

<style scoped>
.courier-workflow-empty {
    display: grid;
    gap: 0.75rem;
    padding: 1.25rem;
    border: 1px solid rgba(10, 10, 15, 0.08);
    background: rgba(255, 255, 255, 0.92);
}

.courier-workflow-empty__kicker {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pz-color-earth-orange);
}

.courier-workflow-empty__title {
    margin: 0;
    font-size: 1rem;
}

.courier-workflow-empty__body {
    margin: 0;
    color: var(--pz-color-text-secondary);
    line-height: 1.6;
}

.courier-workflow-empty__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.pz-table {
    width: 100%;
    border-collapse: collapse;
}

.pz-table th {
    text-align: left;
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    color: var(--pz-color-concrete-grey);
    padding: var(--pz-space-4);
    border-bottom: 1px solid rgba(0,0,0,0.1);
}

.pz-table td {
    padding: var(--pz-space-4);
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
</style>
