<template>
    <div :class="indicatorClasses">
        <span class="pz-phase__number">Phase {{ phase }}</span>
        <span class="pz-phase__name">{{ phaseName }}</span>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        phase: {
            type: Number,
            required: true,
            validator: (v) => v >= 1 && v <= 6
        },
        size: {
            type: String,
            default: 'medium'
        }
    })

    const phaseNames = {
        1: 'Materials',
        2: 'Contracts',
        3: 'Finance',
        4: 'Projects',
        5: 'Institutional',
        6: 'Infrastructure'
    }

    const phaseColors = {
        1: 'earth',
        2: 'steel',
        3: 'copper',
        4: 'violet',
        5: 'foundation',
        6: 'gradient'
    }

    const phaseName = computed(() => phaseNames[props.phase])

    const indicatorClasses = computed(() => ({
        'pz-phase': true,
        [`pz-phase--${props.size}`]: true,
        [`pz-phase--color-${phaseColors[props.phase]}`]: true
    }))
</script>

<style scoped>
    .pz-phase {
        display: inline-flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .pz-phase__number {
        font-family: var(--pz-font-mono);
        font-size: var(--pz-text-caption);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .pz-phase__name {
        font-family: var(--pz-font-display);
        font-weight: var(--pz-weight-bold);
    }

    .pz-phase--small .pz-phase__name {
        font-size: var(--pz-text-small);
    }

    .pz-phase--medium .pz-phase__name {
        font-size: var(--pz-text-body);
    }

    .pz-phase--large .pz-phase__name {
        font-size: var(--pz-text-h3);
    }

    .pz-phase--color-earth {
        color: var(--pz-color-earth-orange);
    }

    .pz-phase--color-steel {
        color: var(--pz-color-steel-blue);
    }

    .pz-phase--color-copper {
        color: var(--pz-color-copper-circuit);
    }

    .pz-phase--color-violet {
        color: var(--pz-color-african-violet);
    }

    .pz-phase--color-foundation {
        color: var(--pz-color-foundation-black);
    }
</style>
