<template>
    <div class="pz-admin-console">
        <div class="pz-l-container pz-admin-console__layout">
            <!-- 01: Portfolio Sidebar -->
            <aside class="pz-admin-console__sidebar">
                <div class="pz-side-nav">
                    <div class="pz-side-nav__group">
                        <h3 class="pz-side-nav__title">CAPITAL_OVERSIGHT</h3>
                        <button class="pz-side-nav__item pz-side-nav__item--active">
                            <span class="pz-side-nav__icon">◰</span> PORTFOLIO_OVERVIEW
                        </button>
                        <button class="pz-side-nav__item">
                            <span class="pz-side-nav__icon">◈</span> ESCROW_RELEASES
                        </button>
                        <button class="pz-side-nav__item">
                            <span class="pz-side-nav__icon">⧇</span> PROCUREMENT_LOGS
                        </button>
                    </div>

                    <div class="pz-side-nav__group u-mt-12">
                        <h3 class="pz-side-nav__title">QUICK_ACTIONS</h3>
                        <button class="pz-side-nav__item" @click="$router.push('/projects/new')">
                            <span class="pz-side-nav__icon">+</span> INITIALIZE_PROJECT
                        </button>
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
                                SECURE_IDENTITY: PROJECT_OWNER // SESSION: ACTIVE
                            </div>
                            <h1 class="pz-u-text-display" style="font-size: 2.5rem; line-height: 1;">Project Control
                            </h1>
                        </div>
                        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
                            <div class="pz-status-indicator pz-status-indicator--pulse"></div>
                            <Badge variant="success">COMPLIANCE: NOMINAL</Badge>
                        </div>
                    </div>
                </header>

                <!-- Command Nodes (Stats) -->
                <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6 u-mb-12">
                    <div class="pz-command-node pz-card--interactive u-hover-spring">
                        <div class="pz-command-node__label u-text-glitch" data-text="CAPITAL_DEPLOYED">CAPITAL_DEPLOYED
                        </div>
                        <div class="pz-command-node__value pz-u-color-savanna">$850,000</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node pz-card--interactive u-hover-spring">
                        <div class="pz-command-node__label u-text-glitch" data-text="ESCROW_SECURED">ESCROW_SECURED
                        </div>
                        <div class="pz-command-node__value">$120,400</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                    <div class="pz-command-node pz-card--interactive u-hover-spring">
                        <div class="pz-command-node__label u-text-glitch" data-text="ASSET_VALUATION">ASSET_VALUATION
                        </div>
                        <div class="pz-command-node__value pz-u-color-earth">$2.4M</div>
                        <div class="pz-command-node__accent"></div>
                    </div>
                </div>

                <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--lg-cols-3 pz-l-grid--gap-8">
                    <!-- Active Portfolio Node -->
                    <section class="u-lg-col-span-1">
                        <div class="pz-admin-card pz-u-border-b">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">ACTIVE_PROJECT_NODES</h3>
                                <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ projects.length }}
                                    UNITS</span>
                            </div>
                            <div class="pz-l-flex pz-l-flex--column">
                                <div v-for="project in projects" :key="project.id"
                                    class="pz-u-p-6 pz-u-border-b u-cursor-pointer pz-u-transition-base"
                                    style="background: white;" @click="$router.push(`/projects/${project.id}`)">
                                    <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start u-mb-3">
                                        <strong class="pz-u-text-mono text-sm">{{ project.title.toUpperCase()
                                            }}</strong>
                                        <Badge variant="secondary" size="sm">{{ project.status }}</Badge>
                                    </div>
                                    <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
                                        <span class="pz-u-text-mono text-xs pz-u-color-concrete">📍 {{ project.location
                                            }}</span>
                                        <span class="pz-u-text-mono text-xs pz-u-color-earth">↳ VIEW_DETAIL</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Procurement Stream -->
                    <section class="u-lg-col-span-2">
                        <div class="pz-admin-card">
                            <div class="pz-admin-card__header">
                                <h3 class="pz-admin-card__title">PROCUREMENT_TIMELINE</h3>
                            </div>
                            <div class="pz-table-wrapper">
                                <table class="pz-admin-table">
                                    <thead>
                                        <tr>
                                            <th>SEQUENCE_ID</th>
                                            <th>RESOURCE_ALLOCATION</th>
                                            <th>PROTOCOL_STATUS</th>
                                            <th class="u-text-right">VALUATION</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td class="pz-u-text-mono text-xs">ORD-00881</td>
                                            <td>
                                                <div class="font-bold">Dangote Cement (Type II)</div>
                                                <div class="pz-u-text-mono text-xs pz-u-color-concrete">VOLUME: 500
                                                    UNITS</div>
                                            </td>
                                            <td>
                                                <Badge variant="warning">IN_TRANSIT</Badge>
                                            </td>
                                            <td class="pz-u-text-mono text-right font-bold">$4,250.00</td>
                                        </tr>
                                        <tr>
                                            <td class="pz-u-text-mono text-xs">ORD-00879</td>
                                            <td>
                                                <div class="font-bold">TMT Structural Steel</div>
                                                <div class="pz-u-text-mono text-xs pz-u-color-concrete">SPEC: 12mm Grade
                                                    60</div>
                                            </td>
                                            <td>
                                                <Badge variant="success">FULFILLED</Badge>
                                            </td>
                                            <td class="pz-u-text-mono text-right font-bold">$2,100.00</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Escrow Pulse -->
                        <div class="pz-u-bg-limestone pz-u-border u-mt-8 pz-p-6">
                            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
                                <div>
                                    <h4 class="pz-u-text-mono text-xs font-bold u-mb-1">NEXT_ESCROW_MILESTONE</h4>
                                    <p class="pz-u-text-mono text-xs pz-u-color-concrete">PHASE 2: STRUCTURAL FRAMEWORK
                                        SLAB</p>
                                </div>
                                <div class="u-text-right">
                                    <div class="pz-u-text-display text-xl">$45,000</div>
                                    <span class="pz-u-text-mono text-xs pz-u-color-savanna">READY_FOR_RELEASE</span>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import api from '../services/api';
    import Button from '../components/ui/Button.vue';
    import Badge from '../components/ui/Badge.vue';

    const projects = ref([]);

    onMounted(async () => {
        try {
            const res = await api.get('/v2/projects/');
            projects.value = (res.data.results || res.data).slice(0, 3);
        } catch (e) {
            console.error(e);
        }
    });
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
        justify-content: space-between;
        align-items: center;
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
