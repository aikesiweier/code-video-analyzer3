from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token, UserUpdate   # 新增 UserUpdate
from app.core.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api", tags=["users"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    exist = await db.execute(select(User).where(User.username == user.username))
    if exist.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_me(
    update: UserUpdate,                      # 使用新模型
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 只更新传入的非 None 字段
    if update.username is not None:
        # 检查用户名是否被占用
        exist = await db.execute(select(User).where(User.username == update.username))
        if exist.scalar_one_or_none():
            raise HTTPException(400, "用户名已被使用")
        current_user.username = update.username
    if update.email is not None:
        current_user.email = update.email
    if update.password is not None:
        current_user.hashed_password = get_password_hash(update.password)
    await db.commit()
    await db.refresh(current_user)
    return current_user