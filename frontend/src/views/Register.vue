<template>
  <div class="pz-auth-page">
    <div class="pz-auth-shell pz-auth-shell--register">
      <section class="pz-auth-shell__intro">
        <div class="pz-auth-shell__eyebrow">PLATFORM INDUCTION</div>
        <h1 class="pz-auth-shell__title">Start with one account. Expand into every workflow.</h1>
        <p class="pz-auth-shell__copy">
          Buyer, vendor, and contractor journeys begin from a shared identity layer, then branch into the right workspace after onboarding.
        </p>

        <div class="pz-auth-shell__steps">
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">01</span>
            <div>
              <h3>Identity setup</h3>
              <p>Create the core account used for platform communication and approvals.</p>
            </div>
          </div>
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">02</span>
            <div>
              <h3>Workspace selection</h3>
              <p>Start with a shared account, then activate vendor, contractor, investor, property, courier, or government workflows after sign-in.</p>
            </div>
          </div>
          <div class="pz-auth-shell__step">
            <span class="pz-auth-shell__step-index">03</span>
            <div>
              <h3>Workspace activation</h3>
              <p>Each workspace shows the next step, required documents, and approval status so you can complete it without help.</p>
            </div>
          </div>
        </div>
      </section>

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

          <div class="pz-auth-card__note">
            <span class="pz-auth-card__note-label">Operational note</span>
            <span class="pz-auth-card__note-text">
              New accounts start in the shared base workspace. The platform will guide you through additional workflows when you activate them.
            </span>
          </div>

          <Button type="submit" variant="primary" size="large" fullWidth :loading="authStore.loading">
            {{ authStore.loading ? 'Processing Induction...' : 'Request Induction' }}
          </Button>
        </form>

        <div class="u-mt-8 u-text-center text-sm pz-u-text-mono">
          ALREADY INDUCTED?
          <router-link :to="loginLink" class="pz-u-color-earth font-bold u-ml-2">Secure Login</router-link>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
  import { computed, inject, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import PzInput from '../components/PzInput.vue';
  import PzPhaseIndicator from '../components/PzPhaseIndicator.vue';

  const form = ref({
    name: '',
    email: '',
    password: ''
  });

  const authStore = useAuthStore();
  const router = useRouter();
  const route = useRoute();
  const showAlert = inject('showAlert', null);

  function safeRedirectTarget() {
    const redirect = route.query.redirect;
    if (typeof redirect !== 'string') return null;
    if (!redirect.startsWith('/') || redirect.startsWith('//')) return null;
    if (redirect === '/login' || redirect.startsWith('/login?') || redirect === '/register' || redirect.startsWith('/register?')) return null;
    return redirect;
  }

  const loginLink = computed(() => {
    const redirect = safeRedirectTarget();
    return redirect ? { path: '/login', query: { redirect } } : '/login';
  });

  async function handleRegister() {
    const nameParts = form.value.name.trim().split(' ');
    const firstName = nameParts[0];
    const lastName = nameParts.slice(1).join(' ') || '';

    const success = await authStore.register({
      username: form.value.email,
      email: form.value.email,
      password: form.value.password,
      first_name: firstName,
      last_name: lastName
    });

    if (success) {
      const redirect = safeRedirectTarget();
      if (authStore.isAuthenticated && redirect) {
        showAlert?.('Account created successfully. Continue with the activation workflow.', 'success');
        router.push(redirect);
        return;
      }
      showAlert?.('Account created successfully. Sign in to choose your workspace and complete any specialized onboarding.', 'success');
      router.push(redirect ? { path: '/login', query: { redirect } } : '/login');
    }
  }
</script>

<style scoped>
  .pz-auth-page {
    min-height: calc(100vh - 88px);
    padding: clamp(1.5rem, 4vw, 3rem);
  }

  .pz-auth-shell {
    max-width: 1180px;
    margin: 0 auto;
    display: grid;
    gap: 1.5rem;
  }

  .pz-auth-shell__intro {
    position: relative;
    overflow: hidden;
    padding: clamp(1.5rem, 4vw, 3rem);
    background:
      linear-gradient(155deg, rgba(10, 10, 15, 0.98), rgba(34, 24, 18, 0.94)),
      radial-gradient(circle at top right, rgba(212, 101, 42, 0.22), transparent 28%);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 18px 18px 0 rgba(10, 10, 15, 0.12);
  }

  .pz-auth-shell__intro::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, transparent 0, transparent calc(100% - 1px), rgba(255, 255, 255, 0.06) calc(100% - 1px)),
      linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(255, 255, 255, 0.03) calc(100% - 1px));
    background-size: 88px 88px;
    pointer-events: none;
  }

  .pz-auth-shell__eyebrow,
  .pz-auth-shell__step-index {
    font-family: var(--pz-font-mono);
    text-transform: uppercase;
    letter-spacing: 0.18em;
  }

  .pz-auth-shell__eyebrow {
    display: inline-flex;
    margin-bottom: 1rem;
    font-size: 0.72rem;
    color: var(--pz-color-earth-orange);
  }

  .pz-auth-shell__title {
    max-width: 12ch;
    font-size: clamp(2.4rem, 6vw, 4.6rem);
    line-height: 0.96;
    margin-bottom: 1rem;
    color: white;
  }

  .pz-auth-shell__copy {
    max-width: 46ch;
    color: rgba(255, 255, 255, 0.74);
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 2rem;
  }

  .pz-auth-shell__steps {
    display: grid;
    gap: 0.95rem;
  }

  .pz-auth-shell__step {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1rem;
    align-items: start;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }

  .pz-auth-shell__step-index {
    font-size: 0.68rem;
    color: var(--pz-color-savanna-green);
    padding-top: 0.2rem;
  }

  .pz-auth-shell__step h3 {
    font-size: 1.05rem;
    color: white;
    margin-bottom: 0.35rem;
  }

  .pz-auth-shell__step p {
    font-size: 0.88rem;
    line-height: 1.65;
    color: rgba(255, 255, 255, 0.68);
  }

  .pz-auth-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-width: 2px;
    box-shadow: 16px 16px 0 rgba(10, 10, 15, 0.08);
  }

  .pz-auth-card__note {
    display: grid;
    gap: 0.35rem;
    padding: 0.95rem 1rem;
    background: rgba(212, 101, 42, 0.08);
    border-left: 3px solid var(--pz-color-earth-orange);
  }

  .pz-auth-card__note-label {
    font-family: var(--pz-font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--pz-color-earth-orange);
  }

  .pz-auth-card__note-text {
    font-size: 0.92rem;
    color: var(--pz-color-structural-steel);
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

  @media (min-width: 960px) {
    .pz-auth-shell {
      grid-template-columns: minmax(0, 1.15fr) minmax(360px, 0.85fr);
      align-items: stretch;
    }
  }
</style>
