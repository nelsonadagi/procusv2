<template>
  <div class="pz-auth-page">
    <Card class="pz-auth-card">
      <template #header>
        <div class="pz-u-text-center u-w-full">
          <PzPhaseIndicator :phase="1" size="small" class="u-mb-4" />
          <h1 class="pz-u-text-display u-mb-2">Induction Request</h1>
          <p class="pz-u-text-mono text-xs">JOIN THE GLOBAL CONSTRUCTION MARKETPLACE</p>
        </div>
      </template>

      <div v-if="authStore.error" class="pz-alert pz-alert--error u-mb-6">
        <span class="u-icon">⚠️</span>
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleRegister" class="l-grid l-grid--cols-1 l-grid--gap-lg">
        <PzInput v-model="form.name" label="Full Legal Name" placeholder="e.g. John Doe" required />

        <PzInput v-model="form.email" label="Communication Endpoint (Email)" type="email" placeholder="name@company.com"
          required />

        <PzInput v-model="form.password" label="Security Token (Password)" type="password" placeholder="••••••••"
          required hint="Minimum 8 characters for baseline security." />

        <div class="pz-badge pz-badge--info pz-badge--small u-w-full u-p-3"
          style="text-transform: none; line-height: 1.4;">
          <strong>Operational Note:</strong> Role initialization (Buyer, Vendor, Contractor) occurs during
          post-induction
          synchronization.
        </div>

        <Button type="submit" variant="primary" size="large" fullWidth :loading="authStore.loading">
          {{ authStore.loading ? 'Processing Induction...' : 'Request Induction' }}
        </Button>
      </form>

      <div class="u-mt-8 u-text-center text-sm pz-u-text-mono">
        ALREADY INDUCTED?
        <router-link to="/login" class="pz-u-color-earth font-bold u-ml-2">Secure Login</router-link>
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

  const form = ref({
    name: '',
    email: '',
    role: 'PROJECT_OWNER',
    password: ''
  });

  const authStore = useAuthStore();
  const router = useRouter();

  async function handleRegister() {
    const nameParts = form.value.name.trim().split(' ');
    const firstName = nameParts[0];
    const lastName = nameParts.slice(1).join(' ') || '';

    const success = await authStore.register({
      username: form.value.email,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role,
      first_name: firstName,
      last_name: lastName
    });

    if (success) {
      alert("Account created! Please sign in.");
      router.push('/login');
    }
  }
</script>

<style scoped>
  .l-auth-container {
    min-height: calc(100vh - 72px);
    background: var(--color-bg-body);
  }

  .c-alert--info {
    background-color: var(--color-primary-50);
    color: var(--color-primary-900);
    border-color: var(--color-primary-100);
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

  .u-mt-1 {
    margin-top: 0.25rem;
  }
</style>
