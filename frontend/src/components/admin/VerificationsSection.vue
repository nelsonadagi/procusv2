<template>
  <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
    <div class="pz-l-grid pz-l-grid--md-cols-3 pz-l-grid--gap-6">
      <div class="pz-command-node">
        <div class="pz-command-node__label">PENDING_CONTRACTORS</div>
        <div class="pz-command-node__value">{{ pendingContractors.length }}</div>
      </div>
      <div class="pz-command-node">
        <div class="pz-command-node__label">PENDING_VENDORS</div>
        <div class="pz-command-node__value pz-u-color-earth">{{ pendingVendors.length }}</div>
      </div>
      <div class="pz-command-node">
        <div class="pz-command-node__label">PENDING_KYC</div>
        <div class="pz-command-node__value">{{ pendingKyc.length }}</div>
      </div>
    </div>

    <section class="pz-admin-card pz-section-shell" v-for="section in sections" :key="section.id">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">{{ section.eyebrow }}</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">{{ section.title }}</h3>
          <div class="pz-section-shell__meta">{{ section.meta }}</div>
        </div>
        <Badge :variant="section.items.length ? 'warning' : 'success'">
          {{ section.items.length ? `${section.items.length} PENDING` : 'ALL_CLEAR' }}
        </Badge>
      </div>

      <div v-if="loading" class="pz-section-shell__content">
        <div class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">SCANNING_REGISTRY</div>
        </div>
      </div>

      <div v-else-if="section.items.length === 0" class="pz-section-shell__content">
        <div class="pz-empty-state">
          <div class="pz-empty-state__glyph">{{ section.glyph }}</div>
          <div class="pz-empty-state__eyebrow">{{ section.eyebrow }}</div>
          <h4 class="pz-empty-state__title">{{ section.emptyTitle }}</h4>
          <p class="pz-empty-state__body">{{ section.emptyBody }}</p>
        </div>
      </div>

      <div v-else class="pz-table-wrapper pz-section-shell__content pz-data-table-shell">
        <table class="pz-admin-table">
          <thead>
            <tr>
              <th>{{ section.primaryHeader }}</th>
              <th>{{ section.secondaryHeader }}</th>
              <th>INTAKE_DATE</th>
              <th class="u-text-right">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in section.items" :key="`${section.id}-${item.id}`">
              <td>
                <div class="pz-u-text-mono font-bold">{{ section.primaryValue(item) }}</div>
                <div v-if="section.subValue(item)" class="pz-u-text-mono text-xs pz-u-color-concrete">{{ section.subValue(item) }}</div>
              </td>
              <td>
                <div v-if="section.id !== 'kyc'" class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-2">
                  <span v-for="token in section.tokens(item)" :key="token" class="pz-spec-dot">{{ token }}</span>
                </div>
                <div v-else class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-2">
                  <Badge variant="ghost" size="sm">{{ item.document_type }}</Badge>
                  <span class="pz-u-text-mono text-xs">{{ item.document_number }}</span>
                </div>
              </td>
              <td class="pz-u-text-mono text-xs">{{ new Date(section.dateValue(item)).toLocaleDateString() }}</td>
              <td>
                <div class="pz-l-flex pz-l-flex--justify-end pz-l-flex--gap-3">
                  <Button
                    size="sm"
                    variant="primary"
                    :loading="actionState.id === item.id && actionState.action === `approve-${section.id}`"
                    @click="section.approve(item.id)"
                  >
                    APPROVE
                  </Button>
                  <Button
                    size="sm"
                    variant="danger"
                    :loading="actionState.id === item.id && actionState.action === `reject-${section.id}`"
                    @click="section.reject(item.id)"
                  >
                    REJECT
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';

const contractors = ref([]);
const vendors = ref([]);
const kycRecords = ref([]);
const loading = ref(true);
const actionState = ref({ id: null, action: null });
const showAlert = inject('showAlert', null);

const pendingContractors = computed(() => contractors.value.filter((c) => c.verified_status === 'PENDING'));
const pendingVendors = computed(() => vendors.value.filter((v) => v.verified_status === 'PENDING'));
const pendingKyc = computed(() => kycRecords.value.filter((record) => ['PENDING', 'SUBMITTED'].includes(record.status)));

