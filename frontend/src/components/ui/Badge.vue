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
            validator: (v) => ['default', 'secondary', 'primary', 'success', 'warning', 'danger', 'error', 'info', 'finance'].includes(v)
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

        let s = props.size;
        if (s === 'md') s = 'medium';
        if (s === 'sm') s = 'small';

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
        font-family: var(--pz-font-primary);
        font-weight: var(--pz-weight-medium);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: var(--pz-border-radius);
    }

    .pz-badge--small {
        padding: 0.25rem 0.5rem;
        font-size: var(--pz-text-caption);
    }

    .pz-badge--medium {
        padding: 0.5rem 0.75rem;
        font-size: var(--pz-text-small);
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
        background-color: rgba(212, 101, 42, 0.15);
        color: #B8531F;
    }
</style>
