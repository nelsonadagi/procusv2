<template>
  <div class="pz-location-interface">
    <div class="pz-location-interface__header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-center u-mb-4">
      <div class="pz-location-interface__title-box">
        <h4 class="pz-u-text-mono text-sm font-bold">GEOSPATIAL_IDENTITY</h4>
        <p class="text-xs pz-u-color-steel">PRECISE_LOCATION_DATA_FOR_LOGISTICS</p>
      </div>
      <Button variant="ghost" size="sm" @click="detectLocation" :loading="detecting">
        📍 DETECT_GPS
      </Button>
    </div>

    <!-- Map Discovery Zone -->
    <div class="pz-location-interface__map-container">
      <div ref="mapContainer" class="pz-map-frame"></div>
      <div class="pz-map-search">
        <input 
          v-model="searchQuery" 
          placeholder="SEARCH_FOR_LOCATION_OR_LANDMARK..." 
          class="pz-map-search__input"
          @keydown.enter.prevent="searchLocation"
        />
        <button class="pz-map-search__btn" @click.prevent="searchLocation">SEARCH</button>
      </div>
    </div>

    <!-- Resolved Data Feed -->
    <div class="pz-location-interface__data u-mt-8">
      <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-6">
        <div class="pz-data-card" :class="{ 'pz-data-card--active': resolvedCountry }">
          <label class="pz-input__label">COUNTRY_REGISTRY</label>
          <div class="pz-data-value" :class="{ 'pz-data-value--empty': !resolvedCountry, 'pulse-resolving': resolving }">
            {{ resolvedCountry ? resolvedCountry.flag_emoji + ' ' + resolvedCountry.name : (resolving ? 'RESOLVING_COUNTRY...' : 'AWAITING_RESOLUTION...') }}
          </div>
        </div>
        <div class="pz-data-card" :class="{ 'pz-data-card--active': localLocation.city }">
          <label class="pz-input__label">LOCALITY_CITY</label>
          <div class="pz-data-value" :class="{ 'pz-data-value--empty': !localLocation.city, 'pulse-resolving': resolving }">
            {{ localLocation.city || (resolving ? 'FETCHING_LOCALITY...' : 'SELECT_ON_MAP') }}
          </div>
        </div>
      </div>

      <div class="pz-data-card u-mt-6" :class="{ 'pz-data-card--active': localLocation.address }">
        <label class="pz-input__label">FORMATTED_ADDRESS (REVERSE_GEOCODED)</label>
        <div class="pz-data-value pz-data-value--address" :class="{ 'pz-data-value--empty': !localLocation.address, 'pulse-resolving': resolving }">
          {{ localLocation.address || (resolving ? 'DISCOVERING_ADDRESS_HIERARCHY...' : 'POINT_MARKER_ON_MAP_TO_DISCOVER_ADDRESS') }}
        </div>
      </div>

      <div class="pz-l-flex pz-l-flex--gap-6 u-mt-6 pz-u-text-mono text-[10px] pz-u-color-steel pz-u-border-t pz-pt-4">
        <span>LAT: {{ localLocation.lat?.toFixed(6) || '0.00' }}</span>
        <span>LNG: {{ localLocation.lng?.toFixed(6) || '0.00' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useConfigStore } from '../../stores/config';
import Button from './Button.vue';
import { inject } from 'vue';

const showAlert = inject('showAlert', null);

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ lat: -1.2921, lng: 36.8219, address: '', city: '', country_id: null })
  },
  height: {
    type: String,
    default: '350px'
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

const configStore = useConfigStore();
const mapContainer = ref(null);
const map = ref(null);
const marker = ref(null);
const searchQuery = ref('');
const localLocation = ref({ ...props.modelValue });
const detecting = ref(false);
const resolving = ref(false);
const resolvedCountry = ref(null);

const normalizeCountryName = (value) => (
  value
    ?.toLowerCase()
    .replace(/\b(republic|state|states|federal|democratic|kingdom|of|the)\b/g, '')
    .replace(/[^a-z]/g, '')
    .trim() || ''
);

const isoMap = {
  KE: 'KEN',
  UG: 'UGA',
  TZ: 'TZA',
  RW: 'RWA',
  BI: 'BDI',
  SS: 'SSD',
  ET: 'ETH'
};

const isoReverseMap = Object.fromEntries(
  Object.entries(isoMap).map(([alpha2, alpha3]) => [alpha3, alpha2])
);

const initMap = () => {
  if (!mapContainer.value) return;

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
    updateLocationFromManual(lat, lng);
  });

  map.value.on('click', (event) => {
    const { lat, lng } = event.latlng;
    updateLocationFromManual(lat, lng);
  });
};

