
import os

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

# 預設正式／開發資料庫位置
DEFAULT_DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "taiwan_mobile.db"
)

# 支援透過環境變數指定資料庫位置
DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(DEFAULT_DATABASE_PATH),
    )
).expanduser().resolve()

# SQLite Connection URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ==========================================
# Database Engine
# ==========================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# ==========================================
# Database Session
# ==========================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ==========================================
# SQLAlchemy Base
# ==========================================

class Base(DeclarativeBase):
    pass


# ==========================================
# Database Dependency
# ==========================================

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
