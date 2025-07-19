<template>
  <div>
    <h2>Task</h2>
    <div v-if="loading">loading...</div>
    <div v-else-if="error">Error：{{ error }}</div>
    <ul v-else>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} ({{ task.deadline }}) - ({{ task.status }})
      </li>
    </ul>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'

const tasks   = ref([])
const loading = ref(true)
const error   = ref(null)

onMounted(async () =>{
  try {
    const res = await fetch('http://localhost:5000/api/tasks')
    if (!res.ok) throw new Error('APIエラー')
    tasks.value = await res.json()
  } catch (err){
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>