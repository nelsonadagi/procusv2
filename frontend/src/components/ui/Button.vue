<template>
    <button :class="buttonClasses" :disabled="disabled || loading" @click="$emit('click', $event)">
        <span v-if="loading" class="pz-button__spinner"></span>
        <slot v-else></slot>
    </button>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        variant: {
            type: String,
            default: 'primary',
            // Mapping old variants to new ones
            validator: (v) => ['primary', 'secondary', 'outline', 'ghost', 'danger', 'white', 'tertiary'].includes(v)
        },
        size: {
            type: String,
            default: 'md',
            validator: (v) => ['sm', 'md', 'lg', 'small', 'medium', 'large'].includes(v)
        },
        disabled: Boolean,
        loading: Boolean,
        block: Boolean, // Alias for fullWidth
        fullWidth: Boolean
    })

    defineEmits(['click'])

    const buttonClasses = computed(() => {
        let v = props.variant;
        if (v === 'outline') v = 'secondary';
        if (v === 'white') v = 'ghost';

        let s = props.size;
        if (s === 'sm') s = 'small';
        if (s === 'md') s = 'medium';
        if (s === 'lg') s = 'large';

        return {
            'pz-button': true,
            [`pz-button--${v}`]: true,
            [`pz-button--${s}`]: true,
            'pz-button--full-width': props.fullWidth || props.block,
            'pz-button--loading': props.loading
        }
    })
</script>

<style scoped>
    .pz-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: var(--pz-space-1);
        font-family: var(--pz-font-primary);
        font-weight: var(--pz-weight-semibold);
        text-transform: uppercase;
        letter-spacing: 0.0625em;
        border: var(--pz-border-width) solid transparent;
        border-radius: var(--pz-border-radius);
        cursor: pointer;
        transition: all var(--pz-transition-base);
        text-decoration: none;
    }

    @media (min-width: 1024px) {
        .pz-button {
            transition: all var(--pz-transition-spring);
        }
    }

    .pz-button--small {
        padding: var(--pz-space-1) var(--pz-space-2);
        font-size: var(--pz-text-caption);
    }

    .pz-button--medium {
        padding: var(--pz-space-2) var(--pz-space-3);
        font-size: var(--pz-text-small);
    }

    .pz-button--large {
        padding: calc(var(--pz-space-2) + 0.25rem) var(--pz-space-4);
        font-size: var(--pz-text-body);
    }

    .pz-button--primary {
        background-color: var(--pz-color-earth-orange);
        color: var(--pz-color-limestone-white);
        border-color: var(--pz-color-earth-orange);
    }

    .pz-button--primary:hover:not(:disabled) {
        background-color: #B8531F;
        border-color: #B8531F;
        transform: translateY(-2px);
    }

    @media (min-width: 1024px) {
        .pz-button--primary:hover:not(:disabled) {
            transform: translateY(-4px) scale(1.02);
            box-shadow: var(--pz-shadow-focal);
        }
    }

    .pz-button--secondary {
        background-color: transparent;
        color: var(--pz-color-steel-blue);
        border-color: var(--pz-color-steel-blue);
    }

    .pz-button--secondary:hover:not(:disabled) {
        background-color: rgba(37, 99, 235, 0.1);
    }

    @media (min-width: 1024px) {
        .pz-button--secondary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: var(--pz-shadow-sm);
        }
    }

    .pz-button--tertiary {
        background-color: transparent;
        color: var(--pz-color-text-primary);
        border-color: transparent;
        text-transform: none;
        letter-spacing: normal;
        font-weight: var(--pz-weight-medium);
    }

    .pz-button--tertiary::after {
        content: '→';
        margin-left: var(--pz-space-1);
        transition: transform var(--pz-transition-base);
    }

    @media (min-width: 1024px) {
        .pz-button--tertiary::after {
            transition: transform var(--pz-transition-spring);
        }
    }

    .pz-button--tertiary:hover:not(:disabled)::after {
        transform: translateX(4px);
    }

    .pz-button--ghost {
        background-color: transparent;
        color: var(--pz-color-text-secondary);
        border-color: var(--pz-color-concrete-grey);
    }

    .pz-button--danger {
        background-color: #ef4444;
        color: white;
        border-color: #ef4444;
    }

    .pz-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .pz-button--full-width {
        width: 100%;
    }

    .pz-button__spinner {
        width: 1em;
        height: 1em;
        border: 2px solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        animation: pz-spin 0.75s linear infinite;
    }

    @keyframes pz-spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
