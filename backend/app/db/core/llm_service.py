import json
import httpx
from typing import AsyncGenerator
from app.models.model_config import ModelConfig

async def call_llm_stream(model: ModelConfig, messages: list, **kwargs) -> AsyncGenerator[str, None]:
    """通用流式调用大模型，返回 token 生成器"""
    headers = {"Authorization": f"Bearer {model.api_key}", "Content-Type": "application/json"}
    url = f"{model.api_base}/chat/completions"
    payload = {
        "model": model.model_name,
        "messages": messages,
        "stream": True,
        **model.config,
        **kwargs
    }
    async with httpx.AsyncClient(timeout=300) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"]
                        if "content" in delta:
                            yield delta["content"]
                    except Exception:
                        continue