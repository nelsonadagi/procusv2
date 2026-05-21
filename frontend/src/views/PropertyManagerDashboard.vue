<template>
  <DashboardShell
    v-model:active-section="activeSection"
    accent="earth"
    :title="dashboardTitle"
    :eyebrow="dashboardEyebrow"
    signal-text="PROPERTY GRID ONLINE"
    workspace-label="Operations"
    :sidebar-groups="navGroups"
    :quickstats="quickstats"
  >
    <template #headerActions>
      <Button v-if="canCreateListing" variant="primary" size="sm" @click="openPropertyModal">New Listing</Button>
      <Button v-if="canManageAppointments" variant="outline" size="sm" @click="openAvailabilityModal">Publish Availability</Button>
      <Button variant="ghost" size="sm" @click="loadDashboard">Refresh</Button>
    </template>

    <WorkflowGuide title="Workflow Path" eyebrow="Start Here">
      <div class="pz-workflow-banner">
        <div class="pz-workflow-banner__summary">
          <div class="pz-workflow-banner__kicker">{{ workflowSummary.stage }}</div>
          <h3 class="pz-workflow-banner__title">{{ workflowSummary.title }}</h3>
          <p class="pz-workflow-banner__body">{{ workflowSummary.body }}</p>
        </div>
        <div class="pz-workflow-banner__actions">
          <Button v-if="workflowSummary.primaryAction" variant="primary" @click="workflowSummary.primaryAction.handler">
            {{ workflowSummary.primaryAction.label }}
          </Button>
          <Button v-if="workflowSummary.secondaryAction" variant="outline" @click="workflowSummary.secondaryAction.handler">
            {{ workflowSummary.secondaryAction.label }}
          </Button>
        </div>
      </div>
      <div class="pz-workflow-banner__steps">
        <div
          v-for="step in workflowSteps"
          :key="step.label"
          class="pz-workflow-step"
          :class="{ 'pz-workflow-step--done': step.done, 'pz-workflow-step--active': step.active }"
        >
          <div class="pz-workflow-step__icon">{{ step.index }}</div>
          <div class="pz-workflow-step__content">
            <strong>{{ step.label }}</strong>
            <span>{{ step.help }}</span>
          </div>
        </div>
      </div>
    

    <ModuleCTA
      eyebrow="Listing Pipeline"
      title="Add another property or turn a listing into a project."
      body="Publish availability, attach media, and move qualified assets into project planning when buyers or developers show interest."
      primary-label="New Listing"
      primary-to="/property-manager/dashboard"
      secondary-label="Start Project"
      secondary-to="/projects/new"
      tone="steel"
    />
