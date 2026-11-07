
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import EnterpriseService


API_URL = "/api/enterprise-services"


# ==========================================
# Test Helper
# ==========================================

def _create_service(
    client: TestClient,
    payload: dict[str, object],
) -> dict[str, object]:
    """建立企業服務，並回傳 API Response。"""

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


# ==========================================
# GET Tests
# ==========================================

def test_list_enterprise_services_returns_empty_list(
    client: TestClient,
) -> None:
    """查詢沒有資料的企業服務清單。"""

    response = client.get(API_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_list_enterprise_services_returns_all_records(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """查詢所有企業服務。"""

    first_payload = service_payload.copy()

    second_payload = service_payload.copy()
    second_payload["code"] = "QA-TEST-002"
    second_payload["name"] = "Second Test Service"

    _create_service(client, first_payload)
    _create_service(client, second_payload)

    response = client.get(API_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_services_by_category(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """依照服務分類篩選。"""

    first_payload = service_payload.copy()

    second_payload = service_payload.copy()
    second_payload["code"] = "QA-TEST-002"
    second_payload["category"] = "cloud_computing"

    _create_service(client, first_payload)
    _create_service(client, second_payload)

    response = client.get(
        API_URL,
        params={"category": "connectivity"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "connectivity"


def test_list_services_by_active_status(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """依照服務啟用狀態篩選。"""

    active_payload = service_payload.copy()

    inactive_payload = service_payload.copy()
    inactive_payload["code"] = "QA-TEST-002"
    inactive_payload["is_active"] = False

    _create_service(client, active_payload)
    _create_service(client, inactive_payload)

    response = client.get(
        API_URL,
        params={"is_active": True},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["is_active"] is True


def test_list_services_by_multiple_filters(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """同時依照分類及啟用狀態篩選。"""

    matching_payload = service_payload.copy()

    inactive_payload = service_payload.copy()
    inactive_payload["code"] = "QA-TEST-002"
    inactive_payload["is_active"] = False

    other_category_payload = service_payload.copy()
    other_category_payload["code"] = "QA-TEST-003"
    other_category_payload["category"] = "cloud_computing"

    _create_service(client, matching_payload)
    _create_service(client, inactive_payload)
    _create_service(client, other_category_payload)

    response = client.get(
        API_URL,
        params={
            "category": "connectivity",
            "is_active": True,
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["code"] == "QA-TEST-001"


def test_get_existing_enterprise_service(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """查詢存在的企業服務。"""

    created = _create_service(
        client,
        service_payload,
    )

    response = client.get(
        f"{API_URL}/{created['id']}",
    )

    assert response.status_code == 200
    assert response.json()["code"] == service_payload["code"]


def test_get_nonexistent_service_returns_404(
    client: TestClient,
) -> None:
    """查詢不存在的企業服務。"""

    response = client.get(
        f"{API_URL}/9999",
    )

    assert response.status_code == 404


# ==========================================
# POST Tests
# ==========================================

def test_create_enterprise_service(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """成功新增企業服務。"""

    response = client.post(
        API_URL,
        json=service_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["code"] == service_payload["code"]
    assert data["name"] == service_payload["name"]
    assert data["is_active"] is True
    assert data["id"] > 0


def test_create_service_with_default_active_status(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """新增服務時未提供 is_active，預設應為 True。"""

    payload = service_payload.copy()
    payload.pop("is_active")

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["is_active"] is True


def test_create_duplicate_service_code_returns_409(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """新增重複的企業服務代碼。"""

    first_response = client.post(
        API_URL,
        json=service_payload,
    )

    second_response = client.post(
        API_URL,
        json=service_payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.parametrize(
    ("code", "expected_status"),
    [
        ("AB", 422),
        ("ABC", 201),
        ("A" * 30, 201),
        ("A" * 31, 422),
    ],
)
def test_service_code_length_boundaries(
    client: TestClient,
    service_payload: dict[str, object],
    code: str,
    expected_status: int,
) -> None:
    """測試 Code 長度的 Boundary Values。"""

    payload = service_payload.copy()
    payload["code"] = code

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "code",
    [
        "abc-001",
        "A--001",
        "-ABC",
        "ABC-",
        "ABC_001",
    ],
)
def test_create_service_with_invalid_code_format(
    client: TestClient,
    service_payload: dict[str, object],
    code: str,
) -> None:
    """測試不符合 Code 格式的輸入。"""

    payload = service_payload.copy()
    payload["code"] = code

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("name", "expected_status"),
    [
        ("", 422),
        ("A", 201),
        ("N" * 150, 201),
        ("N" * 151, 422),
    ],
)
def test_service_name_length_boundaries(
    client: TestClient,
    service_payload: dict[str, object],
    name: str,
    expected_status: int,
) -> None:
    """測試 Name 長度的 Boundary Values。"""

    payload = service_payload.copy()
    payload["name"] = name

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("description", "expected_status"),
    [
        ("", 422),
        ("D", 201),
        ("D" * 2000, 201),
        ("D" * 2001, 422),
    ],
)
def test_service_description_length_boundaries(
    client: TestClient,
    service_payload: dict[str, object],
    description: str,
    expected_status: int,
) -> None:
    """測試 Description 長度的 Boundary Values。"""

    payload = service_payload.copy()
    payload["description"] = description

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == expected_status


def test_create_service_with_invalid_category_returns_422(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """測試不合法的服務分類。"""

    payload = service_payload.copy()
    payload["category"] = "invalid_category"

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == 422


def test_create_service_without_required_field_returns_422(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """測試缺少必要欄位。"""

    payload = service_payload.copy()
    payload.pop("description")

    response = client.post(
        API_URL,
        json=payload,
    )

    assert response.status_code == 422


# ==========================================
# PUT Tests
# ==========================================

def test_update_enterprise_service(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """成功修改企業服務。"""

    created = _create_service(
        client,
        service_payload,
    )

    updated_payload = service_payload.copy()
    updated_payload["name"] = "Updated QA Service"

    response = client.put(
        f"{API_URL}/{created['id']}",
        json=updated_payload,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated QA Service"


def test_update_service_persists_record(
    client: TestClient,
    db_session: Session,
    service_payload: dict[str, object],
) -> None:
    """確認修改後的資料確實寫入資料庫。"""

    created = _create_service(
        client,
        service_payload,
    )

    updated_payload = service_payload.copy()
    updated_payload["name"] = "Persisted Updated Service"

    response = client.put(
        f"{API_URL}/{created['id']}",
        json=updated_payload,
    )

    assert response.status_code == 200

    record = db_session.get(
        EnterpriseService,
        created["id"],
    )

    assert record is not None
    assert record.name == "Persisted Updated Service"


def test_update_service_without_required_field_returns_422(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """PUT 缺少必要欄位時應回傳 422。"""

    created = _create_service(
        client,
        service_payload,
    )

    payload = service_payload.copy()
    payload.pop("description")

    response = client.put(
        f"{API_URL}/{created['id']}",
        json=payload,
    )

    assert response.status_code == 422


def test_update_nonexistent_service_returns_404(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """修改不存在的企業服務。"""

    response = client.put(
        f"{API_URL}/9999",
        json=service_payload,
    )

    assert response.status_code == 404


def test_update_service_with_duplicate_code_returns_409(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """修改成其他服務已使用的 Code。"""

    first_payload = service_payload.copy()

    second_payload = service_payload.copy()
    second_payload["code"] = "QA-TEST-002"

    first_service = _create_service(
        client,
        first_payload,
    )

    _create_service(
        client,
        second_payload,
    )

    update_payload = first_payload.copy()
    update_payload["code"] = "QA-TEST-002"

    response = client.put(
        f"{API_URL}/{first_service['id']}",
        json=update_payload,
    )

    assert response.status_code == 409


# ==========================================
# DELETE Tests
# ==========================================

def test_delete_enterprise_service(
    client: TestClient,
    service_payload: dict[str, object],
) -> None:
    """成功刪除企業服務。"""

    created = _create_service(
        client,
        service_payload,
    )

    response = client.delete(
        f"{API_URL}/{created['id']}",
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(
        f"{API_URL}/{created['id']}",
    )

    assert get_response.status_code == 404


def test_delete_service_persists_removal(
    client: TestClient,
    db_session: Session,
    service_payload: dict[str, object],
) -> None:
    """確認刪除後資料庫不再存在該筆資料。"""

    created = _create_service(
        client,
        service_payload,
    )

    response = client.delete(
        f"{API_URL}/{created['id']}",
    )

    assert response.status_code == 204

    record = db_session.get(
        EnterpriseService,
        created["id"],
    )

    assert record is None


def test_delete_nonexistent_service_returns_404(
    client: TestClient,
) -> None:
    """刪除不存在的企業服務。"""

    response = client.delete(
        f"{API_URL}/9999",
    )

    assert response.status_code == 404
