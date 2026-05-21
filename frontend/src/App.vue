<template>
  <div class="l-app">
    <!-- 1. Floating Glass Navigation -->
    <nav class="pz-nav" :class="{ 'pz-nav--scrolled': isScrolled }">
      <div class="pz-nav__wrapper">
        <router-link to="/" class="pz-nav__logo">
          <template v-if="platformLogoUrl">
            <img :src="platformLogoUrl" alt="Platform logo" class="pz-nav__logo-img" />
          </template>
          <template v-else>
            <span class="pz-nav__logo-text">{{ $t('app.logoText') }}</span>
            <span class="pz-nav__logo-line"></span>
          </template>
        </router-link>

        <div class="pz-nav__menu u-hide-tablet">
          <router-link to="/" class="pz-nav__link" active-class="pz-nav__link--active">Materials</router-link>
          <router-link to="/properties" class="pz-nav__link"
            active-class="pz-nav__link--active">Properties</router-link>
          <router-link to="/contracts" class="pz-nav__link"
            active-class="pz-nav__link--active">Contracts</router-link>
          <router-link to="/projects" class="pz-nav__link" active-class="pz-nav__link--active">Projects</router-link>
          <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard" class="pz-nav__link"
            active-class="pz-nav__link--active">Investor</router-link>
        </div>

        <div class="pz-nav__actions">
          <!-- Workspace Indicator -->
          <div v-if="authStore.isAuthenticated && workspaceLabel" class="pz-nav__workspace u-hide-mobile">
            <span class="pz-nav__workspace-dot" aria-hidden="true"></span>
            <span class="pz-nav__workspace-label">{{ workspaceLabel }}</span>
          </div>

          <!-- Global Localization Section -->
          <div class="pz-nav__localization u-hide-mobile">
            <div class="pz-nav__loc-item">
              <select v-model="configStore.activeCountryCode" @change="configStore.setCountry($event.target.value)"
                class="pz-nav__loc-select">
                <option v-for="c in configStore.countries" :key="c.iso_code" :value="c.iso_code">
                  {{ c.flag_emoji }} {{ c.name }} ({{ c.iso_code }} · {{ c.default_currency || 'KES' }})
                </option>
              </select>
            </div>
            <div class="pz-nav__loc-item">
              <select v-model="configStore.activeCurrencyCode" disabled
                class="pz-nav__loc-select pz-nav__loc-select--currency"
                title="Currency is derived from the selected country">
                <option v-for="cur in configStore.availableCurrencies" :key="cur.currency_code"
                  :value="cur.currency_code">
                  {{ cur.currency_code }} ({{ cur.symbol }})
                </option>
              </select>
            </div>
            <div class="pz-nav__loc-item">
              <select v-model="locale" @change="changeLanguage" class="pz-nav__loc-select">
                <option value="en">EN</option>
                <option value="sw">SW</option>
              </select>
            </div>
          </div>

          <template v-if="!authStore.isAuthenticated">
            <Button variant="ghost" size="sm" @click="openAuthModal('login')" class="u-hide-mobile">Login</Button>
            <Button variant="primary" size="sm" @click="openAuthModal('register')">Get Started</Button>
          </template>

          <template v-else>
            <div class="pz-nav__notification-wrapper">
              <button
                class="pz-nav__notification-trigger"
                type="button"
                aria-label="Notifications"
                :aria-expanded="showNotificationDropdown"
                @click.stop="toggleNotificationDropdown"
              >
                <span class="pz-nav__notification-glyph" aria-hidden="true">!</span>
                <span v-if="notificationCount" class="pz-nav__notification-badge">{{ notificationCount }}</span>
              </button>

              <transition name="dropdown-slide">
                <div
                  v-if="showNotificationDropdown"
                  class="pz-nav__notification-dropdown"
                  v-click-outside="() => showNotificationDropdown = false"
                >
                  <div class="pz-nav__notification-header">
                    <span>Notifications</span>
                    <button type="button" @click.stop="refreshNotificationFeed">Refresh</button>
                  </div>
                  <div v-if="notificationFeed.length === 0" class="pz-nav__notification-empty">
                    No workflow notifications yet.
                  </div>
                  <button
                    v-for="notification in notificationFeed"
                    :key="notification.id"
                    type="button"
                    class="pz-nav__notification-item"
                    @click="openNotification(notification)"
                  >
                    <span class="pz-nav__notification-type">{{ notificationLabel(notification) }}</span>
                    <strong>{{ notification.subject || notification.message }}</strong>
                    <span>{{ notification.message }}</span>
                    <span v-if="notification.data?.property_title" class="pz-nav__notification-meta">
                      {{ notification.data.property_title }}
                    </span>
                    <time>{{ formatNotificationTime(notification.timestamp) }}</time>
                  </button>
                </div>
              </transition>
            </div>

            <!-- Premium Profile Dropdown -->
            <div class="pz-nav__dropdown-wrapper">
              <div
                class="pz-nav__profile-trigger"
                role="button"
                tabindex="0"
                aria-haspopup="true"
                :aria-expanded="showSettingsDropdown"
                aria-label="Account menu"
                @click.stop="showSettingsDropdown = !showSettingsDropdown"
                @keydown.enter.space.prevent="showSettingsDropdown = !showSettingsDropdown"
              >
                <div class="pz-nav__avatar">{{ authStore.user?.first_name?.charAt(0) || 'U' }}</div>
                <span class="pz-nav__username u-hide-mobile">{{ authStore.user?.first_name }}</span>
                <span class="pz-nav__dropdown-icon" aria-hidden="true">▾</span>
              </div>

              <transition name="dropdown-slide">
                <div v-if="showSettingsDropdown" class="pz-nav__dropdown"
                  v-click-outside="() => showSettingsDropdown = false">
                  <div class="pz-nav__dropdown-header">
                    <span class="u-text-mono text-xs">Account Management</span>
                  </div>

                  <div class="pz-nav__dropdown-section">
                    <h5 class="pz-nav__dropdown-label">Dashboards</h5>

                    <!-- Active Workspaces -->
                    <div class="pz-nav__dropdown-pill-group u-mb-4">
                      <router-link
                        v-for="ws in activeWorkspaces"
                        :key="ws.id"
                        :to="ws.path"
                        class="pz-nav__dropdown-pill"
                        :class="{ 'pz-nav__dropdown-pill--active': workspaceLabel === ws.label, 'pz-nav__dropdown-pill--admin': ws.id === 'admin' }"
                        active-class="pz-nav__dropdown-pill--active"
                        @click="showSettingsDropdown = false"
                      >
                        {{ ws.label }}
                      </router-link>
                    </div>

                    <!-- Activation Links -->
                    <div v-if="activationWorkspaces.length" class="pz-nav__dropdown-section-links">
                      <div class="pz-nav__dropdown-label" style="margin-bottom: 8px;">Activate Workspace</div>
                      <router-link
                        v-for="ws in activationWorkspaces"
                        :key="ws.path"
                        :to="ws.path"
                        class="pz-nav__dropdown-item pz-nav__dropdown-item--activate"
                        @click="showSettingsDropdown = false"
                      >
                        <span aria-hidden="true">🔒</span> {{ ws.label }}
                      </router-link>
                    </div>
                  </div>

                  <div class="pz-nav__dropdown-footer">
                    <button class="pz-nav__dropdown-item"
                       @click="showProfileModal = true; showSettingsDropdown = false">
                       Account Settings
                     </button>
                    <button class="pz-nav__dropdown-item pz-nav__dropdown-item--danger"
                      @click="authStore.logout(); showSettingsDropdown = false">
                      Log Out [⏻]
                    </button>
                  </div>
                </div>
              </transition>
            </div>
          </template>

          <button
            class="pz-nav__hamburger u-show-tablet"
            aria-label="Toggle menu"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <span aria-hidden="true">{{ mobileMenuOpen ? '✕' : '☰' }}</span>
          </button>
        </div>
      </div>

      <!-- Mobile Menu Overlay -->
      <transition name="fade">
        <div v-if="mobileMenuOpen" class="pz-nav__mobile-overlay" @click="mobileMenuOpen = false">
          <div class="pz-nav__mobile-menu" @click.stop>
            <router-link to="/" class="pz-nav__mobile-link" @click="mobileMenuOpen = false">Materials</router-link>
            <router-link to="/properties" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Properties</router-link>
            <router-link to="/contracts" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Contracts</router-link>
            <router-link to="/projects" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Projects</router-link>
            <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Investor</router-link>

            <div v-if="authStore.isAuthenticated" class="u-mt-auto pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
              <!-- Mobile Localization Cluster -->
              <div class="pz-nav__mobile-localization">
                <div class="pz-nav__mobile-loc-row">
                  <label>Region</label>
                  <select v-model="configStore.activeCountryCode" @change="configStore.setCountry($event.target.value)">
                    <option v-for="c in configStore.countries" :key="c.iso_code" :value="c.iso_code">{{ c.flag_emoji }} {{
                      c.name }} ({{ c.iso_code }} · {{ c.default_currency || 'KES' }})</option>
                  </select>
                </div>
                <div class="pz-nav__mobile-loc-row">
                  <label>Currency (auto)</label>
                  <select v-model="configStore.activeCurrencyCode" disabled
                    title="Currency is derived from the selected country">
                    <option v-for="cur in configStore.availableCurrencies" :key="cur.currency_code"
                      :value="cur.currency_code">{{
                        cur.currency_code }} ({{ cur.symbol }})</option>
                  </select>
                </div>
                <div class="pz-nav__mobile-loc-row">
                  <label>Language</label>
                  <select v-model="locale" @change="changeLanguage">
                    <option value="en">English (US)</option>
                    <option value="sw">Kiswahili (KE)</option>
                  </select>
                </div>
              </div>

              <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
                <div class="pz-nav__mobile-section-label">Active Workspaces</div>
                <router-link
                  v-for="ws in activeWorkspaces"
                  :key="ws.id"
                  :to="ws.path"
                  class="pz-nav__mobile-link"
                  :style="ws.id === 'admin' ? 'color: var(--pz-color-earth-orange);' : ''"
                  @click="mobileMenuOpen = false"
                >
                  {{ ws.label }}
                </router-link>

                <template v-if="activationWorkspaces.length">
                  <div class="pz-nav__mobile-section-label">Activate Workspace</div>
                  <router-link
                    v-for="ws in activationWorkspaces"
                    :key="ws.path"
                    :to="ws.path"
                    class="pz-nav__mobile-link pz-nav__mobile-link--dim"
                    @click="mobileMenuOpen = false"
                  >
                    <span aria-hidden="true">🔒</span> {{ ws.label }}
                  </router-link>
                </template>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </nav>

    <!-- 2. Main Terminal Content -->
    <main class="l-main">
      <router-view v-slot="{ Component, route }">
        <transition name="fade">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>

    <footer class="pz-shell-footer">
      <div class="pz-l-container pz-shell-footer__container">
        <div class="pz-shell-footer__cta">
          <div>
            <p class="pz-shell-footer__eyebrow">Ready To Act</p>
            <h2 class="pz-shell-footer__title">Search, classify, open details, and move straight into the workflow.</h2>
            <p class="pz-shell-footer__body">
              The platform should help users act quickly. These links take them to the live entry points that matter.
            </p>
          </div>
          <div class="pz-shell-footer__cta-links">
            <router-link to="/" class="pz-shell-footer__button">Search Materials</router-link>
            <router-link to="/properties" class="pz-shell-footer__button">Browse Properties</router-link>
            <router-link to="/contracts" class="pz-shell-footer__button">View Contracts</router-link>
            <router-link to="/projects" class="pz-shell-footer__button">Open Projects</router-link>
          </div>
        </div>

        <div class="pz-shell-footer__grid">
          <div class="pz-shell-footer__column">
            <h3 class="pz-shell-footer__heading">Explore</h3>
            <router-link to="/" class="pz-shell-footer__link">Materials Marketplace</router-link>
            <router-link to="/properties" class="pz-shell-footer__link">Property Marketplace</router-link>
            <router-link to="/contracts" class="pz-shell-footer__link">Contracts</router-link>
            <router-link to="/projects" class="pz-shell-footer__link">Projects</router-link>
          </div>

          <div class="pz-shell-footer__column">
            <h3 class="pz-shell-footer__heading">Workspaces</h3>
            <router-link to="/owner/dashboard" class="pz-shell-footer__link">Owner Workspace</router-link>
            <router-link to="/property-manager/dashboard" class="pz-shell-footer__link">Property Workspace</router-link>
            <router-link to="/contractor/dashboard" class="pz-shell-footer__link">Contractor Workspace</router-link>
            <router-link to="/vendor/dashboard" class="pz-shell-footer__link">Vendor Workspace</router-link>
            <router-link to="/buyer/dashboard" class="pz-shell-footer__link">Buyer Workspace</router-link>
            <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard" class="pz-shell-footer__link">Investor Workspace</router-link>
          </div>

          <div class="pz-shell-footer__column">
            <h3 class="pz-shell-footer__heading">Account</h3>
            <router-link v-if="!authStore.isAuthenticated" to="/login" class="pz-shell-footer__link">Login</router-link>
            <router-link v-if="!authStore.isAuthenticated" to="/register" class="pz-shell-footer__link">Register</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/buyer/dashboard" class="pz-shell-footer__link">My Workspace</router-link>
            <router-link v-if="authStore.hasRole('VENDOR')" to="/vendor/dashboard" class="pz-shell-footer__link">Vendor Dashboard</router-link>
            <router-link v-if="authStore.hasRole('CONTRACTOR')" to="/contractor/dashboard" class="pz-shell-footer__link">Contractor Dashboard</router-link>
            <router-link v-if="authStore.hasRole('PROPERTY_MANAGER')" to="/property-manager/dashboard" class="pz-shell-footer__link">Property Dashboard</router-link>
            <router-link v-if="authStore.hasRole('REAL_ESTATE_AGENT')" to="/agent/dashboard" class="pz-shell-footer__link">Agent Dashboard</router-link>
            <router-link v-if="authStore.hasRole('SURVEYOR')" to="/surveyor/dashboard" class="pz-shell-footer__link">Surveyor Dashboard</router-link>
            <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard" class="pz-shell-footer__link">Investor Dashboard</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin" class="pz-shell-footer__link">Admin</router-link>
          </div>
        </div>

        <div class="pz-shell-footer__bottom">
          <span>Paanguzo Marketplace</span>
          <span>Construction workflows across materials, property, contracts, and projects.</span>
        </div>
      </div>
    </footer>

    <!-- 4. Global Modals -->
    <Modal :isOpen="showProfileModal" title="Profile Settings" size="md" @close="showProfileModal = false">
      <form id="profile-form" @submit.prevent="saveProfile" class="l-grid l-grid--cols-1 pz-u-mb-4">
        <div class="l-grid l-grid--cols-2 l-grid--gap-md">
          <PzInput v-model="userForm.first_name" label="First Name" required />
          <PzInput v-model="userForm.last_name" label="Last Name" required />
        </div>

        <div class="u-mt-4">
          <PzInput v-model="userForm.email" label="Email Address" disabled
            hint="Email cannot be changed" />
        </div>

        <div class="pz-input-wrapper u-mt-4">
          <label class="pz-input__label u-mb-1">Approved Workspace Access</label>
          <div class="pz-profile-role-panel">
            <div class="pz-profile-role-panel__section">
              <span class="pz-profile-role-panel__label">Primary</span>
              <strong>{{ userForm.role || 'PROJECT_OWNER' }}</strong>
            </div>
            <div class="pz-profile-role-panel__section">
              <span class="pz-profile-role-panel__label">Additional approved roles</span>
              <span>{{ formattedApprovedRoles }}</span>
            </div>
          </div>
          <span class="pz-input__hint">Admins grant specialized workspace access after the related onboarding workflow is reviewed.</span>
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="showProfileModal = false">Cancel</Button>
        <Button type="submit" form="profile-form" variant="primary" :loading="loading">Save Changes</Button>
      </template>
    </Modal>
    <!-- 5. Notification Center -->
    <NotificationCenter />

    <!-- 6. Global Chat Modal -->
    <Modal :isOpen="uiStore.isChatOpen" title="Contact Support" size="lg" @close="uiStore.closeChat">
      <ChatWindow v-if="uiStore.activeChatRoomId" :roomId="String(uiStore.activeChatRoomId)" />
    </Modal>
  </div>
