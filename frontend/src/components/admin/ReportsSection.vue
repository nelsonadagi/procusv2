<template>
  <div class="pz-reports-section">
    <!-- Header + Date Range -->
    <div class="pz-reports-header">
      <div>
        <div class="pz-reports-header__eyebrow">ANALYTICS ENGINE</div>
        <h2 class="pz-reports-header__title">Platform Intelligence</h2>
      </div>
      <div class="pz-reports-header__controls">
        <div class="pz-segmented-control">
          <button
            v-for="opt in dayOptions"
            :key="opt.value"
            :class="['pz-segmented-control__btn', { active: days === opt.value }]"
            @click="days = opt.value; refreshAll()"
          >
            {{ opt.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Sub-tabs -->
    <div class="pz-reports-tabs">
      <button
        v-for="tab in reportTabs"
        :key="tab.id"
        :class="['pz-reports-tabs__btn', { active: activeReportTab === tab.id }]"
        @click="activeReportTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="pz-loading-state pz-loading-state--inline">
      <div class="pz-loading-state__indicator"></div>
      <div class="pz-loading-state__label">AGGREGATING_PLATFORM_DATA</div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="pz-empty-state">
      <div class="pz-empty-state__glyph">ERR</div>
      <h3 class="pz-empty-state__title">Analytics service unavailable</h3>
      <p class="pz-empty-state__body">{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else class="pz-reports-content">
      <!-- OVERVIEW -->
      <div v-if="renderedTabs.has('overview')" v-show="activeReportTab === 'overview'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6">
          <div v-for="kpi in overviewKPIs" :key="kpi.label" class="pz-command-node pz-card--interactive">
            <div class="pz-command-node__label">{{ kpi.label }}</div>
            <div class="pz-command-node__value" :class="kpi.class">{{ kpi.value }}</div>
            <div class="pz-command-node__accent"></div>
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Order Trend</div>
            <apexchart type="area" height="280" :options="areaChartOptions" :series="orderTrendSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Revenue Trend</div>
            <apexchart type="area" height="280" :options="areaChartOptionsCurrency" :series="revenueTrendSeries" />
          </div>
        </div>
      </div>

      <!-- FINANCIAL -->
      <div v-if="renderedTabs.has('financial')" v-show="activeReportTab === 'financial'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6">
          <div class="pz-kpi-card">
            <div class="pz-kpi-card__label">Period Revenue</div>
            <div class="pz-kpi-card__value">{{ formatCurrency(financialData?.aov ? financialData.period_revenue : 0) }}</div>
          </div>
          <div class="pz-kpi-card">
            <div class="pz-kpi-card__label">Average Order Value</div>
            <div class="pz-kpi-card__value">{{ formatCurrency(financialData?.aov || 0) }}</div>
          </div>
          <div class="pz-kpi-card">
            <div class="pz-kpi-card__label">Total Transactions</div>
            <div class="pz-kpi-card__value">{{ financialData?.payment_status?.reduce((a,b)=>a+b.count,0) || 0 }}</div>
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Payment Status Breakdown</div>
            <apexchart type="donut" height="300" :options="dynamicDonutOptions" :series="paymentStatusSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Revenue Trend (Daily)</div>
            <apexchart type="bar" height="300" :options="barChartOptions" :series="revenueBarSeries" />
          </div>
        </div>
      </div>

      <!-- MARKETPLACE -->
      <div v-if="renderedTabs.has('marketplace')" v-show="activeReportTab === 'marketplace'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Order Funnel (All Time)</div>
            <apexchart type="bar" height="300" :options="horizontalBarOptions" :series="orderFunnelSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Product Status Distribution</div>
            <apexchart type="pie" height="300" :options="dynamicPieOptions" :series="productStatusSeries" />
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Top Products (Period)</div>
            <div class="pz-data-table-shell">
              <table class="pz-report-table">
                <thead>
                  <tr><th>PRODUCT</th><th class="u-text-right">QTY SOLD</th><th class="u-text-right">REVENUE</th></tr>
                </thead>
                <tbody>
                  <tr v-for="p in (marketplaceData?.top_products || []).slice(0,8)" :key="p.name">
                    <td>{{ p.name }}</td>
                    <td class="u-text-right">{{ p.quantity_sold }}</td>
                    <td class="u-text-right">{{ formatCurrency(p.revenue) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Vendor Leaderboard</div>
            <div class="pz-data-table-shell">
              <table class="pz-report-table">
                <thead>
                  <tr><th>VENDOR</th><th class="u-text-right">ORDERS</th><th class="u-text-right">RATING</th></tr>
                </thead>
                <tbody>
                  <tr v-for="v in (marketplaceData?.vendor_leaderboard || []).slice(0,8)" :key="v.name">
                    <td>{{ v.name }}</td>
                    <td class="u-text-right">{{ v.orders }}</td>
                    <td class="u-text-right">{{ v.rating.toFixed(1) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- USERS -->
      <div v-if="renderedTabs.has('users')" v-show="activeReportTab === 'users'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">User Role Distribution</div>
            <apexchart type="donut" height="320" :options="dynamicRoleDonutOptions" :series="roleDistSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Signup Trend</div>
            <apexchart type="area" height="320" :options="areaChartOptions" :series="signupTrendSeries" />
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Activation Status</div>
            <apexchart type="pie" height="280" :options="dynamicActivationPieOptions" :series="activationSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Role Breakdown Table</div>
            <div class="pz-data-table-shell">
              <table class="pz-report-table">
                <thead>
                  <tr><th>ROLE</th><th class="u-text-right">COUNT</th></tr>
                </thead>
                <tbody>
                  <tr v-for="r in (userData?.role_distribution || [])" :key="r.role">
                    <td>{{ formatRole(r.role) }}</td>
                    <td class="u-text-right">{{ r.count }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- OPERATIONS -->
      <div v-if="renderedTabs.has('operations')" v-show="activeReportTab === 'operations'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">KYC Verification Pipeline</div>
            <apexchart type="bar" height="300" :options="horizontalBarOptions" :series="kycSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Dispute Status</div>
            <apexchart type="donut" height="300" :options="dynamicDisputeDonutOptions" :series="disputeSeries" />
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Contract Status</div>
            <apexchart type="pie" height="260" :options="dynamicContractPieOptions" :series="contractSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Project Status</div>
            <apexchart type="pie" height="260" :options="dynamicProjectPieOptions" :series="projectSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Contractor Verification</div>
            <apexchart type="pie" height="260" :options="dynamicContractorPieOptions" :series="contractorSeries" />
          </div>
        </div>
      </div>

      <!-- REAL ESTATE -->
      <div v-if="renderedTabs.has('property')" v-show="activeReportTab === 'property'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Listing Status</div>
            <apexchart type="donut" height="300" :options="dynamicListingDonutOptions" :series="listingStatusSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Asset Type Distribution</div>
            <apexchart type="pie" height="300" :options="dynamicAssetTypePieOptions" :series="assetTypeSeries" />
          </div>
        </div>
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6" style="margin-top:1.5rem">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Inquiry Trend</div>
            <apexchart type="area" height="280" :options="areaChartOptions" :series="inquiryTrendSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Appointment Status</div>
            <apexchart type="bar" height="280" :options="barChartOptions" :series="appointmentSeries" />
          </div>
        </div>
      </div>

      <!-- GEOGRAPHIC -->
      <div v-if="renderedTabs.has('geographic')" v-show="activeReportTab === 'geographic'" class="pz-reports-tab-panel">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Entity Count by Type</div>
            <apexchart type="bar" height="300" :options="barChartOptions" :series="geoCountSeries" />
          </div>
          <div class="pz-chart-card">
            <div class="pz-chart-card__header">Geographic Coverage Summary</div>
            <div class="pz-data-table-shell">
              <table class="pz-report-table">
                <thead>
                  <tr><th>ENTITY TYPE</th><th class="u-text-right">MAPPED</th></tr>
                </thead>
                <tbody>
                  <tr><td>Vendors</td><td class="u-text-right">{{ (geographicData?.vendors || []).length }}</td></tr>
                  <tr><td>Projects</td><td class="u-text-right">{{ (geographicData?.projects || []).length }}</td></tr>
                  <tr><td>Properties</td><td class="u-text-right">{{ (geographicData?.properties || []).length }}</td></tr>
                  <tr><td>Orders (with location)</td><td class="u-text-right">{{ (geographicData?.orders || []).length }}</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- REGULATORY -->
      <div v-if="renderedTabs.has('regulatory')" v-show="activeReportTab === 'regulatory'" class="pz-reports-tab-panel">
        <RegulatoryReports />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import api from '../../services/api';
import { useConfigStore } from '../../stores/config';
import RegulatoryReports from '../../views/RegulatoryReports.vue';

const days = ref(30);
const dayOptions = [
  { label: '7D', value: 7 },
  { label: '30D', value: 30 },
  { label: '90D', value: 90 },
  { label: '1Y', value: 365 },
];

const activeReportTab = ref('overview');
const renderedTabs = ref(new Set(['overview']));

watch(activeReportTab, (tab) => {
  renderedTabs.value.add(tab);
});

const reportTabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'financial', label: 'Financial' },
  { id: 'marketplace', label: 'Marketplace' },
  { id: 'users', label: 'Users' },
  { id: 'operations', label: 'Operations' },
  { id: 'property', label: 'Real Estate' },
  { id: 'geographic', label: 'Geographic' },
  { id: 'regulatory', label: 'Regulatory' },
];

const loading = ref(false);
const error = ref('');
const configStore = useConfigStore();

const summaryData = ref(null);
const financialData = ref(null);
const marketplaceData = ref(null);
const userData = ref(null);
const operationsData = ref(null);
const propertyData = ref(null);
const geographicData = ref(null);

const overviewKPIs = computed(() => {
  const s = summaryData.value;
  if (!s) return [];
  return [
    { label: 'TOTAL_USERS', value: s.users.total, class: '' },
    { label: 'TOTAL_ORDERS', value: s.orders.total, class: '' },
    { label: 'TOTAL_REVENUE', value: formatCurrency(s.revenue.total), class: 'pz-u-color-savanna' },
    { label: 'PERIOD_REVENUE', value: formatCurrency(s.revenue.period), class: 'pz-u-color-earth' },
    { label: 'VENDORS', value: `${s.vendors.approved}/${s.vendors.total}`, class: '' },
    { label: 'PROPERTIES', value: `${s.properties.active}/${s.properties.total}`, class: '' },
    { label: 'OPEN_DISPUTES', value: s.disputes.open, class: 'u-color-error' },
    { label: 'PENDING_KYC', value: s.pending_kyc, class: 'pz-u-color-earth' },
  ];
});

// Chart options
const baseChartOptions = {
  chart: { toolbar: { show: false }, fontFamily: 'inherit' },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  colors: ['#D4652A', '#10B981', '#3B82F6', '#F59E0B', '#EF4444'],
  grid: { borderColor: 'rgba(0,0,0,0.06)', strokeDashArray: 4 },
  xaxis: { labels: { style: { fontSize: '11px' } }, axisBorder: { show: false } },
  yaxis: { labels: { style: { fontSize: '11px' } } },
  legend: { fontSize: '12px', position: 'top', horizontalAlign: 'right' },
};

const areaChartOptions = computed(() => ({
  ...baseChartOptions,
  chart: { ...baseChartOptions.chart, type: 'area' },
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.35, opacityTo: 0.05 } },
  xaxis: { ...baseChartOptions.xaxis, type: 'datetime' },
}));

const areaChartOptionsCurrency = computed(() => ({
  ...areaChartOptions.value,
  yaxis: { ...baseChartOptions.yaxis, labels: { formatter: (v) => formatCurrency(v) } },
}));

const barChartOptions = computed(() => ({
  ...baseChartOptions,
  chart: { ...baseChartOptions.chart, type: 'bar' },
  plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
  xaxis: { ...baseChartOptions.xaxis, type: 'datetime' },
}));

const horizontalBarOptions = computed(() => ({
  ...baseChartOptions,
  chart: { ...baseChartOptions.chart, type: 'bar' },
  plotOptions: { bar: { borderRadius: 4, horizontal: true } },
}));

const donutOptions = computed(() => ({
  ...baseChartOptions,
  chart: { ...baseChartOptions.chart, type: 'donut' },
  plotOptions: { pie: { donut: { size: '60%' } } },
  labels: [],
}));

const pieOptions = computed(() => ({
  ...baseChartOptions,
  chart: { ...baseChartOptions.chart, type: 'pie' },
}));

// Series helpers
function makeSeries(name, data) {
  return [{ name, data: data || [] }];
}

function makeSingleSeries(data, labelKey = 'status', valueKey = 'count') {
  if (!data) return [];
  const entries = Object.entries(data);
  return entries.map(([k, v]) => (typeof v === 'object' ? v[valueKey] : v));
}

function makeLabels(data, labelKey = 'status') {
  if (!data) return [];
  const entries = Object.entries(data);
  return entries.map(([k, v]) => (typeof v === 'object' ? v[labelKey] : k));
}

const orderTrendSeries = computed(() => makeSeries('Orders', summaryData.value?.order_trend || []));
const revenueTrendSeries = computed(() => makeSeries('Revenue', summaryData.value?.revenue_trend || []));

const paymentStatusSeries = computed(() => {
  const d = financialData.value?.payment_status || [];
  return d.map(p => p.count);
});
const paymentStatusLabels = computed(() => {
  const d = financialData.value?.payment_status || [];
  return d.map(p => p.status);
});
const revenueBarSeries = computed(() => makeSeries('Revenue', financialData.value?.revenue_trend || []));

const orderFunnelSeries = computed(() => {
  const d = marketplaceData.value?.order_funnel_all || {};
  const entries = Object.entries(d);
  return [{ data: entries.map(([k, v]) => ({ x: k, y: v })) }];
});

const productStatusSeries = computed(() => {
  const d = marketplaceData.value?.product_status || [];
  return d.map(p => p.count);
});
const productStatusLabels = computed(() => {
  const d = marketplaceData.value?.product_status || [];
  return d.map(p => p.status);
});

const roleDistSeries = computed(() => (userData.value?.role_distribution || []).map(r => r.count));
const roleDistLabels = computed(() => (userData.value?.role_distribution || []).map(r => formatRole(r.role)));
const signupTrendSeries = computed(() => makeSeries('Signups', userData.value?.signup_trend || []));
const activationSeries = computed(() => {
  const a = userData.value?.activation || {};
  return [a.active || 0, a.inactive || 0];
});

const kycSeries = computed(() => {
  const d = operationsData.value?.kyc_pipeline || {};
  const entries = Object.entries(d);
  return [{ data: entries.map(([k, v]) => ({ x: k, y: v })) }];
});
const disputeSeries = computed(() => {
  const d = operationsData.value?.dispute_status || {};
  return Object.values(d);
});
const disputeLabels = computed(() => {
  const d = operationsData.value?.dispute_status || {};
  return Object.keys(d);
});
const contractSeries = computed(() => {
  const d = operationsData.value?.contract_status || {};
  return Object.values(d);
});
const contractLabels = computed(() => {
  const d = operationsData.value?.contract_status || {};
  return Object.keys(d);
});
const projectSeries = computed(() => {
  const d = operationsData.value?.project_status || {};
  return Object.values(d);
});
const projectLabels = computed(() => {
  const d = operationsData.value?.project_status || {};
  return Object.keys(d);
});
const contractorSeries = computed(() => {
  const d = operationsData.value?.contractor_status || {};
  return Object.values(d);
});
const contractorLabels = computed(() => {
  const d = operationsData.value?.contractor_status || {};
  return Object.keys(d);
});

const listingStatusSeries = computed(() => {
  const d = propertyData.value?.listing_status || {};
  return Object.values(d);
});
const listingStatusLabels = computed(() => {
  const d = propertyData.value?.listing_status || {};
  return Object.keys(d);
});
const assetTypeSeries = computed(() => (propertyData.value?.asset_types || []).map(a => a.count));
const assetTypeLabels = computed(() => (propertyData.value?.asset_types || []).map(a => a.type));
const inquiryTrendSeries = computed(() => makeSeries('Inquiries', propertyData.value?.inquiry_trend || []));
const appointmentSeries = computed(() => {
  const d = propertyData.value?.appointment_status || {};
  const entries = Object.entries(d);
  return [{ data: entries.map(([k, v]) => ({ x: k, y: v })) }];
});

const geoCountSeries = computed(() => {
  const d = geographicData.value || {};
  const counts = [
    { x: 'Vendors', y: (d.vendors || []).length },
    { x: 'Projects', y: (d.projects || []).length },
    { x: 'Properties', y: (d.properties || []).length },
    { x: 'Orders', y: (d.orders || []).length },
  ];
  return [{ data: counts }];
});

// Watchers for dynamic labels
const dynamicDonutOptions = computed(() => ({ ...donutOptions.value, labels: paymentStatusLabels.value }));
const dynamicPieOptions = computed(() => ({ ...pieOptions.value, labels: productStatusLabels.value }));
const dynamicRoleDonutOptions = computed(() => ({ ...donutOptions.value, labels: roleDistLabels.value }));
const dynamicActivationPieOptions = computed(() => ({ ...pieOptions.value, labels: ['Active', 'Inactive'] }));
const dynamicDisputeDonutOptions = computed(() => ({ ...donutOptions.value, labels: disputeLabels.value }));
const dynamicContractPieOptions = computed(() => ({ ...pieOptions.value, labels: contractLabels.value }));
const dynamicProjectPieOptions = computed(() => ({ ...pieOptions.value, labels: projectLabels.value }));
const dynamicContractorPieOptions = computed(() => ({ ...pieOptions.value, labels: contractorLabels.value }));
const dynamicListingDonutOptions = computed(() => ({ ...donutOptions.value, labels: listingStatusLabels.value }));
const dynamicAssetTypePieOptions = computed(() => ({ ...pieOptions.value, labels: assetTypeLabels.value }));

async function fetchAll() {
  loading.value = true;
  error.value = '';
  try {
    const [s, f, m, u, o, p, g] = await Promise.all([
      api.get(`/v6/analytics/summary/?days=${days.value}`),
      api.get(`/v6/analytics/financial/?days=${days.value}`),
      api.get(`/v6/analytics/marketplace/?days=${days.value}`),
      api.get(`/v6/analytics/users/?days=${days.value}`),
      api.get(`/v6/analytics/operations/?days=${days.value}`),
      api.get(`/v6/analytics/property/?days=${days.value}`),
      api.get(`/v6/analytics/geographic/`),
    ]);
    summaryData.value = s.data;
    financialData.value = f.data;
    marketplaceData.value = m.data;
    userData.value = u.data;
    operationsData.value = o.data;
    propertyData.value = p.data;
    geographicData.value = g.data;
  } catch (err) {
    console.error(err);
    error.value = 'Failed to load analytics data. Ensure the backend analytics endpoints are available.';
  } finally {
    loading.value = false;
  }
}

function refreshAll() {
  fetchAll();
}

function formatCurrency(val) {
  const n = Number(val) || 0;
  return configStore.formatPrice ? configStore.formatPrice(n, 'KES') : `KES ${n.toLocaleString('en-KE', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

function formatRole(role) {
  if (!role) return 'Unknown';
  return role.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

onMounted(() => {
  fetchAll();
});
</script>

<style scoped>
.pz-reports-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.pz-reports-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 1rem;
  padding: clamp(1.25rem, 3vw, 2rem);
  background: linear-gradient(135deg, rgba(10,10,15,0.98), rgba(24,24,30,0.94));
  color: white;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 16px 16px 0 rgba(10,10,15,0.12);
}

.pz-reports-header__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--pz-color-earth-orange);
  margin-bottom: 0.5rem;
}

.pz-reports-header__title {
  color: white;
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  line-height: 0.95;
  margin: 0;
}

.pz-segmented-control {
  display: inline-flex;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 6px;
  overflow: hidden;
}

.pz-segmented-control__btn {
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.7);
  padding: 0.5rem 1rem;
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  cursor: pointer;
  transition: all 0.2s;
}

.pz-segmented-control__btn.active,
.pz-segmented-control__btn:hover {
  background: var(--pz-color-earth-orange);
  color: white;
}

.pz-reports-tabs {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid rgba(10,10,15,0.1);
  overflow-x: auto;
}

.pz-reports-tabs__btn {
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  padding: 0.75rem 1.25rem;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.pz-reports-tabs__btn.active {
  color: var(--pz-color-foundation-black);
  border-bottom-color: var(--pz-color-earth-orange);
  font-weight: 700;
}

.pz-reports-content {
  min-height: 200px;
}

.pz-reports-tab-panel {
  animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.pz-chart-card {
  background: white;
  border: 1px solid rgba(10,10,15,0.1);
  padding: 1.25rem;
  box-shadow: 8px 8px 0 rgba(10,10,15,0.04);
}

.pz-chart-card__header {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.75rem;
}

.pz-kpi-card {
  background: white;
  border: 1px solid rgba(10,10,15,0.1);
  padding: 1.25rem;
  box-shadow: 8px 8px 0 rgba(10,10,15,0.04);
}

.pz-kpi-card__label {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.5rem;
}

.pz-kpi-card__value {
  font-family: var(--pz-font-display);
  font-size: 1.6rem;
  font-weight: 800;
}

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
  font-size: 1.55rem;
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

.pz-loading-state--inline {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.pz-data-table-shell {
  overflow-x: auto;
}

.pz-report-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.pz-report-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  color: var(--pz-color-limestone-white);
  background: linear-gradient(180deg, rgba(10,10,15,0.98), rgba(30,30,38,0.96));
}

.pz-report-table td {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid rgba(10,10,15,0.07);
}

.pz-report-table tbody tr:hover {
  background: rgba(212,101,42,0.04);
}

.u-text-right {
  text-align: right;
}
</style>
