<script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from './stores/auth';
  import api from './services/api';
  import Modal from './components/ui/Modal.vue';
  import Button from './components/ui/Button.vue';
  import PzInput from './components/PzInput.vue';

  const authStore = useAuthStore();
  const router = useRouter();

  const showProfileModal = ref(false);
  const userForm = ref({
    first_name: '',
    last_name: '',
    role: '',
    roles: [],
    email: ''
  });
  const loading = ref(false);

  const availableRoles = [
    { code: 'PROJECT_OWNER', label: 'Project Owner / Buyer' },
    { code: 'CONTRACTOR', label: 'Contractor' },
    { code: 'VENDOR', label: 'Vendor / Supplier' },
    { code: 'INVESTOR', label: 'Investor' }
  ];

  const isScrolled = ref(false);
  const mobileMenuOpen = ref(false);

  onMounted(() => {
    authStore.init();
    window.addEventListener('scroll', () => {
      isScrolled.value = window.scrollY > 20;
    });
  });

  function logout() {
    authStore.logout();
    router.push('/login');
  }

  function openProfile() {
    if (authStore.user) {
      userForm.value = {
        ...authStore.user,
        roles: authStore.user.roles || [authStore.user.role] // Ensure valid list
      };
      showProfileModal.value = true;
    }
  }

  // Ensure Primary Role key is in Roles list
  watch(() => userForm.value.role, (newRole) => {
    if (newRole && !userForm.value.roles.includes(newRole)) {
      userForm.value.roles.push(newRole);
    }
  });

  async function saveProfile() {
    loading.value = true;
    // Basic Validation: Roles list must contain Primary role
    if (!userForm.value.roles.includes(userForm.value.role)) {
      userForm.value.roles.push(userForm.value.role);
    }

    try {
      const res = await api.patch('/accounts/profile/', userForm.value);
      // Update local store
      authStore.user = res.data;
      // Update localStorage
      localStorage.setItem('user', JSON.stringify(res.data));

      alert("Profile updated successfully!");
      showProfileModal.value = false;
    } catch (err) {
      console.error("Profile update failed", err);
      alert("Failed to update profile.");
    } finally {
      loading.value = false;
    }
  }
</script>

