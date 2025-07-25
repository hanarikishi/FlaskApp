// FlaskApp/frontend/vue-task-app/src/main.js
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

createApp(App)
    .use(router)
    .mount('#app')
