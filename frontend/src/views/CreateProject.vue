<template>
  <div class="pz-l-container u-py-12">
    <Card title="List a New Project" class="pz-auth-card u-mx-auto">
      <template #header>
        <div class="pz-u-text-center">
          <h2 class="pz-u-text-display u-mb-2">Project Creation</h2>
          <p class="pz-u-text-mono text-xs pz-u-color-steel">Fill in the details for your new construction project</p>
        </div>
      </template>

      <form @submit.prevent="createProject" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <PzInput v-model="form.title" label="Project Title" required />

        <div class="pz-input-wrapper">
          <label class="pz-input__label">Project Description</label>
          <textarea v-model="form.description" class="pz-input" rows="4" required></textarea>
        </div>

        <div class="pz-location-section">
           <label class="pz-input__label u-mb-2">Project Location</label>
           <LocationInterface v-model="locationState" @change="handleLocationChange" />
        </div>

        <PzInput v-model="form.estimated_budget" label="Estimated Budget ($)" type="number" required />

        <div class="pz-u-bg-limestone pz-p-4 pz-u-border pz-border-radius-sm">
          <label class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 pz-u-text-mono text-sm cursor-pointer">
            <input type="checkbox" v-model="form.funding_required" />
            <span>Open for syndicated funding</span>
          </label>
        </div>

        <div class="u-mt-4">
          <Button type="submit" variant="primary" size="large" fullWidth :loading="submitting">
            {{ submitting ? 'Creating...' : 'Create Project' }}
          </Button>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup>
  import { inject, ref } from 'vue';
  import api from '../services/api';
  import { useRouter } from 'vue-router';
  import Card from '../components/ui/Card.vue';
  import Button from '../components/ui/Button.vue';
  import PzInput from '../components/PzInput.vue';
  import LocationInterface from '../components/ui/LocationInterface.vue';

  const router = useRouter();
  const showAlert = inject('showAlert');
  const submitting = ref(false);
  const form = ref({
    title: '',
    description: '',
    latitude: null,
    longitude: null,
    formatted_address: '',
    location_text: '',
    country: null,
    estimated_budget: 0,
    funding_required: false
  });

  const locationState = ref({
    lat: -1.2921,
    lng: 36.8219,
    address: '',
    city: '',
    country_id: null
  });

  function handleLocationChange(loc) {
    form.value.latitude = loc.lat;
    form.value.longitude = loc.lng;
    form.value.formatted_address = loc.address;
    form.value.location_text = loc.city;
    form.value.country = loc.country_id;
  }

  async function createProject() {
    submitting.value = true;
    try {
      await api.post('/v4/projects/', form.value);
      showAlert('Project initialized successfully.', 'success');
      router.push('/projects');
    } catch (err) {
      showAlert(err.response?.data?.detail || 'Failed to initialize project.', 'error');
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
