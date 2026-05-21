<template>
  <div class="pz-l-container pz-contract-posting u-py-12">
    <div class="pz-contract-posting__hero">
      <div class="pz-contract-posting__hero-copy">
        <div class="pz-contract-posting__eyebrow-row">
          <p class="pz-u-text-mono text-xs pz-u-color-earth">PROCUREMENT BRIEF</p>
          <Badge variant="info" size="sm">OWNER WORKSPACE</Badge>
        </div>
        <h1 class="pz-u-text-display">Post a work order contractors can price with confidence.</h1>
        <p class="pz-u-text-mono text-sm pz-u-color-steel">
          Keep the brief sharp, visual, and complete. The form below captures the scope, category, timing, commercial range, and bid conditions in one place.
        </p>
        <div class="pz-contract-posting__hero-stats">
          <div class="pz-contract-posting__stat">
            <span class="pz-u-text-mono text-xs pz-u-color-concrete">Completeness</span>
            <strong>{{ briefCompletion }}%</strong>
          </div>
          <div class="pz-contract-posting__stat">
            <span class="pz-u-text-mono text-xs pz-u-color-concrete">Budget Range</span>
            <strong>{{ budgetPreview }}</strong>
          </div>
          <div class="pz-contract-posting__stat">
            <span class="pz-u-text-mono text-xs pz-u-color-concrete">Deadline</span>
            <strong>{{ deadlinePreview }}</strong>
          </div>
        </div>
      </div>
      <div class="pz-contract-posting__hero-note">
        <div>
          <span class="pz-u-text-mono text-xs pz-u-color-concrete">Minimum brief</span>
          <strong>Scope, location, budget, dates, category, and image</strong>
        </div>
        <div class="pz-contract-posting__hero-badges">
          <Badge variant="ghost" size="sm">TENDER READY</Badge>
          <Badge variant="ghost" size="sm">BID SAFE</Badge>
        </div>
      </div>
    </div>

    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="pz-contract-posting__workflow">
        <div class="pz-contract-posting__workflow-summary">
          <div class="pz-contract-posting__workflow-kicker">{{ workflowSummary.stage }}</div>
          <h2 class="pz-contract-posting__workflow-title">{{ workflowSummary.title }}</h2>
          <p class="pz-contract-posting__workflow-body">{{ workflowSummary.body }}</p>
        </div>
        <div class="pz-contract-posting__workflow-actions">
          <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
            {{ workflowSummary.primaryAction.label }}
          </Button>
          <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
            {{ workflowSummary.secondaryAction.label }}
          </Button>
        </div>
      </div>
      <div class="pz-contract-posting__workflow-steps">
        <div
          v-for="step in workflowSteps"
          :key="step.label"
          class="pz-contract-posting__workflow-step"
          :class="{ 'pz-contract-posting__workflow-step--done': step.done, 'pz-contract-posting__workflow-step--active': step.active }"
        >
          <span class="pz-contract-posting__workflow-step-num">{{ step.index }}</span>
          <div class="pz-contract-posting__workflow-step-content">
            <strong>{{ step.label }}</strong>
            <span>{{ step.help }}</span>
          </div>
        </div>
      </div>
    

    <ModuleCTA
      eyebrow="Supplier Readiness"
      title="This tender may need materials and delivery support too."
      body="After posting the contract, use vendor and courier workspaces to line up product availability and site logistics."
      primary-label="Browse Materials"
      primary-to="/products"
      secondary-label="Open Courier Workspace"
      secondary-to="/courier/dashboard"
      tone="savanna"
    />
