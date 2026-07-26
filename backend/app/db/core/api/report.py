import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.task import Task
from app.schemas.report import ReportResponse
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/report", tags=["report"])

@router.get("/{task_id}", response_model=ReportResponse)
async def get_report(task_id: int, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    if task.status != "completed":
        raise HTTPException(400, "任务未完成或已失败")
    if not task.report_json:
        raise HTTPException(404, "报告尚未生成")

    report_data = json.loads(task.report_json)
    return report_data