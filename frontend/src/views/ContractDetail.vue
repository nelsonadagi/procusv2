<template>
  <div class="pz-l-container u-py-8" v-if="contract">
    <!-- Header -->
    <header class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start u-mb-10">
      <div>
        <button @click="$router.back()" class="pz-u-text-mono text-xs pz-u-color-steel u-mb-2 hover:pz-u-color-earth">
          &larr; RETURN TO MARKET
        </button>
        <h1 class="pz-u-text-display text-4xl">{{ contract.title }}</h1>
        <div class="pz-u-text-mono text-xs pz-u-color-concrete mt-1">ASSET DEPLOYMENT ID: {{ contract.id }}</div>
      </div>
      <Badge :variant="getContractStatusVariant(contract.status)">{{ contract.status }}</Badge>
    </header>

    <div class="pz-l-dashboard">
      <!-- Main Details -->
      <div class="pz-space-y-8">
        <div class="pz-u-border u-mb-8">
          <div class="pz-gallery__main">
            <img :src="contract.featured_image_url || '/placeholder.png'" :alt="contract.title"
              class="pz-gallery__image">
          </div>
        </div>

        <Card title="Operational Scope">
          <div class="pz-u-text-mono text-sm pz-u-color-steel u-mb-6 whitespace-pre-line">
            {{ contract.description_scope }}
          </div>
          <div class="pz-l-grid pz-l-grid--cols-2 pz-l-grid--gap-6 pz-u-border-t pz-pt-6">
            <div>
              <div class="pz-u-text-mono text-xs pz-u-color-concrete">DEPLOYMENT LOCATION</div>
              <div class="pz-u-text-display text-lg">{{ contract.location }}</div>
            </div>
            <div>
              <div class="pz-u-text-mono text-xs pz-u-color-concrete">PROJECTED BUDGET</div>
              <div class="pz-u-text-display text-lg pz-u-color-savanna">{{ configStore.formatPrice(contract.budget_min)
                }} - {{
                  configStore.formatPrice(contract.budget_max) }}</div>
            </div>
          </div>
        </Card>

        <!-- MILESTONES -->
        <Card title="Execution Milestones" v-if="contract.status === 'AWARDED' || contract.status === 'IN_PROGRESS'">
          <template #header>
            <Button v-if="isOwner" size="sm" variant="outline" @click="showAddMilestone = true">+ PROVISION
              MILESTONE</Button>
          </template>

          <div v-if="milestones.length === 0" class="pz-u-text-mono text-xs pz-u-color-concrete italic">NO MILESTONES
            REGISTERED
          </div>
          <div v-else class="pz-space-y-4">
            <div v-for="m in milestones" :key="m.id"
              class="pz-u-border pz-p-4 pz-u-bg-limestone pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
              <div>
                <div class="pz-u-text-display">{{ m.title }}</div>
                <div class="pz-u-text-mono text-xs pz-u-color-steel">DUE: {{ m.due_date }} • CAPITAL: {{
                  configStore.formatPrice(m.amount) }}
                </div>
              </div>
              <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
                <Badge :variant="getMilestoneVariant(m.status)">{{ m.status }}</Badge>
                <Button v-if="isOwner && m.status === 'COMPLETED'" size="small" variant="finance"
                  @click="approveMilestone(m.id)">RELEASE FUNDS</Button>
                <Button v-if="isContractor && m.status === 'PENDING'" size="small" variant="primary">DEPLOY
                  WORK</Button>
                <Button size="small" variant="outline" @click="openChat">Chat</Button>
              </div>
            </div>
          </div>
        </Card>

        <!-- OWNER: BIDS REVIEW -->
        <Card title="Received Bids" v-if="isOwner && (contract.status === 'POSTED' || contract.status === 'BIDDING')">
          <div v-if="bids.length === 0" class="text-muted">No bids received yet.</div>
          <div v-else class="space-y-4">
            <div v-for="bid in bids" :key="bid.id" class="border p-4 rounded hover:bg-gray-50">
              <div class="flex justify-between">
                <div class="font-bold">{{ bid.contractor?.company_name || 'Contractor' }}</div>
                <div class="text-right">
                  <div class="font-bold text-xl">{{ configStore.formatPrice(bid.proposed_cost) }}</div>
                  <div class="text-sm text-muted">{{ bid.proposed_timeline_days }} Days</div>
                </div>
              </div>
              <div class="mt-2 text-sm text-gray-600">{{ bid.message }}</div>
              <div class="mt-4 flex justify-end gap-2" v-if="bid.status === 'SUBMITTED'">
                <Button size="sm" variant="outline" :loading="shortlistingBidId === bid.id" @click="shortlistBid(bid.id)">Shortlist</Button>
                <Button size="sm" variant="primary" @click="awardBid(bid.id)">Award Contract</Button>
              </div>
              <div v-else class="mt-2 text-right">
                <Badge>{{ bid.status }}</Badge>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Sidebar Actions -->
      <div class="pz-space-y-6">
        <Card title="Operational Command" v-if="canBid" class="u-sticky u-top-24">
          <form @submit.prevent="submitBid" class="pz-space-y-6">
            <PzInput :label="`Projected Expenditure (${configStore.activeCurrency.symbol})`" type="number"
              v-model="bidForm.proposed_cost" required />
            <PzInput label="Deployment Duration (Days)" type="number" v-model="bidForm.proposed_timeline_days"
              required />

            <div class="pz-input-wrapper">
              <label class="pz-input__label">Strategic Proposal</label>
              <textarea v-model="bidForm.message" class="pz-input" rows="4"
                placeholder="OUTLINE COMPETITIVE ADVANTAGE..."></textarea>
            </div>

            <Button type="submit" variant="primary" fullWidth :loading="submittingBid">SUBMIT PROPOSAL</Button>
          </form>
        </Card>

        <Card v-if="isContractor && hasBid" title="Your Bid Status">
          <div class="text-center py-4">
            <Badge size="lg" :variant="getBidStatusVariant(myBid.status)">{{ myBid.status }}</Badge>
            <p class="mt-2 text-sm text-muted">Submitted on {{ new Date(myBid.created_at).toLocaleDateString() }}</p>
          </div>
        </Card>

        <div v-if="isOwner">
          <Card title="Management">
            <p class="text-sm text-muted mb-4">Manage this project lifecycle.</p>
            <Button block variant="danger" disabled>Close Bidding</Button>
          </Card>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex justify-center p-12">
    <div class="spinner"></div>
  </div>

  <!-- Add Milestone Modal -->
  <Modal :isOpen="showAddMilestone" title="Add Milestone" size="md" @close="showAddMilestone = false">
    <form id="ms-form" @submit.prevent="addMilestone" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
      <PzInput v-model="milestoneForm.title" label="Title" required />
      <PzInput v-model="milestoneForm.amount" :label="`Amount (${configStore.activeCurrency.symbol})`" type="number"
        required />
      <PzInput v-model="milestoneForm.due_date" label="Due Date" type="date" required />
    </form>
    <template #footer>
      <Button variant="outline" @click="showAddMilestone = false">Cancel</Button>
      <Button type="submit" form="ms-form" variant="primary">Add</Button>
    </template>
  </Modal>

  <!-- Chat Modal -->
  <Modal :isOpen="showChatModal" title="CONTRACT_OPERATIONS_CHAT" size="lg" @close="showChatModal = false">
    <ChatWindow v-if="activeChatRoomId" :roomId="String(activeChatRoomId)" />
  </Modal>

  <Modal :isOpen="showAwardConfirm" title="AWARD_CONTRACT" size="sm" @close="closeAwardConfirm">
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
</template>

