from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    model_config_id = Column(Integer, ForeignKey("model_configs.id"))
    prompt_template = Column(Text, default="")
    agent_type = Column(String, default="chat")   # chat, function, video_analyzer
    config = Column(JSON, default={})
    is_active = Column(Boolean, default=True)