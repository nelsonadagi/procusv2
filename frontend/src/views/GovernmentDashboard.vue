<template>
  <DashboardShell
    accent="earth"
    title="Public Tender Access"
    eyebrow="GOVERNMENT PROCUREMENT WORKSPACE"
    signal-text="PROCUREMENT GRID ONLINE"
    :sidebar-groups="[
      {
        title: 'Operations',
        items: [
          { id: 'overview', label: 'Tender Overview', icon: '📋' },
          { id: 'exit', label: 'Exit Console', icon: '⇚', action: () => $router.push('/') }
        ]
      }
    ]"
    :quickstats="[
      { label: 'Access Level', value: 'Public Tender' },
      { label: 'Status', value: 'Active' },
      { label: 'Mode', value: 'Discovery' }
    ]"
  >
    <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--gap-8">
      <section class="pz-government-panel">
        <div class="pz-government-panel__body">
          <p>
            Browse the live tender surface and confirm the taxonomy and listing flow you expect before deeper procurement setup. Government-specific publishing workflows remain backend-first while tender discovery is available now.
          </p>
        </div>

        <div class="pz-government-panel__step">
          <div class="pz-government-panel__step-label">01</div>
          <div>
            <h3>Start with the public tender board</h3>
            <p>Browse active tenders, filter by region and category, and understand the procurement landscape.</p>
          </div>
        </div>

        <div class="pz-government-panel__step">
          <div class="pz-government-panel__step-label">02</div>
          <div>
            <h3>Use your shared account profile</h3>
            <p>Keep your base account active through the project owner workspace while government-specific publishing UI continues to mature.</p>
          </div>
        </div>

        <div class="pz-government-panel__actions">
          <Button variant="primary" @click="$router.push('/tenders')">View Public Tenders</Button>
          <Button variant="outline" @click="$router.push('/buyer/dashboard')">Return to Project Owner Workspace</Button>
        </div>
      </section>
    </div>
  </DashboardShell>
</template>

<script setup>
import Button from '../components/ui/Button.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
</script>

<style scoped>
.pz-government-panel {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
  box-shadow: 12px 12px 0 rgba(10, 10, 15, 0.06);
  padding: var(--pz-space-6);
  display: grid;
  gap: 1.25rem;
}

.pz-government-panel__body {
  max-width: 48rem;
  color: var(--pz-color-text-secondary);
  line-height: 1.7;
}

.pz-government-panel__step {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 1rem;
  align-items: start;
}

.pz-government-panel__step-label {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  color: var(--pz-color-earth-orange);
}

.pz-government-panel__step h3 {
  margin-bottom: 0.35rem;
}

.pz-government-panel__step p {
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

.pz-government-panel__actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}
</style>
