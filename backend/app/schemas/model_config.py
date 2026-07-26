from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class ModelConfigCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    name: str
    provider: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    model_name: str
    config: Dict[str, Any] = {}

class ModelConfigUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())   # 添加此行
    name: Optional[str] = None
    provider: Optional[str] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ModelConfigOut(ModelConfigCreate):
    id: int
    is_active: bool
    model_config = ConfigDict(protected_namespaces=())