</template>

<script setup>
  import { ref, onMounted, onUnmounted, provide, watch, computed } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import { useAuthStore } from './stores/auth';
  import { useNotificationStore } from './stores/notifications';
  import { useUIStore } from './stores/ui';
  import { useConfigStore } from './stores/config';
  import Button from './components/ui/Button.vue';
  import Modal from './components/ui/Modal.vue';
  import PzInput from './components/PzInput.vue';
  import NotificationCenter from './components/ui/NotificationCenter.vue';
  import ChatWindow from './components/chat/ChatWindow.vue'; // Added ChatWindow
  import api from './services/api';
  import { useI18n } from 'vue-i18n';

  const { locale } = useI18n();

  const authStore = useAuthStore();
  const notificationStore = useNotificationStore();
  const uiStore = useUIStore();
  const configStore = useConfigStore();
  const router = useRouter();
  const route = useRoute();

  const isScrolled = ref(false);
  const mobileMenuOpen = ref(false);
  const showProfileModal = ref(false);
  const showSettingsDropdown = ref(false);
  const showNotificationDropdown = ref(false);
  const loading = ref(false);

  const userForm = ref({
    first_name: '',
    last_name: '',
    email: '',
    role: '',
    roles: []
  });
  const platformLogoUrl = computed(() => {
    const logo = configStore.platformSettings?.logo;
    if (!logo) return null;
    if (logo.startsWith('http')) return logo;
    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    const baseOrigin = apiBase.replace(/\/api\/?$/, '').replace(/\/+$/, '');
    return `${baseOrigin}${logo}`;
  });

  const formattedApprovedRoles = computed(() => {
    if (userForm.value.role === 'ADMIN') return 'Admin accounts do not carry additional non-admin roles.';
    const roles = userForm.value.roles || [];
    return roles.length ? roles.join(', ') : 'No additional approved roles yet.';
  });
  const notificationFeed = computed(() => notificationStore.notificationFeed.slice(0, 10));
  const notificationCount = computed(() => Math.min(notificationStore.notificationFeed.length, 99));

  // Workspace detection for nav indicator
  const workspaceLabel = computed(() => {
    const path = route.path;
    if (path.startsWith('/buyer/dashboard')) return 'Buyer';
    if (path.startsWith('/vendor/dashboard')) return 'Vendor';
    if (path.startsWith('/contractor/dashboard')) return 'Contractor';
    if (path.startsWith('/owner/dashboard')) return 'Owner';
    if (path.startsWith('/property-manager/dashboard')) return 'Property';
    if (path.startsWith('/agent/dashboard')) return 'Agent';
    if (path.startsWith('/surveyor/dashboard')) return 'Surveyor';
    if (path.startsWith('/investor/dashboard')) return 'Investor';
    if (path.startsWith('/courier/dashboard')) return 'Courier';
    if (path.startsWith('/government/dashboard')) return 'Government';
    if (path.startsWith('/admin')) return 'Admin';
    return null;
  });

  // Approved vs activatable workspaces
  const activeWorkspaces = computed(() => {
    const items = [];
    // Base workspace is always available
    items.push({ label: 'My Orders', path: '/buyer/dashboard', id: 'buyer' });
    if (authStore.hasRole('VENDOR')) items.push({ label: 'Vendor', path: '/vendor/dashboard', id: 'vendor' });
    if (authStore.hasRole('CONTRACTOR')) items.push({ label: 'Contractor', path: '/contractor/dashboard', id: 'contractor' });
    if (authStore.hasRole('PROPERTY_MANAGER')) items.push({ label: 'Property', path: '/property-manager/dashboard', id: 'property' });
    if (authStore.hasRole('REAL_ESTATE_AGENT')) items.push({ label: 'Agent', path: '/agent/dashboard', id: 'agent' });
    if (authStore.hasRole('SURVEYOR')) items.push({ label: 'Surveyor', path: '/surveyor/dashboard', id: 'surveyor' });
    if (authStore.hasRole('INVESTOR')) items.push({ label: 'Investor', path: '/investor/dashboard', id: 'investor' });
    if (authStore.hasRole('COURIER')) items.push({ label: 'Courier', path: '/courier/dashboard', id: 'courier' });
    if (authStore.hasRole('GOVERNMENT')) items.push({ label: 'Government', path: '/government/dashboard', id: 'government' });
    if (authStore.isAdmin) items.push({ label: 'Admin', path: '/admin', id: 'admin' });
    return items;
  });

  const activationWorkspaces = computed(() => {
    const items = [];
    if (!authStore.hasRole('VENDOR')) items.push({ label: 'Vendor Workspace', path: '/vendor/dashboard' });
    if (!authStore.hasRole('CONTRACTOR')) items.push({ label: 'Contractor Workspace', path: '/contractor/dashboard' });
    if (!authStore.hasRole('PROPERTY_MANAGER')) items.push({ label: 'Property Workspace', path: '/property-manager/dashboard' });
    if (!authStore.hasRole('REAL_ESTATE_AGENT')) items.push({ label: 'Agent Workspace', path: '/agent/dashboard' });
    if (!authStore.hasRole('SURVEYOR')) items.push({ label: 'Surveyor Workspace', path: '/surveyor/dashboard' });
    if (!authStore.hasRole('INVESTOR')) items.push({ label: 'Investor Workspace', path: '/investor/dashboard' });
    if (!authStore.hasRole('COURIER')) items.push({ label: 'Courier Workspace', path: '/courier/dashboard' });
    if (!authStore.hasRole('GOVERNMENT')) items.push({ label: 'Government Workspace', path: '/government/dashboard' });
    return items;
  });

  function handleScroll() {
    isScrolled.value = window.scrollY > 20;
  }

  function openAuthModal(mode = 'login') {
    router.push(mode === 'register' ? '/register' : '/login');
  }

  function changeLanguage() {
    // locale.value is already synced via v-model
    localStorage.setItem('locale', locale.value);
  }

  function showAlert(message, type = 'info') {
    notificationStore.addNotification({
      message,
      type: String(type || 'info').toUpperCase(),
      timestamp: new Date().toISOString()
    });
  }

  provide('showAlert', showAlert);

  async function refreshNotificationFeed() {
    try {
      await notificationStore.fetchNotifications();
    } catch (err) {
      console.error('Failed to fetch notifications', err);
    }
  }

  async function toggleNotificationDropdown() {
    showNotificationDropdown.value = !showNotificationDropdown.value;
    if (showNotificationDropdown.value) {
      await refreshNotificationFeed();
    }
  }

  function formatNotificationTime(timestamp) {
    const value = timestamp ? new Date(timestamp) : new Date();
    if (Number.isNaN(value.getTime())) return '';
    return value.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function openNotification(notification) {
    const data = notification.data || {};
    showNotificationDropdown.value = false;
    if (notification.type === 'CHAT' && data.room_id) {
      uiStore.openChat(data.room_id);
      return;
    }
    if (data.property_url) {
      router.push(data.property_url);
      return;
    }
    if (data.property_id) {
      router.push(`/properties/${data.property_id}`);
      return;
    }
    if (data.action === 'respond_quote' || data.quote_request_id) {
      router.push(authStore.hasRole('VENDOR') ? '/vendor/dashboard' : '/buyer/dashboard');
      return;
    }
    if (data.order_id) {
      router.push('/buyer/dashboard');
      return;
    }
    router.push('/buyer/dashboard');
  }

  function notificationLabel(notification) {
    const data = notification?.data || {};
    if (data.action === 'review_inquiry') return 'PROPERTY';
    if (data.action === 'review_appointment') return 'PROPERTY';
    if (data.property_id) return 'PROPERTY';
    return notification?.type || 'SYSTEM';
  }

  async function saveProfile() {
    loading.value = true;
    try {
      const res = await api.patch('/accounts/profile/', {
        first_name: userForm.value.first_name,
        last_name: userForm.value.last_name
      });
      authStore.setUser(res.data);
      userForm.value = {
        first_name: res.data.first_name,
        last_name: res.data.last_name,
        email: res.data.email,
        role: res.data.role,
        roles: res.data.roles || []
      };
      showAlert("✅ Profile sync successful", 'payment');
      showProfileModal.value = false;
    } catch (err) {
      showAlert("❌ Profile update failed", 'error');
    } finally {
      loading.value = false;
    }
  }

  // Watch for auth state changes to connect/disconnect notifications
  watch(() => authStore.isAuthenticated, (newVal) => {
    if (newVal) {
      notificationStore.connect();
      refreshNotificationFeed();
    } else {
      notificationStore.disconnect();
    }
  });

  onMounted(() => {
    window.addEventListener('scroll', handleScroll);
    configStore.fetchConfig();

    // Restore locale if present
    const savedLocale = localStorage.getItem('locale');
    if (savedLocale) locale.value = savedLocale;

    if (authStore.user) {
      userForm.value = {
        first_name: authStore.user.first_name,
        last_name: authStore.user.last_name,
        email: authStore.user.email,
        role: authStore.user.role,
        roles: authStore.user.roles || []
      };
      // Connect if already authenticated
      if (authStore.isAuthenticated) {
        notificationStore.connect();
        refreshNotificationFeed();
      }
    }
  });

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
    notificationStore.disconnect();
  });
