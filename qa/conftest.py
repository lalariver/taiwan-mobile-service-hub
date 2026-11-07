
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend import models  # noqa: F401
from backend.database import Base, get_db
from backend.main import app


# ==========================================
# Test Database
# ==========================================

@pytest.fixture
def test_engine(tmp_path: Path) -> Generator[Engine, None, None]:
    """建立每個測試專用的暫存 SQLite Database。"""

    database_url = URL.create(
        drivername="sqlite",
        database=str(tmp_path / "test.db"),
    )

    engine = create_engine(
        database_url,
        connect_args={
            "check_same_thread": False,
        },
    )

    Base.metadata.create_all(bind=engine)

    try:
        yield engine

    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


# ==========================================
# Test Session Factory
# ==========================================

@pytest.fixture
def test_session_factory(
    test_engine: Engine,
) -> sessionmaker[Session]:
    """建立測試環境專用的 Session Factory。"""

    return sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )


# ==========================================
# Database Session Fixture
# ==========================================

@pytest.fixture
def db_session(
    test_session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """提供測試程式直接操作資料庫的 Session。"""

    db = test_session_factory()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# FastAPI TestClient Fixture
# ==========================================

@pytest.fixture
def client(
    test_session_factory: sessionmaker[Session],
) -> Generator[TestClient, None, None]:
    """建立使用測試資料庫的 FastAPI TestClient。"""

    def override_get_db() -> Generator[Session, None, None]:
        db = test_session_factory()

        try:
            yield db

        finally:
            db.close()

    # 將正式 Database Dependency 替換成測試版本。
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # 移除本次測試的 Dependency Override。
        app.dependency_overrides.pop(get_db, None)


# ==========================================
# Test Data
# ==========================================

@pytest.fixture
def service_payload() -> dict[str, object]:
    """提供新增企業服務的預設測試資料。"""

    return {
        "code": "QA-TEST-001",
        "name": "QA Test Service",
        "category": "connectivity",
        "description": "Test service for automation testing.",
        "is_active": True,
    }
