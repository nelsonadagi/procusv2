<template>
  <div class="pz-property-page">
    <div class="pz-l-container u-py-8">
      <div v-if="loading" class="pz-u-text-center u-py-20">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">Loading property intelligence...</p>
      </div>

      <div v-else-if="property" class="pz-space-y-8">
        <nav class="pz-breadcrumb pz-u-text-mono text-xs">
          <router-link to="/properties" class="pz-breadcrumb__item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:0.85rem;height:0.85rem"><path d="m15 18-6-6 6-6"/></svg>
            Properties
          </router-link>
          <span class="pz-breadcrumb__separator">/</span>
          <span class="pz-breadcrumb__current pz-u-color-steel">{{ property.title }}</span>
        </nav>

        <section class="pz-property-hero">
          <div class="pz-property-hero__media">
            <img
              v-if="heroMediaUrl"
              :src="heroMediaUrl"
              :alt="property.primary_media?.alt_text || property.title"
              class="pz-property-hero__image"
            />
            <div v-else class="pz-property-hero__fallback">
              <span class="pz-u-text-mono text-xs">PROPERTY MEDIA</span>
              <strong>{{ property.asset_type }}</strong>
            </div>
          </div>

          <div class="pz-property-hero__content">
            <div class="pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start pz-l-flex--gap-4 pz-l-flex--wrap">
              <div class="pz-space-y-3">
                <div class="pz-u-text-mono text-xs pz-u-color-earth">{{ property.listing_type }}</div>
                <h1 class="pz-u-text-display">{{ property.title }}</h1>
                <p class="pz-u-text-mono text-sm pz-u-color-steel pz-property-hero__description">{{ property.description }}</p>
              </div>
              <div class="pz-l-flex pz-l-flex--gap-2 pz-l-flex--wrap">
                <Badge variant="ghost">{{ property.asset_type }}</Badge>
                <Badge :variant="property.status === 'ACTIVE' ? 'success' : 'secondary'">{{ property.status }}</Badge>
              </div>
            </div>

            <div class="pz-property-hero__price">
              <span class="pz-u-text-mono text-xs pz-u-color-concrete">Commercial Terms</span>
              <strong>{{ displayPrice }}</strong>
              <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ property.location_display || 'Location pending' }}</span>
            </div>

            <div v-if="summaryStats.length" class="pz-property-summary-grid">
              <div v-for="stat in summaryStats" :key="stat.label" class="pz-property-detail__metric">
                <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                <div class="pz-metric__content">
                  <span class="pz-property-detail__label">{{ stat.label }}</span>
                  <span class="pz-property-detail__value">{{ stat.value }}</span>
                </div>
              </div>
            </div>

            <div v-if="property.highlighted_features?.length" class="pz-property-chip-row">
              <span v-for="feature in property.highlighted_features" :key="feature.id" class="pz-property-chip">
                {{ feature.name }}
              </span>
            </div>
          </div>
        </section>

        <div class="pz-property-layout">
          <section class="pz-space-y-6">
            <!-- Tab Navigation -->
            <div class="pz-property-tabs">
              <button
                v-for="tab in propertyTabs"
                :key="tab.id"
                type="button"
                class="pz-property-tab"
                :class="{ 'pz-property-tab--active': activeTab === tab.id }"
                @click="activeTab = tab.id"
              >
                <span class="pz-property-tab__label">{{ tab.label }}</span>
                <span v-if="tab.badge" class="pz-property-tab__badge">{{ tab.badge }}</span>
              </button>
            </div>

            <Card v-if="canModifyProperty" title="Operator Console" variant="elevated" eyebrow="Management">
              <div class="pz-operator-summary">
                <div class="pz-operator-summary__row">
                  <div class="pz-operator-summary__item">
                    <span class="pz-operator-summary__label">Status</span>
                    <span class="pz-operator-summary__value">
                      <Badge :variant="property.status === 'ACTIVE' ? 'success' : 'secondary'">{{ property.status }}</Badge>
                    </span>
                  </div>
                  <div class="pz-operator-summary__item">
                    <span class="pz-operator-summary__label">Inquiries</span>
                    <span class="pz-operator-summary__value">{{ property.inquiry_enabled !== false ? 'Open' : 'Closed' }}</span>
                  </div>
                  <div class="pz-operator-summary__item">
                    <span class="pz-operator-summary__label">Appointments</span>
                    <span class="pz-operator-summary__value">{{ property.appointment_enabled !== false ? 'Open' : 'Closed' }}</span>
                  </div>
                  <div class="pz-operator-summary__item">
                    <span class="pz-operator-summary__label">Financing</span>
                    <span class="pz-operator-summary__value">{{ property.financing_allowed ? 'Enabled' : 'Disabled' }}</span>
                  </div>
                </div>
                <div class="pz-operator-summary__actions">
                  <router-link :to="`/properties/${property.id}/edit`">
                    <Button variant="primary" size="sm">Edit Property</Button>
                  </router-link>
                </div>
              </div>
            </Card>

            <div v-show="activeTab === 'overview'" class="pz-tab-panel pz-space-y-6">
            <Card title="Overview" variant="premium" eyebrow="Property Details">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Owner')" v-html="getMetricIcon('Owner')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Owner</span>
                    <span class="pz-property-detail__value">{{ property.owner_name }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Manager')" v-html="getMetricIcon('Manager')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Manager</span>
                    <span class="pz-property-detail__value">{{ property.manager_name || 'Owner-managed' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Address')" v-html="getMetricIcon('Address')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Address</span>
                    <span class="pz-property-detail__value">{{ property.formatted_address || property.location_display || 'Address pending' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Finance')" v-html="getMetricIcon('Finance')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Finance</span>
                    <span class="pz-property-detail__value">{{ property.financing_allowed ? 'Financing supported' : 'Direct purchase only' }}</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card title="Market Positioning" variant="premium" eyebrow="Market Analysis">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in marketStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card title="Property Operations" eyebrow="Operations">
              <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Ownership')" v-html="getMetricIcon('Ownership')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Ownership</span>
                    <span class="pz-property-detail__value">{{ ownershipSummary }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Verification')" v-html="getMetricIcon('Verification')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Verification</span>
                    <span class="pz-property-detail__value">{{ property.ownership_profile?.verification_status || 'UNVERIFIED' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Pricing Strategy')" v-html="getMetricIcon('Pricing Strategy')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Pricing Strategy</span>
                    <span class="pz-property-detail__value">{{ property.pricing_profile?.pricing_strategy || 'FIXED' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Deposit')" v-html="getMetricIcon('Deposit')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Deposit</span>
                    <span class="pz-property-detail__value">{{ depositSummary }}</span>
                  </div>
                </div>
              </div>
            </Card>
            </div>

            <div v-show="activeTab === 'specs'" class="pz-tab-panel pz-space-y-6">
            <Card title="Property Specification" variant="premium" eyebrow="Key Specs">
              <div v-if="specificationStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
                <div v-for="stat in specificationStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No structured specification has been published yet.</p>
            </Card>

            <Card title="Development Readiness" eyebrow="Development">
              <div v-if="property.development_metadata" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Zoning')" v-html="getMetricIcon('Zoning')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Zoning</span>
                    <span class="pz-property-detail__value">{{ property.development_metadata.zoning_info || 'Not specified' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Build Ready')" v-html="getMetricIcon('Build Ready')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Build Ready</span>
                    <span class="pz-property-detail__value">{{ property.development_metadata.build_ready ? 'Yes' : 'No' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Development Stage')" v-html="getMetricIcon('Development Stage')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Development Stage</span>
                    <span class="pz-property-detail__value">{{ property.development_metadata.development_stage || 'Not specified' }}</span>
                  </div>
                </div>
                <div class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor('Utilities')" v-html="getMetricIcon('Utilities')"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">Utilities</span>
                    <span class="pz-property-detail__value">{{ formatUtilities(property.development_metadata.utilities_available) }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Development metadata has not been published for this property yet.</p>
            </Card>

            <Card title="Features And Amenities" eyebrow="Amenities">
              <div v-if="property.features?.length" class="pz-property-feature-grid">
                <div v-for="feature in property.features" :key="feature.id" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(feature.category)" v-html="getMetricIcon(feature.category)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ feature.category || 'Feature' }}</span>
                    <span class="pz-property-detail__value">{{ feature.name }}</span>
                    <span v-if="feature.description" class="pz-u-text-mono text-xs pz-u-color-steel">{{ feature.description }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No feature list published yet.</p>
            </Card>
            </div>

            <div v-show="activeTab === 'financials'" class="pz-tab-panel pz-space-y-6">
            <Card title="Financial Structure" variant="premium" eyebrow="Pricing">
              <div v-if="financialStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in financialStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Detailed pricing data has not been published yet.</p>
            </Card>

            <Card title="Ownership And Compliance" eyebrow="Legal">
              <div v-if="ownershipStats.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                <div v-for="stat in ownershipStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Ownership diligence notes have not been published yet.</p>
            </Card>
            </div>

            <div v-show="activeTab === 'links'" class="pz-tab-panel pz-space-y-6">
            <Card v-if="mediaGallery.length" title="Media" variant="elevated" eyebrow="Gallery">
              <div class="pz-property-gallery">
                <a
                  v-for="asset in mediaGallery"
                  :key="asset.id"
                  :href="asset.media_url || asset.external_url"
                  class="pz-property-gallery__item"
                  target="_blank"
                  rel="noreferrer"
                >
                  <div class="pz-property-gallery__preview">
                    <img
                      v-if="asset.media_type === 'IMAGE' && (asset.media_url || asset.external_url)"
                      :src="asset.media_url || asset.external_url"
                      :alt="asset.alt_text || asset.title"
                    />
                    <div v-else class="pz-property-gallery__placeholder">
                      {{ readableMediaType(asset.media_type) }}
                    </div>
                  </div>
                  <div class="pz-space-y-1">
                    <div class="pz-u-text-display text-sm">{{ asset.title || readableMediaType(asset.media_type) }}</div>
                    <div class="pz-u-text-mono text-xs pz-u-color-steel">{{ asset.caption || 'Open asset' }}</div>
                  </div>
                </a>
              </div>
            </Card>

            <Card title="Linked Projects" eyebrow="Connected">
              <div v-if="property.linked_projects?.length" class="pz-space-y-3">
                <router-link v-for="link in property.linked_projects" :key="link.id" :to="`/projects/${link.project}`" class="pz-property-detail__link-card">
                  <span class="pz-u-text-display text-sm">{{ link.project_title }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-steel">Open project workspace</span>
                </router-link>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">This property is currently operating as a standalone asset.</p>
            </Card>

            <Card title="Suggested Materials" eyebrow="Recommendations">
              <div v-if="materials.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
                <router-link v-for="material in materials" :key="material.id" :to="`/products/${material.id}`" class="pz-property-detail__link-card">
                  <span class="pz-u-text-display text-sm">{{ material.name }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ configStore.formatPrice(material.base_price, material.currency) }}</span>
                </router-link>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No material suggestions available yet.</p>
            </Card>
            </div>
          </section>

          <aside class="pz-space-y-6">
            <Card title="Showings And Visits">
              <!-- Upcoming Showings -->
              <div class="pz-showing-section">
                <div class="pz-showing-section__header">
                  <span class="pz-showing-section__title">Upcoming Showings</span>
                  <span v-if="property.showings?.length" class="pz-showing-section__count">{{ property.showings.length }}</span>
                </div>

                <div v-if="property.showings?.length" class="pz-showing-list">
                  <div v-for="showing in property.showings.slice(0, 3)" :key="showing.id" class="pz-showing-item">
                    <div class="pz-showing-item__date">
                      <span class="pz-showing-item__day">{{ new Date(showing.start_at).toLocaleDateString(undefined, { weekday: 'short' }) }}</span>
                      <span class="pz-showing-item__date-num">{{ new Date(showing.start_at).getDate() }}</span>
                    </div>
                    <div class="pz-showing-item__info">
                      <strong>{{ readableShowingType(showing.event_type) }}</strong>
                      <span>{{ new Date(showing.start_at).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }}</span>
                      <span v-if="showing.instructions" class="pz-showing-item__note">{{ showing.instructions }}</span>
                    </div>
                  </div>
                  <div v-if="property.showings.length > 3" class="pz-showing-more">
                    +{{ property.showings.length - 3 }} more showing{{ property.showings.length - 3 > 1 ? 's' : '' }}
                  </div>
                </div>
                <p v-else class="pz-showing-empty">No upcoming showings scheduled.</p>
              </div>

              <!-- Divider -->
              <div v-if="property.showings?.length && availableSlots.length" class="pz-showing-divider"></div>

              <!-- Book a Visit -->
              <div class="pz-showing-section">
                <div class="pz-showing-section__header">
                  <span class="pz-showing-section__title">Book a Visit</span>
                  <span v-if="availableSlots.length" class="pz-showing-section__count pz-showing-section__count--available">{{ availableSlots.length }} slot{{ availableSlots.length > 1 ? 's' : '' }}</span>
                </div>

                <div v-if="availableSlots.length" class="pz-slot-list">
                  <button
                    v-for="slot in availableSlots"
                    :key="slot.start_at"
                    type="button"
                    class="pz-slot-card"
                    :class="{ 'pz-slot-card--selected': selectedSlot?.start_at === slot.start_at }"
                    @click="selectedSlot = slot"
                  >
                    <span class="pz-slot-card__day">{{ new Date(slot.start_at).toLocaleDateString(undefined, { weekday: 'short' }).toUpperCase() }}</span>
                    <span class="pz-slot-card__date">{{ new Date(slot.start_at).getDate() }}</span>
                    <span class="pz-slot-card__time">{{ new Date(slot.start_at).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }}</span>
                  </button>
                </div>

                <!-- Selected Slot Summary -->
                <div v-if="selectedSlot" class="pz-slot-selected">
                  <span class="pz-slot-selected__label">Selected</span>
                  <span class="pz-slot-selected__value">{{ formatSlot(selectedSlot) }}</span>
                  <button type="button" class="pz-slot-selected__clear" @click="selectedSlot = null">×</button>
                </div>

                <!-- Booking Form -->
                <form v-if="selectedSlot" class="pz-booking-form" @submit.prevent="submitAppointment">
                  <div class="pz-booking-form__row">
                    <PzInput v-model="appointmentForm.full_name" label="Full Name" required size="sm" />
                    <PzInput v-model="appointmentForm.email" label="Email" type="email" size="sm" />
                  </div>
                  <PzInput v-model="appointmentForm.phone_number" label="Phone Number" size="sm" />
                  <textarea v-model="appointmentForm.notes" class="pz-input" rows="2" placeholder="Add visit notes or questions" />
                  <Button type="submit" variant="primary" fullWidth size="sm" :loading="submittingAppointment">Confirm Booking</Button>
                </form>

                <p v-else-if="!availableSlots.length" class="pz-showing-empty">No public appointment slots are currently available. Check back soon or send an inquiry.</p>
              </div>
            </Card>

            <Card title="Availability Snapshot" eyebrow="Status">
              <div class="pz-space-y-3">
                <div v-for="stat in availabilityStats" :key="stat.label" class="pz-property-detail__metric">
                  <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                  <div class="pz-metric__content">
                    <span class="pz-property-detail__label">{{ stat.label }}</span>
                    <span class="pz-property-detail__value">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card title="Inquiry" variant="accent" eyebrow="Get In Touch">
              <div v-if="property.inquiry_enabled !== false" class="pz-space-y-4">
                <form class="pz-space-y-4" @submit.prevent="submitInquiry">
                  <PzInput v-model="inquiryForm.full_name" label="Full Name" required />
                  <PzInput v-model="inquiryForm.email" label="Email" type="email" />
                  <PzInput v-model="inquiryForm.phone_number" label="Phone Number" />
                  <select v-model="inquiryForm.inquiry_type" class="pz-input">
                    <option value="GENERAL">General</option>
                    <option value="VIEWING">Viewing</option>
                    <option value="FINANCING">Financing</option>
                    <option value="MATERIALS">Materials</option>
                    <option value="SERVICE">Service</option>
                  </select>
                  <textarea v-model="inquiryForm.message" class="pz-input" rows="4" placeholder="How can the owner or manager help?" />
                  <Button type="submit" variant="primary" fullWidth :loading="submittingInquiry">Send Inquiry</Button>
                </form>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Inquiries are currently disabled for this property.</p>
            </Card>

            <Card title="Financing" variant="accent" eyebrow="Funding">
              <div v-if="financeProducts.length" class="pz-space-y-4">
                <div class="pz-property-side-note">
                  <span class="pz-u-text-mono text-xs pz-u-color-concrete">Finance target</span>
                  <strong>{{ property.financing_allowed ? 'Property-ready application' : 'Project-linked finance only' }}</strong>
                </div>
                <select v-model="financeForm.product" class="pz-input">
                  <option disabled value="">Select financing product</option>
                  <option v-for="product in financeProducts" :key="product.id" :value="product.id">{{ product.name }}</option>
                </select>
                <select v-model="financeForm.purpose_category" class="pz-input">
                  <option value="ACQUISITION">Acquisition</option>
                  <option value="COMPLETION">Completion</option>
                  <option value="RENOVATION">Renovation</option>
                </select>
                <PzInput v-model="financeForm.requested_amount" type="number" label="Requested Amount" />
                <textarea v-model="financeForm.purpose" class="pz-input" rows="3" placeholder="Describe what the financing will support" />
                <Button variant="primary" fullWidth :loading="submittingFinance" @click="submitFinance">Apply For Financing</Button>
              </div>
              <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">Financing products are not available at the moment.</p>
            </Card>

            <Card v-if="operatorView" title="Operator Feed" variant="elevated">
              <div class="pz-space-y-4">
                <div class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-4">
                  <div v-for="stat in operatorStats" :key="stat.label" class="pz-property-detail__metric">
                    <span class="pz-metric__icon" :class="'pz-metric__icon--' + getMetricColor(stat.label)" v-html="getMetricIcon(stat.label)"></span>
                    <div class="pz-metric__content">
                      <span class="pz-property-detail__label">{{ stat.label }}</span>
                      <span class="pz-property-detail__value">{{ stat.value }}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Recent Inquiries</div>
                  <div v-if="operatorInquiries.length" class="pz-space-y-2">
                    <div v-for="inquiry in operatorInquiries.slice(0, 4)" :key="inquiry.id" class="pz-property-detail__feed">
                      <strong>{{ inquiry.full_name }}</strong>
                      <span>{{ inquiry.inquiry_type }}</span>
                      <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ inquiry.email || inquiry.phone_number || 'No contact provided' }}</span>
                    </div>
                  </div>
                  <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No inquiries yet.</p>
                </div>
                <div>
                  <div class="pz-u-text-mono text-xs pz-u-color-earth u-mb-2">Upcoming Appointments</div>
                  <div v-if="operatorAppointments.length" class="pz-space-y-2">
                    <div v-for="appointment in operatorAppointments.slice(0, 4)" :key="appointment.id" class="pz-property-detail__feed">
                      <strong>{{ appointment.full_name }}</strong>
                      <span>{{ formatDateTime(appointment.scheduled_start) }}</span>
                      <span class="pz-u-text-mono text-xs pz-u-color-steel">{{ appointment.email || appointment.phone_number || 'No contact provided' }}</span>
                    </div>
                  </div>
                  <p v-else class="pz-u-text-mono text-xs pz-u-color-concrete">No appointments scheduled.</p>
                </div>
              </div>
            </Card>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Card from '../components/ui/Card.vue';
import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import PzInput from '../components/PzInput.vue';

const route = useRoute();
const authStore = useAuthStore();
const configStore = useConfigStore();
const showAlert = inject('showAlert');

const property = ref(null);
const availableSlots = ref([]);
const financeProducts = ref([]);
const materials = ref([]);
const operatorInquiries = ref([]);
const operatorAppointments = ref([]);
const selectedSlot = ref(null);
const loading = ref(true);
const activeTab = ref('overview');
const propertyTabs = computed(() => [
  { id: 'overview', label: 'Overview', badge: null },
  { id: 'specs', label: 'Specifications', badge: property.value?.features?.length || null },
  { id: 'financials', label: 'Financials', badge: null },
  { id: 'links', label: 'Projects & Media', badge: property.value?.linked_projects?.length || null },
]);
const submittingInquiry = ref(false);
const submittingAppointment = ref(false);
const submittingFinance = ref(false);
const inquiryForm = ref({
  full_name: '',
  email: '',
  phone_number: '',
  inquiry_type: 'GENERAL',
  message: '',
});

const appointmentForm = ref({
  full_name: '',
  email: '',
  phone_number: '',
  notes: '',
});

const financeForm = ref({
  product: '',
  requested_amount: '',
  purpose_category: 'ACQUISITION',
  purpose: '',
});

const operatorView = computed(() => {
  if (!property.value || !authStore.user) return false;
  // Direct ownership or management
  if (authStore.isAdmin || authStore.user.id === property.value.owner || authStore.user.id === property.value.manager) return true;
  // Permission-based operators (agents, surveyors, government auditors)
  if (authStore.hasPermission('property:manage_inquiries')) return true;
  if (authStore.hasPermission('property:manage_appointments')) return true;
  if (authStore.hasPermission('property:verify_property')) return true;
  return false;
});

const canModifyProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  if (authStore.isAdmin) return true;
  if (authStore.user.id === property.value.owner) return true;
  if (authStore.user.id === property.value.manager) return true;
  // Agents and property managers with update permission
  if (authStore.hasPermission('property:update_property')) return true;
  return false;
});

const canDeleteProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  if (authStore.isAdmin) return true;
  if (authStore.user.id === property.value.owner) return true;
  return authStore.hasPermission('property:delete_property');
});

const canVerifyProperty = computed(() => {
  if (!property.value || !authStore.user) return false;
  if (authStore.isAdmin) return true;
  return authStore.hasPermission('property:verify_property');
});

const heroMediaUrl = computed(() => property.value?.primary_media?.media_url || property.value?.primary_media?.external_url || '');

const mediaGallery = computed(() => property.value?.media_assets || []);

const displayPrice = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (pricing?.asking_price) {
    return `${configStore.formatPrice(pricing.asking_price, pricing.currency)} ${pricing.pricing_strategy || ''}`.trim();
  }
  if (property.value?.price_estimate) {
    return configStore.formatPrice(property.value.price_estimate, property.value?.pricing_profile?.currency || property.value?.country?.default_currency || 'KES');
  }
  return 'Price on request';
});

const marketStats = computed(() => {
  if (!property.value) return [];
  const items = [
    { label: 'Listing Type', value: property.value.listing_type },
    { label: 'Asset Type', value: property.value.asset_type },
    { label: 'Listing Status', value: property.value.status },
    { label: 'Purpose', value: property.value.purpose_name || property.value.purpose_slug || 'Not classified' },
    { label: 'Location', value: property.value.location_display || property.value.location_text || 'Location pending' },
    { label: 'Published', value: formatDate(property.value.created_at) },
    { label: 'Last Updated', value: formatDate(property.value.updated_at) },
    { label: 'Public Inquiry', value: property.value.inquiry_enabled ? 'Open' : 'Closed' },
    { label: 'Appointment Booking', value: property.value.appointment_enabled ? 'Open' : 'Closed' },
  ];
  return items.filter((item) => item.value);
});

const summaryStats = computed(() => {
  if (!property.value) return [];
  const specification = property.value.specification || {};
  const stats = [
    { label: 'Bedrooms', value: specification.bedrooms },
    { label: 'Bathrooms', value: specification.bathrooms },
    { label: 'Parking', value: specification.parking_spaces },
    {
      label: 'Internal Area',
      value: specification.internal_area ? `${specification.internal_area} ${specification.internal_area_unit}` : '',
    },
  ];
  return stats.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const specificationStats = computed(() => {
  const specification = property.value?.specification;
  if (!specification) return [];
  const stats = [
    { label: 'Bedrooms', value: specification.bedrooms },
    { label: 'Bathrooms', value: specification.bathrooms },
    { label: 'Floors', value: specification.floors },
    { label: 'Parking Spaces', value: specification.parking_spaces },
    {
      label: 'Internal Area',
      value: specification.internal_area ? `${specification.internal_area} ${specification.internal_area_unit}` : '',
    },
    {
      label: 'Lot Size',
      value: specification.lot_size ? `${specification.lot_size} ${specification.lot_size_unit}` : '',
    },
    { label: 'Year Built', value: specification.year_built },
    { label: 'Renovation Year', value: specification.renovation_year },
    { label: 'Furnishing', value: specification.furnishing_state },
    { label: 'Condition', value: specification.condition_rating },
    { label: 'Energy Rating', value: specification.energy_rating },
    { label: 'Occupancy', value: specification.occupancy_status },
  ];
  return stats.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const ownershipSummary = computed(() => {
  const ownership = property.value?.ownership_profile;
  if (!ownership) return 'Ownership profile not published';
  return ownership.legal_owner_name || ownership.ownership_type || 'Ownership profile available';
});

const depositSummary = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (!pricing?.requires_deposit) return 'No deposit requirement published';
  if (pricing.deposit_amount) return configStore.formatPrice(pricing.deposit_amount, pricing.currency);
  return 'Deposit required';
});

const financialStats = computed(() => {
  const pricing = property.value?.pricing_profile;
  if (!pricing) return [];
  const items = [
    { label: 'Currency', value: pricing.currency },
    { label: 'Asking Price', value: formatMoney(pricing.asking_price, pricing.currency) },
    { label: 'Rent Amount', value: formatMoney(pricing.rent_amount, pricing.currency) },
    { label: 'Pricing Strategy', value: pricing.pricing_strategy },
    {
      label: 'Price Per Unit',
      value: pricing.price_per_area_unit ? `${configStore.formatPrice(pricing.price_per_area_unit, pricing.currency)} / ${pricing.area_unit}` : '',
    },
    { label: 'Service Charge', value: formatMoney(pricing.service_charge_amount, pricing.currency) },
    { label: 'Tax Percentage', value: pricing.tax_percentage ? `${pricing.tax_percentage}%` : '' },
    { label: 'Insurance Percentage', value: pricing.insurance_percentage ? `${pricing.insurance_percentage}%` : '' },
    { label: 'Financing Notes', value: pricing.financing_notes },
  ];
  return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const ownershipStats = computed(() => {
  const ownership = property.value?.ownership_profile;
  if (!ownership) return [];
  const items = [
    { label: 'Legal Owner', value: ownership.legal_owner_name },
    { label: 'Ownership Type', value: ownership.ownership_type },
    { label: 'Title Reference', value: ownership.title_reference },
    { label: 'Deed Reference', value: ownership.deed_reference },
    { label: 'Verification Status', value: ownership.verification_status },
    { label: 'Lien Position', value: ownership.has_liens ? 'Liens declared' : 'No liens declared' },
    { label: 'Lien Notes', value: ownership.lien_notes },
    { label: 'Disclosure Notes', value: ownership.disclosure_notes },
  ];
  return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
});

const availabilityStats = computed(() => {
  const nextSlot = availableSlots.value[0];
  return [
    { label: 'Open Slots', value: availableSlots.value.length ? `${availableSlots.value.length} available` : 'No open slots' },
    { label: 'Next Available Slot', value: nextSlot ? formatSlot(nextSlot) : 'Not scheduled' },
    { label: 'Published Showings', value: property.value?.showings?.length ? `${property.value.showings.length} scheduled` : 'No showings' },
  ];
});

const operatorStats = computed(() => [
  { label: 'Open Leads', value: operatorInquiries.value.length },
  { label: 'Scheduled Appointments', value: operatorAppointments.value.length },
  { label: 'Open Slots', value: availableSlots.value.length },
  { label: 'Linked Projects', value: property.value?.linked_projects?.length || 0 },
]);

function formatUtilities(items) {
  if (!items?.length) return 'Not specified';
  return items.join(', ');
}

function formatMoney(value, sourceCurrency = 'KES') {
  if (value === null || value === undefined || value === '') return '';
  return configStore.formatPrice(value, sourceCurrency);
}

function formatDate(value) {
  if (!value) return '';
  return new Date(value).toLocaleDateString();
}

function formatDateTime(value) {
  return new Date(value).toLocaleString();
}

function formatSlot(slot) {
  return `${formatDateTime(slot.start_at)} - ${new Date(slot.end_at).toLocaleTimeString()}`;
}

function readableMediaType(type) {
  return (type || '').replaceAll('_', ' ');
}

const ICONS = {
  bed: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/></svg>',
  bath: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21h6"/><path d="M12 21v-7"/><path d="M8 14a4 4 0 0 1 8 0v7H8z"/><path d="M4 14h16"/></svg>',
  ruler: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 6H3"/><path d="M10 12H3"/><path d="M10 18H3"/><path d="M14 9h.01"/><path d="M18 9h.01"/><path d="M14 15h.01"/><path d="M18 15h.01"/></svg>',
  map: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
  pin: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
  user: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  briefcase: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
  dollar: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
  calendar: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>',
  car: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
  check: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
  layers: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
  bolt: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
  shield: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
  tag: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><path d="M7 7h.01"/></svg>',
  wallet: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5"/><path d="M16 12h.01"/></svg>',
  image: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
  home: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
  trend: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
  info: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/></svg>',
  default: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>'
};

function getMetricIcon(label) {
  if (!label) return ICONS.default;
  const l = label.toLowerCase();
  if (l.includes('bed')) return ICONS.bed;
  if (l.includes('bath')) return ICONS.bath;
  if (l.includes('sqft') || l.includes('square') || l.includes('area') || l.includes('size')) return ICONS.ruler;
  if (l.includes('lot')) return ICONS.map;
  if (l.includes('year') || l.includes('built')) return ICONS.calendar;
  if (l.includes('park')) return ICONS.car;
  if (l.includes('owner')) return ICONS.user;
  if (l.includes('manager')) return ICONS.briefcase;
  if (l.includes('address') || l.includes('location')) return ICONS.pin;
  if (l.includes('finance') || l.includes('price') || l.includes('cost') || l.includes('deposit') || l.includes('fee')) return ICONS.dollar;
  if (l.includes('zoning')) return ICONS.map;
  if (l.includes('build') || l.includes('ready')) return ICONS.check;
  if (l.includes('stage') || l.includes('development')) return ICONS.layers;
  if (l.includes('util')) return ICONS.bolt;
  if (l.includes('ownership')) return ICONS.shield;
  if (l.includes('verify')) return ICONS.check;
  if (l.includes('strategy') || l.includes('pricing')) return ICONS.tag;
  if (l.includes('market') || l.includes('trend') || l.includes('growth')) return ICONS.trend;
  if (l.includes('home') || l.includes('property') || l.includes('type')) return ICONS.home;
  return ICONS.default;
}

function getMetricColor(label) {
  if (!label) return 'default';
  const l = label.toLowerCase();
  if (l.includes('bed') || l.includes('bath') || l.includes('sqft') || l.includes('square') || l.includes('area') || l.includes('size') || l.includes('lot') || l.includes('park') || l.includes('year') || l.includes('built')) return 'blue';
  if (l.includes('finance') || l.includes('price') || l.includes('cost') || l.includes('deposit') || l.includes('fee') || l.includes('market') || l.includes('trend') || l.includes('growth')) return 'green';
  if (l.includes('ownership') || l.includes('verify') || l.includes('title') || l.includes('deed') || l.includes('lien') || l.includes('legal') || l.includes('compliance')) return 'purple';
  if (l.includes('address') || l.includes('location') || l.includes('owner') || l.includes('manager') || l.includes('home') || l.includes('property') || l.includes('type')) return 'orange';
  if (l.includes('build') || l.includes('ready') || l.includes('stage') || l.includes('development') || l.includes('zoning') || l.includes('util')) return 'teal';
  if (l.includes('strategy') || l.includes('pricing')) return 'slate';
  return 'default';
}

function readableShowingType(type) {
  return (type || '').replaceAll('_', ' ');
}

function readableOccurrenceType(type) {
  return (type || '').replaceAll('_', ' ');
}

async function loadProperty() {
  loading.value = true;
  try {
    // Core property data — must succeed
    const [propertyRes, availabilityRes] = await Promise.all([
      api.get(`/property/${route.params.id}/`),
      api.get(`/property/${route.params.id}/availability/`),
    ]);

    property.value = propertyRes.data;
    availableSlots.value = availabilityRes.data;

    // Optional enrichment — failures should not block the page
    try {
      const financeRes = await api.get('/v3/finance/products/');
      financeProducts.value = financeRes.data.results || financeRes.data;
    } catch {
      financeProducts.value = [];
    }

    try {
      const materialsRes = await api.get('/v1/products/');
      materials.value = (materialsRes.data.results || materialsRes.data || []).slice(0, 3);
    } catch {
      materials.value = [];
    }

    if (operatorView.value) {
      const [inquiriesRes, appointmentsRes] = await Promise.all([
        api.get('/property/inquiries/', { params: { property: route.params.id } }),
        api.get('/property/appointments/', { params: { property: route.params.id } }),
      ]);
      operatorInquiries.value = inquiriesRes.data.results || inquiriesRes.data;
      operatorAppointments.value = appointmentsRes.data.results || appointmentsRes.data;
    }
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property details.', 'error');
  } finally {
    loading.value = false;
  }
}

async function submitInquiry() {
  submittingInquiry.value = true;
  try {
    await api.post('/property/inquiries/', {
      property: route.params.id,
      ...inquiryForm.value,
    });
    showAlert?.('Inquiry submitted successfully.', 'success');
    inquiryForm.value = { full_name: '', email: '', phone_number: '', inquiry_type: 'GENERAL', message: '' };
    await loadProperty();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to submit inquiry.', 'error');
  } finally {
    submittingInquiry.value = false;
  }
}

async function submitAppointment() {
  if (!selectedSlot.value) {
    showAlert?.('Select an available slot first.', 'error');
    return;
  }

  submittingAppointment.value = true;
  try {
    await api.post('/property/appointments/', {
      property: route.params.id,
      availability_window: selectedSlot.value.window_id,
      scheduled_start: selectedSlot.value.start_at,
      scheduled_end: selectedSlot.value.end_at,
      ...appointmentForm.value,
    });
    showAlert?.('Appointment request submitted.', 'success');
    appointmentForm.value = { full_name: '', email: '', phone_number: '', notes: '' };
    selectedSlot.value = null;
    await loadProperty();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to book appointment.', 'error');
  } finally {
    submittingAppointment.value = false;
  }
}

async function submitFinance() {
  if (!authStore.isAuthenticated) {
    showAlert?.('Sign in to apply for financing.', 'error');
    return;
  }

  submittingFinance.value = true;
  try {
    await api.post('/v3/finance/applications/', {
      product: financeForm.value.product,
      target_type: 'PROPERTY',
      property: route.params.id,
      requested_amount: financeForm.value.requested_amount,
      purpose_category: financeForm.value.purpose_category,
      purpose: financeForm.value.purpose,
    });
    showAlert?.('Financing application submitted.', 'success');
    financeForm.value = { product: '', requested_amount: '', purpose_category: 'ACQUISITION', purpose: '' };
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to submit financing application.', 'error');
  } finally {
    submittingFinance.value = false;
  }
}

onMounted(loadProperty);
</script>

<style scoped>
.pz-property-page {
  /* Premium dynamic background using brand colors */
  background: 
    radial-gradient(circle at top left, rgba(212, 101, 42, 0.06), transparent 40%),
    radial-gradient(circle at bottom right, rgba(184, 115, 51, 0.05), transparent 40%),
    linear-gradient(180deg, var(--pz-color-limestone-white) 0%, #f4f1ea 100%);
  color: var(--pz-color-foundation-black);
  min-height: 100vh;
  position: relative;
  overflow: visible;
  font-family: var(--pz-font-primary);
}

/* Decorative ambient background glows using brand colors */
.pz-property-page::before,
.pz-property-page::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
  pointer-events: none;
}
.pz-property-page::before {
  top: -10%; left: -10%; width: 600px; height: 600px;
  background: rgba(212, 101, 42, 0.12); /* Earth Orange */
}
.pz-property-page::after {
  bottom: 10%; right: -10%; width: 700px; height: 700px;
  background: rgba(184, 115, 51, 0.08); /* Copper Circuit */
}

/* Ensure content is above background blobs */
.pz-l-container {
  position: relative;
  z-index: 1;
}

/* Hero Section */
.pz-property-hero {
  display: grid;
  gap: 2.5rem;
  grid-template-columns: 1.4fr 1fr;
  padding: 0;
  border-radius: 24px;
  background: #ffffff;
  border: 1px solid rgba(10, 10, 15, 0.06);
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.02),
    0 8px 24px rgba(10, 10, 15, 0.06),
    0 24px 48px rgba(10, 10, 15, 0.04);
  margin-bottom: 2rem;
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-property-hero:hover {
  transform: translateY(-4px);
  box-shadow:
    0 4px 8px rgba(10, 10, 15, 0.03),
    0 16px 32px rgba(10, 10, 15, 0.06),
    0 32px 64px rgba(10, 10, 15, 0.08);
}

.pz-property-hero__media {
  overflow: hidden;
  position: relative;
  min-height: 28rem;
}
.pz-property-hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.pz-property-hero:hover .pz-property-hero__image {
  transform: scale(1.04);
}
.pz-property-hero__fallback {
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, var(--pz-color-structural-steel), var(--pz-color-foundation-black));
  color: var(--pz-color-limestone-white);
  min-height: 28rem;
  flex-direction: column;
  gap: 0.5rem;
}

.pz-property-hero__content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.5rem;
  padding: 2.5rem 2.5rem 2.5rem 0;
}

.pz-u-text-display {
  font-family: var(--pz-font-display);
  font-size: 2.75rem;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--pz-color-foundation-black) 0%, var(--pz-color-structural-steel) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.pz-property-hero__description {
  line-height: 1.7;
  color: var(--pz-color-structural-steel);
  font-size: 1.05rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pz-property-hero__price {
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(212, 101, 42, 0.06), rgba(212, 101, 42, 0.02));
  border: 1px solid rgba(212, 101, 42, 0.12);
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.pz-property-hero__price strong {
  font-family: var(--pz-font-display);
  font-size: 2rem;
  font-weight: 800;
  color: var(--pz-color-earth-orange);
  letter-spacing: -0.02em;
  line-height: 1.1;
}

/* Feature Grids */
.pz-property-summary-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}

.pz-property-feature-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}

.pz-property-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}
.pz-property-chip {
  padding: 0.4rem 1rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.1);
  border: 1px solid rgba(212, 101, 42, 0.2);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: all 0.3s ease;
}
.pz-property-chip:hover {
  background: rgba(212, 101, 42, 0.15);
  border-color: rgba(212, 101, 42, 0.3);
  transform: translateY(-2px);
}

/* Media Gallery */
.pz-property-gallery {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
}
.pz-property-gallery__item,
.pz-property-detail__link-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.08);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-property-gallery__item:hover,
.pz-property-detail__link-card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(212, 101, 42, 0.3);
  box-shadow: 0 15px 30px -5px rgba(10, 10, 15, 0.1);
}

.pz-property-gallery__preview {
  height: 12rem;
  border-radius: 8px;
  overflow: hidden;
  background: var(--pz-color-concrete-grey);
}
.pz-property-gallery__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.pz-property-gallery__item:hover .pz-property-gallery__preview img {
  transform: scale(1.08);
}

/* Metrics and Cards inside Grid */
.pz-property-detail__metric,
.pz-property-detail__slot,
.pz-property-detail__feed,
.pz-property-side-note {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 1rem 1.25rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(10, 10, 15, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.pz-property-detail__metric:hover,
.pz-property-detail__feed:hover {
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(10, 10, 15, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(10, 10, 15, 0.06);
}

/* Modern metric item with icon */
.pz-property-detail__metric {
  flex-direction: row;
  align-items: flex-start;
  gap: 0.85rem;
  padding: 1.1rem 1.25rem;
}

.pz-metric__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.4rem;
  height: 2.4rem;
  border-radius: 12px;
  background: rgba(212, 101, 42, 0.08);
  color: var(--pz-color-earth-orange);
  flex-shrink: 0;
  margin-top: 0.1rem;
  transition: all 0.3s ease;
}
.pz-property-detail__metric:hover .pz-metric__icon {
  transform: scale(1.08);
}
.pz-metric__icon svg {
  width: 1.15rem;
  height: 1.15rem;
}

/* Color-coded metric icons */
.pz-metric__icon--blue {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}
.pz-property-detail__metric:hover .pz-metric__icon--blue {
  background: rgba(59, 130, 246, 0.18);
}

.pz-metric__icon--green {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}
.pz-property-detail__metric:hover .pz-metric__icon--green {
  background: rgba(34, 197, 94, 0.18);
}

.pz-metric__icon--purple {
  background: rgba(168, 85, 247, 0.1);
  color: #9333ea;
}
.pz-property-detail__metric:hover .pz-metric__icon--purple {
  background: rgba(168, 85, 247, 0.18);
}

.pz-metric__icon--orange {
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
}
.pz-property-detail__metric:hover .pz-metric__icon--orange {
  background: rgba(249, 115, 22, 0.18);
}

.pz-metric__icon--teal {
  background: rgba(20, 184, 166, 0.1);
  color: #0d9488;
}
.pz-property-detail__metric:hover .pz-metric__icon--teal {
  background: rgba(20, 184, 166, 0.18);
}

.pz-metric__icon--slate {
  background: rgba(100, 116, 139, 0.1);
  color: #475569;
}
.pz-property-detail__metric:hover .pz-metric__icon--slate {
  background: rgba(100, 116, 139, 0.18);
}

.pz-metric__content {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.pz-property-detail__label {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}
.pz-property-detail__value {
  color: var(--pz-color-foundation-black);
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.3;
}

.pz-operator-summary {
  display: grid;
  gap: 0.75rem;
}

.pz-operator-summary__row {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr));
}

.pz-operator-summary__item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 0.6rem 0.75rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.05);
}

.pz-operator-summary__label {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-operator-summary__value {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.pz-operator-summary__actions {
  display: flex;
  justify-content: flex-end;
}

/* Slots for appointments */
.pz-property-detail__slot {
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
}
.pz-property-detail__slot:hover {
  background: rgba(255, 255, 255, 0.9);
}
.pz-property-detail__slot:has(input:checked) {
  background: rgba(212, 101, 42, 0.08);
  border-color: rgba(212, 101, 42, 0.4);
  box-shadow: inset 0 0 0 1px rgba(212, 101, 42, 0.2);
}

/* Breadcrumbs */
.pz-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 2rem;
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
}
.pz-breadcrumb__item {
  color: var(--pz-color-concrete-grey);
  text-decoration: none;
  transition: color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.pz-breadcrumb__item:hover {
  color: var(--pz-color-earth-orange);
}
.pz-breadcrumb__separator {
  color: rgba(10, 10, 15, 0.15);
  font-size: 0.65rem;
}
.pz-breadcrumb__current {
  color: var(--pz-color-structural-steel);
  font-weight: 500;
}

/* Ensure inputs look clean */
:deep(.pz-input),
:deep(select.pz-input),
:deep(textarea.pz-input) {
  background: rgba(255, 255, 255, 0.8) !important;
  border: 1px solid rgba(10, 10, 15, 0.1) !important;
  color: var(--pz-color-foundation-black) !important;
  transition: all 0.3s ease !important;
}
:deep(.pz-input:focus),
:deep(select.pz-input:focus),
:deep(textarea.pz-input:focus) {
  border-color: var(--pz-color-earth-orange) !important;
  box-shadow: 0 0 0 2px rgba(212, 101, 42, 0.15) !important;
  background: white !important;
  outline: none;
}

/* Layout */
.pz-property-layout {
  display: grid;
  gap: 2.5rem;
  grid-template-columns: minmax(0, 1.6fr) minmax(22rem, 1fr);
}

/* Tab Navigation */
.pz-property-tabs {
  display: flex;
  gap: 0.4rem;
  margin-bottom: 1.5rem;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  border: 1px solid rgba(10, 10, 15, 0.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  width: fit-content;
  max-width: 100%;
}
.pz-property-tabs::-webkit-scrollbar {
  display: none;
}

.pz-property-tab {
  position: relative;
  padding: 0.7rem 1.1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--pz-color-concrete-grey);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.pz-property-tab:hover {
  color: var(--pz-color-structural-steel);
  background: rgba(10, 10, 15, 0.03);
}
.pz-property-tab--active {
  background: white;
  color: var(--pz-color-earth-orange);
  box-shadow: 0 2px 8px rgba(10, 10, 15, 0.08);
}

.pz-property-tab__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.4rem;
  height: 1.4rem;
  padding: 0 0.35rem;
  border-radius: 999px;
  background: rgba(212, 101, 42, 0.12);
  color: var(--pz-color-earth-orange);
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  font-weight: 600;
}

/* Tab Panels */
.pz-tab-panel {
  animation: fadeIn 0.25s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Sticky Sidebar */
.pz-property-sidebar,
aside.pz-space-y-6 {
  position: sticky;
  top: 2rem;
  align-self: start;
  height: fit-content;
}

/* Showings & Visits Card */
.pz-showing-section {
  display: grid;
  gap: 0.75rem;
}

.pz-showing-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.pz-showing-section__title {
  font-family: var(--pz-font-display);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--pz-color-foundation-black);
}

.pz-showing-section__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.5rem;
  height: 1.5rem;
  padding: 0 0.4rem;
  border-radius: 999px;
  background: rgba(10, 10, 15, 0.06);
  color: var(--pz-color-concrete-grey);
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  font-weight: 600;
}
.pz-showing-section__count--available {
  background: rgba(34, 139, 34, 0.1);
  color: #228b22;
}

.pz-showing-list {
  display: grid;
  gap: 0.5rem;
}

.pz-showing-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.05);
  transition: all 0.2s ease;
}
.pz-showing-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(10, 10, 15, 0.1);
}

