from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TimelineEvent(BaseModel):
    start_time: float
    end_time: float
    action: str

class Statistics(BaseModel):
    compile_count: int
    debug_count: int
    edit_segments: int
    pause_total_seconds: float
    coding_total_seconds: float

class LLMAnalysis(BaseModel):
    summary: str
    habits: str
    issues: str

class ReportResponse(BaseModel):
    task_id: int
    timeline: List[TimelineEvent]
    statistics: Statistics
    llm_analysis: LLMAnalysis
    similar_cases: Optional[List[Dict[str, Any]]] = None