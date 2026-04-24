<template>
    <button
        :class="buttonClasses"
        :disabled="disabled || loading"
        :aria-busy="loading"
        @click="$emit('click', $event)"
    >
        <span v-if="$slots.leading && !loading" class="pz-button__icon pz-button__icon--leading">
            <slot name="leading" />
        </span>
        <span v-if="loading" class="pz-button__spinner" aria-hidden="true"></span>
        <span class="pz-button__content" :class="{ 'pz-button__content--hidden': loading }">
            <slot></slot>
        </span>
        <span v-if="$slots.trailing && !loading" class="pz-button__icon pz-button__icon--trailing">
            <slot name="trailing" />
        </span>
    </button>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        variant: {
            type: String,
            default: 'primary',
            // Mapping old variants to new ones
            validator: (v) => ['primary', 'secondary', 'outline', 'ghost', 'danger', 'white', 'tertiary', 'success'].includes(v)
        },
        size: {
            type: String,
            default: 'md',
            validator: (v) => ['xs', 'sm', 'md', 'lg', 'small', 'medium', 'large'].includes(v)
        },
        disabled: Boolean,
        loading: Boolean,
        block: Boolean, // Alias for fullWidth
        fullWidth: Boolean,
        pill: Boolean
    })

    defineEmits(['click'])

    const buttonClasses = computed(() => {
        let v = props.variant;
        if (v === 'white') v = 'ghost';

        let s = props.size;
        if (s === 'xs') s = 'xsmall';
        if (s === 'sm') s = 'small';
        if (s === 'md') s = 'medium';
        if (s === 'lg') s = 'large';

        return {
            'pz-button': true,
            [`pz-button--${v}`]: true,
            [`pz-button--${s}`]: true,
            'pz-button--full-width': props.fullWidth || props.block,
            'pz-button--loading': props.loading,
            'pz-button--pill': props.pill
        }
    })
</script>

<style scoped>
    .pz-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: var(--pz-space-1);
        font-family: var(--pz-font-mono);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        border: var(--pz-border-width) solid var(--pz-border-color-strong);
        border-radius: var(--pz-border-radius-sm);
        cursor: pointer;
        transition: all var(--pz-transition-base);
        text-decoration: none;
        box-shadow: var(--pz-shadow-sm);
        line-height: 1;
        position: relative;
        isolation: isolate;
        overflow: hidden;
        min-height: 2.85rem;
        white-space: nowrap;
    }

    @media (min-width: 1024px) {
        .pz-button {
            transition: all var(--pz-transition-spring);
        }
    }

    .pz-button::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0));
        opacity: 0;
        transition: opacity var(--pz-transition-base);
        pointer-events: none;
    }

    .pz-button--xsmall {
        padding: 0.42rem 0.72rem;
        font-size: 0.62rem;
        min-height: 2rem;
    }

    .pz-button--small {
        padding: var(--pz-space-1) var(--pz-space-2);
        font-size: 0.68rem;
        min-height: 2.35rem;
    }

    .pz-button--medium {
        padding: var(--pz-space-2) var(--pz-space-3);
        font-size: 0.74rem;
    }

    .pz-button--large {
        padding: calc(var(--pz-space-2) + 0.25rem) var(--pz-space-4);
        font-size: 0.82rem;
        min-height: 3.2rem;
    }

    .pz-button--primary {
        background-color: var(--pz-color-earth-orange);
        color: var(--pz-color-limestone-white);
        border-color: var(--pz-color-earth-orange);
        box-shadow: var(--pz-shadow-offset-sm);
    }

    .pz-button--primary:hover:not(:disabled) {
        background-color: #A84C1F;
        border-color: #A84C1F;
        transform: translate(-2px, -2px);
    }

    @media (min-width: 1024px) {
        .pz-button--primary:hover:not(:disabled) {
            transform: translate(-3px, -3px);
            box-shadow: var(--pz-shadow-focal);
        }
    }

    .pz-button--secondary {
        background-color: var(--pz-color-foundation-black);
        color: var(--pz-color-limestone-white);
        border-color: var(--pz-color-foundation-black);
        box-shadow: var(--pz-shadow-offset-sm);
    }

    .pz-button--secondary:hover:not(:disabled) {
        transform: translate(-2px, -2px);
        box-shadow: var(--pz-shadow-focal);
    }

    .pz-button--outline {
        background-color: rgba(255, 255, 255, 0.84);
        color: var(--pz-color-foundation-black);
        border-color: var(--pz-color-foundation-black);
        box-shadow: var(--pz-shadow-offset-sm);
    }

    .pz-button--outline:hover:not(:disabled) {
        transform: translate(-2px, -2px);
        background-color: white;
        box-shadow: var(--pz-shadow-focal);
    }

    .pz-button--tertiary {
        background-color: transparent;
        color: var(--pz-color-text-primary);
        border-color: transparent;
        text-transform: none;
        letter-spacing: -0.01em;
        font-weight: var(--pz-weight-medium);
        font-family: var(--pz-font-primary);
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
        border-color: transparent;
        box-shadow: none;
    }

    .pz-button--ghost:hover:not(:disabled) {
        background-color: rgba(10, 10, 15, 0.06);
        color: var(--pz-color-foundation-black);
    }

    .pz-button--danger {
        background-color: var(--pz-color-danger);
        color: white;
        border-color: var(--pz-color-danger);
    }

    .pz-button--success {
        background-color: var(--pz-color-savanna-green);
        color: white;
        border-color: var(--pz-color-savanna-green);
    }

    .pz-button--success:hover:not(:disabled) {
        background-color: #047857;
        border-color: #047857;
        transform: translate(-2px, -2px);
        box-shadow: var(--pz-shadow-focal);
    }

    .pz-button:disabled {
        opacity: 0.58;
        cursor: not-allowed;
        transform: none;
        box-shadow: var(--pz-shadow-sm);
    }

    .pz-button:hover:not(:disabled)::before,
    .pz-button:focus-visible::before {
        opacity: 1;
    }

    .pz-button:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px rgba(212, 101, 42, 0.18), 0 0 0 1px rgba(10, 10, 15, 0.12), var(--pz-shadow-lg);
    }

    .pz-button--full-width {
        width: 100%;
    }

    .pz-button--pill {
        border-radius: var(--pz-border-radius-full);
    }

    .pz-button__spinner {
        width: 1em;
        height: 1em;
        border: 2px solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        animation: pz-spin 0.75s linear infinite;
        position: absolute;
    }

    .pz-button__content,
    .pz-button__icon {
        position: relative;
        z-index: 1;
    }

    .pz-button__content--hidden {
        opacity: 0;
    }

    .pz-button__icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05em;
    }

    @keyframes pz-spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