</WorkflowGuide>

    <Card title="Operations Snapshot" eyebrow="Action First" class="pz-ops-snapshot-card">
      <div class="pz-ops-snapshot">
        <div class="pz-ops-snapshot__summary">
          <div class="pz-ops-snapshot__kicker">
            <span class="pz-ops-snapshot__dot" aria-hidden="true"></span>
            {{ urgentActions.length }} urgent action{{ urgentActions.length === 1 ? '' : 's' }} · {{ healthSnapshot[0].value }} healthy · {{ healthSnapshot[1].value }} need attention · {{ healthSnapshot[2].value }} blocked
          </div>
          <h3 class="pz-ops-snapshot__title">{{ workflowSummary.title }}</h3>
          <p class="pz-ops-snapshot__body">{{ workflowSummary.body }}</p>
          <div class="pz-ops-snapshot__actions">
            <Button v-if="workflowSummary.primaryAction" variant="primary" @click="workflowSummary.primaryAction.handler">
              {{ workflowSummary.primaryAction.label }}
            </Button>
            <Button v-if="workflowSummary.secondaryAction" variant="outline" @click="workflowSummary.secondaryAction.handler">
              {{ workflowSummary.secondaryAction.label }}
            </Button>
          </div>
        </div>
        <div class="pz-ops-snapshot__metrics">
          <button
            v-for="metric in overviewMetrics"
            :key="metric.label"
            type="button"
            class="pz-ops-metric"
            @click="metric.action"
          >
            <span class="pz-ops-metric__label">{{ metric.label }}</span>
            <strong class="pz-ops-metric__value">{{ metric.value }}</strong>
            <span class="pz-ops-metric__body">{{ metric.body }}</span>
          </button>
        </div>
      </div>
    </Card>

    <Card title="Portfolio Performance" eyebrow="Live Metrics" class="pz-ops-snapshot-card">
      <div class="pz-performance-strip">
        <div v-for="metric in performanceMetrics" :key="metric.label" class="pz-performance-metric">
          <span>{{ metric.label }}</span>
          <strong>{{ metric.value }}</strong>
        </div>
      </div>
    </Card>

    <Card title="Activity And Alerts" eyebrow="Recent Work" class="pz-activity-shell">
      <div class="pz-activity-shell__tabs">
        <Button variant="ghost" size="sm" :class="{ 'is-active': activityView === 'alerts' }" @click="activityView = 'alerts'">Alerts</Button>
        <Button variant="ghost" size="sm" :class="{ 'is-active': activityView === 'timeline' }" @click="activityView = 'timeline'">Timeline</Button>
      </div>
      <PropertyNotificationPanel
        v-if="activityView === 'alerts'"
        :notifications="propertyNotifications"
        @action="handlePropertyNotificationAction"
      />
      <PropertyActivityTimeline v-else :events="propertyTimeline" />
    </Card>

    <div v-if="activeSection === 'listings'" class="pz-manager-layout">
      <Card title="Listing Operations" class="u-xl-col-span-2">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Create structured property listings in a focused modal flow instead of inline page editing.</p>
          <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
            <Button type="button" variant="primary" @click="openPropertyModal">Create Listing</Button>
            <Button type="button" variant="outline" @click="openAvailabilityModal">Publish Availability</Button>
          </div>
        </div>
      </Card>

      <Card title="Availability">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Manage visitor booking windows in a modal so the live inventory grid stays visible.</p>
          <Button type="button" variant="outline" fullWidth @click="openAvailabilityModal">Open Availability Publisher</Button>
        </div>
      </Card>

      <Card title="Managed Properties" class="u-xl-col-span-3">
        <div v-if="properties.length" class="pz-property-groups">
          <section v-for="group in propertyGroups" :key="group.id" class="pz-property-group">
            <div class="pz-property-group__header">
              <strong>{{ group.label }}</strong>
              <span>{{ group.items.length }}</span>
            </div>
            <div v-if="group.items.length" class="pz-manager-list">
              <router-link
                v-for="item in group.items"
                :key="item.id"
                :to="`/properties/${item.id}`"
                class="pz-manager-list__row"
              >
                <label class="pz-checkbox-row" @click.stop>
                  <input v-model="selectedProperties" type="checkbox" :value="item.id" />
                  <span>Select</span>
                </label>
                <div class="pz-manager-list__primary">
                  <div class="pz-u-text-display text-sm">{{ item.title }}</div>
                  <div class="pz-u-text-mono text-xs pz-u-color-steel">
                    {{ item.asset_type }} // {{ item.location_display || 'Location pending' }}
                  </div>
                </div>
                <div class="pz-manager-list__meta">
                  <span class="pz-manager-pill">{{ item.appointment_enabled ? 'Appointments On' : 'Appointments Off' }}</span>
                  <span class="pz-manager-pill">{{ item.inquiry_enabled ? 'Inquiries On' : 'Inquiries Off' }}</span>
                </div>
                <div class="pz-manager-list__commercial">
                  <strong>{{ configStore.formatPrice(item.pricing_profile?.asking_price || item.price_estimate, item.pricing_profile?.currency || item.country?.default_currency || configStore.activeCurrencyCode) }}</strong>
                  <span class="pz-u-text-mono text-xs pz-u-color-earth">{{ item.status }}</span>
                </div>
                <div class="pz-manager-list__readiness">
                  <span class="pz-manager-pill">{{ getPropertyHealth(item).label }}</span>
                  <span class="pz-u-text-mono text-xs pz-u-color-concrete">{{ getPropertyHealth(item).summary }}</span>
                </div>
              </router-link>
            </div>
          </section>
          <div v-if="selectedProperties.length" class="pz-bulk-actions">
            <span>{{ selectedProperties.length }} selected</span>
            <Button size="sm" variant="outline" @click="bulkUpdateStatus('ACTIVE')">Publish</Button>
            <Button size="sm" variant="outline" @click="bulkUpdateStatus('INACTIVE')">Archive</Button>
            <Button size="sm" variant="ghost" @click="selectedProperties = []">Clear</Button>
          </div>
        </div>
        <EmptyState
          v-else
          icon="🏠"
          title="No properties yet"
          description="Create your first listing to start managing properties."
          next-step="Add a title, location, price, and availability, then publish the listing so visitors can find it."
          action-label="Create Listing"
          action-variant="primary"
          @action="openPropertyModal"
        />
      </Card>
    </div>

    <div v-else-if="activeSection === 'availability'" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--gap-8">
      <Card title="Publish Availability">
        <div class="pz-space-y-4">
          <p class="pz-u-color-steel">Open the availability modal to publish new slots without losing context.</p>
          <Button type="button" variant="primary" fullWidth @click="openAvailabilityModal">Publish Slots</Button>
        </div>
      </Card>

      <Card title="Current Appointments">
        <EmptyState
          v-if="!appointments.length"
          icon="🗓"
          title="No appointments yet"
          description="Published slots and visitor bookings will appear here."
        />
        <div v-else class="pz-space-y-3">
          <div v-for="appt in appointments.slice(0, 6)" :key="appt.id" class="pz-manager-feed">
            <strong>{{ appt.property_title }}</strong>
            <span>{{ formatDateTime(appt.scheduled_start) }}</span>
          </div>
        </div>
      </Card>
    </div>

    <div v-else-if="activeSection === 'leads'">
      <Card title="Incoming Leads">
        <div v-if="inquiries.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-2 pz-l-grid--lg-cols-3 pz-l-grid--gap-4">
          <div v-for="inquiry in inquiries" :key="inquiry.id" class="pz-manager-feed">
            <strong>{{ inquiry.full_name }}</strong>
            <span>{{ inquiry.property_title }}</span>
            <span class="pz-u-text-mono text-xs pz-u-color-earth">{{ inquiry.inquiry_type }}</span>
          </div>
        </div>
        <EmptyState
          v-else
          icon="📭"
          title="No inquiries yet"
          description="No one has contacted these properties yet. Add media, improve the description, and publish visit slots to make the next action obvious."
          next-step="Improve the lowest-health listing first, then refresh this lead queue."
          action-label="Improve Listing"
          action-variant="primary"
          @action="openLowestHealthListing"
        />
      </Card>
    </div>

    <div v-else-if="activeSection === 'appointments'">
      <Card title="Appointments">
        <div v-if="appointments.length" class="pz-l-grid pz-l-grid--cols-1 pz-l-grid--md-cols-3 pz-l-grid--gap-4">
          <div v-for="appointment in appointments" :key="appointment.id" class="pz-manager-feed">
            <strong>{{ appointment.full_name }}</strong>
            <span>{{ appointment.property_title }}</span>
            <span>{{ formatDateTime(appointment.scheduled_start) }}</span>
            <div class="pz-manager-feed__actions">
              <Button v-if="appointment.status === 'REQUESTED'" size="sm" variant="outline" @click="updateAppointmentStatus(appointment, 'confirm')">Confirm</Button>
              <Button size="sm" variant="ghost" @click="captureVisitOutcome(appointment)">Outcome</Button>
              <Button size="sm" variant="ghost" @click="updateAppointmentStatus(appointment, 'cancel')">Cancel</Button>
            </div>
          </div>
        </div>
        <EmptyState
          v-else
          icon="🗓"
          title="No appointments scheduled"
          description="Visitors cannot book yet until clear visit slots exist."
          next-step="Publish visit slots so interested buyers can act without calling."
          action-label="Add Visit Slots"
          action-variant="primary"
          @action="openAvailabilityModal"
        />
      </Card>
    </div>

    <div v-else-if="activeSection === 'verification'">
      <Card title="Approval Queue">
        <div v-if="approvalQueue.length" class="pz-space-y-3">
          <div v-for="item in approvalQueue" :key="item.id" class="pz-manager-feed">
            <strong>{{ item.title }}</strong>
            <span>{{ item.location_display || item.location_text || 'Location pending' }}</span>
            <span class="pz-u-text-mono text-xs pz-u-color-earth">{{ item.status }}</span>
            <div class="pz-manager-feed__actions">
              <Button size="sm" variant="primary" @click="moderateProperty(item, 'approve')">Approve</Button>
              <Button size="sm" variant="outline" @click="moderateProperty(item, 'request_changes')">Request Changes</Button>
              <Button size="sm" variant="ghost" @click="moderateProperty(item, 'reject')">Reject</Button>
            </div>
          </div>
        </div>
        <EmptyState
          v-else
          icon="✓"
          title="No properties pending review"
          description="Listings submitted for moderation will appear here."
        />
      </Card>
    </div>

    <Modal :isOpen="showPropertyModal" title="PUBLISH_PROPERTY_LISTING" size="xl" @close="closePropertyModal">
      <form id="property-form" class="pz-space-y-6" @submit.prevent="createProperty">
        <div class="pz-template-picker">
          <button
            v-for="template in propertyTemplates"
            :key="template.id"
            type="button"
            class="pz-template-picker__item"
            :class="{ 'is-active': activeTemplate === template.id }"
            @click="applyPropertyTemplate(template.id)"
          >
            <strong>{{ template.label }}</strong>
            <span>{{ template.help }}</span>
          </button>
        </div>

        <div class="pz-readiness-meter">
          <span>Creation readiness</span>
          <div class="pz-readiness-meter__bar"><i :style="{ width: `${creationReadinessScore}%` }"></i></div>
          <strong>{{ creationReadinessScore }}%</strong>
        </div>

        <div class="pz-manager-form-grid">
          <PzInput v-model="propertyForm.title" label="Title" required />
          <PzInput v-model="propertyForm.location_text" label="Searchable Location" />
          <select v-model="propertyForm.asset_type" class="pz-input">
            <option value="LAND">Land</option>
            <option value="RESIDENTIAL">Residential</option>
            <option value="COMMERCIAL">Commercial</option>
            <option value="INDUSTRIAL">Industrial</option>
            <option value="MIXED_USE">Mixed Use</option>
            <option value="HOSPITALITY">Hospitality</option>
            <option value="RENOVATION">Renovation</option>
            <option value="SPECIAL_PURPOSE">Special Purpose</option>
          </select>
          <select v-model="propertyForm.listing_type" class="pz-input">
            <option value="SALE">Sale</option>
            <option value="LEASE">Lease</option>
            <option value="DEVELOPMENT_OPPORTUNITY">Development Opportunity</option>
            <option value="COMPLETED_PROJECT">Completed Project</option>
          </select>
          <PzInput v-model="propertyForm.price_estimate" label="Estimated Value" type="number" required />
          <PzInput v-model="propertyForm.formatted_address" label="Formatted Address" />
        </div>

        <textarea
          v-model="propertyForm.description"
          class="pz-input"
          rows="4"
          placeholder="Describe the property, commercial positioning, and operating context"
        />

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Specifications</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Capture the facts users will compare quickly.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="specificationForm.bedrooms" label="Bedrooms" type="number" />
            <PzInput v-model="specificationForm.bathrooms" label="Bathrooms" type="number" />
            <PzInput v-model="specificationForm.parking_spaces" label="Parking Spaces" type="number" />
            <PzInput v-model="specificationForm.floors" label="Floors" type="number" />
            <PzInput v-model="specificationForm.internal_area" label="Internal Area" type="number" />
            <select v-model="specificationForm.internal_area_unit" class="pz-input">
              <option value="SQM">Square Meters</option>
              <option value="SQFT">Square Feet</option>
              <option value="ACRE">Acre</option>
              <option value="HECTARE">Hectare</option>
            </select>
            <PzInput v-model="specificationForm.lot_size" label="Lot Size" type="number" />
            <select v-model="specificationForm.lot_size_unit" class="pz-input">
              <option value="SQM">Square Meters</option>
              <option value="SQFT">Square Feet</option>
              <option value="ACRE">Acre</option>
              <option value="HECTARE">Hectare</option>
            </select>
            <select v-model="specificationForm.condition_rating" class="pz-input">
              <option value="">Condition Rating</option>
              <option value="SHELL">Shell</option>
              <option value="FAIR">Fair</option>
              <option value="GOOD">Good</option>
              <option value="EXCELLENT">Excellent</option>
            </select>
            <select v-model="specificationForm.occupancy_status" class="pz-input">
              <option value="">Occupancy Status</option>
              <option value="VACANT">Vacant</option>
              <option value="OCCUPIED">Occupied</option>
              <option value="OWNER_OCCUPIED">Owner Occupied</option>
              <option value="TENANTED">Tenanted</option>
              <option value="UNDER_CONSTRUCTION">Under Construction</option>
            </select>
          </div>
        </div>

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Pricing And Finance</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Expose commercial terms and financing posture.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="pricingForm.asking_price" label="Asking Price" type="number" />
            <PzInput v-model="pricingForm.rent_amount" label="Rent Amount" type="number" />
            <select v-model="pricingForm.currency" class="pz-input">
              <option v-for="currency in configStore.availableCurrencies" :key="currency.currency_code" :value="currency.currency_code">
                {{ currency.currency_code }}{{ currency.symbol ? ` (${currency.symbol})` : '' }}
              </option>
            </select>
            <select v-model="pricingForm.pricing_strategy" class="pz-input">
              <option value="FIXED">Fixed</option>
              <option value="NEGOTIABLE">Negotiable</option>
              <option value="PRICE_ON_APPLICATION">Price On Application</option>
              <option value="PER_UNIT">Per Unit</option>
            </select>
            <PzInput v-model="pricingForm.deposit_amount" label="Deposit Amount" type="number" />
            <label class="pz-checkbox-row">
              <input v-model="pricingForm.requires_deposit" type="checkbox" />
              <span>Requires deposit</span>
            </label>
            <label class="pz-checkbox-row">
              <input v-model="propertyForm.financing_allowed" type="checkbox" />
              <span>Financing allowed</span>
            </label>
            <label class="pz-checkbox-row">
              <input v-model="propertyForm.appointment_enabled" type="checkbox" />
              <span>Appointments enabled</span>
            </label>
          </div>
        </div>

        <div class="pz-manager-section">
          <div>
            <div class="pz-u-text-display text-sm">Development And Media</div>
            <div class="pz-u-text-mono text-xs pz-u-color-concrete">Publish due-diligence context and visual assets.</div>
          </div>
          <div class="pz-manager-form-grid">
            <PzInput v-model="developmentForm.zoning_info" label="Zoning" />
            <select v-model="developmentForm.development_stage" class="pz-input">
              <option value="">Development Stage</option>
              <option value="RAW_LAND">Raw Land</option>
              <option value="SERVICED_SITE">Serviced Site</option>
              <option value="IN_DESIGN">In Design</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
            </select>
            <PzInput v-model="developmentForm.recommended_use" label="Recommended Use" />
            <PzInput v-model="developmentForm.utilities_text" label="Utilities" placeholder="Water, Power, Fiber" />
            <PzInput v-model="mediaForm.primary_image_url" label="Primary Image URL" />
            <PzInput v-model="mediaForm.virtual_tour_url" label="Virtual Tour URL" />
            <label class="pz-checkbox-row">
              <input v-model="developmentForm.build_ready" type="checkbox" />
              <span>Build ready</span>
            </label>
          </div>
          <textarea v-model="propertyForm.feature_tags" class="pz-input" rows="3" placeholder="Feature highlights, comma separated" />
          <div class="pz-upload-grid">
            <div class="pz-upload-card">
              <div class="pz-upload-card__title">Property Images</div>
              <p class="pz-u-color-steel text-sm">Select one or more images. They upload after the listing is created.</p>
              <input ref="propertyImageInput" type="file" accept="image/*" multiple class="u-sr-only" @change="handlePropertyImagesSelected">
              <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                <Button type="button" variant="secondary" @click="triggerPropertyImageUpload">UPLOAD_IMAGES</Button>
                <Button v-if="selectedPropertyImageFiles.length" type="button" variant="ghost" @click="clearSelectedPropertyImages">CLEAR_IMAGES</Button>
              </div>
              <div v-if="selectedPropertyImageFiles.length" class="pz-upload-selection">
                {{ selectedPropertyImageFiles.length }} image{{ selectedPropertyImageFiles.length === 1 ? '' : 's' }} queued.
              </div>
            </div>

            <div class="pz-upload-card">
              <div class="pz-upload-card__title">Property Documents</div>
              <p class="pz-u-color-steel text-sm">Upload floor plans, brochures, or due-diligence documents after create.</p>
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Document upload type</label>
                <select v-model="propertyUploadDocumentType" class="pz-input">
                  <option value="DOCUMENT">Document</option>
                  <option value="FLOOR_PLAN">Floor Plan</option>
                </select>
              </div>
              <input ref="propertyDocumentInput" type="file" multiple class="u-sr-only" @change="handlePropertyDocumentsSelected">
              <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
                <Button type="button" variant="secondary" @click="triggerPropertyDocumentUpload">UPLOAD_DOCUMENTS</Button>
                <Button v-if="selectedPropertyDocumentFiles.length" type="button" variant="ghost" @click="clearSelectedPropertyDocuments">CLEAR_DOCUMENTS</Button>
              </div>
              <div v-if="selectedPropertyDocumentFiles.length" class="pz-upload-selection">
                <div
                  v-for="(file, idx) in selectedPropertyDocumentFiles"
                  :key="`${file.name}-${idx}`"
                  class="pz-document-category-row"
                >
                  <span>{{ file.name }}</span>
                  <select v-model="selectedPropertyDocumentCategories[idx]" class="pz-input">
                    <option value="GENERAL">General</option>
                    <option value="DEED">Title Deed</option>
                    <option value="FLOOR_PLAN">Floor Plan</option>
                    <option value="COMPLIANCE">Compliance</option>
                    <option value="SURVEY">Survey</option>
                    <option value="VALUATION">Valuation</option>
                    <option value="BROCHURE">Brochure</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closePropertyModal">Cancel</Button>
        <Button type="submit" form="property-form" variant="primary" :loading="submittingProperty" :disabled="creationReadinessScore < 45">Publish Listing</Button>
      </template>
    </Modal>

    <Modal :isOpen="showAvailabilityModal" title="PUBLISH_AVAILABILITY_WINDOWS" size="lg" @close="closeAvailabilityModal">
      <form id="availability-form" class="pz-space-y-4" @submit.prevent="createAvailability">
        <select v-model="availabilityForm.property" class="pz-input">
          <option disabled value="">Select property</option>
          <option v-for="item in properties" :key="item.id" :value="item.id">{{ item.title }}</option>
        </select>
        <PzInput v-model="availabilityForm.start_at" label="Start" type="datetime-local" required />
        <PzInput v-model="availabilityForm.end_at" label="End" type="datetime-local" required />
        <PzInput v-model="availabilityForm.slot_duration_minutes" label="Slot Duration (minutes)" type="number" required />
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeAvailabilityModal">Cancel</Button>
        <Button type="submit" form="availability-form" variant="primary" :loading="submittingAvailability">Publish Slots</Button>
      </template>
    </Modal>

    <nav class="pz-property-mobile-nav">
      <button type="button" @click="activeSection = 'listings'">Portfolio</button>
      <button type="button" @click="openPropertyModal">Publish</button>
      <button type="button" @click="activeSection = 'leads'">Leads</button>
      <button type="button" @click="activeSection = 'appointments'">Visits</button>
      <button type="button" @click="activeSection = 'verification'">Review</button>
    </nav>
  </DashboardShell>
