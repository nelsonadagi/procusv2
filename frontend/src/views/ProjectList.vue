<template>
  <div class="pz-marketplace">
    <EntryHero
      v-model="searchQuery"
      search-only
      title="Search projects"
      placeholder="Search projects by title or location"
      search-label="Search Projects"
    />

    <div class="pz-l-container u-py-12">
      <!-- Unified Discovery Filters -->
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Operations Region</span>
            <select v-model="selectedLocation" class="pz-filter-bar__control">
              <option value="">All Regions</option>
              <option value="Nairobi">Nairobi</option>
              <option value="Coast">Coast</option>
              <option value="Western">Western</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Asset Lifecycle</span>
            <select v-model="selectedStatus" class="pz-filter-bar__control">
              <option value="">All States</option>
              <option value="PLANNING">Planning</option>
              <option value="ACTIVE">Under Construction</option>
              <option value="COMPLETED">Completed</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Valuation Range ({{ configStore.activeCurrency.symbol || '$' }})</span>
            <div class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-2">
              <input v-model.number="budgetMin" type="number" placeholder="MIN" class="pz-filter-bar__input">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">/</span>
              <input v-model.number="budgetMax" type="number" placeholder="MAX" class="pz-filter-bar__input">
            </div>
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
          <Button variant="ghost" size="sm" @click="clearFilters">RESET PORTFOLIO</Button>
        </div>
      </div>

      <div class="l-flex l-flex--justify-between l-flex--align-center u-mb-8">
        <h2 class="u-text-2xl u-font-bold">Featured Opportunities</h2>
        <Button variant="primary" @click="$router.push('/projects/new')">List New Project</Button>
      </div>

      <div v-if="loading" class="u-text-center u-py-20">
        <div class="loading-spinner"></div>
        <p class="u-mt-4 u-color-muted">Fetching project portfolio...</p>
      </div>
      <div v-else-if="filteredProjects.length" :class="viewMode === 'grid' ? 'pz-premium-grid' : 'pz-listing-list'">
        <article v-for="project in filteredProjects" :key="project.id" class="pz-premium-card"
          :class="{ 'pz-premium-card--list': viewMode === 'list' }" @click="$router.push(`/projects/${project.id}`)">

          <div class="pz-premium-card__media">
            <img :src="project.primary_image_url || '/placeholder.png'" :alt="project.title"
              class="pz-premium-card__img">
            <div class="pz-premium-card__badges">
              <Badge variant="default">{{ project.status }}</Badge>
              <Badge v-if="project.funding_required" variant="finance">FUNDING OPEN</Badge>
            </div>
          </div>

          <div class="pz-premium-card__content">
            <div class="pz-premium-card__top">
              <span class="pz-premium-card__vendor">{{ project.location }}</span>
              <div class="pz-premium-card__rating">NODE_#{{ project.id }}</div>
            </div>

            <h3 class="pz-premium-card__title">{{ project.title }}</h3>

            <div class="pz-premium-card__specs">
              <span class="pz-spec-dot">COMPLETION: {{ project.completion_percentage || '15%' }}</span>
              <span class="pz-spec-dot">SECURITY: SECURED</span>
            </div>

            <div class="pz-premium-card__pricing">
              <div class="pz-price-display">
                <span class="pz-price-display__unit">PROJECT VALUATION</span>
                <div class="pz-price-display__val">{{ configStore.formatPrice(project.estimated_budget) }}</div>
              </div>
              <Button variant="primary" size="sm">GO TO SITE</Button>
            </div>
          </div>
        </article>
      </div>
      <div v-else class="pz-u-text-center u-py-20 pz-u-border">
        <p class="pz-u-text-mono text-xs pz-u-color-concrete">No projects match the current search and filter selection.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue';
  import api from '../services/api';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import EntryHero from '../components/ui/EntryHero.vue';
  import { useConfigStore } from '../stores/config';

  const configStore = useConfigStore();
  const projects = ref([]);
  const loading = ref(true);
  const viewMode = ref('grid');
  const searchQuery = ref('');
  const selectedLocation = ref('');
  const selectedStatus = ref('');
  const budgetMin = ref(null);
  const budgetMax = ref(null);
  const filteredProjects = computed(() => {
    return projects.value.filter((project) => {
      const matchesSearch = !searchQuery.value || [project.title, project.location].some((value) =>
        String(value || '').toLowerCase().includes(searchQuery.value.toLowerCase())
      );
      const matchesLocation = !selectedLocation.value || String(project.location || '').toLowerCase().includes(selectedLocation.value.toLowerCase());
      const matchesStatus = !selectedStatus.value || project.status === selectedStatus.value;
      const budget = Number(project.estimated_budget || 0);
      const matchesBudgetMin = budgetMin.value === null || budget >= Number(budgetMin.value);
      const matchesBudgetMax = budgetMax.value === null || budget <= Number(budgetMax.value);
      return matchesSearch && matchesLocation && matchesStatus && matchesBudgetMin && matchesBudgetMax;
    });
  });
  const clearFilters = () => {
    searchQuery.value = '';
    selectedLocation.value = '';
    selectedStatus.value = '';
    budgetMin.value = null;
    budgetMax.value = null;
  };

  onMounted(async () => {
    try {
      const res = await api.get('/v4/projects/');
      projects.value = res.data.results || res.data;
    } catch (err) {
      console.error(err);
    } finally {
      loading.value = false;
    }
  });
</script>

<style scoped>

  /* Marketplace Global */
  .pz-marketplace {
    background-color: var(--pz-color-limestone-white);
    min-height: 100vh;
  }

  /* Marketplace Specific */
  .pz-marketplace {
    background-color: var(--pz-color-limestone-white);
    min-height: 100vh;
  }
</style>
