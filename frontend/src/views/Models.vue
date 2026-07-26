<template>
  <div>
    <el-button type="primary" @click="showDialog = true">添加模型</el-button>
    <el-table :data="models" style="margin-top: 20px">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="provider" label="提供商" />
      <el-table-column prop="model_name" label="模型名" />
      <el-table-column prop="is_active" label="启用">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button size="small" @click="editModel(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editing ? '编辑模型' : '添加模型'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="提供商">
          <el-input v-model="form.provider" />
        </el-form-item>
        <el-form-item label="API Base">
          <el-input v-model="form.api_base" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="form.api_key" type="password" />
        </el-form-item>
        <el-form-item label="模型名">
          <el-input v-model="form.model_name" />
        </el-form-item>
        <el-form-item label="额外配置">
          <el-input v-model="form.config" type="textarea" :rows="3" placeholder='{"temperature":0.7}' />
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
import { listModels, createModel, updateModel, deleteModel } from '../api/models'

const models = ref([])
const showDialog = ref(false)
const editing = ref(false)
const form = reactive({
  id: null,
  name: '',
  provider: '',
  api_base: '',
  api_key: '',
  model_name: '',
  config: '{}'
})

async function load() {
  models.value = await listModels()
}

function editModel(row) {
  editing.value = true
  Object.assign(form, row)
  form.config = JSON.stringify(row.config || {})
  showDialog.value = true
}

async function handleSave() {
  try {
    const data = { ...form, config: JSON.parse(form.config) }
    if (editing.value) {
      await updateModel(form.id, data)
      ElMessage.success('更新成功')
    } else {
      await createModel(data)
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
  await deleteModel(id)
  ElMessage.success('删除成功')
  await load()
}

onMounted(load)
</script>