<template>
  <div>
    <el-button type="primary" @click="showDialog = true">添加智能体</el-button>
    <el-table :data="agents" style="margin-top: 20px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="agent_type" label="类型" />
      <el-table-column prop="is_active" label="启用">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/agent/${row.id}`)">详情</el-button>
          <el-button size="small" @click="editAgent(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editing ? '编辑智能体' : '添加智能体'" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
        <el-form-item label="模型配置">
          <el-select v-model="form.model_config_id" placeholder="选择模型">
            <el-option v-for="m in models" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="提示词模板">
          <el-input v-model="form.prompt_template" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.agent_type">
            <el-option label="聊天" value="chat" />
            <el-option label="视频分析" value="video_analyzer" />
          </el-select>
        </el-form-item>
        <el-form-item label="额外配置">
          <el-input v-model="form.config" type="textarea" :rows="2" placeholder='{}' />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listAgents, createAgent, updateAgent, deleteAgent } from '../api/agents'
import { listModels } from '../api/models'

const agents = ref([])
const models = ref([])
const showDialog = ref(false)
const editing = ref(false)
const form = reactive({
  id: null,
  name: '',
  description: '',
  model_config_id: null,
  prompt_template: '',
  agent_type: 'chat',
  config: '{}'
})

async function load() {
  agents.value = await listAgents()
  models.value = await listModels()
}

function editAgent(row) {
  editing.value = true
  Object.assign(form, row)
  form.config = JSON.stringify(row.config || {})
  showDialog.value = true
}

async function handleSave() {
  try {
    const data = { ...form, config: JSON.parse(form.config) }
    if (editing.value) {
      await updateAgent(form.id, data)
      ElMessage.success('更新成功')
    } else {
      await createAgent(data)
      ElMessage.success('添加成功')
    }
    showDialog.value = false
    await load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}

async function handleDelete(id) {
  await ElMessageBox.confirm('确认删除？', '提示')
  await deleteAgent(id)
  ElMessage.success('删除成功')
  await load()
}

onMounted(load)
</script>