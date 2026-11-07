
import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from backend.models import EnterpriseService
from backend.repositories import enterprise_service_repository
from backend.services.enterprise_service import (
    _commit_transaction,
    validate_service_code,
)


def test_unique_constraint_rolls_back_all_pending_changes(
    test_session_factory: sessionmaker[Session],
) -> None:
    """測試資料庫唯一性衝突時，整個 Transaction 都會 Rollback。"""

    duplicate_code = "QA-RACE-001"

    # ==========================================
    # 建立兩個獨立 Database Sessions
    # ==========================================

    with (
        test_session_factory() as session_a,
        test_session_factory() as session_b,
    ):

        # ==========================================
        # Step 1：兩個 Session 都先檢查 Code
        # ==========================================

        validate_service_code(
            session_a,
            duplicate_code,
        )

        validate_service_code(
            session_b,
            duplicate_code,
        )

        # 此時資料庫都還沒有這個 Code。
        # 因此兩個 Session 都通過事前檢查。

        # ==========================================
        # Step 2：Session A 新增資料
        # ==========================================

        enterprise_service_repository.create_enterprise_service(
            session_a,
            code=duplicate_code,
            name="Created by Request A",
            category="connectivity",
            description="Created by session A.",
            is_active=True,
        )

        # ==========================================
        # Step 3：Session B 新增兩筆資料
        # ==========================================

        # 第一筆是合法資料
        enterprise_service_repository.create_enterprise_service(
            session_b,
            code="QA-RACE-002",
            name="Pending Valid Service",
            category="connectivity",
            description="This record should be rolled back.",
            is_active=True,
        )

        # 第二筆與 Session A 重複
        enterprise_service_repository.create_enterprise_service(
            session_b,
            code=duplicate_code,
            name="Duplicate Service",
            category="connectivity",
            description="This record violates unique constraint.",
            is_active=True,
        )

        # ==========================================
        # Step 4：Session A 先 Commit
        # ==========================================

        _commit_transaction(session_a)

        # ==========================================
        # Step 5：Session B Commit 時應發生 IntegrityError
        # ==========================================

        with pytest.raises(HTTPException) as exc_info:
            _commit_transaction(session_b)

        assert exc_info.value.status_code == 409

        assert (
            exc_info.value.detail
            == "Enterprise service code already exists"
        )

        # Rollback 後，Session B 不應仍處於交易中。
        assert session_b.in_transaction() is False

    # ==========================================
    # Step 6：使用新的 Session 驗證資料庫結果
    # ==========================================

    with test_session_factory() as verify_session:

        statement = (
            select(EnterpriseService)
            .order_by(EnterpriseService.id)
        )

        records = verify_session.scalars(statement).all()

        # 只能留下 Session A 已成功提交的資料。
        assert len(records) == 1

        assert records[0].code == duplicate_code
        assert records[0].name == "Created by Request A"

        # Session B 的合法資料也必須一起 Rollback。
        assert all(
            record.code != "QA-RACE-002"
            for record in records
        )
