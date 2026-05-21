<template>
  <div class="pz-project-list">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Project Portfolio"
      placeholder="Search by title, location, or owner"
      search-label="Search Projects"
    >
      <template #actions>
        <Button variant="primary" size="sm" @click="$router.push('/projects/new')">Start Project</Button>
      </template>
    </EntryHero>

    <div class="pz-l-container">
      <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
        <div class="pz-project-workflow-banner">
          <div class="pz-project-workflow-banner__summary">
            <div class="pz-project-workflow-banner__kicker">{{ workflowSummary.stage }}</div>
            <h2 class="pz-project-workflow-banner__title">{{ workflowSummary.title }}</h2>
            <p class="pz-project-workflow-banner__body">{{ workflowSummary.body }}</p>
          </div>
          <div class="pz-project-workflow-banner__actions">
            <Button v-if="workflowSummary.primaryAction" variant="primary" size="sm" @click="workflowSummary.primaryAction.handler">
              {{ workflowSummary.primaryAction.label }}
            </Button>
            <Button v-if="workflowSummary.secondaryAction" variant="outline" size="sm" @click="workflowSummary.secondaryAction.handler">
              {{ workflowSummary.secondaryAction.label }}
            </Button>
          </div>
        </div>
        <div class="pz-project-workflow-banner__steps">
          <div
            v-for="step in workflowSteps"
            :key="step.label"
            class="pz-project-workflow-step"
            :class="{ 'pz-project-workflow-step--done': step.done, 'pz-project-workflow-step--active': step.active }"
          >
            <div class="pz-project-workflow-step__index">{{ step.index }}</div>
            <div class="pz-project-workflow-step__content">
              <strong>{{ step.label }}</strong>
              <span>{{ step.help }}</span>
            </div>
          </div>
        </div>
      

      <ModuleCTA
        eyebrow="Build From Here"
        title="Have land, a brief, or materials ready for a new build?"
        body="Create a project workspace, connect it to property or procurement needs, and move from discovery into funded execution."
        primary-label="Start Project"
        primary-to="/projects/new"
        secondary-label="Post Tender"
        secondary-to="/contracts/new"
        tone="savanna"
      />