const updateLocationFromManual = async (lat, lng) => {
  localLocation.value.lat = lat;
  localLocation.value.lng = lng;
  if (marker.value) {
    marker.value.setLatLng([lat, lng]);
  }
  if (map.value) {
    map.value.panTo([lat, lng]);
  }

  await reverseGeocode(lat, lng);
  emitUpdate();
};

const reverseGeocode = async (lat, lng) => {
  resolving.value = true;
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=en`);
    const data = await response.json();
    
    if (data && data.address) {
      localLocation.value.address = data.display_name;
      localLocation.value.city = data.address.city || data.address.town || data.address.village || data.address.municipality;
      
      // Sync country with registry
      const geoCountryCode = data.address.country_code?.toUpperCase();
      matchCountry(geoCountryCode, data.address.country);
    }
  } catch (error) {
    console.error('Geocoding error:', error);
  } finally {
    resolving.value = false;
  }
};

const matchCountry = (isoCode, name) => {
  if (!configStore.countries.length) {
    console.warn('[GEO] Registry not loaded yet, deferring match');
    return;
  }
  
  const searchCode = isoCode?.toUpperCase()?.trim();
  const searchCodeAlt = searchCode?.length === 2 ? isoMap[searchCode] : isoReverseMap[searchCode];
  const searchName = name?.toLowerCase().trim();
  const normalizedSearchName = normalizeCountryName(name);

  const matched = configStore.countries.find(c => {
    const regCode = c.iso_code?.toUpperCase().trim();
    const regName = c.name?.toLowerCase().trim();
    const normalizedRegName = normalizeCountryName(c.name);
    
    const codeMatch = regCode === searchCode || regCode === searchCodeAlt;
    const nameMatch = regName === searchName || 
                     (searchName === 'kenya' && regName === 'kenya') ||
                     (searchName && regName && regName.includes(searchName)) ||
                     (searchName && regName && searchName.includes(regName)) ||
                     (normalizedSearchName && normalizedRegName && normalizedSearchName === normalizedRegName) ||
                     (normalizedSearchName && normalizedRegName && normalizedRegName.includes(normalizedSearchName)) ||
                     (normalizedSearchName && normalizedRegName && normalizedSearchName.includes(normalizedRegName));
    
    return codeMatch || nameMatch;
  });
  
  if (matched) {
    console.log(`[GEO] Registry Match SUCCESS: ${matched.name}`);
    resolvedCountry.value = matched;
    localLocation.value.country_id = matched.id;
  } else {
    console.warn(`[GEO] Registry Match FAIL for: ${name} (${isoCode})`);
    const defaultCountry = configStore.activeCountry;
    const defaultCode = defaultCountry?.iso_code?.toUpperCase()?.trim();
    const defaultName = normalizeCountryName(defaultCountry?.name);
    const defaultMatches =
      (defaultCode && (defaultCode === searchCode || defaultCode === searchCodeAlt)) ||
      (defaultName && normalizedSearchName && defaultName === normalizedSearchName);

    if (defaultCountry && defaultMatches) {
      console.log('[GEO] Falling back to active platform country');
      resolvedCountry.value = defaultCountry;
      localLocation.value.country_id = defaultCountry.id;
      return;
    }

    // If we only have ONE country in the registry and it's most likely that, auto-select
    if (configStore.countries.length === 1) {
       console.log('[GEO] Single country registry, auto-defaulting');
       resolvedCountry.value = configStore.countries[0];
       localLocation.value.country_id = configStore.countries[0].id;
    }
  }
};

// Tactical Watcher: Re-match country if the registry loads after location detection
watch(() => configStore.countries, (newCounties) => {
  if (newCounties.length > 0 && localLocation.value.lat && !resolvedCountry.value) {
    console.log('[GEO] Registry loaded post-detection, attempting re-match');
    reverseGeocode(localLocation.value.lat, localLocation.value.lng);
  }
}, { immediate: true });

const searchLocation = async () => {
  if (!searchQuery.value) return;
  
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}&limit=1`);
    const data = await response.json();
    if (data && data.length > 0) {
      const { lat, lon } = data[0];
      updateLocationFromManual(parseFloat(lat), parseFloat(lon));
      if (map.value) map.value.setZoom(15);
    }
  } catch (error) {
    console.error('Search error:', error);
  }
};

