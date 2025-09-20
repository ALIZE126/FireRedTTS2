from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import gradio as gr
from app.api import ui

app = FastAPI(
    title="Voice Clone API",
    description="API for Voice Clone",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 启动的时候初始化模型

# 1) 构建并挂载 Gradio 应用到 /voice/ui
gradio_page = ui.build_gradio_ui()
# 注意：mount_gradio_app 会返回 FastAPI 实例（同名覆盖是官方示例做法）
app = gr.mount_gradio_app(app, gradio_page, path="/voice/ui")

