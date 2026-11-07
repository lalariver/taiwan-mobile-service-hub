# QA 測試計畫（QA Test Plan）
## Taiwan Mobile Service Hub

[English Version](./test-plan.md) | [測試策略](./test-strategy.zh-TW.md)

| 文件資訊 | 內容 |
|---|---|
| 專案名稱 | Taiwan Mobile Service Hub |
| 文件版本 | 1.0 |
| 最後更新日期 | 2026 年 11 月 8 日 |
| 測試框架 | Pytest + Playwright |
| 測試範圍 | API、Unit、Integration、E2E |
| 文件狀態 | 使用中 |
| 基準 Commit | `32d5c99` |

---

## 1. 測試目標（Test Objectives）

本測試計畫旨在驗證 Taiwan Mobile Service Hub 的功能正確性、資料完整性及系統可靠性。

測試活動的目標：

1. 驗證企業服務 API 是否符合規格。
2. 驗證後端業務邏輯及例外處理。
3. 確認資料庫操作能維持資料完整性。
4. 透過 React 管理介面驗證完整使用者操作流程。
5. 透過自動化測試預防回歸缺陷。
6. 將自動化品質檢查整合至 CI Pipeline。

## 2. 測試範圍（Test Scope）

### 2.1 功能測試範圍（Functional Scope）

目前測試週期涵蓋以下功能：

| 模組 | 功能 | 優先級 |
|---|---|---|
| 企業服務 | 查詢服務清單 | 高 |
| 企業服務 | 依分類篩選 | 中 |
| 企業服務 | 依啟用狀態篩選 | 中 |
| 企業服務 | 新增服務 | 高 |
| 企業服務 | 修改服務 | 高 |
| 企業服務 | 刪除服務 | 高 |
| 企業服務 | 啟用／停用服務 | 中 |
| 企業服務 | 搜尋服務 | 中 |
| 資料庫 | Unique Constraint 驗證 | 高 |
| 資料庫 | Transaction Rollback | 高 |
| 資料庫 | Session 資源清理 | 中 |

### 2.2 非功能測試範圍（Non-Functional Scope）

目前測試週期也會驗證：

- 測試環境與開發資料庫之間的隔離。
- 自動化測試的執行穩定性。
- Backend Code Coverage 門檻。
- Frontend Production Build 是否成功。
- 測試報告產生及保存。

效能測試、資訊安全測試及跨瀏覽器相容性測試不在本次範圍內。

## 3. 測試層級與執行計畫（Test Levels and Execution Plan）

### 3.1 單元測試（Unit Testing）

**測試框架：** Pytest

**測試位置：** `qa/tests/unit/`

**測試目的：** 不依賴外部系統或正式資料庫，獨立驗證後端個別函式及其錯誤處理。

測試範圍：

| 測試項目 | 驗證內容 |
|---|---|
| Transaction Commit | 驗證正常提交交易 |
| Transaction Rollback | 驗證資料庫錯誤時的回滾 |
| IntegrityError Handling | 驗證重複資料約束錯誤處理 |
| Database Session | 驗證 Session 資源清理 |

**預計測試案例數：4**

### 3.2 API 測試（API Testing）

**測試框架：** Pytest + FastAPI TestClient

**測試位置：** `qa/tests/api/`

**測試目的：** 驗證 REST API 行為、Request Validation、Response Status Code 及業務規則。

測試範圍：

| 測試項目 | 驗證內容 |
|---|---|
| GET | 查詢企業服務清單 |
| GET | 查詢條件篩選 |
| GET | 查詢存在及不存在的資料 |
| POST | 新增合法企業服務 |
| POST | 重複服務代碼 |
| POST | 欄位驗證 |
| POST | 邊界值分析 |
| PUT | 修改既有企業服務 |
| PUT | 不合法的修改請求 |
| DELETE | 刪除存在的企業服務 |
| DELETE | 刪除不存在的企業服務 |

**預計測試案例數：37**

### 3.3 資料庫整合測試（Database Integration Testing）

**測試框架：** Pytest + SQLAlchemy + SQLite

**測試位置：** `qa/tests/integration/`

**測試目的：** 驗證應用程式 Service、Repository、SQLAlchemy Session 及資料庫約束之間的整合。

測試範圍：

- 資料庫 UNIQUE Constraint 驗證。
- Transaction Commit 行為。
- IntegrityError 錯誤處理。
- Transaction Rollback。
- 已提交資料的持久性。
- Rollback 後未提交資料的移除。

