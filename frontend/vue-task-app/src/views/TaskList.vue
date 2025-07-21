<!-- FlaskApp/frontend/vue-task-app/src/TaskList.vue -->
<template>
    <h2>タスク一覧</h2>
    <div class="filter-bar">
      <label class="filter-label">
        ステータス：
        <select v-model="filterStatus">
          <option value="">すべて</option>
          <option>未着手</option>
          <option>作業中</option>
          <option>完了</option>
        </select>
      </label>

      <label class="filter-label">
        キーワード：
        <input type="text" v-model="filterKeyword" placeholder="タイトル or タグ検索">
      </label>
    </div>

    <div v-if="loading" class="status">loading...</div>
    <div v-else-if="error" class="error">Error：{{ error }}</div>

    <table v-else class="task-table">
      <thead>
        <tr>
          <th>タイトル</th>
          <th>開始</th>
          <th>期限</th>
          <th>状態</th>
          <th>優先度</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in filteredTasks" :key="task.id">
          <td>
            <router-link :to="`/tasks/${task.id}/edit`">
              {{ task.title }}
            </router-link>
          </td>
          <td><input type="date" v-model="task.start" @change="updateStatus(task)" /></td>
          <td><input type="date" v-model="task.deadline" @change="updateStatus(task)" /></td>
          <td>
            <select v-model="task.status" @change="updateStatus(task)">
              <option>未着手</option>
              <option>作業中</option>
              <option>完了</option>
            </select>
          </td>
          <td>
            <select v-model="task.priority" @change="updateStatus(task)">
              <option>-</option>
              <option>低</option>
              <option>中</option>
              <option>高</option>
            </select>
          </td>
          <td><button @click="confirmDelete(task.id)" class="del-btn">Delete</button></td>
        </tr>
      </tbody>
    </table>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import GanttChart from './GanttChart.vue'

const tasks = ref([])
const loading = ref(true)
const error = ref(null)
const filterStatus = ref('')
const filterKeyword = ref('')

const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchStatus = filterStatus.value === '' || task.status === filterStatus.value
    const keyword = filterKeyword.value.toLowerCase()
    const matchKeyword =
      task.title.toLowerCase().includes(keyword) ||
      (task.tag || '').toLowerCase().includes(keyword)
    return matchStatus && matchKeyword
  })
})

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:5000/api/tasks')
    if (!res.ok) throw new Error('APIエラー')
    tasks.value = await res.json()
    console.log('✅ tasks fetched:', tasks.value)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchTasks)

watch(filteredTasks, (newVal) => {
  console.log('🔁 filteredTasks updated:', newVal)
})

const updateStatus = async (task) => {
  try {
    const res = await fetch(`http://localhost:5000/api/tasks/${task.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task)
    })
    if (!res.ok) throw new Error('ステータス更新失敗')
  } catch (err) {
    alert(err.message)
  }
}

const confirmDelete = async (id) => {
  const ok = confirm('このタスクを削除しますか？')
  if (!ok) return
  try {
    const res = await fetch(`http://localhost:5000/api/tasks/${id}`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error('削除に失敗しました')
    tasks.value = tasks.value.filter(task => task.id !== id)
  } catch (err) {
    alert(err.message)
  }
}
</script>

<style scoped>

/* テーブル関連 */
.task-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.task-table th,
.task-table td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ccc;
}
.task-table td:first-child {
  text-align: left;
  word-break: break-word;
  max-width: 250px;
}
.task-table input {
  width: 100%;
  padding: 4px;
  box-sizing: border-box;
}

.del-btn {
  padding: 4px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.del-btn:hover {
  background-color: #d32f2f;
}

/* フィルター */
.filter-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  align-items: center;
}
.filter-label {
  display: flex;
  gap: 8px;
  align-items: center;
  font-weight: bold;
}
</style>
