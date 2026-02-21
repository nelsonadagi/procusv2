<template>
    <nav class="pz-nav" :class="{ 'pz-nav--dark': dark }">
        <div class="pz-nav__brand">
            <router-link to="/" class="pz-nav__logo">
                <span class="pz-nav__logo-text">PAANGUZO</span>
                <span class="pz-nav__logo-line"></span>
            </router-link>
        </div>

        <div class="pz-nav__menu">
            <router-link v-for="item in menuItems" :key="item.path" :to="item.path" class="pz-nav__link"
                :class="{ 'pz-nav__link--active': $route.path === item.path }">
                {{ item.label }}
            </router-link>
        </div>

        <div class="pz-nav__actions">
            <slot name="actions"></slot>
        </div>
    </nav>
</template>

<script setup>
    defineProps({
        dark: Boolean,
        menuItems: {
            type: Array,
            default: () => []
        }
    })
</script>

<style scoped>
    .pz-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 64px;
        padding: 0 var(--pz-space-4);
        background-color: var(--pz-color-limestone-white);
        border-bottom: var(--pz-border-width) solid rgba(113, 128, 150, 0.2);
    }

    .pz-nav--dark {
        background-color: var(--pz-color-foundation-black);
        border-bottom-color: rgba(250, 250, 248, 0.1);
    }

    .pz-nav__logo {
        display: flex;
        flex-direction: column;
        text-decoration: none;
    }

    .pz-nav__logo-text {
        font-family: var(--pz-font-display);
        font-size: var(--pz-text-h4);
        font-weight: var(--pz-weight-bold);
        color: var(--pz-color-foundation-black);
        letter-spacing: 0.02em;
    }

    .pz-nav--dark .pz-nav__logo-text {
        color: var(--pz-color-limestone-white);
    }

    .pz-nav__logo-line {
        display: block;
        height: 3px;
        background-color: var(--pz-color-earth-orange);
        margin-top: 2px;
    }

    .pz-nav__menu {
        display: flex;
        gap: var(--pz-space-4);
    }

    .pz-nav__link {
        font-family: var(--pz-font-primary);
        font-size: var(--pz-text-small);
        font-weight: var(--pz-weight-medium);
        color: var(--pz-color-text-secondary);
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: var(--pz-space-1) 0;
        border-bottom: 2px solid transparent;
        transition: all var(--pz-transition-fast);
    }

    .pz-nav__link:hover,
    .pz-nav__link--active {
        color: var(--pz-color-earth-orange);
        border-bottom-color: var(--pz-color-earth-orange);
    }

    .pz-nav--dark .pz-nav__link {
        color: var(--pz-color-concrete-grey);
    }

    .pz-nav--dark .pz-nav__link:hover,
    .pz-nav--dark .pz-nav__link--active {
        color: var(--pz-color-limestone-white);
        border-bottom-color: var(--pz-color-earth-orange);
    }
</style>
