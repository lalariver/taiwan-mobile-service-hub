
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)


# ==========================================
# Database Configuration
# ==========================================

# 資料庫檔案位置
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "taiwan_mobile.db"
)

# SQLite Connection URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ==========================================
# Database Engine
# ==========================================

# 建立資料庫 Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# ==========================================
# Database Session
# ==========================================

# 建立 Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ==========================================
# SQLAlchemy Base
# ==========================================

# 所有 ORM Model 的共同父類別
class Base(DeclarativeBase):
    pass


# ==========================================
# Database Dependency
# ==========================================

# 每個 HTTP Request 取得獨立的 Database Session
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