</script>

<style scoped>
  .pz-profile-role-panel {
    display: grid;
    gap: 0.75rem;
    padding: 0.95rem 1rem;
    border: 1px solid rgba(10, 10, 15, 0.12);
    background: rgba(10, 10, 15, 0.03);
  }

  .pz-profile-role-panel__section {
    display: grid;
    gap: 0.2rem;
  }

  .pz-profile-role-panel__label {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pz-color-concrete-grey);
  }

  .pz-nav__logo-text {
    font-family: var(--pz-font-display);
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    text-transform: uppercase;
  }

  .pz-nav__logo-line {
    display: inline-flex;
    width: 26px;
    height: 2px;
    margin-left: 0.5rem;
    background: var(--pz-color-earth-orange);
  }

  .pz-nav__logo-img {
    max-height: 32px;
    width: auto;
    object-fit: contain;
    display: block;
  }

  .pz-nav__link {
    font-family: var(--pz-font-primary);
    font-size: 0.92rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--pz-color-foundation-black);
  }

  .pz-nav__link:hover,
  .pz-nav__link--active {
    color: var(--pz-color-earth-orange);
  }

  .l-app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .l-main {
    flex: 1;
    min-height: calc(100vh - 80px - 400px);
    position: relative;
  }

  .l-main::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
      radial-gradient(circle at top left, rgba(212, 101, 42, 0.06), transparent 22%),
      radial-gradient(circle at 85% 15%, rgba(16, 185, 129, 0.05), transparent 18%),
      linear-gradient(90deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.02) calc(100% - 1px)),
      linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(10, 10, 15, 0.016) calc(100% - 1px));
    background-size: auto, auto, 112px 112px, 112px 112px;
    pointer-events: none;
    z-index: -1;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.2s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  /* Navbar Localization Cluster */
  .pz-nav__localization {
    display: flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(255, 250, 243, 0.72));
    padding: 2px 6px;
    border: 1px solid rgba(10, 10, 15, 0.08);
    margin-right: 8px;
    box-shadow: 8px 8px 0 rgba(10, 10, 15, 0.04);
    backdrop-filter: blur(12px);
  }

  .pz-nav__loc-item {
    display: flex;
    align-items: center;
    position: relative;
  }

  .pz-nav__loc-item:not(:last-child)::after {
    content: "";
    height: 12px;
    width: 1px;
    background: rgba(0, 0, 0, 0.1);
    margin-left: 8px;
  }

  .pz-nav__loc-select {
    background: transparent;
    border: none;
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    font-weight: 800;
    color: var(--pz-color-foundation-black);
    cursor: pointer;
    padding: 4px 12px 4px 4px;
    outline: none;
    text-align: left;
    transition: color 0.2s;
  }

  .pz-nav__loc-select:hover {
    color: var(--pz-color-earth-orange);
  }

  .pz-nav__loc-select--currency {
    color: var(--pz-color-earth-orange);
    letter-spacing: 0.05em;
  }

  /* Mobile Localization Styling */
  .pz-nav__mobile-localization {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .pz-nav__mobile-loc-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pz-nav__mobile-loc-row label {
    font-family: var(--pz-font-mono);
    font-size: 0.6rem;
    color: var(--pz-color-concrete-grey);
    letter-spacing: 0.1em;
  }

  .pz-nav__mobile-loc-row select {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    padding: 4px 8px;
    border-radius: 4px;
    outline: none;
    min-width: 120px;
    text-align: right;
  }

  /* Dropdown System */
  .pz-nav__notification-wrapper {
    position: relative;
  }

  .pz-nav__notification-trigger {
    position: relative;
    width: 42px;
    height: 42px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(10, 10, 15, 0.08);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(255, 250, 243, 0.72));
    box-shadow: 8px 8px 0 rgba(10, 10, 15, 0.04);
    cursor: pointer;
    backdrop-filter: blur(12px);
  }

  .pz-nav__notification-trigger:hover {
    border-color: rgba(10, 10, 15, 0.14);
    background: rgba(255, 255, 255, 0.92);
  }

  .pz-nav__notification-glyph {
    width: 22px;
    height: 22px;
    border: 2px solid var(--pz-color-foundation-black);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    font-weight: 900;
    line-height: 1;
  }

  .pz-nav__notification-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    min-width: 18px;
    height: 18px;
    padding: 0 5px;
    border-radius: 999px;
    background: var(--pz-color-earth-orange);
    color: white;
    border: 2px solid rgba(248, 246, 240, 0.98);
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    font-weight: 900;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .pz-nav__notification-dropdown {
    position: absolute;
    top: calc(100% + 12px);
    right: 0;
    width: min(360px, calc(100vw - 24px));
    max-height: 480px;
    overflow: auto;
    background: rgba(248, 246, 240, 0.98);
    border: 2px solid var(--pz-color-foundation-black);
    box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.1);
    z-index: 1000;
  }

  .pz-nav__notification-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: var(--pz-space-3) var(--pz-space-4);
    background: var(--pz-color-foundation-black);
    color: white;
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .pz-nav__notification-header button {
    border: 0;
    background: transparent;
    color: var(--pz-color-earth-orange);
    font: inherit;
    font-size: 0.62rem;
    cursor: pointer;
  }

  .pz-nav__notification-empty {
    padding: var(--pz-space-5);
    color: var(--pz-color-concrete-grey);
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
  }

  .pz-nav__notification-item {
    width: 100%;
    display: grid;
    gap: 5px;
    padding: var(--pz-space-4);
    border: 0;
    border-bottom: 1px solid rgba(10, 10, 15, 0.08);
    background: transparent;
    text-align: left;
    cursor: pointer;
  }

  .pz-nav__notification-item:hover {
    background: rgba(255, 255, 255, 0.72);
  }

  .pz-nav__notification-item strong {
    color: var(--pz-color-foundation-black);
    font-size: 0.88rem;
  }

  .pz-nav__notification-item span:not(.pz-nav__notification-type),
  .pz-nav__notification-item time {
    color: var(--pz-color-concrete-grey);
    font-size: 0.75rem;
    line-height: 1.35;
  }

  .pz-nav__notification-type {
    width: fit-content;
    padding: 2px 6px;
    background: rgba(10, 10, 15, 0.06);
    color: var(--pz-color-earth-orange);
    font-family: var(--pz-font-mono);
    font-size: 0.58rem;
    font-weight: 900;
    letter-spacing: 0.12em;
  }

  .pz-nav__dropdown-wrapper {
    position: relative;
    box-sizing: border-box;
  }

  .pz-nav__profile-trigger {
    display: flex;
    align-items: center;
    gap: var(--pz-space-3);
    padding: var(--pz-space-1) var(--pz-space-3);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(255, 250, 243, 0.72));
    cursor: pointer;
    transition: all var(--pz-transition-base);
    border: 1px solid rgba(10, 10, 15, 0.08);
    box-sizing: border-box;
    box-shadow: 8px 8px 0 rgba(10, 10, 15, 0.04);
    backdrop-filter: blur(12px);
  }

  .pz-nav__profile-trigger:hover {
    background: rgba(255, 255, 255, 0.92);
    border-color: rgba(10, 10, 15, 0.12);
  }

  .pz-nav__avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--pz-color-foundation-black);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-family: var(--pz-font-mono);
    font-size: 0.8rem;
    box-sizing: border-box;
  }

  .pz-nav__username {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--pz-color-foundation-black);
    letter-spacing: -0.02em;
  }

  .pz-footer__heading {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.68);
    margin-bottom: 1rem;
  }

  .pz-nav__dropdown-icon {
    font-size: 0.8rem;
    opacity: 0.5;
  }

  .pz-nav__dropdown {
    position: absolute;
    top: calc(100% + 12px);
    right: 0;
    width: 280px;
    background: rgba(248, 246, 240, 0.98);
    border: 2px solid var(--pz-color-foundation-black);
    box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.1);
    z-index: 1000;
    overflow: hidden;
    box-sizing: border-box;
  }

  .pz-nav__dropdown-header {
    background: var(--pz-color-foundation-black);
    color: white;
    padding: var(--pz-space-3) var(--pz-space-6);
  }

  .pz-nav__dropdown-section {
    padding: var(--pz-space-4) var(--pz-space-6);
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }

  .pz-nav__dropdown-label {
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    color: var(--pz-color-concrete-grey);
    letter-spacing: 0.1em;
    margin-bottom: var(--pz-space-4);
    text-transform: uppercase;
  }

  /* Role Hub Pills inside Dropdown */
  .pz-nav__dropdown-pill-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: rgba(0, 0, 0, 0.03);
    padding: 6px;
    border-radius: 12px;
  }

  .pz-nav__dropdown-pill {
    flex: 1;
    min-width: calc(50% - 4px);
    text-align: center;
    padding: 8px 12px;
    font-size: 0.7rem;
    font-family: var(--pz-font-mono);
    text-transform: uppercase;
    text-decoration: none;
    color: var(--pz-color-text-secondary);
    border-radius: 8px;
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    border: 1px solid transparent;
  }

  .pz-nav__dropdown-pill:hover {
    transform: translateY(-1px);
    background: #f8fafc;
    color: var(--pz-color-foundation-black);
  }

  .pz-nav__dropdown-pill--active {
    background: var(--pz-color-foundation-black);
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .pz-nav__dropdown-pill--admin {
    color: var(--pz-color-earth-orange);
    border-color: rgba(234, 88, 12, 0.2);
  }

  .pz-nav__dropdown-pill--admin.pz-nav__dropdown-pill--active {
    background: var(--pz-color-earth-orange);
    color: white;
  }

  .pz-nav__dropdown-section-links {
    margin-top: var(--pz-space-4);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .pz-nav__dropdown-item {
    display: block;
    width: 100%;
    text-align: left;
    padding: var(--pz-space-2) 0;
    font-size: 0.85rem;
    color: var(--pz-color-text-secondary);
    text-decoration: none;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s;
  }

  .pz-nav__dropdown-item:hover {
    color: var(--pz-color-earth-orange);
  }

  .pz-nav__dropdown-item--admin {
    color: var(--pz-color-earth-orange);
    font-weight: bold;
  }

  .pz-nav__dropdown-item--danger {
    color: #e53e3e;
    font-weight: var(--pz-weight-bold);
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    margin-top: var(--pz-space-2);
  }

  .pz-nav__dropdown-field {
    margin-bottom: var(--pz-space-4);
    box-sizing: border-box;
  }

  .pz-nav__dropdown-field label {
    display: block;
    font-family: var(--pz-font-mono);
    font-size: 0.6rem;
    color: var(--pz-color-foundation-black);
    margin-bottom: 4px;
    font-weight: bold;
  }

  .pz-nav__select {
    width: 100%;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    padding: 6px 10px;
    font-size: 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    box-sizing: border-box;
  }

  .pz-nav__select:focus {
    outline: none;
    border-color: var(--pz-color-earth-orange);
  }

  .pz-nav__dropdown-footer {
    padding: var(--pz-space-4) var(--pz-space-6);
    background: #f8fafc;
  }

  /* Animations */
  .dropdown-slide-enter-active,
  .dropdown-slide-leave-active {
    transition: all 0.2s ease-out;
  }

  .dropdown-slide-enter-from,
  .dropdown-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }

  .pz-nav__workspace {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(10, 10, 15, 0.08);
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--pz-color-structural-steel);
    margin-right: 8px;
  }

  .pz-nav__workspace-dot {
    width: 6px;
    height: 6px;
    background: var(--pz-color-earth-orange);
    border-radius: 50%;
  }

  .pz-shell-footer {
    margin-top: var(--pz-space-16);
    padding: var(--pz-space-10) 0 var(--pz-space-8);
    background:
      linear-gradient(180deg, rgba(10, 10, 15, 0.98), rgba(18, 18, 24, 0.98)),
      radial-gradient(circle at top right, rgba(212, 101, 42, 0.18), transparent 24%),
      radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.1), transparent 20%);
    color: white;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }

  .pz-shell-footer__container {
    display: grid;
    gap: var(--pz-space-8);
  }

  .pz-shell-footer__cta {
    display: grid;
    gap: var(--pz-space-5);
    padding: var(--pz-space-6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
    box-shadow: 0 18px 48px rgba(0, 0, 0, 0.26);
  }

  .pz-shell-footer__eyebrow {
    margin: 0 0 0.75rem;
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--pz-color-earth-orange);
  }

  .pz-shell-footer__title {
    margin: 0;
    font-family: var(--pz-font-display);
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    line-height: 1.04;
    letter-spacing: -0.04em;
  }

  .pz-shell-footer__body {
    max-width: 44rem;
    margin: 0.85rem 0 0;
    color: rgba(255, 255, 255, 0.72);
    line-height: 1.7;
  }

  .pz-shell-footer__cta-links {
    display: flex;
    flex-wrap: wrap;
    gap: var(--pz-space-3);
  }

  .pz-shell-footer__button,
  .pz-shell-footer__link {
    text-decoration: none;
  }

  .pz-shell-footer__button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 2.75rem;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.06);
    color: white;
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    transition: transform var(--pz-transition-spring), border-color var(--pz-transition-base), background var(--pz-transition-base);
  }

  .pz-shell-footer__button:hover {
    transform: translate(-2px, -2px);
    border-color: var(--pz-color-earth-orange);
    background: rgba(255, 107, 43, 0.16);
    box-shadow: 10px 10px 0 rgba(255, 255, 255, 0.04);
  }

  .pz-shell-footer__grid {
    display: grid;
    gap: var(--pz-space-6);
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }

  .pz-shell-footer__column {
    display: grid;
    gap: 0.85rem;
    align-content: start;
  }

  .pz-shell-footer__heading {
    margin: 0;
    font-family: var(--pz-font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.54);
  }

  .pz-shell-footer__link {
    color: white;
    font-size: 0.95rem;
    line-height: 1.4;
    opacity: 0.86;
    transition: opacity var(--pz-transition-base), transform var(--pz-transition-spring);
  }

  .pz-shell-footer__link:hover {
    opacity: 1;
    transform: translateX(4px);
    color: var(--pz-color-earth-orange);
  }

  .pz-shell-footer__bottom {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: var(--pz-space-3);
    padding-top: var(--pz-space-5);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.46);
  }

  @media (min-width: 960px) {
    .pz-shell-footer__cta {
      grid-template-columns: minmax(0, 1.3fr) minmax(18rem, 0.9fr);
      align-items: end;
    }

    .pz-shell-footer__cta-links {
      justify-content: flex-end;
    }
  }

  .pz-nav__dropdown-item--activate {
    opacity: 0.7;
    font-size: 0.8rem;
  }

  .pz-nav__dropdown-item--activate:hover {
    opacity: 1;
  }

  .pz-nav__mobile-section-label {
    font-family: var(--pz-font-mono);
    font-size: 0.6rem;
    color: rgba(255, 255, 255, 0.4);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
  }

  .pz-nav__mobile-link--dim {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.8rem;
  }

  .u-hide-tablet {
    display: none !important;
  }

  @media (min-width: 1024px) {
    .u-hide-tablet {
      display: flex !important;
    }
  }

  .u-hide-mobile {
    display: none !important;
  }

  @media (min-width: 768px) {
    .u-hide-mobile {
      display: flex !important;
    }
  }
</style>