<script setup>
  import { ref, onMounted, computed, inject } from 'vue';
  import { useRoute } from 'vue-router';
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';
  import { useConfigStore } from '../stores/config';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import Modal from '../components/ui/Modal.vue';
  import PzInput from '../components/PzInput.vue';
  import ChatWindow from '../components/chat/ChatWindow.vue';

  const route = useRoute();
  const authStore = useAuthStore();
  const configStore = useConfigStore();
  const showAlert = inject('showAlert');
  const contract = ref(null);
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

  const bidForm = ref({ proposed_cost: null, proposed_timeline_days: null, message: '' });
  const milestoneForm = ref({ title: '', amount: null, due_date: '' });

  const isOwner = computed(() => contract.value && authStore.user?.id === contract.value.owner);
  const isContractor = computed(() => authStore.hasRole('CONTRACTOR'));
  const hasBid = computed(() => !!myBid.value);
  const canBid = computed(() => isContractor.value && !hasBid.value && (contract.value?.status === 'POSTED' || contract.value?.status === 'BIDDING'));

  onMounted(async () => {
    loadContract();
  });

  async function loadContract() {
    const id = route.params.id;
    try {
      bids.value = [];
      milestones.value = [];
      myBid.value = null;
      const res = await api.get(`/contracts/${id}/`);
      contract.value = res.data;

      if (isOwner.value) {
        // Owner sees all
        const bidsRes = await api.get(`/contracts/${id}/bids/`);
        bids.value = bidsRes.data;
      } else if (isContractor.value) {
        // Contractor checks if they already bid
        // The API /contracts/{id}/bids/ for non-owner returns THEIR bids only (filtered in backend)
        // Or 403?
        // "ContractViewSet: if hasattr(request.user, 'contractor_profile'): bids = contract.bids.filter(contractor=...)"
        // So we can fetch bids endpoint to see our bid.
        try {
          const myBidsRes = await api.get(`/contracts/${id}/bids/`);
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
          const milestonesRes = await api.get(`/contracts/${id}/milestones/`);
          milestones.value = milestonesRes.data;
        } catch (e) {
          milestones.value = [];
        }
      }

    } catch (err) {
      console.error("Load failed", err);
    }
  }

  async function submitBid() {
    submittingBid.value = true;
    try {
      await api.post(`/contracts/${route.params.id}/bids/`, bidForm.value);
      showAlert('Bid submitted successfully.', 'success');
      loadContract();
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Bid submission failed.', 'error');
    } finally {
      submittingBid.value = false;
    }
  }

  async function shortlistBid(bidId) {
    shortlistingBidId.value = bidId;
    try {
      await api.post(`/bids/${bidId}/shortlist/`);
      showAlert('Bid shortlisted successfully.', 'success');
      loadContract();
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
      await api.post(`/bids/${pendingAwardBidId.value}/award/`);
      showAlert('Contract awarded successfully.', 'success');
      closeAwardConfirm();
      loadContract();
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Award failed.', 'error');
    } finally {
      awardingBid.value = false;
    }
  }

  async function addMilestone() {
    try {
      await api.post(`/contracts/${route.params.id}/milestones/`, milestoneForm.value);
      showAddMilestone.value = false;
      milestoneForm.value = { title: '', amount: null, due_date: '' };
      showAlert('Milestone added successfully.', 'success');
      loadContract(); // Refresh to see new milestone
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to add milestone.', 'error');
    }
  }

  async function approveMilestone(mId) {
    try {
      await api.post(`/milestones/${mId}/approve/`);
      showAlert('Milestone approved and funds released.', 'success');
      loadContract();
    } catch (err) {
      showAlert(err.response?.data?.detail || err.response?.data?.error || 'Approval failed.', 'error');
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
</script>

<style scoped>
  .layout-grid {
    display: grid;
  }

  .spinner {
    box-sizing: border-box;
    border: 4px solid var(--color-border);
    border-top: 4px solid var(--color-primary);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(360deg);
    }
  }

  .pz-confirm-panel__title {
    margin: 0;
    font-weight: 700;
    line-height: 1.5;
  }

  .pz-confirm-panel__body {
    margin: 0.75rem 0 0;
    color: var(--pz-color-text-secondary);
    line-height: 1.6;
  }
</style>
