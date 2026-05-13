<template>
  <div class="pz-project-page">
    <div class="pz-l-container u-py-8">
      <div v-if="loading" class="pz-u-text-center u-py-20">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">Loading project workspace...</p>
      </div>

      <div v-else-if="project" class="pz-space-y-8">
        <!-- Breadcrumb -->
        <nav class="pz-breadcrumb pz-u-text-mono text-xs">
          <router-link to="/projects" class="pz-breadcrumb__item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
            Projects
          </router-link>
          <span class="pz-breadcrumb__separator">/</span>
          <span class="pz-breadcrumb__current pz-u-color-steel">{{ project.title }}</span>
        </nav>

        <!-- Hero -->
        <section class="pz-project-hero">
          <div class="pz-project-hero__media">
            <img
              v-if="coverImageUrl"
              :src="coverImageUrl"
              :alt="project.title"
              class="pz-project-hero__image"
            />
            <div v-else class="pz-project-hero__fallback">
              <span class="pz-u-text-mono text-xs">PROJECT</span>
              <strong>{{ project.category_label || 'Construction' }}</strong>
            </div>
          </div>

          <div class="pz-project-hero__content">
            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start pz-l-flex--gap-4 pz-l-flex--wrap">
              <div class="pz-space-y-3">
                <div class="pz-u-text-mono text-xs pz-u-color-earth">{{ project.category_label || 'Construction Project' }}</div>
                <h1 class="pz-u-text-display">{{ project.title }}</h1>
                <p class="pz-u-text-mono text-sm pz-u-color-steel pz-project-hero__description">{{ project.description }}</p>
              </div>
              <div class="pz-l-flex pz-l-flex--gap-2 pz-l-flex--wrap">
                <Badge :variant="statusTone(project.status)">{{ statusLabel(project.status) }}</Badge>
                <Badge v-if="project.funding_required" variant="finance">Funding Open</Badge>
              </div>
            </div>

            <div class="pz-project-hero__price">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Estimated Budget</span>
              <strong>{{ budgetDisplay }}</strong>
              <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ projectLocation }}</span>
            </div>

            <div v-if="summaryStats.length" class="pz-project-summary-grid">
              <div v-for="stat in summaryStats" :key="stat.label" class="pz-project-detail__metric">
                <span class="pz-metric__icon" :class="'pz-metric__icon--' + metricColor(stat.icon)" v-html="metricIcon(stat.icon)"></span>
                <div class="pz-metric__content">
                  <span class="pz-project-detail__label">{{ stat.label }}</span>
                  <span class="pz-project-detail__value">{{ stat.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Layout -->
        <div class="pz-project-layout">
          <section class="pz-space-y-6">
            <!-- Tabs -->
            <div class="pz-project-tabs">
              <button
                v-for="section in sections"
                :key="section.id"
                type="button"
                class="pz-project-tab"
                :class="{ 'pz-project-tab--active': activeSection === section.id }"
                @click="activeSection = section.id"
              >
                <span class="pz-project-tab__label">{{ section.label }}</span>
                <span v-if="section.count" class="pz-project-tab__badge">{{ section.count }}</span>
              </button>
            </div>

            <!-- Overview -->
            <div v-show="activeSection === 'overview'" class="pz-tab-panel pz-space-y-6">
              <Card title="Project Overview" variant="premium" eyebrow="Status">
                <div class="project-overview__grid">
                  <div>
                    <p class="project-overview__label">Execution state</p>
                    <p class="project-overview__value">{{ statusLabel(project.status) }}</p>
                  </div>
                  <div>
                    <p class="project-overview__label">Created</p>
                    <p class="project-overview__value">{{ formatDate(project.created_at) }}</p>
                  </div>
                  <div>
                    <p class="project-overview__label">Funding intent</p>
                    <p class="project-overview__value">{{ project.funding_required ? 'Seeking capital' : 'Owner funded' }}</p>
                  </div>
                  <div>
                    <p class="project-overview__label">Progress</p>
                    <p class="project-overview__value">{{ progressPercent }}%</p>
                  </div>
                </div>

                <div class="project-health">
                  <div class="project-health__item" v-for="item in healthSignals" :key="item.label">
                    <span class="project-health__label">{{ item.label }}</span>
                    <strong class="project-health__value">{{ item.value }}</strong>
                  </div>
                </div>

                <p class="project-overview__body">{{ project.description }}</p>
              </Card>
            </div>

            <!-- Requirements -->
            <div v-show="activeSection === 'requirements'" class="pz-tab-panel pz-space-y-6">
              <Card title="Requirements" variant="premium" eyebrow="Procurement">
                <div v-if="project.requirements && project.requirements.length" class="project-grid-list">
                  <div v-for="req in project.requirements" :key="req.id" class="project-item">
                    <div class="project-item__head">
                      <Badge :variant="requirementTone(req.type)" size="sm">{{ req.type }}</Badge>
                      <div style="display:flex;gap:0.5rem;align-items:center;">
                        <span class="project-item__meta">{{ req.quantity }}</span>
                        <button v-if="isOwner" class="project-item__remove" @click.stop="removeRequirement(req.id)">Remove</button>
                      </div>
                    </div>
                    <p class="project-item__title">{{ req.description }}</p>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No requirements have been added yet.</p>
                  <p v-if="isOwner">Add the first requirement to define procurement demand.</p>
                </div>

                <div v-if="isOwner" class="project-form">
                  <PzInput v-model="newReq.description" label="Requirement description" placeholder="e.g. 500 bags of cement" />
                  <div class="project-form__row">
                    <div class="pz-input-wrapper">
                      <label class="pz-input__label">Type</label>
                      <select v-model="newReq.type" class="pz-input">
                        <option value="MATERIAL">Material</option>
                        <option value="CONTRACTOR">Contractor</option>
                        <option value="SERVICE">Service</option>
                      </select>
                    </div>
                    <PzInput v-model="newReq.quantity" label="Quantity" placeholder="e.g. 500 bags" />
                  </div>
                  <Button variant="primary" @click="addRequirement">Add requirement</Button>
                </div>
              </Card>
            </div>

            <!-- Contracts -->
            <div v-show="activeSection === 'contracts'" class="pz-tab-panel pz-space-y-6">
              <Card title="Linked Contracts" variant="premium" eyebrow="Procurement">
                <div v-if="project.linked_contracts && project.linked_contracts.length" class="project-grid-list">
                  <div v-for="link in project.linked_contracts" :key="link.id" class="project-item">
                    <div class="project-item__head">
                      <Badge :variant="contractTone(link.contract.status)" size="sm">{{ contractStatus(link.contract.status) }}</Badge>
                      <span class="project-item__meta">{{ link.contract.location }}</span>
                    </div>
                    <p class="project-item__title">{{ link.contract.title }}</p>
                    <p class="project-item__body">
                      {{ formatBudget(link.contract.budget_min) }} to {{ formatBudget(link.contract.budget_max) }}
                    </p>
                    <div class="project-item__footer">
                      <router-link :to="`/contracts/${link.contract.id}`" class="project-item__link">Open contract</router-link>
                      <div style="display:flex;gap:0.5rem;align-items:center;">
                        <span class="project-item__meta">{{ (link.contract.milestones || []).length }} milestones</span>
                        <button v-if="isOwner" class="project-item__remove" @click.stop="unlinkContract(link.id)">Unlink</button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No contracts linked yet.</p>
                </div>

                <div v-if="isOwner" class="project-form project-form--stacked">
                  <PzInput v-model="contractIdToLink" label="Link contract by ID" placeholder="e.g. 12" />
                  <Button variant="outline" @click="linkContract">Link contract</Button>
                </div>
              </Card>
            </div>

            <!-- Milestones -->
            <div v-show="activeSection === 'milestones'" class="pz-tab-panel pz-space-y-6">
              <Card title="Milestones" variant="premium" eyebrow="Execution">
                <div v-if="milestoneItems.length" class="project-grid-list">
                  <div v-for="milestone in milestoneItems" :key="`${milestone.contractId}-${milestone.id}`" class="project-item">
                    <div class="project-item__head">
                      <Badge :variant="milestoneTone(milestone.status)" size="sm">{{ milestone.status }}</Badge>
                      <span class="project-item__meta">{{ milestone.contractTitle }}</span>
                    </div>
                    <p class="project-item__title">{{ milestone.title }}</p>
                    <p class="project-item__body">{{ milestone.description || 'No description provided.' }}</p>
                    <div class="project-item__footer">
                      <span class="project-item__meta">{{ formatBudget(milestone.amount) }}</span>
                      <span class="project-item__meta">{{ formatDate(milestone.due_date) }}</span>
                    </div>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No milestones are linked to awarded contracts yet.</p>
                  <p>Milestones are defined on the awarded contract and appear here once linked.</p>
                </div>

                <div v-if="isOwner" class="project-form project-form--stacked">
                  <div class="project-form__row">
                    <div class="pz-input-wrapper">
                      <label class="pz-input__label">Contract</label>
                      <select v-model="milestoneForm.contract_id" class="pz-input" :disabled="!linkedContracts.length">
                        <option disabled value="">Select contract</option>
                        <option v-for="contract in linkedContracts" :key="contract.id" :value="contract.id">
                          {{ contract.title }}
                        </option>
                      </select>
                    </div>
                    <PzInput v-model="milestoneForm.title" label="Milestone title" placeholder="e.g. Foundation works" />
                  </div>
                  <PzInput
                    v-model="milestoneForm.description"
                    label="Description"
                    type="textarea"
                    rows="3"
                    placeholder="Describe what must be completed before this milestone can be approved."
                  />
                  <div class="project-form__row">
                    <PzInput v-model="milestoneForm.amount" label="Amount" type="number" min="0" />
                    <PzInput v-model="milestoneForm.due_date" label="Due date" type="date" />
                  </div>
                  <Button variant="primary" :disabled="!linkedContracts.length" @click="createMilestone">
                    Add milestone
                  </Button>
                </div>
              </Card>
            </div>

            <!-- Funding -->
            <div v-show="activeSection === 'funding'" class="pz-tab-panel pz-space-y-6">
              <Card title="Funding" variant="premium" eyebrow="Investment">
                <div class="project-funding">
                  <div class="project-funding__row">
                    <span>Committed</span>
                    <strong>{{ committedDisplay }}</strong>
                  </div>
                  <div class="project-funding__row">
                    <span>Target</span>
                    <strong>{{ budgetDisplay }}</strong>
                  </div>
                  <div class="project-funding__bar">
                    <div class="project-funding__bar-fill" :style="{ width: `${fundingProgress}%` }"></div>
                  </div>
                  <p class="project-funding__note">
                    {{ project.funding_required ? 'This project can accept pledges while funding is open.' : 'This project is not marked as funding-ready.' }}
                  </p>
                </div>

                <div v-if="project.commitments && project.commitments.length" class="project-grid-list">
                  <div v-for="commitment in project.commitments" :key="commitment.id" class="project-item">
                    <div class="project-item__head">
                      <Badge :variant="commitment.status === 'CONFIRMED' ? 'success' : 'finance'" size="sm">
                        {{ commitment.status }}
                      </Badge>
                      <span class="project-item__meta">{{ formatDate(commitment.created_at) }}</span>
                    </div>
                    <p class="project-item__title">{{ formatBudget(commitment.amount_committed) }}</p>
                    <p class="project-item__body">{{ commitment.investor }}</p>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No capital has been committed yet.</p>
                </div>

                <div v-if="canPledge" class="project-form project-form--stacked">
                  <PzInput
                    v-model="pledgeAmount"
                    :label="`Commitment amount (${configStore.activeCurrency?.currency_code || 'KES'})`"
                    type="number"
                    min="0"
                  />
                  <Button variant="primary" @click="pledge">Commit capital</Button>
                </div>
              </Card>
            </div>

            <!-- Documents -->
            <div v-show="activeSection === 'documents'" class="pz-tab-panel pz-space-y-6">
              <Card title="Documents" variant="premium" eyebrow="Files">
                <div v-if="attachmentItems.length" class="project-grid-list">
                  <div v-for="item in attachmentItems" :key="`${item.contractId}-${item.id}`" class="project-item">
                    <div class="project-item__head">
                      <Badge variant="default" size="sm">{{ item.typeLabel }}</Badge>
                      <span class="project-item__meta">{{ item.contractTitle }}</span>
                    </div>
                    <p class="project-item__title">{{ item.title }}</p>
                    <a :href="item.fileUrl" target="_blank" rel="noreferrer" class="project-item__link">Open file</a>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No documents or attachments have been uploaded yet.</p>
                  <p>Use contract attachments for drawings, reports, specifications, or site photos.</p>
                </div>
              </Card>
            </div>

            <!-- Updates -->
            <div v-show="activeSection === 'updates'" class="pz-tab-panel pz-space-y-6">
              <Card title="Updates" variant="premium" eyebrow="Activity">
                <div v-if="project.updates && project.updates.length" class="project-timeline">
                  <div v-for="upd in project.updates" :key="upd.id" class="project-timeline__item">
                    <div class="project-timeline__node"></div>
                    <div class="project-timeline__content">
                      <div class="project-timeline__meta">
                        <strong>{{ upd.posted_by }}</strong>
                        <div style="display:flex;gap:0.5rem;align-items:center;">
                          <span>{{ formatDateTime(upd.created_at) }}</span>
                          <button v-if="isOwner" class="project-item__remove" @click.stop="removeUpdate(upd.id)">Remove</button>
                        </div>
                      </div>
                      <p>{{ upd.update_text }}</p>
                    </div>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No updates have been published yet.</p>
                </div>

                <div v-if="isOwner" class="project-form project-form--stacked">
                  <PzInput
                    v-model="updateText"
                    label="Publish an update"
                    type="textarea"
                    rows="4"
                    placeholder="Share site progress, approvals, delays, or milestones."
                  />
                  <Button variant="primary" @click="postUpdate">Post update</Button>
                </div>
              </Card>
            </div>

            <!-- Risks -->
            <div v-show="activeSection === 'risks'" class="pz-tab-panel pz-space-y-6">
              <Card title="Risk Assessment" variant="premium" eyebrow="Health">
                <div class="project-grid-list">
                  <div v-for="risk in riskItems" :key="risk.label" class="project-item">
                    <div class="project-item__head">
                      <Badge :variant="risk.variant" size="sm">{{ risk.level }}</Badge>
                      <span class="project-item__meta">RISK</span>
                    </div>
                    <p class="project-item__title">{{ risk.label }}</p>
                    <p class="project-item__body">{{ risk.body }}</p>
                  </div>
                </div>
              </Card>
            </div>

            <!-- Activity -->
            <div v-show="activeSection === 'activity'" class="pz-tab-panel pz-space-y-6">
              <Card title="Activity Feed" variant="premium" eyebrow="History">
                <div v-if="activityItems.length" class="project-timeline">
                  <div v-for="item in activityItems" :key="item.id" class="project-timeline__item">
                    <div class="project-timeline__node" :class="`project-timeline__node--${item.variant}`"></div>
                    <div class="project-timeline__content">
                      <div class="project-timeline__meta">
                        <strong>{{ item.title }}</strong>
                        <span>{{ item.time }}</span>
                      </div>
                      <p>{{ item.body }}</p>
                    </div>
                  </div>
                </div>
                <div v-else class="project-empty-state">
                  <p>No activity recorded yet.</p>
                </div>
              </Card>
            </div>
          </section>

          <!-- Sidebar -->
          <aside class="pz-project-sidebar">
            <Card title="Project Summary" variant="elevated">
              <div class="project-summary">
                <div class="project-summary__row">
                  <span>Status</span>
                  <Badge :variant="statusTone(project.status)" size="sm">{{ statusLabel(project.status) }}</Badge>
                </div>
                <div class="project-summary__row">
                  <span>Budget</span>
                  <strong>{{ budgetDisplay }}</strong>
                </div>
                <div class="project-summary__row">
                  <span>Funding</span>
                  <strong>{{ committedDisplay }}</strong>
                </div>
                <div class="project-summary__row">
                  <span>Linked contracts</span>
                  <strong>{{ linkedContracts.length }}</strong>
                </div>
                <div class="project-summary__row">
                  <span>Active milestones</span>
                  <strong>{{ milestoneItems.length }}</strong>
                </div>
              </div>

              <div class="project-funding project-funding--compact">
                <div class="project-funding__bar">
                  <div class="project-funding__bar-fill" :style="{ width: `${fundingProgress}%` }"></div>
                </div>
                <p class="project-funding__note">{{ fundingProgress }}% of target committed.</p>
              </div>
            </Card>

            <Card title="Quick Actions" variant="glass">
              <div class="project-quick-actions">
                <Button variant="ghost" fullWidth @click="activeSection = 'requirements'">Manage requirements</Button>
                <Button variant="ghost" fullWidth @click="activeSection = 'contracts'">Review contracts</Button>
                <Button variant="ghost" fullWidth @click="activeSection = 'funding'">View funding</Button>
                <Button variant="ghost" fullWidth @click="activeSection = 'activity'">View activity</Button>
              </div>
            </Card>

            <Card v-if="project.funding_required && canPledge" title="Invest" variant="accent">
              <div class="project-form project-form--stacked" style="border-top:none;padding-top:0;">
                <PzInput
                  v-model="pledgeAmount"
                  :label="`Amount (${configStore.activeCurrency?.currency_code || 'KES'})`"
                  type="number"
                  min="0"
                />
                <Button variant="primary" @click="pledge">Pledge capital</Button>
              </div>
            </Card>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';
import ProjectsService from '../services/projects';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import PzInput from '../components/PzInput.vue';

const route = useRoute();
const authStore = useAuthStore();
const configStore = useConfigStore();
const showAlert = inject('showAlert');

const project = ref(null);
const loading = ref(true);
const activeSection = ref('overview');
const financeProducts = ref([]);

const newReq = ref({ type: 'MATERIAL', description: '', quantity: '' });
const pledgeAmount = ref('');
const contractIdToLink = ref('');
const updateText = ref('');
const milestoneForm = ref({ contract_id: '', title: '', description: '', amount: '', due_date: '' });
const financeForm = ref({
  product: '',
  requested_amount: '',
  purpose_category: 'COMPLETION',
  purpose: ''
});

const statusLabels = {
  LISTED: 'Planning',
  FUNDING_OPEN: 'Funding Open',
  EXECUTION_STARTED: 'Execution Started',
  COMPLETED: 'Completed'
};

const contractStatusLabels = {
  PENDING: 'Draft',
  POSTED: 'Posted',
  BIDDING: 'Bidding',
  AWARDED: 'Awarded',
  IN_PROGRESS: 'In Progress',
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

function contractStatus(status) {
  return contractStatusLabels[status] || status || 'Unknown';
}

function contractTone(status) {
  if (status === 'AWARDED' || status === 'COMPLETED') return 'success';
  if (status === 'IN_PROGRESS') return 'earth';
  if (status === 'POSTED' || status === 'BIDDING') return 'finance';
  return 'default';
}

function requirementTone(type) {
  if (type === 'MATERIAL') return 'finance';
  if (type === 'CONTRACTOR') return 'earth';
  return 'default';
}

function milestoneTone(status) {
  if (status === 'PAID') return 'success';
  if (status === 'APPROVED') return 'earth';
  if (status === 'COMPLETED') return 'finance';
  return 'default';
}

function formatDate(value) {
  if (!value) return 'Pending';
  return new Date(value).toLocaleDateString();
}

function formatDateTime(value) {
  if (!value) return 'Pending';
  return new Date(value).toLocaleString();
}

function getProjectCurrency() {
  return project.value?.currency || project.value?.country?.default_currency || 'KES';
}

function formatBudget(value, sourceCurrency = getProjectCurrency()) {
  return configStore.formatPrice(Number(value || 0), sourceCurrency);
}

function metricIcon(type) {
  const icons = {
    budget: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>',
    requirements: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    contracts: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    funding: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    milestones: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    updates: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  };
  return icons[type] || icons.budget;
}

function metricColor(type) {
  const colors = {
    budget: 'earth',
    requirements: 'steel',
    contracts: 'copper',
    funding: 'finance',
    milestones: 'violet',
    updates: 'green',
  };
  return colors[type] || 'earth';
}

const coverImageUrl = computed(() => {
  if (!project.value?.cover_photo) return null;
  const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/api\/?$/, '');
  return `${base}/media/${project.value.cover_photo}`;
});

const ownerId = computed(() => project.value?.owner?.id ?? project.value?.owner);
const isOwner = computed(() => {
  if (!project.value || !authStore.user) return false;
  return authStore.isAdmin || authStore.user.id === ownerId.value;
});

const projectLocation = computed(() => {
  if (!project.value) return 'Location pending';
  return project.value.formatted_address || project.value.location_text || project.value.location || 'Location pending';
});

const budgetDisplay = computed(() => formatBudget(project.value?.estimated_budget, getProjectCurrency()));

const linkedContracts = computed(() => {
  return (project.value?.linked_contracts || [])
    .map((link) => link.contract)
    .filter(Boolean);
});

const requirementCount = computed(() => project.value?.requirements?.length || 0);
const totalCommitted = computed(() => {
  return (project.value?.commitments || []).reduce((sum, item) => sum + Number(item.amount_committed || 0), 0);
});

const committedDisplay = computed(() => formatBudget(totalCommitted.value, getProjectCurrency()));

const fundingProgress = computed(() => {
  const budget = Number(project.value?.estimated_budget || 0);
  if (!budget) return 0;
  return Math.min(100, Math.round((totalCommitted.value / budget) * 100));
});

const progressPercent = computed(() => {
  const map = {
    LISTED: 15,
    FUNDING_OPEN: 40,
    EXECUTION_STARTED: 75,
    COMPLETED: 100
  };
  return map[project.value?.status] || 0;
});

const milestoneItems = computed(() => {
  return linkedContracts.value.flatMap((contract) =>
    (contract.milestones || []).map((milestone) => ({
      ...milestone,
      contractId: contract.id,
      contractTitle: contract.title
    }))
  );
});

const attachmentItems = computed(() => {
  return linkedContracts.value.flatMap((contract) =>
    (contract.attachments || []).map((attachment) => ({
      ...attachment,
      contractId: contract.id,
      contractTitle: contract.title,
      fileUrl: attachment.file_url || attachment.file,
      typeLabel: attachment.attachment_type_label || attachment.attachment_type
    }))
  );
});

const sections = computed(() => [
  { id: 'overview', label: 'Overview', count: null },
  { id: 'requirements', label: 'Requirements', count: requirementCount.value },
  { id: 'contracts', label: 'Contracts', count: linkedContracts.value.length },
  { id: 'milestones', label: 'Milestones', count: milestoneItems.value.length },
  { id: 'funding', label: 'Funding', count: project.value?.commitments?.length || 0 },
  { id: 'documents', label: 'Documents', count: attachmentItems.value.length },
  { id: 'updates', label: 'Updates', count: project.value?.updates?.length || 0 },
  { id: 'risks', label: 'Risks', count: riskItems.value.length },
  { id: 'activity', label: 'Activity', count: activityItems.value.length }
]);

const activeSectionLabel = computed(() => {
  const current = sections.value.find((section) => section.id === activeSection.value);
  return current?.label || 'Summary';
});

const canPledge = computed(() => {
  return project.value?.funding_required && project.value?.status === 'FUNDING_OPEN' && !isOwner.value;
});

const summaryStats = computed(() => [
  { label: 'Budget', value: budgetDisplay.value, icon: 'budget' },
  { label: 'Requirements', value: requirementCount.value, icon: 'requirements' },
  { label: 'Contracts', value: linkedContracts.value.length, icon: 'contracts' },
  { label: 'Funding', value: committedDisplay.value, icon: 'funding' },
  { label: 'Milestones', value: milestoneItems.value.length, icon: 'milestones' },
  { label: 'Updates', value: project.value?.updates?.length || 0, icon: 'updates' },
]);

const healthSignals = computed(() => [
  { label: 'Execution state', value: statusLabel(project.value?.status) },
  { label: 'Funding', value: `${fundingProgress.value}% committed` },
  { label: 'Contracts', value: `${linkedContracts.value.length} linked` },
  { label: 'Issues', value: `${riskItems.value.length} flagged` }
]);

const riskItems = computed(() => {
  const items = [];
  if (!project.value) return items;
  if (!project.value.requirements?.length) {
    items.push({
      label: 'No requirements defined',
      body: 'The project does not yet specify materials, contractor needs, or services. Execution planning remains incomplete.',
      level: 'Medium',
      variant: 'finance'
    });
  }
  if (!linkedContracts.value.length) {
    items.push({
      label: 'No awarded contracts linked',
      body: 'The project has not been connected to any procurement outcome yet. Execution tracking will remain partial.',
      level: 'Medium',
      variant: 'warning'
    });
  }
  if (project.value.funding_required && fundingProgress.value < 20) {
    items.push({
      label: 'Funding still thin',
      body: 'Funding has started but commitment is still low relative to the project target.',
      level: 'Watch',
      variant: 'warning'
    });
  }
  if (!project.value.updates?.length) {
    items.push({
      label: 'No recent progress updates',
      body: 'Owners should publish execution updates so investors and managers can see current progress.',
      level: 'Low',
      variant: 'default'
    });
  }
  if (!items.length) {
    items.push({
      label: 'No major issues flagged',
      body: 'Current project data does not show an obvious blocker.',
      level: 'Low',
      variant: 'success'
    });
  }
  return items;
});

const activityItems = computed(() => {
  const items = [];
  if (!project.value) return items;
  items.push({
    id: `project-${project.value.id}`,
    title: 'Project created',
    body: `Project shell opened on ${formatDate(project.value.created_at)}.`,
    time: formatDateTime(project.value.created_at),
    timestamp: project.value.created_at ? new Date(project.value.created_at).getTime() : 0,
    variant: 'system'
  });
  linkedContracts.value.slice(0, 5).forEach((contract) => {
    items.push({
      id: `contract-${contract.id}`,
      title: `Contract linked: ${contract.title}`,
      body: `${contract.location} \u00b7 ${contractStatus(contract.status)}`,
      time: formatDateTime(contract.created_at),
      timestamp: contract.created_at ? new Date(contract.created_at).getTime() : 0,
      variant: 'external'
    });
  });
  (project.value.commitments || []).slice(0, 5).forEach((commitment) => {
    items.push({
      id: `commitment-${commitment.id}`,
      title: `Capital commitment recorded`,
      body: `${formatBudget(commitment.amount_committed)} from ${commitment.investor} (${commitment.status}).`,
      time: formatDateTime(commitment.created_at),
      timestamp: commitment.created_at ? new Date(commitment.created_at).getTime() : 0,
      variant: 'finance'
    });
  });
  (project.value.updates || []).slice(0, 5).forEach((update) => {
    items.push({
      id: `update-${update.id}`,
      title: `Update published by ${update.posted_by}`,
      body: update.update_text,
      time: formatDateTime(update.created_at),
      timestamp: update.created_at ? new Date(update.created_at).getTime() : 0,
      variant: 'user'
    });
  });
  return items
    .sort((left, right) => right.timestamp - left.timestamp)
    .slice(0, 10);
});

async function loadProject() {
  loading.value = true;
  try {
    const [projectRes, financeProductsRes] = await Promise.all([
      ProjectsService.get(route.params.id),
      api.get('/v3/finance/products/')
    ]);
    project.value = projectRes.data;
    financeProducts.value = financeProductsRes.data.results || financeProductsRes.data;
    const linked = project.value?.linked_contracts || [];
    if (!milestoneForm.value.contract_id && linked.length === 1) {
      milestoneForm.value.contract_id = linked[0].contract.id;
    }
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function addRequirement() {
  if (!isOwner.value) return;
  try {
    await ProjectsService.addRequirement(project.value.id, newReq.value);
    newReq.value = { type: 'MATERIAL', description: '', quantity: '' };
    showAlert('Requirement added successfully.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to add requirement.', 'error');
  }
}

async function pledge() {
  if (!canPledge.value) return;
  const amount = Number(pledgeAmount.value);
  if (!amount || amount <= 0) {
    showAlert('Enter a valid commitment amount.', 'error');
    return;
  }

  try {
    await ProjectsService.pledgeCommitment(project.value.id, amount);
    pledgeAmount.value = '';
    showAlert('Project commitment recorded successfully.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to record project commitment.', 'error');
  }
}

async function linkContract() {
  if (!isOwner.value || !contractIdToLink.value) return;
  try {
    await ProjectsService.linkContract(project.value.id, contractIdToLink.value);
    contractIdToLink.value = '';
    showAlert('Contract linked successfully.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to link contract.', 'error');
  }
}

async function postUpdate() {
  if (!isOwner.value) return;
  const text = updateText.value.trim();
  if (!text) return;
  try {
    await ProjectsService.postUpdate(project.value.id, { update_text: text });
    updateText.value = '';
    showAlert('Project update published successfully.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to publish project update.', 'error');
  }
}

async function removeRequirement(reqId) {
  if (!isOwner.value) return;
  try {
    await ProjectsService.removeRequirement(project.value.id, reqId);
    showAlert('Requirement removed.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Failed to remove requirement.', 'error');
  }
}

async function removeUpdate(updId) {
  if (!isOwner.value) return;
  try {
    await ProjectsService.removeUpdate(project.value.id, updId);
    showAlert('Update removed.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Failed to remove update.', 'error');
  }
}

async function unlinkContract(linkId) {
  if (!isOwner.value) return;
  try {
    await ProjectsService.unlinkContract(project.value.id, linkId);
    showAlert('Contract unlinked.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Failed to unlink contract.', 'error');
  }
}

async function createMilestone() {
  if (!isOwner.value) return;
  const contractId = milestoneForm.value.contract_id || (linkedContracts.value.length === 1 ? linkedContracts.value[0].id : '');
  if (!contractId) {
    showAlert('Select a linked contract first.', 'error');
    return;
  }
  if (!milestoneForm.value.title.trim() || !milestoneForm.value.amount || !milestoneForm.value.due_date) {
    showAlert('Milestone title, amount, and due date are required.', 'error');
    return;
  }
  try {
    await api.post(`/contracts/${contractId}/milestones/`, {
      title: milestoneForm.value.title.trim(),
      description: milestoneForm.value.description.trim(),
      amount: Number(milestoneForm.value.amount),
      due_date: milestoneForm.value.due_date
    });
    milestoneForm.value = {
      contract_id: milestoneForm.value.contract_id,
      title: '',
      description: '',
      amount: '',
      due_date: ''
    };
    showAlert('Milestone added successfully.', 'success');
    loadProject();
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Failed to add milestone.', 'error');
  }
}

async function applyForFinance() {
  if (!authStore.isAuthenticated) {
    showAlert('Sign in to apply for project financing.', 'error');
    return;
  }
  try {
    await api.post('/v3/finance/applications/', {
      product: financeForm.value.product,
      target_type: 'PROJECT',
      project: project.value.id,
      requested_amount: financeForm.value.requested_amount,
      purpose_category: financeForm.value.purpose_category,
      purpose: financeForm.value.purpose
    });
    showAlert('Project financing application submitted successfully.', 'success');
    financeForm.value = { product: '', requested_amount: '', purpose_category: 'COMPLETION', purpose: '' };
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to submit financing application.', 'error');
  }
}

onMounted(loadProject);
</script>

<style scoped>
.pz-project-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255, 252, 247, 0.92), rgba(243, 239, 231, 0.98)),
    radial-gradient(circle at top right, rgba(212, 101, 42, 0.08), transparent 28%);
}

/* Breadcrumb */
.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--pz-color-concrete-grey);
}

