<template>
  <div class="pz-config-layout">
    <!-- Left: Config Sub-Nav -->
    <nav class="pz-config-nav">
      <button v-for="s in configSections" :key="s.id" class="pz-config-nav__item"
        :class="{ 'pz-config-nav__item--active': activeConfigSection === s.id }" @click="activeConfigSection = s.id">
        <span class="pz-config-nav__icon">{{ s.icon }}</span>
        <span>{{ s.label }}</span>
      </button>
    </nav>

    <!-- Right: Config Content -->
    <div class="pz-config-content">
      <!-- ➊ Platform Identity -->
      <section v-if="activeConfigSection === 'platform'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">🏛</div>
          <div>
            <h2 class="pz-config-section__title">Platform Identity</h2>
            <p class="pz-config-section__sub">Name, branding, contact and regional defaults.</p>
          </div>
        </div>
        <form @submit.prevent="savePlatformSettings" class="pz-config-form">
          <div class="pz-config-form__grid">
            <div class="pz-config-field">
              <label class="pz-config-field__label">Platform Name</label>
              <input v-model="platformConfig.platform_name" class="pz-config-field__input"
                placeholder="e.g. Ujenzi Marketplace" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Tagline</label>
              <input v-model="platformConfig.tagline" class="pz-config-field__input"
                placeholder="e.g. Build the Future" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Support Email</label>
              <input v-model="platformConfig.support_email" type="email" class="pz-config-field__input"
                placeholder="support@example.com" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Support Phone</label>
              <input v-model="platformConfig.support_phone" class="pz-config-field__input"
                placeholder="+254 700 000000" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Website URL</label>
              <input v-model="platformConfig.website" type="url" class="pz-config-field__input"
                placeholder="https://ujenzi.com" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Default Region Code</label>
              <input v-model="platformConfig.default_region" class="pz-config-field__input" placeholder="KE"
                maxlength="10" />
            </div>
            <div class="pz-config-field pz-config-field--colors">
              <label class="pz-config-field__label">Brand Colors</label>
              <div class="pz-config-colors">
                <div class="pz-config-color-pick">
                  <input type="color" v-model="platformConfig.primary_color" class="pz-config-color-pick__swatch" />
                  <span class="pz-config-color-pick__label">Primary</span>
                  <span class="pz-config-color-pick__value">{{ platformConfig.primary_color }}</span>
                </div>
                <div class="pz-config-color-pick">
                  <input type="color" v-model="platformConfig.secondary_color" class="pz-config-color-pick__swatch" />
                  <span class="pz-config-color-pick__label">Secondary</span>
                  <span class="pz-config-color-pick__value">{{ platformConfig.secondary_color }}</span>
                </div>
              </div>
            </div>
            <div class="pz-config-field pz-config-field--full">
              <label class="pz-config-field__label">Physical Address</label>
              <textarea v-model="platformConfig.address" class="pz-config-field__input" rows="2"
                placeholder="Street, City, Country"></textarea>
            </div>
          </div>
          <div class="pz-config-form__footer">
            <Badge v-if="configSaved" variant="success">✓ Saved</Badge>
            <Button type="submit" variant="primary" :disabled="configSaving">
              {{ configSaving ? 'Saving...' : 'Save Settings' }}
            </Button>
          </div>
        </form>
      </section>

      <!-- ➋ Currency -->
      <section v-if="activeConfigSection === 'currency'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">💱</div>
          <div>
            <h2 class="pz-config-section__title">Currency & Exchange Rates</h2>
            <p class="pz-config-section__sub">Manage currencies and rates relative to the platform default ({{
              platformConfig.default_currency || 'KES' }}).</p>
          </div>
        </div>
        <div class="pz-config-add-row">
          <input v-model="newCurrency.currency_code" class="pz-config-field__input" placeholder="Code (USD)"
            maxlength="10" style="width:100px" />
          <input v-model="newCurrency.currency_name" class="pz-config-field__input" placeholder="Name (US Dollar)" />
          <input v-model="newCurrency.symbol" class="pz-config-field__input" placeholder="Symbol ($)" maxlength="10"
            style="width:80px" />
          <input v-model="newCurrency.rate_to_default" type="number" step="0.000001" min="0"
            class="pz-config-field__input" placeholder="Rate (e.g. 130.5)" style="width:140px" />
          <Button variant="primary" size="sm" @click="addCurrency">+ Add</Button>
        </div>
        <div class="pz-config-table-wrap">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Symbol</th>
                <th>Rate to {{ platformConfig.default_currency || 'KES' }}</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="currencies.length === 0">
                <td colspan="6" class="pz-config-table__empty">No currencies yet. Add one above.</td>
              </tr>
              <tr v-for="c in currencies" :key="c.id" :class="{ 'pz-config-table__row--inactive': !c.is_active }">
                <td><strong>{{ c.currency_code }}</strong></td>
                <td>{{ c.currency_name }}</td>
                <td>{{ c.symbol }}</td>
                <td><input v-model="c.rate_to_default" type="number" step="0.000001" min="0"
                    class="pz-config-rate-input" @change="updateCurrency(c)" /></td>
                <td>
                  <Badge :variant="c.is_active ? 'success' : 'warning'">{{ c.is_active ? 'Active' : 'Off' }}
                  </Badge>
                </td>
                <td class="pz-config-table__actions">
                  <Button size="sm" :variant="c.is_active ? 'outline' : 'primary'" @click="toggleCurrency(c)">{{
                    c.is_active ? 'Disable' : 'Enable' }}</Button>
                  <Button size="sm" variant="danger" @click="deleteCurrency(c.id)">Del</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➌ Users -->
      <section v-if="activeConfigSection === 'users'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">👥</div>
          <div>
            <h2 class="pz-config-section__title">User Management</h2>
            <p class="pz-config-section__sub">Account status and access visibility. Non-admin role grants should come from onboarding approval workflows, not manual reassignment here.</p>
          </div>
        </div>
        <div class="pz-config-table-wrap">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Primary Role</th>
                <th>Granted Groups</th>
                <th>Access Source</th>
                <th>Joined</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="allUsers.length === 0">
                <td colspan="8" class="pz-config-table__empty">Loading users...</td>
              </tr>
              <tr v-for="u in allUsers" :key="u.id" :class="{ 'pz-config-table__row--inactive': !u.is_active }">
                <td>{{ u.first_name || u.username }}</td>
                <td class="pz-config-table__email">{{ u.email }}</td>
                <td>
                  <Badge :variant="u.role === 'ADMIN' ? 'danger' : 'primary'">{{ u.role }}</Badge>
                </td>
                <td>
                  <div class="pz-config-role-grid">
                    <span v-for="group in (u.groups || [])" :key="`${u.id}-${group}`" class="pz-config-role-chip">
                      {{ group }}
                    </span>
                    <span v-if="!(u.groups || []).length" class="pz-config-role-chip pz-config-role-chip--muted">No group sync yet</span>
                  </div>
                </td>
                <td class="pz-config-table__mono">
                  {{ u.role === 'ADMIN' ? 'Manual admin assignment' : 'Approval-driven role grant expected' }}
                </td>
                <td>{{ new Date(u.date_joined).toLocaleDateString() }}</td>
                <td>
                  <Badge :variant="u.is_active ? 'success' : 'warning'">{{ u.is_active ? 'Active' : 'Inactive'
                  }}</Badge>
                </td>
                <td class="pz-config-table__actions">
                  <Button size="sm" :variant="u.is_active ? 'outline' : 'primary'" @click="toggleUserActive(u)">
                    {{ u.is_active ? 'Deactivate' : 'Activate' }}
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➍ Roles -->
      <section v-if="activeConfigSection === 'roles'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">🔐</div>
          <div>
            <h2 class="pz-config-section__title">Roles & Groups</h2>
            <p class="pz-config-section__sub">Manage RBAC role bundles. Roles are Django groups, and permissions are attached to the role before the role is granted through approval workflows.</p>
          </div>
        </div>
        <div class="pz-config-add-row">
          <input v-model="newRoleName" class="pz-config-field__input" placeholder="Role name (e.g. Auditor)" />
          <Button variant="primary" size="sm" @click="addRole">+ Add Role</Button>
        </div>
        <div class="pz-config-table-wrap">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Role / Group Name</th>
                <th>Permissions</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="roles.length === 0">
                <td colspan="3" class="pz-config-table__empty">No groups defined.</td>
              </tr>
              <tr v-for="r in roles" :key="r.id">
                <td><strong>{{ r.name }}</strong></td>
                <td>
                  <div class="pz-config-role-grid">
                    <span v-for="perm in (r.permissions || []).slice(0, 6)" :key="`${r.id}-${perm.id}`" class="pz-config-role-chip">
                      {{ perm.codename }}
                    </span>
                    <span v-if="(r.permissions || []).length > 6" class="pz-config-role-chip pz-config-role-chip--muted">
                      +{{ (r.permissions || []).length - 6 }} more
                    </span>
                    <span v-if="!(r.permissions || []).length" class="pz-config-role-chip pz-config-role-chip--muted">
                      No permissions assigned
                    </span>
                  </div>
                </td>
                <td class="pz-config-table__actions">
                  <Button size="sm" variant="outline" @click="openRolePermissions(r)">Permissions</Button>
                  <Button size="sm" variant="danger" @click="deleteRole(r.id)">Delete</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➎ Countries -->
      <section v-if="activeConfigSection === 'countries'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">🌍</div>
          <div>
            <h2 class="pz-config-section__title">Countries</h2>
            <p class="pz-config-section__sub">Active countries the platform operates in. The default country
              determines regional defaults.</p>
          </div>
        </div>
        <div class="pz-config-add-row">
          <input v-model="newCountry.iso_code" class="pz-config-field__input" placeholder="ISO (KE)" maxlength="3"
            style="width:80px" />
          <input v-model="newCountry.name" class="pz-config-field__input" placeholder="Country name" />
          <input v-model="newCountry.flag_emoji" class="pz-config-field__input" placeholder="🇰🇪" maxlength="10"
            style="width:70px" />
          <input v-model="newCountry.phone_prefix" class="pz-config-field__input" placeholder="+254" maxlength="10"
            style="width:90px" />
          <input v-model="newCountry.default_currency" class="pz-config-field__input" placeholder="Currency (KES)"
            maxlength="10" style="width:110px" />
          <Button variant="primary" size="sm" @click="addCountry">+ Add</Button>
        </div>
        <div class="pz-config-table-wrap">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Flag</th>
                <th>Name</th>
                <th>ISO</th>
                <th>Phone</th>
                <th>Currency</th>
                <th>Status</th>
                <th>Default</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="countries.length === 0">
                <td colspan="8" class="pz-config-table__empty">No countries configured.</td>
              </tr>
              <tr v-for="c in countries" :key="c.id" :class="{ 'pz-config-table__row--inactive': !c.is_active }">
                <td>{{ c.flag_emoji }}</td>
                <td><strong>{{ c.name }}</strong></td>
                <td>{{ c.iso_code }}</td>
                <td>{{ c.phone_prefix }}</td>
                <td>{{ c.default_currency }}</td>
                <td>
                  <Badge :variant="c.is_active ? 'success' : 'warning'">{{ c.is_active ? 'Active' : 'Off' }}
                  </Badge>
                </td>
                <td>
                  <Badge v-if="c.is_default" variant="primary">⭐ Default</Badge>
                  <Button v-else size="sm" variant="outline" @click="setDefaultCountry(c)">Set Default</Button>
                </td>
                <td class="pz-config-table__actions">
                  <Button size="sm" :variant="c.is_active ? 'outline' : 'primary'" @click="toggleCountry(c)">{{
                    c.is_active ? 'Disable' : 'Enable' }}</Button>
                  <Button size="sm" variant="danger" @click="deleteCountry(c.id)">Del</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➏ Master Data -->
      <section v-if="activeConfigSection === 'masterdata'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">🗂</div>
          <div>
            <h2 class="pz-config-section__title">Master Data — Taxonomy Categories</h2>
            <p class="pz-config-section__sub">Categories used for classifying materials, services, projects, and
              more.</p>
          </div>
        </div>
        <div class="pz-config-add-row">
          <input v-model="newCategory.name" class="pz-config-field__input" placeholder="Category name" />
          <input v-model="newCategory.slug" class="pz-config-field__input" placeholder="slug-identifier" />
          <select v-model="newCategory.taxonomy_type" class="pz-config-field__input" style="width:150px">
            <option value="">— Type —</option>
            <option v-for="t in TAXONOMY_TYPES" :key="t" :value="t">{{ t }}</option>
          </select>
          <Button variant="primary" size="sm" @click="addCategory">+ Add</Button>
        </div>
        <div class="pz-config-table-wrap">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Slug</th>
                <th>Type</th>
                <th>Region</th>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="categories.length === 0">
                <td colspan="6" class="pz-config-table__empty">No categories found.</td>
              </tr>
              <tr v-for="cat in categories" :key="cat.id" :class="{ 'pz-config-table__row--inactive': !cat.active }">
                <td><strong>{{ cat.name }}</strong></td>
                <td class="pz-config-table__mono">{{ cat.slug }}</td>
                <td>
                  <Badge variant="primary">{{ cat.taxonomy_type }}</Badge>
                </td>
                <td>{{ cat.region_code || '—' }}</td>
                <td>
                  <Badge :variant="cat.active ? 'success' : 'warning'">{{ cat.active ? 'Active' : 'Off' }}
                  </Badge>
                </td>
                <td class="pz-config-table__actions">
                  <Button size="sm" :variant="cat.active ? 'outline' : 'primary'" @click="toggleCategory(cat)">{{
                    cat.active ? 'Disable' : 'Enable' }}</Button>
                  <Button size="sm" variant="danger" @click="deleteCategory(cat.id)">Del</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>

  <Modal :isOpen="confirmDeleteState.open" :title="confirmDeleteState.title" size="sm" @close="closeDeleteConfirm">
    <div class="pz-confirm-panel">
      <p class="pz-confirm-panel__title">{{ confirmDeleteState.message }}</p>
      <p class="pz-confirm-panel__body">
        This action updates platform configuration immediately and may affect live operational workflows.
      </p>
    </div>
    <template #footer>
      <Button variant="outline" @click="closeDeleteConfirm">Cancel</Button>
      <Button variant="danger" :loading="confirmDeleteState.loading" @click="confirmDeleteAction">Delete</Button>
    </template>
  </Modal>

  <Modal :isOpen="rolePermissionEditor.open" :title="rolePermissionEditor.title" size="lg" @close="closeRolePermissions">
    <div class="pz-role-editor">
      <div class="pz-role-editor__toolbar">
        <div>
          <div class="pz-role-editor__bucket-title">Permission Registry</div>
          <div class="pz-config-section__sub">Permissions are predefined by the platform catalog. Admins assign them to roles here, and seeded roles start with default bundles.</div>
        </div>
      </div>

      <div v-for="bucket in permissionBuckets" :key="bucket.namespace" class="pz-role-editor__bucket">
        <div class="pz-role-editor__bucket-title">{{ bucket.namespace }}</div>
        <div class="pz-role-editor__permission-list">
          <div v-for="perm in bucket.permissions" :key="perm.id" class="pz-role-editor__permission-row">
            <label class="pz-config-role-chip pz-role-editor__permission-chip">
              <input
                type="checkbox"
                :disabled="!perm.id"
                :checked="rolePermissionEditor.selectedPermissionIds.includes(perm.id)"
                @change="togglePermissionSelection(perm.id, $event.target.checked)"
              />
              <span>{{ perm.codename }}</span>
            </label>
            <div class="pz-role-editor__permission-copy">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ perm.name }}</span>
              <span class="pz-role-editor__permission-description">{{ perm.description }}</span>
              <span v-if="!perm.seeded" class="pz-role-editor__permission-warning">Seed pending: run the RBAC seed command before this permission can be assigned.</span>
              <div v-if="perm.default_roles?.length" class="pz-config-role-grid">
                <span v-for="roleName in perm.default_roles" :key="`${perm.codename}-${roleName}`" class="pz-config-role-chip pz-config-role-chip--muted">
                  {{ roleName }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <template #footer>
      <Button variant="outline" @click="closeRolePermissions">Cancel</Button>
      <Button variant="primary" :loading="rolePermissionEditor.saving" @click="saveRolePermissions">Save Permissions</Button>
    </template>
  </Modal>
</template>

<script setup>
  import { ref, onMounted, inject, computed } from 'vue';
  import api from '../../services/api';
  import Button from '../ui/Button.vue';
  import Badge from '../ui/Badge.vue';
  import Modal from '../ui/Modal.vue';

  const activeConfigSection = ref('platform');
  const configSections = [
    { id: 'platform', label: 'Platform', icon: '🏛' },
    { id: 'currency', label: 'Currency', icon: '💱' },
    { id: 'users', label: 'Users', icon: '👥' },
    { id: 'roles', label: 'Roles', icon: '🔐' },
    { id: 'countries', label: 'Countries', icon: '🌍' },
    { id: 'masterdata', label: 'Master Data', icon: '🗂' },
  ];

  const TAXONOMY_TYPES = ['MATERIAL', 'SERVICE', 'PROJECT', 'PROPERTY', 'FINANCE', 'GOVERNMENT', 'COMPLIANCE'];

  const platformConfig = ref({
    platform_name: '', tagline: '', support_email: '', support_phone: '',
    website: '', address: '', default_currency: 'KES', default_region: 'KE',
    primary_color: '#FF6B2B', secondary_color: '#1A1A2E',
  });
  const currencies = ref([]);
  const allUsers = ref([]);
  const roles = ref([]);
  const permissionCatalog = ref([]);
  const countries = ref([]);
  const categories = ref([]);

  const newCurrency = ref({ currency_code: '', currency_name: '', symbol: '', rate_to_default: '' });
  const newRoleName = ref('');
  const newCountry = ref({ iso_code: '', name: '', flag_emoji: '', phone_prefix: '', default_currency: '' });
  const newCategory = ref({ name: '', slug: '', taxonomy_type: '' });
  const showAlert = inject('showAlert');

  const configSaving = ref(false);
  const configSaved = ref(false);
  const confirmDeleteState = ref({
    open: false,
    title: '',
    message: '',
    loading: false,
    action: null
  });
  const rolePermissionEditor = ref({
    open: false,
    title: 'Edit Role Permissions',
    roleId: null,
    selectedPermissionIds: [],
    saving: false
  });
  const permissionBuckets = computed(() => {
    const grouped = new Map();
    for (const perm of permissionCatalog.value) {
      if (!grouped.has(perm.namespace)) grouped.set(perm.namespace, []);
      grouped.get(perm.namespace).push(perm);
    }
    return Array.from(grouped.entries()).map(([namespace, permissions]) => ({ namespace, permissions }));
  });

  function openDeleteConfirm({ title, message, action }) {
    confirmDeleteState.value = {
      open: true,
      title,
      message,
      loading: false,
      action
    };
  }

  function closeDeleteConfirm() {
    confirmDeleteState.value = {
      open: false,
      title: '',
      message: '',
      loading: false,
      action: null
    };
  }

  async function confirmDeleteAction() {
    if (!confirmDeleteState.value.action) return;
    confirmDeleteState.value.loading = true;
    try {
      await confirmDeleteState.value.action();
      closeDeleteConfirm();
    } catch (err) {
      confirmDeleteState.value.loading = false;
    }
  }

  async function fetchConfigData() {
    try {
      const [configRes, currenciesRes, allUsersRes, rolesRes, permissionCatalogRes, countriesRes, catRes] = await Promise.all([
        api.get('/platform_settings/platform/'),
        api.get('/platform_settings/currencies/'),
        api.get('/platform_settings/admin-users/'),
        api.get('/platform_settings/roles/'),
        api.get('/platform_settings/roles/permission_catalog/'),
        api.get('/platform_settings/countries/'),
        api.get('/taxonomy/categories/'),
      ]);
      if (configRes.data) Object.assign(platformConfig.value, configRes.data);
      currencies.value = currenciesRes.data.results || currenciesRes.data;
      allUsers.value = allUsersRes.data.results || allUsersRes.data;
      roles.value = rolesRes.data.results || rolesRes.data;
      permissionCatalog.value = permissionCatalogRes.data.results || permissionCatalogRes.data || [];
      countries.value = countriesRes.data.results || countriesRes.data;
      categories.value = catRes.data.results || catRes.data;
    } catch (err) {
      console.error("Fetch error", err);
    }
  }

  // Business Logic Methods (CRUDs)
  async function savePlatformSettings() {
    configSaving.value = true; configSaved.value = false;
    try {
      const res = await api.patch('/platform_settings/platform/', platformConfig.value);
      Object.assign(platformConfig.value, res.data);
      configSaved.value = true;
      setTimeout(() => configSaved.value = false, 3000);
      showAlert('Platform settings saved successfully.', 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to save settings.', 'error');
    } finally { configSaving.value = false; }
  }

  async function addCurrency() {
    if (!newCurrency.value.currency_code || !newCurrency.value.rate_to_default) return;
    try {
      const res = await api.post('/platform_settings/currencies/', newCurrency.value);
      currencies.value.push(res.data);
      newCurrency.value = { currency_code: '', currency_name: '', symbol: '', rate_to_default: '' };
      showAlert('Currency added successfully.', 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to add currency.', 'error'); }
  }

  async function updateCurrency(c) {
    try { await api.patch(`/platform_settings/currencies/${c.id}/`, { rate_to_default: c.rate_to_default }); }
    catch (err) { showAlert(err.response?.data?.detail || 'Failed to update rate.', 'error'); }
  }

  async function toggleCurrency(c) {
    try {
      const res = await api.patch(`/platform_settings/currencies/${c.id}/`, { is_active: !c.is_active });
      c.is_active = res.data.is_active;
      showAlert(`Currency ${c.is_active ? 'enabled' : 'disabled'} successfully.`, 'success');
    }
    catch (err) { showAlert(err.response?.data?.detail || 'Failed to toggle currency.', 'error'); }
  }

  async function deleteCurrency(id) {
    openDeleteConfirm({
      title: 'DELETE_CURRENCY',
      message: 'Delete this currency from the platform configuration?',
      action: async () => {
        await api.delete(`/platform_settings/currencies/${id}/`);
        currencies.value = currencies.value.filter(c => c.id !== id);
        showAlert('Currency deleted successfully.', 'success');
      }
    });
  }

  async function toggleUserActive(u) {
    try {
      const res = await api.patch(`/platform_settings/admin-users/${u.id}/toggle_active/`);
      u.is_active = res.data.is_active;
      showAlert(`User ${u.is_active ? 'activated' : 'deactivated'} successfully.`, 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to toggle user status.', 'error'); }
  }

  async function addRole() {
    if (!newRoleName.value.trim()) return;
    try {
      const res = await api.post('/platform_settings/roles/', { name: newRoleName.value.trim() });
      roles.value.push(res.data); newRoleName.value = '';
      showAlert('Role added successfully.', 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to add role.', 'error'); }
  }

  async function deleteRole(id) {
    openDeleteConfirm({
      title: 'DELETE_ROLE',
      message: 'Delete this role or group from the platform?',
      action: async () => {
        await api.delete(`/platform_settings/roles/${id}/`);
        roles.value = roles.value.filter(r => r.id !== id);
        showAlert('Role deleted successfully.', 'success');
      }
    });
  }

  function openRolePermissions(role) {
    const assignablePermissionIds = new Set(permissionCatalog.value.map((perm) => perm.id).filter(Boolean));
    rolePermissionEditor.value = {
      open: true,
      title: `Permissions: ${role.name}`,
      roleId: role.id,
      selectedPermissionIds: (role.permissions || []).map((perm) => perm.id).filter((id) => assignablePermissionIds.has(id)),
      saving: false
    };
  }

  function closeRolePermissions() {
    rolePermissionEditor.value = {
      open: false,
      title: 'Edit Role Permissions',
      roleId: null,
      selectedPermissionIds: [],
      saving: false
    };
  }

  function togglePermissionSelection(permissionId, checked) {
    if (!permissionId) return;
    const selected = new Set(rolePermissionEditor.value.selectedPermissionIds);
    if (checked) selected.add(permissionId);
    else selected.delete(permissionId);
    rolePermissionEditor.value.selectedPermissionIds = Array.from(selected);
  }

  async function saveRolePermissions() {
    if (!rolePermissionEditor.value.roleId) return;
    rolePermissionEditor.value.saving = true;
    try {
      const res = await api.patch(`/platform_settings/roles/${rolePermissionEditor.value.roleId}/set_permissions/`, {
        permission_ids: rolePermissionEditor.value.selectedPermissionIds
      });
      const updatedRole = res.data;
      roles.value = roles.value.map((role) => role.id === updatedRole.id ? updatedRole : role);
      showAlert('Role permissions updated successfully.', 'success');
      closeRolePermissions();
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to update role permissions.', 'error');
      rolePermissionEditor.value.saving = false;
    }
  }

  async function addCountry() {
    if (!newCountry.value.iso_code || !newCountry.value.name) return;
    try {
      const res = await api.post('/platform_settings/countries/', newCountry.value);
      countries.value.push(res.data);
      newCountry.value = { iso_code: '', name: '', flag_emoji: '', phone_prefix: '', default_currency: '' };
      showAlert('Country added successfully.', 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to add country.', 'error'); }
  }

  async function toggleCountry(c) {
    try {
      const res = await api.patch(`/platform_settings/countries/${c.id}/`, { is_active: !c.is_active });
      c.is_active = res.data.is_active;
      showAlert(`Country ${c.is_active ? 'enabled' : 'disabled'} successfully.`, 'success');
    }
    catch (err) { showAlert(err.response?.data?.detail || 'Failed to toggle country.', 'error'); }
  }

  async function setDefaultCountry(c) {
    try {
      await api.post(`/platform_settings/countries/${c.id}/set_default/`);
      countries.value.forEach(x => x.is_default = (x.id === c.id));
      showAlert('Default country updated successfully.', 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to set default country.', 'error'); }
  }

  async function deleteCountry(id) {
    openDeleteConfirm({
      title: 'DELETE_COUNTRY',
      message: 'Delete this country from the platform configuration?',
      action: async () => {
        await api.delete(`/platform_settings/countries/${id}/`);
        countries.value = countries.value.filter(c => c.id !== id);
        showAlert('Country deleted successfully.', 'success');
      }
    });
  }

  async function addCategory() {
    if (!newCategory.value.name || !newCategory.value.taxonomy_type) return;
    if (!newCategory.value.slug) newCategory.value.slug = newCategory.value.name.toLowerCase().replace(/\s+/g, '-');
    try {
      const res = await api.post('/taxonomy/categories/', newCategory.value);
      categories.value.push(res.data);
      newCategory.value = { name: '', slug: '', taxonomy_type: '' };
      showAlert('Category added successfully.', 'success');
    } catch (err) { showAlert(err.response?.data?.detail || 'Failed to add category.', 'error'); }
  }

  async function toggleCategory(cat) {
    try {
      const res = await api.patch(`/taxonomy/categories/${cat.id}/`, { active: !cat.active });
      cat.active = res.data.active;
      showAlert(`Category ${cat.active ? 'enabled' : 'disabled'} successfully.`, 'success');
    }
    catch (err) { showAlert(err.response?.data?.detail || 'Failed to toggle category.', 'error'); }
  }

  async function deleteCategory(id) {
    openDeleteConfirm({
      title: 'DELETE_CATEGORY',
      message: 'Delete this taxonomy category from the platform?',
      action: async () => {
        await api.delete(`/taxonomy/categories/${id}/`);
        categories.value = categories.value.filter(c => c.id !== id);
        showAlert('Category deleted successfully.', 'success');
      }
    });
  }

  onMounted(() => {
    fetchConfigData();
  });
</script>

<style scoped>

  /* System Config Specific Styles from AdminDashboard */
  .pz-config-layout {
    display: flex;
    gap: 24px;
    align-items: flex-start;
  }

  .pz-config-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-inline-size: 180px;
    background: #fff;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 14px;
    padding: 12px;
    position: sticky;
    top: 80px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  }

  .pz-config-nav__item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border: none;
    border-radius: 10px;
    background: transparent;
    font-size: 0.875rem;
    font-weight: 600;
    color: #555;
    cursor: pointer;
    text-align: left;
    transition: all 0.15s;
  }

  .pz-config-nav__item:hover {
    background: #F4F5F7;
    color: #333;
  }

  .pz-config-nav__item--active {
    background: linear-gradient(135deg, rgba(255, 107, 43, 0.12), rgba(255, 107, 43, 0.06));
    color: var(--pz-color-earth-orange, #FF6B2B);
    font-weight: 700;
  }

  .pz-config-nav__icon {
    font-size: 1.1rem;
  }

  .pz-config-content {
    flex: 1;
    min-inline-size: 0;
  }

  .pz-config-section {
    background: #fff;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  }

  .pz-config-section__header {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  }

  .pz-config-section__icon {
    font-size: 2rem;
    line-height: 1;
  }

  .pz-config-section__title {
    font-size: 1.1rem;
    font-weight: 800;
    margin: 0 0 4px;
    color: #1a1a2e;
  }

  .pz-config-section__sub {
    font-size: 0.83rem;
    color: #888;
    margin: 0;
  }

  .pz-config-form__grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  @media (max-width: 768px) {
    .pz-config-form__grid {
      grid-template-columns: 1fr;
    }
  }

  .pz-config-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .pz-config-field--full {
    grid-column: 1 / -1;
  }

  .pz-config-field__label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #666;
  }

  .pz-config-field__input {
    width: 100%;
    padding: 8px 12px;
    border: 1.5px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    font-size: 0.875rem;
    background: #FAFAFA;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-sizing: border-box;
  }

  .pz-config-field__input:focus {
    outline: none;
    border-color: #FF6B2B;
    box-shadow: 0 0 0 3px rgba(255, 107, 43, 0.1);
    background: #fff;
  }

  .pz-config-colors {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .pz-config-color-pick {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #F8FAFC;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 8px 12px;
  }

  .pz-config-color-pick__swatch {
    border: none;
    border-radius: 50%;
    cursor: pointer;
    padding: 0;
    background: transparent;
    min-inline-size: 32px;
    min-block-size: 32px;
  }

  .pz-config-color-pick__label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #555;
  }

  .pz-config-color-pick__value {
    font-size: 0.72rem;
    font-family: monospace;
    color: #999;
  }

  .pz-config-form__footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 12px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .pz-config-add-row {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
    padding: 16px;
    background: #F8FAFC;
    border-radius: 10px;
    border: 1px dashed rgba(0, 0, 0, 0.1);
  }

  .pz-config-table-wrap {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.07);
  }

  .pz-config-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }

  .pz-config-table th {
    background: #F0F2F5;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  }

  .pz-config-table td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    vertical-align: middle;
  }

  .pz-config-table__empty {
    text-align: center;
    color: #aaa;
    font-style: italic;
    padding: 24px !important;
  }

  .pz-config-table__row--inactive {
    opacity: 0.5;
  }

  .pz-config-table__actions {
    display: flex;
    gap: 6px;
  }

  .pz-config-rate-input {
    width: 130px;
    padding: 5px 8px;
    border: 1.5px solid rgba(0, 0, 0, 0.12);
    border-radius: 6px;
    font-size: 0.85rem;
    font-family: monospace;
  }

  .pz-config-role-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    max-width: 320px;
  }

  .pz-config-role-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.5rem;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 999px;
    background: #F8FAFC;
    font-family: monospace;
    font-size: 0.68rem;
  }

  .pz-config-role-chip--muted {
    color: #777;
  }

  .pz-role-editor {
    display: grid;
    gap: 1rem;
    max-height: 60vh;
    overflow: auto;
  }

  .pz-role-editor__toolbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .pz-role-editor__form {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto;
    gap: 0.75rem;
    align-items: end;
    padding: 0.9rem;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    background: #F8FAFC;
  }

  .pz-role-editor__bucket {
    padding: 0.9rem;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    background: #fff;
  }

  .pz-role-editor__bucket-title {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
    color: #555;
  }

  .pz-role-editor__permission-list {
    display: grid;
    gap: 0.5rem;
  }

  .pz-role-editor__permission-row {
    display: grid;
    grid-template-columns: minmax(0, 220px) minmax(0, 1fr);
    gap: 0.75rem;
    align-items: start;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }

  .pz-role-editor__permission-row:last-child {
    border-bottom: none;
  }

  .pz-role-editor__permission-chip {
    justify-self: start;
  }

  .pz-role-editor__permission-copy {
    display: grid;
    gap: 0.35rem;
  }

  .pz-role-editor__permission-description {
    font-size: 0.82rem;
    color: #5f6b7a;
    line-height: 1.45;
  }

  .pz-role-editor__permission-warning {
    font-size: 0.78rem;
    color: #B45309;
  }
</style>
