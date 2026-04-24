import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

export const useConfigStore = defineStore('config', () => {
    const countries = ref([]);
    const currencies = ref([]);
    const activeCountryCode = ref(localStorage.getItem('activeCountry') || 'KE');
    const activeCurrencyCode = ref(localStorage.getItem('activeCurrency') || 'USD');
    const platformSettings = ref(null);

    const activeCountry = computed(() =>
        countries.value.find(c => c.iso_code === activeCountryCode.value) ||
        countries.value.find(c => c.is_default) ||
        null
    );

    // Guaranteed list including USD as base even if not in DB
    const availableCurrencies = computed(() => {
        const list = [...currencies.value];
        if (!list.find(c => c.currency_code === 'USD')) {
            list.unshift({ currency_code: 'USD', symbol: '$', rate_to_default: 1 });
        }
        return list;
    });

    const activeCurrency = computed(() =>
        availableCurrencies.value.find(c => c.currency_code === activeCurrencyCode.value) ||
        { currency_code: 'USD', symbol: '$', rate_to_default: 1 }
    );

    async function fetchConfig() {
        try {
            // Fetch individually to handle partial failures
            const fetchCountries = api.get('/platform_settings/countries/').catch(err => {
                console.warn("Countries fetch failed", err);
                return { data: [] };
            });
            const fetchCurrencies = api.get('/platform_settings/currencies/').catch(err => {
                console.warn("Currencies fetch failed", err);
                return { data: [] };
            });
            const fetchPlatform = api.get('/platform_settings/platform/').catch(err => {
                console.warn("Platform settings fetch failed", err);
                return { data: null };
            });

            const [countriesRes, currenciesRes, platformRes] = await Promise.all([
                fetchCountries,
                fetchCurrencies,
                fetchPlatform
            ]);

            countries.value = countriesRes.data.results || countriesRes.data || [];
            currencies.value = currenciesRes.data.results || currenciesRes.data || [];
            platformSettings.value = platformRes.data;

            // If no active selection, use platform defaults
            if (!localStorage.getItem('activeCountry') && platformSettings.value) {
                activeCountryCode.value = platformSettings.value.default_region || 'KE';
            }
            if (!localStorage.getItem('activeCurrency') && platformSettings.value) {
                activeCurrencyCode.value = platformSettings.value.default_currency || 'USD';
            }
        } catch (err) {
            console.error("General config fetch error", err);
        }
    }

    function setCountry(code) {
        activeCountryCode.value = code;
        localStorage.setItem('activeCountry', code);
    }

    function setCurrency(code) {
        activeCurrencyCode.value = code;
        localStorage.setItem('activeCurrency', code);
    }

    function formatPrice(amount) {
        const value = typeof amount === 'string' ? parseFloat(amount) : amount;
        if (isNaN(value)) return 'N/A';

        const rate = parseFloat(activeCurrency.value.rate_to_default) || 1;
        const symbol = activeCurrency.value.symbol || '';
        const converted = value * rate;

        return `${symbol}${converted.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;
    }

    return {
        countries,
        currencies,
        availableCurrencies,
        activeCountryCode,
        activeCurrencyCode,
        activeCountry,
        activeCurrency,
        platformSettings,
        fetchConfig,
        setCountry,
        setCurrency,
        formatPrice
    };
});
