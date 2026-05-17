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
              <label class="pz-config-field__label">Platform Logo</label>
              <div class="pz-config-logo-row">
                <div v-if="logoPreview || platformConfig.logo" class="pz-config-logo-preview">
                  <img :src="logoPreview || getMediaUrl(platformConfig.logo)" alt="Platform logo preview" />
                </div>
                <div class="pz-config-logo-actions">
                  <input ref="logoInput" type="file" accept="image/*" class="u-sr-only" @change="handleLogoSelected" />
                  <Button type="button" variant="outline" size="sm" @click="logoInput?.click()">
                    {{ platformConfig.logo || logoPreview ? 'Change Logo' : 'Upload Logo' }}
                  </Button>
                  <Button v-if="platformConfig.logo || logoPreview" type="button" variant="danger" size="sm" @click="removeLogo">
                    Remove
                  </Button>
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

      <!-- ➌ Exchange Rate Provider -->
      <section v-if="activeConfigSection === 'exchangeRates'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">📈</div>
          <div>
            <h2 class="pz-config-section__title">Exchange Rate Providers</h2>
            <p class="pz-config-section__sub">Configure the live FX sync source. Frankfurter is the default provider and ExchangeRate-API is available as fallback.</p>
          </div>
        </div>

        <form @submit.prevent="saveExchangeRateConfig" class="pz-config-form">
          <div class="pz-config-form__grid">
            <div class="pz-config-field">
              <label class="pz-config-field__label">Provider</label>
              <select v-model="exchangeRateForm.provider" class="pz-config-field__input">
                <option value="FRANKFURTER">Frankfurter</option>
                <option value="EXCHANGE_RATE_API">ExchangeRate-API</option>
              </select>
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Label</label>
              <input v-model="exchangeRateForm.label" class="pz-config-field__input" placeholder="Primary FX Sync" />
            </div>
            <div class="pz-config-field pz-config-field--full">
              <label class="pz-config-field__label">Base URL</label>
              <input v-model="exchangeRateForm.base_url" class="pz-config-field__input"
                placeholder="https://api.frankfurter.dev/v1/latest?base=BASE" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">API Key</label>
              <input v-model="exchangeRateForm.api_key" type="password" class="pz-config-field__input"
                placeholder="Leave blank to keep existing key" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Default Source</label>
              <div class="pz-config-flag-row">
                <label><input v-model="exchangeRateForm.is_default" type="checkbox" /> Default</label>
                <label><input v-model="exchangeRateForm.active" type="checkbox" /> Active</label>
              </div>
            </div>
            <div class="pz-config-field pz-config-field--full">
              <label class="pz-config-field__label">Mapping Config</label>
              <textarea v-model="exchangeRateForm.mapping_config" class="pz-config-field__input" rows="2"
                placeholder='{"rates_key":"rates"}'></textarea>
            </div>
          </div>
          <div class="pz-config-form__footer">
            <Button v-if="editingExchangeRateConfigId" variant="outline" @click="resetExchangeRateForm" type="button">Cancel Edit</Button>
            <Button type="submit" variant="primary">{{ editingExchangeRateConfigId ? 'Update Source' : 'Add Source' }}</Button>
          </div>
        </form>

        <div class="pz-config-table-wrap u-mt-6">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Label</th>
                <th>Provider</th>
                <th>Base URL</th>
                <th>Default</th>
                <th>Status</th>
                <th>Last Sync</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="exchangeRateConfigs.length === 0">
                <td colspan="7" class="pz-config-table__empty">No exchange rate providers configured yet.</td>
              </tr>
              <tr v-for="cfg in exchangeRateConfigs" :key="cfg.id" :class="{ 'pz-config-table__row--inactive': !cfg.active }">
                <td><strong>{{ cfg.label }}</strong></td>
                <td><Badge variant="primary">{{ cfg.provider }}</Badge></td>
                <td class="pz-config-table__mono">{{ cfg.base_url }}</td>
                <td><Badge v-if="cfg.is_default" variant="success">Default</Badge><span v-else class="pz-config-table__mono">-</span></td>
                <td><Badge :variant="cfg.active ? 'success' : 'warning'">{{ cfg.active ? 'Active' : 'Off' }}</Badge></td>
                <td>{{ cfg.last_sync ? new Date(cfg.last_sync).toLocaleString() : 'Never' }}</td>
                <td class="pz-config-table__actions">
                  <Button size="sm" variant="outline" @click="editExchangeRateConfig(cfg)">Edit</Button>
                  <Button size="sm" :variant="cfg.active ? 'outline' : 'primary'" @click="toggleExchangeRateConfig(cfg)">
                    {{ cfg.active ? 'Disable' : 'Enable' }}
                  </Button>
                  <Button v-if="!cfg.is_default" size="sm" variant="secondary" @click="setDefaultExchangeRateConfig(cfg)">Default</Button>
                  <Button size="sm" variant="danger" @click="deleteExchangeRateConfig(cfg.id)">Del</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➌ Payment Methods -->
      <section v-if="activeConfigSection === 'payments'" class="pz-config-section">
        <div class="pz-config-section__header">
          <div class="pz-config-section__icon">💳</div>
          <div>
            <h2 class="pz-config-section__title">Payment Methods</h2>
            <p class="pz-config-section__sub">Customize the simulated and live gateway methods exposed at checkout. Active gateways drive buyer payment options.</p>
          </div>
        </div>

        <form @submit.prevent="savePaymentGateway" class="pz-config-form">
          <div class="pz-config-form__grid">
            <div class="pz-config-field">
              <label class="pz-config-field__label">Gateway Provider</label>
              <select v-model="paymentGatewayForm.provider" class="pz-config-field__input">
                <option value="">Select provider</option>
                <option value="MPESA">M-Pesa</option>
                <option value="STRIPE">Stripe</option>
                <option value="FLUTTERWAVE">Flutterwave</option>
                <option value="PAYPAL">PayPal</option>
              </select>
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Display Label</label>
              <input v-model="paymentGatewayForm.label" class="pz-config-field__input" placeholder="M-Pesa Sandbox" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Public Key</label>
              <input v-model="paymentGatewayForm.public_key" class="pz-config-field__input" placeholder="Public key or client id" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Secret Key</label>
              <input v-model="paymentGatewayForm.secret_key" type="password" class="pz-config-field__input" placeholder="Leave blank to keep existing secret" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Webhook Secret</label>
              <input v-model="paymentGatewayForm.webhook_secret" class="pz-config-field__input" placeholder="Webhook signing secret" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Display Order</label>
              <input v-model="paymentGatewayForm.display_order" type="number" min="0" class="pz-config-field__input" />
            </div>
            <div class="pz-config-field pz-config-field--full">
              <label class="pz-config-field__label">Instructions</label>
              <textarea v-model="paymentGatewayForm.instructions" class="pz-config-field__input" rows="2"
                placeholder="Short customer-facing instructions shown at checkout."></textarea>
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Enabled Regions</label>
              <input v-model="paymentGatewayForm.enabled_regions_text" class="pz-config-field__input" placeholder="KE, UG, TZ" />
            </div>
            <div class="pz-config-field">
              <label class="pz-config-field__label">Flags</label>
              <div class="pz-config-flag-row">
                <label><input v-model="paymentGatewayForm.is_default" type="checkbox" /> Default</label>
                <label><input v-model="paymentGatewayForm.active" type="checkbox" /> Active</label>
                <label><input v-model="paymentGatewayForm.is_test_mode" type="checkbox" /> Test Mode</label>
              </div>
            </div>
          </div>
          <div class="pz-config-form__footer">
            <Button v-if="editingPaymentGatewayId" variant="outline" @click="resetPaymentGatewayForm" type="button">Cancel Edit</Button>
            <Button type="submit" variant="primary">{{ editingPaymentGatewayId ? 'Update Method' : 'Add Method' }}</Button>
          </div>
        </form>

        <div class="pz-config-table-wrap u-mt-6">
          <table class="pz-config-table">
            <thead>
              <tr>
                <th>Label</th>
                <th>Provider</th>
                <th>Regions</th>
                <th>Status</th>
                <th>Default</th>
                <th>Mode</th>
                <th>Order</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="paymentGateways.length === 0">
                <td colspan="8" class="pz-config-table__empty">No payment methods configured yet.</td>
              </tr>
              <tr v-for="gw in paymentGateways" :key="gw.id" :class="{ 'pz-config-table__row--inactive': !gw.active }">
                <td>
                  <strong>{{ gw.label }}</strong>
                  <div class="pz-config-table__mono" v-if="gw.instructions">{{ gw.instructions }}</div>
                </td>
                <td><Badge variant="primary">{{ gw.provider }}</Badge></td>
                <td>{{ (gw.enabled_regions || []).join(', ') || 'All' }}</td>
                <td><Badge :variant="gw.active ? 'success' : 'warning'">{{ gw.active ? 'Active' : 'Off' }}</Badge></td>
                <td>
                  <Badge v-if="gw.is_default" variant="success">Default</Badge>
                  <span v-else class="pz-config-table__mono">-</span>
                </td>
                <td><Badge :variant="gw.is_test_mode ? 'warning' : 'primary'">{{ gw.is_test_mode ? 'Test' : 'Live' }}</Badge></td>
                <td>{{ gw.display_order }}</td>
                <td class="pz-config-table__actions">
                  <Button size="sm" variant="outline" @click="editPaymentGateway(gw)">Edit</Button>
                  <Button size="sm" :variant="gw.active ? 'outline' : 'primary'" @click="togglePaymentGateway(gw)">
                    {{ gw.active ? 'Disable' : 'Enable' }}
                  </Button>
                  <Button v-if="!gw.is_default" size="sm" variant="secondary" @click="setDefaultGateway(gw)">Default</Button>
                  <Button size="sm" variant="danger" @click="deletePaymentGateway(gw.id)">Del</Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ➍ Users -->
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

      <!-- ➎ Roles -->
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

      <!-- ➏ Countries -->
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

      <!-- ➐ Master Data -->
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
    { id: 'exchangeRates', label: 'FX Sync', icon: '📈' },
    { id: 'payments', label: 'Payments', icon: '💳' },
    { id: 'users', label: 'Users', icon: '👥' },
    { id: 'roles', label: 'Roles', icon: '🔐' },
    { id: 'countries', label: 'Countries', icon: '🌍' },
    { id: 'masterdata', label: 'Master Data', icon: '🗂' },
  ];

  const TAXONOMY_TYPES = ['MATERIAL', 'SERVICE', 'PROJECT', 'PROPERTY', 'FINANCE', 'GOVERNMENT', 'COMPLIANCE'];

  const platformConfig = ref({
    platform_name: '', tagline: '', support_email: '', support_phone: '',
    website: '', address: '', default_currency: 'KES', default_region: 'KE',
    primary_color: '#FF6B2B', secondary_color: '#1A1A2E', logo: null,
  });
  const logoFile = ref(null);
  const logoPreview = ref(null);
  const logoInput = ref(null);
  const currencies = ref([]);
  const exchangeRateConfigs = ref([]);
  const paymentGateways = ref([]);
  const allUsers = ref([]);
  const roles = ref([]);
  const permissionCatalog = ref([]);
  const countries = ref([]);
  const categories = ref([]);

  const newCurrency = ref({ currency_code: '', currency_name: '', symbol: '', rate_to_default: '' });
  const exchangeRateForm = ref({
    provider: 'FRANKFURTER',
    label: '',
    base_url: '',
    api_key: '',
    mapping_config: '',
    is_default: true,
    active: true,
  });
  const editingExchangeRateConfigId = ref(null);
  const paymentGatewayForm = ref({
    provider: '',
    label: '',
    public_key: '',
    secret_key: '',
    webhook_secret: '',
    instructions: '',
    enabled_regions_text: '',
    display_order: 0,
    is_default: false,
    active: true,
    is_test_mode: true,
  });
  const editingPaymentGatewayId = ref(null);
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
      const [configRes, currenciesRes, exchangeRateRes, paymentGatewaysRes, allUsersRes, rolesRes, permissionCatalogRes, countriesRes, catRes] = await Promise.all([
        api.get('/platform_settings/platform/'),
        api.get('/platform_settings/currencies/'),
        api.get('/platform_settings/exchange-rate-configs/'),
        api.get('/platform_settings/payment-gateways/'),
        api.get('/platform_settings/admin-users/'),
        api.get('/platform_settings/roles/'),
        api.get('/platform_settings/roles/permission_catalog/'),
        api.get('/platform_settings/countries/'),
        api.get('/taxonomy/categories/'),
      ]);
      if (configRes.data) Object.assign(platformConfig.value, configRes.data);
      currencies.value = currenciesRes.data.results || currenciesRes.data;
      exchangeRateConfigs.value = exchangeRateRes.data.results || exchangeRateRes.data;
      paymentGateways.value = paymentGatewaysRes.data.results || paymentGatewaysRes.data;
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
  function getMediaUrl(path) {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    const baseOrigin = apiBase.replace(/\/api\/?$/, '').replace(/\/+$/, '');
    return `${baseOrigin}${path}`;
  }

  function handleLogoSelected(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (logoPreview.value) URL.revokeObjectURL(logoPreview.value);
    logoFile.value = file;
    logoPreview.value = URL.createObjectURL(file);
  }

  function removeLogo() {
    if (logoPreview.value) URL.revokeObjectURL(logoPreview.value);
    logoFile.value = null;
    logoPreview.value = null;
    platformConfig.value.logo = null;
    if (logoInput.value) logoInput.value.value = '';
  }

  async function savePlatformSettings() {
    configSaving.value = true; configSaved.value = false;
    try {
      const editableFields = ['platform_name', 'tagline', 'support_email', 'support_phone', 'website', 'address', 'default_currency', 'default_region', 'primary_color', 'secondary_color'];
      let payload;
      if (logoFile.value) {
        payload = new FormData();
        editableFields.forEach((key) => {
          const value = platformConfig.value[key];
          if (value !== null && value !== undefined) payload.append(key, value);
        });
        payload.append('logo', logoFile.value);
      } else {
        payload = {};
        editableFields.forEach((key) => payload[key] = platformConfig.value[key]);
        if (platformConfig.value.logo === null) payload.logo = null;
      }
      const res = await api.patch('/platform_settings/platform/', payload);
      Object.assign(platformConfig.value, res.data);
      if (logoPreview.value) URL.revokeObjectURL(logoPreview.value);
      logoFile.value = null;
      logoPreview.value = null;
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

  function resetExchangeRateForm() {
    editingExchangeRateConfigId.value = null;
    exchangeRateForm.value = {
      provider: 'FRANKFURTER',
      label: '',
      base_url: 'https://api.frankfurter.dev/v1/latest?base=BASE',
      api_key: '',
      mapping_config: '',
      is_default: true,
      active: true,
    };
  }

  function editExchangeRateConfig(cfg) {
    editingExchangeRateConfigId.value = cfg.id;
    exchangeRateForm.value = {
      provider: cfg.provider,
      label: cfg.label,
      base_url: cfg.base_url || '',
      api_key: '',
      mapping_config: cfg.mapping_config ? JSON.stringify(cfg.mapping_config) : '',
      is_default: Boolean(cfg.is_default),
      active: Boolean(cfg.active),
    };
  }

  async function saveExchangeRateConfig() {
    if (!exchangeRateForm.value.provider || !exchangeRateForm.value.label) return;
    const payload = {
      provider: exchangeRateForm.value.provider,
      label: exchangeRateForm.value.label,
      base_url: exchangeRateForm.value.base_url || (
        exchangeRateForm.value.provider === 'FRANKFURTER'
          ? 'https://api.frankfurter.dev/v1/latest?base=BASE'
          : 'https://v6.exchangerate-api.com/v6/KEY/latest/BASE'
      ),
      is_default: Boolean(exchangeRateForm.value.is_default),
      active: Boolean(exchangeRateForm.value.active),
    };
    if (exchangeRateForm.value.api_key) payload.api_key = exchangeRateForm.value.api_key;
    if (exchangeRateForm.value.mapping_config) {
      try {
        payload.mapping_config = JSON.parse(exchangeRateForm.value.mapping_config);
      } catch (e) {
        showAlert('Mapping config must be valid JSON.', 'error');
        return;
      }
    }
    try {
      let res;
      if (editingExchangeRateConfigId.value) {
        res = await api.patch(`/platform_settings/exchange-rate-configs/${editingExchangeRateConfigId.value}/`, payload);
        exchangeRateConfigs.value = exchangeRateConfigs.value.map((item) => item.id === res.data.id ? res.data : item);
      } else {
        res = await api.post('/platform_settings/exchange-rate-configs/', payload);
        exchangeRateConfigs.value.push(res.data);
      }
      exchangeRateConfigs.value = [...exchangeRateConfigs.value].sort((a, b) => (a.is_default === b.is_default ? 0 : a.is_default ? -1 : 1) || String(a.label).localeCompare(String(b.label)));
      resetExchangeRateForm();
      showAlert('Exchange rate source saved successfully.', 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to save exchange rate source.', 'error');
    }
  }

  async function toggleExchangeRateConfig(cfg) {
    try {
      const res = await api.patch(`/platform_settings/exchange-rate-configs/${cfg.id}/`, { active: !cfg.active });
      exchangeRateConfigs.value = exchangeRateConfigs.value.map((item) => item.id === cfg.id ? res.data : item);
      showAlert(`Exchange rate source ${res.data.active ? 'enabled' : 'disabled'} successfully.`, 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to toggle exchange rate source.', 'error');
    }
  }

  async function setDefaultExchangeRateConfig(cfg) {
    try {
      const res = await api.patch(`/platform_settings/exchange-rate-configs/${cfg.id}/`, { is_default: true, active: true });
      exchangeRateConfigs.value = exchangeRateConfigs.value.map((item) => item.id === cfg.id ? res.data : { ...item, is_default: false });
      showAlert('Default exchange rate source updated successfully.', 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to set default exchange rate source.', 'error');
    }
  }

  async function deleteExchangeRateConfig(id) {
    openDeleteConfirm({
      title: 'DELETE_EXCHANGE_RATE_SOURCE',
      message: 'Delete this exchange rate source from the platform?',
      action: async () => {
        await api.delete(`/platform_settings/exchange-rate-configs/${id}/`);
        exchangeRateConfigs.value = exchangeRateConfigs.value.filter((cfg) => cfg.id !== id);
        showAlert('Exchange rate source deleted successfully.', 'success');
      }
    });
  }

  function resetPaymentGatewayForm() {
    editingPaymentGatewayId.value = null;
    paymentGatewayForm.value = {
      provider: '',
      label: '',
      public_key: '',
      secret_key: '',
      webhook_secret: '',
      instructions: '',
      enabled_regions_text: '',
      display_order: 0,
      is_default: false,
      active: true,
      is_test_mode: true,
    };
  }

  function editPaymentGateway(gateway) {
    editingPaymentGatewayId.value = gateway.id;
    paymentGatewayForm.value = {
      provider: gateway.provider,
      label: gateway.label,
      public_key: gateway.public_key || '',
      secret_key: '',
      webhook_secret: gateway.webhook_secret || '',
      instructions: gateway.instructions || '',
      enabled_regions_text: (gateway.enabled_regions || []).join(', '),
      display_order: gateway.display_order || 0,
      is_default: Boolean(gateway.is_default),
      active: Boolean(gateway.active),
      is_test_mode: Boolean(gateway.is_test_mode),
    };
  }

  async function savePaymentGateway() {
    if (!paymentGatewayForm.value.provider || !paymentGatewayForm.value.label || !paymentGatewayForm.value.public_key) return;
    const payload = {
      provider: paymentGatewayForm.value.provider,
      label: paymentGatewayForm.value.label,
      public_key: paymentGatewayForm.value.public_key,
      webhook_secret: paymentGatewayForm.value.webhook_secret,
      instructions: paymentGatewayForm.value.instructions,
      enabled_regions: paymentGatewayForm.value.enabled_regions_text
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
      display_order: Number(paymentGatewayForm.value.display_order || 0),
      is_default: Boolean(paymentGatewayForm.value.is_default),
      active: Boolean(paymentGatewayForm.value.active),
      is_test_mode: Boolean(paymentGatewayForm.value.is_test_mode),
    };
    if (paymentGatewayForm.value.secret_key) {
      payload.secret_key = paymentGatewayForm.value.secret_key;
    }
    try {
      let res;
      if (editingPaymentGatewayId.value) {
        res = await api.patch(`/platform_settings/payment-gateways/${editingPaymentGatewayId.value}/`, payload);
        paymentGateways.value = paymentGateways.value.map((gw) => gw.id === res.data.id ? res.data : gw);
      } else {
        res = await api.post('/platform_settings/payment-gateways/', payload);
        paymentGateways.value.push(res.data);
      }
      paymentGateways.value = [...paymentGateways.value].sort((a, b) => (a.display_order || 0) - (b.display_order || 0) || String(a.label).localeCompare(String(b.label)));
      resetPaymentGatewayForm();
      showAlert('Payment method saved successfully.', 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to save payment method.', 'error');
    }
  }

  async function togglePaymentGateway(gw) {
    try {
      const res = await api.patch(`/platform_settings/payment-gateways/${gw.id}/`, { active: !gw.active });
      paymentGateways.value = paymentGateways.value.map((item) => item.id === gw.id ? res.data : item);
      showAlert(`Payment method ${res.data.active ? 'enabled' : 'disabled'} successfully.`, 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to toggle payment method.', 'error');
    }
  }

  async function setDefaultGateway(gw) {
    try {
      const res = await api.patch(`/platform_settings/payment-gateways/${gw.id}/`, { is_default: true, active: true });
      paymentGateways.value = paymentGateways.value.map((item) => item.id === gw.id ? res.data : { ...item, is_default: false });
      showAlert('Default payment method updated successfully.', 'success');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to set default payment method.', 'error');
    }
  }

  async function deletePaymentGateway(id) {
    openDeleteConfirm({
      title: 'DELETE_PAYMENT_METHOD',
      message: 'Delete this payment method from the platform?',
      action: async () => {
        await api.delete(`/platform_settings/payment-gateways/${id}/`);
        paymentGateways.value = paymentGateways.value.filter((gw) => gw.id !== id);
        showAlert('Payment method deleted successfully.', 'success');
      }
    });
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
    resetExchangeRateForm();
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

  .pz-config-flag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.75rem 0.9rem;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    background: #F8FAFC;
    font-size: 0.8rem;
    color: #444;
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

  .pz-config-logo-row {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
  }

  .pz-config-logo-preview {
    width: 120px;
    height: 120px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    overflow: hidden;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pz-config-logo-preview img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }

  .pz-config-logo-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
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
