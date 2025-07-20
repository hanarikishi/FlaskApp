<template>
  <div class="list">
    <h2>タスク一覧</h2>
    <div v-if="loading" class="status">loading...</div>
    <div v-else-if="error" class="error">Error：{{ error }}</div>
      <table>
        <thead>
          <tr>
            <th>タイトル</th>
            <th>開始</th>
            <th>期限</th>
            <th>状態</th>
            <th>優先度</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>
              <router-link :to="`/tasks/${task.id}/edit`">
                {{ task.title }}
              </router-link>
            </td>
            <td>
              <input v-model="task.start" @chage="updateStatus">
            </td>
            <td>
              <input v-model="task.deadline" @chage="updateStatus">
            </td>
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
            <button @click="confirmDelete(task.id)" class="del-btn">Delete</button>
          </tr>
        </tbody>
      </table>
  </div>
</template>

<script setup>
import '../assets/style.css'
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
    error.value = err.messagegit
  } finally {
    loading.value = false
  }
}

onMounted(fetchTasks)

// 状況、優先度変更
const updateStatus = async (task) => {
  try{
    const res = await fetch(`http://localhost:5000/api/tasks/${task.id}`,{
      method: 'PUT',
      headers: {'Content-Type' : 'application/json'},
      body: JSON.stringify(task)
    })
    if (!res.ok) {
      throw new Error('ステータス更新失敗しました')
    }
  } catch (err) {
    alert(err.message)
  }
}

// 削除
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

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 2px;
    text-align: left;
  }

  th:nth-child(1), td:nth-child(1) { /* タイトル */
    width: 20%;
    white-space: nowrap;
  }

  th:nth-child(2), td:nth-child(2), /* 開始 */
  th:nth-child(3), td:nth-child(3) { /* 期限 */ 
    width: 40%;
  }

  /* th:nth-child(4), td:nth-child(4),
  th:nth-child(5), td:nth-child(5){
  width: 10%;
  } */

  input {
    width: 100%;
    box-sizing: border-box;
  }

  .del-btn {
    margin-left: 2px;
  }
</style>
