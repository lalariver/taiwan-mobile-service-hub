
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request

from collections.abc import Generator
from pathlib import Path

import pytest


# ==========================================
# Configuration
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"


# ==========================================
# Server Readiness
# ==========================================

def wait_for_server(
    url: str,
    process: subprocess.Popen,
    log_path: Path,
    timeout: int = 30,
) -> None:
    """等待伺服器啟動，或在啟動失敗時回報 Log。"""

    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:

        if process.poll() is not None:
            raise RuntimeError(
                f"Server exited unexpectedly.\n"
                f"Log:\n{log_path.read_text(encoding='utf-8')}"
            )

        try:
            with urllib.request.urlopen(
                url,
                timeout=1,
            ):
                return

        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ):
            time.sleep(0.25)

    raise TimeoutError(
        f"Server did not become ready: {url}\n"
        f"Log:\n{log_path.read_text(encoding='utf-8')}"
    )


# ==========================================
# E2E Environment
# ==========================================

@pytest.fixture(scope="session")
def e2e_environment(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[dict[str, str], None, None]:
    """建立獨立 E2E Database 並自動啟動前後端。"""

    temp_dir = tmp_path_factory.mktemp("e2e")

    database_path = temp_dir / "e2e.db"

    # E2E Backend 使用獨立資料庫。
    backend_env = os.environ.copy()
    backend_env["DATABASE_PATH"] = str(database_path)

    backend_log_path = temp_dir / "backend.log"
    frontend_log_path = temp_dir / "frontend.log"

    backend_process = None
    frontend_process = None

    with (
        backend_log_path.open("w", encoding="utf-8") as backend_log,
        frontend_log_path.open("w", encoding="utf-8") as frontend_log,
    ):

        try:
            # ==========================================
            # Initialize E2E Database
            # ==========================================

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "backend.init_db",
                ],
                cwd=PROJECT_ROOT,
                env=backend_env,
                check=True,
                capture_output=True,
                text=True,
            )

            # ==========================================
            # Start FastAPI
            # ==========================================

            backend_process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "backend.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8000",
                    "--log-level",
                    "warning",
                ],
                cwd=PROJECT_ROOT,
                env=backend_env,
                stdout=backend_log,
                stderr=subprocess.STDOUT,
            )

            wait_for_server(
                f"{BACKEND_URL}/openapi.json",
                backend_process,
                backend_log_path,
            )

            # ==========================================
            # Start React / Vite
            # ==========================================

            frontend_process = subprocess.Popen(
                [
                    "npm",
                    "run",
                    "dev",
                    "--",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "5173",
                    "--strictPort",
                ],
                cwd=PROJECT_ROOT / "frontend",
                env=os.environ.copy(),
                stdout=frontend_log,
                stderr=subprocess.STDOUT,
            )

            wait_for_server(
                FRONTEND_URL,
                frontend_process,
                frontend_log_path,
            )

            yield {
                "base_url": FRONTEND_URL,
                "database_path": str(database_path),
            }

        finally:
            # ==========================================
            # Stop Servers
            # ==========================================

            for process in (
                frontend_process,
                backend_process,
            ):

                if process is None:
                    continue

                if process.poll() is None:
                    process.terminate()

                try:
                    process.wait(timeout=10)

                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


# ==========================================
# Test Data Isolation
# ==========================================

@pytest.fixture(autouse=True)
def reset_e2e_database(
    e2e_environment: dict[str, str],
) -> None:
    """每個 UI Test 開始前清空 E2E Database。"""

    connection = sqlite3.connect(
        e2e_environment["database_path"],
        timeout=10,
    )

    try:
        connection.execute(
            "DELETE FROM enterprise_services",
        )

        connection.commit()

    finally:
        connection.close()