.pz-showing-item__date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  padding: 0.3rem 0.5rem;
  border-radius: 8px;
  background: rgba(212, 101, 42, 0.08);
  border: 1px solid rgba(212, 101, 42, 0.15);
}

.pz-showing-item__day {
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-showing-item__date-num {
  font-family: var(--pz-font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--pz-color-earth-orange);
  line-height: 1;
}

.pz-showing-item__info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}
.pz-showing-item__info strong {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}
.pz-showing-item__info span {
  font-size: 0.78rem;
  color: var(--pz-color-steel);
}

.pz-showing-item__note {
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pz-showing-more {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  color: var(--pz-color-concrete-grey);
  text-align: center;
  padding: 0.25rem 0;
}

.pz-showing-empty {
  font-family: var(--pz-font-mono);
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  padding: 0.5rem 0;
}

.pz-showing-divider {
  height: 1px;
  background: rgba(10, 10, 15, 0.08);
  margin: 0.25rem 0;
}

/* Slot Cards */
.pz-slot-list {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.pz-slot-list::-webkit-scrollbar {
  display: none;
}

.pz-slot-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  min-width: 3.8rem;
  padding: 0.5rem 0.4rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--pz-font-display);
}
.pz-slot-card:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(212, 101, 42, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(10, 10, 15, 0.06);
}
.pz-slot-card--selected {
  background: rgba(212, 101, 42, 0.1);
  border-color: var(--pz-color-earth-orange);
  box-shadow: 0 0 0 2px rgba(212, 101, 42, 0.15);
}
.pz-slot-card--selected:hover {
  background: rgba(212, 101, 42, 0.14);
}

