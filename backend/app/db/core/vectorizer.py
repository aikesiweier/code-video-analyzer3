from app.db.chroma_client import collection
from .stats_calculator import BehaviorStats

def stats_to_vector(stats: BehaviorStats):
    return [
        float(stats.compile_count),
        float(stats.debug_count),
        float(stats.edit_segments),
        stats.pause_total_seconds,
        stats.coding_total_seconds,
    ]

def store_behavior_vector(task_id: int, stats: BehaviorStats):
    vector = stats_to_vector(stats)
    collection.add(
        embeddings=[vector],
        metadatas=[{"task_id": task_id}],
        ids=[f"task_{task_id}"]
    )