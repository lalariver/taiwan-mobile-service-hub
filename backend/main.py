from fastapi import FastAPI

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
# Router Registration
# ==========================================

# 註冊企業服務 API
app.include_router(enterprise_services_router)