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
              <div class="pz-u-text-display text-lg pz-u-color-savanna">${{ contract.budget_min }} - ${{
                contract.budget_max }}</div>
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
                <div class="pz-u-text-mono text-xs pz-u-color-steel">DUE: {{ m.due_date }} • CAPITAL: ${{ m.amount }}
                </div>
              </div>
              <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-4">
                <Badge :variant="getMilestoneVariant(m.status)">{{ m.status }}</Badge>
                <Button v-if="isOwner && m.status === 'COMPLETED'" size="small" variant="finance"
                  @click="approveMilestone(m.id)">RELEASE FUNDS</Button>
                <Button v-if="isContractor && m.status === 'PENDING'" size="small" variant="primary">DEPLOY
                  WORK</Button>
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
                  <div class="font-bold text-xl">${{ bid.proposed_cost }}</div>
                  <div class="text-sm text-muted">{{ bid.proposed_timeline_days }} Days</div>
                </div>
              </div>
              <div class="mt-2 text-sm text-gray-600">{{ bid.message }}</div>
              <div class="mt-4 flex justify-end gap-2" v-if="bid.status === 'SUBMITTED'">
                <Button size="sm" variant="outline">Shortlist</Button>
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
            <PzInput label="Projected Expenditure ($)" type="number" v-model="bidForm.proposed_cost" required />
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
      <PzInput v-model="milestoneForm.amount" label="Amount" type="number" required />
      <PzInput v-model="milestoneForm.due_date" label="Due Date" type="date" required />
    </form>
    <template #footer>
      <Button variant="outline" @click="showAddMilestone = false">Cancel</Button>
      <Button type="submit" form="ms-form" variant="primary">Add</Button>
    </template>
  </Modal>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router';
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import Modal from '../components/ui/Modal.vue';
  import PzInput from '../components/PzInput.vue';

  const route = useRoute();
  const authStore = useAuthStore();
  const contract = ref(null);
  const bids = ref([]);
  const milestones = ref([]);
  const myBid = ref(null);
  const submittingBid = ref(false);
  const showAddMilestone = ref(false);

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

      // Milestones
      // Use 'nested' milestones if provided in serializer, or fetch active ones.
      // Assuming /milestones/?contract={id} works?
      // We didn't enable filtering for MilestoneViewSet.
      // But ContractSerializer might include 'milestones'.
      if (contract.value.milestones) {
        milestones.value = contract.value.milestones;
      }

    } catch (err) {
      console.error("Load failed", err);
    }
  }

  async function submitBid() {
    submittingBid.value = true;
    try {
      await api.post(`/contracts/${route.params.id}/bids/`, bidForm.value);
      alert('Bid submitted successfully!');
      loadContract();
    } catch (err) {
      alert('Bid submission failed');
    } finally {
      submittingBid.value = false;
    }
  }

  async function awardBid(bidId) {
    if (!confirm("Award contract to this bidder? This action cannot be undone.")) return;
    try {
      await api.post(`/bids/${bidId}/award/`);
      alert('Contract Awarded!');
      loadContract();
    } catch (err) {
      alert('Award failed');
    }
  }

  async function addMilestone() {
    try {
      await api.post(`/contracts/${route.params.id}/milestones/`, milestoneForm.value);
      showAddMilestone.value = false;
      loadContract(); // Refresh to see new milestone
    } catch (err) {
      alert('Failed to add milestone');
    }
  }

  async function approveMilestone(mId) {
    try {
      await api.post(`/milestones/${mId}/approve/`);
      // Refresh local state
      const m = milestones.value.find(x => x.id === mId);
      if (m) m.status = 'APPROVED';
    } catch (err) {
      alert('Approval failed');
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
</style>
