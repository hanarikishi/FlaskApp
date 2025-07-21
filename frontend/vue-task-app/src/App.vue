<!-- FlaskApp/frontend/vue-task-app/src/App.vue -->
<template>
  <div class="container">
    <h1>はなりきしタスク</h1>

    <nav class="nav">
      <router-link to="/tasks">一覧</router-link>
      <router-link to="/tasks/register">新規作成</router-link>
    </nav>

    <div class="view">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: 40px auto;
  padding: 20px;
  font-family: sans-serif;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  font-size: 28px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 8px;
  margin-bottom: 20px;
}

.nav {
  margin-bottom: 20px;
}

.nav a {
  margin-right: 20px;
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

.nav a:hover {
  color: #0056b3;
}

.view {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}
</style>
