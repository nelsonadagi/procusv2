<template>
  <div class="pz-reporting-page">
    <div class="pz-l-container">
      <section class="pz-reporting-hero">
        <div class="pz-reporting-hero__eyebrow">COMPLIANCE INTELLIGENCE</div>
        <h1 class="pz-reporting-hero__title">Regulatory reporting workspace</h1>
        <p class="pz-reporting-hero__body">
          Review generated filings, monitor submission state, and export structured report payloads for audit workflows.
        </p>
        <div class="pz-reporting-hero__stats">
          <div class="pz-reporting-hero__stat">
            <span class="pz-reporting-hero__stat-label">Generated</span>
            <strong>{{ reports.length }}</strong>
          </div>
          <div class="pz-reporting-hero__stat">
            <span class="pz-reporting-hero__stat-label">Submitted</span>
            <strong>{{ submittedCount }}</strong>
          </div>
          <div class="pz-reporting-hero__stat">
            <span class="pz-reporting-hero__stat-label">Pending</span>
            <strong>{{ pendingCount }}</strong>
          </div>
        </div>
      </section>

      <section class="pz-section-shell">
        <div class="pz-section-shell__header">
          <div>
            <div class="pz-section-shell__eyebrow">Regulatory Stream</div>
            <h2 class="pz-section-shell__title">Generated reports</h2>
            <div class="pz-section-shell__meta">Admin-facing export registry for audit, AML, and tax artifacts.</div>
          </div>
          <Button variant="ghost" size="sm" @click="fetchReports">REFRESH_REPORTS</Button>
        </div>

        <div class="pz-section-shell__content">
          <div v-if="loading" class="pz-loading-state">
            <div class="pz-loading-state__indicator"></div>
            <div class="pz-loading-state__label">COLLECTING_REGULATORY_ARTIFACTS</div>
          </div>

          <div v-else-if="error" class="pz-empty-state">
            <div class="pz-empty-state__glyph">ERR</div>
            <div class="pz-empty-state__eyebrow">Reporting Feed</div>
            <h3 class="pz-empty-state__title">The reporting stream could not be synchronized.</h3>
            <p class="pz-empty-state__body">{{ error }}</p>
          </div>

          <div v-else-if="reports.length === 0" class="pz-empty-state">
            <div class="pz-empty-state__glyph">RPT</div>
            <div class="pz-empty-state__eyebrow">Report Queue</div>
            <h3 class="pz-empty-state__title">No regulatory reports have been generated yet.</h3>
            <p class="pz-empty-state__body">
              Once reporting jobs run, completed filings will appear here with jurisdiction, timing, and export actions.
            </p>
          </div>

          <div v-else class="pz-data-table-shell">
            <table class="pz-report-table">
              <thead>
                <tr>
                  <th>TYPE</th>
                  <th>JURISDICTION</th>
                  <th>GENERATED</th>
                  <th>SUBMITTED</th>
                  <th>STATUS</th>
                  <th class="u-text-right">EXPORT</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="report in reports" :key="report.id">
                  <td>
                    <div class="pz-u-text-mono text-xs font-bold">{{ formatType(report.type) }}</div>
                  </td>
                  <td>{{ report.jurisdiction }}</td>
                  <td class="pz-u-text-mono text-xs">{{ formatDate(report.generated_at) }}</td>
                  <td class="pz-u-text-mono text-xs">
                    {{ report.submitted_at ? formatDate(report.submitted_at) : 'PENDING_SUBMISSION' }}
                  </td>
                  <td>
                    <Badge :variant="getStatusVariant(report.status)">{{ report.status }}</Badge>
                  </td>
                  <td class="u-text-right">
                    <Button size="sm" variant="outline" @click="downloadReport(report)">EXPORT_JSON</Button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import api from '../services/api';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';

const reports = ref([]);
const loading = ref(true);
const error = ref('');

const submittedCount = computed(() => reports.value.filter((report) => !!report.submitted_at).length);
const pendingCount = computed(() => reports.value.filter((report) => !report.submitted_at).length);

async function fetchReports() {
  loading.value = true;
  error.value = '';
  try {
    const res = await api.get('/v6/regulatory-reports/');
    const data = res.data?.results || res.data || [];
    reports.value = Array.isArray(data) ? data : [];
  } catch (e) {
    console.error(e);
    error.value = 'The compliance service is reachable, but report data did not load successfully.';
    reports.value = [];
  } finally {
    loading.value = false;
  }
}

function formatDate(value) {
  return new Date(value).toLocaleString('en-GB', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).toUpperCase();
}

function formatType(type) {
  return String(type || 'UNKNOWN').replaceAll('_', ' ');
}

function getStatusVariant(status) {
  if (status === 'SUBMITTED') return 'success';
  if (status === 'FAILED') return 'danger';
  if (status === 'GENERATED') return 'warning';
  return 'secondary';
}

function downloadReport(report) {
  const payload = JSON.stringify(report.report_data || {}, null, 2);
  const blob = new Blob([payload], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `regulatory-report-${report.id}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

onMounted(fetchReports);
</script>

<style scoped>
.pz-reporting-page {
  min-height: 100vh;
  padding: clamp(1.5rem, 4vw, 3rem) 0;
}

.pz-reporting-hero {
  margin-bottom: 2rem;
  padding: clamp(1.5rem, 4vw, 2.5rem);
  background: linear-gradient(135deg, rgba(10, 10, 15, 0.98), rgba(24, 24, 30, 0.94));
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 16px 16px 0 rgba(10, 10, 15, 0.12);
}

.pz-reporting-hero__eyebrow,
.pz-reporting-hero__stat-label {
  font-family: var(--pz-font-mono);
  text-transform: uppercase;
  letter-spacing: 0.18em;
}

.pz-reporting-hero__eyebrow {
  font-size: 0.68rem;
  color: var(--pz-color-earth-orange);
  margin-bottom: 1rem;
}

.pz-reporting-hero__title {
  color: white;
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: 0.95;
  margin-bottom: 0.85rem;
}

.pz-reporting-hero__body {
  max-width: 56ch;
  color: rgba(255, 255, 255, 0.74);
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.pz-reporting-hero__stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.8rem;
}

.pz-reporting-hero__stat {
  display: grid;
  gap: 0.2rem;
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.pz-reporting-hero__stat-label {
  font-size: 0.62rem;
  color: rgba(255, 255, 255, 0.62);
}

.pz-reporting-hero__stat strong {
  font-family: var(--pz-font-display);
  font-size: 1.35rem;
}

.pz-report-table {
  width: 100%;
  border-collapse: collapse;
}

.pz-report-table th {
  padding: 1rem 1.25rem;
  text-align: left;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  color: var(--pz-color-limestone-white);
  background: linear-gradient(180deg, rgba(10, 10, 15, 0.98), rgba(30, 30, 38, 0.96));
}

.pz-report-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-report-table tbody tr:hover {
  background: rgba(212, 101, 42, 0.04);
}
</style>
