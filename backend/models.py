
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class EnterpriseService(Base):
    """企業服務資料模型。"""

    __tablename__ = "enterprise_services"

    # 資料庫主鍵
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # 服務代碼，例如 CONNECT-001
    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False,
    )

    # 服務名稱
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # 服務分類
    # connectivity
    # cloud_computing
    # ai_solutions
    # cybersecurity
    # carbon_energy
    # consulting_managed
    category: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )

    # 服務詳細說明
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # 是否啟用
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # 建立時間
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    # 最後更新時間
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