.pz-slot-card__day {
  font-family: var(--pz-font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  color: var(--pz-color-concrete-grey);
}
.pz-slot-card--selected .pz-slot-card__day {
  color: var(--pz-color-earth-orange);
}

.pz-slot-card__date {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--pz-color-foundation-black);
  line-height: 1;
}
.pz-slot-card--selected .pz-slot-card__date {
  color: var(--pz-color-earth-orange);
}

.pz-slot-card__time {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-steel);
}
.pz-slot-card--selected .pz-slot-card__time {
  color: var(--pz-color-earth-orange);
}

/* Selected Slot Summary */
.pz-slot-selected {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  background: rgba(212, 101, 42, 0.08);
  border: 1px solid rgba(212, 101, 42, 0.2);
}

.pz-slot-selected__label {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
  font-weight: 600;
}

.pz-slot-selected__value {
  flex: 1;
  font-size: 0.82rem;
  color: var(--pz-color-foundation-black);
  font-weight: 500;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pz-slot-selected__clear {
  display: grid;
  place-items: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: none;
  background: rgba(212, 101, 42, 0.15);
  color: var(--pz-color-earth-orange);
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s;
}
.pz-slot-selected__clear:hover {
  background: rgba(212, 101, 42, 0.25);
}

/* Booking Form */
.pz-booking-form {
  display: grid;
  gap: 0.6rem;
}

.pz-booking-form__row {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: 1fr 1fr;
}

@media (max-width: 1024px) {
  .pz-property-layout {
    grid-template-columns: 1fr;
  }

  .pz-editor-shell {
    grid-template-columns: 1fr;
  }

  .pz-editor-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .pz-property-hero {
    grid-template-columns: 1fr;
  }
  .pz-property-hero__content {
    padding: 0 2rem 2rem;
  }
  .pz-property-hero__media,
  .pz-property-hero__fallback {
    min-height: 20rem;
    border-radius: 24px 24px 0 0;
  }
}
</style>