</WorkflowGuide>
    </div>

    <div class="pz-market-shell">
      <aside class="pz-market-sidebar u-hide-mobile">
        <div class="pz-filter-rail">
          <div class="pz-filter-rail__header">
            <div>
              <div class="pz-filter-rail__eyebrow">Filter Results</div>
              <h3 class="pz-filter-rail__title">Refine Projects</h3>
            </div>
            <Button v-if="activeFilterLabels.length" variant="ghost" size="sm" @click="clearFilters">Reset</Button>
          </div>

          <div class="pz-filter-section">
            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Country</span>
              <select v-model="selectedCountry" class="pz-filter-bar__control">
                <option value="">All countries</option>
                <option v-for="c in configStore.countries" :key="c.id" :value="c.iso_code">{{ c.flag_emoji }} {{ c.name }}</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Lifecycle</span>
              <select v-model="selectedStatus" class="pz-filter-bar__control">
                <option value="">All stages</option>
                <option value="LISTED">Planning</option>
                <option value="FUNDING_OPEN">Funding Open</option>
                <option value="EXECUTION_STARTED">Execution Started</option>
                <option value="COMPLETED">Completed</option>
              </select>
            </div>

            <div class="pz-filter-bar__item">
              <span class="pz-filter-bar__label">Budget Range</span>
              <div class="pz-filter-range">
                <input v-model="budgetMin" type="number" placeholder="Min" class="pz-filter-bar__input">
                <input v-model="budgetMax" type="number" placeholder="Max" class="pz-filter-bar__input">
              </div>
            </div>
          </div>
        </div>
      </aside>

      <section class="pz-market-results">
        <div class="pz-results-header">
          <div>
            <div class="pz-u-text-display text-lg">Project Discovery</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">
              {{ projects.length }} projects • {{ activeFilterLabels.length }} active filters • {{ countryLabel }}
            </div>
          </div>
          <div class="pz-results-header__actions">
            <div class="pz-view-switcher u-hide-mobile">
              <button
                class="pz-view-switcher__btn"
                :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                type="button"
              >
                ⣿
              </button>
              <button
                class="pz-view-switcher__btn"
                :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }"
                @click="viewMode = 'list'"
                type="button"
              >
                ≡
              </button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="pz-u-text-center u-py-20">
          <div class="pz-status-indicator pz-status-indicator--pulse"></div>
          <p class="pz-u-text-mono text-xs u-mt-4">Loading projects...</p>
        </div>

        <EmptyState
          v-else-if="!projects.length"
          icon="📁"
          title="No projects found"
          description="Projects appear here once a project shell has been created and shared into the workspace."
          next-step="Start a project with a title, location, and budget. If filters are hiding results, reset them to review the full portfolio."
          action-label="Reset Filters"
          action-variant="outline"
          @action="clearFilters"
        />

        <div v-else :class="viewMode === 'grid' ? 'pz-results-grid' : 'pz-results-list'">
          <article
            v-for="project in projects"
            :key="project.id"
            class="pz-project-card"
            @click="$router.push(`/projects/${project.id}`)"
          >
            <div class="pz-project-card__media">
              <img
                v-if="coverImageUrl(project)"
                :src="coverImageUrl(project)"
                :alt="project.title"
                class="pz-project-card__img"
                loading="lazy"
              />
              <div v-else class="pz-project-card__fallback">
                <span>{{ project.category_label || 'Construction' }}</span>
              </div>
              <div class="pz-project-card__badges">
                <span
                  class="pz-project-card__badge pz-project-card__badge--status"
                  :class="`pz-project-card__badge--${(project.status || 'listed').toLowerCase()}`"
                >
                  {{ statusLabel(project.status) }}
                </span>
                <span v-if="project.funding_required" class="pz-project-card__badge pz-project-card__badge--finance">
                  Funding Open
                </span>
              </div>
            </div>

            <div class="pz-project-card__body">
              <div class="pz-project-card__meta">
                <span class="pz-project-card__eyebrow">{{ project.category_label || 'Construction Project' }}</span>
              </div>
              <h3 class="pz-project-card__title">{{ project.title }}</h3>
              <div class="pz-project-card__location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>{{ getLocation(project) }}</span>
              </div>

              <div class="pz-project-card__specs">
                <div class="pz-project-card__spec">
                  <span class="pz-project-card__spec-label">Budget</span>
                  <strong>{{ formatBudget(project.estimated_budget, project.currency || project.country?.default_currency || 'KES') }}</strong>
                </div>
                <div class="pz-project-card__spec">
                  <span class="pz-project-card__spec-label">Requirements</span>
                  <strong>{{ (project.requirements || []).length }}</strong>
                </div>
                <div class="pz-project-card__spec">
                  <span class="pz-project-card__spec-label">Updates</span>
                  <strong>{{ (project.updates || []).length }}</strong>
                </div>
              </div>

              <div class="pz-project-card__progress">
                <div class="pz-project-card__progress-head">
                  <span>Execution Progress</span>
                  <strong>{{ projectProgress(project) }}%</strong>
                </div>
                <div class="pz-project-card__bar">
                  <div class="pz-project-card__bar-fill" :style="{ width: `${projectProgress(project)}%` }"></div>
                </div>
              </div>

              <div class="pz-project-card__footer">
                <div class="pz-project-card__owner">
                  <div class="pz-project-card__owner-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </div>
                  <span>{{ project.owner_username || 'Project Owner' }}</span>
                </div>
                <Button variant="outline" size="sm" @click.stop="$router.push(`/projects/${project.id}`)">
                  View Project
                </Button>
              </div>
            </div>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import ProjectsService from '../services/projects';
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import EntryHero from '../components/ui/EntryHero.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import { useConfigStore } from '../stores/config';

const router = useRouter();
const configStore = useConfigStore();
const projects = ref([]);
const loading = ref(true);
const viewMode = ref('grid');
const searchQuery = ref('');
const selectedCountry = ref('');
const selectedStatus = ref('');
const budgetMin = ref('');
const budgetMax = ref('');
const countryLabel = computed(() => {
  if (selectedCountry.value) {
    const c = configStore.countries.find(x => String(x.iso_code).toUpperCase() === String(selectedCountry.value).toUpperCase());
    return c?.name || selectedCountry.value;
  }
  return 'All countries';
});
const hasProjects = computed(() => projects.value.length > 0);

