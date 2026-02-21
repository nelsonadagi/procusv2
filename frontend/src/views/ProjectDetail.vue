<template>
  <div class="pz-l-container u-py-8">
    <div v-if="loading" class="pz-l-flex pz-l-flex--center u-p-20 pz-l-flex--column">
      <div class="c-loader u-mb-4"></div>
      <p class="pz-u-text-mono">CONSULTING PROJECT BLUEPRINTS...</p>
    </div>

    <div v-else-if="project" class="pz-space-y-12">
      <!-- Premium Breadcrumb -->
      <nav class="pz-breadcrumb pz-u-text-mono text-xs">
        <router-link to="/projects" class="pz-breadcrumb__item">PROJECT PORTFOLIO</router-link>
        <span class="pz-breadcrumb__separator">//</span>
        <span class="pz-breadcrumb__current pz-u-color-steel">{{ project.title }}</span>
      </nav>

      <div class="pz-l-dashboard">
        <!-- Left: Project Gallery and Details -->
        <div class="pz-space-y-8">
          <div class="pz-gallery-section">
            <div class="pz-gallery__main pz-u-border">
              <img :src="selectedImage || project.primary_image_url || '/placeholder.png'" :alt="project.title"
                class="pz-gallery__image">
              <div class="pz-gallery__badges">
                <Badge variant="savanna" size="large">{{ project.status }}</Badge>
                <Badge v-if="project.funding_required" variant="finance" size="large">FUNDING ACTIVE</Badge>
              </div>
            </div>

            <div v-if="project.images && project.images.length > 1"
              class="pz-l-grid pz-l-grid--cols-6 pz-l-grid--gap-4 u-mt-4">
              <div v-for="img in project.images" :key="img.id" class="pz-u-border pz-p-1"
                :class="{ 'pz-u-border-earth': selectedImage === img.image_url }"
                @click="selectedImage = img.image_url">
                <img :src="img.image_url" :alt="project.title" class="u-w-full u-h-full u-object-cover">
              </div>
            </div>
          </div>

          <!-- Project Description -->
          <Card title="Blueprint Overview">
            <p class="pz-u-text-mono text-sm pz-u-color-steel u-line-height-relaxed">{{ project.description }}</p>
          </Card>

          <!-- Requirements Section -->
          <Card title="Asset Requirements">
            <template #header>
              <Badge v-if="isOwner" variant="earth">ADMINISTRATIVE VIEW</Badge>
            </template>

            <div class="pz-space-y-4">
              <div v-for="req in project.requirements" :key="req.id"
                class="pz-u-bg-limestone pz-u-border pz-p-4 pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center">
                <div>
                  <span class="pz-u-text-mono text-xs pz-u-color-earth u-block u-mb-1">{{ req.type }}</span>
                  <span class="pz-u-text-display text-lg">{{ req.description }}</span>
                </div>
                <div class="u-text-right">
                  <span class="pz-u-text-mono text-xs pz-u-color-steel u-block">REQUIRED VOLUME</span>
                  <span class="pz-u-text-display text-xl">{{ req.quantity }}</span>
                </div>
              </div>
            </div>

            <div v-if="isOwner" class="pz-u-bg-limestone pz-p-6 u-mt-6 pz-u-border">
              <h4 class="pz-u-text-mono text-xs u-mb-4">ADD NEW REQUIREMENT</h4>
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
                <select v-model="newReq.type" class="pz-input">
                  <option value="MATERIAL">MATERIAL</option>
                  <option value="CONTRACTOR">CONTRACTOR</option>
                  <option value="SERVICE">SERVICE</option>
                </select>
                <input v-model="newReq.description" placeholder="DESCRIPTION" class="pz-input">
                <input v-model="newReq.quantity" placeholder="QTY" class="pz-input">
              </div>
              <Button variant="primary" size="small" class="u-mt-4" @click="addRequirement">PROVISION
                REQUIREMENT</Button>
            </div>
          </Card>
        </div>

        <!-- Right: Action & Status Column -->
        <div class="pz-space-y-8">
          <Card title="Strategic Status">
            <div class="pz-space-y-6">
              <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">DEPLOYMENT ZONE</span>
                <span class="pz-u-text-display">{{ project.location }}</span>
              </div>
              <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">EST. CAPITAL</span>
                <span class="pz-u-text-display pz-u-color-earth">${{ project.estimated_budget }}</span>
              </div>
              <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-end">
                <span class="pz-u-text-mono text-xs pz-u-color-concrete">CURRENT PHASE</span>
                <Badge variant="savanna">{{ project.status }}</Badge>
              </div>
            </div>

            <div v-if="project.funding_required" class="pz-u-border-t u-mt-6 u-pt-6">
              <h4 class="pz-u-text-mono text-xs u-mb-4">FUNDING PROGRESS</h4>
              <div class="pz-u-border pz-p-1 u-mb-4">
                <div class="u-h-2 pz-u-bg-limestone">
                  <div class="u-h-full pz-u-bg-earth" style="width: 45%;"></div>
                </div>
              </div>
              <div class="pz-l-flex pz-l-flex--justify-between pz-u-text-mono text-xs">
                <span>$450K COMMITTED</span>
                <span>TARGET: $1M</span>
              </div>

              <div v-if="!isOwner" class="u-mt-6 pz-space-y-4">
                <PzInput label="Commitment Amount ($)" type="number" v-model="pledgeAmount" />
                <Button variant="primary" fullWidth @click="pledge">COMMIT CAPITAL</Button>
              </div>
            </div>
          </Card>

          <!-- Execution Team -->
          <Card v-if="isOwner" title="Execution Team">
            <div v-if="project.linked_contracts && project.linked_contracts.length" class="pz-space-y-3">
              <div v-for="c in project.linked_contracts" :key="c.id"
                class="pz-u-border pz-p-3 pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3">
                <span class="u-text-xl">📄</span>
                <div>
                  <span class="pz-u-text-mono text-xs u-block">CONTRACT #{{ c.id }}</span>
                  <span class="pz-u-text-display text-sm">AWARDED: {{ c.contractor_name }}</span>
                </div>
              </div>
            </div>
            <div v-else class="pz-u-bg-limestone pz-p-4 pz-u-text-center">
              <p class="pz-u-text-mono text-xs pz-u-color-steel">NO CONTRACTS AWARDED</p>
            </div>

            <div class="u-mt-6 pz-u-border-t u-pt-6">
              <PzInput label="Link Contract ID" v-model="contractIdToLink" />
              <Button variant="outline" size="small" fullWidth class="u-mt-4" @click="linkContract">LINK
                DEPLOYMENT</Button>
            </div>
          </Card>
        </div>
      </div>

      <!-- Timeline & Updates -->
      <Card title="Execution Timeline">
        <div class="pz-timeline">
          <div v-for="upd in project.updates" :key="upd.id" class="pz-timeline__item">
            <div class="pz-timeline__marker"></div>
            <div class="pz-timeline__content pz-u-border">
              <div class="pz-l-flex pz-l-flex--justify-between u-mb-2">
                <span class="pz-u-text-display text-sm">{{ upd.posted_by }}</span>
                <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ new Date(upd.created_at).toLocaleDateString()
                  }}</span>
              </div>
              <p class="pz-u-text-mono text-xs pz-u-color-concrete">{{ upd.update_text }}</p>
            </div>
          </div>

          <div v-if="isOwner" class="pz-u-bg-limestone pz-p-6 u-mt-8 pz-u-border">
            <h4 class="pz-u-text-mono text-xs u-mb-4">BROADCAST UPDATE</h4>
            <textarea v-model="updateText" class="pz-input u-w-full u-mb-4" rows="3"
              placeholder="SHARE DEVELOPMENT PROGRESS..."></textarea>
            <Button variant="primary" size="small" @click="postUpdate">POST UPDATE</Button>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import api from '../services/api';

  // UI Components
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';

  const route = useRoute();
  const project = ref(null);
  const loading = ref(true);
  const isOwner = ref(true);
  const selectedImage = ref(null);

  // Forms
  const newReq = ref({ type: 'MATERIAL', description: '', quantity: '' });
  const pledgeAmount = ref(0);
  const contractIdToLink = ref('');
  const updateText = ref('');

  const loadProject = async () => {
    loading.value = true;
    try {
      const res = await api.get(`/v4/projects/${route.params.id}/`);
      project.value = res.data;
      if (project.value.primary_image_url) selectedImage.value = project.value.primary_image_url;
    } catch (err) {
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  async function addRequirement() {
    await api.post(`/v4/projects/${project.value.id}/requirements/`, newReq.value);
    newReq.value = { type: 'MATERIAL', description: '', quantity: '' };
    loadProject();
  }

  async function pledge() {
    if (pledgeAmount.value <= 0) return alert('Enter a valid amount');
    await api.post(`/v4/projects/${project.value.id}/commit/`, { amount_committed: pledgeAmount.value });
    alert('Project commitment recorded successfully!');
    pledgeAmount.value = 0;
    loadProject();
  }

  async function linkContract() {
    if (!contractIdToLink.value) return;
    await api.post(`/v4/projects/${project.value.id}/link-contract/`, { contract_id: contractIdToLink.value });
    contractIdToLink.value = '';
    loadProject();
  }

  async function postUpdate() {
    if (!updateText.value) return;
    await api.post(`/v4/projects/${project.value.id}/updates/`, { update_text: updateText.value });
    updateText.value = '';
    loadProject();
  }

  onMounted(loadProject);
</script>

<style scoped>
  .pz-breadcrumb__item {
    color: var(--pz-color-earth-orange);
    text-decoration: none;
  }

  .pz-breadcrumb__separator {
    color: var(--pz-color-concrete-grey);
  }

  .pz-gallery__main {
    position: relative;
    aspect-ratio: 16/9;
    background: var(--pz-color-limestone-white);
    overflow: hidden;
  }

  .pz-gallery__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .pz-gallery__badges {
    position: absolute;
    top: var(--pz-space-4);
    left: var(--pz-space-4);
    display: flex;
    flex-direction: column;
    gap: var(--pz-space-2);
  }

  .pz-timeline {
    position: relative;
    padding-left: var(--pz-space-8);
    border-left: 1px solid var(--pz-color-limestone-white);
  }

  .pz-timeline__item {
    position: relative;
    padding-bottom: var(--pz-space-10);
  }

  .pz-timeline__marker {
    position: absolute;
    left: -37px;
    top: 0;
    width: 10px;
    height: 10px;
    background: var(--pz-color-earth-orange);
  }

  .pz-timeline__content {
    background: var(--pz-color-limestone-white);
    padding: var(--pz-space-4);
  }
</style>