</template>

<script setup>
import { inject, onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useConfigStore } from '../stores/config';
import Card from '../components/ui/Card.vue';
import WorkflowGuide from '../components/ui/WorkflowGuide.vue';
import ModuleCTA from '../components/ui/ModuleCTA.vue';
import Button from '../components/ui/Button.vue';
import EmptyState from '../components/ui/EmptyState.vue';
import PzInput from '../components/PzInput.vue';
import DashboardShell from '../components/layout/DashboardShell.vue';
import Modal from '../components/ui/Modal.vue';
import PropertyNotificationPanel from '../components/property/PropertyNotificationPanel.vue';
import PropertyActivityTimeline from '../components/property/PropertyActivityTimeline.vue';

const configStore = useConfigStore();
const authStore = useAuthStore();
const router = useRouter();
const showAlert = inject('showAlert');

const activeSection = ref('listings');
const activityView = ref('alerts');

const properties = ref([]);
const inquiries = ref([]);
const appointments = ref([]);
const portfolioAnalytics = ref(null);
const backendRecommendations = ref([]);
const approvalQueue = ref([]);
const selectedProperties = ref([]);
const submittingProperty = ref(false);
const submittingAvailability = ref(false);
const showPropertyModal = ref(false);
const showAvailabilityModal = ref(false);
const propertyImageInput = ref(null);
const propertyDocumentInput = ref(null);
const selectedPropertyImageFiles = ref([]);
const selectedPropertyDocumentFiles = ref([]);
const selectedPropertyDocumentCategories = ref([]);
const propertyUploadDocumentType = ref('DOCUMENT');
const activeTemplate = ref('residential');

