import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import api from '../services/api';

export const useConfigStore = defineStore('config', () => {
    const countries = ref([]);
    const currencies = ref([]);
    const activeCountryCode = ref(localStorage.getItem('activeCountry') || '');
    const activeCurrencyCode = ref(localStorage.getItem('activeCurrency') || '');
    const platformSettings = ref(null);
    const fallbackCurrencyCatalog = {
        KES: { currency_name: 'Kenyan Shilling', symbol: 'KSh', rate_to_default: 1 },
        UGX: { currency_name: 'Ugandan Shilling', symbol: 'USh', rate_to_default: 0.035 },
        TZS: { currency_name: 'Tanzanian Shilling', symbol: 'TSh', rate_to_default: 0.051 },
        RWF: { currency_name: 'Rwandan Franc', symbol: 'RF', rate_to_default: 0.0071 },
        BIF: { currency_name: 'Burundian Franc', symbol: 'FBu', rate_to_default: 0.0034 },
        SSP: { currency_name: 'South Sudanese Pound', symbol: 'SSP', rate_to_default: 1 },
        ETB: { currency_name: 'Ethiopian Birr', symbol: 'Br', rate_to_default: 0.43 },
        USD: { currency_name: 'US Dollar', symbol: '$', rate_to_default: 130 },
        EUR: { currency_name: 'Euro', symbol: '€', rate_to_default: 138.5 },
        GBP: { currency_name: 'British Pound', symbol: '£', rate_to_default: 160 },
        AED: { currency_name: 'UAE Dirham', symbol: 'AED', rate_to_default: 35.3 },
        CNY: { currency_name: 'Chinese Yuan', symbol: '¥', rate_to_default: 18.2 },
    };

    const activeCountry = computed(() =>
        countries.value.find(c => c.iso_code === activeCountryCode.value) ||
        countries.value.find(c => c.is_default) ||
        null
    );

    const resolvedCountryCode = computed(() =>
        activeCountry.value?.iso_code?.trim()?.toUpperCase() ||
        platformSettings.value?.default_region?.trim()?.toUpperCase() ||
        countries.value.find(c => c.is_default)?.iso_code?.trim()?.toUpperCase() ||
        countries.value[0]?.iso_code?.trim()?.toUpperCase() ||
        'KE'
    );

    // Guaranteed list including KES as base even if not in DB
    const availableCurrencies = computed(() => {
        const list = [...currencies.value];
        const seen = new Set(list.map(c => normalizeCurrencyCode(c.currency_code)));
        Object.entries(fallbackCurrencyCatalog).forEach(([code, fallback]) => {
            if (!seen.has(code)) {
                list.push({
                    currency_code: code,
                    currency_name: fallback.currency_name,
                    symbol: fallback.symbol,
                    rate_to_default: fallback.rate_to_default,
                    is_active: true,
                });
            }
        });
        if (!list.find(c => normalizeCurrencyCode(c.currency_code) === 'KES')) {
            list.unshift({ currency_code: 'KES', currency_name: 'Kenyan Shilling', symbol: 'KSh', rate_to_default: 1 });
        }
        return list;
    });

    const resolvedCurrencyCode = computed(() => {
        const countryCurrency = activeCountry.value?.default_currency?.trim()?.toUpperCase();
        const platformCurrency = platformSettings.value?.default_currency?.trim()?.toUpperCase();
        return countryCurrency || platformCurrency || 'KES';
    });

    const activeCurrency = computed(() =>
        availableCurrencies.value.find(c => c.currency_code === activeCurrencyCode.value) ||
        availableCurrencies.value.find(c => c.currency_code === resolvedCurrencyCode.value) ||
        { currency_code: resolvedCurrencyCode.value, symbol: resolvedCurrencyCode.value, rate_to_default: 1 }
    );

    function normalizeCurrencyCode(code, fallback = 'KES') {
        return (code || fallback).toString().trim().toUpperCase() || fallback;
    }

    function resolveCurrency(code) {
        const normalized = normalizeCurrencyCode(code);
        const matched = availableCurrencies.value.find(c => normalizeCurrencyCode(c.currency_code) === normalized);
        const fallback = fallbackCurrencyCatalog[normalized] || {};
        return {
            currency_code: matched?.currency_code || normalized,
            currency_name: matched?.currency_name || fallback.currency_name || normalized,
            symbol: matched?.symbol || fallback.symbol || normalized,
            rate_to_default: matched?.rate_to_default ?? fallback.rate_to_default ?? 1,
            is_active: matched?.is_active ?? true,
        };
    }

    function syncCurrencyToCountry() {
        const resolvedCode = resolvedCountryCode.value;
        if (!resolvedCode) return;

        if (activeCountryCode.value !== resolvedCode) {
            activeCountryCode.value = resolvedCode;
            localStorage.setItem('activeCountry', resolvedCode);
        }

        const countryCurrency = activeCountry.value?.default_currency?.trim()?.toUpperCase() || platformSettings.value?.default_currency?.trim()?.toUpperCase() || 'KES';
        activeCurrencyCode.value = countryCurrency;
        localStorage.setItem('activeCurrency', countryCurrency);
    }

    watch([activeCountry, platformSettings], () => {
        syncCurrencyToCountry();
    }, { immediate: true });

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

            syncCurrencyToCountry();
        } catch (err) {
            console.error("General config fetch error", err);
        }
    }

    function setCountry(code) {
        activeCountryCode.value = code;
        localStorage.setItem('activeCountry', code);
        syncCurrencyToCountry();
    }

    function setCurrency(code) {
        activeCurrencyCode.value = code;
        localStorage.setItem('activeCurrency', code);
    }

    function formatPrice(amount, sourceCurrency = 'KES', targetCurrency = null) {
        const value = typeof amount === 'string' ? parseFloat(amount) : amount;
        if (isNaN(value)) return 'N/A';

        const source = resolveCurrency(sourceCurrency);
        const target = resolveCurrency(targetCurrency || activeCurrencyCode.value || resolvedCurrencyCode.value);
        const sourceRate = parseFloat(source.rate_to_default) || 1;
        const targetRate = parseFloat(target.rate_to_default) || 1;
        const converted = (value * sourceRate) / targetRate;
        const symbol = target.symbol || target.currency_code || '';
        const prefix = symbol ? `${symbol} ` : '';

        return `${prefix}${converted.toLocaleString(undefined, {
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
        resolveCurrency,
        fetchConfig,
        setCountry,
        setCurrency,
        formatPrice
    };
});
