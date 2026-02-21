<template>
  <div class="pz-auth-page">
    <Card class="pz-auth-card">
      <template #header>
        <div class="pz-u-text-center u-w-full">
          <PzPhaseIndicator :phase="1" size="small" class="u-mb-4" />
          <h1 class="pz-u-text-display u-mb-2">Security Access</h1>
          <p class="pz-u-text-mono text-xs">GLOBAL CONSTRUCTION MARKETPLACE OS</p>
        </div>
      </template>

      <div v-if="authStore.error" class="pz-alert pz-alert--error u-mb-6">
        <span class="u-icon">⚠️</span>
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin" class="l-grid l-grid--cols-1 l-grid--gap-lg">
        <PzInput v-model="email" label="Identity (Email or Username)" placeholder="admin or name@company.com" required
          autofocus />

        <div class="c-field-group">
          <PzInput v-model="password" label="Security Credentials" type="password" placeholder="••••••••" required />
          <div class="u-mt-2 u-text-right">
            <a href="#" class="pz-u-text-mono text-xs pz-u-color-steel">Forgot credentials?</a>
          </div>
        </div>

        <Button type="submit" variant="primary" size="large" fullWidth :loading="authStore.loading">
          {{ authStore.loading ? 'Authenticating...' : 'Secure Login' }}
        </Button>
      </form>

      <div class="u-mt-8 u-text-center text-sm pz-u-text-mono">
        OFFICE OF INNOVATION ACCESS
        <router-link to="/register" class="pz-u-color-earth font-bold u-ml-2">Request Induction</router-link>
      </div>
    </Card>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import PzInput from '../components/PzInput.vue';
  import PzPhaseIndicator from '../components/PzPhaseIndicator.vue';

  const email = ref('');
  const password = ref('');
  const authStore = useAuthStore();
  const router = useRouter();

  async function handleLogin() {
    const success = await authStore.login(email.value, password.value);
    if (success) {
      const role = authStore.user?.role;
      if (role === 'VENDOR') router.push('/vendor/dashboard');
      else if (role === 'CONTRACTOR') router.push('/contractor/dashboard');
      else if (role === 'ADMIN') router.push('/admin');
      else router.push('/buyer/dashboard');
    }
  }
</script>

<style scoped>
  .l-auth-container {
    min-height: calc(100vh - 72px);
    background: var(--color-bg-body);
  }

  .u-icon {
    font-size: 1.2rem;
  }

  .u-w-full {
    width: 100%;
  }

  .u-text-center {
    text-align: center;
  }

  .u-text-muted {
    color: var(--color-text-muted);
  }

  .u-color-primary {
    color: var(--color-primary);
  }

  .u-color-muted {
    color: var(--color-text-muted);
  }

  .u-font-bold {
    font-weight: 700;
  }
</style>