const dashboardProfile = computed(() => {
  if (authStore.hasRole('SURVEYOR')) {
    return {
      title: 'Surveyor Hub',
      eyebrow: 'VALUATION & VERIFICATION',
      canCreateListing: false,
      canManageAppointments: false,
      canVerify: true,
    };
  }
  if (authStore.hasRole('REAL_ESTATE_AGENT')) {
    return {
      title: 'Agent Hub',
      eyebrow: 'SALES & LISTING OPERATIONS',
      canCreateListing: true,
      canManageAppointments: true,
      canVerify: false,
    };
  }
  return {
    title: 'Property Manager Hub',
    eyebrow: 'PROPERTY OPERATIONS',
    canCreateListing: true,
    canManageAppointments: true,
    canVerify: false,
  };
});

const dashboardTitle = computed(() => dashboardProfile.value.title);
const dashboardEyebrow = computed(() => dashboardProfile.value.eyebrow);
const canCreateListing = computed(() => dashboardProfile.value.canCreateListing);
const canManageAppointments = computed(() => dashboardProfile.value.canManageAppointments);
const canVerify = computed(() => dashboardProfile.value.canVerify);

const quickstats = computed(() => [
  { label: 'Listings', value: properties.value.length },
  { label: 'Leads', value: inquiries.value.length },
  { label: 'Appointments', value: appointments.value.length },
]);

const performanceMetrics = computed(() => [
  { label: 'Total Views', value: portfolioAnalytics.value?.total_views || 0 },
  { label: 'Inquiries', value: portfolioAnalytics.value?.inquiries_this_month ?? inquiries.value.length },
  { label: 'Appointments', value: portfolioAnalytics.value?.appointments_booked ?? appointments.value.length },
  { label: 'Conversion', value: `${portfolioAnalytics.value?.conversion_rate || 0}%` },
]);

const workflowSummary = computed(() => {
  if (!properties.value.length) {
    return {
      stage: 'LISTING_SETUP',
      title: 'Create a property listing to start the workflow',
      body: 'Add a property, then publish availability so visitors can book and inquire without extra help.',
      primaryAction: { label: 'Create Listing', handler: openPropertyModal },
      secondaryAction: canManageAppointments.value ? { label: 'Publish Availability', handler: openAvailabilityModal } : null,
    };
  }

  if (inquiries.value.length === 0 && appointments.value.length === 0) {
    return {
      stage: 'LISTING_PUBLISHED',
      title: 'Your properties are live. Now make them easier to act on.',
      body: 'Publish availability, add more media if needed, and link the strongest development opportunities to projects.',
      primaryAction: canManageAppointments.value ? { label: 'Publish Availability', handler: openAvailabilityModal } : { label: 'Create Listing', handler: openPropertyModal },
      secondaryAction: { label: 'Refresh', handler: loadDashboard },
    };
  }

  if (inquiries.value.length > 0 && appointments.value.length === 0) {
    return {
      stage: 'LEAD_FLOW_ACTIVE',
      title: 'Leads are coming in. Focus on response and booking.',
      body: 'Answer inquiries, publish visit slots, and keep the conversation moving so prospects do not stall.',
      primaryAction: { label: 'Review Leads', handler: () => { activeSection.value = 'leads'; } },
      secondaryAction: canManageAppointments.value ? { label: 'Publish Availability', handler: openAvailabilityModal } : { label: 'Refresh', handler: loadDashboard },
    };
  }

  return {
    stage: 'OPERATIONS_ACTIVE',
    title: 'Properties, leads, and appointments are all in motion.',
    body: 'Keep listings current, maintain availability, and review the latest inquiries and appointments as they arrive.',
    primaryAction: { label: 'Review Appointments', handler: () => { activeSection.value = 'appointments'; } },
    secondaryAction: { label: 'Review Leads', handler: () => { activeSection.value = 'leads'; } },
  };
});

const workflowSteps = computed(() => [
  {
    index: '01',
    label: 'Create Listing',
    help: 'Publish a property with enough detail to be discoverable.',
    done: properties.value.length > 0,
    active: properties.value.length === 0,
  },
  {
    index: '02',
    label: 'Publish Availability',
    help: 'Open visit slots so people can book without calling first.',
    done: appointments.value.length > 0,
    active: properties.value.length > 0 && appointments.value.length === 0,
  },
  {
    index: '03',
    label: 'Respond to Leads',
    help: 'Answer inquiries promptly to keep interest warm.',
    done: inquiries.value.length > 0,
    active: inquiries.value.length > 0,
  },
  {
    index: '04',
    label: 'Link to Project',
    help: 'Move development opportunities into execution when ready.',
    done: properties.value.some((item) => item.linked_project_count),
    active: properties.value.some((item) => item.development_stage && item.development_stage !== 'COMPLETED'),
  },
]);

const healthSnapshot = computed(() => {
  const healthy = properties.value.filter((item) => getPropertyHealthScore(item) >= 80).length;
  const attention = properties.value.filter((item) => getPropertyHealthScore(item) >= 50 && getPropertyHealthScore(item) < 80).length;
  const blocked = properties.value.filter((item) => getPropertyHealthScore(item) < 50).length;
  const active = properties.value.filter((item) => item.status === 'ACTIVE').length;
  return [
    { label: 'Healthy', value: healthy },
    { label: 'Needs Attention', value: attention },
    { label: 'Blocked', value: blocked },
    { label: 'Active Listings', value: active },
  ];
});

const overviewMetrics = computed(() => [
  {
    label: 'Urgent',
    value: urgentActions.value.length,
    body: 'Actions needing attention now',
    action: () => {
      if (urgentActions.value[0]?.handler) {
        urgentActions.value[0].handler();
      } else {
        activeSection.value = 'listings';
      }
    },
  },
  {
    label: 'Health',
    value: `${workspaceHealthScore.value}%`,
    body: workspaceHealthLabel.value,
    action: () => {
      activeSection.value = 'listings';
    },
  },
  {
    label: 'Leads',
    value: inquiries.value.length,
    body: 'Waiting on reply',
    action: () => {
      activeSection.value = 'leads';
    },
  },
  {
    label: 'Appointments',
    value: appointments.value.length,
    body: 'Scheduled visits',
    action: () => {
      activeSection.value = 'appointments';
    },
  },
]);

const workspaceHealthScore = computed(() => {
  if (!properties.value.length) return 0;
  const total = properties.value.reduce((sum, item) => sum + getPropertyHealthScore(item), 0);
  return Math.round(total / properties.value.length);
});

const workspaceHealthLabel = computed(() => {
  const score = workspaceHealthScore.value;
  if (score >= 90) return 'Excellent';
  if (score >= 70) return 'Good';
  if (score >= 50) return 'Fair';
  if (score >= 30) return 'Needs Work';
  return 'At Risk';
});

