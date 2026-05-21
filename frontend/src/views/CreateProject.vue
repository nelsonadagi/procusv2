<template>
  <div class="project-create">
    <div class="pz-l-container u-py-10">
      <div class="project-create__header">
        <div>
          <p class="project-create__eyebrow">PROJECT INITIALIZATION</p>
          <h1 class="project-create__title">Create the project shell</h1>
          <p class="project-create__description">
            Set up the project record first. Requirements, linked contracts, funding, and updates belong in the project workspace after creation.
          </p>
        </div>

        <div class="project-create__header-actions">
          <Button variant="ghost" @click="$router.push('/owner/dashboard')">Owner Dashboard</Button>
          <Button variant="ghost" @click="$router.push('/projects')">Back to Projects</Button>
        </div>
      </div>

      <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
        <div class="project-create__workflow-banner">
          <div class="project-create__workflow-summary">
            <div class="project-create__workflow-kicker">{{ workflowSummary.stage }}</div>
            <h2 class="project-create__workflow-title">{{ workflowSummary.title }}</h2>
            <p class="project-create__workflow-body">{{ workflowSummary.body }}</p>
          </div>
          <div class="project-create__workflow-actions">
            <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
              {{ workflowSummary.primaryAction.label }}
            </Button>
            <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
              {{ workflowSummary.secondaryAction.label }}
            </Button>
          </div>
        </div>
        <div class="project-create__workflow-steps">
          <div
            v-for="step in workflowSteps"
            :key="step.label"
            class="project-create__workflow-step"
            :class="{ 'project-create__workflow-step--done': step.done, 'project-create__workflow-step--active': step.active }"
          >
            <span class="project-create__workflow-step-num">{{ step.index }}</span>
            <div class="project-create__workflow-step-content">
              <strong>{{ step.label }}</strong>
              <span>{{ step.help }}</span>
            </div>
          </div>
        </div>
      

      <ModuleCTA
        eyebrow="Procurement Ready"
        title="Already know the work package you need delivered?"
        body="Start the project here, then post a tender so contractors can respond against the same construction plan."
        primary-label="Continue Project Setup"
        primary-to="/projects/new"
        secondary-label="Post Tender"
        secondary-to="/contracts/new"
        tone="savanna"
      />
</WorkflowGuide>

      <div class="project-create__layout">
        <Card variant="premium" title="Project basics" class="project-create__form-card">
          <form @submit.prevent="createProject" class="project-create__form">
            <PzInput v-model="form.title" label="Project title" required placeholder="e.g. Riverside Apartments" />

            <PzInput
              v-model="form.description"
              label="Project description"
              type="textarea"
              rows="5"
              required
              placeholder="Briefly describe the construction scope, current opportunity, or execution intent."
            />

            <div class="project-create__section">
              <label class="pz-input__label">Location</label>
              <LocationInterface v-model="locationState" @change="handleLocationChange" />
            </div>

            <div class="project-create__budget">
              <PzInput
                v-model="form.estimated_budget"
                label="Estimated budget"
                type="number"
                min="0"
                required
                :placeholder="configStore?.activeCurrency?.symbol || 'KSh'"
              />
              <div class="project-create__flag">
                <label class="project-create__checkbox">
                  <input type="checkbox" v-model="form.funding_required" />
                  <span>Open for funding</span>
                </label>
                <p class="project-create__hint">
                  When enabled, the project will appear as funding-ready once it moves into the open phase.
                </p>
              </div>
            </div>

            <div class="project-create__actions">
              <Button type="button" variant="ghost" @click="resetForm">Reset</Button>
              <Button type="submit" variant="primary" :loading="submitting">
                {{ submitting ? 'Creating...' : 'Create project shell' }}
              </Button>
            </div>
          </form>
        </Card>

        <Card variant="premium" title="What happens next" class="project-create__preview">
          <div class="project-create__summary">
            <div class="project-create__summary-row">
              <span class="project-create__summary-label">Owner</span>
              <strong>{{ authStore.user?.username || 'Signed-in user' }}</strong>
            </div>
            <div class="project-create__summary-row">
              <span class="project-create__summary-label">Status</span>
              <Badge variant="default">LISTED</Badge>
            </div>
            <div class="project-create__summary-row">
              <span class="project-create__summary-label">Location</span>
              <strong>{{ locationSummary }}</strong>
            </div>
            <div class="project-create__summary-row">
              <span class="project-create__summary-label">Budget</span>
              <strong>{{ budgetSummary }}</strong>
            </div>
          </div>

          <div class="project-create__steps">
            <div class="project-create__step">
              <span class="project-create__step-num">01</span>
              <div>
                <h3>Publish the shell</h3>
                <p>The project record is created immediately after submission.</p>
              </div>
            </div>
            <div class="project-create__step">
              <span class="project-create__step-num">02</span>
              <div>
                <h3>Open the workspace</h3>
                <p>You land on the project detail page to add requirements and execution context.</p>
              </div>
            </div>
            <div class="project-create__step">
              <span class="project-create__step-num">03</span>
              <div>
                <h3>Run the project</h3>
                <p>Link awarded contracts, post updates, and manage funding from the detail view.</p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import ProjectsService from '../services/projects';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import PzInput from '../components/PzInput.vue';
