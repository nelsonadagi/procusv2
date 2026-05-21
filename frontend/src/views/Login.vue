<template>
  <div class="pz-auth-page">
    <div class="pz-auth-shell">
      <Card class="pz-auth-card">
        <template #header>
          <div class="pz-auth-card__header">
            <p class="pz-auth-card__eyebrow">Sign in</p>
            <h1 class="pz-auth-card__title">Log in</h1>
            <p class="pz-auth-card__copy">Use your email or username and password to continue.</p>
          </div>
        </template>

        <div v-if="authStore.error" class="pz-alert pz-alert--error u-mb-6">
          <span class="u-icon">!</span>
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleLogin" class="pz-auth-form">
          <PzInput v-model="email" label="Email or username" placeholder="name@company.com" required autofocus />

          <PzInput v-model="password" label="Password" type="password" placeholder="••••••••" required />

          <Button type="submit" variant="primary" size="large" fullWidth :loading="authStore.loading">
            {{ authStore.loading ? 'Signing in...' : 'Log in' }}
          </Button>

          <div class="pz-auth-form__meta">
            <router-link :to="registerLink" class="pz-auth-form__link">Create an account</router-link>
          </div>
        </form>
      </Card>
    </div>
  </div>
</template>

<script setup>
  import { computed, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import PzInput from '../components/PzInput.vue';

  const email = ref('');
  const password = ref('');
  const authStore = useAuthStore();
  const router = useRouter();
  const route = useRoute();
  const registerLink = computed(() => {
    const redirect = safeRedirectTarget();
    return redirect ? { path: '/register', query: { redirect } } : '/register';
  });

  function safeRedirectTarget() {
    const redirect = route.query.redirect;
    if (typeof redirect !== 'string') return null;
    if (!redirect.startsWith('/') || redirect.startsWith('//')) return null;
    if (redirect === '/login' || redirect.startsWith('/login?')) return null;
    return redirect;
  }

  function defaultDashboardPath() {
    const role = authStore.user?.role;
    if (role === 'ADMIN') return '/admin';
    if (role === 'PROPERTY_MANAGER' || authStore.hasRole('PROPERTY_MANAGER')) return '/property-manager/dashboard';
    if (role === 'REAL_ESTATE_AGENT' || authStore.hasRole('REAL_ESTATE_AGENT')) return '/agent/dashboard';
    if (role === 'SURVEYOR' || authStore.hasRole('SURVEYOR')) return '/surveyor/dashboard';
    if (role === 'INVESTOR' || authStore.hasRole('INVESTOR')) return '/investor/dashboard';
    if (role === 'GOVERNMENT' || authStore.hasRole('GOVERNMENT')) return '/government/dashboard';
    if (role === 'COURIER' || authStore.hasRole('COURIER')) return '/courier/dashboard';
    if (role === 'VENDOR' || authStore.hasRole('VENDOR')) return '/vendor/dashboard';
    if (role === 'CONTRACTOR' || authStore.hasRole('CONTRACTOR')) return '/contractor/dashboard';
    return '/buyer/dashboard';
  }

  async function handleLogin() {
    const success = await authStore.login(email.value, password.value);
    if (success) {
      router.push(safeRedirectTarget() || defaultDashboardPath());
    }
  }
</script>

<style scoped>
  .pz-auth-page {
    min-height: calc(100vh - 88px);
    padding: clamp(1.5rem, 4vw, 3rem);
    display: grid;
    place-items: center;
  }

  .pz-auth-shell {
    display: grid;
    width: min(100%, 420px);
  }

  .pz-auth-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    border-width: 2px;
    box-shadow: 14px 14px 0 rgba(10, 10, 15, 0.08);
  }

  .pz-auth-card__header {
    display: grid;
    gap: 0.35rem;
  }

  .pz-auth-card__eyebrow {
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--pz-color-earth-orange);
  }

  .pz-auth-card__title {
    font-size: 2rem;
    line-height: 1.05;
    color: var(--pz-color-structural-charcoal);
  }

  .pz-auth-card__copy {
    font-size: 0.95rem;
    color: var(--pz-color-structural-steel);
  }

  .pz-auth-form {
    display: grid;
    gap: 1rem;
  }

  .pz-auth-form__meta {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 0.875rem;
  }

  .pz-auth-form__link {
    color: var(--pz-color-earth-orange);
    text-decoration: none;
    font-weight: 600;
  }

  .pz-auth-form__link:hover {
    text-decoration: underline;
  }

  .u-icon {
    font-weight: 700;
  }

  @media (max-width: 640px) {
    .pz-auth-page {
      padding: 1rem;
    }

    .pz-auth-card__title {
      font-size: 1.6rem;
    }

    .pz-auth-form__meta {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
