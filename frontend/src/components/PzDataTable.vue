<template>
    <div class="pz-table-wrapper pz-data-table-shell">
        <table class="pz-table">
            <thead class="pz-table__head">
                <tr>
                    <th v-for="column in columns" :key="column.key" class="pz-table__th"
                        :class="{ 'pz-table__th--numeric': column.numeric }">
                        {{ column.label }}
                    </th>
                </tr>
            </thead>
            <tbody class="pz-table__body">
                <tr v-for="(row, index) in data" :key="index" class="pz-table__tr">
                    <td v-for="column in columns" :key="column.key" class="pz-table__td" :class="{
                        'pz-table__td--numeric': column.numeric,
                        'pz-table__td--mono': column.numeric || column.mono
                    }">
                        <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
                            {{ row[column.key] }}
                        </slot>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
    defineProps({
        columns: {
            type: Array,
            required: true
        },
        data: {
            type: Array,
            required: true
        }
    })
</script>

<style scoped>
    .pz-table-wrapper {
        overflow-x: auto;
        border: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
    }

    .pz-table {
        width: 100%;
        border-collapse: collapse;
        font-size: var(--pz-text-small);
    }

    .pz-table__head {
        background: linear-gradient(180deg, rgba(10, 10, 15, 0.98), rgba(30, 30, 38, 0.96));
    }

    .pz-table__th {
        padding: var(--pz-space-2) var(--pz-space-3);
        text-align: left;
        font-family: var(--pz-font-primary);
        font-weight: var(--pz-weight-semibold);
        color: var(--pz-color-limestone-white);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: var(--pz-text-caption);
        white-space: nowrap;
    }

    .pz-table__th--numeric {
        text-align: right;
    }

    .pz-table__tr:nth-child(even) {
        background-color: rgba(245, 245, 243, 0.8);
    }

    .pz-table__tr:hover {
        background: rgba(212, 101, 42, 0.04);
    }

    .pz-table__td {
        padding: var(--pz-space-2) var(--pz-space-3);
        color: var(--pz-color-text-primary);
        border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.1);
    }

    .pz-table__td--numeric {
        text-align: right;
    }

    .pz-table__td--mono {
        font-family: var(--pz-font-mono);
        font-variant-numeric: tabular-nums;
    }
</style>
