
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Enterprise Service
# ==========================================

# 台灣大哥大企業服務 6C 分類
class EnterpriseServiceCategory(str, Enum):
    CONNECTIVITY = "connectivity"
    CLOUD_COMPUTING = "cloud_computing"
    CLIENT_SOLUTIONS_AI = "client_solutions_ai"
    CYBERSECURITY = "cybersecurity"
    CARBON_ENERGY = "carbon_energy"
    CONSULTING_MANAGED = "consulting_managed"


# 企業服務共用欄位
class EnterpriseServiceBase(BaseModel):

    # 服務代碼，例如 CONNECT-001
    code: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    )

    # 服務名稱
    name: str = Field(
        min_length=1,
        max_length=150,
    )

    # 服務分類
    category: EnterpriseServiceCategory

    # 服務說明
    description: str = Field(
        min_length=1,
        max_length=2000,
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
    )


# 新增企業服務時使用
class EnterpriseServiceCreate(EnterpriseServiceBase):

    # 新服務預設啟用
    is_active: bool = True


# 修改企業服務時使用
class EnterpriseServiceUpdate(EnterpriseServiceBase):

    # PUT 採完整更新，因此所有欄位都必須提供
    is_active: bool


# API 回傳企業服務時使用
class EnterpriseServiceResponse(EnterpriseServiceBase):

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )
