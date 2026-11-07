# 測試案例文件（Test Cases）

**專案：** Taiwan Mobile Service Hub
**文件：** Test Cases
**版本：** 1.0
**最後更新：** 2026-11-08
**驗證版本：** `32d5c99`

## 1. 測試總覽

本文件定義 QA 自動化測試套件中實際實作的 50 個測試案例。

| 測試層級 | 案例數量 | 測試範圍 |
|---|---:|---|
| API Testing | 37 | CRUD、輸入驗證、HTTP 錯誤處理 |
| Unit Testing | 4 | Transaction 與 Database Session Lifecycle |
| Integration Testing | 1 | 多個 Database Session 的交易回滾 |
| E2E Testing | 8 | 企業服務管理後台 UI 操作流程 |
| **總計** | **50** | |

## 2. 測試環境與前置條件

### 2.1 API 測試環境

- Python 3.12
- FastAPI TestClient
- SQLAlchemy
- SQLite
- Pytest
- 每個測試使用獨立的暫存 SQLite Database。
- 透過 FastAPI Dependency Override，將 `get_db` 替換成測試專用資料庫。

### 2.2 預設測試資料

| 欄位 | 預設值 |
|---|---|
| code | `QA-TEST-001` |
| name | `QA Test Service` |
| category | `connectivity` |
| description | `Test service for automation testing.` |
| is_active | `true` |

### 2.3 一般前置條件

- 已安裝應用程式及測試所需依賴套件。
- Database Fixtures 已成功初始化。
- API 測試使用獨立的暫存資料庫。
- E2E 測試使用獨立的 E2E 環境與測試資料庫。
- 每個測試使用自己的測試資料。

## 3. API 測試案例

### 3.1 GET — 查詢企業服務

| ID | 測試情境／測試資料 | 預期結果 | Pytest Function |
|---|---|---|---|
| API-001 | 查詢沒有任何資料的企業服務清單。 | HTTP 200；Response 為空陣列。 | `test_list_enterprise_services_returns_empty_list` |
| API-002 | 建立兩筆企業服務後查詢清單。 | HTTP 200；回傳兩筆資料。 | `test_list_enterprise_services_returns_all_records` |
| API-003 | 使用 `category=connectivity` 篩選服務。 | HTTP 200；只回傳符合分類的資料。 | `test_list_services_by_category` |
| API-004 | 使用 `is_active=true` 篩選服務。 | HTTP 200；只回傳啟用中的服務。 | `test_list_services_by_active_status` |
| API-005 | 同時使用分類及啟用狀態進行篩選。 | HTTP 200；只回傳同時符合兩個條件的資料。 | `test_list_services_by_multiple_filters` |
| API-006 | 使用 ID 查詢存在的企業服務。 | HTTP 200；回傳資料的 Code 與建立時一致。 | `test_get_existing_enterprise_service` |
| API-007 | 使用 ID `9999` 查詢不存在的企業服務。 | HTTP 404。 | `test_get_nonexistent_service_returns_404` |

### 3.2 POST — 新增企業服務

| ID | 測試情境／測試資料 | 預期結果 | Pytest Function |
|---|---|---|---|
| API-008 | 使用預設合法資料新增企業服務。 | HTTP 201；回傳 Code、Name 與請求一致；啟用狀態為 true；產生的 ID 大於 0。 | `test_create_enterprise_service` |
| API-009 | 新增時不提供 `is_active`。 | HTTP 201；`is_active` 預設為 true。 | `test_create_service_with_default_active_status` |
| API-010 | 使用相同服務代碼連續新增兩次。 | 第一次 HTTP 201；第二次 HTTP 409。 | `test_create_duplicate_service_code_returns_409` |
| API-011 | Code 長度為 2 個字元：`AB`。 | HTTP 422。 | `test_service_code_length_boundaries` |
| API-012 | Code 長度為 3 個字元：`ABC`。 | HTTP 201。 | `test_service_code_length_boundaries` |
| API-013 | Code 長度為 30 個字元。 | HTTP 201。 | `test_service_code_length_boundaries` |
| API-014 | Code 長度為 31 個字元。 | HTTP 422。 | `test_service_code_length_boundaries` |
| API-015 | Code 格式錯誤：`abc-001`。 | HTTP 422。 | `test_create_service_with_invalid_code_format` |
| API-016 | Code 格式錯誤：`A--001`。 | HTTP 422。 | `test_create_service_with_invalid_code_format` |
| API-017 | Code 格式錯誤：`-ABC`。 | HTTP 422。 | `test_create_service_with_invalid_code_format` |
| API-018 | Code 格式錯誤：`ABC-`。 | HTTP 422。 | `test_create_service_with_invalid_code_format` |
| API-019 | Code 格式錯誤：`ABC_001`。 | HTTP 422。 | `test_create_service_with_invalid_code_format` |
| API-020 | Name 為空字串。 | HTTP 422。 | `test_service_name_length_boundaries` |
| API-021 | Name 長度為 1 個字元。 | HTTP 201。 | `test_service_name_length_boundaries` |
| API-022 | Name 長度為 150 個字元。 | HTTP 201。 | `test_service_name_length_boundaries` |
| API-023 | Name 長度為 151 個字元。 | HTTP 422。 | `test_service_name_length_boundaries` |
| API-024 | Description 為空字串。 | HTTP 422。 | `test_service_description_length_boundaries` |
| API-025 | Description 長度為 1 個字元。 | HTTP 201。 | `test_service_description_length_boundaries` |
| API-026 | Description 長度為 2,000 個字元。 | HTTP 201。 | `test_service_description_length_boundaries` |
| API-027 | Description 長度為 2,001 個字元。 | HTTP 422。 | `test_service_description_length_boundaries` |
| API-028 | 提交不支援的分類：`invalid_category`。 | HTTP 422。 | `test_create_service_with_invalid_category_returns_422` |
| API-029 | 新增時缺少必要欄位 `description`。 | HTTP 422。 | `test_create_service_without_required_field_returns_422` |

