import asyncio
from app.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.model_config import ModelConfig
from app.models.agent import Agent
from app.core.auth import get_password_hash

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 创建管理员
        admin = await session.get(User, 1)
        if not admin:
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                email="admin@example.com"
            )
            session.add(admin)

        # 默认模型配置（使用 qwen，需自行填入 API Key）
        default_model = ModelConfig(
            name="qwen-max",
            provider="qwen",
            api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="your-api-key",   # 请替换
            model_name="qwen-max"
        )
        session.add(default_model)

        # 默认聊天智能体
        agent = Agent(
            name="通用助手",
            description="默认AI对话助手",
            model_config_id=1,
            prompt_template="你是一个有用的助手。",
            agent_type="chat"
        )
        session.add(agent)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(init())