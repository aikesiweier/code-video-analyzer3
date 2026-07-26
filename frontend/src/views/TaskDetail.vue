<template>
  <div class="task-detail">
    <el-card v-if="task">
      <template #header>
        <span>任务 #{{ task.task_id }}</span>
        <el-button style="float: right" @click="$router.push('/video')">返回</el-button>
      </template>
      <div v-if="task.status === 'pending' || task.status === 'processing'">
        <el-progress :percentage="task.progress" :stroke-width="20" :text-inside="true" />
        <p class="status-text">状态: {{ task.status === 'pending' ? '等待处理' : '分析中...' }}</p>
      </div>
      <div v-else-if="task.status === 'completed'">
        <el-result icon="success" title="分析完成">
          <template #extra>
            <el-button type="primary" @click="$router.push(`/report/${task.task_id}`)">查看报告</el-button>
          </template>
        </el-result>
      </div>
      <div v-else-if="task.status === 'failed'">
        <el-result icon="error" title="处理失败" sub-title="请重试">
          <template #extra>
            <el-button @click="$router.push('/video')">返回</el-button>
          </template>
        </el-result>
      </div>
    </el-card>
    <el-empty v-else description="任务不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTaskStatus } from '../api/video'
import { ElMessage } from 'element-plus'

const route = useRoute()
const task = ref(null)
let interval = null

async function fetchStatus() {
  try {
    const data = await getTaskStatus(route.params.id)
    task.value = data
    if (data.status === 'completed' || data.status === 'failed') {
      clearInterval(interval)
    }
  } catch (e) {
    clearInterval(interval)
    ElMessage.error('获取状态失败')
  }
}

onMounted(() => {
  fetchStatus()
  interval = setInterval(fetchStatus, 3000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
.task-detail {
  max-width: 600px;
  margin: 20px auto;
}
.status-text {
  text-align: center;
  margin-top: 15px;
  color: #606266;
}
</style>