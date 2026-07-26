from sqlalchemy import Column, Integer, String, JSON, Boolean
from app.database import Base

class ModelConfig(Base):
    __tablename__ = "model_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    provider = Column(String, nullable=False)   # openai, qwen, deepseek
    api_base = Column(String, nullable=True)
    api_key = Column(String, nullable=True)
    model_name = Column(String, nullable=False)
    config = Column(JSON, default={})
    is_active = Column(Boolean, default=True)