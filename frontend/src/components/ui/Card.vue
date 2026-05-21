<template>
    <div :class="cardClasses">
        <div v-if="$slots.header || title || eyebrow || icon" class="pz-card__header">
            <div class="pz-card__header-main">
                <span v-if="eyebrow" class="pz-card__eyebrow">{{ eyebrow }}</span>
                <div class="pz-card__header-row">
                    <span v-if="icon" class="pz-card__icon" v-html="icon"></span>
                    <h3 v-if="title" class="pz-card__title">{{ title }}</h3>
                </div>
            </div>
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
        interactive: Boolean,
        title: String,
        eyebrow: String,
        icon: String,
        bodyClass: String,
        variant: {
            type: String,
            default: 'default',
            validator: (v) => ['default', 'premium', 'glass', 'accent', 'elevated'].includes(v)
        },
        accentColor: {
            type: String,
            default: ''
        },
        padding: {
            type: String,
            default: 'medium',
            validator: (v) => ['none', 'small', 'medium', 'large'].includes(v)
        }
    })

    const cardClasses = computed(() => {
        const classes = {
            'pz-card': true,
            'pz-card--hoverable': props.hoverable || props.interactive,
            [`pz-card--padding-${props.padding}`]: true,
            [`pz-card--${props.variant}`]: true
        }
        if (props.accentColor) {
            classes[`pz-card--accent-${props.accentColor}`] = true
        }
        return classes
    })
</script>

<style scoped>
    .pz-card {
        background: #ffffff;
        border: 1px solid rgba(10, 10, 15, 0.12);
        border-radius: 14px;
        transition: border-color 0.35s ease, transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow:
            10px 10px 0 rgba(10, 10, 15, 0.03),
            0 2px 4px rgba(10, 10, 15, 0.03),
            0 10px 24px rgba(10, 10, 15, 0.04);
        height: 100%;
        overflow: hidden;
        position: relative;
    }

    /* Premium variant */
    .pz-card--premium {
        background: #ffffff;
        border: 1px solid rgba(10, 10, 15, 0.1);
        box-shadow:
            10px 10px 0 rgba(10, 10, 15, 0.02),
            0 6px 16px rgba(10, 10, 15, 0.04),
            0 18px 36px rgba(10, 10, 15, 0.04);
    }

    /* Glass variant */
    .pz-card--glass {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: blur(20px) saturate(1.4);
        -webkit-backdrop-filter: blur(20px) saturate(1.4);
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow:
            0 1px 2px rgba(10, 10, 15, 0.03),
            0 8px 24px rgba(10, 10, 15, 0.06);
    }

    /* Accent variant - left border */
    .pz-card--accent {
        border-left: 3px solid var(--pz-color-earth-orange, #d4652a);
        border-radius: 20px;
    }

    /* Elevated variant */
    .pz-card--elevated {
        background: #ffffff;
        box-shadow:
            12px 12px 0 rgba(10, 10, 15, 0.03),
            0 8px 20px rgba(10, 10, 15, 0.04),
            0 24px 48px rgba(10, 10, 15, 0.05);
    }

    /* Top accent line */
    .pz-card::before {
        content: '';
        position: absolute;
        inset: 0 0 auto 0;
        height: 3px;
        background: linear-gradient(90deg, rgba(212, 101, 42, 0), rgba(212, 101, 42, 0.7), rgba(212, 101, 42, 0));
        opacity: 0;
        transition: opacity 0.35s ease;
        pointer-events: none;
    }
    .pz-card--premium::before,
    .pz-card--elevated::before {
        background: linear-gradient(90deg, rgba(212, 101, 42, 0.5), rgba(184, 115, 51, 0.8), rgba(212, 101, 42, 0.5));
        opacity: 0.6;
    }

    /* Hover states */
    .pz-card--hoverable:hover {
        border-color: rgba(212, 101, 42, 0.25);
        transform: translateY(-5px);
        box-shadow:
            0 4px 8px rgba(10, 10, 15, 0.04),
            0 16px 32px rgba(10, 10, 15, 0.08),
            0 32px 64px rgba(10, 10, 15, 0.06);
    }

    .pz-card--hoverable.pz-card--premium:hover {
        box-shadow:
            0 4px 8px rgba(10, 10, 15, 0.03),
            0 16px 32px rgba(10, 10, 15, 0.06),
            0 32px 64px rgba(10, 10, 15, 0.08),
            0 0 0 1px rgba(212, 101, 42, 0.1);
    }

    .pz-card--hoverable.pz-card--elevated:hover {
        transform: translateY(-6px);
        box-shadow:
            0 4px 8px rgba(10, 10, 15, 0.03),
            0 20px 40px rgba(10, 10, 15, 0.06),
            0 48px 96px rgba(10, 10, 15, 0.08);
    }

    .pz-card--hoverable:hover::before,
    .pz-card:focus-within::before {
        opacity: 1 !important;
    }

    /* Padding variants */
    .pz-card--padding-none .pz-card__body {
        padding: 0;
    }
    .pz-card--padding-small .pz-card__body {
        padding: 1rem;
    }
    .pz-card--padding-medium .pz-card__body {
        padding: 1.4rem 1.5rem 1.5rem;
    }
    .pz-card--padding-large .pz-card__body {
        padding: 1.8rem 2rem 2rem;
    }

    /* Header */
    .pz-card__header {
        padding: 1rem 1.35rem 0.85rem;
        border-bottom: 1px solid rgba(10, 10, 15, 0.08);
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0));
    }

    .pz-card__header-main {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        min-width: 0;
    }

    .pz-card__header-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .pz-card__eyebrow {
        font-family: var(--pz-font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--pz-color-earth-orange);
    }

    .pz-card__icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.75rem;
        height: 1.75rem;
        border-radius: 8px;
        background: rgba(212, 101, 42, 0.1);
        color: var(--pz-color-earth-orange);
        flex-shrink: 0;
    }
    .pz-card__icon :deep(svg) {
        width: 1rem;
        height: 1rem;
    }

    .pz-card__title {
        margin: 0;
        font-family: var(--pz-font-display);
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
        color: var(--pz-color-foundation-black);
    }

    .pz-card__body {
        position: relative;
    }

    .pz-card__footer {
        padding: 0.95rem 1.35rem 1.1rem;
        border-top: 1px solid rgba(10, 10, 15, 0.08);
        background: linear-gradient(180deg, rgba(250, 249, 245, 0.3), rgba(255, 255, 255, 0.65));
    }
</style>