<template>
  <div class="l-app">
    <!-- 1. Modernized Main Navigation -->
    <nav class="pz-nav" :class="{ 'pz-nav--scrolled': isScrolled }">
      <div class="pz-nav__wrapper">
        <!-- Logo & Platform Name -->
        <router-link to="/" class="pz-nav__logo">
          <span class="pz-nav__logo-text">PAANGUZO</span>
          <span class="pz-nav__logo-line"></span>
        </router-link>

        <!-- Public Navigation Menu -->
        <div class="pz-nav__menu u-hide-tablet">
          <router-link to="/" class="pz-nav__link"
            :class="{ 'pz-nav__link--active': $route.path === '/' }">Marketplace</router-link>
          <router-link to="/contracts" class="pz-nav__link"
            :class="{ 'pz-nav__link--active': $route.path === '/contracts' }">Contractors</router-link>
          <router-link to="/tenders" class="pz-nav__link"
            :class="{ 'pz-nav__link--active': $route.path === '/tenders' }">Tenders</router-link>
          <router-link to="/projects" class="pz-nav__link"
            :class="{ 'pz-nav__link--active': $route.path === '/projects' }">Projects</router-link>
          <router-link to="/market/secondary" class="pz-nav__link"
            :class="{ 'pz-nav__link--active': $route.path === '/market/secondary' }">Property</router-link>
        </div>

        <!-- Role-Specific Management & User Actions -->
        <div class="pz-nav__actions">
          <div v-if="authStore.isAuthenticated" class="pz-nav__panels u-hide-tablet">
            <router-link v-if="authStore.hasRole('ADMIN')" to="/admin" class="pz-nav__pill pz-nav__pill--admin">⚙
              Admin</router-link>
            <router-link v-if="authStore.hasRole('PROJECT_OWNER')" to="/owner/dashboard"
              class="pz-nav__pill">Owner</router-link>
            <router-link v-if="authStore.hasRole('VENDOR')" to="/vendor/dashboard"
              class="pz-nav__pill">Vendor</router-link>
            <router-link v-if="authStore.hasRole('CONTRACTOR')" to="/contractor/dashboard"
              class="pz-nav__pill">Contractor</router-link>
            <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard"
              class="pz-nav__pill">Investor</router-link>
          </div>

          <template v-if="authStore.isAuthenticated">
            <!-- Admin Quick Access -->
            <router-link v-if="authStore.hasRole('ADMIN')" to="/admin" class="pz-nav__admin-btn"
              title="Admin Dashboard">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
              </svg>
              <span>Admin</span>
            </router-link>
            <button @click="openProfile" class="pz-nav__profile-trigger">
              <span class="pz-nav__avatar">👤</span>
              <span class="pz-nav__username">{{ authStore.user?.first_name }}</span>
            </button>
            <button @click="logout" title="Logout" class="pz-nav__logout-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
            </button>
          </template>

          <template v-else>
            <router-link to="/login" class="pz-nav__link">Sign In</router-link>
            <Button variant="primary" size="small" @click="router.push('/register')">Join Platform</Button>
          </template>

          <!-- Mobile Toggle -->
          <button class="pz-nav__hamburger" @click="mobileMenuOpen = !mobileMenuOpen">
            ☰
          </button>
        </div>
      </div>

      <!-- Mobile Flyout Menu -->
      <transition name="fade">
        <div v-if="mobileMenuOpen" class="pz-nav__mobile-overlay" @click="mobileMenuOpen = false">
          <div class="pz-nav__mobile-menu" @click.stop>
            <div class="pz-u-text-uppercase pz-u-color-steel u-mb-4" style="font-size: 0.75rem; font-weight: 700;">
              Public
              Marketplace</div>
            <router-link to="/" class="pz-nav__mobile-link" @click="mobileMenuOpen = false">Marketplace</router-link>
            <router-link to="/contracts" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Contractors</router-link>
            <router-link to="/tenders" class="pz-nav__mobile-link" @click="mobileMenuOpen = false">Tenders</router-link>
            <router-link to="/projects" class="pz-nav__mobile-link"
              @click="mobileMenuOpen = false">Projects</router-link>
            <router-link to="/property" class="pz-nav__mobile-link" @click="mobileMenuOpen = false">Property
              Listings</router-link>

            <template v-if="authStore.isAuthenticated">
              <hr class="u-my-6">
              <div class="pz-u-text-uppercase pz-u-color-earth u-mb-4" style="font-size: 0.75rem; font-weight: 700;">
                Management Panels</div>
              <router-link v-if="authStore.hasRole('PROJECT_OWNER')" to="/owner/dashboard" class="pz-nav__mobile-link"
                @click="mobileMenuOpen = false">Owner Panel</router-link>
              <router-link v-if="authStore.hasRole('VENDOR')" to="/vendor/dashboard" class="pz-nav__mobile-link"
                @click="mobileMenuOpen = false">Vendor Shop</router-link>
              <router-link v-if="authStore.hasRole('CONTRACTOR')" to="/contractor/dashboard" class="pz-nav__mobile-link"
                @click="mobileMenuOpen = false">Contractor Panel</router-link>
              <router-link v-if="authStore.hasRole('INVESTOR')" to="/investor/dashboard" class="pz-nav__mobile-link"
                @click="mobileMenuOpen = false">Investor Hub</router-link>

              <hr class="u-my-6">
              <button @click="openProfile(); mobileMenuOpen = false" class="pz-nav__mobile-link">Profile
                Settings</button>
              <button @click="logout(); mobileMenuOpen = false" class="pz-nav__mobile-link">Log Out</button>
            </template>
          </div>
        </div>
      </transition>
    </nav>

    <!-- 2. Main Content Area -->
    <main class="l-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 3. Premium Global Footer (Industrial Command) -->
    <footer class="pz-footer">
      <div class="pz-footer__mesh"></div>

      <!-- Precision Status Bar -->
      <div class="pz-footer__status">
        <div class="pz-l-container pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
          <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3">
            <span class="pz-status-indicator pz-status-indicator--pulse"></span>
            <span class="pz-u-text-mono text-xs u-color-savanna" style="letter-spacing: 0.2em;">PROTOCOL: NOMINAL</span>
          </div>
          <div class="pz-u-text-mono text-xs pz-u-color-concrete u-hide-mobile">
            NODE: P-CORE-2026 // UPTIME: 99.98% // ENCRYPTION: SECURE
          </div>
        </div>
      </div>

      <div class="pz-l-container pz-footer__main">
        <!-- Industrial Status Bar (Integrated) -->
        <div class="pz-footer__brand-lockup u-mb-12 u-hide-mobile">
          <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
            <h2 class="pz-u-text-display" style="font-size: 1.5rem; color: white;">BUILDING_BEYOND_BOUNDARIES</h2>
            <div class="pz-footer__cta">
              <Button variant="ghost" size="sm"
                style="border-color: rgba(255,255,255,0.1); color: rgba(255,255,255,0.6);">
                CONNECTED_TERMINAL_V1.1
              </Button>
            </div>
          </div>
        </div>

        <!-- Industrial Grid (4-Column Premium Desktop Layout) -->
        <div
          class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--lg-cols-4 pz-l-grid--gap-12 pz-u-border-t pz-pt-12"
          style="border-top-color: rgba(255,255,255,0.05);">

          <!-- Column 01: Brand Identity -->
          <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-8">
            <div class="pz-nav__logo">
              <span class="pz-nav__logo-text" style="color: white; font-size: 1.5rem;">PAANGUZO</span>
              <span class="pz-nav__logo-line" style="width: 32px;"></span>
            </div>
            <div>
              <h4 class="pz-footer__heading">SOCIAL_NODES</h4>
              <div class="pz-l-flex pz-l-flex--gap-2 pz-l-flex--wrap">
                <a href="#" class="pz-social-icon">LN</a>
                <a href="#" class="pz-social-icon">X</a>
                <a href="#" class="pz-social-icon">GH</a>
                <a href="#" class="pz-social-icon">IG</a>
              </div>
            </div>
          </div>

          <!-- Column 02: Strategic Mission -->
          <div>
            <h4 class="pz-footer__heading">01_CORE_MISSION</h4>
            <p class="pz-u-text-mono text-xs pz-u-color-concrete u-line-height-relaxed">
              THE DEFINITIVE OPERATING SYSTEM FOR GLOBAL INFRASTRUCTURE.
              ENGINEERING BEYOND BOUNDARIES THROUGH UNIFIED PROCUREMENT AND COMMAND-LEVEL LOGISTICS.
            </p>
            <div class="u-mt-12 pz-u-border-l pz-pl-6" style="border-left: 2px solid var(--pz-color-earth-orange);">
              <span class="pz-u-text-display text-lg" style="color: white; line-height: 1.2;">BUILDING THE
                FUTURE.</span>
            </div>
          </div>

          <!-- Column 03: Operational Network -->
          <div>
            <h4 class="pz-footer__heading">02_OPERATIONAL_NODES</h4>
            <ul class="pz-footer__list pz-l-grid pz-l-grid--cols-1 pz-l-grid--gap-4">
              <li><router-link to="/" class="pz-footer__link">PROCUREMENT_OS</router-link></li>
              <li><router-link to="/contracts" class="pz-footer__link">WORKS_REGISTRY</router-link></li>
              <li><router-link to="/tenders" class="pz-footer__link">TENDER_BOARD</router-link></li>
              <li><router-link to="/projects" class="pz-footer__link">PROTOCOL_CORE</router-link></li>
            </ul>
          </div>

          <!-- Column 04: Command Center -->
          <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-8">
            <div>
              <h4 class="pz-footer__heading">03_COMMAND_HUB</h4>
              <div class="pz-footer__input-wrapper u-mb-4">
                <input type="email" placeholder="OPERATOR@SYSTEM.IO" class="pz-footer__input">
                <button class="pz-footer__input-btn">➔</button>
              </div>
              <p class="pz-u-text-mono" style="font-size: 0.6rem; color: var(--pz-color-concrete-grey);">
                SECURE TLS-ENCRYPTED DATA STREAM.
              </p>
            </div>
            <div>
              <h4 class="pz-footer__heading">SYSTEM_STATUS</h4>
              <ul class="pz-footer__list">
                <li><a href="#" class="pz-footer__link pz-footer__link--dim">LEGAL.MD</a></li>
                <li><a href="#" class="pz-footer__link pz-footer__link--dim">PRIVACY.MD</a></li>
              </ul>
            </div>
          </div>
        </div>

        <div class="pz-footer__bottom">
          <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center pz-l-flex--wrap pz-l-flex--gap-4">
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">
              / PAANGUZO CORE SYSTEM / 2026 / ALL PROTOCOLS RESERVED
            </div>
            <div class="pz-l-flex pz-l-flex--gap-6">
              <a href="#" class="pz-footer__link pz-footer__link--dim">LEGAL.MD</a>
              <a href="#" class="pz-footer__link pz-footer__link--dim">PRIVACY.MD</a>
            </div>
          </div>
        </div>
      </div>
    </footer>

    <!-- 4. Global Modals -->
    <Modal :isOpen="showProfileModal" title="Sovereign Identity Settings" size="md" @close="showProfileModal = false">
      <form id="profile-form" @submit.prevent="saveProfile" class="l-grid l-grid--cols-1 pz-u-mb-4">
        <div class="l-grid l-grid--cols-2 l-grid--gap-md">
          <PzInput v-model="userForm.first_name" label="First Name" required />
          <PzInput v-model="userForm.last_name" label="Last Name" required />
        </div>

        <div class="u-mt-4">
          <PzInput v-model="userForm.email" label="Verified Email" disabled
            hint="Email cannot be changed by the user" />
        </div>

        <div class="pz-input-wrapper u-mt-4">
          <label class="pz-input__label u-mb-1">Primary Operational Role</label>
          <select v-model="userForm.role" class="pz-input">
            <option v-for="r in availableRoles" :key="r.code" :value="r.code">{{ r.label }}</option>
          </select>
          <span class="pz-input__hint">This determines your primary interface and workspace.</span>
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="showProfileModal = false">Cancel</Button>
        <Button type="submit" form="profile-form" variant="primary" :loading="loading">Synchronize Profile</Button>
      </template>
    </Modal>
  </div>
