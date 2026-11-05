
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models import EnterpriseService
from ..schemas import (
    EnterpriseServiceCreate,
    EnterpriseServiceUpdate,
)
from ..repositories import enterprise_service_repository


# ==========================================
# 查詢企業服務
# ==========================================

# 查詢所有企業服務，支援分類及啟用狀態篩選
def list_enterprise_services(
    db: Session,
    category: str | None = None,
    is_active: bool | None = None,
) -> list[EnterpriseService]:

    return enterprise_service_repository.get_all_enterprise_services(
        db,
        category=category,
        is_active=is_active,
    )


# 查詢單一企業服務
def get_enterprise_service(
    db: Session,
    service_id: int,
) -> EnterpriseService:

    enterprise_service = (
        enterprise_service_repository.get_enterprise_service_by_id(
            db,
            service_id,
        )
    )

    if enterprise_service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise service not found",
        )

    return enterprise_service


# ==========================================
# 企業服務代碼驗證
# ==========================================

# 確認服務代碼是否已被其他服務使用
def validate_service_code(
    db: Session,
    code: str,
    current_service_id: int | None = None,
) -> None:

    existing_service = (
        enterprise_service_repository.get_enterprise_service_by_code(
            db,
            code,
        )
    )

    if (
        existing_service is not None
        and existing_service.id != current_service_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enterprise service code already exists",
        )


# ==========================================
# 新增企業服務
# ==========================================

def create_enterprise_service(
    db: Session,
    service_data: EnterpriseServiceCreate,
) -> EnterpriseService:

    # 新增前檢查服務代碼是否重複
    validate_service_code(
        db,
        service_data.code,
    )

    try:
        return enterprise_service_repository.create_enterprise_service(
            db,
            code=service_data.code,
            name=service_data.name,
            category=service_data.category,
            description=service_data.description,
            is_active=service_data.is_active,
        )

    except IntegrityError as exc:
        # 處理資料庫唯一性約束衝突
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enterprise service code already exists",
        ) from exc


# ==========================================
# 修改企業服務
# ==========================================

def update_enterprise_service(
    db: Session,
    service_id: int,
    service_data: EnterpriseServiceUpdate,
) -> EnterpriseService:

    # 確認企業服務存在
    enterprise_service = get_enterprise_service(
        db,
        service_id,
    )

    # 確認新服務代碼沒有與其他服務衝突
    validate_service_code(
        db,
        service_data.code,
        current_service_id=service_id,
    )

    try:
        return enterprise_service_repository.update_enterprise_service(
            db,
            enterprise_service,
            code=service_data.code,
            name=service_data.name,
            category=service_data.category,
            description=service_data.description,
            is_active=service_data.is_active,
        )

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enterprise service code already exists",
        ) from exc


# ==========================================
# 刪除企業服務
# ==========================================

def delete_enterprise_service(
    db: Session,
    service_id: int,
) -> None:

    # 確認企業服務存在
    enterprise_service = get_enterprise_service(
        db,
        service_id,
    )

    enterprise_service_repository.delete_enterprise_service(
        db,
        enterprise_service,
    )
