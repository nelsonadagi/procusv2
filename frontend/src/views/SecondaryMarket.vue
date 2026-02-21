<template>
  <div class="pz-marketplace">
    <!-- Premium Global Hero -->
    <section class="pz-hero-premium">
      <div class="pz-hero-premium__mesh"></div>
      <div class="pz-l-container pz-hero-premium__content">
        <h1 class="pz-u-text-display pz-hero-premium__title">Institutional Asset Exchange</h1>
        <p class="pz-hero-premium__subtitle pz-u-text-mono">
          SECONDARY LIQUIDITY • PEER-TO-PEER ASSET SETTLEMENT
        </p>

        <!-- Glassmorphism Discovery -->
        <div class="pz-discovery-glass">
          <div class="pz-discovery-glass__input-group">
            <span class="pz-discovery-glass__icon">🔍</span>
            <input v-model="searchQuery" type="text" placeholder="PROSPECT LIQUID ASSETS..."
              class="pz-discovery-glass__input">
          </div>
          <Button variant="primary" size="lg" class="u-hide-mobile">EXECUTE DISCOVERY</Button>
        </div>

        <div class="pz-hero-premium__stats pz-u-text-mono">
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">$12M+</span>
            <span class="pz-stat-premium__label">VOLUME</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">8.5%</span>
            <span class="pz-stat-premium__label">AVG YIELD</span>
          </div>
          <div class="pz-stat-premium">
            <span class="pz-stat-premium__val">SECURED</span>
            <span class="pz-stat-premium__label"> PROTOCOL</span>
          </div>
        </div>
      </div>
    </section>

    <div class="pz-l-container u-py-12">
      <!-- Unified Discovery Filters -->
      <div class="pz-filter-bar">
        <div class="pz-l-flex pz-l-flex--gap-6 pz-l-flex--align-center pz-l-flex--wrap">
          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Asset Class</span>
            <select v-model="selectedAssetType" class="pz-filter-bar__control">
              <option value="">All Instruments</option>
              <option value="EQUITY">Equity Stakes</option>
              <option value="DEBT">Debt Instruments</option>
              <option value="REIT">REIT Tokens</option>
            </select>
          </div>

          <div class="pz-filter-bar__item">
            <span class="pz-filter-bar__label">Yield Protocol</span>
            <select v-model="selectedYield" class="pz-filter-bar__control">
              <option value="">Full Spectrum</option>
              <option value="HIGH">High Yield (>10%)</option>
              <option value="STABLE">Performance (5-10%)</option>
              <option value="GROWTH">Equity Growth</option>
            </select>
          </div>
        </div>

        <div class="pz-l-flex pz-l-flex--gap-4 pz-l-flex--align-center">
          <Button variant="outline" size="sm" @click="requestSale">LIQUIDATE ASSET</Button>
          <Button variant="ghost" size="sm">RESET PARAMETERS</Button>
        </div>
      </div>

      <div v-if="loading" class="pz-l-flex pz-l-flex--center u-py-20 pz-l-flex--column">
        <div class="c-loader u-mb-4"></div>
        <p class="pz-u-text-mono text-xs">SYNCHRONIZING SEC-MARKET PROTOCOLS...</p>
      </div>

      <div v-else class="pz-premium-grid">
        <div v-for="trade in trades" :key="trade.id" class="pz-premium-card">
          <div class="pz-premium-card__media">
            <img :src="trade.property_image_url || '/placeholder.png'" alt="Property Stake"
              class="pz-premium-card__img">
            <div class="pz-premium-card__badges">
              <Badge variant="finance">YIELD: {{ trade.yield || '8.5%' }}</Badge>
            </div>
          </div>
          <div class="pz-premium-card__content">
            <div class="pz-premium-card__top">
              <span class="pz-premium-card__vendor">SEC-MARKET NODE</span>
              <div class="pz-premium-card__rating">STAKE #{{ trade.id }}</div>
            </div>

            <h4 class="pz-premium-card__title">Operational Equity Share</h4>

            <div class="pz-premium-card__specs">
              <span class="pz-spec-dot">VOLUME: ${{ trade.amount }}</span>
              <span class="pz-spec-dot">VALUATION: ${{ trade.price }}</span>
            </div>

            <div class="pz-premium-card__pricing">
              <div class="pz-price-display">
                <span class="pz-price-display__unit">ASK PRICE</span>
                <span class="pz-price-display__val">${{ trade.price }}</span>
              </div>
              <Button variant="primary" size="sm" @click="buy(trade.id)">ACQUIRE</Button>
            </div>
          </div>
        </div>
      </div>

      <div class="pz-u-bg-limestone pz-u-border pz-p-10 u-mt-12 pz-u-text-center">
        <h3 class="pz-u-text-display text-2xl u-mb-4">Liquidate Operational Stakes</h3>
        <p class="pz-u-text-mono text-sm pz-u-color-steel u-mb-8 max-w-2xl mx-auto">
          LIST YOUR PROJECT EQUITY FOR SALE ON THE REGULATED SECONDARY MARKET. ALL TRADES ARE SECURED VIA ESCROW
          PROTOCOLS.
        </p>
        <Button variant="outline" size="large" @click="requestSale">INITIALIZE SELL ORDER</Button>
      </div>
    </div>

    <!-- Buy Modal -->
    <Modal :isOpen="showBuyModal" title="Acquire Asset" size="md" @close="closeBuyModal">
      <div class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
        <p class="pz-u-text-mono pz-u-color-steel">Confirm acquisition of asset stake #{{ selectedTradeId }}.</p>
        <div class="pz-alert pz-alert--info">
          Funds will be placed in secure escrow until ownership transfer is verified.
        </div>
        <div class="pz-l-flex pz-l-flex--justify-between u-mt-4">
          <Button variant="ghost" @click="closeBuyModal">CANCEL</Button>
          <Button variant="primary" @click="confirmBuy">CONFIRM ACQUISITION</Button>
        </div>
      </div>
    </Modal>

    <!-- Sell Modal -->
    <Modal :isOpen="showSellModal" title="Initialize Sell Order" size="md" @close="closeSellModal">
      <form @submit.prevent="confirmSell" class="pz-l-flex pz-l-flex--column pz-l-flex--gap-4">
        <PzInput v-model="sellForm.assetName" label="Asset Name / Description" required />
        <PzInput v-model="sellForm.volume" label="Volume ($)" type="number" required />
        <PzInput v-model="sellForm.price" label="Asking Price ($)" type="number" required />
        <PzInput v-model="sellForm.yield" label="Target Yield (%)" type="number" required />
        <div class="pz-l-flex pz-l-flex--justify-between u-mt-4">
          <Button type="button" variant="ghost" @click="closeSellModal">CANCEL</Button>
          <Button type="submit" variant="primary">SUBMIT LISTING</Button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import api from '../services/api';
  import { useAuthStore } from '../stores/auth';
  import Button from '../components/ui/Button.vue';
  import Badge from '../components/ui/Badge.vue';
  import Modal from '../components/ui/Modal.vue';
  import PzInput from '../components/PzInput.vue';

  const authStore = useAuthStore();
  const trades = ref([]);
  const loading = ref(true);
  const viewMode = ref('grid');
  const searchQuery = ref('');
  const selectedAssetType = ref('');
  const selectedYield = ref('');
  const priceMin = ref(null);
  const priceMax = ref(null);

  const showBuyModal = ref(false);
  const selectedTradeId = ref(null);

  const showSellModal = ref(false);
  const sellForm = ref({ assetName: '', volume: 0, price: 0, yield: 0 });

  const clearFilters = () => {
    searchQuery.value = '';
    selectedAssetType.value = '';
    selectedYield.value = '';
    priceMin.value = null;
    priceMax.value = null;
  };

  onMounted(async () => {
    try {
      const res = await api.get('/v6/secondary-trades/');
      trades.value = res.data.results || res.data;
    } catch (e) {
      console.error(e);
    } finally {
      loading.value = false;
    }
  });

  function buy(id) {
    selectedTradeId.value = id;
    showBuyModal.value = true;
  }

  function closeBuyModal() {
    showBuyModal.value = false;
    selectedTradeId.value = null;
  }

  function confirmBuy() {
    // API call would go here
    closeBuyModal();
    // Use an alert just for feedback after action if needed, or another toast
  }

  function requestSale() {
    showSellModal.value = true;
  }

  function closeSellModal() {
    showSellModal.value = false;
  }

  function confirmSell() {
    // API call would go here
    closeSellModal();
  }
</script>

<style scoped></style>
