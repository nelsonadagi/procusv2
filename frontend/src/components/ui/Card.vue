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
        background-color: var(--pz-color-limestone-white);
        border: var(--pz-border-width) solid rgba(113, 128, 150, 0.2);
        border-radius: var(--pz-border-radius);
        transition: border-color var(--pz-transition-base);
        height: 100%;
    }

    .pz-card--hoverable:hover {
        border-color: var(--pz-color-earth-orange);
    }

    .pz-card--padding-none .pz-card__body {
        padding: 0;
    }

    .pz-card--padding-small .pz-card__body {
        padding: var(--pz-space-2);
    }

    .pz-card--padding-medium .pz-card__body {
        padding: var(--pz-space-3);
    }

    .pz-card--padding-large .pz-card__body {
        padding: var(--pz-space-4);
    }

    .pz-card__header {
        padding: var(--pz-space-3);
        border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .pz-card__title {
        margin: 0;
        font-size: var(--pz-text-h4);
    }

    .pz-card__footer {
        padding: var(--pz-space-3);
        border-top: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
    }
</style>
