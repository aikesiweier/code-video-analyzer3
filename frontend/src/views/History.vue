<template>
  <div>
    <el-table :data="history" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="input_text" label="输入" min-width="150" />
      <el-table-column prop="output_text" label="输出" min-width="200" />
      <el-table-column prop="created_at" label="时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHistory } from '../api/history'

const history = ref([])

onMounted(async () => {
  try {
    history.value = await getHistory()
  } catch (e) {
    console.error('加载历史失败', e)
  }
})
</script>