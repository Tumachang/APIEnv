
# Dockerfile
FROM python:3.12-slim

# 系統必要套件（編譯/運行需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 建置非 root 使用者
RUN useradd -m appuser
WORKDIR /home/appuser/app

# 複製需求與程式
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# 權限設定
RUN chown -R appuser:appuser /home/appuser
USER appuser

# 服務埠
EXPOSE 8000

# 預設啟動（開發用的 --reload）
# Render 可覆寫成無 --reload 的命令（Production）
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