**預計測試案例數：1**

目前的整合測試使用兩個獨立 Database Session 模擬交錯執行，並不代表真正的多執行緒負載測試。

### 3.4 端對端測試（End-to-End Testing）

**測試框架：** Playwright Python

**瀏覽器：** Chromium

**測試位置：** `qa/tests/e2e/`

**測試目的：** 透過 React 管理介面驗證完整的使用者操作流程。

| ID | 測試情境 | 預期結果 |
|---|---|---|
| UI-001 | 管理後台載入 | 管理畫面正確顯示 |
| UI-002 | 新增企業服務 | 新服務出現在清單中 |
| UI-003 | 修改企業服務 | 畫面顯示更新後的資料 |
| UI-004 | 刪除企業服務 | 被刪除的服務從清單中消失 |
| UI-005 | 重複服務代碼 | 顯示錯誤訊息 |
| UI-006 | 切換服務狀態 | 服務啟用狀態正確更新 |
| UI-007 | 搜尋企業服務 | 正確顯示符合條件的資料 |
| UI-008 | 重新載入頁面 | 先前建立的資料仍然存在 |

**預計測試案例數：8**

## 4. 測試環境及設定（Test Environment and Configuration）

### 4.1 本機環境（Local Environment）

| 元件 | 設定 |
|---|---|
| 作業系統 | macOS |
| Python | 3.12 |
| 後端 | FastAPI |
| ORM | SQLAlchemy 2.x |
| 資料庫 | SQLite |
| 前端 | React |
| 建置工具 | Vite |
| 測試框架 | Pytest |
| 瀏覽器自動化 | Playwright |
| 瀏覽器 | Chromium |

### 4.2 CI 環境（CI Environment）

| 元件 | 設定 |
|---|---|
| 平台 | GitHub Actions |
| Runner | Ubuntu Latest |
| Python | 3.12 |
| Node.js | 24 |
| 瀏覽器 | Chromium |
| 測試資料庫 | 暫存 SQLite |
| 覆蓋率工具 | pytest-cov |

### 4.3 服務設定（Service Configuration）

| 服務 | 位址 |
|---|---|
| FastAPI | `http://127.0.0.1:8000` |
| React / Vite | `http://127.0.0.1:5173` |
| Swagger UI | `http://127.0.0.1:8000/docs` |

## 5. 測試資料管理（Test Data Management）

測試資料必須與開發資料庫隔離。

API 測試與 E2E 測試使用不同的隔離機制。

**API Testing**

- 使用 Pytest `tmp_path` 建立暫存 SQLite Database。
- 建立獨立 SQLAlchemy Engine。
- 使用 FastAPI Dependency Overrides 替換 `get_db`。
- 每個 API Request 使用獨立 Database Session。
- 測試結束後清理暫存資料表。

**E2E Testing**

- 使用獨立的暫存 SQLite Database。
- 透過 `DATABASE_PATH` 環境變數設定 E2E Backend。
- 啟動 FastAPI 前先初始化測試資料庫。
- 每個 E2E Test 執行前清除測試資料。
- 測試 Session 結束後停止 Backend 和 Frontend Process。

自動化測試執行期間，不得修改開發資料庫 `taiwan_mobile.db`。

## 6. 測試執行排程（Test Execution Schedule）

測試依照以下階段執行：

| 階段 | 執行項目 | 交付成果 |
|---|---|---|
| 1 | 確認依賴套件與測試環境 | 可使用的測試環境 |
| 2 | 執行 Unit Tests | 單元測試結果 |
| 3 | 執行 API Tests | API 測試結果 |
| 4 | 執行 Database Integration Tests | 資料庫完整性驗證結果 |
| 5 | 啟動 Backend 與 Frontend | E2E 測試環境 |
| 6 | 執行 Playwright Tests | UI 測試結果 |
| 7 | 產生 Coverage 與測試報告 | 測試報告 |
| 8 | 執行 Frontend Production Build | 建置結果 |
| 9 | 驗證 CI Pipeline | CI 執行結果 |

以上流程由 GitHub Actions 自動執行。

## 7. 測試執行指令（Test Execution Commands）

### 7.1 執行全部測試

```bash
python -m pytest -v qa/tests
```

### 7.2 執行 API Tests

```bash
python -m pytest -v qa/tests/api
```

### 7.3 執行 Unit Tests

```bash
python -m pytest -v qa/tests/unit
```

### 7.4 執行 Integration Tests

