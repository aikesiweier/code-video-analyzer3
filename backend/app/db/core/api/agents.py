from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.agent import Agent
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentOut, AgentUpdate
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/agents", tags=["agents"])

# 修改：去掉 "/" 改为空字符串
@router.get("", response_model=list[AgentOut])
async def list_agents(db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Agent))
    return result.scalars().all()

@router.post("", response_model=AgentOut)
async def create_agent(agent: AgentCreate, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    new_agent = Agent(**agent.model_dump())
    db.add(new_agent)
    await db.commit()
    await db.refresh(new_agent)
    return new_agent

@router.get("/{agent_id}", response_model=AgentOut)
async def get_agent(agent_id: int, db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentOut)
async def update_agent(
    agent_id: int,
    agent: AgentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_agent = await db.get(Agent, agent_id)
    if not db_agent:
        raise HTTPException(404, "Agent not found")
    update_data = agent.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_agent, key, value)
    await db.commit()
    await db.refresh(db_agent)
    return db_agent

@router.delete("/{agent_id}")
async def delete_agent(agent_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    db_agent = await db.get(Agent, agent_id)
    if not db_agent:
        raise HTTPException(404)
    await db.delete(db_agent)
    await db.commit()
    return {"ok": True}