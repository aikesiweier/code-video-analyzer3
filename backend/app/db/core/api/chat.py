from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse
from app.database import get_db, AsyncSessionLocal
from app.models.agent import Agent
from app.models.model_config import ModelConfig
from app.models.user import User
from app.models.history import CallHistory
from app.core.auth import get_current_user
from app.core.llm_service import call_llm_stream
from app.core.video_agent import run_video_analysis
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/stream")
async def chat_stream(request: ChatRequest,
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    agent = await db.get(Agent, request.agent_id)
    if not agent:
        raise HTTPException(404, "Agent not found")
    model = await db.get(ModelConfig, agent.model_config_id)
    if not model:
        raise HTTPException(404, "Model config not found")

    messages = []
    if agent.prompt_template:
        messages.append({"role": "system", "content": agent.prompt_template})
    messages.append({"role": "user", "content": request.message})

    async def event_generator():
        full_output = ""
        if agent.agent_type == "video_analyzer":
            result = await run_video_analysis(request.message)
            yield {"data": result}
            full_output = result
        else:
            async for token in call_llm_stream(model, messages):
                yield {"data": token}
                full_output += token

        # 使用独立会话保存历史，避免与主会话冲突
        async with AsyncSessionLocal() as history_db:
            history = CallHistory(
                user_id=current_user.id,
                agent_id=agent.id,
                model_config_id=model.id,
                input_text=request.message,
                output_text=full_output
            )
            history_db.add(history)
            await history_db.commit()

    return EventSourceResponse(event_generator())