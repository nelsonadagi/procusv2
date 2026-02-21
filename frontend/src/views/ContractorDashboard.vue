<template>
    <div class="pz-admin-console">
        <div class="pz-l-container pz-admin-console__layout">
            <!-- 01: Execution Sidebar -->
            <aside class="pz-admin-console__sidebar">
                <div class="pz-side-nav">
                    <div class="pz-side-nav__group">
                        <h3 class="pz-side-nav__title">EXECUTION_MGMT</h3>
                        <button @click="activeSection = 'bids'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'bids' }">
                            <span class="pz-side-nav__icon">📜</span> ACTIVE_BIDS
                        </button>
                        <button @click="activeSection = 'jobs'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'jobs' }">
                            <span class="pz-side-nav__icon">🏗️</span> ACTIVE_JOBS
                        </button>
                        <button @click="activeSection = 'my-tenders'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'my-tenders' }">
                            <span class="pz-side-nav__icon">📝</span> POSTED_TENDERS
                        </button>
                        <button @click="$router.push('/tenders')" class="pz-side-nav__item">
                            <span class="pz-side-nav__icon">🔍</span> FIND_TENDERS
                        </button>
                        <button @click="activeSection = 'profile'" class="pz-side-nav__item"
                            :class="{ 'pz-side-nav__item--active': activeSection === 'profile' }">
                            <span class="pz-side-nav__icon">👤</span> OPERATOR_PROFILE
                        </button>
                    </div>

                    <div class="pz-side-nav__group u-mt-12">
                        <h3 class="pz-side-nav__title">SYSTEM_EXIT</h3>
                        <button class="pz-side-nav__item" @click="$router.push('/')">
                            <span class="pz-side-nav__icon">⇚</span> EXIT_CONSOLE
                        </button>
                    </div>
                </div>
            </aside>

            <!-- 02: Operational Interface -->
            <main class="pz-admin-console__main">
                <header class="pz-admin-console__header">
                    <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
                        <div>
                            <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2" style="letter-spacing: 0.3em;">
                                OPERATOR: {{ profile?.company_name || 'AUTHENTICATING' }} // STATUS: {{
                                    profile?.verified_status || 'PENDING' }}
                            </div>
                            <h1 class="pz-u-text-display" style="font-size: 2.5rem; line-height: 1;">Execution Hub</h1>
                        </div>
                        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
                            <div class="pz-status-indicator pz-status-indicator--pulse"></div>
                            <Badge :variant="profile?.verified_status === 'APPROVED' ? 'success' : 'warning'">
                                {{ profile?.verified_status === 'APPROVED' ? 'NOMINAL' : 'LIMIT_ACCESS' }}
                            </Badge>
                        </div>
                    </div>
                </header>

                <!-- Command Nodes (Stats) -->
                <div class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6 u-mb-8">
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">ACTIVE_PROPOSALS</div>
                        <div class="pz-command-node__value">{{ pendingBids.length }}</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">AWARDED_JOBS</div>
                        <div class="pz-command-node__value pz-u-color-savanna">{{ activeJobs.length }}</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">BID_SUCCESS_RATE</div>
                        <div class="pz-command-node__value pz-u-color-earth">74%</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node">
                        <div class="pz-command-node__label">SYSTEM_RATING</div>
                        <div class="pz-command-node__value">4.9</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                </div>

                <div class="pz-admin-console__content">
                    <!-- ACTIVE BIDS -->
                    <div v-if="activeSection === 'bids'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">SUBMITTED_PROPOSALS_STREAM</h3>
                                <Button size="sm" variant="outline" @click="fetchBids">SYNCHRONIZE</Button>
                            </div>

                            <div class="pz-table-wrapper">
                                <table class="pz-admin-table">
                                    <thead>
                                        <tr>
                                            <th>PROJECT_ID</th>
                                            <th>SUBMISSION_DATE</th>
                                            <th>QUOTED_VALUATION</th>
                                            <th>STATUS</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="bid in pendingBids" :key="bid.id">
                                            <td>
                                                <div class="font-bold">{{ bid.contract_title || 'NODE_#00' +
                                                    bid.contract }}</div>
                                            </td>
                                            <td class="pz-u-text-mono text-xs">{{ new
                                                Date(bid.created_at).toLocaleDateString() }}</td>
                                            <td class="pz-u-text-mono font-bold">${{ bid.proposed_cost }}</td>
                                            <td>
                                                <Badge :variant="getBidStatusVariant(bid.status)">{{ bid.status }}
                                                </Badge>
                                            </td>
                                        </tr>
                                        <tr v-if="pendingBids.length === 0">
                                            <td colspan="4"
                                                class="u-text-center pz-u-color-concrete u-py-12 pz-u-text-mono text-xs">
                                                // NO_ACTIVE_PROPOSALS_DETECTED
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- ACTIVE JOBS -->
                    <div v-if="activeSection === 'jobs'" class="pz-l-grid pz-l-grid--columns-1 pz-l-grid--gap-6">
                        <div v-for="job in activeJobs" :key="job.id" class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">LIVE_EXECUTION: {{ job.contract_title || 'JOB_#' +
                                    job.id }}</h3>
                                <Badge variant="success">IN_PROGRESS</Badge>
                            </div>
                            <div class="pz-p-6">
                                <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-12 pz-l-flex--align-center">
                                    <div>
                                        <h4 class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4">ALLOCATION_METRICS
                                        </h4>
                                        <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                                            <div class="pz-l-flex pz-l-flex--justify-between">
                                                <span class="pz-u-text-mono text-xs">VALUATION:</span>
                                                <span class="pz-u-text-mono text-xs font-bold">${{ job.proposed_cost
                                                }}</span>
                                            </div>
                                            <div class="pz-l-flex pz-l-flex--justify-between">
                                                <span class="pz-u-text-mono text-xs">DURATION:</span>
                                                <span class="pz-u-text-mono text-xs font-bold">{{
                                                    job.proposed_timeline_days }} DAYS</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="pz-u-bg-limestone pz-p-4 pz-u-border u-text-center">
                                        <p class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2">COMPLETION_INDEX
                                        </p>
                                        <div class="pz-u-text-display text-2xl">45%</div>
                                        <Button size="sm" variant="secondary" class="u-mt-4"
                                            @click="viewJobDetails(job)">OPEN_COMMAND</Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="activeJobs.length === 0"
                            class="u-text-center u-py-20 pz-u-bg-limestone pz-u-border pz-u-text-mono text-xs pz-u-color-concrete">
                            // NO_LIVE_EXECUTION_STREAM_FOUND
                        </div>
                    </div>

                    <!-- POSTED TENDERS -->
                    <div v-if="activeSection === 'my-tenders'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">RESOURCE_REQUESTS_LOG</h3>
                                <Button size="sm" variant="primary" @click="$router.push('/contracts/new')">+
                                    INITIALIZE_TENDER</Button>
                            </div>
                            <div class="pz-table-wrapper">
                                <table class="pz-admin-table">
                                    <thead>
                                        <tr>
                                            <th>TENDER_TITLE</th>
                                            <th>LOCATION_NODE</th>
                                            <th>ALLOCATION_RANGE</th>
                                            <th>STATUS</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="c in myContracts" :key="c.id"
                                            @click="$router.push(`/contracts/${c.id}`)" class="u-cursor-pointer">
                                            <td class="font-bold">{{ c.title }}</td>
                                            <td class="pz-u-text-mono text-xs">📍 {{ c.location }}</td>
                                            <td class="pz-u-text-mono text-xs">${{ c.budget_min }} - ${{ c.budget_max }}
                                            </td>
                                            <td>
                                                <Badge :variant="c.status === 'POSTED' ? 'success' : 'warning'">{{
                                                    c.status }}</Badge>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- PROFILE SECTION -->
                    <div v-if="activeSection === 'profile'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">OPERATOR_REGISTRY_DATA</h3>
                            </div>
                            <div class="pz-p-8">
                                <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-8">
                                    <div>
                                        <div class="u-mb-6">
                                            <label
                                                class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2 u-block">ENTITY_NAME</label>
                                            <div class="font-bold text-lg pz-u-border-b pz-pb-2">{{
                                                profile?.company_name }}</div>
                                        </div>
                                        <div class="u-mb-6">
                                            <label
                                                class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-2 u-block">OPERATING_HUB</label>
                                            <div class="font-bold text-lg pz-u-border-b pz-pb-2">{{
                                                profile?.operating_region }}</div>
                                        </div>
                                    </div>
                                    <div>
                                        <label
                                            class="pz-u-text-mono text-xs pz-u-color-concrete u-mb-4 u-block">TECHNICAL_CAPABILITIES</label>
                                        <div class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-3">
                                            <span v-for="s in profile?.service_categories" :key="s"
                                                class="pz-spec-dot">{{ s }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useRouter } from 'vue-router';
    import api from '../services/api';
    import Button from '../components/ui/Button.vue';
    import Badge from '../components/ui/Badge.vue';
    import { useAuthStore } from '../stores/auth';

    const router = useRouter();
    const authStore = useAuthStore();
    const activeSection = ref('bids');
    const loading = ref(true);
    const profile = ref(null);
    const bids = ref([]);
    const myContracts = ref([]);

    const pendingBids = computed(() => bids.value.filter(b => b.status !== 'AWARDED'));
    const activeJobs = computed(() => bids.value.filter(b => b.status === 'AWARDED'));

    const fetchData = async () => {
        loading.value = true;
        try {
            const [profRes, bidsRes, contRes] = await Promise.all([
                api.get('/contractors/'),
                api.get('/bids/'),
                api.get('/v2/contracts/')
            ]);

            if (profRes.data.length > 0) profile.value = profRes.data[0];
            bids.value = bidsRes.data.results || bidsRes.data;

            const allContracts = contRes.data.results || contRes.data;
            myContracts.value = allContracts.filter(c => c.owner_username === authStore.user?.username);
        } catch (err) {
            console.error('Fetch error', err);
        } finally {
            loading.value = false;
        }
    };

    const getBidStatusVariant = (status) => {
        if (status === 'SHORTLISTED') return 'info';
        if (status === 'AWARDED') return 'success';
        if (status === 'REJECTED') return 'danger';
        return 'warning';
    };

    const viewJobDetails = (job) => {
        router.push(`/contracts/${job.contract}`);
    };

    onMounted(() => fetchData());
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

    .pz-admin-table tr:hover {
        background: rgba(0, 0, 0, 0.02);
    }
</style>
