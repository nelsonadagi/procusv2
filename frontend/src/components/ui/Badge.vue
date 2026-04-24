<template>
    <span :class="badgeClasses">
        <slot></slot>
    </span>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        variant: {
            type: String,
            default: 'default',
            validator: (v) => ['default', 'secondary', 'primary', 'success', 'warning', 'danger', 'error', 'info', 'finance', 'ghost', 'earth', 'savanna'].includes(v)
        },
        size: {
            type: String,
            default: 'medium'
        }
    })

    const badgeClasses = computed(() => {
        let v = props.variant;
        if (v === 'secondary') v = 'default';
        if (v === 'danger') v = 'error';
        if (v === 'primary') v = 'info';
        if (v === 'earth') v = 'warning';
        if (v === 'savanna') v = 'success';

        let s = props.size;
        if (s === 'xs') s = 'small';
        if (s === 'md') s = 'medium';
        if (s === 'sm') s = 'small';
        if (s === 'lg' || s === 'large') s = 'large';

        return {
            'pz-badge': true,
            [`pz-badge--${v}`]: true,
            [`pz-badge--${s}`]: true
        }
    })
</script>

<style scoped>
    .pz-badge {
        display: inline-flex;
        align-items: center;
        font-family: var(--pz-font-mono);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        border-radius: var(--pz-border-radius-sm);
        border: 1px solid currentColor;
        line-height: 1;
    }

    .pz-badge--small {
        padding: 0.28rem 0.52rem;
        font-size: 0.62rem;
    }

    .pz-badge--medium {
        padding: 0.42rem 0.7rem;
        font-size: 0.68rem;
    }

    .pz-badge--large {
        padding: 0.55rem 0.9rem;
        font-size: 0.72rem;
    }

    .pz-badge--default {
        background-color: rgba(113, 128, 150, 0.1);
        color: var(--pz-color-structural-steel);
    }

    .pz-badge--success {
        background-color: rgba(5, 150, 105, 0.1);
        color: var(--pz-color-savanna-green);
    }

    .pz-badge--info {
        background-color: rgba(37, 99, 235, 0.1);
        color: var(--pz-color-steel-blue);
    }

    .pz-badge--finance {
        background-color: rgba(184, 115, 51, 0.1);
        color: var(--pz-color-copper-circuit);
    }

    .pz-badge--warning {
        background-color: rgba(212, 101, 42, 0.1);
        color: var(--pz-color-earth-orange);
    }

    .pz-badge--error {
        background-color: var(--pz-color-danger-soft);
        color: var(--pz-color-danger);
    }

    .pz-badge--ghost {
        background-color: transparent;
        color: var(--pz-color-structural-steel);
    }
</style>
