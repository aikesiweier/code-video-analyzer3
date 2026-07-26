<template>
  <div class="report-page">
    <el-card v-if="report">
      <template #header>
        <span>分析报告 - 任务 #{{ report.task_id }}</span>
        <el-button style="float: right" @click="$router.push('/video')">返回</el-button>
      </template>
      <el-divider content-position="left">行为时间线</el-divider>
      <timeline-view :events="report.timeline" />

      <el-divider content-position="left">统计数据</el-divider>
      <stat-chart :statistics="report.statistics" />

      <el-divider content-position="left">AI 分析</el-divider>
      <el-alert title="总结" type="info" :description="report.llm_analysis.summary" show-icon :closable="false" />
      <el-alert title="习惯" type="success" :description="report.llm_analysis.habits" show-icon :closable="false" class="analysis-item" />
      <el-alert title="问题" type="warning" :description="report.llm_analysis.issues" show-icon :closable="false" class="analysis-item" />

      <div v-if="report.similar_cases && report.similar_cases.length">
        <el-divider content-position="left">相似案例</el-divider>
        <el-tag v-for="c in report.similar_cases" :key="c.task_id" class="case-tag">任务 #{{ c.task_id }}</el-tag>
      </div>
    </el-card>
    <el-empty v-else description="报告加载中..." />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getReport } from '../api/report'
import TimelineView from '../components/TimelineView.vue'
import StatChart from '../components/StatChart.vue'

const route = useRoute()
const report = ref(null)

onMounted(async () => {
  try {
    report.value = await getReport(route.params.id)
  } catch (e) {
    console.error('加载报告失败', e)
  }
})
</script>

<style scoped>
.report-page {
  max-width: 900px;
  margin: 20px auto;
}
.analysis-item {
  margin-top: 15px;
}
.case-tag {
  margin-right: 10px;
}
</style>