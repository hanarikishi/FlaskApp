<template>
    <div>
        <h2>{{ isEdit ? 'EditMode': 'Create Mode' }}</h2>
        <form @submit.prevent="sendPrevent">
            <!-- 一応divでまとめとく -->
            <div>
                <label for="title">Task Name</label>
                <input id="title" v-model="form.title" required>
            </div>

            <div>
                <label for="deadline">Deadline</label>
                <input id="deadline" v-model="form.deadline" type="date" required>
            </div>

            <div>
                <label for="status">Status</label>
                <select id="status" v-model="form.status" required>
                    <option>Todo</option>
                    <option>Doing</option>
                    <option>Done</option>
                </select>
            </div>

            <div>
                <label for="priority">Priority</label>
                <select id="priority" v-model="form.priority" required>
                    <option>-</option>
                    <option>Low</option>
                    <option>Medium</option>
                    <option>High</option>
                </select>
            </div>

            <div>
                <label for="tag">Tag</label>
                <!-- 
                【追加する機能】
                ・今あるタグのリストから選べる
                ・新たにタグを作成したらリストに入る
                ・入力中に予測してくれるやつ(オートコンプリート？)
                -->
                <input id="tag" v-model="form.tag">
            </div>

            <div>
                <label for="memo">Memo</label>
                <textarea id="memo" v-model="form.memo"></textarea>
            </div>
            <button type="submit">{{ isEdit ? 'Update': 'Create' }}</button>
        </form>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter, useRoute} from 'vue-router'
import { onMounted } from 'vue';

const router = useRouter()
const route = useRoute()
const isEdit = !!route.params.id

// 初期値
const form =reactive({
    title: '',
    deadline: '',
    status: 'Todo',
    priority: '-',
    tag: '',
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
    if (isEdit) {
        const res = await fetch('http://localhost:5000/api/tasks')
        const tasks = await res.json()
        const task = tasks.find(task => task.id === parseInt(route.params.id))
        if(task) {
            Object.assign(form,task)
        }
    }
})
</script>