
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import EnterpriseService


# ==========================================
# 查詢企業服務
# ==========================================

def get_all_enterprise_services(
    db: Session,
    category: str | None = None,
    is_active: bool | None = None,
) -> list[EnterpriseService]:

    statement = select(EnterpriseService)

    # 依服務分類篩選
    if category is not None:
        statement = statement.where(
            EnterpriseService.category == category,
        )

    # 依啟用狀態篩選
    if is_active is not None:
        statement = statement.where(
            EnterpriseService.is_active == is_active,
        )

    # 依照 ID 排序
    statement = statement.order_by(
        EnterpriseService.id,
    )

    return list(db.scalars(statement).all())


# 根據 ID 查詢企業服務
def get_enterprise_service_by_id(
    db: Session,
    service_id: int,
) -> EnterpriseService | None:

    return db.get(
        EnterpriseService,
        service_id,
    )


# 根據服務代碼查詢企業服務
def get_enterprise_service_by_code(
    db: Session,
    code: str,
) -> EnterpriseService | None:

    statement = select(EnterpriseService).where(
        EnterpriseService.code == code,
    )

    return db.scalar(statement)


# ==========================================
# 新增企業服務
# ==========================================

def create_enterprise_service(
    db: Session,
    code: str,
    name: str,
    category: str,
    description: str,
    is_active: bool,
) -> EnterpriseService:

    enterprise_service = EnterpriseService(
        code=code,
        name=name,
        category=category,
        description=description,
        is_active=is_active,
    )

    db.add(enterprise_service)

    return enterprise_service


# ==========================================
# 修改企業服務
# ==========================================

def update_enterprise_service(
    db: Session,
    enterprise_service: EnterpriseService,
    code: str,
    name: str,
    category: str,
    description: str,
    is_active: bool,
) -> EnterpriseService:

    enterprise_service.code = code
    enterprise_service.name = name
    enterprise_service.category = category
    enterprise_service.description = description
    enterprise_service.is_active = is_active

    return enterprise_service


# ==========================================
# 刪除企業服務
# ==========================================

def delete_enterprise_service(
    db: Session,
    enterprise_service: EnterpriseService,
) -> None:

    db.delete(enterprise_service)
