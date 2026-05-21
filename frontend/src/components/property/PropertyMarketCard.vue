<template>
  <article class="pvm-card" :class="[`pvm-card--${cardTone}`]">
    <div class="pvm-card__image">
      <img
        v-if="imageUrl"
        :src="imageUrl"
        :alt="property.primary_media?.alt_text || property.title"
      >
      <div v-else class="pvm-card__image-fallback">
        {{ readableValue(property.asset_type) }}
      </div>
      <div class="pvm-card__badges">
        <span class="pvm-card__badge">{{ readableValue(property.asset_type) }}</span>
        <span class="pvm-card__badge" :class="property.status === 'ACTIVE' ? 'pvm-card__badge--active' : 'pvm-card__badge--state'">
          {{ readableValue(property.status) }}
        </span>
      </div>
    </div>

    <div class="pvm-card__body">
      <div class="pvm-card__header">
        <div class="pvm-card__headcopy">
          <div class="pvm-card__meta-line">
            <span v-if="property.purpose_name">{{ property.purpose_name }}</span>
            <span v-if="property.financing_allowed" class="pvm-card__chip pvm-card__chip--positive">Finance ready</span>
          </div>
          <h3 class="pvm-card__title">{{ property.title }}</h3>
          <div class="pvm-card__subline">
            {{ property.location_display || property.location_text || property.formatted_address || 'Location pending' }}
          </div>
        </div>
        <div class="pvm-card__price-block">
          <div class="pvm-card__price">
            {{ formatNumber(property.pricing_profile?.asking_price || property.price_estimate, property.pricing_profile?.currency || property.country?.default_currency || 'KES') }}
          </div>
          <div class="pvm-card__readiness">
            <div class="pvm-card__readiness-bar">
              <div class="pvm-card__readiness-fill" :style="{ width: `${readiness}%` }"></div>
            </div>
            <span class="pvm-card__readiness-label">{{ readinessLabel }}</span>
          </div>
        </div>
      </div>

      <div class="pvm-card__stats">
        <span class="pvm-card__stat">{{ property.specification?.bedrooms || 0 }} bed</span>
        <span class="pvm-card__stat">{{ property.specification?.bathrooms || 0 }} bath</span>
        <span class="pvm-card__stat">{{ readableValue(property.development_metadata?.development_stage || 'NO_STAGE') }}</span>
      </div>

      <div v-if="highlightedFeatures.length" class="pvm-card__features">
        <span v-for="feature in highlightedFeatures" :key="feature.id" class="pvm-card__feature">
          {{ feature.name }}
        </span>
      </div>

      <div class="pvm-card__footer">
        <div class="pvm-card__owner">
          <span class="pvm-card__owner-mark">◎</span>
          <span>{{ property.manager_name || property.owner_name || 'Property team' }}</span>
        </div>
        <div class="pvm-card__actions">
          <Button size="sm" variant="primary" @click="$emit('open', property)">View details</Button>
          <Button size="sm" variant="ghost" @click="$emit('secondary', property)">{{ secondaryActionLabel }}</Button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue';
import Button from '../ui/Button.vue';

const props = defineProps({
  property: { type: Object, required: true },
  placeholderImage: { type: String, default: '/placeholder.png' },
});

defineEmits(['open', 'secondary']);

const imageUrl = computed(() => {
  const url = props.property.primary_media?.media_url || props.property.primary_media?.external_url;
  if (!url) return '';
  if (url.startsWith('http')) return url;
  const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/api\/?$/, '');
  return `${base}${url}`;
});

const highlightedFeatures = computed(() => (props.property.highlighted_features || []).slice(0, 3));

const readiness = computed(() => {
  const p = props.property;
  let score = 0;
  if (p.title) score += 15;
  if (p.location_display || p.location_text || p.formatted_address) score += 15;
  if (p.pricing_profile?.asking_price || p.price_estimate) score += 15;
  if (p.primary_media?.media_url || p.primary_media?.external_url) score += 20;
  if (p.purpose_name) score += 10;
  if (p.specification?.bedrooms || p.specification?.bathrooms) score += 10;
  if (highlightedFeatures.value.length) score += 10;
  if (p.financing_allowed) score += 5;
  return Math.min(score, 100);
});

const readinessLabel = computed(() => {
  if (readiness.value >= 80) return 'Strong listing';
  if (readiness.value >= 50) return 'Needs polish';
  return 'Listing in progress';
});

const cardTone = computed(() => {
  if (props.property.status === 'ACTIVE') return 'active';
  if (props.property.status === 'DRAFT') return 'draft';
  return 'neutral';
});

const secondaryActionLabel = computed(() => {
  if (props.property.status === 'ACTIVE' && props.property.appointment_enabled !== false) return 'Book visit';
  if (props.property.status === 'ACTIVE' && props.property.inquiry_enabled !== false) return 'Inquire';
  if (props.property.status === 'DRAFT') return 'Open';
  return 'Details';
});

function readableValue(value) {
  if (!value) return 'Unknown';
  return String(value)
    .replaceAll('_', ' ')
    .toLowerCase()
    .replace(/(^|\s)\S/g, (t) => t.toUpperCase());
}

