<template>
    <div>
        <h2>New Task Create</h2>
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
                <lavel for="priority">Priority</lavel>
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
            <button type="submit">Create</button>
        </form>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter} from 'vue-router'

const router = useRouter()

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
    try {
        const res = await fetch('http://localhost:5000/api/tasks',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(form)
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
</script>