import LocationInterface from '../components/ui/LocationInterface.vue';

const router = useRouter();
const showAlert = inject('showAlert');
const authStore = useAuthStore();
const configStore = useConfigStore();
const submitting = ref(false);

const initialForm = () => ({
  title: '',
  description: '',
  latitude: null,
  longitude: null,
  formatted_address: '',
  location_text: '',
  country: null,
  estimated_budget: '',
  funding_required: false
});

const form = ref(initialForm());

const locationState = ref({
  lat: -1.2921,
  lng: 36.8219,
  address: '',
  city: '',
  country_id: null
});

const locationSummary = computed(() => {
  return form.value.formatted_address || form.value.location_text || 'Location pending';
});

const budgetSummary = computed(() => {
  const value = Number(form.value.estimated_budget || 0);
  return configStore.formatPrice(value, configStore.activeCurrencyCode || 'KES');
});

const workflowSummary = computed(() => {
  const titleMissing = !form.value.title.trim();
  const descriptionMissing = !form.value.description.trim();
  const locationMissing = !form.value.formatted_address && !form.value.location_text;
  const budgetMissing = !form.value.estimated_budget;

  const nextStep = titleMissing || descriptionMissing
    ? 'basic'
    : locationMissing
      ? 'location'
      : budgetMissing
        ? 'budget'
        : 'submit';

  if (nextStep === 'basic') {
    return {
      stage: 'DRAFT',
      title: 'Start with the project identity',
      body: 'Add the title and description first so the project has a clear purpose before you set location or budget.',
      primaryAction: { label: 'Focus Basics', handler: () => window.scrollTo({ top: 0, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  if (nextStep === 'location') {
    return {
      stage: 'LOCATION',
      title: 'Add the project location',
      body: 'Use the map picker and address fields to make the project searchable and easy to hand off to the workspace.',
      primaryAction: { label: 'Focus Location', handler: () => window.scrollTo({ top: 180, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  if (nextStep === 'budget') {
    return {
      stage: 'BUDGET',
      title: 'Confirm the budget and funding mode',
      body: 'Set the estimated budget and decide whether the project should accept funding once it opens.',
      primaryAction: { label: 'Focus Budget', handler: () => window.scrollTo({ top: 280, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  return {
    stage: 'READY',
    title: 'Review and create the shell',
    body: 'The form is complete. Submit it to open the project workspace where requirements, contracts, milestones, and updates belong.',
    primaryAction: { label: 'Create Project', handler: createProject },
    secondaryAction: null,
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Project basics',
    help: 'Title and description explain what is being created.',
    done: Boolean(form.value.title.trim() && form.value.description.trim()),
    active: !form.value.title.trim() || !form.value.description.trim(),
  },
  {
    index: '02',
    label: 'Location',
    help: 'Address and map placement make the project searchable.',
    done: Boolean(form.value.formatted_address || form.value.location_text),
    active: Boolean(form.value.title.trim() && form.value.description.trim() && !(form.value.formatted_address || form.value.location_text)),
  },
  {
    index: '03',
    label: 'Budget and funding',
    help: 'Set the estimated budget and whether funding is open.',
    done: Boolean(form.value.estimated_budget),
    active: Boolean((form.value.formatted_address || form.value.location_text) && !form.value.estimated_budget),
  },
  {
    index: '04',
    label: 'Submit shell',
    help: 'Create the record and continue in the project workspace.',
    done: false,
    active: Boolean(form.value.title.trim() && form.value.description.trim() && (form.value.formatted_address || form.value.location_text) && form.value.estimated_budget),
  },
]);

function resetForm() {
  form.value = initialForm();
  locationState.value = {
    lat: -1.2921,
    lng: 36.8219,
    address: '',
    city: '',
    country_id: null
  };
}

function handleLocationChange(loc) {
  form.value.latitude = loc.lat;
  form.value.longitude = loc.lng;
  form.value.formatted_address = loc.address;
  form.value.location_text = loc.city;
  form.value.country = loc.country_id;
}

async function createProject() {
  if (!authStore.isAuthenticated) {
    showAlert?.('Sign in before creating a project.', 'info');
    router.push({ path: '/login', query: { redirect: '/projects/new' } });
    return;
  }

  submitting.value = true;
  try {
    const response = await ProjectsService.create(form.value);
    showAlert('Project shell created successfully.', 'success');
    router.push(`/projects/${response.data.id}`);
  } catch (err) {
    const details = err.response?.data;
    const message =
      details?.detail ||
      Object.values(details || {})
        .flat()
        .join(', ') ||
      'Failed to create project shell.';
    showAlert(message, 'error');
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.replace({ path: '/login', query: { redirect: '/projects/new' } });
  }
});
</script>

<style scoped>
.project-create {
  min-height: 100vh;
  background-color: var(--pz-color-limestone-white);
}

.project-create__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.project-create__eyebrow {
  margin: 0 0 0.35rem;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.project-create__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(2rem, 4vw, 3.2rem);
  color: var(--pz-color-foundation-black);
}

.project-create__description {
  max-width: 52rem;
  margin: 0.75rem 0 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.project-create__header-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.project-create__workflow {
  margin-bottom: 1.25rem;
}

.project-create__workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.project-create__workflow-summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.project-create__workflow-kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.project-create__workflow-title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.project-create__workflow-body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.project-create__workflow-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.project-create__workflow-steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.project-create__workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
}

.project-create__workflow-step-num {
  display: inline-flex;
  width: 1.9rem;
  height: 1.9rem;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(247, 244, 239, 0.95);
  border: 1px solid rgba(10, 10, 15, 0.12);
  color: var(--pz-color-foundation-black);
  flex-shrink: 0;
}

.project-create__workflow-step-content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.project-create__workflow-step-content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.project-create__workflow-step-content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.project-create__workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.project-create__workflow-step--done .project-create__workflow-step-num {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.project-create__workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.project-create__layout {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
  gap: 1.25rem;
}

.project-create__form {
  display: grid;
  gap: 1rem;
}

.project-create__section {
  display: grid;
  gap: 0.5rem;
}

.project-create__budget {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 1rem;
  align-items: start;
}

.project-create__flag {
  display: grid;
  gap: 0.65rem;
  padding-top: 1.85rem;
}

.project-create__checkbox {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

.project-create__hint {
  margin: 0;
  color: var(--pz-color-concrete-grey);
  line-height: 1.55;
}

.project-create__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.project-create__summary {
  display: grid;
  gap: 0.85rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.project-create__summary-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.project-create__summary-label {
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.project-create__steps {
  display: grid;
  gap: 0.95rem;
  margin-top: 1rem;
}

.project-create__step {
  display: grid;
  grid-template-columns: 3rem minmax(0, 1fr);
  gap: 0.9rem;
  align-items: start;
  padding: 0.9rem 0;
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.project-create__step:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

.project-create__step-num {
  width: 3rem;
  height: 3rem;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
}

.project-create__step h3 {
  margin: 0 0 0.25rem;
  font-family: var(--pz-font-display);
  font-size: 1.05rem;
}

.project-create__step p {
  margin: 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.55;
}

@media (max-width: 960px) {
  .project-create__header,
  .project-create__layout,
  .project-create__budget {
    grid-template-columns: 1fr;
  }

  .project-create__header {
    display: grid;
    align-items: start;
  }

  .project-create__header-actions,
  .project-create__actions {
    justify-content: flex-start;
  }

  .project-create__workflow-banner {
    grid-template-columns: 1fr;
  }

  .project-create__workflow-actions {
    justify-content: flex-start;
  }

  .project-create__workflow-steps {
    grid-template-columns: 1fr;
  }
}
</style>
