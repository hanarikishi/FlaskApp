// FlaskApp/frontend/vue-task-app/src/route/index.js
import {createRouter, createWebHistory } from 'vue-router'
import TaskList from '../views/TaskList.vue'
import TaskForm from '../views/TaskForm.vue'

// ルーティングを設定
const routes = [
  { path: '/tasks', component: TaskList },
  { path: '/tasks/register', component: TaskForm },
  { path: '/tasks/:id/edit', component: TaskForm, props: true }
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router