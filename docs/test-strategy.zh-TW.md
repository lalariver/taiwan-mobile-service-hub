# QA 測試策略（QA Test Strategy）
## Taiwan Mobile Service Hub

[English Version](./test-strategy.md)

| 文件資訊 | 內容 |
|---|---|
| 專案名稱 | Taiwan Mobile Service Hub |
| 文件版本 | 1.0 |
| 最後更新日期 | 2026 年 11 月 8 日 |
| 測試框架 | Pytest + Playwright |
| 文件狀態 | 使用中 |
| 驗證 Commit | `32d5c99` |

---

## 1. 文件目的（Purpose）

本文件定義 Taiwan Mobile Service Hub 專案的整體測試策略。

主要目標是建立一套可維護且可靠的自動化測試架構，用於驗證後端 API、業務邏輯、資料庫操作及前端管理介面流程。

測試策略著重於：

- 在軟體開發生命週期早期發現缺陷。
- 預防回歸缺陷（Regression Bugs）。
- 驗證資料完整性及交易一致性（Transaction Consistency）。
- 自動化重複性的測試工作。
- 透過持續整合（Continuous Integration, CI）提升程式碼變更的可靠性。

## 2. 受測系統（System Under Test, SUT）

Taiwan Mobile Service Hub 是一個企業服務管理平台，作為 Quality Engineering 作品集專案開發。

### 2.1 技術架構（Technology Stack）

| 元件 | 技術 |
|---|---|
| 後端 | Python、FastAPI |
| 前端 | React、JavaScript |
| 建置工具 | Vite |
| ORM | SQLAlchemy 2.x |
| 資料庫 | SQLite |
| API | RESTful API |
| 單元／API 測試 | Pytest |
| 瀏覽器自動化 | Playwright |
| CI 平台 | GitHub Actions |

### 2.2 核心功能（Core Functionalities）

目前系統提供以下企業服務管理功能：

1. 查詢企業服務資料。
2. 依照服務分類及啟用狀態篩選。
3. 新增企業服務。
4. 修改既有企業服務。
5. 刪除企業服務。
6. 啟用或停用企業服務。
7. 依照服務名稱、代碼或說明搜尋服務。

## 3. 測試範圍（Testing Scope）

### 3.1 範圍內（In Scope）

**API 測試（API Testing）**

- HTTP Response Status 驗證。
- Request / Response Payload 驗證。
- 必填欄位驗證。
- 邊界值驗證。
- 重複服務代碼處理。
- 不存在資源的錯誤處理。
- Query Parameter 與篩選功能驗證。

**後端單元測試（Backend Unit Testing）**

- Transaction Commit 處理。
- Transaction Rollback 處理。
- 資料庫例外處理。
- Database Session 生命週期及資源清理。

**資料庫整合測試（Database Integration Testing）**

- SQLAlchemy ORM 操作。
- 資料庫 Unique Constraint。
- Transaction 完整性。
- 資料持久化。
- Rollback 驗證。

**前端端對端測試（Frontend End-to-End Testing）**

- 管理後台載入。
- 新增企業服務。
- 修改企業服務。
- 刪除企業服務。
- 重複服務代碼錯誤處理。
- 服務啟用／停用。
- 關鍵字搜尋。
- 重新載入頁面後的資料持久性。

**持續整合（Continuous Integration）**

- 自動執行測試。
- 後端程式碼覆蓋率驗證。
- 前端 Production Build 驗證。
- 測試報告產生。
- 測試產物保存。

### 3.2 範圍外（Out of Scope）

目前尚未納入測試範圍的項目：

- 使用者身分驗證（Authentication）。
- 權限驗證（Authorization）。
- 角色權限控制（Role-Based Access Control, RBAC）。
- 效能及負載測試（Performance / Load Testing）。
- 資訊安全滲透測試（Security Penetration Testing）。
- Chromium 以外瀏覽器的相容性測試。
- 正式環境部署驗證。
- 真正的並行負載及多程序競爭條件測試。

未來可以依照專案需求，逐步將上述項目納入測試範圍。

