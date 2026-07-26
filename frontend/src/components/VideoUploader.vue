<template>
  <div class="uploader">
    <el-upload
      class="upload-area"
      drag
      :auto-upload="false"
      :on-change="handleFileChange"
      :limit="1"
      accept=".mp4,.avi,.mov"
    >
      <el-icon :size="60"><upload-filled /></el-icon>
      <div class="el-upload__text">拖拽视频到此处，或 <em>点击上传</em></div>
      <template #tip>
        <div class="el-upload__tip">支持 mp4 / avi / mov</div>
      </template>
    </el-upload>
    <el-button
      type="primary"
      :disabled="!selectedFile || uploading"
      :loading="uploading"
      @click="submitUpload"
      style="margin-top: 20px; width: 100%"
    >
      {{ uploading ? '上传中...' : '开始分析' }}
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadVideo } from '../api/video'

const emit = defineEmits(['uploadSuccess'])
const selectedFile = ref(null)
const uploading = ref(false)

function handleFileChange(file) {
  selectedFile.value = file.raw
}

async function submitUpload() {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    const { task_id } = await uploadVideo(selectedFile.value)
    ElMessage.success('上传成功，正在分析...')
    emit('uploadSuccess', task_id)
  } catch (e) {
    ElMessage.error('上传失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.upload-area {
  width: 100%;
}
</style>