</WorkflowGuide>

    <div class="pz-contract-workspace">
      <Card title="Post a New Contract" eyebrow="Structured procurement" class="pz-contract-form-card" variant="premium">
        <form @submit.prevent="postContract" class="pz-contract-form">
          <div class="pz-contract-section">
            <div class="pz-contract-section__header">
              <div>
                <div class="pz-contract-section__title">1. Core Brief</div>
                <div class="pz-contract-section__body">Define what needs to be done, where it is, and which trade category it belongs to.</div>
              </div>
            </div>
            <div class="pz-contract-grid pz-contract-grid--two">
              <PzInput v-model="form.title" label="Contract Title" required placeholder="Example: Roof replacement and waterproofing" />
              <PzInput v-model="form.location" label="Location" required placeholder="Example: Nairobi, Kilimani" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label" for="category">Category <span class="pz-input__required" aria-hidden="true">*</span></label>
                <select id="category" v-model="form.category_uuid" class="pz-input" required>
                  <option disabled value="">Select category</option>
                  <option v-for="option in categoryOptions" :key="option.value" :value="option.value">
                    {{ option.label }}
                  </option>
                </select>
                <span class="pz-input__hint">Choose the closest trade or service category.</span>
              </div>
              <div class="pz-input-wrapper">
                <label class="pz-input__label" for="currency">Currency</label>
                <select id="currency" v-model="form.currency" class="pz-input">
                  <option value="KES">KES</option>
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                </select>
                <span class="pz-input__hint">The currency contractors should price in.</span>
              </div>
            </div>
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Contract Description</label>
              <textarea
                v-model="form.description_scope"
                class="pz-input pz-contract-textarea"
                rows="6"
                required
                placeholder="Describe the site, scope boundaries, deliverables, assumptions, and anything the contractor must know before bidding."
              ></textarea>
            </div>
          </div>

          <div class="pz-contract-section">
            <div class="pz-contract-section__header">
              <div>
                <div class="pz-contract-section__title">2. Commercial Range</div>
                <div class="pz-contract-section__body">Give contractors the corridor they need to price realistically.</div>
              </div>
            </div>
            <div class="pz-contract-grid pz-contract-grid--three">
              <PzInput v-model="form.budget_min" label="Minimum Budget" type="number" inputmode="decimal" min="0" required placeholder="0" />
              <PzInput v-model="form.budget_max" label="Maximum Budget" type="number" inputmode="decimal" min="0" required placeholder="0" />
              <PzInput v-model="form.bid_deadline" label="Bid Deadline" type="datetime-local" required />
              <PzInput v-model="form.project_start_date" label="Project Start Date" type="date" required />
              <PzInput v-model="form.project_end_date" label="Project End Date" type="date" required />
              <div class="pz-contract-mini-summary">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">Timeline</span>
                <strong>{{ timelinePreview }}</strong>
                <span class="pz-u-text-mono text-xs pz-u-color-steel">Project dates should reflect the real execution window.</span>
              </div>
            </div>
          </div>

          <div class="pz-contract-section">
            <div class="pz-contract-section__header">
              <div>
                <div class="pz-contract-section__title">3. Visual Context</div>
                <div class="pz-contract-section__body">Attach a site image or rendering so bidders know what they are pricing.</div>
              </div>
            </div>
            <div class="pz-contract-upload">
              <label class="pz-contract-upload__dropzone">
                <input type="file" accept="image/*" class="u-sr-only" @change="handleFeaturedImageChange" />
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">Featured Image</span>
                <strong>{{ featuredImageLabel }}</strong>
                <span class="pz-u-text-mono text-xs pz-u-color-steel">Upload a site photo, rendering, or cover image.</span>
              </label>
              <div v-if="featuredImagePreview" class="pz-contract-upload__preview">
                <img :src="featuredImagePreview" alt="Featured image preview" />
              </div>
            </div>
          </div>

          <div class="pz-contract-section">
            <div class="pz-contract-section__header">
              <div>
                <div class="pz-contract-section__title">4. Bid Conditions</div>
                <div class="pz-contract-section__body">Optional terms that improve the quality of received bids.</div>
              </div>
            </div>
            <div class="pz-contract-grid pz-contract-grid--two">
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Payment Terms</label>
                <textarea
                  v-model="form.payment_terms"
                  class="pz-input pz-contract-textarea"
                  rows="5"
                  placeholder="30% advance, milestone payments, retention, sign-off rules, and any commercial terms."
                ></textarea>
              </div>
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Eligibility Criteria</label>
                <textarea
                  v-model="form.eligibility_criteria"
                  class="pz-input pz-contract-textarea"
                  rows="5"
                  placeholder="Required contractor class, insurance, experience, site visit requirements, and any pre-qualification conditions."
                ></textarea>
              </div>
            </div>
          </div>

          <div class="pz-contract-actions">
            <div class="pz-contract-actions__group">
              <Button type="button" variant="ghost" size="large" @click="router.push('/owner/dashboard')">Back to Dashboard</Button>
              <Button type="button" variant="ghost" size="large" @click="router.push('/contracts')">Back to Contracts</Button>
            </div>
            <Button type="submit" variant="primary" size="large" :loading="submitting">
              {{ submitting ? 'Posting...' : 'Post Work Order' }}
            </Button>
          </div>
        </form>
      </Card>

      <aside class="pz-contract-summary">
        <Card title="Live Brief Preview" eyebrow="What contractors will see" variant="glass" class="pz-contract-summary__card" body-class="pz-contract-summary__body">
          <div class="pz-contract-summary__hero">
            <div class="pz-contract-summary__image">
              <img v-if="featuredImagePreview" :src="featuredImagePreview" alt="Featured image preview" />
              <div v-else class="pz-contract-summary__image-placeholder">
                <span>Upload a cover image</span>
              </div>
            </div>
            <div class="pz-contract-summary__identity">
              <span class="pz-contract-summary__eyebrow">{{ selectedCategoryLabel || 'Category pending' }}</span>
              <h3>{{ form.title || 'Untitled work order' }}</h3>
              <p>{{ form.location || 'Location will appear here' }}</p>
            </div>
          </div>

          <div class="pz-contract-summary__metrics">
            <div>
              <span>Budget</span>
              <strong>{{ budgetPreview }}</strong>
            </div>
            <div>
              <span>Deadline</span>
              <strong>{{ deadlinePreview }}</strong>
            </div>
            <div>
              <span>Timeline</span>
              <strong>{{ timelinePreview }}</strong>
            </div>
          </div>

          <div class="pz-contract-summary__stack">
            <div class="pz-contract-summary__line">
              <span>Currency</span>
              <strong>{{ form.currency }}</strong>
            </div>
            <div class="pz-contract-summary__line">
              <span>Payment terms</span>
              <strong>{{ form.payment_terms ? 'Added' : 'Not set' }}</strong>
            </div>
            <div class="pz-contract-summary__line">
              <span>Eligibility</span>
              <strong>{{ form.eligibility_criteria ? 'Added' : 'Not set' }}</strong>
            </div>
          </div>
        </Card>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import api from '../services/api';
import ContractsService from '../services/contracts';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import PzInput from '../components/PzInput.vue';

const router = useRouter();
const authStore = useAuthStore();
const showAlert = inject('showAlert');
const submitting = ref(false);
const categories = ref([]);
const form = ref({
  title: '',
  description_scope: '',
  location: '',
  budget_min: '',
  budget_max: '',
  currency: 'KES',
  category_uuid: '',
  bid_deadline: '',
  project_start_date: '',
  project_end_date: '',
  payment_terms: '',
  eligibility_criteria: '',
  featured_image: null,
});

const featuredImageLabel = computed(() => form.value.featured_image?.name || 'Choose an image');
const featuredImagePreview = ref('');
let previewObjectUrl = '';

const categoryOptions = computed(() => flattenCategories(categories.value));
const selectedCategoryLabel = computed(() => {
  const match = categoryOptions.value.find((option) => option.value === form.value.category_uuid);
  return match?.label || '';
});
const budgetPreview = computed(() => formatBudgetRange(form.value.currency, form.value.budget_min, form.value.budget_max));
const deadlinePreview = computed(() => deadlineLabel(form.value.bid_deadline));
const timelinePreview = computed(() => formatTimeline(form.value.project_start_date, form.value.project_end_date));
const briefCompletion = computed(() => {
  const fields = [
    form.value.title,
    form.value.description_scope,
    form.value.location,
    form.value.category_uuid,
    form.value.bid_deadline,
    form.value.project_start_date,
    form.value.project_end_date,
    form.value.featured_image,
    form.value.budget_min,
    form.value.budget_max,
  ];
  const filled = fields.filter((value) => value !== null && value !== undefined && value !== '').length;
  return Math.round((filled / fields.length) * 100);
});

