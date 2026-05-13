<template>
  <div class="pz-auth-page">
    <div class="pz-auth-shell">
      <section class="pz-auth-shell__intro">
        <div class="pz-auth-shell__eyebrow">SECURE ACCESS NODE</div>
        <h1 class="pz-auth-shell__title">Enter the construction operating system.</h1>
        <p class="pz-auth-shell__copy">
          Procurement, logistics, compliance, and project execution in one industrial control surface.
        </p>

        <div class="pz-auth-shell__metrics">
          <div class="pz-auth-shell__metric">
            <span class="pz-auth-shell__metric-value">24/7</span>
            <span class="pz-auth-shell__metric-label">system access</span>
          </div>
          <div class="pz-auth-shell__metric">
            <span class="pz-auth-shell__metric-value">Multi-role</span>
            <span class="pz-auth-shell__metric-label">buyer, vendor, contractor</span>
          </div>
          <div class="pz-auth-shell__metric">
            <span class="pz-auth-shell__metric-value">Live</span>
            <span class="pz-auth-shell__metric-label">notifications and workflow sync</span>
          </div>
        </div>

        <div class="pz-auth-shell__rail">
          <div class="pz-auth-shell__rail-item">
            <span class="pz-auth-shell__rail-label">Identity</span>
            <span class="pz-auth-shell__rail-text">Use your account email or username.</span>
          </div>
          <div class="pz-auth-shell__rail-item">
            <span class="pz-auth-shell__rail-label">Routing</span>
            <span class="pz-auth-shell__rail-text">You will be directed to the correct operational dashboard.</span>
          </div>
          <div class="pz-auth-shell__rail-item">
            <span class="pz-auth-shell__rail-label">Security</span>
            <span class="pz-auth-shell__rail-text">Profile updates, alerts, and chat remain attached to your session.</span>
          </div>
        </div>
      </section>

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

          <div class="pz-auth-card__note">
            <span class="pz-auth-card__note-label">Operational note</span>
            <span class="pz-auth-card__note-text">Live notifications and workspace routing resume after sign-in.</span>
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
      if (role === 'ADMIN') router.push('/admin');
      else if (role === 'PROPERTY_MANAGER' || authStore.hasRole('PROPERTY_MANAGER')) router.push('/property-manager/dashboard');
      else if (role === 'REAL_ESTATE_AGENT' || authStore.hasRole('REAL_ESTATE_AGENT')) router.push('/agent/dashboard');
      else if (role === 'SURVEYOR' || authStore.hasRole('SURVEYOR')) router.push('/surveyor/dashboard');
      else if (role === 'INVESTOR') router.push('/investor/dashboard');
      else if (role === 'GOVERNMENT') router.push('/government/dashboard');
      else if (role === 'COURIER') router.push('/courier/dashboard');
      else if (role === 'VENDOR') router.push('/vendor/dashboard');
      else if (role === 'CONTRACTOR') router.push('/contractor/dashboard');
      else router.push('/owner/dashboard');
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
    align-items: stretch;
  }

  .pz-auth-shell__intro {
    position: relative;
    overflow: hidden;
    padding: clamp(1.5rem, 4vw, 3rem);
    background:
      linear-gradient(135deg, rgba(10, 10, 15, 0.98), rgba(28, 28, 34, 0.94)),
      radial-gradient(circle at top right, rgba(212, 101, 42, 0.25), transparent 28%);
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
      linear-gradient(0deg, transparent 0, transparent calc(100% - 1px), rgba(255, 255, 255, 0.04) calc(100% - 1px));
    background-size: 84px 84px;
    pointer-events: none;
  }

  .pz-auth-shell__eyebrow,
  .pz-auth-shell__rail-label {
    font-family: var(--pz-font-mono);
    text-transform: uppercase;
    letter-spacing: 0.18em;
  }

  .pz-auth-shell__eyebrow {
    display: inline-flex;
    margin-bottom: 1rem;
    font-size: 0.72rem;
    color: var(--pz-color-savanna-green);
  }

  .pz-auth-shell__title {
    max-width: 12ch;
    font-size: clamp(2.6rem, 6vw, 4.8rem);
    line-height: 0.94;
    margin-bottom: 1rem;
    color: white;
  }

  .pz-auth-shell__copy {
    max-width: 46ch;
    color: rgba(255, 255, 255, 0.75);
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 2rem;
  }

  .pz-auth-shell__metrics {
    display: grid;
    gap: 0.85rem;
    margin-bottom: 2rem;
  }

  .pz-auth-shell__metric {
    display: grid;
    gap: 0.35rem;
    padding: 0.95rem 1rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
  }

  .pz-auth-shell__metric-value {
    font-family: var(--pz-font-display);
    font-size: 1.15rem;
    color: white;
  }

  .pz-auth-shell__metric-label,
  .pz-auth-shell__rail-text {
    font-family: var(--pz-font-mono);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255, 255, 255, 0.62);
  }

  .pz-auth-shell__rail {
    display: grid;
    gap: 0.9rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .pz-auth-shell__rail-item {
    display: grid;
    gap: 0.35rem;
  }

  .pz-auth-shell__rail-label {
    font-size: 0.64rem;
    color: var(--pz-color-earth-orange);
  }

  .pz-auth-card {
    align-self: stretch;
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
      grid-template-columns: minmax(0, 1.2fr) minmax(360px, 0.8fr);
    }
  }
</style>
