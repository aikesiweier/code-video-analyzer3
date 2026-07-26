import cv2
import os
import imagehash
from PIL import Image
from typing import List, Tuple

def extract_keyframes(video_path: str, output_dir: str, interval: float = 1.0, hash_threshold: int = 5) -> List[Tuple[str, float]]:
    """
    同步提取关键帧（CPU密集，建议在 run_in_executor 中调用）
    返回：[(保存路径, 时间戳秒), ...]
    """
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    frame_interval = max(1, int(fps * interval))
    keyframes = []
    prev_hash = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            current_hash = imagehash.phash(pil_img)

            if prev_hash is None or (current_hash - prev_hash) > hash_threshold:
                filename = f"frame_{frame_count:06d}.jpg"
                save_path = os.path.join(output_dir, filename)
                cv2.imwrite(save_path, frame)
                keyframes.append((save_path, timestamp))
                prev_hash = current_hash

        frame_count += 1

    cap.release()
    return keyframes