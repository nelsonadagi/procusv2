<template>
  <div class="pz-marketplace">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Search tenders"
      placeholder="Search tender opportunities"
      search-label="Search Tenders"
    />

    <main class="pz-l-container u-py-12">
      <WorkflowGuide title="Tender CTA" eyebrow="Action">
        <ModuleCTA
          eyebrow="Tender Participation"
          title="Want to publish work or bid as a contractor?"
          body="Post a tender when you need delivery partners, or complete contractor onboarding before responding to open opportunities."
          primary-label="Post Tender"
          primary-to="/contracts/new"
          secondary-label="Contractor Onboarding"
          secondary-to="/contractors/register"
          tone="savanna"
        />
      </WorkflowGuide>

      <!-- Unified Discovery Filters -->
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Tender Status</span>
            <select v-model="selectedStatus" class="pz-filter-bar__control">
              <option value="">All Tenders</option>
              <option value="OPEN">Open</option>
              <option value="CLOSED">Closed/Bidding</option>
              <option value="AWARDED">Awarded</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Deployment Zone</span>
            <select v-model="selectedLocation" class="pz-filter-bar__control">
              <option value="">All Regions</option>
              <option value="Nairobi">Nairobi</option>
              <option value="Mombasa">Mombasa</option>
              <option value="Kisumu">Kisumu</option>
            </select>
          </div>
        </div>

        <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
          <div class="pz-view-switcher u-hide-mobile">
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'grid' }"
              @click="viewMode = 'grid'">
              ⣿
            </button>
            <button class="pz-view-switcher__btn" :class="{ 'pz-view-switcher__btn--active': viewMode === 'list' }"
              @click="viewMode = 'list'">
              ≡
            </button>
          </div>
          <Button variant="ghost" size="sm" @click="clearFilters">RESET PARAMETERS</Button>
        </div>
      </div>

      <div v-if="loading" class="pz-l-flex pz-l-flex--center u-py-20 pz-l-flex--column">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">SYNCHRONIZING TENDER REGISTRY...</p>
      </div>

      <div v-else-if="filteredTenders.length > 0" :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
        <div v-for="tender in filteredTenders" :key="tender.id" class="pz-premium-card">
          <div class="pz-premium-card__media">
            <img :src="tender.featured_image_url || '/placeholder.png'" :alt="tender.title"
              class="pz-premium-card__img">
            <div class="pz-premium-card__badges">
              <Badge variant="savanna">{{ tender.status }}</Badge>
            </div>
          </div>
          <div class="pz-premium-card__content">
            <div class="pz-premium-card__top">
              <span class="pz-premium-card__vendor">{{ tender.location }}</span>
              <div class="pz-premium-card__rating">ID_#{{ tender.id }}</div>
            </div>

            <h3 class="pz-premium-card__title">{{ tender.title }}</h3>

            <div class="pz-premium-card__specs">
              <span class="pz-spec-dot">SECTOR: {{ tender.sector || 'INFRA' }}</span>
              <span class="pz-spec-dot">DUE: 48H</span>
            </div>

            <p class="pz-u-text-mono text-xs pz-u-color-concrete u-line-clamp-2 u-mb-6" style="height: 3em;">
              {{ tender.description_scope }}
            </p>

            <div class="pz-premium-card__pricing">
              <div class="pz-price-display">
                <span class="pz-price-display__unit">BUDGET RANGE</span>
                <div class="pz-price-display__val">{{ configStore.formatPrice(tender.budget_min, tender.currency || 'KES') }} - {{
                  configStore.formatPrice(tender.budget_max, tender.currency || 'KES') }}</div>
              </div>
              <Button @click="bid(tender.id)" variant="primary" size="sm">EXECUTE BID</Button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 text-muted">
        No active tenders found matching your criteria.
      </div>
    </main>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRouter } from 'vue-router';
  const viewMode = ref('grid');
  import api from '../services/api';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import EntryHero from '../components/ui/EntryHero.vue';
  import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
  import ModuleCTA from '../components/ui/ModuleCTA.vue';
  import { useAuthStore } from '../stores/auth';
  import { useConfigStore } from '../stores/config';

  const router = useRouter();
  const authStore = useAuthStore();
  const configStore = useConfigStore();
  const tenders = ref([]);
  const loading = ref(true);
  const searchQuery = ref('');
  const selectedStatus = ref('');
  const selectedLocation = ref('');
  const budgetMin = ref(null);
  const budgetMax = ref(null);
  const filteredTenders = computed(() => {
    return tenders.value.filter((tender) => {
      const matchesSearch = !searchQuery.value || [tender.title, tender.description_scope, tender.location].some((value) =>
        String(value || '').toLowerCase().includes(searchQuery.value.toLowerCase())
      );
      const matchesStatus = !selectedStatus.value || tender.status === selectedStatus.value;
      const matchesLocation = !selectedLocation.value || String(tender.location || '').toLowerCase().includes(selectedLocation.value.toLowerCase());
      return matchesSearch && matchesStatus && matchesLocation;
    });
  });
  const clearFilters = () => {
    searchQuery.value = '';
    selectedStatus.value = '';
    selectedLocation.value = '';
    budgetMin.value = null;
    budgetMax.value = null;
  };

  onMounted(async () => {
    try {
      // Fetch contracts with status POSTED or BIDDING
      // Backend ContractViewSet allows listing. 
      // We might need to filter status=POSTED in query params if it returns all.
      const res = await api.get('/contracts/?status=POSTED');
      tenders.value = res.data.results || res.data;
    } catch (err) {
      console.error("Failed to load tenders", err);
    } finally {
      loading.value = false;
    }
  });

  const bid = (id) => {
    if (!authStore.isAuthenticated) {
      router.push('/login?redirect=/tenders');
      return;
    }
    router.push(`/contracts/${id}`);
  };
</script>

<style scoped>
  .u-line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
