from typing import List
from .event_annotator import EventSegment

class BehaviorStats:
    def __init__(self, compile_count: int, debug_count: int, edit_segments: int,
                 pause_total_seconds: float, coding_total_seconds: float):
        self.compile_count = compile_count
        self.debug_count = debug_count
        self.edit_segments = edit_segments
        self.pause_total_seconds = pause_total_seconds
        self.coding_total_seconds = coding_total_seconds

def calculate_statistics(events: List[EventSegment]) -> BehaviorStats:
    compile_count = sum(1 for e in events if e.action == "编译")
    debug_count = sum(1 for e in events if e.action == "调试")
    edit_segments = sum(1 for e in events if e.action == "编辑代码")

    coding_total = sum((e.end_time - e.start_time) for e in events if e.action == "编辑代码")
    pause_total = sum((e.end_time - e.start_time) for e in events if e.action in ("查阅资料", "未知"))

    return BehaviorStats(
        compile_count=compile_count,
        debug_count=debug_count,
        edit_segments=edit_segments,
        pause_total_seconds=pause_total,
        coding_total_seconds=coding_total
    )