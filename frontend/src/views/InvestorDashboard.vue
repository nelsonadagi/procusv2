<template>
    <div class="pz-admin-console">
        <div class="pz-l-container pz-admin-console__layout">
            <!-- 01: Portfolio Sidebar -->
            <aside class="pz-admin-console__sidebar">
                <div class="pz-side-nav">
                    <div class="pz-side-nav__group">
                        <h3 class="pz-side-nav__title">CAPITAL_METRICS</h3>
                        <button class="pz-side-nav__item pz-side-nav__item--active">
                            <span class="pz-side-nav__icon">◰</span> PORTFOLIO_VITAL
                        </button>
                        <button class="pz-side-nav__item">
                            <span class="pz-side-nav__icon">◈</span> AGREEMENT_LOGS
                        </button>
                        <button class="pz-side-nav__item">
                            <span class="pz-side-nav__icon">🛡</span> COMPLIANCE_VAULT
                        </button>
                    </div>

                    <div class="pz-side-nav__group u-mt-12">
                        <h3 class="pz-side-nav__title">SYSTEM_CMD</h3>
                        <button class="pz-side-nav__item" @click="$router.push('/')">
                            <span class="pz-side-nav__icon">⇚</span> EXIT_CONSOLE
                        </button>
                    </div>
                </div>
            </aside>

            <!-- 02: Investment Interface -->
            <main class="pz-admin-console__main">
                <header class="pz-admin-console__header">
                    <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
                        <div>
                            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2" style="letter-spacing: 0.3em;">
                                SECURE_IDENTITY: INSTITUTIONAL_INVESTOR // SESSION: ENCRYPTED
                            </div>
                            <h1 class="pz-u-text-display" style="font-size: 2.5rem; line-height: 1;">Asset Control</h1>
                        </div>
                        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
                            <div class="pz-status-indicator pz-status-indicator--pulse"></div>
                            <Badge variant="primary">ALPHA_TIER_ACCESS</Badge>
                        </div>
                    </div>
                </header>

                <!-- Command Nodes (Stats) -->
                <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6 u-mb-12">
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">TOTAL_CAPITAL_COMMITTED</div>
                        <div class="pz-command-node__value pz-u-color-savanna">${{ totalAmount.toLocaleString() }}</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">ACTIVE_PROJECT_NODES</div>
                        <div class="pz-command-node__value">{{ agreements.length }}</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">COMPLIANCE_STATUS</div>
                        <div class="pz-command-node__value"
                            :class="profile?.kyc_status === 'VERIFIED' ? 'pz-u-color-savanna' : 'pz-u-color-earth'">
                            {{ profile?.kyc_status || 'NOT_FOUND' }}
                        </div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                </div>

                <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--lg-cols-3 pz-l-grid--gap-8">
                    <!-- Compliance Module -->
                    <section class="u-lg-col-span-1">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">IDENTITY_VERIFICATION</h3>
                                <Badge :variant="profile?.kyc_status === 'VERIFIED' ? 'success' : 'warning'">
                                    {{ profile?.kyc_status === 'VERIFIED' ? 'SECURE' : 'PENDING' }}
                                </Badge>
                            </div>
                            <div class="pz-p-6">
                                <div v-if="profile" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
                                    <div class="pz-u-border-b pz-pb-4">
                                        <span
                                            class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">KYC_PROTOCOL</span>
                                        <div class="font-bold pz-u-text-mono">{{ profile.kyc_status }}</div>
                                    </div>
                                    <div class="pz-u-border-b pz-pb-4">
                                        <span
                                            class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">ACCREDITATION_LEVEL</span>
                                        <div class="font-bold pz-u-text-mono">{{ profile.accreditation_status }}</div>
                                    </div>
                                    <div class="pz-u-border-b pz-pb-4">
                                        <span
                                            class="pz-u-text-mono text-xs pz-u-color-concrete u-block u-mb-1">LEGAL_JURISDICTION</span>
                                        <div class="font-bold pz-u-text-mono">{{ profile.jurisdiction }}</div>
                                    </div>
                                </div>
                                <div v-else class="u-text-center u-py-12">
                                    <p class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-6">// NO_DATA_DETECTED</p>
                                    <Button variant="primary" block @click="onboard">INITIALIZE_ONBOARDING</Button>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Investment Stream -->
                    <section class="u-lg-col-span-2">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">INVESTMENT_AGREEMENT_STREAM</h3>
                                <span v-if="loading"
                                    class="pz-u-text-mono text-xs pz-u-color-concrete">SYNCING...</span>
                            </div>
                            <div class="pz-table-wrapper">
                                <table class="pz-admin-table">
                                    <thead>
                                        <tr>
                                            <th>ASSET_NODE</th>
                                            <th>CAPITAL_ALLOCATION</th>
                                            <th>PROTOCOL_STATUS</th>
                                            <th class="u-text-right">COMMAND</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="agr in agreements" :key="agr.id">
                                            <td>
                                                <div class="font-bold pz-u-text-mono">PROJECT_#{{ agr.project }}</div>
                                            </td>
                                            <td class="pz-u-text-mono font-bold">
                                                ${{ agr.amount.toLocaleString() }}
                                            </td>
                                            <td>
                                                <Badge :variant="agr.status === 'SIGNED' ? 'success' : 'secondary'">{{
                                                    agr.status }}</Badge>
                                            </td>
                                            <td>
                                                <div class="pz-l-flex pz-l-flex--justify-end">
                                                    <Button v-if="agr.status === 'DRAFT'" variant="primary" size="sm"
                                                        @click="sign(agr.id)">
                                                        EXECUTE_SIGN
                                                    </Button>
                                                    <span v-else
                                                        class="pz-u-text-mono text-xs pz-u-color-concrete">VERIFIED</span>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr v-if="agreements.length === 0">
                                            <td colspan="4"
                                                class="u-text-center pz-u-color-concrete u-py-12 pz-u-text-mono text-xs">
                                                // NO_ACTIVE_AGREEMENTS_DETECTED_IN_LEDGER
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import api from '../services/api';
    import Badge from '../components/ui/Badge.vue';
    import Button from '../components/ui/Button.vue';

    const profile = ref(null);
    const agreements = ref([]);
    const loading = ref(false);

    const totalAmount = computed(() => {
        return agreements.value.reduce((sum, agr) => sum + (parseFloat(agr.amount) || 0), 0);
    });

    onMounted(() => loadData());

    async function loadData() {
        loading.value = true;
        try {
            const pRes = await api.get('/v5/investors/');
            if (pRes.data && pRes.data.length > 0) {
                profile.value = pRes.data[0];
            } else if (pRes.data.results && pRes.data.results.length > 0) {
                profile.value = pRes.data.results[0];
            }

            const aRes = await api.get('/v5/agreements/');
            agreements.value = aRes.data.results || aRes.data;
        } catch (e) {
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    async function onboard() {
        await api.post('/v5/investors/onboard/', { jurisdiction: 'KE' });
        loadData();
    }

    async function sign(id) {
        await api.post(`/v5/agreements/${id}/sign/`);
        loadData();
    }
</script>

<style scoped>
    .pz-admin-console {
        background: var(--pz-color-limestone-white);
        min-height: 100vh;
        padding: var(--pz-space-4) 0;
    }

    @media (min-width: 768px) {
        .pz-admin-console {
            padding: var(--pz-space-8) 0;
        }
    }

    .pz-admin-console__layout {
        display: flex;
        flex-direction: column;
        gap: var(--pz-space-6);
    }

    @media (min-width: 1024px) {
        .pz-admin-console__layout {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: var(--pz-space-8);
        }
    }

    .pz-admin-console__sidebar {
        height: auto;
    }

    @media (min-width: 1024px) {
        .pz-admin-console__sidebar {
            position: sticky;
            top: var(--pz-space-8);
            height: fit-content;
        }
    }

    .pz-admin-console__header {
        margin-bottom: var(--pz-space-6);
        padding-bottom: var(--pz-space-4);
        border-bottom: 2px solid var(--pz-color-foundation-black);
    }

    @media (min-width: 768px) {
        .pz-admin-console__header {
            margin-bottom: var(--pz-space-8);
            padding-bottom: var(--pz-space-6);
        }
    }

    /* Command Nodes */
    .pz-command-node {
        background: white;
        border: 1px solid var(--pz-color-foundation-black);
        padding: var(--pz-space-4);
        position: relative;
        overflow: hidden;
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

    .pz-command-node:hover .pz-command-node__accent {
        background: var(--pz-color-earth-orange);
    }

    /* Admin Cards & Tables */
    .pz-admin-card {
        background: white;
        border: 1px solid var(--pz-color-concrete-grey);
    }

    .pz-admin-card__header {
        padding: var(--pz-space-4) var(--pz-space-6);
        border-bottom: 1px solid var(--pz-color-concrete-grey);
        display: flex;
        flex-direction: column;
        gap: var(--pz-space-3);
        align-items: flex-start;
    }

    @media (min-width: 640px) {
        .pz-admin-card__header {
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
        }
    }

    .pz-admin-card__title {
        font-family: var(--pz-font-mono);
        font-size: 0.875rem;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    .pz-table-wrapper {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    .pz-admin-table {
        width: 100%;
        border-collapse: collapse;
        min-width: 600px;
    }

    .pz-admin-table th {
        text-align: left;
        padding: var(--pz-space-3) var(--pz-space-6);
        font-family: var(--pz-font-mono);
        font-size: 0.65rem;
        color: var(--pz-color-concrete-grey);
        border-bottom: 1px solid var(--pz-color-concrete-grey);
        background: var(--pz-color-limestone-white);
    }

    .pz-admin-table td {
        padding: var(--pz-space-4) var(--pz-space-6);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        vertical-align: middle;
    }

    .u-lg-col-span-1 {
        grid-column: span 1;
    }

    .u-lg-col-span-2 {
        grid-column: span 2;
    }
</style>
