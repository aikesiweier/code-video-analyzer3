from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(Float)
    end_time = Column(Float)
    action = Column(String)