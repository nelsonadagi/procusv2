<template>
  <div class="pz-contract-page">
    <div v-if="loading" class="pz-u-text-center u-py-20">
      <div class="c-loader u-mb-4"></div>
      <p class="pz-u-text-mono text-xs">Loading contract intelligence...</p>
    </div>

    <div v-else-if="error" class="pz-u-text-center u-py-20">
      <div class="c-alert c-alert--danger u-mb-6">{{ error }}</div>
      <Button variant="primary" @click="$router.push('/contracts')">Back to Contracts</Button>
    </div>

    <div v-else-if="contract" class="pz-l-container u-py-8">
      <!-- Breadcrumb -->
      <nav class="pz-breadcrumb u-mb-8">
        <router-link to="/contracts" class="pz-breadcrumb__item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
          Contracts
        </router-link>
        <span class="pz-breadcrumb__separator">/</span>
        <span class="pz-breadcrumb__current pz-u-color-steel">{{ contract.title }}</span>
      </nav>

      <!-- Hero -->
      <section class="pz-contract-hero">
        <div class="pz-contract-hero__media">
          <img :src="contract.featured_image_url || '/placeholder.png'" :alt="contract.title" class="pz-contract-hero__image" />
          <div class="pz-contract-hero__badges">
            <Badge variant="ghost">{{ categoryLabel }}</Badge>
            <Badge :variant="getContractStatusVariant(contract.status)">{{ contract.status }}</Badge>
          </div>
        </div>

        <div class="pz-contract-hero__content">
          <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start pz-l-flex--gap-4 pz-l-flex--wrap">
            <div class="pz-space-y-3">
              <div class="pz-u-text-mono text-xs pz-u-color-earth">Work Order</div>
              <h1 class="pz-u-text-display">{{ contract.title }}</h1>
              <p class="pz-u-text-mono text-sm pz-u-color-steel pz-contract-hero__description">{{ contract.description_scope }}</p>
            </div>
            <div class="pz-l-flex pz-l-flex--gap-2 pz-l-flex--wrap">
              <Button variant="outline" size="sm" @click="$router.back()">Back</Button>
              <Badge variant="secondary">ID {{ contract.id }}</Badge>
            </div>
          </div>

          <div class="pz-contract-hero__price">
            <span class="pz-u-text-mono text-xs pz-u-color-concrete">Budget Range</span>
            <strong>{{ formatMoney(contract.budget_min) }} - {{ formatMoney(contract.budget_max) }}</strong>
            <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ contract.location || 'Location pending' }}</span>
          </div>

          <div v-if="summaryStats.length" class="pz-contract-summary-grid">
            <div v-for="stat in summaryStats" :key="stat.label" class="pz-contract-detail__metric">
              <span class="pz-metric__icon" :class="'pz-metric__icon--' + metricColor(stat.icon)" v-html="metricIcon(stat.icon)"></span>
              <div class="pz-metric__content">
                <span class="pz-contract-detail__label">{{ stat.label }}</span>
                <span class="pz-contract-detail__value">{{ stat.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
        <div class="pz-contract-workflow-banner">
          <div class="pz-contract-workflow-banner__summary">
            <div class="pz-contract-workflow-banner__kicker">{{ workflowBanner.stage }}</div>
            <h2 class="pz-contract-workflow-banner__title">{{ workflowBanner.title }}</h2>
            <p class="pz-contract-workflow-banner__body">{{ workflowBanner.body }}</p>
          </div>
          <div class="pz-contract-workflow-banner__actions">
            <Button v-if="workflowBanner.primaryAction" variant="primary" size="sm" @click="workflowBanner.primaryAction.handler">
              {{ workflowBanner.primaryAction.label }}
            </Button>
            <Button v-if="workflowBanner.secondaryAction" variant="outline" size="sm" @click="workflowBanner.secondaryAction.handler">
              {{ workflowBanner.secondaryAction.label }}
            </Button>
          </div>
        </div>
        <div class="pz-contract-workflow-banner__steps">
          <div
            v-for="step in workflowSteps"
            :key="step.label"
            class="pz-contract-workflow-step"
            :class="{ 'pz-contract-workflow-step--done': step.done, 'pz-contract-workflow-step--active': step.active }"
          >
            <span class="pz-contract-workflow-step__index">{{ step.index }}</span>
            <div class="pz-contract-workflow-step__content">
              <strong>{{ step.label }}</strong>
              <span>{{ step.help }}</span>
            </div>
          </div>
        </div>
      

      <ModuleCTA
        eyebrow="Procurement Path"
        title="Need another contractor or want to respond to similar tenders?"
        body="Post a new tender as a project owner, or activate contractor onboarding to submit compliant responses to open opportunities."
        primary-label="Post Tender"
        primary-to="/contracts/new"
        secondary-label="Contractor Onboarding"
        secondary-to="/contractors/register"
        tone="savanna"
      />
</WorkflowGuide>

      <!-- Layout -->
      <div class="pz-contract-layout">
        <section class="pz-space-y-6">
          <!-- Tabs -->
          <div class="pz-contract-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="pz-contract-tab"
              :class="{ 'pz-contract-tab--active': activeTab === tab.id }"
              @click="activeTab = tab.id"
            >
              <span class="pz-contract-tab__label">{{ tab.label }}</span>
              <span v-if="tab.count !== null" class="pz-contract-tab__badge">{{ tab.count }}</span>
            </button>
          </div>

          <!-- Overview -->
          <div v-show="activeTab === 'overview'" class="pz-tab-panel pz-space-y-6">
            <Card title="Procurement Snapshot" variant="premium" eyebrow="Summary">
              <div class="pz-detail-chip-grid">
                <div v-for="item in snapshotItems" :key="item.label" class="pz-detail-chip">
                  <span>{{ item.label }}</span>
                  <strong>{{ item.value }}</strong>
                </div>
              </div>
              <div class="pz-detail-stack pz-u-mt-4">
                <div v-for="step in timelineSteps" :key="step.label" class="pz-detail-subcard">
                  <div class="pz-detail-card__eyebrow">{{ step.kicker }}</div>
                  <h4>{{ step.label }}</h4>
                  <p>{{ step.value }}</p>
                </div>
              </div>
            </Card>

            <Card title="Work Scope" variant="premium" eyebrow="Operations">
              <p class="pz-contract-scope__text">{{ contract.description_scope }}</p>
              <div class="pz-detail-chip-grid u-mt-4">
                <div class="pz-detail-chip">
                  <span>Deployment Location</span>
                  <strong>{{ contract.location || 'Location pending' }}</strong>
                </div>
                <div class="pz-detail-chip">
                  <span>Projected Budget</span>
                  <strong>{{ formatMoney(contract.budget_min) }} - {{ formatMoney(contract.budget_max) }}</strong>
                </div>
                <div class="pz-detail-chip">
                  <span>Start Date</span>
                  <strong>{{ formatDate(contract.project_start_date) }}</strong>
                </div>
                <div class="pz-detail-chip">
                  <span>End Date</span>
                  <strong>{{ formatDate(contract.project_end_date) }}</strong>
                </div>
              </div>
            </Card>

            <Card title="Payment and Eligibility" variant="premium" eyebrow="Commercial Terms">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-detail-subcard">
                  <div class="pz-detail-card__eyebrow">Payment Terms</div>
                  <p>{{ contract.payment_terms || 'Not specified' }}</p>
                </div>
                <div class="pz-detail-subcard">
                  <div class="pz-detail-card__eyebrow">Eligibility</div>
                  <p>{{ contract.eligibility_criteria || 'Not specified' }}</p>
                </div>
              </div>
            </Card>
          </div>

          <!-- Bids -->
          <div v-show="activeTab === 'bids'" class="pz-tab-panel pz-space-y-6">
            <Card v-if="isOwner && (contract.status === 'POSTED' || contract.status === 'BIDDING')" title="Received Bids" variant="premium" eyebrow="Owner Review">
              <div v-if="bids.length === 0" class="pz-contract-empty">
                <div class="pz-contract-empty__kicker">NO BIDS RECEIVED YET</div>
                <p>The tender is live. Contractors will appear here as submissions come in.</p>
              </div>
              <div v-else class="pz-detail-stack">
                <article v-for="bid in bids" :key="bid.id" class="pz-bid-card">
                  <div class="pz-bid-card__top">
                    <div>
                      <div class="pz-bid-card__company">{{ bid.contractor?.company_name || 'Contractor' }}</div>
                      <div class="pz-bid-card__meta">Timeline: {{ bid.proposed_timeline_days }} days</div>
                    </div>
                    <div class="pz-bid-card__price">{{ formatMoney(bid.proposed_cost) }}</div>
                  </div>
                  <p class="pz-bid-card__message">{{ bid.message }}</p>
                  <div v-if="bid.status === 'SUBMITTED'" class="pz-bid-card__footer">
                    <Button size="sm" variant="outline" :loading="shortlistingBidId === bid.id" @click="shortlistBid(bid.id)">Shortlist</Button>
                    <Button size="sm" variant="primary" @click="awardBid(bid.id)">Award Contract</Button>
                  </div>
                  <div v-else class="pz-bid-card__footer pz-bid-card__footer--status">
                    <Badge>{{ bid.status }}</Badge>
                  </div>
                </article>
              </div>
            </Card>

            <Card v-else-if="canBid" title="Submit Bid" variant="premium" eyebrow="Contractor">
              <form @submit.prevent="submitBid" class="pz-space-y-5">
                <PzInput :label="`Projected Expenditure (${contract.currency || 'KES'})`" type="number" v-model="bidForm.proposed_cost" required />
                <PzInput label="Deployment Duration (Days)" type="number" v-model="bidForm.proposed_timeline_days" required />
                <div class="pz-input-wrapper">
                  <label class="pz-input__label">Strategic Proposal</label>
                  <textarea v-model="bidForm.message" class="pz-input" rows="4" placeholder="Outline your approach, team, and delivery advantage..."></textarea>
                </div>
                <Button type="submit" variant="primary" fullWidth :loading="submittingBid">Submit Proposal</Button>
              </form>
            </Card>

            <Card v-else-if="isContractor && hasBid" title="Your Bid" variant="premium" eyebrow="Submission">
              <div class="pz-bid-status">
                <Badge size="lg" :variant="getBidStatusVariant(myBid.status)">{{ myBid.status }}</Badge>
                <p>Submitted on {{ new Date(myBid.created_at).toLocaleDateString() }}</p>
              </div>
            </Card>

            <Card v-else title="Bids" variant="premium" eyebrow="Status">
              <p class="pz-contract-empty">Bidding is {{ contract.status === 'AWARDED' || contract.status === 'IN_PROGRESS' || contract.status === 'COMPLETED' ? 'closed' : 'not yet open' }} for this contract.</p>
            </Card>
          </div>

          <!-- Milestones -->
          <div v-show="activeTab === 'milestones'" class="pz-tab-panel pz-space-y-6">
            <Card title="Execution Milestones" variant="premium" eyebrow="Delivery">
              <div v-if="milestones.length === 0" class="pz-contract-empty">
                <div class="pz-contract-empty__kicker">NO MILESTONES REGISTERED</div>
                <p>Define checkpoints once the contract is awarded so payment and delivery stay controlled.</p>
              </div>
              <div v-else class="pz-detail-stack">
                <div v-for="m in milestones" :key="m.id" class="pz-detail-subcard pz-contract-milestone">
                  <div class="pz-contract-milestone__top">
                    <div>
                      <h4>{{ m.title }}</h4>
                      <p>Due {{ m.due_date }} &bull; {{ formatMoney(m.amount) }}</p>
                    </div>
                    <Badge :variant="getMilestoneVariant(m.status)">{{ m.status }}</Badge>
                  </div>
                  <div class="pz-contract-milestone__actions">
                    <Button v-if="isOwner && m.status === 'COMPLETED'" size="sm" variant="finance" @click="approveMilestone(m.id)">Release Funds</Button>
                    <Button v-if="isContractor && m.status === 'PENDING'" size="sm" variant="primary" @click="completeMilestone(m.id)">Mark Complete</Button>
                    <Button size="sm" variant="outline" @click="openChat">Chat</Button>
                  </div>
                </div>
              </div>
              <div v-if="canManageMilestones" class="pz-u-mt-4">
                <Button size="sm" variant="outline" @click="showAddMilestone = true">Add Milestone</Button>
              </div>
            </Card>
          </div>

          <!-- Attachments -->
          <div v-show="activeTab === 'attachments'" class="pz-tab-panel pz-space-y-6">
            <Card v-if="attachments.length" title="Procurement Pack" variant="premium" eyebrow="Files">
              <div class="pz-detail-stack">
                <a v-for="attachment in attachments" :key="attachment.id" :href="attachment.file_url || '#'" class="pz-detail-doc" target="_blank" rel="noreferrer">
                  <div class="pz-contract-attachment__preview">
                    <img v-if="isImageAttachment(attachment)" :src="attachment.file_url" :alt="attachment.title">
                    <div v-else class="pz-contract-attachment__placeholder">{{ attachment.attachment_type_label }}</div>
                  </div>
                  <div class="pz-space-y-1">
                    <strong>{{ attachment.title }}</strong>
                    <span>{{ attachment.attachment_type_label }}</span>
                  </div>
                </a>
              </div>
            </Card>
            <Card v-else title="Attachments" variant="premium" eyebrow="Files">
              <p class="pz-contract-empty">No documents have been uploaded for this contract yet.</p>
            </Card>
          </div>
        </section>

        <!-- Sidebar -->
        <aside class="pz-contract-sidebar">
          <Card title="Quick View" variant="elevated">
            <div class="pz-detail-stack">
              <div class="pz-detail-subcard">
                <span>Status</span>
                <strong>{{ contract.status }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Category</span>
                <strong>{{ categoryLabel }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Owner</span>
                <strong>{{ contract.owner_username || 'Project Owner' }}</strong>
              </div>
              <div class="pz-detail-subcard">
                <span>Deadline</span>
                <strong>{{ deadlineLabel }}</strong>
              </div>
            </div>
          </Card>

          <Card v-if="canBid" title="Submit Bid" variant="accent">
            <form @submit.prevent="submitBid" class="pz-space-y-4">
              <PzInput :label="`Amount (${contract.currency || 'KES'})`" type="number" v-model="bidForm.proposed_cost" required />
              <PzInput label="Duration (Days)" type="number" v-model="bidForm.proposed_timeline_days" required />
              <Button type="submit" variant="primary" fullWidth :loading="submittingBid">Submit Proposal</Button>
            </form>
          </Card>

          <Card v-if="isContractor && hasBid" title="Your Bid" variant="glass">
            <div class="pz-bid-status">
              <Badge size="lg" :variant="getBidStatusVariant(myBid.status)">{{ myBid.status }}</Badge>
              <p class="pz-u-text-mono text-xs pz-u-color-concrete u-mt-2">Submitted {{ new Date(myBid.created_at).toLocaleDateString() }}</p>
            </div>
          </Card>

          <Card v-if="canManageMilestones" title="Management" variant="glass">
            <div class="pz-detail-stack">
              <Button v-if="contract.status === 'PENDING'" block variant="primary" :loading="publishingContract" @click="publishContract">Publish to Marketplace</Button>
              <Button v-else-if="contract.status === 'POSTED' || contract.status === 'BIDDING'" block variant="danger" disabled>Close Bidding</Button>
              <Button v-else block variant="outline" disabled>Contract {{ contract.status }}</Button>
            </div>
          </Card>
        </aside>
      </div>
    </div>

    <!-- Modals -->
    <Modal :isOpen="showAddMilestone" title="Add Milestone" size="md" @close="showAddMilestone = false">
      <form id="ms-form" @submit.prevent="addMilestone" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
        <PzInput v-model="milestoneForm.title" label="Title" required />
        <PzInput v-model="milestoneForm.description" label="Description" type="textarea" rows="3" />
        <PzInput v-model="milestoneForm.amount" :label="`Amount (${contract?.currency || 'KES'})`" type="number" required />
        <PzInput v-model="milestoneForm.due_date" label="Due Date" type="date" required />
      </form>
      <template #footer>
        <Button variant="outline" @click="showAddMilestone = false">Cancel</Button>
        <Button type="submit" form="ms-form" variant="primary">Add</Button>
      </template>
    </Modal>

    <Modal :isOpen="showChatModal" title="Contract Operations Chat" size="lg" @close="showChatModal = false">
      <ChatWindow v-if="activeChatRoomId" :roomId="String(activeChatRoomId)" />
    </Modal>

    <Modal :isOpen="showAwardConfirm" title="Award Contract" size="sm" @close="closeAwardConfirm">
      <div class="pz-confirm-panel">
        <p class="pz-confirm-panel__title">Award this contract to the selected bidder?</p>
        <p class="pz-confirm-panel__body">
          This moves the contract out of bidding and into the awarded workflow. Use this only when procurement review is complete.
        </p>
      </div>
      <template #footer>
        <Button variant="outline" @click="closeAwardConfirm">Cancel</Button>
        <Button variant="primary" :loading="awardingBid" @click="confirmAwardBid">Award Contract</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue';
import { useRoute } from 'vue-router';
import ContractsService from '../services/contracts';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Modal from '../components/ui/Modal.vue';
import PzInput from '../components/PzInput.vue';
import ChatWindow from '../components/chat/ChatWindow.vue';

const route = useRoute();
const authStore = useAuthStore();
const showAlert = inject('showAlert');
const contract = ref(null);
const loading = ref(true);
const error = ref(null);
const bids = ref([]);
const milestones = ref([]);
const myBid = ref(null);
const submittingBid = ref(false);
const showAddMilestone = ref(false);
const showChatModal = ref(false);
const activeChatRoomId = ref(null);
const showAwardConfirm = ref(false);
const pendingAwardBidId = ref(null);
const awardingBid = ref(false);
const shortlistingBidId = ref(null);
const publishingContract = ref(false);
const activeTab = ref('overview');

const attachments = computed(() => contract.value?.attachments || []);
const categoryLabel = computed(() => contract.value?.category?.name || 'Uncategorized');
const deadlineLabel = computed(() => formatDeadline(contract.value?.bid_deadline));

const tabs = computed(() => [
  { id: 'overview', label: 'Overview', count: null },
  { id: 'bids', label: 'Bids', count: bids.value.length || null },
  { id: 'milestones', label: 'Milestones', count: milestones.value.length || null },
  { id: 'attachments', label: 'Attachments', count: attachments.value.length || null },
]);

function openTab(tabId) {
  activeTab.value = tabId;
}

const workflowBanner = computed(() => {
  if (!contract.value) {
    return {
      stage: 'LOADING',
      title: 'Preparing contract workspace',
      body: 'Loading the tender, bids, and milestone state so the next action is visible as soon as the page opens.',
      primaryAction: null,
      secondaryAction: null,
    };
  }

  if (contract.value.status === 'PENDING') {
    return {
      stage: 'DRAFT',
      title: 'Publish the tender to the market',
      body: 'The brief is still private. Publish it when the scope, dates, and budget are ready for contractors.',
      primaryAction: canManageMilestones.value ? { label: 'Publish Tender', handler: publishContract } : null,
      secondaryAction: { label: 'Review Overview', handler: () => openTab('overview') },
    };
  }

  if (contract.value.status === 'POSTED' || contract.value.status === 'BIDDING') {
    return {
      stage: 'BIDDING',
      title: 'Review live bids and scope coverage',
      body: 'Open the bids tab to shortlist submissions, check compliance, and move toward award once a strong proposal is ready.',
      primaryAction: { label: 'Review Bids', handler: () => openTab('bids') },
      secondaryAction: { label: 'Open Milestones', handler: () => openTab('milestones') },
    };
  }

  if (contract.value.status === 'AWARDED') {
    return {
      stage: 'AWARDED',
      title: 'Move this contract into execution',
      body: 'The contract has been awarded. Add or review milestones, keep attachments current, and move progress into the active workspace.',
      primaryAction: { label: 'Open Milestones', handler: () => openTab('milestones') },
      secondaryAction: { label: 'Review Attachments', handler: () => openTab('attachments') },
    };
  }

  if (contract.value.status === 'IN_PROGRESS') {
    return {
      stage: 'EXECUTION',
      title: 'Keep the delivery stage visible',
      body: 'Use milestones and attachments to track what is complete, what is pending, and what the next approval should be.',
      primaryAction: { label: 'Open Milestones', handler: () => openTab('milestones') },
      secondaryAction: { label: 'Open Overview', handler: () => openTab('overview') },
    };
  }

  return {
    stage: contract.value.status || 'SUMMARY',
    title: 'Track completion and close out the tender',
    body: 'The contract is complete. Keep the history visible for reference, disputes, and audit review.',
    primaryAction: { label: 'View Activity', handler: () => openTab('overview') },
    secondaryAction: { label: 'Open Attachments', handler: () => openTab('attachments') },
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Publish the tender',
    help: 'Move the brief from draft into the market.',
    done: contract.value?.status !== 'PENDING',
    active: contract.value?.status === 'PENDING',
  },
  {
    index: '02',
    label: 'Review bids',
    help: 'Compare contractor submissions and shortlist the strongest proposals.',
    done: Boolean(bids.value.length),
    active: activeTab.value === 'bids',
  },
  {
    index: '03',
    label: 'Award or start execution',
    help: 'Award the contract and keep milestones visible.',
    done: ['AWARDED', 'IN_PROGRESS', 'COMPLETED'].includes(contract.value?.status),
    active: activeTab.value === 'milestones',
  },
  {
    index: '04',
    label: 'Track close-out',
    help: 'Use attachments and history for handoff, approvals, and audit context.',
    done: contract.value?.status === 'COMPLETED',
    active: activeTab.value === 'attachments',
  },
]);

const snapshotItems = computed(() => [
  { label: 'Category', value: categoryLabel.value },
  { label: 'Bid Deadline', value: formatDateTime(contract.value?.bid_deadline) || 'TBD' },
  { label: 'Start Date', value: formatDate(contract.value?.project_start_date) },
  { label: 'Completion Date', value: formatDate(contract.value?.project_end_date) },
  { label: 'Currency', value: contract.value?.currency || 'KES' },
]);

const timelineSteps = computed(() => [
  {
    kicker: '01',
    label: 'Bid Window',
    value: deadlineLabel.value,
    state: getTimelineState(contract.value?.bid_deadline),
  },
  {
    kicker: '02',
    label: 'Start',
    value: formatDate(contract.value?.project_start_date),
    state: contract.value?.project_start_date ? 'active' : 'pending',
  },
  {
    kicker: '03',
    label: 'Finish',
    value: formatDate(contract.value?.project_end_date),
    state: contract.value?.project_end_date ? 'active' : 'pending',
  },
]);

const summaryStats = computed(() => [
  { label: 'Budget', value: `${formatMoney(contract.value?.budget_min)} - ${formatMoney(contract.value?.budget_max)}`, icon: 'budget' },
  { label: 'Deadline', value: deadlineLabel.value, icon: 'deadline' },
  { label: 'Status', value: contract.value?.status || 'Pending', icon: 'status' },
  { label: 'Bids', value: bids.value.length, icon: 'bids' },
  { label: 'Milestones', value: milestones.value.length, icon: 'milestones' },
  { label: 'Files', value: attachments.value.length, icon: 'files' },
]);

const bidForm = ref({ proposed_cost: null, proposed_timeline_days: null, message: '' });
const milestoneForm = ref({ title: '', description: '', amount: null, due_date: '' });

const isOwner = computed(() => contract.value && authStore.user?.id === contract.value.owner);
const linkedProjectOwnerId = computed(() => contract.value?.linked_project?.owner || null);
const canManageMilestones = computed(() => {
  if (!contract.value || !authStore.user) return false;
  return authStore.isAdmin || authStore.user.id === contract.value.owner || authStore.user.id === linkedProjectOwnerId.value;
});
const isContractor = computed(() => authStore.hasRole('CONTRACTOR'));
const hasBid = computed(() => !!myBid.value);
const canBid = computed(() => isContractor.value && !hasBid.value && (contract.value?.status === 'POSTED' || contract.value?.status === 'BIDDING'));

onMounted(async () => {
  loadContract();
});

function formatDate(dateStr) {
  if (!dateStr) return 'TBD';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatDateTime(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
}

function formatMoney(amount, sourceCurrency = contract.value?.currency || 'KES') {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return configStore.formatPrice(0, sourceCurrency);
  return configStore.formatPrice(value, sourceCurrency);
}

function formatDeadline(dateStr) {
  if (!dateStr) return 'Deadline TBD';
  const deadline = new Date(dateStr);
  const diffDays = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
  if (diffDays > 1) return `Closes in ${diffDays} days`;
  if (diffDays === 1) return 'Closes tomorrow';
  if (diffDays === 0) return 'Closes today';
  return `Closed ${Math.abs(diffDays)} days ago`;
}

function getTimelineState(dateStr) {
  if (!dateStr) return 'pending';
  return new Date(dateStr) >= new Date() ? 'active' : 'completed';
}

function isImageAttachment(attachment) {
  const url = attachment.file_url || '';
  return /\.(png|jpe?g|gif|webp|bmp|svg)$/i.test(url);
}

function metricIcon(type) {
  const icons = {
    budget: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>',
    deadline: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    status: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    bids: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    milestones: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    files: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>',
  };
  return icons[type] || icons.budget;
}

function metricColor(type) {
  const colors = {
    budget: 'earth',
    deadline: 'steel',
    status: 'copper',
    bids: 'finance',
    milestones: 'violet',
    files: 'green',
  };
  return colors[type] || 'earth';
}

async function loadContract(options = {}) {
  const { silent = false } = options;
  const id = route.params.id;
  if (!silent) {
    loading.value = true;
    error.value = null;
  }
  try {
    bids.value = [];
    milestones.value = [];
    myBid.value = null;
    const res = await ContractsService.get(id);
    contract.value = res.data;

    if (isOwner.value) {
      const bidsRes = await ContractsService.getBids(id);
      bids.value = bidsRes.data;
    } else if (isContractor.value) {
      try {
        const myBidsRes = await ContractsService.getBids(id);
        if (myBidsRes.data.length > 0) {
          myBid.value = myBidsRes.data[0];
        }
      } catch (e) {
        // maybe 403 or empty
      }
    }

    if (contract.value?.milestones?.length) {
      milestones.value = contract.value.milestones;
    } else if (contract.value?.status === 'AWARDED' || contract.value?.status === 'IN_PROGRESS' || contract.value?.status === 'COMPLETED') {
      try {
        const milestonesRes = await ContractsService.getMilestones(id);
        milestones.value = milestonesRes.data;
      } catch (e) {
        milestones.value = [];
      }
    }
    error.value = null;
  } catch (err) {
    console.error("Load failed", err);
    error.value = err.response?.data?.detail || 'Unable to load contract details.';
  } finally {
    if (!silent) {
      loading.value = false;
    }
  }
}

async function submitBid() {
  submittingBid.value = true;
  try {
    await ContractsService.submitBid(route.params.id, {
      contract: contract.value.id,
      proposed_cost: bidForm.value.proposed_cost === '' || bidForm.value.proposed_cost === null
        ? null
        : Number(bidForm.value.proposed_cost),
      proposed_timeline_days: bidForm.value.proposed_timeline_days === '' || bidForm.value.proposed_timeline_days === null
        ? null
        : Number(bidForm.value.proposed_timeline_days),
      message: bidForm.value.message?.trim() || '',
    });
    showAlert('Bid submitted successfully.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(formatApiError(err, 'Bid submission failed.'), 'error');
  } finally {
    submittingBid.value = false;
  }
}

async function shortlistBid(bidId) {
  shortlistingBidId.value = bidId;
  try {
    await ContractsService.shortlistBid(bidId);
    showAlert('Bid shortlisted successfully.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Shortlisting failed.', 'error');
  } finally {
    shortlistingBidId.value = null;
  }
}

function awardBid(bidId) {
  pendingAwardBidId.value = bidId;
  showAwardConfirm.value = true;
}

function closeAwardConfirm() {
  showAwardConfirm.value = false;
  pendingAwardBidId.value = null;
}

async function confirmAwardBid() {
  if (!pendingAwardBidId.value) return;
  awardingBid.value = true;
  try {
    await ContractsService.awardBid(pendingAwardBidId.value);
    showAlert('Contract awarded successfully.', 'success');
    closeAwardConfirm();
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Award failed.', 'error');
  } finally {
    awardingBid.value = false;
  }
}

async function addMilestone() {
  try {
    await ContractsService.addMilestone(route.params.id, milestoneForm.value);
    showAddMilestone.value = false;
    milestoneForm.value = { title: '', description: '', amount: null, due_date: '' };
    showAlert('Milestone added successfully.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || 'Failed to add milestone.', 'error');
  }
}

async function completeMilestone(mId) {
  try {
    await ContractsService.completeMilestone(mId);
    showAlert('Milestone marked as complete.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Failed to complete milestone.', 'error');
  }
}

async function approveMilestone(mId) {
  try {
    await ContractsService.approveMilestone(mId);
    showAlert('Milestone approved and funds released.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Approval failed.', 'error');
  }
}

async function publishContract() {
  if (!isOwner.value) return;
  publishingContract.value = true;
  try {
    await ContractsService.publish(route.params.id);
    showAlert('Contract published to marketplace.', 'success');
    loadContract({ silent: true });
  } catch (err) {
    showAlert(err.response?.data?.detail || err.response?.data?.error || 'Publish failed.', 'error');
  } finally {
    publishingContract.value = false;
  }
}

async function openChat() {
  try {
    const res = await api.post('/chat/rooms/get-or-create/', { contract: route.params.id });
    activeChatRoomId.value = res.data.id;
    showChatModal.value = true;
  } catch (err) {
    showAlert(err.response?.data?.error || 'Failed to initiate chat session.', 'error');
  }
}

const getContractStatusVariant = (s) => {
  return s === 'AWARDED' ? 'success' : 'info';
};
const getBidStatusVariant = (s) => {
  return s === 'AWARDED' ? 'success' : 'warning';
};
const getMilestoneVariant = (s) => {
  return s === 'APPROVED' ? 'success' : s === 'COMPLETED' ? 'warning' : 'secondary';
};

function formatApiError(err, fallback) {
  const data = err?.response?.data;
  if (!data) return fallback;
  if (typeof data.detail === 'string') return data.detail;
  if (typeof data.error === 'string') return data.error;
  if (typeof data === 'string') return data;
  if (typeof data === 'object') {
    const entries = Object.entries(data)
      .map(([key, value]) => {
        if (Array.isArray(value)) return `${key}: ${value.join(', ')}`;
        if (typeof value === 'string') return `${key}: ${value}`;
        return null;
      })
      .filter(Boolean);
    if (entries.length) return entries.join(' | ');
  }
  return fallback;
}
</script>

<style scoped>
.pz-contract-page {
  min-height: 100vh;
  background-color: var(--pz-color-limestone-white);
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
.pz-contract-hero {
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

.pz-contract-hero__media {
  position: relative;
  min-height: 24rem;
  overflow: hidden;
  background: linear-gradient(135deg, #e8e4db, #d4cfc5);
}

.pz-contract-hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.pz-contract-hero:hover .pz-contract-hero__image {
  transform: scale(1.03);
}

.pz-contract-hero__badges {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pz-contract-hero__content {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pz-contract-hero__description {
  max-width: 36rem;
  line-height: 1.6;
}

.pz-contract-hero__price {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  background: rgba(212, 101, 42, 0.06);
  border: 1px solid rgba(212, 101, 42, 0.12);
}

.pz-contract-hero__price strong {
  font-family: var(--pz-font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--pz-color-foundation-black);
  letter-spacing: -0.02em;
}

.pz-contract-workflow-banner {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.pz-contract-workflow-banner__summary {
  display: grid;
  gap: 0.45rem;
  min-width: 0;
}

.pz-contract-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-contract-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.2vw, 1.55rem);
  line-height: 1.2;
  color: var(--pz-color-foundation-black);
}

.pz-contract-workflow-banner__body {
  max-width: 70ch;
  color: var(--pz-color-structural-steel);
  line-height: 1.65;
}

.pz-contract-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.65rem;
}

.pz-contract-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.pz-contract-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  min-width: 0;
  padding: 0.9rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.86);
}

.pz-contract-workflow-step__index {
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

.pz-contract-workflow-step__content {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.pz-contract-workflow-step__content strong {
  font-size: 0.82rem;
  line-height: 1.3;
}

.pz-contract-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pz-contract-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
  background: rgba(250, 255, 252, 0.95);
}

.pz-contract-workflow-step--done .pz-contract-workflow-step__index {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
  color: #047857;
}

.pz-contract-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

/* Summary Grid */
.pz-contract-summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
}

.pz-contract-detail__metric {
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

.pz-contract-detail__label {
  font-family: var(--pz-font-mono);
  font-size: 0.64rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-detail__value {
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

/* Layout */
.pz-contract-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.75rem;
  margin-top: 2rem;
}

.pz-contract-sidebar {
  position: sticky;
  top: 2rem;
  align-self: start;
  height: fit-content;
  display: grid;
  gap: 1rem;
}

/* Tabs */
.pz-contract-tabs {
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

.pz-contract-tabs::-webkit-scrollbar {
  display: none;
}

.pz-contract-tab {
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

.pz-contract-tab:hover {
  color: var(--pz-color-structural-steel);
  background: rgba(10, 10, 15, 0.03);
}

.pz-contract-tab--active {
  background: white;
  color: var(--pz-color-earth-orange);
  box-shadow: 0 2px 8px rgba(10, 10, 15, 0.08);
}

.pz-contract-tab__badge {
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

/* Detail components */
.pz-detail-chip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(12rem, 1fr));
  gap: 0.75rem;
}

.pz-detail-chip {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-detail-chip span {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-detail-chip strong {
  font-family: var(--pz-font-display);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-detail-stack {
  display: grid;
  gap: 0.75rem;
}

.pz-detail-subcard {
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-detail-subcard h4 {
  margin: 0.25rem 0 0.15rem;
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 600;
}

.pz-detail-subcard p {
  margin: 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
  line-height: 1.5;
}

.pz-detail-subcard span:first-child {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-detail-subcard strong {
  display: block;
  margin-top: 0.15rem;
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
}

.pz-detail-card__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
  margin-bottom: 0.35rem;
}

.pz-contract-scope__text {
  margin: 0;
  color: var(--pz-color-structural-steel);
  line-height: 1.7;
  font-size: 0.95rem;
}

/* Bid card */
.pz-bid-card {
  padding: 1rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-bid-card__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.pz-bid-card__company {
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pz-bid-card__meta {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.15rem;
}

.pz-bid-card__price {
  font-family: var(--pz-font-display);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--pz-color-earth-orange);
  white-space: nowrap;
}

.pz-bid-card__message {
  margin: 0.75rem 0 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
  line-height: 1.5;
}

.pz-bid-card__footer {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.pz-bid-card__footer--status {
  justify-content: flex-start;
}

/* Milestone */
.pz-contract-milestone__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.pz-contract-milestone__top h4 {
  margin: 0 0 0.15rem;
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 600;
}

.pz-contract-milestone__top p {
  margin: 0;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-milestone__actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

/* Empty state */
.pz-contract-empty {
  padding: 1.5rem 0;
  text-align: center;
}

.pz-contract-empty__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.5rem;
}

.pz-contract-empty p {
  margin: 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
}

/* Bid status */
.pz-bid-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
}

/* Attachments */
.pz-detail-doc {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.pz-detail-doc:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(212, 101, 42, 0.2);
}

.pz-detail-doc strong {
  display: block;
  font-family: var(--pz-font-display);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.pz-detail-doc span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
}

.pz-contract-attachment__preview {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(10, 10, 15, 0.04);
  flex-shrink: 0;
}

.pz-contract-attachment__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pz-contract-attachment__placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

/* Confirm panel */
.pz-confirm-panel {
  text-align: center;
  padding: 1rem 0;
}

.pz-confirm-panel__title {
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 1.1rem;
  margin: 0 0 0.5rem;
}

.pz-confirm-panel__body {
  margin: 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Utilities */
.pz-l-flex { display: flex; }
.pz-l-flex--justify-between { justify-content: space-between; }
.pz-l-flex--align-start { align-items: flex-start; }
.pz-l-flex--align-center { align-items: center; }
.pz-l-flex--gap-2 { gap: 0.5rem; }
.pz-l-flex--gap-4 { gap: 1rem; }
.pz-l-flex--wrap { flex-wrap: wrap; }
.pz-l-flex--column { flex-direction: column; }

.pz-l-grid { display: grid; }
.pz-l-grid--cols-1 { grid-template-columns: 1fr; }
.pz-l-grid--md-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.pz-l-grid--gap-4 { gap: 1rem; }

.pz-space-y-1 > * + * { margin-top: 0.25rem; }
.pz-space-y-3 > * + * { margin-top: 0.75rem; }
.pz-space-y-4 > * + * { margin-top: 1rem; }
.pz-space-y-5 > * + * { margin-top: 1.25rem; }
.pz-space-y-6 > * + * { margin-top: 1.5rem; }

.pz-u-text-center { text-align: center; }
.pz-u-text-display { font-family: var(--pz-font-display); font-weight: 700; color: var(--pz-color-foundation-black); letter-spacing: -0.02em; line-height: 1.2; margin: 0; }
.pz-u-text-mono { font-family: var(--pz-font-mono); }
.pz-u-color-earth { color: var(--pz-color-earth-orange); }
.pz-u-color-steel { color: var(--pz-color-structural-steel); }
.pz-u-color-concrete { color: var(--pz-color-concrete-grey); }
.pz-u-mt-2 { margin-top: 0.5rem; }
.pz-u-mt-4 { margin-top: 1rem; }
.pz-u-mb-4 { margin-bottom: 1rem; }
.pz-u-mb-6 { margin-bottom: 1.5rem; }
.pz-u-mb-8 { margin-bottom: 2rem; }
.u-py-20 { padding-top: 5rem; padding-bottom: 5rem; }

.c-loader {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 2px solid rgba(10, 10, 15, 0.08);
  border-top-color: var(--pz-color-earth-orange);
  margin: 0 auto;
  animation: spin 1s linear infinite;
}

.c-alert {
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
}

.c-alert--danger {
  background: rgba(180, 35, 24, 0.08);
  border: 1px solid rgba(180, 35, 24, 0.2);
  color: #b42318;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .pz-contract-hero {
    grid-template-columns: 1fr;
  }
  .pz-contract-hero__media {
    min-height: 20rem;
    border-radius: 24px 24px 0 0;
  }
  .pz-contract-layout {
    grid-template-columns: 1fr;
  }
  .pz-contract-sidebar {
    position: static;
  }
  .pz-contract-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .pz-contract-hero__content {
    padding: 1.5rem;
  }
  .pz-contract-summary-grid {
    grid-template-columns: 1fr;
  }
  .pz-detail-chip-grid {
    grid-template-columns: 1fr;
  }

  .pz-contract-workflow-banner {
    grid-template-columns: 1fr;
  }

  .pz-contract-workflow-banner__actions {
    justify-content: flex-start;
  }

  .pz-contract-workflow-banner__steps {
    grid-template-columns: 1fr;
  }
}
</style>
