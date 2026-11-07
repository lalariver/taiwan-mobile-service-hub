
from playwright.sync_api import (
    Page,
    expect,
)


# ==========================================
# Test Helpers
# ==========================================

def open_create_dialog(page: Page):
    """開啟新增企業服務視窗。"""

    page.get_by_role(
        "button",
        name="+ 新增服務",
    ).click()

    return page.get_by_role(
        "dialog",
        name="新增企業服務",
    )


def create_service(
    page: Page,
    code: str,
    name: str,
) :
    """透過 UI 建立企業服務。"""

    dialog = open_create_dialog(page)

    dialog.get_by_label("服務代碼").fill(code)
    dialog.get_by_label("服務名稱").fill(name)

    dialog.get_by_label("服務分類").select_option(
        "connectivity",
    )

    dialog.get_by_label("服務說明").fill(
        "Playwright E2E automation test service.",
    )

    dialog.get_by_role(
        "button",
        name="建立服務",
    ).click()

    row = page.get_by_role("row").filter(
        has_text=code,
    )

    expect(row).to_be_visible()

    return row


# ==========================================
# UI-001：Dashboard Loading
# ==========================================

def test_dashboard_loads_successfully(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認管理後台可以正常載入。"""

    page.goto(e2e_environment["base_url"])

    expect(
        page.get_by_role(
            "heading",
            name="企業服務管理",
        ),
    ).to_be_visible()

    expect(
        page.get_by_role(
            "heading",
            name="服務總覽",
        ),
    ).to_be_visible()

    expect(
        page.get_by_text(
            "目前沒有符合條件的企業服務",
        ),
    ).to_be_visible()


# ==========================================
# UI-002：Create Service
# ==========================================

def test_create_enterprise_service(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認管理員可以透過 UI 新增企業服務。"""

    page.goto(e2e_environment["base_url"])

    row = create_service(
        page,
        code="E2E-UI-001",
        name="Playwright Test Service",
    )

    expect(row).to_contain_text(
        "Playwright Test Service",
    )

    expect(row).to_contain_text("E2E-UI-001")
    expect(row).to_contain_text("啟用中")


# ==========================================
# UI-003：Update Service
# ==========================================

def test_update_enterprise_service(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認管理員可以透過 UI 修改企業服務。"""

    page.goto(e2e_environment["base_url"])

    row = create_service(
        page,
        code="E2E-UI-002",
        name="Original Service",
    )

    row.get_by_role(
        "button",
        name="編輯",
    ).click()

    dialog = page.get_by_role(
        "dialog",
        name="編輯企業服務",
    )

    dialog.get_by_label("服務名稱").fill(
        "Updated Playwright Service",
    )

    dialog.get_by_role(
        "button",
        name="儲存修改",
    ).click()

    updated_row = page.get_by_role("row").filter(
        has_text="E2E-UI-002",
    )

    expect(updated_row).to_contain_text(
        "Updated Playwright Service",
    )


# ==========================================
# UI-004：Delete Service
# ==========================================


def test_delete_enterprise_service(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認管理員可以透過 UI 刪除企業服務。"""

    page.goto(e2e_environment["base_url"])

    row = create_service(
        page,
        code="E2E-UI-003",
        name="Service To Delete",
    )

    # 儲存 Dialog 資訊
    dialog_details: dict[str, str] = {}

    # Dialog 出現時立即處理
    def handle_dialog(dialog) -> None:
        dialog_details["type"] = dialog.type
        dialog_details["message"] = dialog.message

        dialog.accept()

    page.once("dialog", handle_dialog)

    # 點擊刪除，Dialog 會由 handle_dialog 接受
    row.get_by_role(
        "button",
        name="刪除",
    ).click()

    # 確認 Dialog 的內容
    assert dialog_details["type"] == "confirm"

    assert (
        dialog_details["message"]
        == "確定要刪除「Service To Delete」嗎？"
    )

    # 確認資料已從畫面移除
    expect(row).to_have_count(0)


# ==========================================
# UI-005：Duplicate Code Error
# ==========================================

def test_duplicate_service_code_displays_error(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認重複服務代碼會顯示 API 錯誤訊息。"""

    page.goto(e2e_environment["base_url"])

    create_service(
        page,
        code="E2E-UI-004",
        name="Original Duplicate Test",
    )

    dialog = open_create_dialog(page)

    dialog.get_by_label("服務代碼").fill(
        "E2E-UI-004",
    )

    dialog.get_by_label("服務名稱").fill(
        "Duplicate Service",
    )

    dialog.get_by_label("服務分類").select_option(
        "connectivity",
    )

    dialog.get_by_label("服務說明").fill(
        "This code already exists.",
    )

    dialog.get_by_role(
        "button",
        name="建立服務",
    ).click()

    expect(
        dialog.get_by_role("alert"),
    ).to_contain_text(
        "Enterprise service code already exists",
    )


# ==========================================
# UI-006：Toggle Service Status
# ==========================================

def test_toggle_enterprise_service_status(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認管理員可以啟用及停用服務。"""

    page.goto(e2e_environment["base_url"])

    row = create_service(
        page,
        code="E2E-UI-005",
        name="Status Test Service",
    )

    expect(row).to_contain_text("啟用中")

    row.get_by_role(
        "button",
        name="停用",
    ).click()

    expect(row).to_contain_text("已停用")

    row.get_by_role(
        "button",
        name="啟用",
    ).click()

    expect(row).to_contain_text("啟用中")


# ==========================================
# UI-007：Search Services
# ==========================================

def test_search_enterprise_services(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認關鍵字搜尋可以正確篩選服務。"""

    page.goto(e2e_environment["base_url"])

    first_row = create_service(
        page,
        code="E2E-UI-006",
        name="Network Service",
    )

    second_row = create_service(
        page,
        code="E2E-UI-007",
        name="Cloud Service",
    )

    search_input = page.get_by_placeholder(
        "搜尋服務名稱、代碼或說明...",
    )

    search_input.fill("Network Service")

    expect(first_row).to_be_visible()
    expect(second_row).to_have_count(0)


# ==========================================
# UI-008：Reload Persistence
# ==========================================

def test_service_persists_after_page_reload(
    page: Page,
    e2e_environment: dict[str, str],
) -> None:
    """確認重新載入頁面後，資料仍然存在。"""

    page.goto(e2e_environment["base_url"])

    create_service(
        page,
        code="E2E-UI-008",
        name="Persistent Service",
    )

    page.reload()

    row = page.get_by_role("row").filter(
        has_text="E2E-UI-008",
    )

    expect(row).to_be_visible()

    expect(row).to_contain_text(
        "Persistent Service",
    )
