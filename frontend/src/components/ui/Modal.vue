<template>
    <div v-if="isOpen" class="pz-modal-overlay" @click.self="close">
        <div :class="computedClasses" role="dialog" aria-modal="true">
            <div class="pz-modal__header">
                <h3 class="pz-modal__title">{{ title }}</h3>
                <button class="pz-modal__close" @click="close" aria-label="Close">&times;</button>
            </div>

            <div class="pz-modal__body">
                <slot />
            </div>

            <div v-if="$slots.footer" class="pz-modal__footer">
                <slot name="footer" />
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        isOpen: {
            type: Boolean,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        size: {
            type: String,
            default: 'medium',
            validator: (v) => ['small', 'medium', 'large', 'xl', 'sm', 'md', 'lg'].includes(v)
        }
    })

    const emit = defineEmits(['close'])

    const close = () => {
        emit('close')
    }

    const computedClasses = computed(() => {
        let s = props.size;
        if (s === 'sm') s = 'small';
        if (s === 'md') s = 'medium';
        if (s === 'lg') s = 'large';

        return {
            'pz-modal': true,
            [`pz-modal--${s}`]: true
        }
    })
</script>

<style scoped>
    .pz-modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(10, 10, 15, 0.6);
        backdrop-filter: blur(4px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: var(--pz-z-modal);
        padding: var(--pz-space-4);
    }

    .pz-modal {
        background: var(--pz-color-limestone-white);
        border: var(--pz-border-width) solid var(--pz-color-foundation-black);
        width: 100%;
        max-height: 90vh;
        display: flex;
        flex-direction: column;
        box-shadow: 10px 10px 0px rgba(10, 10, 15, 0.1);
    }

    .pz-modal--small {
        max-width: 400px;
    }

    .pz-modal--medium {
        max-width: 600px;
    }

    .pz-modal--large {
        max-width: 800px;
    }

    .pz-modal--xl {
        max-width: 1000px;
    }

    .pz-modal__header {
        padding: var(--pz-space-4) var(--pz-space-6);
        border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: var(--pz-color-foundation-black);
        color: var(--pz-color-limestone-white);
    }

    .pz-modal__title {
        font-family: var(--pz-font-display);
        font-size: var(--pz-text-h4);
        margin: 0;
        color: inherit;
    }

    .pz-modal__close {
        background: none;
        border: none;
        font-size: 1.5rem;
        color: inherit;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity var(--pz-transition-fast);
    }

    .pz-modal__close:hover {
        opacity: 1;
    }

    .pz-modal__body {
        padding: var(--pz-space-6);
        overflow-y: auto;
        flex: 1;
    }

    .pz-modal__footer {
        padding: var(--pz-space-4) var(--pz-space-6);
        border-top: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
        display: flex;
        justify-content: flex-end;
        gap: var(--pz-space-2);
        background-color: rgba(113, 128, 150, 0.05);
    }
</style>
