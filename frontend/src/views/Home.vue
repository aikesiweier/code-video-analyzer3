<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>视频分析</template>
          <video-uploader @upload-success="handleUploadSuccess" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>智能体快速入口</template>
          <div v-for="agent in agents" :key="agent.id" class="agent-item">
            <el-button type="text" @click="$router.push(`/chat?agentId=${agent.id}`)">
              {{ agent.name }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VideoUploader from '../components/VideoUploader.vue'
import { listAgents } from '../api/agents'

const router = useRouter()
const agents = ref([])

onMounted(async () => {
  try {
    agents.value = await listAgents()
  } catch (e) {
    console.error('加载智能体列表失败', e)
  }
})

function handleUploadSuccess(taskId) {
  router.push({ name: 'TaskDetail', params: { id: taskId } })
}
</script>

<style scoped>
.home {
  margin-top: 10px;
}
.agent-item {
  margin: 8px 0;
}
</style>