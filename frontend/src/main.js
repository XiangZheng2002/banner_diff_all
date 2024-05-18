import "./assets/theme.scss";
import "./assets/main.scss";

import {createApp} from "vue";
import {createPinia} from "pinia";
import PrimeVue from "primevue/config";

import App from "./App.vue";
import router from "./router";

import ToastService from 'primevue/toastservice';
import Tooltip from "primevue/tooltip";

const app = createApp(App);

app.use(PrimeVue);
app.use(ToastService);
app.directive('tooltip', Tooltip);

app.use(createPinia());
app.use(router);

app.mount("#app");
