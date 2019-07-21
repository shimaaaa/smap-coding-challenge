import Vue from "vue";
import App from "@/App.vue";
import router from '@/router'

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

window.Vue = Vue;

const app = new Vue({
    el: '#app',
    router,
    template: '<App/>',
    components: { App }
});
