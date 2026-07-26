import os
import json
from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.db.chroma_client import collection
from .stats_calculator import BehaviorStats
from .event_annotator import EventSegment
from app.schemas.report import LLMAnalysis

llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
)

async def generate_report(task_id: int, events: List[EventSegment], stats: BehaviorStats) -> dict:
    # 1. 向量检索相似案例
    try:
        current_vector = [
            float(stats.compile_count),
            float(stats.debug_count),
            float(stats.edit_segments),
            stats.pause_total_seconds,
            stats.coding_total_seconds,
        ]
        results = collection.query(
            query_embeddings=[current_vector],
            n_results=3,
            include=["metadatas"]
        )
        similar_cases = [item["task_id"] for item in results["metadatas"][0]] if results["ids"] else []
    except Exception:
        similar_cases = []

    # 2. 构建 Prompt
    timeline_summary = "\n".join(
        [f"{e.start_time:.0f}s - {e.end_time:.0f}s: {e.action}" for e in events[:30]]
    )
    stats_desc = (
        f"编译次数: {stats.compile_count}\n"
        f"调试次数: {stats.debug_count}\n"
        f"编辑段落数: {stats.edit_segments}\n"
        f"停顿总时长(查阅/静止): {stats.pause_total_seconds:.1f}s\n"
        f"编码总时长: {stats.coding_total_seconds:.1f}s"
    )

    system_prompt = (
        "你是一名资深软件开发教练，擅长分析程序员的编码行为。"
        "请根据提供的行为时间线和统计数据，生成一份分析报告，包含三个部分：\n"
        "1. 编码过程总结 (summary)\n"
        "2. 编程习惯分析 (habits)\n"
        "3. 常见问题诊断 (issues)\n"
        "以JSON格式返回：{\"summary\": \"...\", \"habits\": \"...\", \"issues\": \"...\"}"
    )

    human_prompt = (
        f"本次编程任务的行为时间线摘要：\n{timeline_summary}\n\n"
        f"统计数据：\n{stats_desc}\n\n"
        f"相似历史任务ID（参考）：{similar_cases}\n"
        "请进行分析。"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    # 3. 调用 LLM
    llm_response = await llm.ainvoke(messages)
    try:
        analysis_json = json.loads(llm_response.content)
        llm_analysis = LLMAnalysis(**analysis_json)
    except Exception:
        llm_analysis = LLMAnalysis(
            summary="分析生成失败",
            habits="无法解析",
            issues="请重试"
        )

    # 4. 构建报告
    report = {
        "task_id": task_id,
        "timeline": [t.dict() for t in events],
        "statistics": {
            "compile_count": stats.compile_count,
            "debug_count": stats.debug_count,
            "edit_segments": stats.edit_segments,
            "pause_total_seconds": stats.pause_total_seconds,
            "coding_total_seconds": stats.coding_total_seconds,
        },
        "llm_analysis": llm_analysis.dict(),
        "similar_cases": [{"task_id": cid} for cid in similar_cases]
    }
    return report