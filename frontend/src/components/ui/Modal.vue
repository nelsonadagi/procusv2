<template>
    <Teleport to="body">
        <div v-if="isOpen" class="pz-modal-overlay" @click.self="close">
            <div
                ref="modalRef"
                :class="computedClasses"
                role="dialog"
                aria-modal="true"
                :aria-label="title"
                tabindex="-1"
            >
                <div class="pz-modal__header">
                    <div class="pz-modal__heading">
                        <span class="pz-modal__eyebrow">Workspace Panel</span>
                        <h3 class="pz-modal__title">{{ title }}</h3>
                    </div>
                    <button ref="closeBtnRef" class="pz-modal__close" @click="close" aria-label="Close dialog">&times;</button>
                </div>

                <div class="pz-modal__body">
                    <slot />
                </div>

                <div v-if="$slots.footer" class="pz-modal__footer">
                    <slot name="footer" />
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
    import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'

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
    const modalRef = ref(null)
    const closeBtnRef = ref(null)
    let lastFocusedElement = null
    let focusTrapHandler = null

    const close = () => {
        emit('close')
    }

    /** Get all focusable elements inside the modal */
    function getFocusableElements() {
        if (!modalRef.value) return []
        const selector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        return Array.from(modalRef.value.querySelectorAll(selector)).filter(
            (el) => !el.disabled && !el.getAttribute('aria-hidden') && el.offsetParent !== null
        )
    }

    /** Trap focus within modal */
    function trapFocus(event) {
        if (event.key !== 'Tab') return
        const focusable = getFocusableElements()
        if (focusable.length === 0) {
            event.preventDefault()
            return
        }
        const first = focusable[0]
        const last = focusable[focusable.length - 1]

        if (event.shiftKey) {
            if (document.activeElement === first || !modalRef.value.contains(document.activeElement)) {
                event.preventDefault()
                last.focus()
            }
        } else {
            if (document.activeElement === last) {
                event.preventDefault()
                first.focus()
            }
        }
    }

    const handleKeydown = (event) => {
        if (event.key === 'Escape' && props.isOpen) {
            close()
        }
        if (props.isOpen) {
            trapFocus(event)
        }
    }

    watch(
        () => props.isOpen,
        async (isOpen) => {
            if (typeof document === 'undefined') {
                return
            }

            if (isOpen) {
                lastFocusedElement = document.activeElement
                document.body.style.overflow = 'hidden'
                window.addEventListener('keydown', handleKeydown)
                await nextTick()
                // Focus the first focusable element (prefer close button for predictable behavior)
                const focusable = getFocusableElements()
                if (focusable.length > 0) {
                    // Focus close button first, or first input if no close button
                    const closeBtn = focusable.find((el) => el.getAttribute('aria-label') === 'Close dialog')
                    ;(closeBtn || focusable[0]).focus()
                } else {
                    modalRef.value?.focus()
                }
            } else {
                document.body.style.overflow = ''
                window.removeEventListener('keydown', handleKeydown)
                // Return focus to trigger element
                if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
                    await nextTick()
                    lastFocusedElement.focus()
                }
            }
        },
        { immediate: true }
    )

    onBeforeUnmount(() => {
        if (typeof document !== 'undefined') {
            document.body.style.overflow = ''
        }
        window.removeEventListener('keydown', handleKeydown)
    })

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
        background:
            radial-gradient(circle at top, rgba(212, 101, 42, 0.16), transparent 32%),
            rgba(10, 10, 15, 0.72);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: var(--pz-z-modal);
        padding: var(--pz-space-4);
    }

    .pz-modal {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 247, 242, 0.94));
        border: 1px solid rgba(10, 10, 15, 0.12);
        width: 100%;
        max-height: 90vh;
        display: flex;
        flex-direction: column;
        border-radius: var(--pz-border-radius-lg);
        box-shadow: 0 28px 64px rgba(10, 10, 15, 0.24);
        overflow: hidden;
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
        padding: 1.1rem 1.25rem;
        border-bottom: var(--pz-border-width) solid rgba(10, 10, 15, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        background:
            linear-gradient(135deg, rgba(10, 10, 15, 0.98), rgba(45, 55, 72, 0.96));
        color: var(--pz-color-limestone-white);
    }

    .pz-modal__heading {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .pz-modal__eyebrow {
        font-family: var(--pz-font-mono);
        font-size: 0.64rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.64);
    }

    .pz-modal__title {
        font-family: var(--pz-font-display);
        font-size: 1.1rem;
        letter-spacing: -0.03em;
        margin: 0;
        color: inherit;
    }

    .pz-modal__close {
        width: 2.5rem;
        height: 2.5rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 999px;
        font-size: 1.5rem;
        color: inherit;
        cursor: pointer;
        opacity: 0.82;
        transition: all var(--pz-transition-fast);
    }

    .pz-modal__close:hover {
        opacity: 1;
        transform: translateY(-1px);
        background: rgba(255, 255, 255, 0.14);
    }

    .pz-modal__close:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.18);
    }

    .pz-modal__body {
        padding: 1.35rem 1.25rem 1.25rem;
        overflow-y: auto;
        flex: 1;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.92));
    }

    .pz-modal__footer {
        padding: 1rem 1.25rem;
        border-top: var(--pz-border-width) solid rgba(10, 10, 15, 0.08);
        display: flex;
        justify-content: flex-end;
        gap: var(--pz-space-2);
        background:
            linear-gradient(180deg, rgba(241, 240, 235, 0.5), rgba(255, 255, 255, 0.9));
    }
</style>
