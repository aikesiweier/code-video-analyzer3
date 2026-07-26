from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class HistoryOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    id: int
    user_id: int
    agent_id: Optional[int]
    model_config_id: Optional[int] = None
    input_text: str
    output_text: str
    created_at: datetime