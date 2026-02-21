<template>
  <div class="pz-l-container u-py-12">
    <Card title="List a New Project" class="pz-auth-card u-mx-auto">
      <template #header>
        <div class="pz-u-text-center">
          <h2 class="pz-u-text-display u-mb-2">Strategic Asset Command</h2>
          <p class="pz-u-text-mono text-xs pz-u-color-steel">INITIALIZE NEW PROJECT PIPELINE</p>
        </div>
      </template>

      <form @submit.prevent="createProject" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <PzInput v-model="form.title" label="Asset Title" required />

        <div class="pz-input-wrapper">
          <label class="pz-input__label">Strategic Description</label>
          <textarea v-model="form.description" class="pz-input" rows="4" required></textarea>
        </div>

        <PzInput v-model="form.location" label="Operations Region" required />
        <PzInput v-model="form.estimated_budget" label="Estimated Valuation ($)" type="number" required />

        <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-border-radius-sm">
          <label class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 pz-u-text-mono text-sm cursor-pointer">
            <input type="checkbox" v-model="form.funding_required" />
            <span>OPEN FOR SYNDICATED FUNDING</span>
          </label>
        </div>

        <div class="u-mt-4">
          <Button type="submit" variant="primary" size="large" fullWidth :loading="submitting">
            {{ submitting ? 'INITIALIZING...' : 'INITIALIZE PROJECT' }}
          </Button>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import api from '../services/api';
  import { useRouter } from 'vue-router';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import PzInput from '../components/PzInput.vue';

  const router = useRouter();
  const submitting = ref(false);
  const form = ref({
    title: '',
    description: '',
    location: '',
    estimated_budget: 0,
    funding_required: false
  });

  async function createProject() {
    submitting.value = true;
    try {
      await api.post('/v4/projects/', form.value);
      // Could use a toast/modal, but alert is ok right now if no toast system
      alert('Project Successfully Initialized');
      router.push('/projects');
    } catch (err) {
      alert('Failed to initialize project');
    } finally {
      submitting.value = false;
    }
  }
</script>

<style scoped>
  .u-mx-auto {
    margin-left: auto;
    margin-right: auto;
  }
</style>