const statusLabels = {
  LISTED: 'Planning',
  FUNDING_OPEN: 'Funding Open',
  EXECUTION_STARTED: 'Execution Started',
  COMPLETED: 'Completed'
};

function statusLabel(status) {
  return statusLabels[status] || status || 'Unknown';
}

function statusTone(status) {
  if (status === 'COMPLETED') return 'success';
  if (status === 'EXECUTION_STARTED') return 'earth';
  if (status === 'FUNDING_OPEN') return 'finance';
  return 'default';
}

function getLocation(project) {
  return project.formatted_address || project.location_text || project.location || 'Location pending';
}

function formatBudget(amount, sourceCurrency = 'KES') {
  const value = Number(amount || 0);
  return configStore.formatPrice(value, sourceCurrency);
}

function projectProgress(project) {
  const map = {
    LISTED: 15,
    FUNDING_OPEN: 35,
    EXECUTION_STARTED: 70,
    COMPLETED: 100
  };
  return map[project.status] || 0;
}

function coverImageUrl(project) {
  if (!project.cover_photo) return null;
  const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/api\/?$/, '');
  return `${base}/media/${project.cover_photo}`;
}

const workflowSummary = computed(() => {
  const hasProjects = projects.value.length > 0;
  const hasFilters = activeFilterLabels.value.length > 0;

  if (loading.value) {
    return {
      stage: 'LOADING',
      title: 'Preparing the project workspace',
      body: 'Loading projects and portfolio filters so you can move directly to the right record.',
      primaryAction: null,
      secondaryAction: null,
    };
  }

  if (!hasProjects) {
    return {
      stage: 'EMPTY',
      title: 'Start the first project shell',
      body: 'Create a project when a property moves into execution. The shell lets you add requirements, funding, contracts, and updates in one place.',
      primaryAction: { label: 'Start Project', handler: () => router.push('/projects/new') },
      secondaryAction: hasFilters ? { label: 'Reset Filters', handler: clearFilters } : null,
    };
  }

  if (selectedStatus.value === 'FUNDING_OPEN') {
    return {
      stage: 'FUNDING',
      title: 'Review funding-ready projects first',
      body: 'Projects in funding-open state need commitments, clear progress updates, and an active next step.',
      primaryAction: {
        label: 'Open Funding',
        handler: () => {
          const first = projects.value.find((project) => project.status === 'FUNDING_OPEN');
          if (first) router.push(`/projects/${first.id}`);
        },
      },
      secondaryAction: { label: 'Create Project', handler: () => router.push('/projects/new') },
    };
  }

  return {
    stage: 'DISCOVERY',
    title: 'Find the next project to advance',
    body: 'Use search and filters to move from planning to execution. Open a project to add requirements, contracts, milestones, or updates.',
    primaryAction: { label: 'Start Project', handler: () => router.push('/projects/new') },
    secondaryAction: hasProjects.value ? { label: 'Open First Project', handler: () => router.push(`/projects/${projects.value[0].id}`) } : null,
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Start the shell',
    help: 'Create the project record with title, location, and budget.',
    done: hasProjects.value,
    active: !hasProjects.value,
  },
  {
    index: '02',
    label: 'Add requirements',
    help: 'Define materials, contractor work, and other procurement needs.',
    done: projects.value.some((project) => (project.requirements || []).length > 0),
    active: selectedStatus.value === 'LISTED',
  },
  {
    index: '03',
    label: 'Open funding or contracts',
    help: 'Move the project into execution with funding, awards, or milestones.',
    done: projects.value.some((project) => ['FUNDING_OPEN', 'EXECUTION_STARTED', 'COMPLETED'].includes(project.status)),
    active: selectedStatus.value === 'FUNDING_OPEN' || selectedStatus.value === 'EXECUTION_STARTED',
  },
  {
    index: '04',
    label: 'Track progress',
    help: 'Use the detail workspace for updates, activity, and issue visibility.',
    done: projects.value.some((project) => (project.updates || []).length > 0),
    active: viewMode.value === 'list',
  },
]);

async function fetchProjects() {
  loading.value = true;
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    params.country = selectedCountry.value || '';
    if (selectedStatus.value) params.status = selectedStatus.value;
    if (budgetMin.value !== '') params.budget_min = budgetMin.value;
    if (budgetMax.value !== '') params.budget_max = budgetMax.value;
    console.log('[ProjectList] fetching with params:', JSON.stringify(params));
    const res = await ProjectsService.list(params);
    console.log('[ProjectList] received', (res.data.results || res.data || []).length, 'projects');
    projects.value = res.data.results || res.data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
}

