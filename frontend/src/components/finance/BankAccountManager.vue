<template>
  <div class="pz-bank-manager">
    <Card title="Bank Accounts" variant="premium" eyebrow="Payout">
      <div v-if="accounts.length === 0" class="pz-bank-empty">
        <div class="pz-bank-empty__kicker">NO ACCOUNTS REGISTERED</div>
        <p>Add a bank account to receive distributions and settlements.</p>
      </div>
      <div v-else class="pz-bank-list">
        <div v-for="acc in accounts" :key="acc.id" class="pz-bank-item">
          <div class="pz-bank-item__icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M3 10h18"/><path d="M5 6l7-3 7 3"/><path d="M4 10v11"/><path d="M20 10v11"/></svg>
          </div>
          <div class="pz-bank-item__content">
            <strong>{{ acc.bank_name }}</strong>
            <span>**** {{ acc.account_number_last4 }} &bull; {{ acc.currency || 'KES' }}</span>
            <Badge v-if="acc.is_verified" variant="success" size="sm">Verified</Badge>
            <Badge v-else variant="warning" size="sm">Pending</Badge>
          </div>
          <Button size="sm" variant="ghost" @click="removeAccount(acc.id)">Remove</Button>
        </div>
      </div>
    </Card>

    <Card title="Add Account" variant="elevated" eyebrow="New" class="u-mt-4">
      <form @submit.prevent="addAccount" class="pz-bank-form">
        <PzInput v-model="form.bank_name" label="Bank Name" required placeholder="e.g. Equity Bank" />
        <PzInput v-model="form.account_number" label="Account Number" required placeholder="Full account number" />
        <PzInput v-model="form.routing_number" label="Routing / SWIFT Code" placeholder="Optional for local banks" />
        <div class="pz-input-wrapper">
          <label class="pz-input__label">Currency</label>
          <select v-model="form.currency" class="pz-input">
            <option v-for="currency in configStore.availableCurrencies" :key="currency.currency_code" :value="currency.currency_code">
              {{ currency.currency_code }}{{ currency.symbol ? ` (${currency.symbol})` : '' }}
            </option>
          </select>
        </div>
        <Button type="submit" variant="primary" fullWidth :loading="submitting">Add Bank Account</Button>
      </form>
    </Card>

    <Card v-if="settlements.length" title="Settlement History" variant="glass" eyebrow="Transactions" class="u-mt-4">
      <div class="pz-settlement-list">
        <div v-for="st in settlements" :key="st.id" class="pz-settlement-item">
          <div class="pz-settlement-item__content">
            <strong>{{ st.reference }}</strong>
            <span>{{ formatDate(st.created_at) }}</span>
          </div>
          <div class="pz-settlement-item__amount">{{ formatPrice(st.amount, st.currency || form.currency || 'KES') }}</div>
          <Badge :variant="st.status === 'PROCESSED' ? 'success' : 'warning'" size="sm">{{ st.status }}</Badge>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BankingService from '../../services/banking';
import { useConfigStore } from '../../stores/config';
import Button from '../ui/Button.vue';
import Badge from '../ui/Badge.vue';
import Card from '../ui/Card.vue';
import PzInput from '../PzInput.vue';

const configStore = useConfigStore();
const accounts = ref([]);
const settlements = ref([]);
const submitting = ref(false);
const form = ref({
  bank_name: '',
  account_number: '',
  routing_number: '',
  currency: configStore.activeCurrencyCode || 'KES',
});

onMounted(() => loadData());

async function loadData() {
  try {
    const aRes = await BankingService.listAccounts();
    accounts.value = aRes.data.results || aRes.data || [];
    const sRes = await BankingService.listSettlements();
    settlements.value = sRes.data.results || sRes.data || [];
  } catch (e) {
    console.error(e);
  }
}

async function addAccount() {
  submitting.value = true;
  try {
    await BankingService.createAccount({
      bank_name: form.value.bank_name,
      account_number_last4: form.value.account_number.slice(-4),
      routing_number: form.value.routing_number,
      currency: form.value.currency,
    });
    form.value = { bank_name: '', account_number: '', routing_number: '', currency: configStore.activeCurrencyCode || 'KES' };
    loadData();
  } catch (e) {
    console.error(e);
  } finally {
    submitting.value = false;
  }
}

async function removeAccount(id) {
  if (!confirm('Remove this bank account?')) return;
  try {
    await BankingService.deleteAccount(id);
    loadData();
  } catch (e) {
    console.error(e);
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatPrice(amount, sourceCurrency = 'KES') {
  const value = typeof amount === 'string' ? parseFloat(amount) : amount;
  if (Number.isNaN(value)) return 'KES 0.00';
  return configStore.formatPrice ? configStore.formatPrice(value, sourceCurrency) : `KES ${value.toLocaleString()}`;
}
</script>

<style scoped>
.pz-bank-empty {
  padding: 1rem 0;
  text-align: center;
}

.pz-bank-empty__kicker {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--pz-color-concrete-grey);
  margin-bottom: 0.5rem;
}

.pz-bank-empty p {
  margin: 0;
  color: var(--pz-color-structural-steel);
  font-size: 0.9rem;
}

.pz-bank-list {
  display: grid;
  gap: 0.75rem;
}

.pz-bank-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(10, 10, 15, 0.06);
}

.pz-bank-item__icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #d4652a, #b87333);
  display: grid;
  place-items: center;
  color: white;
  flex-shrink: 0;
}

.pz-bank-item__icon svg {
  width: 1.1rem;
  height: 1.1rem;
}

.pz-bank-item__content {
  flex: 1;
  display: grid;
  gap: 0.15rem;
}

.pz-bank-item__content strong {
  font-family: var(--pz-font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--pz-color-foundation-black);
}

.pz-bank-item__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.72rem;
  color: var(--pz-color-concrete-grey);
}

.pz-bank-form {
  display: grid;
  gap: 1rem;
}

.pz-settlement-list {
  display: grid;
  gap: 0.6rem;
}

.pz-settlement-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.5);
}

.pz-settlement-item__content {
  flex: 1;
  display: grid;
  gap: 0.05rem;
}

.pz-settlement-item__content strong {
  font-family: var(--pz-font-display);
  font-size: 0.85rem;
  font-weight: 600;
}

.pz-settlement-item__content span {
  font-family: var(--pz-font-mono);
  font-size: 0.65rem;
  color: var(--pz-color-concrete-grey);
}

.pz-settlement-item__amount {
  font-family: var(--pz-font-display);
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--pz-color-earth-orange);
}

.u-mt-4 { margin-top: 1rem; }
</style>
