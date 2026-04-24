<template>
    <div :class="cardClasses">
        <div v-if="$slots.header || title" class="pz-card__header">
            <h3 v-if="title" class="pz-card__title">{{ title }}</h3>
            <slot name="header"></slot>
        </div>
        <div :class="['pz-card__body', bodyClass]">
            <slot></slot>
        </div>
        <div v-if="$slots.footer" class="pz-card__footer">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        hoverable: Boolean,
        interactive: Boolean, // Alias for hoverable
        title: String,
        bodyClass: String,
        padding: {
            type: String,
            default: 'medium',
            validator: (v) => ['none', 'small', 'medium', 'large'].includes(v)
        }
    })

    const cardClasses = computed(() => ({
        'pz-card': true,
        'pz-card--hoverable': props.hoverable || props.interactive,
        [`pz-card--padding-${props.padding}`]: true
    }))
</script>

<style scoped>
    .pz-card {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 247, 242, 0.94));
        border: 1px solid rgba(10, 10, 15, 0.1);
        border-radius: var(--pz-border-radius-lg);
        transition: border-color var(--pz-transition-base), transform var(--pz-transition-base), box-shadow var(--pz-transition-base);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.92),
            0 16px 32px rgba(10, 10, 15, 0.08);
        height: 100%;
        overflow: hidden;
        position: relative;
    }

    .pz-card::before {
        content: '';
        position: absolute;
        inset: 0 0 auto 0;
        height: 3px;
        background: linear-gradient(90deg, rgba(212, 101, 42, 0), rgba(212, 101, 42, 0.82), rgba(212, 101, 42, 0));
        opacity: 0;
        transition: opacity var(--pz-transition-base);
        pointer-events: none;
    }

    .pz-card--hoverable:hover {
        border-color: var(--pz-color-earth-orange);
        transform: translateY(-6px);
        box-shadow:
            0 24px 46px rgba(10, 10, 15, 0.12),
            0 0 0 1px rgba(212, 101, 42, 0.12);
    }

    .pz-card--hoverable:hover::before,
    .pz-card:focus-within::before {
        opacity: 1;
    }

    .pz-card--padding-none .pz-card__body {
        padding: 0;
    }

    .pz-card--padding-small .pz-card__body {
        padding: 0.9rem;
    }

    .pz-card--padding-medium .pz-card__body {
        padding: 1.2rem 1.25rem 1.25rem;
    }

    .pz-card--padding-large .pz-card__body {
        padding: 1.6rem;
    }

    .pz-card__header {
        padding: 1rem 1.25rem 0.95rem;
        border-bottom: 1px solid rgba(10, 10, 15, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        background:
            linear-gradient(180deg, rgba(10, 10, 15, 0.04), rgba(255, 255, 255, 0));
    }

    .pz-card__title {
        margin: 0;
        font-family: var(--pz-font-display);
        font-size: 1.02rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.15;
        color: var(--pz-color-foundation-black);
    }

    .pz-card__body {
        position: relative;
    }

    .pz-card__footer {
        padding: 0.95rem 1.25rem 1.1rem;
        border-top: 1px solid rgba(10, 10, 15, 0.08);
        background:
            linear-gradient(180deg, rgba(241, 240, 235, 0.36), rgba(255, 255, 255, 0.72));
    }
</style>
