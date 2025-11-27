import os
import time
import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")  # 請在 Render 設定環境變數

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_access_token(sub: str, expires_minutes: int = 60 * 24) -> str:
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + expires_minutes * 60}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
