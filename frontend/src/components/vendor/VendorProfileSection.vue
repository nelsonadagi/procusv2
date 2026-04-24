<template>
  <div class="pz-profile-section">
    <div class="pz-admin-card pz-u-mb-8">
      <div class="pz-admin-card__header">
        <h3 class="pz-admin-card__title">OFFICIAL_REGISTRY_DATA</h3>
      </div>
      <form @submit.prevent="saveProfile" class="pz-p-6">
        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <PzInput v-model="form.business_name" label="BUSINESS_NAME" required />
          <PzInput v-model="form.registration_number" label="REGISTRATION_NO" required />
        </div>

        <!-- Advanced Map Integration via LocationInterface -->
        <div class="u-mt-8">
          <LocationInterface v-model="locationState" @change="handleLocationChange" />
        </div>

        <!-- Logistical Capabilities -->
        <div class="pz-divider u-my-8"></div>
        <h4 class="pz-u-text-mono text-sm font-bold u-mb-4">LOGISTICAL_CAPABILITIES</h4>

        <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
          <div class="pz-input-wrapper">
            <label class="pz-l-flex pz-l-flex--align-center pz-l-flex--gap-3 cursor-pointer">
              <input type="checkbox" v-model="form.provides_delivery" />
              <span class="pz-input__label">OFFER_DELIVERY_SERVICES</span>
            </label>
          </div>

          <PzInput v-if="form.provides_delivery" v-model.number="form.delivery_radius_km" label="DELIVERY_RADIUS (KM)"
            type="number" />
        </div>

        <!-- Industrial Specialization (Multi-category) -->
        <div class="u-mt-8">
          <label class="pz-input__label u-mb-4">INDUSTRIAL_SPECIALIZATION (CATEGORIES)</label>
          <div class="pz-category-chip-grid">
            <label v-for="cat in categories" :key="cat.id" class="pz-category-chip"
              :class="{ 'pz-category-chip--active': isCategorySelected(cat.name) }">
              <input type="checkbox" :value="cat.name" v-model="form.categories_served" class="u-sr-only" />
              {{ cat.name.toUpperCase() }}
            </label>
          </div>
        </div>

        <div class="u-mt-10 pz-l-flex pz-l-flex--justify-end">
          <Button type="submit" variant="primary" :loading="saving">UPDATE_PROFILE</Button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, inject, watch, nextTick } from 'vue';
  import api from '../../services/api';
  import { useConfigStore } from '../../stores/config';
  import PzInput from '../PzInput.vue';
  import Button from '../ui/Button.vue';
  import LocationInterface from '../ui/LocationInterface.vue';

  const configStore = useConfigStore();
  const form = ref({
    business_name: '',
    registration_number: '',
    country: null,
    location: '',
    latitude: null,
    longitude: null,
    formatted_address: '',
    location_hierarchy: {},
    provides_delivery: false,
    delivery_radius_km: 0,
    categories_served: []
  });

  const locationState = ref({
    lat: -1.2921,
    lng: 36.8219,
    address: '',
    city: '',
    country_id: null
  });

  const categories = ref([]);
  const saving = ref(false);

  const emit = defineEmits(['profile-updated']);
  const showAlert = inject('showAlert');

  async function fetchCategories() {
    try {
      const res = await api.get('/taxonomy/categories/');
      categories.value = res.data.results || res.data;
    } catch (err) {
      console.error("Categories fetch error", err);
    }
  }

  async function fetchProfile() {
    try {
      const res = await api.get('/vendors/me/');
      const data = res.data;
      Object.assign(form.value, data);

      // Seed location state
      locationState.value = {
        lat: parseFloat(data.latitude) || -1.2921,
        lng: parseFloat(data.longitude) || 36.8219,
        address: data.formatted_address || '',
        city: data.location || '',
        country_id: data.country
      };
    } catch (err) {
      console.error("Profile fetch error", err);
    }
  }

  function handleLocationChange(newLocation) {
    form.value.latitude = newLocation.lat;
    form.value.longitude = newLocation.lng;
    form.value.formatted_address = newLocation.address;
    form.value.location = newLocation.city;
    form.value.country = newLocation.country_id;
  }

  const isCategorySelected = (name) => {
    return Array.isArray(form.value.categories_served) && form.value.categories_served.includes(name);
  };

  async function saveProfile() {
    if (!form.value.country) {
      if (showAlert) showAlert("Please pinpoint your location on the map to resolve your Shop Country.", "warning");
      return;
    }

    saving.value = true;
    try {
      const res = await api.patch(`/vendors/${form.value.id}/`, form.value);
      if (showAlert) showAlert("Profile synchronized with global registry", "success");
      emit('profile-updated', res.data);
    } catch (err) {
      const msg = "Failed to update official profile";
      if (showAlert) showAlert(msg, "error");
    } finally {
      saving.value = false;
    }
  }

  onMounted(async () => {
    saving.value = true;
    try {
      await configStore.fetchConfig();
      await fetchCategories();
      await fetchProfile();
    } catch (err) {
      console.error("Initialization failed", err);
    } finally {
      saving.value = false;
    }
  });
</script>

<style scoped>
  .pz-admin-card {
    background: white;
    border: 1px solid var(--pz-color-foundation-black);
    box-shadow: 4px 4px 0 var(--pz-color-foundation-black);
  }

  .pz-admin-card__header {
    padding: var(--pz-space-4) var(--pz-space-6);
    border-bottom: 2px solid var(--pz-color-foundation-black);
    background: #f8fafc;
  }

  .pz-admin-card__title {
    font-family: var(--pz-font-mono);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.1em;
  }

  .pz-map-frame {
    height: 350px;
    width: 100%;
    border: 2px solid var(--pz-color-foundation-black);
    background: #eee;
    z-index: 10;
  }

  .pz-divider {
    height: 1px;
    background: rgba(0, 0, 0, 0.1);
    width: 100%;
  }

  .pz-category-chip-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .pz-category-chip {
    padding: 0.5rem 1rem;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    font-family: var(--pz-font-mono);
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
  }

  .pz-category-chip--active {
    background: var(--pz-color-earth-orange);
    color: white;
    border-color: var(--pz-color-foundation-black);
    box-shadow: 2px 2px 0 var(--pz-color-foundation-black);
  }

  .pz-category-chip:hover {
    border-color: var(--pz-color-foundation-black);
  }
</style>
