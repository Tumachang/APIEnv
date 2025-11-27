import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# Render 的 Internal URL 是 "postgresql://..."，async 用 asyncpg 需轉前綴
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Please set it in Render environment variables.")
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    # 若你不小心貼了別的前綴，直接用使用者提供字串
    ASYNC_DATABASE_URL = DATABASE_URL

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # 若要除錯可以改 True
    pool_pre_ping=True,  # 避免連線閒置斷線
)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
