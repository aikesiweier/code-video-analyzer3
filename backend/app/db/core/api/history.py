from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.history import CallHistory
from app.models.user import User
from app.schemas.history import HistoryOut
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("", response_model=list[HistoryOut])
async def get_history(db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(CallHistory)
        .where(CallHistory.user_id == current_user.id)
        .order_by(CallHistory.created_at.desc())
        .limit(100)
    )
    return result.scalars().all()