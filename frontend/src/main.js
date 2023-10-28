import '@arco-design/web-vue/dist/arco.css';
import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';
import 'bootstrap/dist/css/bootstrap.min.css'


const app = createApp(App)

app.use(router)
app.use(VueCookies, {expires: '7d'})
app.use(ArcoVueIcon);
app.use(ArcoVue);
app.mount('#app')
