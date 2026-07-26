from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base, init_db
from app.api import users, models_config, agents, chat, history, video, report

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# 关键：禁用尾部斜杠自动重定向
app = FastAPI(title="AI Agent Platform", lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(models_config.router)
app.include_router(agents.router)
app.include_router(chat.router)
app.include_router(history.router)
app.include_router(video.router)
app.include_router(report.router)

@app.get("/")
async def root():
    return {"message": "AI Agent Platform API"}