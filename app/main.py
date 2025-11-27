# app/main.py
from fastapi import FastAPI, Body

app = FastAPI(title="FastAPI on Render", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running"}

# 用 POST 作為驗證端點，不依賴 health check 進行 GET 測試
@app.post("/echo")
def echo(payload: dict = Body(...)):
    # 回傳收到的資料，便於驗證序列化/反序列化與路由正常
    return {"received": payload}
