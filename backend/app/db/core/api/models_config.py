from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.model_config import ModelConfig
from app.schemas.model_config import ModelConfigCreate, ModelConfigOut, ModelConfigUpdate
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/models", tags=["models"])

@router.get("", response_model=list[ModelConfigOut])
async def list_models(db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    result = await db.execute(select(ModelConfig))
    return result.scalars().all()

@router.post("", response_model=ModelConfigOut)
async def create_model(model: ModelConfigCreate, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    new_model = ModelConfig(**model.model_dump())
    db.add(new_model)
    await db.commit()
    await db.refresh(new_model)
    return new_model

@router.put("/{model_id}", response_model=ModelConfigOut)
async def update_model(
    model_id: int,
    model: ModelConfigUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_model = await db.get(ModelConfig, model_id)
    if not db_model:
        raise HTTPException(404, "Model not found")
    update_data = model.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_model, key, value)
    await db.commit()
    await db.refresh(db_model)
    return db_model

@router.delete("/{model_id}")
async def delete_model(model_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_model = await db.get(ModelConfig, model_id)
    if not db_model:
        raise HTTPException(404)
    await db.delete(db_model)
    await db.commit()
    return {"ok": True}