
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    EnterpriseServiceCategory,
    EnterpriseServiceCreate,
    EnterpriseServiceResponse,
    EnterpriseServiceUpdate,
)
from ..services import enterprise_service


router = APIRouter(
    prefix="/api/enterprise-services",
    tags=["Enterprise Services"],
)


# ==========================================
# GET：取得所有企業服務
# ==========================================

@router.get(
    "",
    response_model=list[EnterpriseServiceResponse],
)
def get_enterprise_services(
    category: EnterpriseServiceCategory | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return enterprise_service.list_enterprise_services(
        db,
        category=category.value if category is not None else None,
        is_active=is_active,
    )


# ==========================================
# GET：取得單一企業服務
# ==========================================

@router.get(
    "/{service_id}",
    response_model=EnterpriseServiceResponse,
)
def get_enterprise_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    return enterprise_service.get_enterprise_service(
        db,
        service_id,
    )


# ==========================================
# POST：新增企業服務
# ==========================================

@router.post(
    "",
    response_model=EnterpriseServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_enterprise_service(
    service_data: EnterpriseServiceCreate,
    db: Session = Depends(get_db),
):
    return enterprise_service.create_enterprise_service(
        db,
        service_data,
    )


# ==========================================
# PUT：修改企業服務
# ==========================================

@router.put(
    "/{service_id}",
    response_model=EnterpriseServiceResponse,
)
def update_enterprise_service(
    service_id: int,
    service_data: EnterpriseServiceUpdate,
    db: Session = Depends(get_db),
):
    return enterprise_service.update_enterprise_service(
        db,
        service_id,
        service_data,
    )


# ==========================================
# DELETE：刪除企業服務
# ==========================================

@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_enterprise_service(
    service_id: int,
    db: Session = Depends(get_db),
) -> None:

    enterprise_service.delete_enterprise_service(
        db,
        service_id,
    )

    return None
