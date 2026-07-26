from typing import List, Dict
from pydantic import BaseModel

class EventSegment(BaseModel):
    start_time: float
    end_time: float
    action: str

def merge_events(raw_predictions: List[Dict]) -> List[EventSegment]:
    """
    将逐帧行为标签合并为连续事件段。
    输入: [{"time": 1.0, "action": "编辑代码"}, ...]
    输出: [EventSegment(start_time, end_time, action), ...]
    """
    if not raw_predictions:
        return []

    segments = []
    current_action = raw_predictions[0]["action"]
    start_time = raw_predictions[0]["time"]

    for i in range(1, len(raw_predictions)):
        item = raw_predictions[i]
        if item["action"] != current_action:
            segments.append(EventSegment(
                start_time=start_time,
                end_time=raw_predictions[i-1]["time"],
                action=current_action
            ))
            current_action = item["action"]
            start_time = item["time"]

    segments.append(EventSegment(
        start_time=start_time,
        end_time=raw_predictions[-1]["time"],
        action=current_action
    ))

    return segments