const activeFilterLabels = computed(() => {
  const labels = [];
  if (selectedCountry.value) labels.push(countryLabel.value);
  if (selectedStatus.value) labels.push(statusLabel(selectedStatus.value));
  if (searchQuery.value) labels.push(`Search: ${searchQuery.value}`);
  if (budgetMin.value !== '') labels.push(`Min ${budgetMin.value}`);
  if (budgetMax.value !== '') labels.push(`Max ${budgetMax.value}`);
  return labels;
});

function clearFilters() {
  searchQuery.value = '';
  selectedCountry.value = '';
  selectedStatus.value = '';
  budgetMin.value = '';
  budgetMax.value = '';
  fetchProjects();
}

// Debounced search
let searchTimeout;
watch(searchQuery, () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(fetchProjects, 300);
});

// Immediate filter watchers
watch([selectedCountry, selectedStatus, budgetMin, budgetMax], fetchProjects, { immediate: false });

onMounted(async () => {
  if (!configStore.countries.length) {
    await configStore.fetchConfig();
  }
  fetchProjects();
});

watch(
  () => configStore.activeCountryCode,
  (newCode) => {
    selectedCountry.value = newCode || '';
    fetchProjects();
  }
);
</script>

<style scoped>
.pz-project-list {
  background-color: var(--pz-color-limestone-white);
  min-height: 100vh;
}

.pz-market-shell {
  display: grid;
  gap: 2rem;
  grid-template-columns: minmax(17rem, 21rem) minmax(0, 1fr);
  width: 100%;
  margin: 2rem 0 0;
  padding: 0 clamp(1rem, 2vw, 2rem) 4rem;
}

.pz-project-workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.pz-project-workflow-banner__summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.pz-project-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-project-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.pz-project-workflow-banner__body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.pz-project-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.pz-project-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.pz-project-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.pz-project-workflow-step__index {
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

.pz-project-workflow-step__content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.pz-project-workflow-step__content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.pz-project-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pz-project-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.pz-project-workflow-step--done .pz-project-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.pz-project-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-market-sidebar {
  position: sticky;
  top: 1rem;
  align-self: start;
}

.pz-filter-rail {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(12px);
  border-radius: 20px;
}

.pz-filter-rail__header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: start;
}

.pz-filter-rail__eyebrow,
.pz-filter-bar__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-filter-rail__title {
  margin: 0.25rem 0 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
}

.pz-filter-section {
  display: grid;
  gap: 0.9rem;
}

.pz-filter-bar__item {
  display: grid;
  gap: 0.45rem;
}

.pz-filter-bar__control,
.pz-filter-bar__input {
  min-height: 2.85rem;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: white;
  padding: 0 0.85rem;
  width: 100%;
  border-radius: 10px;
  font-size: 0.9rem;
  color: var(--pz-color-foundation-black);
}

.pz-filter-range {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pz-market-results {
  display: grid;
  gap: 1.5rem;
}

.pz-results-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  padding: 0.25rem 0;
}

.pz-results-header__actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pz-view-switcher {
  display: inline-flex;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 999px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.8);
}

.pz-view-switcher__btn {
  padding: 0.55rem 0.9rem;
  border: 0;
  background: transparent;
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
  color: var(--pz-color-structural-steel);
  cursor: pointer;
  transition: all 0.2s ease;
}

.pz-view-switcher__btn--active {
  background: var(--pz-color-foundation-black);
  color: #fff;
}

.pz-results-grid {
  display: grid;
  gap: 1.75rem;
  grid-template-columns: repeat(auto-fill, minmax(22rem, 1fr));
}

.pz-results-list {
  display: grid;
  gap: 1rem;
}

.pz-results-list .pz-project-card {
  flex-direction: row;
}

.pz-results-list .pz-project-card__media {
  width: 280px;
  min-height: 100%;
}

@media (max-width: 768px) {
  .pz-results-list .pz-project-card {
    flex-direction: column;
  }
  .pz-results-list .pz-project-card__media {
    width: 100%;
  }
}