const urgentActions = computed(() => {
  const actions = backendRecommendations.value.slice(0, 3).map((item) => ({
    label: item.type === 'MISSING_VISIT_SLOTS' ? 'Add visit slots' : item.type === 'STALE_INQUIRY' ? 'Respond to inquiry' : 'Improve listing',
    body: item.reason,
    handler: () => {
      if (item.property_id && item.type === 'INCOMPLETE_LISTING') router.push(`/properties/${item.property_id}/edit`);
      else activeSection.value = item.type === 'STALE_INQUIRY' ? 'leads' : 'availability';
    },
  }));
  const incompleteListing = properties.value.find((item) => getPropertyHealthScore(item) < 80);
  const leadCount = inquiries.value.length;
  const appointmentCount = appointments.value.length;

  if (incompleteListing) {
    actions.push({
      label: `Complete ${incompleteListing.title || 'property listing'}`,
      body: getPropertyHealth(incompleteListing).summary,
      handler: () => router.push(`/properties/${incompleteListing.id}/edit`),
    });
  }
  if (leadCount) {
    actions.push({
      label: 'Review incoming leads',
      body: `${leadCount} ${leadCount === 1 ? 'inquiry' : 'inquiries'} are waiting for follow-up.`,
      handler: () => { activeSection.value = 'leads'; },
    });
  }
  if (appointmentCount) {
    actions.push({
      label: 'Review appointments',
      body: `${appointmentCount} appointment${appointmentCount === 1 ? '' : 's'} are scheduled or pending confirmation.`,
      handler: () => { activeSection.value = 'appointments'; },
    });
  }
  return actions.slice(0, 3);
});

const propertyNotifications = computed(() => {
  const items = [];
  inquiries.value.slice(0, 3).forEach((inquiry) => {
    items.push({
      id: `inq-${inquiry.id}`,
      icon: '✉️',
      title: 'Inquiry waiting for reply',
      message: `${inquiry.full_name} asked about ${inquiry.property_title}.`,
      timestamp: inquiry.created_at || new Date().toISOString(),
      read: false,
      actionLabel: 'Open',
      data: { type: 'inquiry', id: inquiry.id },
    });
  });
  appointments.value.slice(0, 3).forEach((appointment) => {
    items.push({
      id: `appt-${appointment.id}`,
      icon: '🗓',
      title: 'Appointment scheduled',
      message: `${appointment.full_name} booked ${appointment.property_title}.`,
      timestamp: appointment.created_at || appointment.scheduled_start || new Date().toISOString(),
      read: true,
      actionLabel: 'Review',
      data: { type: 'appointment', id: appointment.id },
    });
  });
  properties.value.filter((item) => getPropertyHealthScore(item) < 80).slice(0, 2).forEach((item) => {
    items.push({
      id: `prop-${item.id}`,
      icon: '⚠️',
      title: 'Property needs attention',
      message: `${item.title || 'A property'} needs updates before it is fully ready.`,
      timestamp: item.updated_at || new Date().toISOString(),
      read: false,
      actionLabel: 'Fix',
      data: { type: 'property', id: item.id },
    });
  });
  return items.slice(0, 6);
});

const propertyTimeline = computed(() => {
  const events = [];
  properties.value.slice(0, 3).forEach((item) => {
    events.push({
      id: `created-${item.id}`,
      title: item.status === 'DRAFT' ? 'Draft listing ready' : 'Property updated',
      message: `${item.title || 'Listing'} is ${String(item.status || 'unknown').toLowerCase()} and can move to the next step.`,
      timestamp: item.updated_at || item.created_at || new Date().toISOString(),
      variant: item.status === 'ACTIVE' ? 'success' : 'info',
    });
  });
  inquiries.value.slice(0, 3).forEach((inquiry) => {
    events.push({
      id: `timeline-inquiry-${inquiry.id}`,
      title: 'Inquiry received',
      message: `${inquiry.full_name} submitted a ${String(inquiry.inquiry_type || 'general').toLowerCase()} inquiry.`,
      timestamp: inquiry.created_at || new Date().toISOString(),
      variant: 'warn',
    });
  });
  appointments.value.slice(0, 3).forEach((appointment) => {
    events.push({
      id: `timeline-appt-${appointment.id}`,
      title: 'Appointment booked',
      message: `${appointment.full_name} booked ${appointment.property_title}.`,
      timestamp: appointment.created_at || appointment.scheduled_start || new Date().toISOString(),
      variant: 'success',
    });
  });
  return events.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 6);
});

const navGroups = computed(() => {
  const items = [
    { id: 'listings', label: 'Publish Property', icon: '🏠' },
  ];
  if (canManageAppointments.value) {
    items.push({ id: 'availability', label: 'Book Visits', icon: '🗓' });
  }
  items.push({ id: 'leads', label: 'Review Leads', icon: '📭' });
  if (canManageAppointments.value) {
    items.push({ id: 'appointments', label: 'Visit Outcomes', icon: '⏰' });
  }
  if (canVerify.value) {
    items.push({ id: 'verification', label: 'Verification Queue', icon: '✓' });
  }
  return [
    {
      title: 'Property Operations',
      items,
    },
    {
      title: 'System',
      items: [
        { id: 'exit', label: 'Exit Console', icon: '⇚', action: () => { window.location.href = '/'; } },
      ],
    },
  ];
});

const propertyForm = ref({
  title: '',
  description: '',
  asset_type: 'RESIDENTIAL',
  listing_type: 'SALE',
  price_estimate: '',
  location_text: '',
  formatted_address: '',
  financing_allowed: false,
  appointment_enabled: true,
  inquiry_enabled: true,
  manager: '',
  feature_tags: '',
});

const specificationForm = ref({
  bedrooms: '',
  bathrooms: '',
  floors: '',
  parking_spaces: '',
  internal_area: '',
  internal_area_unit: 'SQM',
  lot_size: '',
  lot_size_unit: 'SQM',
  condition_rating: '',
  occupancy_status: '',
});

const pricingForm = ref({
  currency: configStore.activeCurrencyCode || 'KES',
  asking_price: '',
  rent_amount: '',
  pricing_strategy: 'FIXED',
  requires_deposit: false,
  deposit_amount: '',
});

const developmentForm = ref({
  zoning_info: '',
  build_ready: false,
  development_stage: '',
  recommended_use: '',
  utilities_text: '',
});

const mediaForm = ref({
  primary_image_url: '',
  virtual_tour_url: '',
});

const propertyTemplates = [
  {
    id: 'residential',
    label: 'Residential',
    help: 'Homes, apartments, and estates',
    values: {
      asset_type: 'RESIDENTIAL',
      listing_type: 'SALE',
      features: 'Secure parking, Water connection, Nearby schools',
      specification: { bedrooms: 3, bathrooms: 2, condition_rating: 'GOOD', occupancy_status: 'VACANT' },
    },
  },
  {
    id: 'commercial',
    label: 'Commercial',
    help: 'Retail, office, and industrial sites',
    values: {
      asset_type: 'COMMERCIAL',
      listing_type: 'LEASE',
      features: 'Truck access, Power backup, High visibility frontage',
      specification: { parking_spaces: 4, condition_rating: 'GOOD', occupancy_status: 'VACANT' },
    },
  },
  {
    id: 'land',
    label: 'Land',
    help: 'Plots and serviced sites',
    values: {
      asset_type: 'LAND',
      listing_type: 'DEVELOPMENT_OPPORTUNITY',
      features: 'Surveyed, Road access, Utility corridor',
      development: { development_stage: 'SERVICED_SITE', build_ready: true },
    },
  },
  {
    id: 'mixed',
    label: 'Mixed Use',
    help: 'Development-ready mixed assets',
    values: {
      asset_type: 'MIXED_USE',
      listing_type: 'DEVELOPMENT_OPPORTUNITY',
      features: 'Mixed zoning, Anchor retail frontage, Residential density',
      development: { development_stage: 'IN_DESIGN', build_ready: false },
    },
  },
];

