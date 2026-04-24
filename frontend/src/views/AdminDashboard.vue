<template>
  <div>
    <DashboardShell
      v-model:active-section="activeTab"
      accent="earth"
      title="Admin Control"
      eyebrow="PLATFORM MANAGEMENT"
      signal-text="CONTROL GRID ONLINE"
      :quickstats="[
        { label: 'Zone', value: 'Admin Core' },
        { label: 'Modules', value: tabs.length },
        { label: 'Mode', value: 'Oversight' }
      ]"
      :sidebar-groups="[
        {
          title: 'Platform Control',
          items: tabs.map(t => ({ id: t.id, label: t.name, icon: t.icon }))
        },
        {
          title: 'Session',
          items: [
            { id: 'logout', label: 'Log Out', icon: '⇚', action: logout }
          ]
        }
      ]"
    >
      <template #headerActions>
        <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
          <div class="pz-status-indicator pz-status-indicator--pulse"></div>
          <Badge variant="primary">Admin Control</Badge>
        </div>
      </template>

      <transition name="fade" mode="out-in">
        <div :key="activeTab">
          <OverviewSection v-if="activeTab === 'overview'" />
          <VerificationsSection v-else-if="activeTab === 'verifications'" />
          <UserManagementSection v-else-if="activeTab === 'users'" @add-user="showAddUser = true" />
          <SystemConfigSection v-else-if="activeTab === 'config'" />
          <ReportsSection v-else-if="activeTab === 'reports'" />
          <PropertiesSection v-else-if="activeTab === 'properties'" />
          <ModerationSection v-else-if="activeTab === 'contracts'" />
          <SecurityMonitorSection v-else-if="activeTab === 'security'" />
          <div v-else class="pz-module-state">
            <div class="pz-module-state__kicker">MODULE_STANDBY</div>
            <h3 class="pz-module-state__title">{{ currentTabName }} is not wired into the console yet</h3>
            <p class="pz-module-state__body">
              The shell is in place, but this admin module still needs its operational surface connected to live data and actions.
            </p>
          </div>
        </div>
      </transition>
    </DashboardShell>

    <Modal :isOpen="showAddUser" title="Add New User" @close="showAddUser = false">
      <div class="pz-p-6 pz-u-text-mono text-xs">
        User management is currently active.
        Please use the central portal for new user creation.
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, defineAsyncComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Badge from '../components/ui/Badge.vue';
import Modal from '../components/ui/Modal.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';

const OverviewSection = defineAsyncComponent(() => import('../components/admin/OverviewSection.vue'));
const VerificationsSection = defineAsyncComponent(() => import('../components/admin/VerificationsSection.vue'));
const UserManagementSection = defineAsyncComponent(() => import('../components/admin/UserManagementSection.vue'));
const SystemConfigSection = defineAsyncComponent(() => import('../components/admin/SystemConfigSection.vue'));
const ReportsSection = defineAsyncComponent(() => import('../components/admin/ReportsSection.vue'));
const PropertiesSection = defineAsyncComponent(() => import('../components/admin/PropertiesSection.vue'));
const SecurityMonitorSection = defineAsyncComponent(() => import('../components/admin/SecurityMonitorSection.vue'));
const ModerationSection = defineAsyncComponent(() => import('../components/admin/ModerationSection.vue'));

const activeTab = ref('overview');
const router = useRouter();
const authStore = useAuthStore();
const tabs = [
  { id: 'overview', name: 'Dashboard', icon: '◰' },
  { id: 'verifications', name: 'Verifications', icon: '🛡' },
  { id: 'properties', name: 'Real Estate', icon: '◰' },
  { id: 'contracts', name: 'Moderation', icon: '◈' },
  { id: 'reports', name: 'Reports', icon: '📊' },
  { id: 'users', name: 'Operators', icon: '⧇' },
  { id: 'security', name: 'Security', icon: '🛡' },
  { id: 'config', name: 'Settings', icon: '⚙' }
];

const showAddUser = ref(false);

const currentTabName = computed(() => tabs.find(t => t.id === activeTab.value)?.name);

function logout() {
  authStore.logout();
  router.push('/login');
}
</script>

<style scoped>
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
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@media (prefers-reduced-motion: reduce) {
  .pz-status-indicator--pulse {
    animation: none;
  }
}

.pz-module-state {
  padding: clamp(1.5rem, 4vw, 2.5rem);
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(10, 10, 15, 0.12);
  box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.06);
}

.pz-module-state__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-concrete-grey);
  text-transform: uppercase;
}

.pz-module-state__title {
  margin: 0.7rem 0 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.4rem, 2.5vw, 2rem);
}

.pz-module-state__body {
  max-width: 42rem;
  margin: 0.8rem 0 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.65;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
