import os
import shutil
import asyncio
import json
import aiofiles
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, AsyncSessionLocal
from app.models.task import Task
from app.models.history import CallHistory  # 新增导入
from app.schemas.task import TaskCreateResponse, TaskStatusResponse
from app.core.video_processor import extract_keyframes
from app.core.behavior_recognizer import recognize_actions
from app.core.event_annotator import merge_events
from app.core.stats_calculator import calculate_statistics
from app.core.vectorizer import store_behavior_vector
from app.core.report_generator import generate_report
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/video", tags=["video"])

UPLOAD_DIR = "./data/videos"
FRAMES_DIR = "./data/frames"

async def process_video_task(task_id: int, video_path: str):
    async with AsyncSessionLocal() as db:
        try:
            task = await db.get(Task, task_id)
            if not task:
                return
            task.status = "processing"
            task.progress = 10
            await db.commit()

            loop = asyncio.get_running_loop()
            task.progress = 20
            await db.commit()
            frame_dir = os.path.join(FRAMES_DIR, str(task_id))
            keyframes = await loop.run_in_executor(
                None, extract_keyframes, video_path, frame_dir, 1.0
            )

            task.progress = 40
            await db.commit()
            predictions = await recognize_actions(keyframes)

            task.progress = 60
            await db.commit()
            events = merge_events(predictions)

            stats = calculate_statistics(events)
            task.progress = 80
            await db.commit()

            store_behavior_vector(task_id, stats)

            task.progress = 90
            await db.commit()
            report_dict = await generate_report(task_id, events, stats)

            task.report_json = json.dumps(report_dict, ensure_ascii=False)
            task.status = "completed"
            task.progress = 100
            await db.commit()

            # ---------- 新增：插入历史记录 ----------
            if report_dict and "llm_analysis" in report_dict:
                summary = report_dict["llm_analysis"].get("summary", "分析完成")
            else:
                summary = "视频分析完成"
            history = CallHistory(
                user_id=task.user_id,
                agent_id=None,           # 无需关联智能体
                model_config_id=None,    # 无需关联模型配置（已改为可空）
                input_text=f"视频分析: {task.filename}",
                output_text=summary,
            )
            db.add(history)
            await db.commit()
            # --------------------------------------

        except Exception as e:
            task.status = "failed"
            task.report_json = json.dumps({"error": str(e)})
            await db.commit()

# 以下路由部分保持不变
@router.post("/upload", response_model=TaskCreateResponse)
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_ext = (".mp4", ".avi", ".mov")
    if not file.filename.lower().endswith(allowed_ext):
        raise HTTPException(400, "仅支持 mp4/avi/mov 格式")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_name = f"{int(asyncio.get_event_loop().time())}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, save_name)
    async with aiofiles.open(save_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    task = Task(filename=file.filename, status="pending", progress=0, user_id=current_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    background_tasks.add_task(process_video_task, task.id, save_path)

    return TaskCreateResponse(task_id=task.id, status="pending")

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    if task.user_id != current_user.id:
        raise HTTPException(403, "无权查看此任务")
    return task