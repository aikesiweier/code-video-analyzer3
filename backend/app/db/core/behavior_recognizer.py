import base64
import json
import os
from typing import List, Tuple, Dict
from openai import AsyncOpenAI
from PIL import Image
import io

# 使用阿里云 DashScope 兼容 OpenAI 接口
client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

MODEL_NAME = "qwen-vl-max"

def pil_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

async def recognize_actions(frame_data: List[Tuple[str, float]], batch_size: int = 5) -> List[Dict]:
    """
    将关键帧分批发送给 Qwen-VL 多模态 API，识别行为标签。
    返回: [{"time": float, "action": str}, ...]
    """
    all_results = []

    for i in range(0, len(frame_data), batch_size):
        batch = frame_data[i:i+batch_size]
        content = []
        for path, ts in batch:
            img = Image.open(path)
            b64_img = pil_to_base64(img)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64_img}"
                }
            })
            content.append({
                "type": "text",
                "text": f"帧时间戳: {ts:.2f}秒"
            })

        content.append({
            "type": "text",
            "text": (
                "请识别以上每一帧中程序员的行为，从以下标签中选择最合适的一个："
                "编辑代码、编译、调试、运行、查阅资料。"
                "返回一个JSON数组，每个元素包含 'time'(帧时间戳) 和 'action'(行为标签)。"
                "确保严格按照时间戳对应。"
            )
        })

        messages = [
            {"role": "user", "content": content}
        ]

        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=1024,
                temperature=0.1
            )
            reply = response.choices[0].message.content

            # 解析回复中的 JSON
            json_str = reply
            if "```json" in reply:
                json_str = reply.split("```json")[1].split("```")[0].strip()
            elif "```" in reply:
                json_str = reply.split("```")[1].split("```")[0].strip()

            batch_results = json.loads(json_str)
            if isinstance(batch_results, list):
                all_results.extend(batch_results)
        except Exception as e:
            print(f"行为识别出错 (batch {i}): {e}")
            for _, ts in batch:
                all_results.append({"time": ts, "action": "未知"})

    all_results.sort(key=lambda x: x["time"])
    return all_results