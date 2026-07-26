<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-left">
          <h1>🤖 AI Agent 平台</h1>
        </div>
        <div class="header-right">
          <el-dropdown v-if="user">
            <span class="user-info">{{ user.username }}</span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button v-else type="primary" @click="$router.push('/login')">登录</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu router :default-active="$route.path">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/models">模型配置</el-menu-item>
            <el-menu-item index="/agents">智能体管理</el-menu-item>
            <el-menu-item index="/history">调用历史</el-menu-item>
            <el-menu-item index="/video">视频分析</el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import store from './store'

const router = useRouter()
const user = computed(() => store.state.user)

function logout() {
  store.commit('clearUser')
  router.push('/login')
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
  color: #2c3e50;
  height: 100vh;
}
.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.el-header h1 {
  margin: 0;
  font-size: 22px;
}
.header-right .user-info {
  cursor: pointer;
  color: white;
  font-weight: bold;
}
.el-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}
.el-main {
  padding: 20px;
  background-color: #f9fafc;
}
</style>