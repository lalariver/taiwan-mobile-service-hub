
from unittest.mock import Mock

import pytest

from backend import database


def test_get_db_closes_session(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """確認 get_db 執行結束後會關閉 Session。"""

    mock_session = Mock()

    monkeypatch.setattr(
        database,
        "SessionLocal",
        lambda: mock_session,
    )

    db_generator = database.get_db()

    # 執行 yield，取得 Database Session。
    db = next(db_generator)

    assert db is mock_session

    # 讓 Generator 執行到結束，觸發 finally。
    with pytest.raises(StopIteration):
        next(db_generator)

    mock_session.close.assert_called_once_with()
