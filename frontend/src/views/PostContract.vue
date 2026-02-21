<template>
  <div class="pz-l-container u-py-12">
    <Card title="Post a New Contract" class="pz-auth-card u-mx-auto">
      <template #header>
        <div class="pz-u-text-center">
          <h2 class="pz-u-text-display u-mb-2">Procurement Engine</h2>
          <p class="pz-u-text-mono text-xs pz-u-color-steel">BROADCAST MAJOR WORKS TENDER</p>
        </div>
      </template>

      <form @submit.prevent="postContract" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-6">
        <PzInput v-model="form.title" label="Contract Specification" required />

        <div class="pz-input-wrapper">
          <label class="pz-input__label">Scope of Works</label>
          <textarea v-model="form.description_scope" class="pz-input" rows="4" required></textarea>
        </div>

        <PzInput v-model="form.location" label="Deployment Region" required />

        <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
          <PzInput v-model="form.budget_min" label="Min CapEx ($)" type="number" class="u-w-full" required />
          <PzInput v-model="form.budget_max" label="Max CapEx ($)" type="number" class="u-w-full" required />
        </div>

        <div class="u-mt-4">
          <Button type="submit" variant="primary" size="large" fullWidth :loading="submitting">
            {{ submitting ? 'BROADCASTING...' : 'BROADCAST TENDER' }}
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
    description_scope: '',
    location: '',
    budget_min: 0,
    budget_max: 0
  });

  async function postContract() {
    submitting.value = true;
    try {
      await api.post('/v2/contracts/', form.value);
      alert('Tender Broadcast Initiated!');
      router.push('/contracts');
    } catch (err) {
      console.error(err);
      alert('Failed to broadcast tender.');
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

  .u-w-full {
    width: 100%;
  }
</style>
