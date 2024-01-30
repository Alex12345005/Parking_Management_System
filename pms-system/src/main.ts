import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import VueApexCharts from 'vue3-apexcharts'
import router from './router';
import './uikit/css/uikit.css';
import './uikit/js/uikit.js'; 
import './uikit/js/uikit-icons.js';

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VueApexCharts)
app.mount('#app');
