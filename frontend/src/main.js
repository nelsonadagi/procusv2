import { createApp } from 'vue'
import './styles/main.css'
import App from './App.vue'

import { createPinia } from 'pinia'
import router from './router'
import { createI18n } from 'vue-i18n'
import VueApexCharts from 'vue3-apexcharts'

const messages = {
  en: {
    message: {
      hello: 'Hello World',
      welcome: 'Welcome to Ujenzi Marketplace'
    },
    app: {
      logoText: 'PAANGUZO'
    },
    nav: {
      explore: 'Explore'
    }
  },
  sw: {
    message: {
      hello: 'Habari Dunia',
      welcome: 'Karibu Soko la Ujenzi'
    },
    app: {
      logoText: 'PAANGUZO'
    },
    nav: {
      explore: 'Chunguza'
    }
  }
}

const i18n = createI18n({
  locale: 'en', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages, // set locale messages
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n) // Use the i18n instance
app.use(VueApexCharts)
// Click outside directive
app.directive('click-outside', {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener("click", el.clickOutsideEvent);
  },
});

app.mount('#app')
