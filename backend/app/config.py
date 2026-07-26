import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取，若未设置则给出警告
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    import warnings
    warnings.warn("SECRET_KEY not set in environment, using insecure default! DO NOT use in production.")
    SECRET_KEY = "change-me-in-production"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/app.db")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")