const creationReadinessScore = computed(() => {
  let score = 0;
  if (propertyForm.value.title?.trim()) score += 18;
  if (propertyForm.value.location_text?.trim() || propertyForm.value.formatted_address?.trim()) score += 18;
  if (numberOrNull(propertyForm.value.price_estimate) !== null || numberOrNull(pricingForm.value.asking_price) !== null) score += 18;
  if (propertyForm.value.description?.trim()) score += 14;
  if (propertyForm.value.asset_type && propertyForm.value.listing_type) score += 10;
  if (specificationForm.value.bedrooms || specificationForm.value.internal_area || specificationForm.value.lot_size) score += 8;
  if (developmentForm.value.development_stage || developmentForm.value.zoning_info) score += 7;
  if (selectedPropertyImageFiles.value.length || mediaForm.value.primary_image_url) score += 7;
  return Math.min(score, 100);
});

const propertyGroups = computed(() => [
  { id: 'attention', label: 'Needs Attention', items: properties.value.filter((item) => getPropertyHealthScore(item) < 75 && item.status !== 'DRAFT') },
  { id: 'healthy', label: 'Active & Healthy', items: properties.value.filter((item) => getPropertyHealthScore(item) >= 75 && item.status === 'ACTIVE') },
  { id: 'drafts', label: 'Drafts', items: properties.value.filter((item) => item.status === 'DRAFT' || item.status === 'PENDING_REVIEW') },
  { id: 'archived', label: 'Archived', items: properties.value.filter((item) => ['INACTIVE', 'SOLD', 'LEASED'].includes(item.status)) },
]);

const availabilityForm = ref({
  property: '',
  start_at: '',
  end_at: '',
  slot_duration_minutes: 60,
});

function formatDateTime(value) {
  return new Date(value).toLocaleString();
}

function getPropertyHealthScore(item) {
  let score = 0;
  if (item.title) score += 20;
  if (item.location_text || item.formatted_address) score += 15;
  if (item.price_estimate || item.pricing_profile?.asking_price || item.pricing_profile?.rent_amount) score += 15;
  if (item.description) score += 10;
  if (item.media_assets?.length) score += 15;
  if (item.inquiry_enabled !== false) score += 5;
  if (item.appointment_enabled) score += 5;
  if (item.pricing_profile?.pricing_strategy) score += 5;
  if (item.development_metadata?.development_stage) score += 5;
  if (item.ownership_profile?.legal_owner_name) score += 5;
  return score;
}

function getPropertyHealth(item) {
  const score = getPropertyHealthScore(item);
  if (score >= 90) {
    return { label: 'Ready', summary: 'Listing is complete and visible to buyers.' };
  }
  if (score >= 75) {
    return { label: 'Nearly Ready', summary: 'A few missing details may still reduce trust or reach.' };
  }
  if (score >= 50) {
    return { label: 'Needs Work', summary: 'Open the listing and finish the missing sections.' };
  }
  return { label: 'Blocked', summary: 'Key listing details are missing and publishing is still risky.' };
}

function handlePropertyNotificationAction(notification) {
  if (!notification?.data) return;
  if (notification.data.type === 'inquiry') {
    activeSection.value = 'leads';
    return;
  }
  if (notification.data.type === 'appointment') {
    activeSection.value = 'appointments';
    return;
  }
  if (notification.data.type === 'property' && notification.data.id) {
    router.push(`/properties/${notification.data.id}`);
  }
}

function numberOrNull(value) {
  return value === '' || value === null || value === undefined ? null : Number(value);
}

function resetPropertyForm() {
  propertyForm.value = {
    title: '',
    description: '',
    asset_type: 'RESIDENTIAL',
    listing_type: 'SALE',
    price_estimate: '',
    location_text: '',
    formatted_address: '',
    financing_allowed: false,
    appointment_enabled: true,
    inquiry_enabled: true,
    manager: '',
    feature_tags: '',
  };
  specificationForm.value = {
    bedrooms: '',
    bathrooms: '',
    floors: '',
    parking_spaces: '',
    internal_area: '',
    internal_area_unit: 'SQM',
    lot_size: '',
    lot_size_unit: 'SQM',
    condition_rating: '',
    occupancy_status: '',
  };
  pricingForm.value = {
    currency: configStore.activeCurrencyCode || 'KES',
    asking_price: '',
    rent_amount: '',
    pricing_strategy: 'FIXED',
    requires_deposit: false,
    deposit_amount: '',
  };
  developmentForm.value = {
    zoning_info: '',
    build_ready: false,
    development_stage: '',
    recommended_use: '',
    utilities_text: '',
  };
  mediaForm.value = {
    primary_image_url: '',
    virtual_tour_url: '',
  };
  selectedPropertyImageFiles.value = [];
  selectedPropertyDocumentFiles.value = [];
  propertyUploadDocumentType.value = 'DOCUMENT';
  activeTemplate.value = 'residential';
  if (propertyImageInput.value) propertyImageInput.value.value = '';
  if (propertyDocumentInput.value) propertyDocumentInput.value.value = '';
}

function applyPropertyTemplate(templateId) {
  const template = propertyTemplates.find((item) => item.id === templateId);
  if (!template) return;
  activeTemplate.value = templateId;
  propertyForm.value.asset_type = template.values.asset_type;
  propertyForm.value.listing_type = template.values.listing_type;
  propertyForm.value.feature_tags = template.values.features;
  specificationForm.value = { ...specificationForm.value, ...(template.values.specification || {}) };
  developmentForm.value = { ...developmentForm.value, ...(template.values.development || {}) };
}

function openLowestHealthListing() {
  const item = [...properties.value].sort((a, b) => getPropertyHealthScore(a) - getPropertyHealthScore(b))[0];
  if (item?.id) router.push(`/properties/${item.id}/edit`);
  else openPropertyModal();
}

function resetAvailabilityForm() {
  availabilityForm.value = { property: '', start_at: '', end_at: '', slot_duration_minutes: 60 };
}

function openPropertyModal() {
  showPropertyModal.value = true;
}

function closePropertyModal() {
  showPropertyModal.value = false;
  resetPropertyForm();
}

function openAvailabilityModal() {
  showAvailabilityModal.value = true;
}

function closeAvailabilityModal() {
  showAvailabilityModal.value = false;
}

function triggerPropertyImageUpload() {
  propertyImageInput.value?.click();
}

function triggerPropertyDocumentUpload() {
  propertyDocumentInput.value?.click();
}

function handlePropertyImagesSelected(event) {
  selectedPropertyImageFiles.value = Array.from(event.target.files || []);
}

function handlePropertyDocumentsSelected(event) {
  selectedPropertyDocumentFiles.value = Array.from(event.target.files || []);
  selectedPropertyDocumentCategories.value = selectedPropertyDocumentFiles.value.map(() => propertyUploadDocumentType.value === 'FLOOR_PLAN' ? 'FLOOR_PLAN' : 'GENERAL');
}

function clearSelectedPropertyImages() {
  selectedPropertyImageFiles.value = [];
  if (propertyImageInput.value) propertyImageInput.value.value = '';
}

function clearSelectedPropertyDocuments() {
  selectedPropertyDocumentFiles.value = [];
  selectedPropertyDocumentCategories.value = [];
  if (propertyDocumentInput.value) propertyDocumentInput.value.value = '';
}

async function loadDashboard() {
  try {
    const [propertiesRes, inquiriesRes, appointmentsRes, analyticsRes, recommendationsRes, approvalRes] = await Promise.all([
      api.get('/property/mine/'),
      api.get('/property/inquiries/'),
      api.get('/property/appointments/'),
      api.get('/property/analytics/').catch(() => ({ data: null })),
      api.get('/property/manager/recommendations/').catch(() => ({ data: [] })),
      canVerify.value ? api.get('/property/', { params: { status: 'PENDING_REVIEW' } }).catch(() => ({ data: [] })) : Promise.resolve({ data: [] }),
    ]);
    properties.value = propertiesRes.data.results || propertiesRes.data;
    inquiries.value = inquiriesRes.data.results || inquiriesRes.data;
    appointments.value = appointmentsRes.data.results || appointmentsRes.data;
    portfolioAnalytics.value = analyticsRes.data;
    backendRecommendations.value = recommendationsRes.data.results || recommendationsRes.data || [];
    approvalQueue.value = approvalRes.data.results || approvalRes.data || [];
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to load property manager dashboard.', 'error');
  }
}

