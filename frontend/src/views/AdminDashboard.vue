<template>
  <div class="pz-admin-console">
    <div class="pz-l-container pz-admin-console__layout">
      <!-- 01: Side Console Navigation -->
      <aside class="pz-admin-console__sidebar">
        <div class="pz-side-nav">
          <div class="pz-side-nav__group">
            <h3 class="pz-side-nav__title">PLATFORM_CONTROL</h3>
            <button v-for="tab in tabs" :key="tab.id" class="pz-side-nav__item"
              :class="{ 'pz-side-nav__item--active': activeTab === tab.id }" @click="activeTab = tab.id">
              <span class="pz-side-nav__icon">{{ tab.icon }}</span>
              {{ tab.name.toUpperCase() }}
            </button>
          </div>

          <div class="pz-side-nav__group u-mt-12">
            <h3 class="pz-side-nav__title">SYSTEM_EXIT</h3>
            <button class="pz-side-nav__item" @click="$router.push('/')">
              <span class="pz-side-nav__icon">⇚</span>
              TERMINATE_SESSION
            </button>
          </div>
        </div>
      </aside>

      <!-- 02: Command Interface -->
      <main class="pz-admin-console__main">
        <header class="pz-admin-console__header">
          <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
            <div>
              <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2" style="letter-spacing: 0.3em;">
                CONSOLE_PATH: /ROOT/ADMIN/{{ activeTab.toUpperCase() }}
              </div>
              <h1 class="pz-u-text-display" style="font-size: 2.5rem; line-height: 1;">{{ currentTabName }}</h1>
            </div>
            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
              <div class="pz-status-indicator pz-status-indicator--pulse"></div>
              <Badge variant="primary">SECURE_LEVEL_ALPHA</Badge>
            </div>
          </div>
        </header>

        <!-- Command Nodes (Stats) -->
        <div v-if="activeTab === 'overview'" class="pz-l-grid pz-l-grid--md-cols-4 pz-l-grid--gap-6 u-mb-12">
          <div v-for="stat in stats" :key="stat.label" class="pz-command-node pz-card--interactive u-hover-spring">
            <div class="pz-command-node__label u-text-glitch" :data-text="stat.label">{{ stat.label }}</div>
            <div class="pz-command-node__value" :class="stat.class">{{ stat.value }}</div>
            <div class="pz-command-node__accent"></div>
          </div>
        </div>

        <div class="pz-admin-console__content">
          <!-- DASHBOARD OVERVIEW -->
          <div v-if="activeTab === 'overview'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-8">
            <div class="pz-terminal-wrapper pz-elevation-lg u-hover-glow">
              <div class="pz-terminal__header">
                <span class="pz-terminal__title">AUDIT_LOG_STREAM</span>
                <div class="pz-terminal__controls">
                  <span>●</span> <span>●</span> <span>●</span>
                </div>
              </div>
              <div class="pz-terminal">
                <div class="pz-terminal__scanline"></div>
                <div v-for="log in auditLogs" :key="log.id" class="pz-terminal__line">
                  <span class="pz-terminal__timestamp">[{{ new Date(log.timestamp).toLocaleTimeString() }}]</span>
                  <span class="pz-terminal__actor">{{ log.actor_name }}</span>
                  <span class="pz-terminal__action">{{ log.action }}</span>
                  <span class="pz-terminal__resource">({RESOURCE: {{ log.resource_type }} #{{ log.resource_id
                  }}})</span>
                </div>
                <div class="pz-terminal__cursor">_</div>
              </div>
            </div>
          </div>

          <!-- VERIFICATIONS -->
          <div v-if="activeTab === 'verifications'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
            <div class="pz-admin-card">
              <div class="pz-admin-card__header">
                <h3 class="pz-admin-card__title">CONTRACTOR_VERIFICATION_QUEUE</h3>
                <Badge variant="warning">{{ pendingContractors.length }} PENDING</Badge>
              </div>

              <div class="pz-table-wrapper">
                <table class="pz-admin-table">
                  <thead>
                    <tr>
                      <th>COMPANY_ID</th>
                      <th>CAPABILITIES</th>
                      <th>INTAKE_DATE</th>
                      <th class="u-text-right">ACTIONS</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="c in pendingContractors" :key="c.id">
                      <td>
                        <div class="pz-u-text-mono font-bold">{{ c.company_name }}</div>
                      </td>
                      <td>
                        <div class="pz-l-flex pz-l-flex--wrap pz-l-flex--gap-2">
                          <span v-for="cat in c.service_categories" :key="cat" class="pz-spec-dot">{{ cat }}</span>
                        </div>
                      </td>
                      <td class="pz-u-text-mono text-xs">{{ new Date(c.created_at).toLocaleDateString() }}</td>
                      <td>
                        <div class="pz-l-flex pz-l-flex--justify-end pz-l-flex--gap-3">
                          <Button size="sm" variant="primary" @click="verifyContractor(c.id)">APPROVE</Button>
                          <Button size="sm" variant="outline">DOCS</Button>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="pendingContractors.length === 0">
                      <td colspan="4" class="u-text-center pz-u-color-concrete u-py-12 u-font-mono text-xs">
                        // NO_PENDING_REGISTRATIONS_DETECTED
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- USER MANAGEMENT -->
          <div v-if="activeTab === 'users'" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
            <div class="pz-admin-card">
              <div class="pz-admin-card__header">
                <h3 class="pz-admin-card__title">SYSTEM_IDENTITY_REGISTRY</h3>
                <Button size="sm" variant="primary" @click="showAddUser = true">+ ADD_OPERATOR</Button>
              </div>

              <div class="pz-table-wrapper">
                <table class="pz-admin-table">
                  <thead>
                    <tr>
                      <th>OPERATOR_NAME</th>
                      <th>ACCESS_ROLE</th>
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
                        <span class="pz-u-text-mono text-xs u-font-bold">{{ u.role.toUpperCase() }}</span>
                      </td>
                      <td>
                        <Badge :variant="u.is_active ? 'success' : 'secondary'">{{ u.is_active ? 'ACTIVE' : 'LOCKED' }}
                        </Badge>
                      </td>
                      <td>
                        <div class="pz-l-flex pz-l-flex--justify-end">
                          <Button size="sm" variant="outline" @click="editUser(u)">CONFIGURE</Button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- SYSTEM CONFIGURATION -->
          <div v-if="activeTab === 'config'" class="pz-config-layout">

            <!-- Left: Config Sub-Nav -->
            <nav class="pz-config-nav">
              <button v-for="s in configSections" :key="s.id" class="pz-config-nav__item"
                :class="{ 'pz-config-nav__item--active': activeConfigSection === s.id }"
                @click="activeConfigSection = s.id">
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
                          <input type="color" v-model="platformConfig.primary_color"
                            class="pz-config-color-pick__swatch" />
                          <span class="pz-config-color-pick__label">Primary</span>
                          <span class="pz-config-color-pick__value">{{ platformConfig.primary_color }}</span>
                        </div>
                        <div class="pz-config-color-pick">
                          <input type="color" v-model="platformConfig.secondary_color"
                            class="pz-config-color-pick__swatch" />
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
                  <input v-model="newCurrency.currency_name" class="pz-config-field__input"
                    placeholder="Name (US Dollar)" />
                  <input v-model="newCurrency.symbol" class="pz-config-field__input" placeholder="Symbol ($)"
                    maxlength="10" style="width:80px" />
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
                      <tr v-for="c in currencies" :key="c.id"
                        :class="{ 'pz-config-table__row--inactive': !c.is_active }">
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
                    <p class="pz-config-section__sub">All registered platform users. Toggle active status or reassign
                      roles.</p>
                  </div>
                </div>
                <div class="pz-config-table-wrap">
                  <table class="pz-config-table">
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Joined</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="allUsers.length === 0">
                        <td colspan="6" class="pz-config-table__empty">Loading users...</td>
                      </tr>
                      <tr v-for="u in allUsers" :key="u.id" :class="{ 'pz-config-table__row--inactive': !u.is_active }">
                        <td>{{ u.first_name || u.username }}</td>
                        <td class="pz-config-table__email">{{ u.email }}</td>
                        <td>
                          <select v-model="u.role" class="pz-config-rate-input" @change="setUserRole(u)"
                            style="width:140px">
                            <option v-for="r in USER_ROLES" :key="r" :value="r">{{ r }}</option>
                          </select>
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
                    <p class="pz-config-section__sub">Manage Django permission groups used as platform roles.</p>
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
                        <td>{{ r.permissions_count }} permission(s)</td>
                        <td class="pz-config-table__actions">
                          <Button size="sm" variant="danger" @click="deleteRole(r.id)">Delete</Button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="pz-config-section__header"
                  style="margin-top:24px;padding-top:16px;border-top:1px solid rgba(0,0,0,0.06)">
                  <div class="pz-config-section__icon">🏷</div>
                  <div>
                    <h2 class="pz-config-section__title">System Role Reference</h2>
                    <p class="pz-config-section__sub">Built-in application roles assigned to users via the role field.
                    </p>
                  </div>
                </div>
                <div class="pz-config-tags">
                  <Badge v-for="r in USER_ROLES" :key="r" variant="primary">{{ r }}</Badge>
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
                  <input v-model="newCountry.iso_code" class="pz-config-field__input" placeholder="ISO (KE)"
                    maxlength="3" style="width:80px" />
                  <input v-model="newCountry.name" class="pz-config-field__input" placeholder="Country name" />
                  <input v-model="newCountry.flag_emoji" class="pz-config-field__input" placeholder="🇰🇪"
                    maxlength="10" style="width:70px" />
                  <input v-model="newCountry.phone_prefix" class="pz-config-field__input" placeholder="+254"
                    maxlength="10" style="width:90px" />
                  <input v-model="newCountry.default_currency" class="pz-config-field__input"
                    placeholder="Currency (KES)" maxlength="10" style="width:110px" />
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
                      <tr v-for="c in countries" :key="c.id"
                        :class="{ 'pz-config-table__row--inactive': !c.is_active }">
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
                      <tr v-for="cat in categories" :key="cat.id"
                        :class="{ 'pz-config-table__row--inactive': !cat.active }">
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
                          <Button size="sm" :variant="cat.active ? 'outline' : 'primary'"
                            @click="toggleCategory(cat)">{{ cat.active ? 'Disable' : 'Enable' }}</Button>
                          <Button size="sm" variant="danger" @click="deleteCategory(cat.id)">Del</Button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>

            </div><!-- /config-content -->
          </div><!-- /config-layout -->


        </div>
      </main>

      <Modal :isOpen="showAddUser" title="Initialize System Identity" @close="showAddUser = false">
        <div class="pz-p-6 pz-u-text-mono text-xs">
          [SYSTEM_MESSAGE] IDENTITY PROVISIONING MODULE ACTIVE.
          PLEASE ACCESS THE CENTRAL RBAC PORTAL FOR NEW USER INITIALIZATION.
        </div>
      </Modal>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import api from '../services/api';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import Modal from '../components/ui/Modal.vue';

  const activeTab = ref('overview');
  const tabs = [
    { id: 'overview', name: 'Dashboard', icon: '◰' },
    { id: 'verifications', name: 'Verifications', icon: '🛡' },
    { id: 'contracts', name: 'Moderation', icon: '◈' },
    { id: 'users', name: 'Operators', icon: '⧇' },
    { id: 'config', name: 'Settings', icon: '⚙' }
  ];

  const users = ref([]);
  const contractors = ref([]);
  const pendingContracts = ref([]);
  const auditLogs = ref([]);
  const showAddUser = ref(false);

  // ── System Config state ──
  const activeConfigSection = ref('platform');
  const configSections = [
    { id: 'platform', label: 'Platform', icon: '🏛' },
    { id: 'currency', label: 'Currency', icon: '💱' },
    { id: 'users', label: 'Users', icon: '👥' },
    { id: 'roles', label: 'Roles', icon: '🔐' },
    { id: 'countries', label: 'Countries', icon: '🌍' },
    { id: 'masterdata', label: 'Master Data', icon: '🗂' },
  ];

  const USER_ROLES = ['ADMIN', 'VENDOR', 'BUYER', 'CONTRACTOR', 'INVESTOR', 'PROJECT_OWNER', 'STAFF'];
  const TAXONOMY_TYPES = ['MATERIAL', 'SERVICE', 'PROJECT', 'PROPERTY', 'FINANCE', 'GOVERNMENT', 'COMPLIANCE'];

  const platformConfig = ref({
    platform_name: '', tagline: '', support_email: '', support_phone: '',
    website: '', address: '', default_currency: 'KES', default_region: 'KE',
    primary_color: '#FF6B2B', secondary_color: '#1A1A2E',
  });
  const currencies = ref([]);
  const allUsers = ref([]);
  const roles = ref([]);
  const countries = ref([]);
  const categories = ref([]);

  const newCurrency = ref({ currency_code: '', currency_name: '', symbol: '', rate_to_default: '' });
  const newRoleName = ref('');
  const newCountry = ref({ iso_code: '', name: '', flag_emoji: '', phone_prefix: '', default_currency: '' });
  const newCategory = ref({ name: '', slug: '', taxonomy_type: '' });

  const configSaving = ref(false);
  const configSaved = ref(false);

  const currentTabName = computed(() => tabs.find(t => t.id === activeTab.value)?.name.toUpperCase());
  const pendingContractors = computed(() => contractors.value.filter(c => !c.is_verified));
  const pendingCount = computed(() => pendingContractors.value.length + pendingContracts.value.length);

  const stats = computed(() => [
    { label: 'ESCROW_LIQUIDITY', value: '$1,240,500', class: 'pz-u-color-savanna' },
    { label: 'ACTIVE_WORKS', value: '124', class: '' },
    { label: 'PENDING_NODES', value: pendingCount.value, class: 'pz-u-color-earth' },
    { label: 'OPEN_DISPUTES', value: '3', class: 'u-color-error' }
  ]);

  onMounted(() => fetchData());

  async function fetchData() {
    try {
      const [usersRes, contractorsRes, contractsRes, logsRes, configRes, currenciesRes, allUsersRes, rolesRes, countriesRes, catRes] = await Promise.all([
        api.get('/accounts/management/'),
        api.get('/contractors/'),
        api.get('/contracts/?status=PENDING'),
        api.get('/rbac/audit-logs/'),
        api.get('/config/platform/'),
        api.get('/config/currencies/'),
        api.get('/config/admin-users/'),
        api.get('/config/roles/'),
        api.get('/config/countries/'),
        api.get('/taxonomy/categories/'),
      ]);
      users.value = usersRes.data.results || usersRes.data;
      contractors.value = contractorsRes.data.results || contractorsRes.data;
      pendingContracts.value = contractsRes.data.results || contractsRes.data;
      auditLogs.value = logsRes.data.results || logsRes.data;
      if (configRes.data) Object.assign(platformConfig.value, configRes.data);
      currencies.value = currenciesRes.data.results || currenciesRes.data;
      allUsers.value = allUsersRes.data.results || allUsersRes.data;
      roles.value = rolesRes.data.results || rolesRes.data;
      countries.value = countriesRes.data.results || countriesRes.data;
      categories.value = catRes.data.results || catRes.data;
    } catch (err) {
      console.error("Fetch error", err);
    }
  }

  async function verifyContractor(id) {
    try { await api.patch(`/contractors/${id}/`, { is_verified: true }); fetchData(); } catch (err) { }
  }

  function editUser(u) { alert("AD_HOC IDENTITY CONFIGURATION: " + u.email); }

  // ── Platform ──
  async function savePlatformSettings() {
    configSaving.value = true; configSaved.value = false;
    try {
      const res = await api.patch('/config/platform/', platformConfig.value);
      Object.assign(platformConfig.value, res.data);
      configSaved.value = true;
      setTimeout(() => configSaved.value = false, 3000);
    } catch (err) {
      alert(err.response?.data ? JSON.stringify(err.response.data) : 'Failed to save settings');
    } finally { configSaving.value = false; }
  }

  // ── Currency ──
  async function addCurrency() {
    if (!newCurrency.value.currency_code || !newCurrency.value.rate_to_default) return;
    try {
      const res = await api.post('/config/currencies/', newCurrency.value);
      currencies.value.push(res.data);
      newCurrency.value = { currency_code: '', currency_name: '', symbol: '', rate_to_default: '' };
    } catch (err) { alert(err.response?.data ? JSON.stringify(err.response.data) : 'Failed to add currency'); }
  }
  async function updateCurrency(c) {
    try { await api.patch(`/config/currencies/${c.id}/`, { rate_to_default: c.rate_to_default }); }
    catch (err) { alert('Failed to update rate'); }
  }
  async function toggleCurrency(c) {
    try { const res = await api.patch(`/config/currencies/${c.id}/`, { is_active: !c.is_active }); c.is_active = res.data.is_active; }
    catch (err) { alert('Failed to toggle currency'); }
  }
  async function deleteCurrency(id) {
    if (!confirm('Delete this currency?')) return;
    try { await api.delete(`/config/currencies/${id}/`); currencies.value = currencies.value.filter(c => c.id !== id); }
    catch (err) { alert('Failed to delete currency'); }
  }

  // ── Users ──
  async function toggleUserActive(u) {
    try {
      const res = await api.post(`/config/admin-users/${u.id}/toggle_active/`);
      u.is_active = res.data.is_active;
    } catch (err) { alert('Failed to toggle user status'); }
  }
  async function setUserRole(u) {
    try { await api.post(`/config/admin-users/${u.id}/set_role/`, { role: u.role }); }
    catch (err) { alert('Failed to update role'); }
  }

  // ── Roles ──
  async function addRole() {
    if (!newRoleName.value.trim()) return;
    try {
      const res = await api.post('/config/roles/', { name: newRoleName.value.trim() });
      roles.value.push(res.data); newRoleName.value = '';
    } catch (err) { alert('Failed to add role'); }
  }
  async function deleteRole(id) {
    if (!confirm('Delete this role/group?')) return;
    try { await api.delete(`/config/roles/${id}/`); roles.value = roles.value.filter(r => r.id !== id); }
    catch (err) { alert('Failed to delete role'); }
  }

  // ── Countries ──
  async function addCountry() {
    if (!newCountry.value.iso_code || !newCountry.value.name) return;
    try {
      const res = await api.post('/config/countries/', newCountry.value);
      countries.value.push(res.data);
      newCountry.value = { iso_code: '', name: '', flag_emoji: '', phone_prefix: '', default_currency: '' };
    } catch (err) { alert(err.response?.data ? JSON.stringify(err.response.data) : 'Failed to add country'); }
  }
  async function toggleCountry(c) {
    try { const res = await api.patch(`/config/countries/${c.id}/`, { is_active: !c.is_active }); c.is_active = res.data.is_active; }
    catch (err) { alert('Failed to toggle country'); }
  }
  async function setDefaultCountry(c) {
    try {
      await api.post(`/config/countries/${c.id}/set_default/`);
      countries.value.forEach(x => x.is_default = (x.id === c.id));
    } catch (err) { alert('Failed to set default'); }
  }
  async function deleteCountry(id) {
    if (!confirm('Delete this country?')) return;
    try { await api.delete(`/config/countries/${id}/`); countries.value = countries.value.filter(c => c.id !== id); }
    catch (err) { alert('Failed to delete country'); }
  }

  // ── Master Data / Categories ──
  async function addCategory() {
    if (!newCategory.value.name || !newCategory.value.taxonomy_type) return;
    if (!newCategory.value.slug) newCategory.value.slug = newCategory.value.name.toLowerCase().replace(/\s+/g, '-');
    try {
      const res = await api.post('/taxonomy/categories/', newCategory.value);
      categories.value.push(res.data);
      newCategory.value = { name: '', slug: '', taxonomy_type: '' };
    } catch (err) { alert(err.response?.data ? JSON.stringify(err.response.data) : 'Failed to add category'); }
  }
  async function toggleCategory(cat) {
    try { const res = await api.patch(`/taxonomy/categories/${cat.id}/`, { active: !cat.active }); cat.active = res.data.active; }
    catch (err) { alert('Failed to toggle category'); }
  }
  async function deleteCategory(id) {
    if (!confirm('Delete this category?')) return;
    try { await api.delete(`/taxonomy/categories/${id}/`); categories.value = categories.value.filter(c => c.id !== id); }
    catch (err) { alert('Failed to delete category'); }
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

  /* Terminal Styles */
  .pz-terminal-wrapper {
    background: var(--pz-color-foundation-black);
    border-radius: var(--pz-border-radius-sm);
    overflow: hidden;
    box-shadow: var(--pz-shadow-lg);
  }

  .pz-terminal__header {
    background: #1A1A24;
    padding: var(--pz-space-2) var(--pz-space-4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .pz-terminal__title {
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    color: var(--pz-color-concrete-grey);
  }

  .pz-terminal__controls {
    display: flex;
    gap: 6px;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.2);
  }

  .pz-terminal {
    padding: var(--pz-space-4);
    height: 320px;
    overflow-y: auto;
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    color: #00FF9C;
    position: relative;
  }

  .pz-terminal__scanline {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
      linear-gradient(to right, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 4px, 3px 100%;
    pointer-events: none;
    z-index: 5;
  }

  .pz-terminal__line {
    margin-bottom: 4px;
    line-height: 1.4;
  }

  .pz-terminal__timestamp {
    color: var(--pz-color-concrete-grey);
    margin-right: 8px;
  }

  .pz-terminal__actor {
    color: var(--pz-color-earth-orange);
    margin-right: 8px;
    font-weight: 700;
  }

  .pz-terminal__action {
    color: white;
    margin-right: 8px;
  }

  .pz-terminal__resource {
    color: #4cc9f0;
    opacity: 0.8;
  }

  .pz-terminal__cursor {
    display: inline-block;
    animation: blink 1s infinite;
  }

  @keyframes blink {
    50% {
      opacity: 0;
    }
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

  /* ── System Config Panel ── */
  .pz-config-panel {
    display: flex;
    flex-direction: column;
    gap: 32px;
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
    color: var(--pz-color-steel-dark, #1a1a2e);
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
    border-color: var(--pz-color-earth-orange, #FF6B2B);
    box-shadow: 0 0 0 3px rgba(255, 107, 43, 0.1);
    background: #fff;
  }

  /* Color pickers */
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

  /* Add currency row */
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

  /* Currency table */
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

  .pz-config-table tr:last-child td {
    border-bottom: none;
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

  .pz-config-rate-input:focus {
    outline: none;
    border-color: var(--pz-color-earth-orange, #FF6B2B);
  }

  /* ── Config 2-column layout ── */
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

  /* Misc helpers */
  .pz-config-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }

  .pz-config-table__email {
    font-size: 0.8rem;
    color: #666;
  }

  .pz-config-table__mono {
    font-family: monospace;
    font-size: 0.8rem;
    color: #777;
  }

  @media (max-width: 768px) {
    .pz-config-layout {
      flex-direction: column;
    }

    .pz-config-nav {
      position: static;
      min-inline-size: unset;
      flex-direction: row;
      flex-wrap: wrap;
    }
  }
</style>