## 4. 測試方法（Testing Approach）

本專案採用分層式測試策略，依照不同測試目的驗證系統品質。

| 測試層級 | 使用工具 | 測試目的 |
|---|---|---|
| 單元測試（Unit Testing） | Pytest | 驗證個別業務邏輯及錯誤處理 |
| API 測試（API Testing） | Pytest + FastAPI TestClient | 驗證 REST API 行為 |
| 整合測試（Integration Testing） | Pytest + SQLAlchemy + SQLite | 驗證資料庫操作與交易完整性 |
| 端對端測試（E2E Testing） | Playwright | 驗證前端至後端的完整操作流程 |

### 4.1 測試設計技術（Test Design Techniques）

**等價類別劃分（Equivalence Partitioning）**

將輸入資料分成有效及無效的等價類別，在維持測試代表性的前提下，減少重複測試案例。

**邊界值分析（Boundary Value Analysis）**

針對欄位定義的長度限制，測試邊界值及其相鄰值。

| 欄位 | 最小長度 | 最大長度 |
|---|---:|---:|
| 服務代碼（Service Code） | 3 | 30 |
| 服務名稱（Service Name） | 1 | 150 |
| 服務說明（Description） | 1 | 2,000 |

**負向測試（Negative Testing）**

驗證系統收到不合法輸入、不存在的資源、重複資料及資料庫錯誤時，是否能正確處理。

**資料庫完整性測試（Database Integrity Testing）**

驗證資料庫約束是否能阻止不合法資料寫入，以及交易失敗時是否能避免留下部分變更。

**回歸測試（Regression Testing）**

在程式碼變更後重新執行自動化測試，確認原本已修正的缺陷沒有再次出現，並檢查是否引入非預期的行為變更。

**風險導向測試（Risk-Based Testing）**

依據商業影響、資料完整性、功能重要性及使用者影響程度，安排測試優先順序。

## 5. 測試環境（Test Environment）

### 5.1 本機測試環境（Local Environment）

| 元件 | 設定 |
|---|---|
| 作業系統 | macOS |
| Python | 3.12 |
| 後端框架 | FastAPI |
| ORM | SQLAlchemy 2.x |
| 資料庫 | SQLite |
| 前端框架 | React |
| 建置工具 | Vite |
| 測試框架 | Pytest |
| API 測試 | FastAPI TestClient |
| UI 自動化 | Playwright |
| 瀏覽器 | Chromium |

### 5.2 CI 測試環境（CI Environment）

| 元件 | 設定 |
|---|---|
| CI 平台 | GitHub Actions |
| Runner | Ubuntu Latest |
| Python | 3.12 |
| Node.js | 24 |
| 瀏覽器 | Chromium |
| 資料庫 | 獨立 SQLite 測試資料庫 |
| 覆蓋率工具 | pytest-cov |

## 6. 測試資料管理（Test Data Management）

測試資料必須與開發資料庫隔離，避免自動化測試意外修改既有資料。

目前自動化測試架構採用以下方式：

- 使用 Pytest `tmp_path` 建立暫存 API 測試資料庫。
- 使用 SQLAlchemy Session Factory 管理測試資料庫連線。
- 使用 FastAPI Dependency Overrides 替換正式資料庫依賴。
- E2E 測試使用獨立的暫存 SQLite Database。
- 每次 E2E 測試執行前清除測試資料。

自動化測試不得修改開發資料庫。

## 7. 自動化測試架構（Automation Architecture）

本專案的自動化測試分為四個層級：

```text
qa/
├── conftest.py
│
└── tests/
    ├── api/
    │   └── test_enterprise_services.py
    │
    ├── unit/
    │   ├── test_transaction.py
    │   └── test_database_dependency.py
    │
    ├── integration/
    │   └── test_transaction_integration.py
    │
    └── e2e/
        ├── conftest.py
        └── test_enterprise_services_ui.py
```

測試架構透過共用 Fixtures 及測試工具，減少重複的環境設定程式碼，提升測試程式的可維護性及擴充性。

## 8. 持續整合策略（Continuous Integration Strategy）