async function createProperty() {
  submittingProperty.value = true;
  try {
    const featureNames = propertyForm.value.feature_tags
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);

    const mediaAssets = [
      mediaForm.value.primary_image_url
        ? {
            media_type: 'IMAGE',
            external_url: mediaForm.value.primary_image_url,
            title: 'Primary property image',
            is_primary: true,
            is_public: true,
          }
        : null,
      mediaForm.value.virtual_tour_url
        ? {
            media_type: 'VIRTUAL_TOUR',
            external_url: mediaForm.value.virtual_tour_url,
            title: 'Virtual tour',
            is_public: true,
          }
        : null,
    ].filter(Boolean);

    const specification = {
      bedrooms: numberOrNull(specificationForm.value.bedrooms),
      bathrooms: numberOrNull(specificationForm.value.bathrooms),
      floors: numberOrNull(specificationForm.value.floors),
      parking_spaces: numberOrNull(specificationForm.value.parking_spaces),
      internal_area: numberOrNull(specificationForm.value.internal_area),
      internal_area_unit: specificationForm.value.internal_area_unit,
      lot_size: numberOrNull(specificationForm.value.lot_size),
      lot_size_unit: specificationForm.value.lot_size_unit,
      condition_rating: specificationForm.value.condition_rating,
      occupancy_status: specificationForm.value.occupancy_status,
    };

    const pricingProfile = {
      currency: pricingForm.value.currency || configStore.activeCurrencyCode || 'KES',
      asking_price: numberOrNull(pricingForm.value.asking_price),
      rent_amount: numberOrNull(pricingForm.value.rent_amount),
      pricing_strategy: pricingForm.value.pricing_strategy,
      requires_deposit: pricingForm.value.requires_deposit,
      deposit_amount: numberOrNull(pricingForm.value.deposit_amount),
    };

    const hasDevelopmentData = Boolean(
      developmentForm.value.zoning_info
      || developmentForm.value.development_stage
      || developmentForm.value.recommended_use
      || developmentForm.value.utilities_text
      || developmentForm.value.build_ready
    );

    const payload = {
      title: propertyForm.value.title,
      description: propertyForm.value.description,
      asset_type: propertyForm.value.asset_type,
      listing_type: propertyForm.value.listing_type,
      price_estimate: numberOrNull(propertyForm.value.price_estimate),
      location_text: propertyForm.value.location_text,
      formatted_address: propertyForm.value.formatted_address,
      financing_allowed: propertyForm.value.financing_allowed,
      appointment_enabled: propertyForm.value.appointment_enabled,
      inquiry_enabled: propertyForm.value.inquiry_enabled,
      manager: authStore.hasRole('PROPERTY_MANAGER') ? authStore.user?.id : null,
      specification,
      pricing_profile: pricingProfile,
      features: featureNames.map((name, index) => ({
        name,
        category: 'Highlight',
        is_highlighted: index < 6,
        sort_order: index + 1,
      })),
      media_assets: mediaAssets,
    };

    if (hasDevelopmentData) {
      payload.development_metadata = {
        zoning_info: developmentForm.value.zoning_info,
        build_ready: developmentForm.value.build_ready,
        utilities_available: developmentForm.value.utilities_text.split(',').map((item) => item.trim()).filter(Boolean),
        development_stage: developmentForm.value.development_stage,
        recommended_use: developmentForm.value.recommended_use,
      };
    }

    const response = await api.post('/property/', payload);
    if (response.data?.id) {
      await uploadPropertyAssets(response.data.id);
    }
    showAlert?.('Property listing created.', 'success');
    resetPropertyForm();
    closePropertyModal();
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to create property listing.', 'error');
  } finally {
    submittingProperty.value = false;
  }
}

async function uploadPropertyAssets(propertyId) {
  if (selectedPropertyImageFiles.value.length) {
    const imageData = new FormData();
    imageData.append('media_type', 'IMAGE');
    selectedPropertyImageFiles.value.forEach((file) => imageData.append('files', file));
    await api.post(`/property/${propertyId}/upload-media/`, imageData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }

  if (selectedPropertyDocumentFiles.value.length) {
      const documentData = new FormData();
      documentData.append('media_type', propertyUploadDocumentType.value);
      selectedPropertyDocumentFiles.value.forEach((file, idx) => {
        documentData.append('files', file);
        documentData.append(`document_category_${idx}`, selectedPropertyDocumentCategories.value[idx] || 'GENERAL');
      });
      await api.post(`/property/${propertyId}/upload-media/`, documentData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }
}

async function updateAppointmentStatus(appointment, action) {
  try {
    await api.post(`/property/appointments/${appointment.id}/${action}/`, {});
    showAlert?.('Appointment updated.', 'success');
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to update appointment.', 'error');
  }
}

async function captureVisitOutcome(appointment) {
  const notes = window.prompt('Visit outcome: Interested, Not Interested, or Follow-up Required');
  if (!notes) return;
  try {
    await api.post(`/property/appointments/${appointment.id}/complete/`, { notes });
    showAlert?.('Visit outcome saved.', 'success');
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to save visit outcome.', 'error');
  }
}

async function moderateProperty(item, decision) {
  const notes = decision === 'approve' ? '' : window.prompt('Moderation notes') || '';
  try {
    await api.post(`/property/${item.id}/moderate/`, { decision, notes });
    showAlert?.('Moderation updated.', 'success');
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to moderate property.', 'error');
  }
}

async function bulkUpdateStatus(status) {
  try {
    await Promise.all(selectedProperties.value.map((id) => api.patch(`/property/${id}/`, { status })));
    selectedProperties.value = [];
    showAlert?.('Properties updated.', 'success');
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to update selected properties.', 'error');
  }
}

async function createAvailability() {
  submittingAvailability.value = true;
  try {
    await api.post('/property/availability-windows/', availabilityForm.value);
    showAlert?.('Availability published.', 'success');
    resetAvailabilityForm();
    closeAvailabilityModal();
    await loadDashboard();
  } catch (error) {
    showAlert?.(error.response?.data?.detail || 'Failed to publish availability.', 'error');
  } finally {
    submittingAvailability.value = false;
  }
}

onMounted(loadDashboard);
</script>

<style scoped>
.pz-manager-form-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
}

.pz-ops-snapshot-card :deep(.pz-card),
.pz-activity-shell :deep(.pz-card),
.pz-manager-layout :deep(.pz-card) {
  border-radius: 12px;
  box-shadow:
    0 1px 2px rgba(10, 10, 15, 0.03),
    0 8px 20px rgba(10, 10, 15, 0.04);
}

.pz-ops-snapshot-card :deep(.pz-card__header),
.pz-activity-shell :deep(.pz-card__header),
.pz-manager-layout :deep(.pz-card__header) {
  padding: 0.85rem 1rem 0.7rem;
}

.pz-ops-snapshot-card :deep(.pz-card__body),
.pz-activity-shell :deep(.pz-card__body),
.pz-manager-layout :deep(.pz-card__body) {
  padding: 1rem;
}

.pz-ops-snapshot-card :deep(.pz-card__title),
.pz-activity-shell :deep(.pz-card__title),
.pz-manager-layout :deep(.pz-card__title) {
  font-size: 0.98rem;
}

.pz-ops-snapshot-card :deep(.pz-card__eyebrow),
.pz-activity-shell :deep(.pz-card__eyebrow),
.pz-manager-layout :deep(.pz-card__eyebrow) {
  font-size: 0.62rem;
}

.pz-manager-layout {
  display: grid;
  gap: 2rem;
  grid-template-columns: 1fr;
}

.pz-property-groups,
.pz-property-group {
  display: grid;
  gap: 1rem;
}

.pz-property-group__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.7rem 0.85rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.66);
  border-radius: 8px;
}

.pz-workflow-banner {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: start;
}

.pz-workflow-banner__summary {
  display: grid;
  gap: 0.5rem;
}

.pz-workflow-banner__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-workflow-banner__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.1rem, 2.4vw, 1.6rem);
}

.pz-workflow-banner__body {
  max-width: 60ch;
  color: var(--pz-color-text-secondary);
  line-height: 1.6;
}

.pz-workflow-banner__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: flex-end;
}