</template>

<style>

  /* 1. Main Navigation Styles (Premium Floating Glass) */
  .pz-nav {
    padding: var(--pz-space-2) var(--pz-space-4);
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
  }

  @media (min-width: 1024px) {
    .pz-nav {
      padding: var(--pz-space-4) var(--pz-space-8);
    }

    .pz-nav--scrolled {
      padding: var(--pz-space-2) var(--pz-space-8);
    }

    .pz-nav--scrolled .pz-nav__wrapper {
      background: rgba(255, 255, 255, 0.75);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.4);
    }
  }

  .pz-nav__wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin: 0 auto;
    padding: 8px 16px;
    border-radius: var(--pz-border-radius-xl, 24px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.3);
  }

  @media (min-width: 1024px) {
    .pz-nav__wrapper {
      max-width: 1440px;
      padding-inline: var(--pz-space-8);
    }
  }

  .pz-nav__logo {
    display: flex;
    flex-direction: column;
    text-decoration: none;
    transition: transform var(--pz-transition-spring);
    position: relative;
  }

  .pz-nav__logo:hover {
    transform: scale(1.05);
  }

  .pz-nav__logo-text {
    font-family: var(--pz-font-display);
    font-size: var(--pz-text-h4);
    font-weight: 800;
    color: var(--pz-color-foundation-black);
    letter-spacing: -0.02em;
    text-transform: uppercase;
    line-height: 1;
  }

  .pz-nav__logo-line {
    display: block;
    height: 4px;
    width: 24px;
    background-color: var(--pz-color-earth-orange);
    margin-top: 4px;
    transition: width var(--pz-transition-base);
  }

  .pz-nav__logo:hover .pz-nav__logo-line {
    width: 100%;
  }

  .pz-nav__menu {
    display: none;
  }

  @media (min-width: 1024px) {
    .pz-nav__menu {
      flex: 1;
      margin-left: var(--pz-space-12);
      display: flex;
      gap: 4px;
      justify-content: center;
    }
  }

  .pz-nav__link {
    font-family: var(--pz-font-mono);
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--pz-color-text-secondary);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    padding: 8px 16px;
    border-radius: var(--pz-border-radius-full);
    transition: all var(--pz-transition-spring);
    display: flex;
    align-items: center;
    background: transparent;
  }

  @media (min-width: 1024px) {
    .pz-nav__link:hover {
      color: var(--pz-color-foundation-black);
      background: rgba(0, 0, 0, 0.04);
      transform: translateY(-1px);
    }

    .pz-nav__link--active {
      color: var(--pz-color-earth-orange);
      background: rgba(255, 107, 43, 0.06);
      box-shadow: 0 4px 12px rgba(255, 107, 43, 0.08);
    }
  }

  .pz-nav__actions {
    display: flex;
    align-items: center;
    gap: var(--pz-space-1);
  }

  @media (min-width: 768px) {
    .pz-nav__actions {
      gap: var(--pz-space-3);
    }
  }

  @media (min-width: 1024px) {
    .pz-nav__actions {
      gap: var(--pz-space-6);
    }
  }

  .pz-nav__panels {
    display: none;
  }

  @media (min-width: 1024px) {
    .pz-nav__panels {
      display: flex;
      gap: 2px;
      align-items: center;
      background: rgba(0, 0, 0, 0.03);
      padding: 4px;
      border-radius: var(--pz-border-radius-full);
      border: 1px solid rgba(255, 255, 255, 0.4);
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
    }
  }

  .pz-nav__pill {
    font-family: var(--pz-font-mono);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 6px 14px;
    color: var(--pz-color-concrete-grey);
    text-decoration: none;
    transition: all var(--pz-transition-base);
    border-radius: var(--pz-border-radius-full);
  }

  .pz-nav__pill:hover,
  .pz-nav__pill--active {
    background: white;
    color: var(--pz-color-earth-orange);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  }

  /* Admin pill - visually distinct in the role panel */
  .pz-nav__pill--admin {
    background: linear-gradient(135deg, #FF6B2B, #e05520) !important;
    color: white !important;
    font-weight: 900 !important;
    box-shadow: 0 4px 12px rgba(255, 107, 43, 0.3);
    letter-spacing: 0.08em;
  }

  .pz-nav__pill--admin:hover {
    background: linear-gradient(135deg, #e05520, #c04010) !important;
    color: white !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(255, 107, 43, 0.4);
  }

  /* Admin quick-access button in the top-right action area */
  .pz-nav__admin-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: linear-gradient(135deg, #FF6B2B, #e05520);
    color: white;
    border-radius: var(--pz-border-radius-full);
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    font-weight: 800;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all var(--pz-transition-base);
    box-shadow: 0 4px 12px rgba(255, 107, 43, 0.3);
  }

  .pz-nav__admin-btn:hover {
    background: linear-gradient(135deg, #e05520, #c04010);
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(255, 107, 43, 0.45);
  }

  .pz-nav__profile-trigger {
    display: flex;
    align-items: center;
    gap: var(--pz-space-3);
    padding: 3px;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: var(--pz-border-radius-full);
    cursor: pointer;
    transition: all var(--pz-transition-spring);
  }

  .pz-nav__profile-trigger:hover {
    transform: translateY(-2px);
    box-shadow: var(--pz-shadow-md);
    border-color: var(--pz-color-earth-orange);
  }

  @media (min-width: 768px) {
    .pz-nav__profile-trigger {
      padding-right: var(--pz-space-4);
    }
  }

  .pz-nav__avatar {
    width: 32px;
    height: 32px;
    background: var(--pz-gradient-premium);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    border-radius: var(--pz-border-radius-full);
    box-shadow: var(--pz-shadow-sm);
  }

  .pz-nav__username {
    display: none;
  }

  @media (min-width: 768px) {
    .pz-nav__username {
      display: inline;
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--pz-color-foundation-black);
      letter-spacing: 0.02em;
    }
  }

  .pz-nav__hamburger {
    background: none;
    border: none;
    font-size: 1.5rem;
    padding: var(--pz-space-2);
    cursor: pointer;
    color: var(--pz-color-foundation-black);
    display: block;
  }

  @media (min-width: 1024px) {
    .pz-nav__hamburger {
      display: none;
    }
  }

  .pz-nav__logout-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    cursor: pointer;
    color: var(--pz-color-concrete-grey);
    padding: 6px;
    border-radius: var(--pz-border-radius-sm);
    transition: all var(--pz-transition-fast);
  }

  .pz-nav__logout-icon:hover {
    color: var(--pz-color-earth-orange);
    background: rgba(255, 107, 43, 0.1);
  }

  .pz-nav__mobile-overlay {
    position: fixed;
    inset: 0;
    background: rgba(10, 10, 15, 0.7);
    backdrop-filter: blur(8px);
    z-index: 2000;
  }

  .pz-nav__mobile-menu {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 320px;
    background: var(--pz-color-foundation-black);
    padding: var(--pz-space-12) var(--pz-space-8);
    display: flex;
    flex-direction: column;
    box-shadow: -20px 0 60px rgba(0, 0, 0, 0.4);
    border-left: 1px solid rgba(255, 107, 43, 0.2);
  }

  .pz-nav__mobile-link {
    font-family: var(--pz-font-mono);
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--pz-color-concrete-grey);
    text-decoration: none;
    padding: var(--pz-space-4) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    transition: all var(--pz-transition-spring);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: flex;
    align-items: center;
    gap: var(--pz-space-3);
  }

  .pz-nav__mobile-link:hover {
    color: white;
    padding-left: var(--pz-space-4);
  }

  .pz-nav__mobile-link::before {
    content: "↳";
    color: var(--pz-color-earth-orange);
    opacity: 0.5;
  }

  /* 2. Content & Footer */
  .l-main {
    min-height: calc(100vh - 80px - 400px);
  }

  /* 2. Premium Global Footer Styles */
  .pz-footer {
    position: relative;
    background: #0D0D12;
    color: white;
    padding: var(--pz-space-12) 0;
    overflow: hidden;
    margin-top: var(--pz-space-20);
    border-top: 1px solid rgba(255, 107, 43, 0.2);
  }

  @media (min-width: 1024px) {
    .pz-footer {
      padding: var(--pz-space-20) 0 var(--pz-space-12);
    }
  }

  /* Cyber Industrial Background Overlay */
  .pz-footer__mesh {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
      radial-gradient(at 0% 100%, rgba(255, 107, 43, 0.12) 0px, transparent 50%),
      radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%);
    pointer-events: none;
    z-index: 1;
  }

  .pz-footer__mesh::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 80px 80px;
    mask-image: radial-gradient(circle at center, black, transparent);
    -webkit-mask-image: radial-gradient(circle at center, black, transparent);
    opacity: 0.4;
  }

  /* Precision Terminal Status Bar */
  .pz-footer__status {
    position: relative;
    z-index: 2;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: var(--pz-blur-sm);
    -webkit-backdrop-filter: var(--pz-blur-sm);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: var(--pz-space-4) 0;
    margin-bottom: var(--pz-space-12);
  }

  @media (min-width: 1024px) {
    .pz-footer__status {
      margin-bottom: var(--pz-space-20);
      padding: var(--pz-space-5) 0;
    }
  }

  /* Scanline Effect */
  .pz-footer__status::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(transparent 0%,
        rgba(255, 107, 43, 0.08) 50%,
        transparent 100%);
    height: 400%;
    animation: pz-scanline 10s linear infinite;
    pointer-events: none;
  }

  @keyframes pz-scanline {
    0% {
      transform: translateY(-75%);
    }

    100% {
      transform: translateY(0%);
    }
  }

  .pz-status-indicator {
    width: 12px;
    height: 12px;
    background: var(--pz-color-savanna-green);
    border-radius: 50%;
    display: inline-block;
  }

  .pz-status-indicator--pulse {
    animation: pz-pulse 3s infinite;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
  }

  @keyframes pz-pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
    }

    70% {
      box-shadow: 0 0 0 15px rgba(16, 185, 129, 0);
    }

    100% {
      box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
    }
  }

  .pz-footer__main {
    position: relative;
    z-index: 2;
  }

  @media (min-width: 1024px) {
    .pz-footer__main {
      padding-inline: var(--pz-space-8);
    }
  }

  .pz-footer__brand-lockup {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: var(--pz-space-12);
    margin-bottom: var(--pz-space-12);
  }

  @media (min-width: 1024px) {
    .pz-footer__brand-lockup {
      padding-bottom: var(--pz-space-16);
      margin-bottom: var(--pz-space-16);
    }
  }

  .pz-footer__heading {
    font-family: var(--pz-font-mono);
    font-size: 0.8125rem;
    font-weight: 800;
    color: white;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: var(--pz-space-6);
    display: flex;
    align-items: center;
    gap: var(--pz-space-4);
  }

  .pz-footer__heading::before {
    content: "";
    width: 16px;
    height: 2px;
    background: var(--pz-color-earth-orange);
  }

  .pz-footer__list {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: var(--pz-space-5);
  }

  .pz-footer__link {
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    color: var(--pz-color-concrete-grey);
    text-decoration: none;
    transition: all var(--pz-transition-spring);
    display: inline-flex;
    align-items: center;
    letter-spacing: 0.05em;
  }

  .pz-footer__link:hover {
    color: white;
    transform: translateX(8px);
  }

  .pz-footer__link::before {
    content: "↳";
    margin-right: 12px;
    color: var(--pz-color-earth-orange);
    opacity: 0;
    transition: opacity var(--pz-transition-fast);
  }

  .pz-footer__link:hover::before {
    opacity: 1;
  }

  .pz-footer__link--dim {
    color: rgba(113, 128, 150, 0.5);
  }

  .pz-footer__link--dim:hover {
    color: white;
    transform: none;
  }

  .pz-footer__input-wrapper {
    display: flex;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    overflow: hidden;
    transition: all var(--pz-transition-base);
    width: 100%;
  }

  @media (min-width: 1024px) {
    .pz-footer__input-wrapper {
      max-width: 400px;
    }
  }

  .pz-footer__input-wrapper:focus-within {
    border-color: var(--pz-color-earth-orange);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 30px rgba(255, 107, 43, 0.15);
  }

  .pz-footer__input {
    background: transparent;
    border: none;
    color: white;
    padding: var(--pz-space-4) var(--pz-space-5);
    font-family: var(--pz-font-mono);
    font-size: 0.8125rem;
    flex: 1;
    width: 100%;
    outline: none;
  }

  .pz-footer__input-btn {
    background: var(--pz-color-earth-orange);
    color: white;
    border: none;
    padding: 0 var(--pz-space-6);
    cursor: pointer;
    font-weight: 800;
    transition: all var(--pz-transition-spring);
  }

  .pz-footer__input-btn:hover {
    background: white;
    color: var(--pz-color-earth-orange);
    transform: scale(1.05);
  }

  .pz-social-icon {
    font-family: var(--pz-font-mono);
    font-size: 0.6875rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    color: var(--pz-color-concrete-grey);
    text-decoration: none;
    transition: all var(--pz-transition-spring);
    padding: var(--pz-space-3) var(--pz-space-5);
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.02);
    border-radius: 4px;
    text-transform: uppercase;
  }

  .pz-social-icon:hover {
    color: white;
    background: rgba(255, 255, 255, 0.06);
    border-color: var(--pz-color-earth-orange);
    box-shadow: var(--pz-shadow-focal);
    transform: translateY(-4px);
  }

  .pz-footer__bottom {
    margin-top: var(--pz-space-16);
    padding-top: var(--pz-space-12);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  /* Transition & Utilities */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.2s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  .u-hide-tablet {
    display: none !important;
  }

  @media (min-width: 1024px) {
    .u-hide-tablet {
      display: flex !important;
    }

    /* Special case for nav menu which is center display */
    .u-hide-tablet.pz-nav__menu {
      display: flex !important;
    }
  }

  .u-show-tablet {
    display: block !important;
  }

  @media (min-width: 1024px) {
    .u-show-tablet {
      display: none !important;
    }
  }

  .u-hide-mobile {
    display: none !important;
  }

  @media (min-width: 768px) {
    .u-hide-mobile {
      display: flex !important;
    }

    /* Ensure span inside block displays correctly */
    .u-hide-mobile.pz-nav__username {
      display: inline !important;
    }
  }
</style>
