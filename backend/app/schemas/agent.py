from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class AgentCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    name: str
    description: Optional[str] = None
    model_config_id: int
    prompt_template: Optional[str] = ""
    agent_type: str = "chat"
    config: Dict[str, Any] = {}

class AgentUpdate(BaseModel):              # 用于部分更新，所有字段可选
    model_config = ConfigDict(protected_namespaces=())
    name: Optional[str] = None
    description: Optional[str] = None
    model_config_id: Optional[int] = None
    prompt_template: Optional[str] = None
    agent_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class AgentOut(AgentCreate):
    id: int
    is_active: bool
    model_config = ConfigDict(protected_namespaces=())