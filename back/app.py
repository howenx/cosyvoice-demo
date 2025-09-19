from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
# 导入 StaticFiles
from fastapi.staticfiles import StaticFiles # <--- 添加这一行
from pydantic import BaseModel # 如果 TTSRequest 是从 models 导入的，这一行可能不需要，但为了 BaseModel 的通用性，保留也无妨
import os
import logging
from core.cosyvoice_manager import cosyvoice_manager # 导入单例
from models import TTSRequest # <--- 确保这一行存在，如果 TTSRequest 在 models.py 中定义

# 导入 CORS 中间件
from fastapi.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# --- CORS 配置 ---
origins = [
    "http://localhost",
    "http://localhost:5173", # 你的 Vue 前端运行的地址
    "http://127.0.0.1:5173", # 如果前端使用 127.0.0.1 访问，也可能需要
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- CORS 配置结束 ---


# 在应用启动时加载模型
@app.on_event("startup")
async def startup_event():
    logging.info("Application startup event triggered. Loading CosyVoice model...")
    try:
        await cosyvoice_manager.load_model()
        logging.info("CosyVoice model loaded successfully during startup.")
    except Exception as e:
        logging.error(f"Failed to load CosyVoice model during startup: {e}")
        raise RuntimeError(f"Model loading failed: {e}")

# 挂载静态文件目录，用于提供生成的音频文件
generated_audio_dir = cosyvoice_manager.get_output_dir()
app.mount("/audio", StaticFiles(directory=generated_audio_dir), name="audio")
logging.info(f"Mounted static files for /audio from directory: {generated_audio_dir}")


# TTSRequest 应该从 models 导入，所以这里不需要再次定义
# class TTSRequest(BaseModel):
#     text: str

@app.post("/tts/generate")
async def generate_tts_audio(request: TTSRequest):
    try:
        logging.info(f"Received TTS request for text: '{request.text[:50]}...'")
        audio_filename = await cosyvoice_manager.generate_audio(request.text)
        audio_url = f"/audio/{audio_filename}" # 前端访问的URL
        logging.info(f"Audio generated: {audio_url}")
        return {"message": "Audio generated successfully", "audio_url": audio_url}
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error generating audio: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {e}")

@app.get("/")
async def root():
    return {"message": "CosyVoice TTS Backend is running!"}

