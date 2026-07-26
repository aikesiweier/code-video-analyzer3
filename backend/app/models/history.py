from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class CallHistory(Base):
    __tablename__ = "call_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    model_config_id = Column(Integer, ForeignKey("model_configs.id"), nullable=True)  # 改为可空
    input_text = Column(Text)
    output_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())