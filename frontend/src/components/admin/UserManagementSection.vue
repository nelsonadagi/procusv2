<template>
  <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header">
        <div>
          <div class="pz-section-shell__eyebrow">Identity Control</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">SYSTEM_IDENTITY_REGISTRY</h3>
          <div class="pz-section-shell__meta">Operator accounts, status, and granted RBAC groups. Non-admin access should be granted by approval workflows, not manually assembled here.</div>
        </div>
        <Button size="sm" variant="primary" @click="$emit('add-user')">+ ADD_OPERATOR</Button>
      </div>

      <div v-if="loading" class="pz-section-shell__content">
        <div class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">QUERYING_IDENTITY_DB</div>
        </div>
      </div>

      <div v-else-if="users.length === 0" class="pz-section-shell__content">
        <div class="pz-empty-state">
          <div class="pz-empty-state__glyph">USR</div>
          <div class="pz-empty-state__eyebrow">Operator Registry</div>
          <h4 class="pz-empty-state__title">No operators are currently available in the registry.</h4>
          <p class="pz-empty-state__body">Create a new operator to start assigning roles and access scopes.</p>
        </div>
      </div>

      <div v-else class="pz-table-wrapper pz-section-shell__content pz-data-table-shell">
        <table class="pz-admin-table">
          <thead>
            <tr>
              <th>OPERATOR_NAME</th>
              <th>PRIMARY_ROLE</th>
              <th>RBAC_GROUPS</th>
              <th>STATUS</th>
              <th class="u-text-right">MGMT</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>
                <div class="u-font-bold">{{ u.first_name }} {{ u.last_name }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-concrete">{{ u.email }}</div>
              </td>
              <td>
                <Badge :variant="u.role === 'ADMIN' ? 'danger' : 'primary'">{{ u.role }}</Badge>
              </td>
              <td>
                <div class="pz-role-grid">
                  <span v-for="group in (u.groups || [])" :key="`${u.id}-${group}`" class="pz-role-chip">{{ group }}</span>
                  <span v-if="!(u.groups || []).length" class="pz-role-chip pz-role-chip--muted">No synced groups</span>
                </div>
              </td>
              <td>
                <Badge :variant="u.is_active ? 'success' : 'secondary'">{{ u.is_active ? 'ACTIVE' : 'LOCKED' }}</Badge>
              </td>
              <td>
                <div class="pz-l-flex pz-l-flex--justify-end">
                  <Button
                    size="sm"
                    :variant="u.is_active ? 'outline' : 'primary'"
                    :loading="actionState.id === u.id && actionState.action === 'toggle'"
                    @click="toggleUser(u)"
                  >
                    {{ u.is_active ? 'DEACTIVATE' : 'ACTIVATE' }}
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';

const users = ref([]);
const loading = ref(true);
const actionState = ref({ id: null, action: null });
const showAlert = inject('showAlert', null);

async function fetchUsers() {
  loading.value = true;
  try {
    const res = await api.get('/platform_settings/admin-users/');
    const data = res.data.results || res.data;
    users.value = Array.isArray(data) ? data : [];
  } catch (err) {
    showAlert?.('Failed to fetch admin operator registry.', 'error');
  } finally {
    loading.value = false;
  }
}

async function toggleUser(user) {
  actionState.value = { id: user.id, action: 'toggle' };
  try {
    const res = await api.patch(`/platform_settings/admin-users/${user.id}/toggle_active/`);
    user.is_active = res.data.is_active;
    showAlert?.(`Operator ${user.is_active ? 'activated' : 'deactivated'} successfully.`, 'success');
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to update operator status.', 'error');
  } finally {
    actionState.value = { id: null, action: null };
  }
}

onMounted(fetchUsers);

defineEmits(['add-user']);
</script>

<style scoped>
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
}

.pz-user-role-select {
  width: 100%;
  min-width: 150px;
  padding: 0.55rem 0.65rem;
  border: 1px solid rgba(10, 10, 15, 0.16);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
}

.pz-role-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  max-width: 320px;
}

.pz-role-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.55rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(10, 10, 15, 0.03);
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
}

.pz-role-chip--muted {
  color: var(--pz-color-concrete-grey);
}
</style>