.pz-workflow-banner__steps {
  display: grid;
  gap: 0.75rem;
  margin-top: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.pz-workflow-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
  padding: 0.85rem 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.84);
}

.pz-workflow-step__icon {
  display: inline-flex;
  width: 1.9rem;
  height: 1.9rem;
  align-items: center;
  justify-content: center;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  border: 1px solid rgba(10, 10, 15, 0.12);
  background: rgba(247, 244, 239, 0.95);
}

.pz-workflow-step__content {
  display: grid;
  gap: 0.2rem;
  min-width: 0;
}

.pz-workflow-step__content strong {
  font-size: 0.82rem;
}

.pz-workflow-step__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
  line-height: 1.5;
}

.pz-workflow-step--done {
  border-color: rgba(5, 150, 105, 0.28);
}

.pz-workflow-step--done .pz-workflow-step__icon {
  background: rgba(5, 150, 105, 0.12);
  border-color: rgba(5, 150, 105, 0.25);
}

.pz-workflow-step--active {
  border-color: rgba(212, 101, 42, 0.35);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-ops-snapshot {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.95fr);
  align-items: start;
}

.pz-ops-snapshot__summary {
  display: grid;
  gap: 0.65rem;
}

.pz-ops-snapshot__kicker {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-ops-snapshot__dot {
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 50%;
  background: var(--pz-color-earth-orange);
}

.pz-ops-snapshot__title {
  margin: 0;
  font-family: var(--pz-font-display);
  font-size: clamp(1.05rem, 2vw, 1.45rem);
}

.pz-ops-snapshot__body {
  max-width: 56ch;
  margin: 0;
  color: var(--pz-color-text-secondary);
  line-height: 1.55;
}

.pz-ops-snapshot__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.pz-ops-snapshot__metrics {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pz-ops-metric {
  display: grid;
  gap: 0.2rem;
  padding: 0.85rem 0.95rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.92);
  text-align: left;
  border-radius: 10px;
}

.pz-ops-metric__label {
  font-family: var(--pz-font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-ops-metric__value {
  font-family: var(--pz-font-display);
  font-size: 1rem;
  color: var(--pz-color-foundation-black);
}

.pz-ops-metric__body {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  line-height: 1.45;
  color: var(--pz-color-concrete-grey);
}

.pz-performance-strip,
.pz-template-picker {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
}

.pz-performance-metric,
.pz-template-picker__item {
  display: grid;
  gap: 0.25rem;
  padding: 0.85rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(255, 255, 255, 0.92);
  text-align: left;
  border-radius: 8px;
}

.pz-performance-metric span,
.pz-template-picker__item span {
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  color: var(--pz-color-concrete-grey);
}

.pz-performance-metric strong,
.pz-template-picker__item strong {
  font-family: var(--pz-font-display);
  color: var(--pz-color-foundation-black);
}

.pz-template-picker__item.is-active {
  border-color: rgba(212, 101, 42, 0.34);
  box-shadow: 0 0 0 1px rgba(212, 101, 42, 0.08);
}

.pz-readiness-meter {
  display: grid;
  grid-template-columns: auto minmax(8rem, 1fr) auto;
  gap: 0.75rem;
  align-items: center;
  padding: 0.8rem 0.9rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 8px;
  background: rgba(247, 244, 239, 0.66);
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
}

.pz-readiness-meter__bar {
  height: 0.5rem;
  background: rgba(10, 10, 15, 0.08);
  overflow: hidden;
  border-radius: 999px;
}

.pz-readiness-meter__bar i {
  display: block;
  height: 100%;
  background: var(--pz-color-earth-orange);
}

.pz-bulk-actions,
.pz-manager-feed__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.pz-bulk-actions {
  position: sticky;
  bottom: 1rem;
  z-index: 12;
  padding: 0.75rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 24px rgba(10, 10, 15, 0.08);
}

.pz-bulk-actions span,
.pz-document-category-row span {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  color: var(--pz-color-concrete-grey);
}

.pz-document-category-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(9rem, 12rem);
  gap: 0.65rem;
  align-items: center;
}

.pz-activity-shell {
  display: grid;
  gap: 0.9rem;
}

.pz-activity-shell__tabs {
  display: inline-flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pz-activity-shell__tabs :deep(.is-active) {
  background: rgba(212, 101, 42, 0.1);
  border-color: rgba(212, 101, 42, 0.35);
  color: var(--pz-color-earth-orange);
}

.pz-manager-section {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(20, 20, 20, 0.08);
  background: rgba(247, 244, 239, 0.8);
  border-radius: 12px;
}

.pz-upload-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}

.pz-upload-card {
  display: grid;
  gap: 0.75rem;
  padding: 1rem;
  border: 1px dashed rgba(10, 10, 15, 0.16);
  background: rgba(255, 255, 255, 0.92);
  border-radius: 10px;
}

.pz-upload-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-upload-selection {
  font-size: 0.8rem;
  color: var(--pz-color-earth-orange);
}

.pz-manager-feed {
  display: grid;
  gap: 0.9rem;
  padding: 1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  text-decoration: none;
  color: inherit;
  border-radius: 10px;
}

.pz-manager-list {
  display: grid;
  gap: 0.75rem;
}

.pz-manager-list__header,
.pz-manager-list__row {
  display: grid;
  gap: 1rem;
  align-items: center;
}

.pz-manager-list__header {
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1.2fr) minmax(0, 1.5fr) minmax(0, 1.1fr) auto;
  padding: 0 0.25rem;
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-manager-list__row {
  grid-template-columns: auto minmax(0, 2.1fr) minmax(0, 1.2fr) minmax(0, 1.5fr) minmax(0, 1.1fr);
  padding: 1rem 1.1rem;
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: white;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 10px;
}

.pz-manager-list__row:hover {
  transform: translateY(-1px);
  border-color: rgba(212, 101, 42, 0.28);
  box-shadow: 0 8px 20px rgba(10, 10, 15, 0.06);
}

.pz-manager-list__primary,
.pz-manager-list__commercial {
  display: grid;
  gap: 0.35rem;
  min-width: 0;
}

.pz-manager-list__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pz-manager-pill {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.2rem 0.7rem;
  border: 1px solid rgba(20, 20, 20, 0.08);
  background: rgba(247, 244, 239, 0.82);
  font-family: var(--pz-font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-radius: 99px;
}

.pz-manager-list__action {
  display: flex;
  justify-content: flex-end;
}

.pz-manager-link {
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--pz-color-earth-orange);
}

.pz-checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 2.8rem;
  padding: 0 0.75rem;
  border: 1px solid var(--pz-color-concrete-grey);
  background: white;
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.u-xl-col-span-2,
.u-xl-col-span-3 {
  grid-column: span 1;
}

.pz-property-mobile-nav {
  display: none;
}

@media (min-width: 1280px) {
  .pz-manager-layout {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .u-xl-col-span-2 {
    grid-column: span 2;
  }

  .u-xl-col-span-3 {
    grid-column: span 3;
  }
}

@media (max-width: 920px) {
  .pz-workflow-banner {
    grid-template-columns: 1fr;
  }

  .pz-workflow-banner__actions {
    justify-content: flex-start;
  }

  .pz-workflow-banner__steps {
    grid-template-columns: 1fr;
  }

  .pz-ops-snapshot,
  .pz-ops-snapshot__metrics {
    grid-template-columns: 1fr;
  }

  .pz-manager-list__header {
    display: none;
  }

  .pz-manager-list__row {
    grid-template-columns: 1fr;
  }

  .pz-manager-list__action {
    justify-content: flex-start;
  }

  .pz-document-category-row {
    grid-template-columns: 1fr;
  }

  .pz-property-mobile-nav {
    position: fixed;
    inset: auto 0 0 0;
    z-index: 40;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    border-top: 1px solid rgba(10, 10, 15, 0.08);
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 -8px 24px rgba(10, 10, 15, 0.08);
  }

  .pz-property-mobile-nav button {
    min-height: 3.2rem;
    border: 0;
    background: transparent;
    font-family: var(--pz-font-mono);
    font-size: 0.62rem;
    text-transform: uppercase;
    color: var(--pz-color-structural-steel);
  }
}
</style>
