
from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="FastAPI on Codespaces + Render")

class EchoIn(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {
        "app": "fastapi-demo",
        "version": "v1",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/echo")
def echo(payload: EchoIn = Body(...)):
    return {"echo": payload.message}