const detectLocation = () => {
  detecting.value = true;
  if (!navigator.geolocation) {
    detecting.value = false;
    if (showAlert) showAlert("Geolocation is not supported by your browser", "error");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      updateLocationFromManual(latitude, longitude);
      if (map.value) map.value.setZoom(16);
      detecting.value = false;
      if (showAlert) showAlert("📍 GPS Signal Lock: Precise coordinates captured.", "success");
    },
    (error) => {
      detecting.value = false;
      if (showAlert) showAlert("Location access denied or unavailable", "warning");
    },
    { enableHighAccuracy: true }
  );
};

const emitUpdate = () => {
  // Precision Guard: Truncate to 6 decimal places (approx 10cm accuracy)
  // This ensures we stay comfortably within the backend's max_digits=12 limit.
  const sanitized = {
    ...localLocation.value,
    lat: localLocation.value.lat ? parseFloat(localLocation.value.lat.toFixed(6)) : null,
    lng: localLocation.value.lng ? parseFloat(localLocation.value.lng.toFixed(6)) : null
  };
  emit('update:modelValue', sanitized);
  emit('change', sanitized);
};

onMounted(async () => {
  await configStore.fetchConfig();
  if (localLocation.value.country_id) {
    resolvedCountry.value = configStore.countries.find(c => c.id === localLocation.value.country_id);
  }
  nextTick(initMap);
});

watch(() => props.modelValue, (newVal) => {
  if (newVal && (newVal.lat !== localLocation.value.lat || newVal.lng !== localLocation.value.lng)) {
    localLocation.value = { ...newVal };
    if (marker.value) marker.value.setLatLng([newVal.lat, newVal.lng]);
    if (map.value) map.value.setView([newVal.lat, newVal.lng]);
    if (newVal.country_id) resolvedCountry.value = configStore.countries.find(c => c.id === newVal.country_id);
  }
}, { deep: true });
</script>

<style scoped>
.pz-location-interface {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
}

.pz-location-interface__map-container {
  position: relative;
  overflow: hidden;
  border: 2px solid var(--pz-color-foundation-black);
  border-radius: 4px;
}

.pz-map-frame {
  height: 380px;
  width: 100%;
  background: #f1f5f9;
  z-index: 10;
}

.pz-map-search {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 500px;
  z-index: 1000;
  display: flex;
  gap: 0;
  background: white;
  padding: 4px;
  border: 2px solid var(--pz-color-foundation-black);
  box-shadow: 4px 4px 0 var(--pz-color-foundation-black);
}

.pz-map-search__input {
  flex: 1;
  border: none;
  padding: 12px 16px;
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
  outline: none !important;
}

.pz-map-search__btn {
  background: var(--pz-color-foundation-black);
  color: white;
  border: none;
  padding: 0 24px;
  font-family: var(--pz-font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.pz-map-search__btn:hover {
  opacity: 0.9;
}

.pz-data-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 16px;
  border-radius: 6px;
  transition: border-color 0.3s;
}

.pz-data-card--active {
  border-color: var(--pz-color-earth-orange);
}

.pz-data-value {
  font-family: var(--pz-font-mono);
  font-size: 1rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  margin-top: 8px;
}

.pz-data-value--empty {
  color: #94a3b8;
  font-weight: 400;
  font-size: 0.85rem;
}

.pz-data-value--address {
  font-size: 0.875rem;
  line-height: 1.6;
}

.pz-input__label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.pulse-resolving {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

:deep(.leaflet-top) {
  top: 80px;
}
:deep(.leaflet-control-zoom) {
  border: 2px solid #000 !important;
  box-shadow: 4px 4px 0 rgba(0,0,0,0.1) !important;
}
</style>
