<!-- FlaskApp/frontend/vue-task-app/src/TaskForm.vue -->
<template>
  <div>
    <h2>{{ isEdit ? 'タスク更新': 'タスク作成' }}</h2>
    <form
      class="grid"
      @submit.prevent="sendPrevent"
    >
      <!-- 一応divでまとめとく -->
      <div class="form-group">
        <label for="title">タスク名</label>
        <input
          id="title"
          v-model="form.title"
          required
        >
      </div>

      <div class="form-group">
        <label for="status">状況</label>
        <select
          id="status"
          v-model="form.status"
          required
        >
          <option>未着手</option>
          <option>作業中</option>
          <option>完了</option>
        </select>
      </div>

      <div class="form-group">
        <label for="priority">優先度</label>
        <select
          id="priority"
          v-model="form.priority"
          required
        >
          <option>-</option>
          <option>低</option>
          <option>中</option>
          <option>高</option>
        </select>
      </div>
      <div class="form-full">
        <label for="tag">タグ</label>
        <input
          id="tag"
          v-model="form.tag"
          list="tag-list"
          placeholder="タグ検索 or 選択"
        >
        <datalist id="tag-list">
          <option
            v-for=" tag in tagList"
            :key="tag"
            :value="tag"
          />
        </datalist>
      </div>

      <div class="form-group">
        <label for="start">開始日</label>
        <input
          id="start"
          v-model="form.start"
          type="date"
          required
        >
      </div>

      <div class="form-group">
        <label for="deadline">終了日</label>
        <input
          id="deadline"
          v-model="form.deadline"
          type="date"
          required
        >
      </div>

      <div class="form-full">
        <label for="memo">メモ</label>
        <textarea
          id="memo"
          v-model="form.memo"
        />
      </div>
      <div class="form-submit">
        <button
          type="submit"
          class="sub-btn"
        >
          {{ isEdit ? '更新': '新規作成' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import '../assets/style.css'
import { reactive , ref, onMounted} from 'vue';
import { useRouter, useRoute} from 'vue-router'

const router = useRouter()
const route = useRoute()
const isEdit = !!route.params.id

const tagList = ref([])

// 初期値
const form =reactive({
    title: '',
    status: '未着手',
    priority: '-',
    tag: '',
    start: '',
    deadline: '',
    memo: ''
})

const sendPrevent = async () => {
    let method
    let url
    if(isEdit){
        method = 'PUT'
        url = `http://localhost:5000/api/tasks/${route.params.id}`
    } else {
        method = 'POST'
        url = 'http://localhost:5000/api/tasks'
    }

    try {
        const res = await fetch(url,{
            method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(form) // JSON変換
        })
        // if 動いてる？
        if (!res.ok){
            const backendError = await res.json();
            throw new Error(`登録失敗しました: ${backendError.message || res.statusText}`)
        }
        router.push('/tasks')
    } catch (err) {
        alert(err.message)
    }
}

onMounted(async () => {
    try{
        const res = await fetch('http://localhost:5000/api/tasks')
        const tasks = await res.json()

        tagList.value = [...new Set(tasks.map(task => task.tag).filter(Boolean))]

        if (isEdit) {
            const task = tasks.find(task => task.id === parseInt(route.params.id))
            if(task) {
                Object.assign(form,task)
            }
        }
    } catch (err) {
        console.error('タスク・タグ取得失敗',err)
    }
})
</script>