const workflowSummary = computed(() => {
  const missingTitle = !form.value.title.trim();
  const missingScope = !form.value.description_scope.trim();
  const missingLocation = !form.value.location.trim();
  const missingBudget = !form.value.budget_min || !form.value.budget_max;
  const missingDates = !form.value.bid_deadline || !form.value.project_start_date || !form.value.project_end_date;
  const missingCategory = !form.value.category_uuid;
  const missingImage = !form.value.featured_image;

  if (missingTitle || missingScope) {
    return {
      stage: 'BRIEF',
      title: 'Write the work order in plain language',
      body: 'Start with the title and scope so contractors understand what is being priced before they open the tender.',
      primaryAction: { label: 'Focus Brief', handler: () => window.scrollTo({ top: 0, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  if (missingLocation || missingCategory) {
    return {
      stage: 'CLASSIFY',
      title: 'Add location and category',
      body: 'Place the work in the right region and trade category so the right contractors see it.',
      primaryAction: { label: 'Focus Classification', handler: () => window.scrollTo({ top: 220, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  if (missingBudget || missingDates || missingImage) {
    return {
      stage: 'READYING',
      title: 'Complete the commercial details',
      body: 'Set the budget corridor, dates, and image so the brief is complete enough for serious bidding.',
      primaryAction: { label: 'Focus Commercials', handler: () => window.scrollTo({ top: 420, behavior: 'smooth' }) },
      secondaryAction: null,
    };
  }

  return {
    stage: 'READY',
    title: 'Review and broadcast the tender',
    body: 'The brief is complete. Post it to the market so contractors can start reviewing and bidding.',
    primaryAction: { label: 'Post Work Order', handler: postContract },
    secondaryAction: null,
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Write the brief',
    help: 'Title and scope explain the work.',
    done: Boolean(form.value.title.trim() && form.value.description_scope.trim()),
    active: !form.value.title.trim() || !form.value.description_scope.trim(),
  },
  {
    index: '02',
    label: 'Classify the work',
    help: 'Location and category route the tender to the right contractors.',
    done: Boolean(form.value.location.trim() && form.value.category_uuid),
    active: Boolean(form.value.title.trim() && form.value.description_scope.trim() && (!form.value.location.trim() || !form.value.category_uuid)),
  },
  {
    index: '03',
    label: 'Confirm commercials',
    help: 'Budget corridor, dates, and image make the tender usable.',
    done: Boolean(form.value.budget_min && form.value.budget_max && form.value.bid_deadline && form.value.project_start_date && form.value.project_end_date && form.value.featured_image),
    active: Boolean(form.value.location.trim() && form.value.category_uuid && (!form.value.budget_min || !form.value.budget_max || !form.value.bid_deadline || !form.value.project_start_date || !form.value.project_end_date || !form.value.featured_image)),
  },
  {
    index: '04',
    label: 'Broadcast the tender',
    help: 'Submit the work order to open bidding.',
    done: false,
    active: Boolean(form.value.title.trim() && form.value.description_scope.trim() && form.value.location.trim() && form.value.category_uuid && form.value.budget_min && form.value.budget_max && form.value.bid_deadline && form.value.project_start_date && form.value.project_end_date && form.value.featured_image),
  },
]);

function flattenCategories(items, depth = 0, output = []) {
  items.forEach((item) => {
    output.push({
      value: item.id,
      label: `${depth ? `${'› '.repeat(depth)}` : ''}${item.name}`,
    });
    if (item.children?.length) {
      flattenCategories(item.children, depth + 1, output);
    }
  });
  return output;
}

async function fetchCategories() {
  try {
    const res = await api.get('/taxonomy/categories/', { params: { taxonomy_type: 'SERVICE', tree: 'true' } });
    categories.value = res.data.results || res.data;
  } catch (err) {
    console.error(err);
    showAlert?.('Could not load contract categories.', 'error');
  }
}

function handleFeaturedImageChange(event) {
  const [file] = event.target.files || [];
  form.value.featured_image = file || null;
}

watch(
  () => form.value.featured_image,
  (file) => {
    if (previewObjectUrl) {
      URL.revokeObjectURL(previewObjectUrl);
      previewObjectUrl = '';
    }
    if (file) {
      previewObjectUrl = URL.createObjectURL(file);
      featuredImagePreview.value = previewObjectUrl;
    } else {
      featuredImagePreview.value = '';
    }
  },
  { immediate: true }
);

onBeforeUnmount(() => {
  if (previewObjectUrl) {
    URL.revokeObjectURL(previewObjectUrl);
  }
});

function appendIfPresent(data, key, value) {
  if (value !== null && value !== undefined && value !== '') {
    data.append(key, value);
  }
}

function formatNumber(amount) {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return '0';
  return value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

function formatBudgetRange(currency, min, max) {
  const cur = currency || 'KES';
  const minValue = min !== '' && min !== null && min !== undefined ? formatNumber(min) : '';
  const maxValue = max !== '' && max !== null && max !== undefined ? formatNumber(max) : '';
  if (minValue && maxValue) return `${cur} ${minValue} - ${cur} ${maxValue}`;
  if (maxValue) return `Up to ${cur} ${maxValue}`;
  if (minValue) return `From ${cur} ${minValue}`;
  return 'Budget pending';
}

function formatTimeline(startDate, endDate) {
  if (!startDate && !endDate) return 'Timeline pending';
  const start = startDate ? new Date(startDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : 'Start TBD';
  const end = endDate ? new Date(endDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : 'End TBD';
  return `${start} → ${end}`;
}

function deadlineLabel(value) {
  if (!value) return 'Deadline pending';
  const deadline = new Date(value);
  const diffDays = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
  if (diffDays > 1) return `Closes in ${diffDays} days`;
  if (diffDays === 1) return 'Closes tomorrow';
  if (diffDays === 0) return 'Closes today';
  return `Closed ${Math.abs(diffDays)} days ago`;
}

async function postContract() {
  if (!authStore.isAuthenticated) {
    showAlert?.('Sign in before posting a tender.', 'info');
    router.push({ path: '/login', query: { redirect: '/contracts/new' } });
    return;
  }

  submitting.value = true;
  try {
    const payload = new FormData();
    appendIfPresent(payload, 'title', form.value.title);
    appendIfPresent(payload, 'description_scope', form.value.description_scope);
    appendIfPresent(payload, 'location', form.value.location);
    appendIfPresent(payload, 'budget_min', form.value.budget_min);
    appendIfPresent(payload, 'budget_max', form.value.budget_max);
    appendIfPresent(payload, 'currency', form.value.currency);
    appendIfPresent(payload, 'category_uuid', form.value.category_uuid);
    appendIfPresent(payload, 'bid_deadline', form.value.bid_deadline);
    appendIfPresent(payload, 'project_start_date', form.value.project_start_date);
    appendIfPresent(payload, 'project_end_date', form.value.project_end_date);
    appendIfPresent(payload, 'payment_terms', form.value.payment_terms);
    appendIfPresent(payload, 'eligibility_criteria', form.value.eligibility_criteria);
    if (form.value.featured_image) {
      payload.append('featured_image', form.value.featured_image);
    }

    await ContractsService.create(payload);
    showAlert('Tender broadcast initiated successfully.', 'success');
    router.push('/contracts');
  } catch (err) {
    console.error(err);
    showAlert(err.response?.data?.detail || 'Failed to broadcast tender.', 'error');
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.replace({ path: '/login', query: { redirect: '/contracts/new' } });
    return;
  }
  fetchCategories();
});
</script>

<style scoped>
.pz-contract-posting {
  display: grid;
  gap: 1.5rem;
}

.pz-contract-posting__workflow {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.pz-contract-posting__workflow-summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.pz-contract-posting__workflow-kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-contract-posting__workflow-title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.pz-contract-posting__workflow-body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.pz-contract-posting__workflow-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.pz-contract-posting__workflow-steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.pz-contract-posting__workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
}

.pz-contract-posting__workflow-step-num {
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

.pz-contract-posting__workflow-step-content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.pz-contract-posting__workflow-step-content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.pz-contract-posting__workflow-step-content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pz-contract-posting__workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.pz-contract-posting__workflow-step--done .pz-contract-posting__workflow-step-num {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.pz-contract-posting__workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-contract-posting__hero {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.55fr) minmax(18rem, 0.95fr);
}

.pz-contract-posting__eyebrow-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.pz-contract-posting__hero-copy,
.pz-contract-posting__hero-note {
  padding: 1.4rem 1.5rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 1px 2px rgba(10, 10, 15, 0.03);
}

.pz-contract-posting__hero-copy {
  display: grid;
  gap: 0.8rem;
}

.pz-contract-posting__hero-copy h1 {
  font-size: clamp(2rem, 4vw, 3.25rem);
  line-height: 1.05;
}

.pz-contract-posting__hero-stats {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.pz-contract-posting__stat {
  padding: 0.85rem 0.95rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(10, 10, 15, 0.08);
  display: grid;
  gap: 0.2rem;
}

.pz-contract-posting__stat strong {
  font-family: var(--pz-font-display);
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pz-contract-posting__hero-note {
  display: grid;
  gap: 1rem;
  align-content: space-between;
}

.pz-contract-posting__hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.pz-contract-workspace {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: minmax(0, 1.9fr) minmax(18rem, 0.95fr);
  align-items: start;
}

.pz-contract-form-card {
  height: 100%;
}

.pz-contract-form {
  display: grid;
  gap: 1rem;
}

.pz-contract-section {
  display: grid;
  gap: 1rem;
  padding: 1.15rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 18px;
  background: rgba(247, 244, 239, 0.65);
  box-shadow: 0 1px 2px rgba(10, 10, 15, 0.03);
}

.pz-contract-section__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.pz-contract-section__title {
  font-family: var(--pz-font-display);
  font-size: 1.05rem;
  font-weight: 700;
}

.pz-contract-section__body {
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-grid {
  display: grid;
  gap: 1rem;
}

.pz-contract-grid--two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pz-contract-grid--three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.pz-contract-textarea {
  resize: vertical;
  min-height: 8rem;
}

.pz-contract-mini-summary {
  padding: 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(10, 10, 15, 0.08);
  display: grid;
  gap: 0.35rem;
  align-content: start;
}

.pz-contract-upload {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
  align-items: start;
}

.pz-contract-upload__dropzone {
  display: grid;
  gap: 0.55rem;
  padding: 1rem;
  border: 1px dashed rgba(10, 10, 15, 0.14);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.85);
  cursor: pointer;
}

.pz-contract-upload__preview {
  border-radius: 16px;
  overflow: hidden;
  min-height: 14rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
}

.pz-contract-upload__preview img {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 14rem;
  object-fit: cover;
}

.pz-contract-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  padding-top: 0.25rem;
  border-top: 1px solid rgba(10, 10, 15, 0.08);
  position: sticky;
  bottom: 0;
  background: linear-gradient(180deg, rgba(251, 248, 243, 0.35), rgba(251, 248, 243, 0.92));
  backdrop-filter: blur(8px);
}

.pz-contract-actions__group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.pz-contract-summary {
  position: sticky;
  top: 1.25rem;
}

.pz-contract-summary__body {
  display: grid;
  gap: 1rem;
}

.pz-contract-summary__hero {
  display: grid;
  gap: 0.9rem;
}

.pz-contract-summary__image {
  border-radius: 18px;
  overflow: hidden;
  min-height: 13rem;
  background: linear-gradient(135deg, rgba(212, 101, 42, 0.08), rgba(10, 10, 15, 0.06));
  border: 1px solid rgba(10, 10, 15, 0.08);
}

.pz-contract-summary__image img {
  width: 100%;
  height: 100%;
  min-height: 13rem;
  object-fit: cover;
  display: block;
}

.pz-contract-summary__image-placeholder {
  min-height: 13rem;
  display: grid;
  place-items: center;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-summary__identity h3 {
  margin: 0.25rem 0;
  font-family: var(--pz-font-display);
  font-size: 1.4rem;
  line-height: 1.1;
}

.pz-contract-summary__identity p {
  margin: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  color: var(--pz-color-structural-steel);
}

.pz-contract-summary__eyebrow {
  display: inline-flex;
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-contract-summary__metrics {
  display: grid;
  gap: 0.65rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.pz-contract-summary__metrics > div,
.pz-contract-summary__line {
  padding: 0.85rem 0.9rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(10, 10, 15, 0.08);
  display: grid;
  gap: 0.2rem;
}

.pz-contract-summary__metrics span,
.pz-contract-summary__line span,
.pz-contract-mini-summary span {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-summary__metrics strong,
.pz-contract-summary__line strong,
.pz-contract-mini-summary strong {
  font-family: var(--pz-font-display);
  font-size: 0.96rem;
  color: var(--pz-color-foundation-black);
}

.pz-contract-summary__stack {
  display: grid;
  gap: 0.65rem;
}

.pz-contract-summary__line {
  grid-template-columns: 1fr;
}

@media (max-width: 1180px) {
  .pz-contract-workspace {
    grid-template-columns: 1fr;
  }

  .pz-contract-summary {
    position: static;
  }
}

@media (max-width: 960px) {
  .pz-contract-posting__hero,
  .pz-contract-upload {
    grid-template-columns: 1fr;
  }

  .pz-contract-posting__hero-stats,
  .pz-contract-summary__metrics,
  .pz-contract-grid--two,
  .pz-contract-grid--three {
    grid-template-columns: 1fr;
  }

  .pz-contract-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .pz-contract-actions__group {
    width: 100%;
  }

  .pz-contract-actions__group .pz-button {
    flex: 1;
  }

  .pz-contract-posting__workflow {
    grid-template-columns: 1fr;
  }

  .pz-contract-posting__workflow-actions {
    justify-content: flex-start;
  }

  .pz-contract-posting__workflow-steps {
    grid-template-columns: 1fr;
  }
}
</style>
