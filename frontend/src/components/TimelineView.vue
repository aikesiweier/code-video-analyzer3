<template>
  <div class="timeline-container">
    <el-timeline>
      <el-timeline-item
        v-for="(event, idx) in events"
        :key="idx"
        :timestamp="formatTime(event.start_time) + ' - ' + formatTime(event.end_time)"
        placement="top"
        :color="getColor(event.action)"
      >
        <el-tag :type="getTagType(event.action)">{{ event.action }}</el-tag>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup>
const props = defineProps({ events: Array })

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
}

function getColor(action) {
  const map = {
    '编辑代码': '#409eff',
    '编译': '#67c23a',
    '调试': '#e6a23c',
    '运行': '#f56c6c',
    '查阅资料': '#909399',
    '未知': '#c0c4cc'
  }
  return map[action] || '#909399'
}

function getTagType(action) {
  const map = {
    '编辑代码': '',
    '编译': 'success',
    '调试': 'warning',
    '运行': 'danger',
    '查阅资料': 'info'
  }
  return map[action] || 'info'
}
</script>

<style scoped>
.timeline-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 0 10px;
}
</style>