```bash
python -m pytest -v qa/tests/integration
```

### 7.5 執行 E2E Tests

```bash
python -m pytest -v qa/tests/e2e
```

### 7.6 執行 Coverage Analysis

```bash
python -m pytest -v qa/tests \
    --cov=backend \
    --cov-branch \
    --cov-fail-under=90 \
    --cov-report=term-missing \
    --cov-report=html
```

### 7.7 建置 Frontend

```bash
cd frontend
npm ci
npm run build
```

## 8. 缺陷管理（Defect Management）

發現的缺陷必須記錄足夠資訊，以便重現及分析問題。

每份 Bug Report 應包含：

- Bug ID。
- 標題。
- 測試環境。
- 前置條件。
- 重現步驟。
- 預期結果。
- 實際結果。
- 嚴重程度（Severity）。
- 修復優先級（Priority）。
- 輔助證據。
- 根本原因（Root Cause），若已確認。
- 修正驗證結果。

### 8.1 嚴重程度分類（Severity Classification）

| 等級 | 定義 |
|---|---|
| Critical | 造成嚴重資料損毀或整體系統故障 |
| High | 主要業務功能無法正常使用 |
| Medium | 部分功能無法正常運作 |
| Low | 輕微功能或視覺問題 |

### 8.2 缺陷處理流程（Defect Lifecycle）

1. 發現問題。
2. 重現問題。
3. 記錄缺陷。
4. 分析根本原因。
5. 修正問題。
6. 重新測試受影響的功能。
7. 執行回歸測試。

只有確認為實際缺陷的問題，才應登記為正式 Bug；尚未驗證的風險則應另外記錄。

## 9. 測試進入條件（Entry Criteria）

符合以下條件後，才開始執行測試：

- Backend 依賴套件已安裝。
- Frontend 依賴套件可正常使用。
- 資料庫設定正確。
- 測試資料庫可以正常初始化。
- Backend 與 Frontend Server 可以正常啟動。
- Playwright Chromium 已安裝。
- 測試程式碼已準備完成。

## 10. 測試退出條件（Exit Criteria）

符合以下條件時，視為本次測試週期成功：

1. 所有必要的自動化測試皆通過。
2. Backend Code Coverage 至少達到 90%。
3. React Production Build 成功。
4. 測試範圍內沒有尚未解決的 Critical Defects。
5. GitHub Actions 執行成功。
6. 測試報告成功產生並上傳。

## 11. 測試交付成果（Test Deliverables）

| 交付項目 | 檔案位置 |
|---|---|
| 測試策略 | `docs/test-strategy.zh-TW.md` |
| 測試計畫 | `docs/test-plan.zh-TW.md` |
| API 測試案例 | `qa/tests/api/` |
| Unit 測試案例 | `qa/tests/unit/` |
| Integration 測試案例 | `qa/tests/integration/` |
| E2E 測試案例 | `qa/tests/e2e/` |
| Bug Reports | `docs/bug-reports/` |
| JUnit XML | `qa/.artifacts/` |
| HTML Coverage | `htmlcov/` |
| CI Workflow | `.github/workflows/ci.yml` |

## 12. 測試基準執行結果（Baseline Execution Results）

目前已驗證的自動化測試基準：

| 測試層級 | 案例數 | 結果 |
|---|---:|---|
| API Testing | 37 | 通過 |
| Unit Testing | 4 | 通過 |
| Integration Testing | 1 | 通過 |
| E2E Testing | 8 | 通過 |
| **總計** | **50** | **全部通過** |

### 品質指標（Quality Metrics）

| 指標 | 結果 |
|---|---:|
| Backend Coverage | 93.85% |
| 最低 Coverage 門檻 | 90% |
| 本機自動化測試 | 50 Passed |
| GitHub Actions CI | 執行成功 |
| React Production Build | 成功 |

### 基準評估（Baseline Assessment）

目前的自動化測試架構已成功驗證現有企業服務 CRUD 功能，測試涵蓋 API、後端、資料庫及前端操作流程。

CI Pipeline 能自動執行回歸測試，並強制執行最低 Backend Coverage 門檻。

以上數據為初始 CI 實作時已驗證的基準。未來每次測試仍應依照當次執行結果判斷，不應直接假設後續版本都會通過。

---

**文件負責單位：** Quality Engineering Project

**文件目的：** 定義 Taiwan Mobile Service Hub 的測試範圍、環境、執行流程、驗收條件及交付成果。