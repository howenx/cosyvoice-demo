import uvicorn # <--- 添加这一行
import os
import sys

# 将当前目录添加到 sys.path，以便 uvicorn 找到 app 模块
# 假设 main.py 和 app.py 在同一目录
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    # uvicorn 会自动查找 app.py 中的 app 实例
    # 注意：这里明确指定了端口是 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
