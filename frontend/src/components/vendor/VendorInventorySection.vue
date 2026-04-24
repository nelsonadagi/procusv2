<template>
  <div class="vendor-inventory-section">
    <div class="pz-admin-card pz-section-shell">
      <div class="pz-admin-card__header pz-section-shell__header pz-l-flex pz-l-flex--justify-between pz-l-flex--align-start">
        <div>
          <div class="pz-section-shell__eyebrow">Inventory Control</div>
          <h3 class="pz-admin-card__title pz-section-shell__title">MATERIAL_PUBLISHING_DESK</h3>
          <div class="pz-section-shell__meta">Manage commercial pricing, structured specs, compliance records, and vendor-facing stock readiness from one workspace.</div>
        </div>
        <div class="pz-l-flex pz-l-flex--gap-3 pz-l-flex--wrap">
          <Button size="sm" variant="ghost" :loading="downloadingTemplate" @click="downloadTemplate">DOWNLOAD_TEMPLATE</Button>
          <input ref="csvInput" type="file" accept=".csv" class="u-sr-only" @change="handleCsvSelected">
          <Button size="sm" variant="secondary" :loading="importing" @click="triggerCsvImport">IMPORT_CSV</Button>
          <Button size="sm" @click="openCreateModal">ADD_MATERIAL</Button>
        </div>
      </div>

      <div class="pz-section-shell__content">
        <div class="pz-summary-grid u-mb-6">
          <div class="pz-summary-card">
            <span>Published</span>
            <strong>{{ products.length }}</strong>
          </div>
          <div class="pz-summary-card">
            <span>Low stock</span>
            <strong>{{ lowStockCount }}</strong>
          </div>
          <div class="pz-summary-card">
            <span>Featured</span>
            <strong>{{ featuredCount }}</strong>
          </div>
          <div class="pz-summary-card">
            <span>Certified</span>
            <strong>{{ certifiedCount }}</strong>
          </div>
        </div>

        <div class="pz-inventory-toolbar u-mb-6">
          <div class="pz-inventory-toolbar__search">
            <label class="pz-inventory-toolbar__label" for="vendor-inventory-search">Search inventory</label>
            <input
              id="vendor-inventory-search"
              v-model.trim="searchQuery"
              type="search"
              class="pz-inventory-toolbar__input"
              placeholder="Search by material, category, brand, SKU, origin, or description"
            >
          </div>
          <div class="pz-inventory-toolbar__meta">
            <span>{{ filteredProducts.length }} visible</span>
            <Button v-if="searchQuery" size="sm" variant="ghost" @click="searchQuery = ''">CLEAR_SEARCH</Button>
          </div>
        </div>

        <div v-if="loading" class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">MAPPING_VENDOR_CATALOGUE</div>
        </div>
        <div v-else-if="products.length === 0" class="pz-empty-state">
          <div class="pz-empty-state__glyph">INV</div>
          <div class="pz-empty-state__eyebrow">Inventory Grid</div>
          <h4 class="pz-empty-state__title">No vendor inventory has been published yet.</h4>
          <p class="pz-empty-state__body">Create your first material record or import a CSV template to activate quote response and order intake.</p>
        </div>
        <div v-else-if="filteredProducts.length === 0" class="pz-empty-state">
          <div class="pz-empty-state__glyph">SRCH</div>
          <div class="pz-empty-state__eyebrow">Search Results</div>
          <h4 class="pz-empty-state__title">No inventory items match this search.</h4>
          <p class="pz-empty-state__body">Try a broader material name, category, brand, origin, or SKU term.</p>
        </div>
        <VendorInventoryList
          v-else
          :products="filteredProducts"
          :deleting-product-id="deletingProductId"
          :placeholder-image="placeholderImage"
          :format-price="configStore.formatPrice"
          :inventory-badge-variant="inventoryBadgeVariant"
          :format-inventory-signal="formatInventorySignal"
          @edit="openEditModal"
          @delete="deleteProduct"
          @adjust="openAdjustmentModal"
          @history="openHistoryModal"
        />
      </div>
    </div>

    <Modal :isOpen="showProductModal" :title="editingProductId ? 'EDIT_MATERIAL_RECORD' : 'PUBLISH_NEW_MATERIAL'" size="xl" @close="closeProductModal">
      <form id="product-form" class="pz-product-form" @submit.prevent="saveProduct">
        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div class="pz-form-section__eyebrow">Commercial Setup</div>
            <h4>Core Listing</h4>
          </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
            <PzInput v-model="productForm.name" label="Material Name" required />
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Category</label>
              <select v-model="productForm.category" class="pz-input" required>
                <option disabled value="">Select category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </div>
            <PzInput v-model="productForm.unit" label="Unit of Sale" required />
            <PzInput v-model.number="productForm.base_price" label="Base Price" type="number" required />
            <PzInput v-model.number="productForm.bulk_price" label="Bulk Price" type="number" />
            <PzInput v-model.number="productForm.bulk_threshold" label="Bulk Threshold" type="number" />
            <PzInput v-model.number="productForm.stock_quantity" label="Stock Quantity" type="number" required />
            <PzInput v-model.number="productForm.reorder_level" label="Reorder Threshold" type="number" />
            <PzInput v-model.number="productForm.min_order_quantity" label="Min Order Qty" type="number" />
            <PzInput v-model.number="productForm.max_order_quantity" label="Max Order Qty" type="number" />
            <PzInput v-model="productForm.brand" label="Brand" />
            <PzInput v-model="productForm.model_number" label="Model / SKU" />
            <PzInput v-model="productForm.quality_grade" label="Quality Grade" />
            <PzInput v-model="productForm.country_of_origin" label="Country of Origin" />
            <PzInput v-model="productForm.packaging_details" label="Packaging Details" />
            <PzInput v-model.number="productForm.estimated_delivery_days" label="Lead Time (Days)" type="number" />
            <div class="pz-input-wrapper">
              <label class="pz-input__label">Status</label>
              <select v-model="productForm.status" class="pz-input">
                <option value="ACTIVE">ACTIVE</option>
                <option value="DRAFT">DRAFT</option>
                <option value="OUT_OF_STOCK">OUT_OF_STOCK</option>
                <option value="DISABLED">DISABLED</option>
              </select>
            </div>
          </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4 u-mt-4">
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.short_description" label="Short Description" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.description" label="Detailed Description" type="textarea" required />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.delivery_regions_text" label="Delivery Regions" help-text="Comma-separated, e.g. NAIROBI, MOMBASA, KISUMU" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.features_text" label="Feature Highlights" type="textarea" help-text="One feature per line" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.applications_text" label="Applications" type="textarea" help-text="One use case per line" />
            </div>
            <div class="pz-col-span-2">
              <PzInput v-model="productForm.handling_instructions" label="Handling Instructions" type="textarea" />
            </div>
          </div>
        </section>

        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div class="pz-form-section__eyebrow">Technical Layer</div>
            <h4>Structured Attributes</h4>
            <Button size="sm" variant="ghost" type="button" @click="addAttribute">Add Attribute</Button>
          </div>
          <div v-if="productForm.attribute_entries.length" class="pz-repeaters">
            <div v-for="(attribute, index) in productForm.attribute_entries" :key="`attribute-${index}`" class="pz-repeater-row">
              <PzInput v-model="attribute.group" label="Group" />
              <PzInput v-model="attribute.name" label="Name" />
              <PzInput v-model="attribute.value" label="Value" />
              <PzInput v-model="attribute.unit" label="Unit" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Highlight</label>
                <select v-model="attribute.is_highlight" class="pz-input">
                  <option :value="false">No</option>
                  <option :value="true">Yes</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeAttribute(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No structured attributes added yet.</p>
        </section>

        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div class="pz-form-section__eyebrow">Compliance</div>
            <h4>Certifications</h4>
            <Button size="sm" variant="ghost" type="button" @click="addCertification">Add Certification</Button>
          </div>
          <div v-if="productForm.certification_entries.length" class="pz-repeaters">
            <div v-for="(certification, index) in productForm.certification_entries" :key="`certification-${index}`" class="pz-repeater-row">
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Registry</label>
                <select v-model="certification.registry" class="pz-input">
                  <option :value="null">Custom</option>
                  <option v-for="option in certificationOptions" :key="option.id" :value="option.id">{{ option.name }}</option>
                </select>
              </div>
              <PzInput v-model="certification.display_name" label="Display Name" />
              <PzInput v-model="certification.certification_number" label="Reference Number" />
              <PzInput v-model="certification.issuing_body" label="Issuing Body" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Status</label>
                <select v-model="certification.status" class="pz-input">
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="PENDING">PENDING</option>
                  <option value="EXPIRED">EXPIRED</option>
                  <option value="REVOKED">REVOKED</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeCertification(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No certification records added yet.</p>
        </section>

        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div class="pz-form-section__eyebrow">Procurement Pack</div>
            <h4>Documents</h4>
            <Button size="sm" variant="ghost" type="button" @click="addDocument">Add Document</Button>
          </div>
          <div v-if="productForm.documents.length" class="pz-repeaters">
            <div v-for="(document, index) in productForm.documents" :key="`document-${index}`" class="pz-repeater-row">
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Document Type</label>
                <select v-model="document.document_type" class="pz-input">
                  <option value="DATASHEET">DATASHEET</option>
                  <option value="SAFETY">SAFETY</option>
                  <option value="WARRANTY">WARRANTY</option>
                  <option value="BROCHURE">BROCHURE</option>
                  <option value="INSTALLATION">INSTALLATION</option>
                  <option value="OTHER">OTHER</option>
                </select>
              </div>
              <PzInput v-model="document.title" label="Title" />
              <PzInput v-model="document.external_url" label="External URL" />
              <PzInput v-model="document.description" label="Description" />
              <div class="pz-input-wrapper">
                <label class="pz-input__label">Visibility</label>
                <select v-model="document.is_public" class="pz-input">
                  <option :value="true">Public</option>
                  <option :value="false">Internal</option>
                </select>
              </div>
              <Button variant="ghost" size="sm" type="button" @click="removeDocument(index)">Remove</Button>
            </div>
          </div>
          <p v-else class="pz-u-color-steel text-sm">No supporting documents added yet.</p>
        </section>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeProductModal">Cancel</Button>
        <Button type="submit" form="product-form" variant="primary" :loading="saving">
          {{ editingProductId ? 'Save Material' : 'Publish Material' }}
        </Button>
      </template>
    </Modal>

    <Modal :isOpen="showAdjustmentModal" title="ADJUST_INVENTORY_LEDGER" size="md" @close="closeAdjustmentModal">
      <form id="inventory-adjustment-form" class="pz-product-form" @submit.prevent="submitInventoryAdjustment">
        <section class="pz-form-section">
          <div class="pz-form-section__header">
            <div>
              <div class="pz-form-section__eyebrow">Stock Ledger</div>
              <h4>{{ selectedInventoryProduct?.name || 'Selected Material' }}</h4>
            </div>
          </div>
          <div class="pz-inventory-adjustment__summary">
            <div>
              <span>On hand</span>
              <strong>{{ selectedInventoryProduct?.stock_quantity ?? 0 }}</strong>
            </div>
            <div>
              <span>Available</span>
              <strong>{{ selectedInventoryProduct?.available_quantity ?? selectedInventoryProduct?.stock_quantity ?? 0 }}</strong>
            </div>
            <div>
              <span>Reorder at</span>
              <strong>{{ selectedInventoryProduct?.reorder_level ?? 0 }}</strong>
            </div>
          </div>
          <div class="pz-l-grid pz-l-grid--md-cols-2 pz-l-grid--gap-4">
            <PzInput v-model.number="inventoryAdjustmentForm.quantity_delta" label="Quantity Delta" type="number" required help-text="Use positive values to restock and negative values to remove stock." />
            <PzInput v-model="inventoryAdjustmentForm.reference" label="Reference" help-text="e.g. GRN-448, cycle count, damaged batch" />
            <div class="pz-col-span-2">
              <PzInput v-model="inventoryAdjustmentForm.note" label="Adjustment Note" type="textarea" required />
            </div>
          </div>
        </section>
      </form>
      <template #footer>
        <Button variant="ghost" @click="closeAdjustmentModal">Cancel</Button>
        <Button type="submit" form="inventory-adjustment-form" variant="primary" :loading="adjustingInventory">
          Apply Adjustment
        </Button>
      </template>
    </Modal>

    <Modal :isOpen="showHistoryModal" title="INVENTORY_MOVEMENT_HISTORY" size="lg" @close="closeHistoryModal">
      <section class="pz-form-section">
        <div class="pz-form-section__header">
          <div>
            <div class="pz-form-section__eyebrow">Movement Ledger</div>
            <h4>{{ selectedInventoryProduct?.name || 'Selected Material' }}</h4>
          </div>
        </div>
        <div v-if="historyLoading" class="pz-loading-state">
          <div class="pz-loading-state__indicator"></div>
          <div class="pz-loading-state__label">LOADING_LEDGER_EVENTS</div>
        </div>
        <div v-else-if="inventoryHistory.length === 0" class="pz-empty-state">
          <div class="pz-empty-state__glyph">LOG</div>
          <div class="pz-empty-state__eyebrow">Inventory Ledger</div>
          <h4 class="pz-empty-state__title">No movement records yet.</h4>
          <p class="pz-empty-state__body">Initial stock loads, manual adjustments, order commits, and restocks will appear here.</p>
        </div>
        <div v-else class="pz-ledger-list">
          <article v-for="movement in inventoryHistory" :key="movement.id" class="pz-ledger-row">
            <div class="pz-ledger-row__top">
              <Badge :variant="movement.quantity_delta < 0 ? 'danger' : 'success'">
                {{ movement.movement_type }}
              </Badge>
              <span class="pz-u-text-mono text-xs">{{ formatMovementDate(movement.created_at) }}</span>
            </div>
            <div class="pz-ledger-row__numbers">
              <span>Delta: {{ movement.quantity_delta > 0 ? `+${movement.quantity_delta}` : movement.quantity_delta }}</span>
              <span>{{ movement.quantity_before }} → {{ movement.quantity_after }}</span>
            </div>
            <p v-if="movement.note" class="pz-ledger-row__note">{{ movement.note }}</p>
            <div class="pz-ledger-row__meta">
              <span v-if="movement.reference">Ref: {{ movement.reference }}</span>
              <span v-if="movement.actor_name">By: {{ movement.actor_name }}</span>
            </div>
          </article>
        </div>
      </section>
    </Modal>
  </div>
</template>

<script setup>
import { computed, inject, onMounted, ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';
import Modal from '../ui/Modal.vue';
import PzInput from '../PzInput.vue';
import { useConfigStore } from '../../stores/config';
import VendorInventoryList from './VendorInventoryList.vue';

const configStore = useConfigStore();
const showAlert = inject('showAlert');

const placeholderImage = 'https://via.placeholder.com/640x420?text=PAANGUZO+MATERIAL';

const products = ref([]);
const categories = ref([]);
const certificationOptions = ref([]);
const loading = ref(true);
const saving = ref(false);
const importing = ref(false);
const downloadingTemplate = ref(false);
const deletingProductId = ref(null);
const showProductModal = ref(false);
const editingProductId = ref(null);
const csvInput = ref(null);
const selectedInventoryProduct = ref(null);
const showAdjustmentModal = ref(false);
const adjustingInventory = ref(false);
const showHistoryModal = ref(false);
const historyLoading = ref(false);
const inventoryHistory = ref([]);
const searchQuery = ref('');

const inventoryAdjustmentForm = ref({
  quantity_delta: 0,
  note: '',
  reference: '',
});

const emptyProductForm = () => ({
  name: '',
  category: '',
  unit: 'bag',
  base_price: 0,
  bulk_price: null,
  bulk_threshold: null,
  stock_quantity: 0,
  reorder_level: 0,
  min_order_quantity: 1,
  max_order_quantity: null,
  brand: '',
  model_number: '',
  quality_grade: '',
  country_of_origin: '',
  packaging_details: '',
  estimated_delivery_days: null,
  short_description: '',
  description: '',
  delivery_regions_text: '',
  features_text: '',
  applications_text: '',
  handling_instructions: '',
  status: 'ACTIVE',
  attribute_entries: [],
  certification_entries: [],
  documents: [],
});

const productForm = ref(emptyProductForm());

const lowStockCount = computed(() => products.value.filter((entry) => entry.inventory_signal === 'LOW_STOCK').length);
const featuredCount = computed(() => products.value.filter((entry) => entry.is_featured).length);
const certifiedCount = computed(() => products.value.filter((entry) => entry.certification_highlights?.length).length);
const filteredProducts = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) {
    return products.value;
  }

  return products.value.filter((product) => {
    const haystack = [
      product.name,
      product.category_name,
      product.category?.name,
      product.brand,
      product.model_number,
      product.country_of_origin,
      product.short_description,
      product.description,
      product.quality_grade,
      product.unit,
      ...(product.certification_highlights || []),
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();

    return haystack.includes(query);
  });
});

function normalizeListPayload(data) {
  return data?.results || data || [];
}

function splitLines(value) {
  return (value || '')
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
    .join('\n');
}

function parseDeliveryRegions(value) {
  return (value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function inventoryBadgeVariant(signal) {
  if (signal === 'LOW_STOCK') return 'warning';
  if (signal === 'OUT_OF_STOCK') return 'danger';
  return 'success';
}

function formatInventorySignal(signal) {
  if (!signal) return 'In Stock';
  return signal.replaceAll('_', ' ');
}

async function fetchCategories() {
  try {
    const res = await api.get('/taxonomy/categories/?taxonomy_type=MATERIAL');
    categories.value = normalizeListPayload(res.data);
  } catch (err) {
    showAlert?.('Failed to load material categories.', 'error');
  }
}

async function fetchCertificationOptions() {
  try {
    const res = await api.get('/v1/products/certification-options/');
    certificationOptions.value = normalizeListPayload(res.data);
  } catch (err) {
    certificationOptions.value = [];
  }
}

async function fetchProducts() {
  loading.value = true;
  try {
    const res = await api.get('/v1/products/me/');
    products.value = normalizeListPayload(res.data);
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to load vendor inventory.', 'error');
  } finally {
    loading.value = false;
  }
}

function addAttribute() {
  productForm.value.attribute_entries.push({
    group: '',
    name: '',
    value: '',
    unit: '',
    is_highlight: false,
    sort_order: productForm.value.attribute_entries.length + 1,
  });
}

function removeAttribute(index) {
  productForm.value.attribute_entries.splice(index, 1);
}

function addCertification() {
  productForm.value.certification_entries.push({
    registry: null,
    display_name: '',
    certification_number: '',
    issuing_body: '',
    status: 'ACTIVE',
  });
}

function removeCertification(index) {
  productForm.value.certification_entries.splice(index, 1);
}

function addDocument() {
  productForm.value.documents.push({
    document_type: 'DATASHEET',
    title: '',
    external_url: '',
    description: '',
    is_public: true,
  });
}

function removeDocument(index) {
  productForm.value.documents.splice(index, 1);
}

function openCreateModal() {
  editingProductId.value = null;
  productForm.value = emptyProductForm();
  showProductModal.value = true;
}

function openEditModal(product) {
  editingProductId.value = product.id;
  productForm.value = {
    name: product.name || '',
    category: product.category?.id || product.category_id || '',
    unit: product.unit || 'unit',
    base_price: Number(product.base_price || 0),
    bulk_price: product.bulk_price ? Number(product.bulk_price) : null,
    bulk_threshold: product.bulk_threshold ?? null,
    stock_quantity: Number(product.stock_quantity || 0),
    reorder_level: product.reorder_level ?? 0,
    min_order_quantity: product.min_order_quantity ?? 1,
    max_order_quantity: product.max_order_quantity ?? null,
    brand: product.brand || '',
    model_number: product.model_number || '',
    quality_grade: product.quality_grade || '',
    country_of_origin: product.country_of_origin || '',
    packaging_details: product.packaging_details || '',
    estimated_delivery_days: product.estimated_delivery_days ?? null,
    short_description: product.short_description || '',
    description: product.description || '',
    delivery_regions_text: (product.delivery_regions || []).join(', '),
    features_text: product.features || '',
    applications_text: product.applications || '',
    handling_instructions: product.handling_instructions || '',
    status: product.status || 'ACTIVE',
    attribute_entries: (product.attribute_entries || []).map((entry) => ({
      group: entry.group || '',
      name: entry.name || '',
      value: entry.value || '',
      unit: entry.unit || '',
      is_highlight: Boolean(entry.is_highlight),
      sort_order: entry.sort_order || 0,
    })),
    certification_entries: (product.certification_entries || []).map((entry) => ({
      registry: entry.registry || null,
      display_name: entry.display_name || '',
      certification_number: entry.certification_number || '',
      issuing_body: entry.issuing_body || '',
      status: entry.status || 'ACTIVE',
    })),
    documents: (product.documents || []).map((entry) => ({
      document_type: entry.document_type || 'DATASHEET',
      title: entry.title || '',
      external_url: entry.external_url || '',
      description: entry.description || '',
      is_public: entry.is_public !== false,
    })),
  };
  showProductModal.value = true;
}

function closeProductModal() {
  showProductModal.value = false;
  editingProductId.value = null;
  productForm.value = emptyProductForm();
}

function openAdjustmentModal(product) {
  selectedInventoryProduct.value = product;
  inventoryAdjustmentForm.value = {
    quantity_delta: 0,
    note: '',
    reference: '',
  };
  showAdjustmentModal.value = true;
}

function closeAdjustmentModal() {
  showAdjustmentModal.value = false;
  selectedInventoryProduct.value = null;
  inventoryAdjustmentForm.value = {
    quantity_delta: 0,
    note: '',
    reference: '',
  };
}

async function submitInventoryAdjustment() {
  if (!selectedInventoryProduct.value) return;
  adjustingInventory.value = true;
  try {
    const response = await api.post(
      `/v1/products/${selectedInventoryProduct.value.id}/adjust-inventory/`,
      inventoryAdjustmentForm.value,
    );
    const updatedProduct = response.data.product;
    products.value = products.value.map((entry) => (
      entry.id === updatedProduct.id ? updatedProduct : entry
    ));
    selectedInventoryProduct.value = updatedProduct;
    showAlert?.('Inventory ledger updated successfully.', 'success');
    closeAdjustmentModal();
  } catch (err) {
    showAlert?.(err.response?.data?.error || 'Failed to adjust inventory.', 'error');
  } finally {
    adjustingInventory.value = false;
  }
}

function formatMovementDate(value) {
  if (!value) return 'Unknown';
  return new Date(value).toLocaleString();
}

async function openHistoryModal(product) {
  selectedInventoryProduct.value = product;
  showHistoryModal.value = true;
  historyLoading.value = true;
  try {
    const response = await api.get(`/v1/products/${product.id}/inventory-history/`);
    inventoryHistory.value = normalizeListPayload(response.data);
  } catch (err) {
    inventoryHistory.value = [];
    showAlert?.(err.response?.data?.detail || 'Failed to load inventory history.', 'error');
  } finally {
    historyLoading.value = false;
  }
}

function closeHistoryModal() {
  showHistoryModal.value = false;
  selectedInventoryProduct.value = null;
  inventoryHistory.value = [];
}

function buildPayload() {
  return {
    name: productForm.value.name,
    category: productForm.value.category,
    unit: productForm.value.unit,
    base_price: productForm.value.base_price,
    bulk_price: productForm.value.bulk_price || null,
    bulk_threshold: productForm.value.bulk_threshold || null,
    stock_quantity: productForm.value.stock_quantity,
    reorder_level: productForm.value.reorder_level || 0,
    min_order_quantity: productForm.value.min_order_quantity || 1,
    max_order_quantity: productForm.value.max_order_quantity || null,
    brand: productForm.value.brand,
    model_number: productForm.value.model_number,
    quality_grade: productForm.value.quality_grade,
    country_of_origin: productForm.value.country_of_origin,
    packaging_details: productForm.value.packaging_details,
    estimated_delivery_days: productForm.value.estimated_delivery_days || null,
    short_description: productForm.value.short_description,
    description: productForm.value.description,
    delivery_regions: parseDeliveryRegions(productForm.value.delivery_regions_text),
    features: splitLines(productForm.value.features_text),
    applications: splitLines(productForm.value.applications_text),
    handling_instructions: productForm.value.handling_instructions,
    status: productForm.value.status,
    attribute_entries: productForm.value.attribute_entries.filter((entry) => entry.name && entry.value),
    certification_entries: productForm.value.certification_entries.filter((entry) => entry.display_name || entry.registry),
    documents: productForm.value.documents.filter((entry) => entry.title && entry.external_url),
  };
}

async function saveProduct() {
  saving.value = true;
  try {
    const payload = buildPayload();
    if (editingProductId.value) {
      await api.patch(`/v1/products/${editingProductId.value}/`, payload);
      showAlert?.('Material record updated successfully.', 'success');
    } else {
      await api.post('/v1/products/', payload);
      showAlert?.('Material published to your vendor catalogue.', 'success');
    }
    closeProductModal();
    await fetchProducts();
  } catch (err) {
    const detail = err.response?.data;
    showAlert?.(typeof detail === 'string' ? detail : 'Failed to save material record.', 'error');
  } finally {
    saving.value = false;
  }
}

async function deleteProduct(product) {
  deletingProductId.value = product.id;
  try {
    await api.delete(`/v1/products/${product.id}/`);
    products.value = products.value.filter((entry) => entry.id !== product.id);
    showAlert?.('Material removed.', 'success');
  } catch (err) {
    showAlert?.(err.response?.data?.detail || 'Failed to delete material.', 'error');
  } finally {
    deletingProductId.value = null;
  }
}

function triggerCsvImport() {
  csvInput.value?.click();
}

async function handleCsvSelected(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  importing.value = true;
  try {
    const res = await api.post('/v1/products/import_products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    const createdCount = res.data?.created_count ?? 0;
    const errors = res.data?.errors || [];
    const message = errors.length
      ? `Imported ${createdCount} materials with ${errors.length} row issues.`
      : `Imported ${createdCount} materials successfully.`;
    showAlert?.(message, errors.length ? 'warning' : 'success');
    await fetchProducts();
  } catch (err) {
    showAlert?.(err.response?.data?.error || 'Failed to import materials.', 'error');
  } finally {
    importing.value = false;
    event.target.value = '';
  }
}

async function downloadTemplate() {
  downloadingTemplate.value = true;
  try {
    const res = await api.get('/v1/products/download_template/', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'product_import_template.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    showAlert?.('CSV template downloaded.', 'success');
  } catch (err) {
    showAlert?.('Failed to download inventory template.', 'error');
  } finally {
    downloadingTemplate.value = false;
  }
}

onMounted(async () => {
  await Promise.all([fetchCategories(), fetchCertificationOptions(), fetchProducts()]);
});
</script>

<style scoped>
.pz-admin-card {
  background: white;
  border: 1px solid var(--pz-color-foundation-black);
}

.pz-admin-card__header {
  padding: var(--pz-space-4) var(--pz-space-6);
  border-bottom: 2px solid var(--pz-color-foundation-black);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pz-admin-card__title {
  font-family: var(--pz-font-mono);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.pz-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.pz-summary-card,
.pz-form-section {
  border: 1px solid rgba(10, 10, 15, 0.1);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 10px 10px 0 rgba(10, 10, 15, 0.05);
}

.pz-summary-card {
  padding: 1rem;
  display: grid;
  gap: 0.2rem;
}

.pz-summary-card span {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.pz-summary-card strong {
  font-size: 1.5rem;
}

.pz-product-form,
.pz-repeaters {
  display: grid;
  gap: 1rem;
}

.pz-inventory-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1rem;
  flex-wrap: wrap;
}

.pz-inventory-toolbar__search {
  flex: 1 1 420px;
  display: grid;
  gap: 0.45rem;
}

.pz-inventory-toolbar__label {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-inventory-toolbar__input {
  width: 100%;
  min-height: 48px;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(10, 10, 15, 0.18);
  background: rgba(255, 255, 255, 0.96);
  color: var(--pz-color-text-primary);
  font: inherit;
}

.pz-inventory-toolbar__input::placeholder {
  color: var(--pz-color-text-secondary);
}

.pz-inventory-toolbar__input:focus {
  outline: 2px solid rgba(212, 101, 42, 0.24);
  outline-offset: 2px;
  border-color: var(--pz-color-earth-orange);
}

.pz-inventory-toolbar__meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: var(--pz-font-mono);
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-text-secondary);
}

.pz-inventory-adjustment__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.pz-inventory-adjustment__summary > div,
.pz-ledger-row {
  border: 1px solid rgba(10, 10, 15, 0.08);
  background: rgba(247, 244, 239, 0.95);
  padding: 0.9rem;
}

.pz-inventory-adjustment__summary span,
.pz-ledger-row__meta,
.pz-ledger-row__numbers {
  display: block;
  font-size: 0.78rem;
  color: var(--pz-color-steel-grey);
}

.pz-inventory-adjustment__summary strong {
  display: block;
  margin-top: 0.3rem;
  font-size: 1.1rem;
}

.pz-ledger-list {
  display: grid;
  gap: 0.75rem;
}

.pz-ledger-row__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.pz-ledger-row__numbers {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.pz-ledger-row__note {
  margin: 0.7rem 0 0.45rem;
  font-size: 0.88rem;
}

.pz-form-section {
  padding: 1rem;
}

.pz-form-section__header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.pz-form-section__eyebrow {
  font-family: var(--pz-font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pz-color-earth-orange);
}

.pz-repeater-row {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 0.75rem;
  align-items: end;
  padding: 0.9rem;
  background: rgba(247, 244, 239, 0.95);
  border: 1px solid rgba(10, 10, 15, 0.08);
}

@media (max-width: 1200px) {
  .pz-summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .pz-repeater-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .pz-summary-grid,
  .pz-repeater-row,
  .pz-inventory-adjustment__summary {
    grid-template-columns: 1fr;
  }

  .pz-ledger-row__top,
  .pz-ledger-row__numbers {
    flex-direction: column;
    align-items: start;
  }
}
</style>
