from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, get_session
from .models import Base, User
from .schemas import RegisterRequest, LoginRequest, TokenResponse, UserOut
from . import auth

# === 將你的靜態網站網域填入（Render 的 Static Site 網域） ===
ALLOWED_ORIGINS = [
    "https://frontend-rjzs.onrender.com",  # TODO: 換成你的靜態站網址
]

app = FastAPI(title="FastAPI Auth Service")

# CORS：只允許你的前端來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=True)

@app.on_event("startup")
async def on_startup():
    # 建表（生產環境可改用 Alembic 做 migration）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Auth service is up"}

# （可選）健康檢查；若你不需要可刪除
#@app.get("/health")
#def health():
#   return {"status": "ok"}

@app.post("/register", response_model=UserOut, status_code=201)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # 檢查是否已存在
    result = await session.execute(select(User).where(User.email == payload.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=auth.hash_password(payload.password),
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserOut(id=user.id, email=user.email, is_active=user.is_active)

@app.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(sub=user.email)
    return TokenResponse(access_token=token)

# 取得當前使用者
@app.get("/me", response_model=UserOut)
async def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials
    try:
        payload = auth.decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut(id=user.id, email=user.email, is_active=user.is_active)