function formatNumber(value, currency) {
  const amount = Number(value || 0);
  const safeCurrency = currency || 'KES';
  return `${safeCurrency} ${amount.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}
</script>

<style scoped>
.pvm-card {
  display: grid;
  grid-template-columns: 5.5rem minmax(0, 1fr) auto;
  gap: 1rem;
  padding: 1rem;
  background: #fff;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 14px;
  box-shadow:
    8px 8px 0 rgba(10, 10, 15, 0.03),
    0 2px 8px rgba(10, 10, 15, 0.03);
  transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  align-items: start;
}

.pvm-card:hover {
  transform: translateY(-2px);
  border-color: rgba(10, 10, 15, 0.14);
  box-shadow:
    10px 10px 0 rgba(10, 10, 15, 0.04),
    0 10px 22px rgba(10, 10, 15, 0.06);
}

.pvm-card--active {
  border-left: 3px solid #16a34a;
}

.pvm-card--draft {
  border-left: 3px solid var(--pz-color-concrete-grey);
}

.pvm-card--neutral {
  border-left: 3px solid rgba(212, 101, 42, 0.45);
}

.pvm-card__image {
  position: relative;
  width: 5.5rem;
  height: 5.5rem;
  overflow: hidden;
  border-radius: 11px;
  background: linear-gradient(135deg, #efe8dd, #ddd2c2);
  flex-shrink: 0;
}

.pvm-card__image img,
.pvm-card__image-fallback {
  width: 100%;
  height: 100%;
}

.pvm-card__image img {
  display: block;
  object-fit: cover;
}

.pvm-card__image-fallback {
  display: grid;
  place-items: center;
  color: var(--pz-color-foundation-black);
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-align: center;
  padding: 0.35rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(247, 243, 237, 0.92));
}

.pvm-card__badges {
  position: absolute;
  inset: auto 0.3rem 0.3rem 0.3rem;
  display: flex;
  gap: 0.28rem;
  flex-wrap: wrap;
}

.pvm-card__badge {
  padding: 0.18rem 0.4rem;
  border-radius: 7px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--pz-color-foundation-black);
  font-family: var(--pz-font-mono);
  font-size: 0.55rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.pvm-card__badge--active {
  background: rgba(22, 163, 74, 0.88);
  color: white;
}

.pvm-card__badge--state {
  background: rgba(10, 10, 15, 0.78);
  color: white;
}

.pvm-card__body {
  display: grid;
  gap: 0.6rem;
  min-width: 0;
}

.pvm-card__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1rem;
  align-items: start;
}

.pvm-card__headcopy {
  min-width: 0;
}

.pvm-card__meta-line {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-wrap: wrap;
  margin-bottom: 0.2rem;
  font-family: var(--pz-font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pvm-card__price {
  font-family: var(--pz-font-display);
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--pz-color-foundation-black);
  line-height: 1.1;
}

.pvm-card__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: 1.05rem;
  line-height: 1.25;
  color: var(--pz-color-foundation-black);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pvm-card__subline {
  margin-top: 0.28rem;
  color: var(--pz-color-concrete-grey);
  font-size: 0.8rem;
  line-height: 1.35;
}

.pvm-card__price-block {
  display: grid;
  gap: 0.35rem;
  justify-items: end;
}

.pvm-card__chip {
  padding: 0.2rem 0.45rem;
  border-radius: 8px;
  font-family: var(--pz-font-mono);
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}

.pvm-card__chip--positive {
  border: 1px solid rgba(22, 163, 74, 0.16);
  background: rgba(22, 163, 74, 0.1);
  color: #15803d;
}

.pvm-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  color: var(--pz-color-concrete-grey);
  font-size: 0.76rem;
  line-height: 1.35;
}

.pvm-card__stats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.pvm-card__stat {
  padding: 0.22rem 0.45rem;
  background: rgba(10, 10, 15, 0.04);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 7px;
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-structural-steel);
}

.pvm-card__readiness {
  display: grid;
  gap: 0.25rem;
  min-width: 8rem;
}

.pvm-card__readiness-bar {
  height: 0.42rem;
  background: rgba(10, 10, 15, 0.08);
  overflow: hidden;
}

.pvm-card__readiness-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--pz-color-earth-orange), #b87333);
}

.pvm-card__readiness-label {
  font-family: var(--pz-font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pvm-card__features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.pvm-card__feature {
  padding: 0.22rem 0.45rem;
  border: 1px solid rgba(212, 101, 42, 0.14);
  background: rgba(212, 101, 42, 0.06);
  border-radius: 7px;
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.pvm-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding-top: 0.25rem;
}

.pvm-card__owner {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  min-width: 0;
  font-size: 0.75rem;
  color: var(--pz-color-structural-steel);
}

.pvm-card__owner-mark {
  color: var(--pz-color-concrete-grey);
}

.pvm-card__actions {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

@media (max-width: 640px) {
  .pvm-card {
    grid-template-columns: 1fr;
  }

  .pvm-card__image {
    width: 100%;
    aspect-ratio: 3 / 2;
    height: auto;
  }

  .pvm-card__footer,
  .pvm-card__header {
    flex-direction: column;
    align-items: stretch;
  }

  .pvm-card__header {
    grid-template-columns: 1fr;
  }

  .pvm-card__price-block {
    justify-items: start;
  }

  .pvm-card__actions {
    justify-content: flex-start;
  }
}
</style>