async function fetchQueues() {
  loading.value = true;
  try {
    const [contractorsRes, vendorsRes, kycRes] = await Promise.all([
      api.get('/contractors/'),
      api.get('/vendors/'),
      api.get('/compliance/kyc-verifications/')
    ]);
    contractors.value = contractorsRes.data.results || contractorsRes.data || [];
    vendors.value = vendorsRes.data.results || vendorsRes.data || [];
    kycRecords.value = kycRes.data.results || kycRes.data || [];
  } catch (err) {
    showAlert?.('Failed to load verification queues.', 'error');
  } finally {
    loading.value = false;
  }
}

async function runAction(id, action, request) {
  actionState.value = { id, action };
  try {
    await request();
    await fetchQueues();
    showAlert?.('Verification queue updated successfully.', 'success');
  } catch (err) {
    showAlert?.(err.response?.data?.error || 'Verification action failed.', 'error');
  } finally {
    actionState.value = { id: null, action: null };
  }
}

const sections = computed(() => ([
  {
    id: 'contractors',
    eyebrow: 'Verification Control',
    title: 'CONTRACTOR_VERIFICATION_QUEUE',
    meta: 'Registration reviews awaiting approval and capability checks.',
    glyph: 'CTR',
    items: pendingContractors.value,
    primaryHeader: 'COMPANY_ID',
    secondaryHeader: 'CAPABILITIES',
    emptyTitle: 'There are no pending contractor registrations to review.',
    emptyBody: 'New contractor applications will appear here once they enter the registry workflow.',
    primaryValue: (item) => item.company_name,
    subValue: () => '',
    tokens: (item) => item.service_categories || [],
    dateValue: (item) => item.created_at,
    approve: (id) => runAction(id, 'approve-contractors', () => api.post(`/contractors/${id}/approve/`)),
    reject: (id) => runAction(id, 'reject-contractors', () => api.post(`/contractors/${id}/reject/`))
  },
  {
    id: 'vendors',
    eyebrow: 'Supply Governance',
    title: 'VENDOR_APPROVAL_QUEUE',
    meta: 'Material suppliers awaiting review before marketplace exposure.',
    glyph: 'VND',
    items: pendingVendors.value,
    primaryHeader: 'BUSINESS_ID',
    secondaryHeader: 'CATEGORIES',
    emptyTitle: 'There are no pending vendor registrations to review.',
    emptyBody: 'New vendor applications will appear here once supplier onboarding is completed.',
    primaryValue: (item) => item.business_name,
    subValue: (item) => item.registration_number,
    tokens: (item) => item.categories_served || [],
    dateValue: (item) => item.created_at,
    approve: (id) => runAction(id, 'approve-vendors', () => api.post(`/vendors/${id}/approve/`)),
    reject: (id) => runAction(id, 'reject-vendors', () => api.post(`/vendors/${id}/reject/`))
  },
  {
    id: 'kyc',
    eyebrow: 'Compliance Review',
    title: 'KYC_REVIEW_QUEUE',
    meta: 'Identity records awaiting compliance decision.',
    glyph: 'KYC',
    items: pendingKyc.value,
    primaryHeader: 'IDENTITY_RECORD',
    secondaryHeader: 'DOCUMENTS',
    emptyTitle: 'There are no pending KYC records to review.',
    emptyBody: 'Submitted compliance identity documents will appear here for operator review.',
    primaryValue: (item) => item.user_name || item.user_email || `USER_${item.user}`,
    subValue: (item) => item.user_email || '',
    tokens: () => [],
    dateValue: (item) => item.submitted_at,
    approve: (id) => runAction(id, 'approve-kyc', () => api.post(`/compliance/kyc-verifications/${id}/approve/`)),
    reject: (id) => runAction(id, 'reject-kyc', () => api.post(`/compliance/kyc-verifications/${id}/reject/`))
  }
]));

onMounted(fetchQueues);
</script>

<style scoped>
.pz-admin-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 700px;
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
}

.pz-spec-dot {
  font-size: 0.65rem;
  padding: var(--pz-space-1) var(--pz-space-2);
  background: #F1F5F9;
  border-radius: 4px;
  color: var(--pz-color-structural-steel);
}

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
</style>
