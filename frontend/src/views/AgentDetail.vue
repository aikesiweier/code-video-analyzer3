<template>
  <div v-if="agent">
    <el-card>
      <template #header>
        <span>{{ agent.name }}</span>
        <el-button style="float: right" type="primary" @click="$router.push(`/chat?agentId=${agent.id}`)">对话</el-button>
      </template>
      <p><strong>描述：</strong>{{ agent.description }}</p>
      <p><strong>类型：</strong>{{ agent.agent_type }}</p>
      <p><strong>提示词：</strong>{{ agent.prompt_template }}</p>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getAgent } from '../api/agents'

const route = useRoute()
const agent = ref(null)

onMounted(async () => {
  try {
    agent.value = await getAgent(route.params.id)
  } catch (e) {
    console.error('加载智能体失败', e)
  }
})
</script>