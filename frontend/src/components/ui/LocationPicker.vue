<template>
  <div class="location-picker-container">
    <div class="search-overlay">
      <input 
        v-model="searchQuery" 
        placeholder="Search for a location..." 
        class="search-input"
        @keydown.enter.prevent="searchLocation"
      />
      <button class="search-btn" @click.prevent="searchLocation">Search</button>
    </div>
    <div ref="mapContainer" class="map-container"></div>
    <div class="location-details" v-if="localLocation.address">
      <p class="text-sm font-medium">{{ localLocation.address }}</p>
      <p class="text-xs text-slate-500">{{ localLocation.lat.toFixed(6) }}, {{ localLocation.lng.toFixed(6) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ lat: -1.2921, lng: 36.8219, address: '' })
  },
  height: {
    type: String,
    default: '400px'
  }
});

const emit = defineEmits(['update:modelValue', 'locationSelect']);

const mapContainer = ref(null);
const map = ref(null);
const marker = ref(null);
const searchQuery = ref('');
const localLocation = ref({ ...props.modelValue });

const initMap = () => {
  if (!mapContainer.value) return;

  // Default to Nairobi if no coords
  const lat = localLocation.value.lat || -1.2921;
  const lng = localLocation.value.lng || 36.8219;

  map.value = L.map(mapContainer.value).setView([lat, lng], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value);

  marker.value = L.marker([lat, lng], {
    draggable: true
  }).addTo(map.value);

  marker.value.on('dragend', (event) => {
    const { lat, lng } = event.target.getLatLng();
    updateLocation(lat, lng);
  });

  map.value.on('click', (event) => {
    const { lat, lng } = event.latlng;
    updateLocation(lat, lng);
  });
};

const updateLocation = async (lat, lng) => {
  localLocation.value.lat = lat;
  localLocation.value.lng = lng;
  marker.value.setLatLng([lat, lng]);
  map.value.panTo([lat, lng]);

  // Reverse Geocoding via Nominatim
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
    const data = await response.json();
    localLocation.value.address = data.display_name;
    localLocation.value.city = data.address.city || data.address.town || data.address.village;
    localLocation.value.country_code = data.address.country_code;
  } catch (error) {
    console.error('Geocoding error:', error);
  }

  emit('update:modelValue', localLocation.value);
  emit('locationSelect', localLocation.value);
};

const searchLocation = async () => {
  if (!searchQuery.value) return;
  
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}`);
    const data = await response.json();
    if (data && data.length > 0) {
      const { lat, lon } = data[0];
      updateLocation(parseFloat(lat), parseFloat(lon));
    }
  } catch (error) {
    console.error('Search error:', error);
  }
};

onMounted(() => {
  initMap();
});

watch(() => props.modelValue, (newVal) => {
  if (newVal && (newVal.lat !== localLocation.value.lat || newVal.lng !== localLocation.value.lng)) {
    localLocation.value = { ...newVal };
    if (marker.value) {
      marker.value.setLatLng([newVal.lat, newVal.lng]);
    }
    if (map.value) {
      map.value.setView([newVal.lat, newVal.lng]);
    }
  }
}, { deep: true });
</script>

<style scoped>
.location-picker-container {
  position: relative;
  width: 100%;
}
.map-container {
  height: 400px;
  width: 100%;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  z-index: 10;
}
.search-overlay {
  position: absolute;
  top: 10px;
  left: 50px;
  right: 10px;
  z-index: 1000;
  display: flex;
  gap: 8px;
  background: white;
  padding: 8px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.search-input {
  flex: 1;
  border: 1px solid #e2e8f0;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
}
.search-btn {
  background: #FF6B2B;
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}
.location-details {
  margin-top: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}
</style>
