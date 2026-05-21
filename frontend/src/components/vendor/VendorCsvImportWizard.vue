<template>
  <div class="vendor-csv-import-wizard">
    <!-- Step 1: Download Template -->
    <div v-if="step === 1" class="vciw-step">
      <div class="vciw-step__header">
        <div class="vciw-step__number">Step 1 of 3</div>
        <h3 class="vciw-step__title">Prepare Your Catalog</h3>
        <p class="vciw-step__body">
          Download our CSV template and fill it with your product data. Each row becomes one product listing.
        </p>
      </div>

      <div class="vciw-template-info">
        <div class="vciw-template-info__title">Required Columns</div>
        <div class="vciw-columns">
          <div class="vciw-column"><strong>Name</strong> <span>Product name</span></div>
          <div class="vciw-column"><strong>Category</strong> <span>e.g. Cement, Steel, Paint</span></div>
          <div class="vciw-column"><strong>Price</strong> <span>Base price per unit</span></div>
          <div class="vciw-column"><strong>Stock</strong> <span>Quantity available</span></div>
          <div class="vciw-column"><strong>Unit</strong> <span>bag, kg, litre, piece</span></div>
          <div class="vciw-column"><strong>Currency</strong> <span>KES, USD, EUR</span></div>
        </div>
        <div class="vciw-template-info__title" style="margin-top: 1rem;">Optional Columns</div>
        <div class="vciw-columns vciw-columns--optional">
          <div class="vciw-column"><strong>Brand</strong> <span>Manufacturer name</span></div>
          <div class="vciw-column"><strong>Description</strong> <span>Detailed product info</span></div>
          <div class="vciw-column"><strong>Bulk Price</strong> <span>Wholesale pricing</span></div>
          <div class="vciw-column"><strong>Reorder Level</strong> <span>Low stock threshold</span></div>
          <div class="vciw-column"><strong>Certifications</strong> <span>KEBS, ISO, CE</span></div>
          <div class="vciw-column"><strong>Quality Grade</strong> <span>Premium, Standard</span></div>
        </div>
      </div>

      <div class="vciw-example">
        <div class="vciw-example__title">Example Row</div>
        <code class="vciw-example__code">
          Name,Category,Price,Stock,Unit,Currency,Brand,Description<br>
          "Dangote Cement 50kg",Cement,650,200,bag,KES,Dangote,"High-quality Portland cement for construction"
        </code>
      </div>

      <div class="vciw-actions">
        <Button variant="ghost" @click="$emit('close')">Cancel</Button>
        <Button variant="primary" :loading="downloading" @click="downloadTemplate">
          📥 Download CSV Template
        </Button>
      </div>
    </div>

    <!-- Step 2: Upload & Validate -->
    <div v-else-if="step === 2" class="vciw-step">
      <div class="vciw-step__header">
        <div class="vciw-step__number">Step 2 of 3</div>
        <h3 class="vciw-step__title">Upload & Validate</h3>
        <p class="vciw-step__body">
          Upload your filled CSV. We'll check for errors before creating any products.
        </p>
      </div>

      <div
        class="vciw-dropzone"
        :class="{ 'vciw-dropzone--active': dragOver }"
        @dragover.prevent="dragOver = true"
        @dragleave.prevent="dragOver = false"
        @drop.prevent="handleDrop"
        @click="fileInput?.click()"
      >
        <input ref="fileInput" type="file" accept=".csv" class="u-sr-only" @change="handleFileChange">
        <div class="vciw-dropzone__icon">📁</div>
        <div class="vciw-dropzone__text">
          <strong>Click to upload</strong> or drag and drop your CSV file here
        </div>
        <div class="vciw-dropzone__meta">Only .csv files up to 5MB</div>
      </div>

      <!-- Validation Results -->
      <div v-if="validationResult" class="vciw-validation">
        <div v-if="validationResult.valid" class="vciw-validation__status vciw-validation__status--ok">
          ✅ {{ validationResult.total_rows }} rows look good. Ready to import.
        </div>
        <div v-else class="vciw-validation__status vciw-validation__status--error">
          ⚠️ Found {{ validationResult.errors.length }} error{{ validationResult.errors.length === 1 ? '' : 's' }} in {{ validationResult.total_rows }} rows.
        </div>

        <!-- Preview Table -->
        <div v-if="validationResult.valid_rows?.length" class="vciw-preview">
          <div class="vciw-preview__title">Preview (first {{ validationResult.valid_rows.length }} rows)</div>
          <table class="vciw-preview__table">
            <thead>
              <tr>
                <th>Row</th>
                <th>Name</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in validationResult.valid_rows" :key="row.row">
                <td>{{ row.row }}</td>
                <td>{{ row.name }}</td>
                <td>{{ row.category }}</td>
                <td>{{ row.base_price }}</td>
                <td>{{ row.stock_quantity }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Error List -->
        <div v-if="validationResult.errors?.length" class="vciw-errors">
          <div class="vciw-errors__title">Errors</div>
          <div v-for="err in validationResult.errors" :key="err.row" class="vciw-error">
            <span class="vciw-error__row">Row {{ err.row }}</span>
            <span class="vciw-error__msg">{{ err.message }}</span>
          </div>
        </div>
      </div>

      <div class="vciw-actions">
        <Button variant="ghost" @click="step = 1">← Back</Button>
        <Button
          variant="primary"
          :disabled="!validationResult?.valid"
          :loading="importing"
          @click="importCsv"
        >
          Import {{ validationResult?.total_rows || 0 }} Products
        </Button>
      </div>
    </div>

    <!-- Step 3: Import Results -->
    <div v-else-if="step === 3" class="vciw-step">
      <div class="vciw-step__header">
        <div class="vciw-step__number">Step 3 of 3</div>
        <h3 class="vciw-step__title">Import Complete</h3>
      </div>

      <div v-if="importResult" class="vciw-result">
        <div class="vciw-result__summary">
          <div class="vciw-result__stat vciw-result__stat--success">
            <div class="vciw-result__value">{{ importResult.created_count }}</div>
            <div class="vciw-result__label">Products Created</div>
          </div>
          <div v-if="importResult.errors?.length" class="vciw-result__stat vciw-result__stat--error">
            <div class="vciw-result__value">{{ importResult.errors.length }}</div>
            <div class="vciw-result__label">Errors</div>
          </div>
        </div>

        <div v-if="importResult.errors?.length" class="vciw-errors">
          <div class="vciw-errors__title">Import Errors</div>
          <div v-for="(err, idx) in importResult.errors" :key="idx" class="vciw-error">
            <span class="vciw-error__msg">{{ err }}</span>
          </div>
        </div>
      </div>

      <div class="vciw-actions">
        <Button variant="ghost" @click="resetAndClose">Close</Button>
        <Button variant="primary" @click="resetAndClose">
          View Imported Products
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../../services/api';
import Button from '../ui/Button.vue';

const emit = defineEmits(['close', 'imported']);

const step = ref(1);
const fileInput = ref(null);
const dragOver = ref(false);
const downloading = ref(false);
const importing = ref(false);
const validationResult = ref(null);
const importResult = ref(null);
const selectedFile = ref(null);

async function downloadTemplate() {
  downloading.value = true;
  try {
    const res = await api.get('/v1/products/import-template/', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'product_import_template.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch {
    // Fallback: generate template client-side
    const headers = ['Name','Category','Price','Stock','Unit','Currency','Brand','Description','Short Description','Bulk Price','Bulk Threshold','Reorder Level','Min Order Quantity','Max Order Quantity','Quality Grade','Model Number','Country of Origin','Packaging Details','Weight','Dimensions','Color','Material Composition','Estimated Delivery Days','Handling Instructions','Features','Applications','Certifications','Warranty Period','Meta Keywords','Is Featured','Is New Arrival','Is On Sale','Requires Special Handling','Shipping Weight','Manufacturing Date','Expiry Date'];
    const csv = headers.join(',') + '\n' + headers.map(() => '').join(',');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'product_import_template.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } finally {
    downloading.value = false;
  }
}

function handleDrop(event) {
  dragOver.value = false;
  const files = event.dataTransfer?.files;
  if (files?.length) processFile(files[0]);
}

function handleFileChange(event) {
  const files = event.target.files;
  if (files?.length) processFile(files[0]);
}

async function processFile(file) {
  if (!file.name.toLowerCase().endsWith('.csv')) {
    validationResult.value = { valid: false, errors: [{ row: '-', message: 'Only CSV files are supported.' }], valid_rows: [], total_rows: 0 };
    return;
  }
  selectedFile.value = file;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await api.post('/v1/products/validate_import/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    validationResult.value = res.data;
  } catch (err) {
    validationResult.value = {
      valid: false,
      errors: [{ row: '-', message: err.response?.data?.error || 'Failed to validate file.' }],
      valid_rows: [],
      total_rows: 0,
    };
  }
}

async function importCsv() {
  if (!selectedFile.value) return;
  importing.value = true;
  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    const res = await api.post('/v1/products/import_products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    importResult.value = res.data;
    step.value = 3;
    emit('imported');
  } catch (err) {
    importResult.value = {
      created_count: 0,
      errors: [err.response?.data?.error || 'Import failed. Please try again.'],
    };
    step.value = 3;
  } finally {
    importing.value = false;
  }
}

function resetAndClose() {
  step.value = 1;
  validationResult.value = null;
  importResult.value = null;
  selectedFile.value = null;
  emit('close');
}
</script>

<style scoped>
.vendor-csv-import-wizard {
  max-width: 42rem;
  margin: 0 auto;
}

.vciw-step__header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.vciw-step__number {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
}

.vciw-step__title {
  font-family: var(--pz-font-display);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0.25rem 0;
}

.vciw-step__body {
  color: var(--pz-color-text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
}

.vciw-template-info {
  background: rgba(247, 244, 239, 0.5);
  border: 1px solid rgba(10, 10, 15, 0.06);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
}

.vciw-template-info__title {
  font-weight: 600;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.vciw-columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem 1rem;
}

.vciw-column {
  font-size: 0.8rem;
  display: flex;
  gap: 0.4rem;
}

.vciw-column strong {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-foundation-black);
}

.vciw-column span {
  color: var(--pz-color-concrete-grey);
}

.vciw-example {
  background: rgba(10, 10, 15, 0.03);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.vciw-example__title {
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: var(--pz-color-concrete-grey);
}

.vciw-example__code {
  display: block;
  font-size: 0.78rem;
  font-family: var(--pz-font-mono);
  color: var(--pz-color-foundation-black);
  line-height: 1.5;
  word-break: break-all;
}

.vciw-dropzone {
  border: 2px dashed rgba(10, 10, 15, 0.15);
  border-radius: 14px;
  padding: 2.5rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1.5rem;
}

.vciw-dropzone:hover,
.vciw-dropzone--active {
  border-color: var(--pz-color-earth-orange);
  background: rgba(212, 101, 42, 0.03);
}

.vciw-dropzone__icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.vciw-dropzone__text {
  font-size: 0.95rem;
  color: var(--pz-color-foundation-black);
}

.vciw-dropzone__meta {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.3rem;
}

.vciw-validation {
  margin-bottom: 1.5rem;
}

.vciw-validation__status {
  padding: 0.6rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.vciw-validation__status--ok {
  background: rgba(22, 163, 74, 0.08);
  color: #166534;
}

.vciw-validation__status--error {
  background: rgba(220, 38, 38, 0.06);
  color: #991b1b;
}

.vciw-preview {
  margin-bottom: 1rem;
}

.vciw-preview__title {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
}

.vciw-preview__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.vciw-preview__table th,
.vciw-preview__table td {
  padding: 0.4rem 0.6rem;
  text-align: left;
  border-bottom: 1px solid rgba(10, 10, 15, 0.06);
}

.vciw-preview__table th {
  font-family: var(--pz-font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  background: rgba(10, 10, 15, 0.02);
}

.vciw-errors__title {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: #991b1b;
}

.vciw-error {
  display: flex;
  gap: 0.5rem;
  padding: 0.35rem 0;
  font-size: 0.82rem;
  border-bottom: 1px solid rgba(10, 10, 15, 0.04);
}

.vciw-error__row {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
  white-space: nowrap;
}

.vciw-error__msg {
  color: #991b1b;
}

.vciw-result__summary {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.vciw-result__stat {
  text-align: center;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  min-width: 8rem;
}

.vciw-result__stat--success {
  background: rgba(22, 163, 74, 0.08);
}

.vciw-result__stat--error {
  background: rgba(220, 38, 38, 0.06);
}

.vciw-result__value {
  font-family: var(--pz-font-mono);
  font-size: 1.5rem;
  font-weight: 700;
}

.vciw-result__stat--success .vciw-result__value { color: #166534; }
.vciw-result__stat--error .vciw-result__value { color: #991b1b; }

.vciw-result__label {
  font-size: 0.78rem;
  color: var(--pz-color-concrete-grey);
  margin-top: 0.2rem;
}

.vciw-actions {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(10, 10, 15, 0.06);
}

@media (max-width: 640px) {
  .vciw-columns {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