### 3.3 PUT — 修改企業服務

| ID | 測試情境／測試資料 | 預期結果 | Pytest Function |
|---|---|---|---|
| API-030 | 將既有服務名稱修改為 `Updated QA Service`。 | HTTP 200；Response 包含更新後的名稱。 | `test_update_enterprise_service` |
| API-031 | 修改服務後直接查詢資料庫。 | HTTP 200；資料庫紀錄包含更新後的名稱。 | `test_update_service_persists_record` |
| API-032 | 修改服務時缺少必要欄位 `description`。 | HTTP 422。 | `test_update_service_without_required_field_returns_422` |
| API-033 | 使用 ID `9999` 修改不存在的企業服務。 | HTTP 404。 | `test_update_nonexistent_service_returns_404` |
| API-034 | 修改服務時使用其他資料已經使用的 Code。 | HTTP 409。 | `test_update_service_with_duplicate_code_returns_409` |

### 3.4 DELETE — 刪除企業服務

| ID | 測試情境／測試資料 | 預期結果 | Pytest Function |
|---|---|---|---|
| API-035 | 刪除存在的企業服務。 | HTTP 204；Response Body 為空；後續 GET 查詢回傳 HTTP 404。 | `test_delete_enterprise_service` |
| API-036 | 刪除服務後直接查詢資料庫。 | HTTP 204；資料庫中已不存在該筆資料。 | `test_delete_service_persists_removal` |
| API-037 | 使用 ID `9999` 刪除不存在的企業服務。 | HTTP 404。 | `test_delete_nonexistent_service_returns_404` |

## 4. Unit Test 測試案例

| ID | 測試情境 | 預期結果 | Pytest Function |
|---|---|---|---|
| UNIT-001 | `commit()` 因服務代碼重複而拋出 UNIQUE Constraint `IntegrityError`。 | 拋出 HTTP 409；`commit()` 與 `rollback()` 各呼叫一次。 | `test_commit_transaction_rolls_back_on_duplicate_code` |
| UNIT-002 | `commit()` 因 NOT NULL Constraint 拋出 `IntegrityError`。 | 重新拋出原始 `IntegrityError`；執行一次 Rollback。 | `test_commit_transaction_rolls_back_on_other_integrity_error` |
| UNIT-003 | `commit()` 發生非預期的 `RuntimeError`。 | 重新拋出原始 `RuntimeError`；執行一次 Rollback。 | `test_commit_transaction_rolls_back_on_unexpected_error` |
| UNIT-004 | 執行 `get_db()` Generator 直到結束。 | 取得的 Session 與 Mock Session 相同；`close()` 被呼叫一次。 | `test_get_db_closes_session` |

## 5. Integration Test 測試案例

| ID | 測試情境 | 預期結果 | Pytest Function |
|---|---|---|---|
| INT-001 | 兩個獨立 Database Session 先檢查相同服務代碼。Session A 新增並 Commit 該代碼；Session B 新增一筆合法資料及一筆重複代碼資料後嘗試 Commit。 | Session B 收到 HTTP 409，並回滾整個 Transaction。使用新的 Session 驗證後，資料庫只保留 Session A 的資料；Session B 原本合法的待提交資料也不存在。 | `test_unique_constraint_rolls_back_all_pending_changes` |

