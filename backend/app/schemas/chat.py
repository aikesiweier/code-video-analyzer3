from pydantic import BaseModel

class ChatRequest(BaseModel):
    agent_id: int
    message: str
    stream: bool = True