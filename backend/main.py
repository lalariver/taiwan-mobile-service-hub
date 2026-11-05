
from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routers.enterprise_services import (
    router as enterprise_services_router,
)


app = FastAPI(
    title="Taiwan Mobile Service Hub API",
    description=(
        "Enterprise Service Management Platform "
        "for Taiwan Mobile portfolio project."
    ),
    version="1.0.0",
)


# ==========================================
# Database Initialization
# ==========================================

# 載入 models，確保所有 SQLAlchemy Model
# 都已註冊到 Base.metadata。
# 建立尚不存在的資料表。
Base.metadata.create_all(bind=engine)


# ==========================================
# Router Registration
# ==========================================

# 註冊企業服務 API
app.include_router(enterprise_services_router)
