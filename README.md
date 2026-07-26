# AI Agent 平台

基于 FastAPI + Vue3 的智能体管理平台，支持多用户、大模型配置、流式对话、视频分析等。

## 快速部署（Docker）
1. 克隆项目
2. 配置环境变量（复制 .env.example 为 .env）
3. 运行 `docker-compose up -d`
4. 访问 http://localhost

## 激活环境
- `conda activate aiagent`

## 本地开发
- 后端：`cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000`
- 前端：`cd frontend && npm run dev`

## 默认管理员账号
- 用户名：admin
- 密码：admin123