GitHub Actions 在以下情況自動執行品質檢查：

- 程式碼 Push 至 `main` Branch。
- 建立目標為 `main` Branch 的 Pull Request。
- 手動觸發 Workflow。

CI Pipeline 執行流程：

1. 取得 Repository 程式碼。
2. 設定 Python 及 Node.js 執行環境。
3. 安裝後端與前端依賴套件。
4. 安裝 Playwright Chromium 及其系統相依套件。
5. 執行 API、Unit、Integration 及 E2E Tests。
6. 驗證後端程式碼覆蓋率。
7. 建置 React Production Build。
8. 上傳測試報告及覆蓋率產物。

### 8.1 品質門檻（Quality Gate）

後端程式碼覆蓋率最低要求為 **90%**。

符合以下任一情況時，CI Workflow 判定為失敗：

- 任一自動化測試失敗。
- Backend Coverage 低於 90%。
- React Production Build 失敗。

程式碼覆蓋率僅用於衡量測試執行時涵蓋的程式碼，不應作為判斷測試品質的唯一指標。

## 9. 測試報告（Test Reporting）

自動化測試架構會產生以下測試證據：

| 測試產物 | 用途 |
|---|---|
| JUnit XML | 結構化的測試執行結果 |
| HTML Coverage Report | 後端原始碼覆蓋率分析 |
| Screenshot | 瀏覽器測試失敗時的畫面證據 |
| Playwright Trace | 瀏覽器操作、DOM Snapshot 及除錯歷程 |

CI 測試產物保留期限為 14 天。

## 10. 測試進入與退出條件（Entry and Exit Criteria）

### 10.1 進入條件（Entry Criteria）

- 所需的應用程式依賴套件皆可使用。
- 資料庫設定正確。
- 前端依賴套件已安裝。
- 測試資料庫可以正常初始化。
- Backend 與 Frontend Server 可以正常啟動。
- Chromium 可供 E2E 測試使用。

### 10.2 退出條件（Exit Criteria）

- 所有必要的自動化測試皆通過。
- Backend Code Coverage 至少達到 90%。
- React Production Build 成功。
- 測試範圍內沒有尚未解決的 Critical Defects。
- GitHub Actions Workflow 執行成功。
- 測試報告成功產生並上傳。

## 11. 已知限制與風險（Known Limitations and Risks）

1. 目前專案使用 SQLite，資料庫行為可能與 PostgreSQL 或其他正式環境資料庫不同。
2. Transaction Integration Test 使用不同 Session 模擬交錯執行，並不是真正的並行負載測試。
3. 目前依賴資料庫錯誤訊息判斷 IntegrityError 類型，未來更換資料庫引擎時，可能需要調整錯誤識別方式。
4. 目前 E2E 測試主要涵蓋 Chromium。
5. 使用者身分驗證、權限控制、資訊安全及效能測試尚未實作。

評估目前測試覆蓋範圍及系統品質時，應將上述限制納入考量。

## 12. 目前測試基準（Current Testing Baseline）

目前自動化測試基準如下：

| 測試類型 | 測試案例數 |
|---|---:|
| API Testing | 37 |
| Unit Testing | 4 |
| Integration Testing | 1 |
| E2E Testing | 8 |
| **總計** | **50** |

### 品質指標（Quality Metrics）

| 指標 | 結果 |
|---|---:|
| Backend Code Coverage | 93.85% |
| 最低覆蓋率門檻 | 90% |
| 本機自動化測試 | 50 Passed |
| GitHub Actions CI | 執行成功 |

### 測試基準評估（Baseline Assessment）

目前的自動化測試架構已成功驗證企業服務 CRUD 功能，測試範圍涵蓋 API、後端業務邏輯、資料庫及前端操作流程。

CI Pipeline 能自動執行回歸測試，並強制執行最低後端程式碼覆蓋率要求。

未來應逐步擴充使用者身分驗證、權限控制、效能、安全性及更多資料庫測試情境。

---

**文件負責單位：** Quality Engineering Project

**文件目的：** 建立可維護的自動化測試策略及持續品質驗證流程。