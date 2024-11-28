import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'
import router from './router.js'
import store from './store.js'
import vuex from 'vuex'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(vuex)
app.mount('#app')
