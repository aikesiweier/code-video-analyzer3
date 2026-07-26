<template>
  <div>
    <div ref="chartDom" style="width: 100%; height: 400px;"></div>
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="4" v-for="item in statItems" :key="item.label">
        <el-card shadow="hover">
          <div class="stat-value">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({ statistics: Object })

const chartDom = ref(null)
let chart = null

const statItems = computed(() => [
  { label: '编译次数', value: props.statistics.compile_count },
  { label: '调试次数', value: props.statistics.debug_count },
  { label: '编辑段落', value: props.statistics.edit_segments },
  { label: '编码时长(s)', value: props.statistics.coding_total_seconds?.toFixed(1) },
  { label: '停顿时长(s)', value: props.statistics.pause_total_seconds?.toFixed(1) }
])

function renderChart() {
  if (!chartDom.value) return
  if (chart) chart.dispose()
  chart = echarts.init(chartDom.value)

  const { compile_count, debug_count, edit_segments, coding_total_seconds, pause_total_seconds } = props.statistics
  const option = {
    radar: {
      indicator: [
        { name: '编译', max: Math.max(compile_count * 1.5, 10) },
        { name: '调试', max: Math.max(debug_count * 1.5, 10) },
        { name: '编辑段', max: Math.max(edit_segments * 1.5, 10) },
        { name: '编码时长', max: Math.max(coding_total_seconds * 1.5, 100) },
        { name: '停顿时长', max: Math.max(pause_total_seconds * 1.5, 100) }
      ],
      shape: 'circle'
    },
    series: [{
      type: 'radar',
      data: [{
        value: [compile_count, debug_count, edit_segments, coding_total_seconds, pause_total_seconds],
        name: '当前行为',
        areaStyle: { color: 'rgba(64,158,255,0.2)' }
      }]
    }]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart?.resize())
}

watch(() => props.statistics, renderChart, { deep: true })
onMounted(renderChart)
</script>

<style scoped>
.stats-cards {
  margin-top: 20px;
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  font-size: 14px;
  color: #909399;
}
</style>