**測試目的：** 驗證 Transaction Atomicity（交易原子性）。當一個交易失敗時，該交易內所有尚未提交的變更都必須回滾。

**測試限制：** 此測試使用兩個獨立 Session，透過先後 Commit 模擬唯一性衝突，並非多執行緒併發負載或壓力測試。

## 6. End-to-End Test 測試案例

| ID | 測試情境 | 預期結果 | Pytest Function |
|---|---|---|---|
| E2E-001 | 開啟企業服務管理後台。 | 後台標題及服務總覽標題顯示；空資料提示訊息顯示。 | `test_dashboard_loads_successfully` |
| E2E-002 | 透過 UI 新增企業服務。 | 新增資料出現在表格中，且 Code、Name、啟用狀態正確。 | `test_create_enterprise_service` |
| E2E-003 | 修改既有企業服務名稱。 | 表格顯示修改後的服務名稱。 | `test_update_enterprise_service` |
| E2E-004 | 刪除既有企業服務。 | 顯示確認 Dialog，內容符合預期；確認刪除後，資料列從畫面移除。 | `test_delete_enterprise_service` |
| E2E-005 | 使用已存在的 Code 新增企業服務。 | UI 顯示 API 回傳的重複服務代碼錯誤訊息。 | `test_duplicate_service_code_displays_error` |
| E2E-006 | 先停用再重新啟用企業服務。 | UI 狀態依序從啟用中變為已停用，再變回啟用中。 | `test_toggle_enterprise_service_status` |
| E2E-007 | 建立兩筆服務後搜尋 `Network Service`。 | 符合搜尋條件的資料列保留顯示；不符合條件的資料列不再顯示。 | `test_search_enterprise_services` |
| E2E-008 | 新增企業服務後重新載入頁面。 | 重新載入後，剛才新增的服務仍然顯示。 | `test_service_persists_after_page_reload` |

## 7. 需求追溯矩陣（Requirements Traceability Matrix）

以下功能需求分類依據目前已實作的系統行為與測試範圍整理，並非已正式核准的獨立商業需求規格。

| Requirement ID | 功能需求 | 對應測試案例 |
|---|---|---|
| FR-01 | 查詢及篩選企業服務。 | API-001～API-007、E2E-001、E2E-007 |
| FR-02 | 新增企業服務。 | API-008～API-029、E2E-002 |
| FR-03 | 修改企業服務。 | API-030～API-034、E2E-003 |
| FR-04 | 刪除企業服務。 | API-035～API-037、E2E-004 |
| FR-05 | 確保服務代碼唯一性並處理衝突。 | API-010、API-034、UNIT-001、UNIT-002、INT-001、E2E-005 |
| FR-06 | 驗證服務欄位格式及長度邊界。 | API-011～API-029 |
| FR-07 | 管理企業服務啟用狀態。 | API-004、API-005、API-008、API-009、E2E-002、E2E-006 |
| FR-08 | 確保服務資料持久化。 | API-031、API-036、INT-001、E2E-008 |
| FR-09 | 管理資料庫交易及 Session Lifecycle。 | UNIT-001～UNIT-004、INT-001 |

## 8. 測試執行指令

執行全部測試：

```bash
./.venv/bin/python -m pytest -v qa/tests
```

只收集測試案例，不實際執行：

```bash
./.venv/bin/python -m pytest --collect-only -vv qa/tests
```

執行測試並檢查 Coverage：

```bash
./.venv/bin/python -m pytest -v qa/tests \
  --cov=backend \
  --cov-branch \
  --cov-fail-under=90 \
  --cov-report=term-missing
```

## 9. 測試結果基準

已驗證的測試結果：

| 指標 | 結果 |
|---|---:|
| 收集測試總數 | 50 |
| API Tests | 37 |
| Unit Tests | 4 |
| Integration Tests | 1 |
| E2E Tests | 8 |
| Backend Coverage | 93.85% |
| Coverage Gate | 90% |
| 本機測試結果 | 50 passed |

**驗證 Commit：** `32d5c99`

## 10. 已知限制

- 尚未涵蓋 Authentication 與 Role-Based Access Control。
- 尚未執行 Security Testing 與 Penetration Testing。
- 尚未執行 Performance Testing 與 Load Testing。
- E2E 瀏覽器測試目前僅涵蓋 Chromium。
- Integration Test 未模擬實際併發負載。
- 資料庫錯誤處理目前仍有 SQLite 專屬行為。
- 需求追溯矩陣依目前已實作功能整理；正式商業需求核准不在本文件範圍內。