/* Project Card */
.pz-project-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  border: 1px solid rgba(10, 10, 15, 0.06);
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 4px 12px rgba(10, 10, 15, 0.04);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.pz-project-card:hover {
  transform: translateY(-6px);
  box-shadow:
    0 8px 24px rgba(10, 10, 15, 0.06),
    0 24px 48px rgba(10, 10, 15, 0.08);
}

.pz-project-card:hover .pz-project-card__img {
  transform: scale(1.05);
}

/* Media */
.pz-project-card__media {
  position: relative;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background: linear-gradient(135deg, #e8e4db, #d4cfc5);
}

.pz-project-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.pz-project-card__fallback {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #2a2825, #5b5148);
  color: white;
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

/* Badges */
.pz-project-card__badges {
  position: absolute;
  top: 0.85rem;
  left: 0.85rem;
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.pz-project-card__badge {
  padding: 0.35rem 0.65rem;
  border-radius: 8px;
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.pz-project-card__badge--status {
  background: rgba(10, 10, 15, 0.75);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.pz-project-card__badge--listed { background: rgba(10, 10, 15, 0.75); }
.pz-project-card__badge--funding_open { background: rgba(212, 101, 42, 0.9); }
.pz-project-card__badge--execution_started { background: rgba(37, 99, 235, 0.9); }
.pz-project-card__badge--completed { background: rgba(16, 185, 129, 0.9); }

.pz-project-card__badge--finance {
  background: rgba(255, 255, 255, 0.92);
  color: var(--pz-color-foundation-black);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

/* Body */
.pz-project-card__body {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}

.pz-project-card__meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pz-project-card__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

.pz-project-card__title {
  font-family: var(--pz-font-display);
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--pz-color-foundation-black);
  margin: 0;
  letter-spacing: -0.01em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pz-project-card__location {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--pz-color-concrete-grey);
  font-size: 0.88rem;
  line-height: 1.4;
}

.pz-project-card__location svg {
  width: 0.9rem;
  height: 0.9rem;
  flex-shrink: 0;
  color: var(--pz-color-earth-orange);
}

/* Specs */
.pz-project-card__specs {
  display: flex;
  gap: 1.25rem;
  padding: 0.6rem 0;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
  margin-top: 0.2rem;
}

.pz-project-card__spec {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.pz-project-card__spec-label {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-project-card__spec strong {
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

/* Progress */
.pz-project-card__progress {
  margin-top: 0.2rem;
}

.pz-project-card__progress-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.45rem;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-project-card__bar {
  height: 0.45rem;
  border-radius: 999px;
  background: rgba(10, 10, 15, 0.08);
  overflow: hidden;
}

.pz-project-card__bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--pz-color-earth-orange), var(--pz-color-savanna-green));
}

/* Footer */
.pz-project-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 0.75rem;
}

.pz-project-card__owner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.pz-project-card__owner-avatar {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: rgba(10, 10, 15, 0.06);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.pz-project-card__owner-avatar svg {
  width: 0.9rem;
  height: 0.9rem;
  color: var(--pz-color-concrete-grey);
}

.pz-project-card__owner span {
  font-size: 0.85rem;
  color: var(--pz-color-structural-steel);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Empty State */
.pz-empty-state {
  display: grid;
  gap: 0.85rem;
  place-items: center;
  padding: 4rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  text-align: center;
  border-radius: 20px;
}

/* Utilities */
.pz-u-text-center {
  text-align: center;
}

.u-py-20 {
  padding-top: 5rem;
  padding-bottom: 5rem;
}

.u-mt-4 {
  margin-top: 1rem;
}

.pz-status-indicator {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 2px solid rgba(10, 10, 15, 0.08);
  border-top-color: var(--pz-color-earth-orange);
  margin: 0 auto;
}

.pz-status-indicator--pulse {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .pz-market-shell {
    grid-template-columns: 1fr;
  }
  .pz-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  }

  .pz-project-workflow-banner {
    grid-template-columns: 1fr;
  }

  .pz-project-workflow-banner__actions {
    justify-content: flex-start;
  }

  .pz-project-workflow-banner__steps {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .pz-results-header,
  .pz-results-header__actions {
    flex-direction: column;
    align-items: stretch;
  }
  .pz-results-grid {
    grid-template-columns: 1fr;
  }
}
</style>
