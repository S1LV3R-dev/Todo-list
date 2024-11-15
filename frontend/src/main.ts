import './assets/main.css'
import '@fortawesome/fontawesome-free/css/all.css'

import { createApp } from 'vue'
import App from './App.vue'
import 'vue-toastification/dist/index.css'
import Toast from 'vue-toastification'
import router from './router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon as any)
app.use(Toast)
app.use(router)

app.mount('#app')