.pz-breadcrumb__item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--pz-color-earth-orange);
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.pz-breadcrumb__item:hover {
  opacity: 0.8;
}

.pz-breadcrumb__separator {
  color: var(--pz-color-concrete-grey);
  opacity: 0.5;
}

.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
}

/* Hero */
.pz-project-hero {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 0;
  background: #ffffff;
  border-radius: 24px;
  overflow: hidden;
  box-shadow:
    0 2px 4px rgba(10, 10, 15, 0.02),
    0 8px 16px rgba(10, 10, 15, 0.04),
    0 20px 40px rgba(10, 10, 15, 0.06);
}

.pz-project-hero__media {
  position: relative;
  min-height: 24rem;
  overflow: hidden;
  background: linear-gradient(135deg, #e8e4db, #d4cfc5);
}

.pz-project-hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.pz-project-hero:hover .pz-project-hero__image {
  transform: scale(1.03);
}

.pz-project-hero__fallback {
  width: 100%;
  height: 100%;
  min-height: 24rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #2a2825, #5b5148);
  color: white;
}

.pz-project-hero__fallback strong {
  font-family: var(--pz-font-display);
  font-size: 1.5rem;
  font-weight: 700;
}

.pz-project-hero__content {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pz-project-hero__description {
  max-width: 36rem;
  line-height: 1.6;
}

.pz-project-hero__price {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  background: rgba(212, 101, 42, 0.06);
  border: 1px solid rgba(212, 101, 42, 0.12);
}

.pz-project-hero__price strong {
  font-family: var(--pz-font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--pz-color-foundation-black);
  letter-spacing: -0.02em;
}

/* Summary Grid */
.pz-project-summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
}

.pz-project-detail__metric {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 0.95rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-metric__icon {
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 10px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  color: white;
}

.pz-metric__icon--earth { background: linear-gradient(135deg, #d4652a, #b87333); }
.pz-metric__icon--steel { background: linear-gradient(135deg, #2563eb, #1d4ed8); }
.pz-metric__icon--copper { background: linear-gradient(135deg, #b87333, #8b5a2b); }
.pz-metric__icon--finance { background: linear-gradient(135deg, #059669, #047857); }
.pz-metric__icon--violet { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
.pz-metric__icon--green { background: linear-gradient(135deg, #10b981, #059669); }

.pz-metric__icon svg {
  width: 1.1rem;
  height: 1.1rem;
}

.pz-metric__content {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.pz-project-detail__label {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-project-detail__value {
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

/* Layout */
.pz-project-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.75rem;
}

.pz-project-sidebar {
  position: sticky;
  top: 2rem;
  align-self: start;
  height: fit-content;
  display: grid;
  gap: 1rem;
}

/* Tabs */
.pz-project-tabs {
  display: flex;
  gap: 0.4rem;
  overflow-x: auto;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  border: 1px solid rgba(10, 10, 15, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  width: fit-content;
  max-width: 100%;
}

.pz-project-tabs::-webkit-scrollbar {
  display: none;
}

.pz-project-tab {
  position: relative;
  padding: 0.7rem 1.1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pz-project-tab:hover {
  color: var(--pz-color-structural-steel);
  background: rgba(10, 10, 15, 0.03);
}

.pz-project-tab--active {
  background: white;
  color: var(--pz-color-earth-orange);
  box-shadow: 0 2px 8px rgba(10, 10, 15, 0.08);
}

.pz-project-tab__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.4rem;
  height: 1.4rem;
  padding: 0 0.35rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
}

.pz-tab-panel {
  animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Tab panel inner content */
.project-overview__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.project-overview__label {
  margin: 0 0 0.25rem;
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.project-overview__value {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.project-overview__body {
  margin: 1.25rem 0 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.7;
}

.project-health {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.85rem;
  margin: 1.25rem 0;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.project-health__item {
  padding: 0.85rem 0.95rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.project-health__label {
  display: block;
  margin-bottom: 0.3rem;
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.project-health__value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

/* Grid lists & items */
.project-grid-list {
  display: grid;
  gap: 0.85rem;
}

.project-item {
  padding: 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(10, 10, 15, 0.06);
  transition: all 0.2s ease;
}

.project-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(10, 10, 15, 0.1);
}

.project-item__head,
.project-item__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.project-item__meta {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.project-item__title {
  margin: 0.75rem 0 0.35rem;
  font-family: var(--pz-font-display);
  font-size: 1.02rem;
  font-weight: 600;
}

.project-item__body {
  margin: 0;
  line-height: 1.6;
  color: var(--pz-color-structural-steel);
}

.project-item__link {
  color: var(--pz-color-earth-orange);
  text-decoration: none;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.project-item__link:hover {
  text-decoration: underline;
}

.project-item__remove {
  background: transparent;
  border: none;
  padding: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  cursor: pointer;
}

.project-item__remove:hover {
  text-decoration: underline;
}

/* Timeline */
.project-timeline {
  display: grid;
  gap: 0.9rem;
}

.project-timeline__item {
  display: grid;
  grid-template-columns: 0.8rem minmax(0, 1fr);
  gap: 0.85rem;
  align-items: start;
}

.project-timeline__node {
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 999px;
  margin-top: 0.35rem;
  background: var(--pz-color-earth-orange);
}

.project-timeline__node--system { background: var(--pz-color-steel-blue); }
.project-timeline__node--user { background: var(--pz-color-savanna-green); }
.project-timeline__node--external { background: var(--pz-color-copper-circuit); }
.project-timeline__node--finance { background: var(--pz-color-earth-orange); }

.project-timeline__content {
  padding: 0.95rem 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.project-timeline__meta {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.45rem;
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.project-timeline__content p {
  margin: 0;
  line-height: 1.6;
}

/* Forms */
.project-form {
  display: grid;
  gap: 0.85rem;
  padding-top: 0.95rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

.project-form--stacked {
  gap: 1rem;
}

.project-form__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}

/* Funding */
.project-funding {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.project-funding--compact {
  margin-top: 1rem;
  margin-bottom: 0;
}

.project-funding__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.95rem;
}

.project-funding__row strong {
  font-family: var(--pz-font-display);
  font-weight: 700;
}

.project-funding__bar {
  height: 0.5rem;
  border-radius: 999px;
  background: rgba(10, 10, 15, 0.08);
  overflow: hidden;
}

.project-funding__bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--pz-color-copper-circuit), var(--pz-color-earth-orange));
}

.project-funding__note {
  margin: 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.6;
  font-size: 0.85rem;
}

/* Empty state */
.project-empty-state {
  padding: 0.75rem 0;
  color: var(--pz-color-structural-steel);
}

/* Summary sidebar */
.project-summary {
  display: grid;
  gap: 0.85rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.project-summary__row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
}

.project-summary__row strong {
  font-family: var(--pz-font-display);
  font-weight: 700;
}

/* Quick actions */
.project-quick-actions {
  display: grid;
  gap: 0.65rem;
}

/* Utilities */
.pz-l-flex {
  display: flex;
}

.pz-l-flex--justify-between {
  justify-content: space-between;
}

.pz-l-flex--align-start {
  align-items: flex-start;
}

.pz-l-flex--align-center {
  align-items: center;
}

.pz-l-flex--gap-2 {
  gap: 0.5rem;
}

.pz-l-flex--gap-4 {
  gap: 1rem;
}

.pz-l-flex--wrap {
  flex-wrap: wrap;
}

.pz-space-y-3 > * + * {
  margin-top: 0.75rem;
}

.pz-space-y-6 > * + * {
  margin-top: 1.5rem;
}

.pz-space-y-8 > * + * {
  margin-top: 2rem;
}

.pz-u-text-center {
  text-align: center;
}

.pz-u-text-display {
  font-family: var(--pz-font-display);
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin: 0;
}

.text-lg {
  font-size: 1.25rem;
}

.text-sm {
  font-size: 0.875rem;
}

.text-xs {
  font-size: 0.75rem;
}

.pz-u-text-mono {
  font-family: var(--pz-font-mono);
}

.pz-u-color-earth {
  color: var(--pz-color-earth-orange);
}

.pz-u-color-steel {
  color: var(--pz-color-structural-steel);
}

.pz-u-color-concrete {
  color: var(--pz-color-concrete-grey);
}

.u-py-20 {
  padding-top: 5rem;
  padding-bottom: 5rem;
}

.u-mb-4 {
  margin-bottom: 1rem;
}

.u-mt-4 {
  margin-top: 1rem;
}

.c-loader {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 2px solid rgba(10, 10, 15, 0.08);
  border-top-color: var(--pz-color-earth-orange);
  margin: 0 auto;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .pz-project-hero {
    grid-template-columns: 1fr;
  }
  .pz-project-hero__media,
  .pz-project-hero__fallback {
    min-height: 20rem;
    border-radius: 24px 24px 0 0;
  }
  .pz-project-layout {
    grid-template-columns: 1fr;
  }
  .pz-project-sidebar {
    position: static;
  }
  .pz-project-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .project-health {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .pz-project-hero__content {
    padding: 1.5rem;
  }
  .pz-project-summary-grid {
    grid-template-columns: 1fr;
  }
  .project-health {
    grid-template-columns: 1fr;
  }
  .project-overview__grid,
  .project-form__row {
    grid-template-columns: 1fr;
  }
}
</style>
