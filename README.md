# CosyVoice Web Demo

这是一个基于 CosyVoice 2.0 的实时文本转语音 (TTS) Web 演示项目。它提供了一个用户友好的界面，允许用户输入文本、选择提示音，并实时生成高质量的语音。该项目采用前后端分离架构，后端负责与 CosyVoice 模型交互并处理语音生成逻辑，前端提供交互式用户界面。

## 项目结构

.
├── back/ # 后端服务目录
│ ├── core/
│ │ └── cosyvoice_manager.py # CosyVoice 模型管理和 TTS 核心逻辑
│ ├── main.py # 后端 API 入口
│ ├── requirements.txt # 后端 Python 依赖
│ └── .gitignore # 后端 Git 忽略文件
├── front/ # 前端应用目录
│ ├── public/
│ ├── src/
│ │ └── App.js # 前端主组件 (示例)
│ ├── package.json # 前端 Node.js 依赖
│ └── .gitignore # 前端 Git 忽略文件
├── pretrained_models/ # 存放 CosyVoice 模型权重
│ └── CosyVoice2-0.5B/ # 模型文件
├── asset/ # 存放默认提示音等资源
│ └── zero_44100.wav # 默认提示音文件
└── README.md # 项目说明文件

## 后端 (Back-end) 介绍

后端服务使用 Python 构建，核心功能是管理 CosyVoice 2.0 模型并提供文本转语音的 API 接口。

- **核心文件**: `back/core/cosyvoice_manager.py`
  - 负责加载 CosyVoice 2.0 模型 (`CosyVoice2-0.5B`)。
  - 处理提示音的加载和重采样（目前配置为 24000 Hz）。
  - 提供 `generate_audio` 方法，通过 `inference_zero_shot` 调用 CosyVoice 模型生成语音。
  - 将生成的语音保存为 WAV 文件。
  - 采用单例模式确保模型只加载一次。
- **技术栈**: Python, CosyVoice 库, PyTorch, torchaudio, numpy, uuid, logging, FastAPI, Uvicorn。
- **API 接口**: 通过 FastAPI 框架暴露一个 POST 接口 `/generate_audio/`，接收文本，返回生成的音频文件。

## 前端 (Front-end) 介绍

前端应用提供用户界面，用于与后端服务交互，实现文本输入、提示音选择、语音生成和播放。

- **核心功能**:
  - 文本输入框，供用户输入待合成的文本。
  - 触发语音生成的按钮。
  - 播放生成语音的音频播放器。
  - 显示生成状态或错误信息。
- **技术栈**: HTML, CSS, JavaScript (推荐使用现代框架如 React, Vue 或 Angular)。

## 致谢

CosyVoice 项目 提供了强大的 TTS 模型。
