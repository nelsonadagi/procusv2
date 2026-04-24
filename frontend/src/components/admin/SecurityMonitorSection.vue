<template>
    <div class="security-monitor">
        <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6 u-mb-12">
            <div class="pz-command-node">
                <div class="pz-command-node__label">ACTIVE_THROTTLES_24H</div>
                <div class="pz-command-node__value">{{ totalViolations }}</div>
                <div class="pz-command-node__accent"></div>
            </div>
            <div class="pz-command-node">
                <div class="pz-command-node__label">UNIQUE_IPS_BLOCKED</div>
                <div class="pz-command-node__value pz-u-color-earth">{{ uniqueIps }}</div>
                <div class="pz-command-node__accent" style="background: var(--pz-color-earth-orange);"></div>
            </div>
            <div class="pz-command-node">
                <div class="pz-command-node__label">CRITICAL_SCOPES_HIT</div>
                <div class="pz-command-node__value">{{ criticalHits }}</div>
                <div class="pz-command-node__accent"></div>
            </div>
        </div>

        <div class="pz-admin-card pz-section-shell">
            <div class="pz-admin-card__header pz-section-shell__header">
                <div>
                    <div class="pz-section-shell__eyebrow">Security Monitor</div>
                    <h3 class="pz-admin-card__title pz-section-shell__title">THROTTLE_VIOLATION_LOG</h3>
                    <div class="pz-section-shell__meta">Observed throttling and access-scope pressure across secured resources.</div>
                </div>
                <Button variant="ghost" size="sm" @click="fetchViolations">SYNC_LOGS</Button>
            </div>

            <div v-if="loading" class="pz-section-shell__content">
                <div class="pz-loading-state">
                    <div class="pz-loading-state__indicator"></div>
                    <div class="pz-loading-state__label">PARSING_SECURITY_PROTOCOLS</div>
                </div>
            </div>

            <div v-else-if="violations.length === 0" class="pz-section-shell__content">
                <div class="pz-empty-state">
                    <div class="pz-empty-state__glyph">SEC</div>
                    <div class="pz-empty-state__eyebrow">Security Feed</div>
                    <h4 class="pz-empty-state__title">No security violations were detected in the current window.</h4>
                    <p class="pz-empty-state__body">Throttle hits and abnormal scope events will appear here when they are logged.</p>
                </div>
            </div>

            <div v-else class="pz-table-wrapper pz-section-shell__content pz-data-table-shell">
                <table class="pz-admin-table">
                    <thead>
                        <tr>
                            <th>TIMESTAMP</th>
                            <th>IP_ADDRESS</th>
                            <th>OPERATOR</th>
                            <th>RESOURCE_PATH</th>
                            <th>SCOPE</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="violation in violations" :key="violation.id">
                            <td class="pz-u-text-mono text-xs">{{ formatDate(violation.timestamp) }}</td>
                            <td class="pz-u-text-mono font-bold">{{ violation.ip_address }}</td>
                            <td>
                                <div v-if="violation.user_email" class="pz-u-text-mono text-xs">{{ violation.user_email
                                    }}</div>
                                <div v-else class="pz-u-text-mono text-xs pz-u-color-concrete">ANONYMOUS_ACTOR</div>
                            </td>
                            <td class="pz-u-text-mono text-xs">
                                <Badge variant="ghost" size="sm">{{ violation.method }}</Badge> {{ violation.path }}
                            </td>
                            <td>
                                <Badge :variant="getScopeVariant(violation.scope)" size="sm">{{ violation.scope ||
                                    'GLOBAL' }}</Badge>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import api from '../../services/api';
    import Button from '../ui/Button.vue';
    import Badge from '../ui/Badge.vue';

    const violations = ref([]);
    const loading = ref(true);

    const totalViolations = computed(() => violations.value.length);
    const uniqueIps = computed(() => new Set(violations.value.map(v => v.ip_address)).size);
    const criticalHits = computed(() => violations.value.filter(v => v.scope === 'auth_sensitive').length);

    async function fetchViolations() {
        loading.value = true;
        try {
            const res = await api.get('/security/violations/');
            violations.value = res.data.results || res.data;
        } catch (err) {
            console.error("Failed to fetch violations", err);
        } finally {
            loading.value = false;
        }
    }

    function formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleString('en-GB', {
            hour12: false,
            year: 'numeric',
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).toUpperCase();
    }

    function getScopeVariant(scope) {
        if (scope === 'auth_sensitive') return 'danger';
        if (scope === 'payment_gateway') return 'warning';
        return 'secondary';
    }

    onMounted(fetchViolations);
</script>

<style scoped>
    .pz-command-node {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(10, 10, 15, 0.08);
        padding: var(--pz-space-4);
        position: relative;
        overflow: hidden;
        box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
    }

    .pz-command-node__label {
        font-family: var(--pz-font-mono);
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--pz-color-concrete-grey);
        margin-bottom: var(--pz-space-2);
    }

    .pz-command-node__value {
        font-family: var(--pz-font-display);
        font-size: 1.75rem;
        font-weight: 800;
    }

    .pz-command-node__accent {
        position: absolute;
        top: 0;
        right: 0;
        width: 4px;
        height: 100%;
        background: var(--pz-color-foundation-black);
    }

    .pz-admin-table {
        width: 100%;
        border-collapse: collapse;
    }

    .pz-admin-table th {
        text-align: left;
        padding: var(--pz-space-3) var(--pz-space-6);
        font-family: var(--pz-font-mono);
        font-size: 0.65rem;
        color: var(--pz-color-concrete-grey);
        border-bottom: 1px solid var(--pz-color-foundation-black);
        background: var(--pz-color-limestone-white);
    }

    .pz-admin-table td {
        padding: var(--pz-space-4) var(--pz-space-6);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        vertical-align: middle;
    }
</style>
