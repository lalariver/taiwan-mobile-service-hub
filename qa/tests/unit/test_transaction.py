
from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from backend.services.enterprise_service import (
    _commit_transaction,
)


def test_commit_transaction_rolls_back_on_duplicate_code(
) -> None:
    """資料庫發生服務代碼唯一性衝突時，應回傳 409。"""

    db = Mock()

    db.commit.side_effect = IntegrityError(
        "INSERT INTO enterprise_services",
        {},
        Exception(
            "UNIQUE constraint failed: enterprise_services.code",
        ),
    )

    with pytest.raises(HTTPException) as exc_info:
        _commit_transaction(db)

    assert exc_info.value.status_code == 409

    db.commit.assert_called_once()
    db.rollback.assert_called_once()


def test_commit_transaction_rolls_back_on_other_integrity_error(
) -> None:
    """其他 IntegrityError 應回滾並繼續拋出原始錯誤。"""

    db = Mock()

    db.commit.side_effect = IntegrityError(
        "INSERT INTO enterprise_services",
        {},
        Exception(
            "NOT NULL constraint failed: enterprise_services.name",
        ),
    )

    with pytest.raises(IntegrityError):
        _commit_transaction(db)

    db.commit.assert_called_once()
    db.rollback.assert_called_once()


def test_commit_transaction_rolls_back_on_unexpected_error(
) -> None:
    """發生其他錯誤時，也必須執行 Rollback。"""

    db = Mock()

    db.commit.side_effect = RuntimeError(
        "Database connection failed",
    )

    with pytest.raises(RuntimeError):
        _commit_transaction(db)

    db.commit.assert_called_once()
    db.rollback.assert_called_once()
