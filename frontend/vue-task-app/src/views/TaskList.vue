<template>
  <div>
    <h2>TaskList</h2>
    <div v-if="loading">loading...</div>
    <div v-else-if="error">Error：{{ error }}</div>
    <ul v-else>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} ({{ task.deadline }}) - ({{ task.status }})
        <button @click="confirmDelete(task.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const loading = ref(true)
const error = ref(null)

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:5000/api/tasks')
    if (!res.ok) throw new Error('APIエラー')
    tasks.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchTasks)

const confirmDelete = async (id) => {
  const ok = confirm('このタスクを削除しますか？')
  if (!ok) return

  try {
    const res = await fetch(`http://localhost:5000/api/tasks/${id}`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('削除に失敗しました')

    // 成功時はリストから削除（再取得せず反映）
    tasks.value = tasks.value.filter(task => task.id !== id)
  } catch (err) {
    alert(err.message)
  }
}
</script>