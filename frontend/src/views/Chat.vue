<template>
  <div class="chat-container">
    <el-card>
      <template #header>对话</template>
      <div class="chat-messages" ref="msgContainer">
        <div v-for="(msg, idx) in messages" :key="idx" class="message">
          <el-tag :type="msg.role === 'user' ? 'primary' : 'success'">
            {{ msg.role === 'user' ? '我' : '助手' }}
          </el-tag>
          <div class="content" v-html="msg.content"></div>
        </div>
      </div>
      <div class="chat-input">
        <el-input v-model="input" placeholder="输入消息..." @keyup.enter="sendMessage" />
        <el-button type="primary" @click="sendMessage" :disabled="!input.trim() || loading">发送</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import apiClient from '../api'

const route = useRoute()
const agentId = ref(route.query.agentId || 1)
const input = ref('')
const loading = ref(false)
const messages = ref([])
const msgContainer = ref(null)

async function sendMessage() {
  if (!input.value.trim() || loading.value) return
  const userMsg = { role: 'user', content: input.value }
  messages.value.push(userMsg)
  const userInput = input.value
  input.value = ''
  loading.value = true

  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ agent_id: agentId.value, message: userInput })
    })

    if (!response.ok) throw new Error('请求失败')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let assistantMsg = { role: 'assistant', content: '' }
    messages.value.push(assistantMsg)
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      buffer += chunk
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') continue
          try {
            const token = JSON.parse(data).data
            if (token) {
              assistantMsg.content += token
              // 更新显示
              const idx = messages.value.length - 1
              messages.value[idx] = { ...assistantMsg }
              await nextTick()
              scrollToBottom()
            }
          } catch (e) {}
        }
      }
    }
    loading.value = false
    scrollToBottom()
  } catch (e) {
    ElMessage.error('对话失败')
    loading.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  if (!route.query.agentId) {
    ElMessage.warning('请选择智能体')
  }
})
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
}
.chat-messages {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #dcdfe6;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}
.message {
  margin-bottom: 12px;
}
.content {
  margin-top: 4px;
  white-space: pre-wrap;
}
.chat-input {
  display: flex;
  gap: 10px;
}
</style>