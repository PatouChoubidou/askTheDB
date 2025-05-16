import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

/* store */
app.use(createPinia())
/* router */ 
app.use(router)

app.mount('#app')
