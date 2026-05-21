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
    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="pz-government-workflow__grid">
        <div class="pz-government-workflow__summary">
          <div class="pz-government-workflow__kicker">DISCOVERY</div>
          <h3 class="pz-government-workflow__title">Review public tenders and procurement guidance</h3>
          <p class="pz-government-workflow__body">
            Start with the public tender board. The workspace keeps discovery separate from backend-only publishing so users know exactly where to begin.
          </p>
          <div class="pz-government-workflow__actions">
            <Button variant="primary" @click="$router.push('/tenders')">View Public Tenders</Button>
            <Button variant="outline" @click="$router.push('/buyer/dashboard')">Return to Project Owner Workspace</Button>
          </div>
        </div>
        <div class="pz-government-workflow__metrics">
          <div class="pz-government-workflow__metric">
            <span>Access Level</span>
            <strong>Public Tender</strong>
          </div>
          <div class="pz-government-workflow__metric">
            <span>Status</span>
            <strong>Active</strong>
          </div>
          <div class="pz-government-workflow__metric">
            <span>Mode</span>
            <strong>Discovery</strong>
          </div>
        </div>
      </div>
    

    <ModuleCTA
      eyebrow="Procurement Action"
      title="Need to publish or review a public construction opportunity?"
      body="Use the tender workflow to expose procurement demand, then keep discovery, compliance review, and owner follow-up connected."
      primary-label="Post Tender"
      primary-to="/contracts/new"
      secondary-label="View Public Tenders"
      secondary-to="/tenders"
      tone="earth"
    />
</WorkflowGuide>

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
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
</script>

<style scoped>
.pz-government-workflow {
  margin-bottom: 1.5rem;
}

.pz-government-workflow__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.95fr);
  gap: 1rem;
  align-items: start;
}

.pz-government-workflow__summary {
  display: grid;
  gap: 0.6rem;
}

.pz-government-workflow__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-government-workflow__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1.25rem;
}

.pz-government-workflow__body {
  max-width: 58ch;
  margin: 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.55;
}

.pz-government-workflow__actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.pz-government-workflow__metrics {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.pz-government-workflow__metric {
  display: grid;
  gap: 0.2rem;
  padding: 0.85rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.8);
}

.pz-government-workflow__metric span {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-government-workflow__metric strong {
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

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

@media (max-width: 768px) {
  .pz-government-workflow__grid,
  .pz-government-workflow__metrics {
    grid-template-columns: 1fr;
  }
}
</style>
