# QA Test Plan
## Taiwan Mobile Service Hub

[繁體中文版](./test-plan.zh-TW.md) | [Test Strategy](./test-strategy.md)

| Document Information | Details |
|---|---|
| Project | Taiwan Mobile Service Hub |
| Document Version | 1.0 |
| Last Updated | November 8, 2026 |
| Test Framework | Pytest + Playwright |
| Test Scope | API, Unit, Integration, E2E |
| Status | Active |
| Baseline Commit | `32d5c99` |

---

## 1. Test Objectives

The objective of this test plan is to verify the functional correctness, data integrity, and reliability of the Taiwan Mobile Service Hub.

The testing activities aim to:

1. Verify that enterprise service APIs behave according to specifications.
2. Validate backend business logic and exception handling.
3. Ensure database operations maintain data integrity.
4. Validate complete user workflows through the React administrative interface.
5. Prevent regression defects through automated testing.
6. Integrate automated quality checks into the CI pipeline.

## 2. Test Scope

### 2.1 Functional Scope

The following functionalities are included in the current test cycle:

| Module | Functionality | Priority |
|---|---|---|
| Enterprise Services | Retrieve service list | High |
| Enterprise Services | Filter by category | Medium |
| Enterprise Services | Filter by active status | Medium |
| Enterprise Services | Create service | High |
| Enterprise Services | Update service | High |
| Enterprise Services | Delete service | High |
| Enterprise Services | Enable / Disable service | Medium |
| Enterprise Services | Search services | Medium |
| Database | Unique constraint validation | High |
| Database | Transaction rollback | High |
| Database | Session cleanup | Medium |

### 2.2 Non-Functional Scope

The current test cycle also verifies:

- Database isolation between test and development environments.
- Automated test execution stability.
- Backend code coverage threshold.
- Frontend production build success.
- Test report generation and artifact retention.

Performance, security, and cross-browser compatibility testing are not included in this cycle.

## 3. Test Levels and Execution Plan

### 3.1 Unit Testing

**Framework:** Pytest

**Test Location:** `qa/tests/unit/`

**Objective:** Verify individual backend functions without relying on external systems or a real production database.

Test coverage includes:

| Test Area | Validation |
|---|---|
| Transaction Commit | Verify successful commit behavior |
| Transaction Rollback | Verify rollback after database errors |
| IntegrityError Handling | Verify duplicate constraint error handling |
| Database Session | Verify session cleanup |

**Expected Test Cases:** 4

### 3.2 API Testing

**Framework:** Pytest + FastAPI TestClient

**Test Location:** `qa/tests/api/`

**Objective:** Verify REST API behavior, request validation, response status codes, and business rules.

Test coverage includes:

| Test Area | Validation |
|---|---|
| GET | Retrieve service records |
| GET | Query filtering |
| GET | Retrieve existing and nonexistent records |
| POST | Create valid service records |
| POST | Duplicate service code |
| POST | Field validation |
| POST | Boundary value validation |
| PUT | Update existing service records |
| PUT | Invalid update requests |
| DELETE | Delete existing service records |
| DELETE | Delete nonexistent records |

**Expected Test Cases:** 37

### 3.3 Database Integration Testing

**Framework:** Pytest + SQLAlchemy + SQLite

**Test Location:** `qa/tests/integration/`

**Objective:** Verify interactions between application services, repositories, SQLAlchemy sessions, and database constraints.

Test coverage includes:

- Database UNIQUE constraint enforcement.
- Transaction commit behavior.
- IntegrityError handling.
- Transaction rollback.
- Persistence of committed records.
- Removal of uncommitted changes after rollback.

**Expected Test Cases:** 1

The current integration test uses two separate database sessions to simulate interleaved operations. It does not represent a real multi-threaded load test.

### 3.4 End-to-End Testing

**Framework:** Playwright Python

**Test Location:** `qa/tests/e2e/`

**Browser:** Chromium

**Objective:** Validate complete user workflows through the React administrative interface.

| ID | Test Scenario | Expected Result |
|---|---|---|
| UI-001 | Dashboard loading | Dashboard displays correctly |
| UI-002 | Create enterprise service | New service appears in the list |
| UI-003 | Update enterprise service | Updated information is displayed |
| UI-004 | Delete enterprise service | Deleted service disappears |
| UI-005 | Duplicate service code | Error message is displayed |
| UI-006 | Toggle service status | Service status is updated |
| UI-007 | Search enterprise services | Matching records are displayed |
| UI-008 | Reload page | Previously created data remains available |

**Expected Test Cases:** 8

## 4. Test Environment and Configuration

### 4.1 Local Environment

| Component | Configuration |
|---|---|
| Operating System | macOS |
| Python | 3.12 |
| Backend | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | SQLite |
| Frontend | React |
| Build Tool | Vite |
| Test Framework | Pytest |
| Browser Automation | Playwright |
| Browser | Chromium |

### 4.2 CI Environment

| Component | Configuration |
|---|---|
| Platform | GitHub Actions |
| Runner | Ubuntu Latest |
| Python | 3.12 |
| Node.js | 24 |
| Browser | Chromium |
| Test Database | Temporary SQLite |
| Coverage Tool | pytest-cov |

### 4.3 Service Configuration

| Service | Address |
|---|---|
| FastAPI | `http://127.0.0.1:8000` |
| React / Vite | `http://127.0.0.1:5173` |
| Swagger UI | `http://127.0.0.1:8000/docs` |

## 5. Test Data Management

Test data must be isolated from the development database.

The test framework uses different isolation mechanisms for API and E2E testing.

**API Testing**

- Use Pytest `tmp_path` to create a temporary SQLite database.
- Create a dedicated SQLAlchemy Engine.
- Override FastAPI's `get_db` dependency.
- Create a separate database session for each API request.
- Remove temporary database tables after the test.

**E2E Testing**

- Create a separate temporary SQLite database for the E2E server.
- Configure the backend using the `DATABASE_PATH` environment variable.
- Initialize the test database before starting FastAPI.
- Clear test records before each E2E test.
- Stop backend and frontend processes after the test session.

The development database `taiwan_mobile.db` must remain unchanged during automated testing.

## 6. Test Execution Schedule

Testing is organized into the following execution stages.

| Stage | Activity | Deliverable |
|---|---|---|
| 1 | Verify dependencies and test environment | Ready test environment |
| 2 | Execute unit tests | Unit test results |
| 3 | Execute API tests | API test results |
| 4 | Execute database integration tests | Database integrity results |
| 5 | Start backend and frontend services | Running E2E environment |
| 6 | Execute Playwright tests | UI test results |
| 7 | Generate coverage and test reports | Test reports |
| 8 | Execute frontend production build | Build result |
| 9 | Validate CI pipeline | CI execution result |

The CI pipeline performs these operations automatically.

## 7. Test Execution Commands

### 7.1 Execute All Tests

```bash
python -m pytest -v qa/tests
```

### 7.2 Execute API Tests

```bash
python -m pytest -v qa/tests/api
```

### 7.3 Execute Unit Tests

```bash
python -m pytest -v qa/tests/unit
```

### 7.4 Execute Integration Tests

```bash
python -m pytest -v qa/tests/integration
```

### 7.5 Execute E2E Tests

```bash
python -m pytest -v qa/tests/e2e
```

### 7.6 Execute Coverage Analysis

```bash
python -m pytest -v qa/tests \
    --cov=backend \
    --cov-branch \
    --cov-fail-under=90 \
    --cov-report=term-missing \
    --cov-report=html
```

### 7.7 Build Frontend

```bash
cd frontend
npm ci
npm run build
```

## 8. Defect Management

All identified defects should be documented with sufficient information for reproduction and investigation.

Each bug report should include:

- Bug ID.
- Title.
- Environment.
- Preconditions.
- Steps to reproduce.
- Expected result.
- Actual result.
- Severity.
- Priority.
- Supporting evidence.
- Root cause, when identified.
- Fix verification result.

### Severity Classification

| Severity | Description |
|---|---|
| Critical | Causes severe data corruption or system-wide failure |
| High | Breaks a major business function |
| Medium | Causes partial functional failure |
| Low | Minor functional or visual issue |

### Defect Lifecycle

1. Identify the issue.
2. Reproduce the behavior.
3. Document the defect.
4. Analyze the root cause.
5. Implement a fix.
6. Retest the affected functionality.
7. Execute regression tests.

Only confirmed defects should be recorded as actual bugs. Unverified risks should be documented separately.

## 9. Entry Criteria

Testing can begin when:

- Backend dependencies are installed.
- Frontend dependencies are available.
- Database configuration is valid.
- Test database initialization succeeds.
- Backend and frontend services can start successfully.
- Playwright Chromium is installed.
- Test code is available.

## 10. Exit Criteria

The current test cycle is considered successful when:

1. All required automated tests pass.
2. Backend statement coverage is at least 90%.
3. The React production build succeeds.
4. No unresolved critical defects remain within the tested scope.
5. GitHub Actions completes successfully.
6. Test reports are generated and uploaded.

## 11. Test Deliverables

| Deliverable | Location |
|---|---|
| Test Strategy | `docs/test-strategy.md` |
| Test Plan | `docs/test-plan.md` |
| API Test Cases | `qa/tests/api/` |
| Unit Test Cases | `qa/tests/unit/` |
| Integration Test Cases | `qa/tests/integration/` |
| E2E Test Cases | `qa/tests/e2e/` |
| Bug Reports | `docs/bug-reports/` |
| JUnit XML | `qa/.artifacts/` |
| HTML Coverage | `htmlcov/` |
| CI Workflow | `.github/workflows/ci.yml` |

## 12. Baseline Execution Results

The initial verified test baseline is:

| Test Level | Cases | Result |
|---|---:|---|
| API Testing | 37 | Passed |
| Unit Testing | 4 | Passed |
| Integration Testing | 1 | Passed |
| E2E Testing | 8 | Passed |
| **Total** | **50** | **Passed** |

### Quality Metrics

| Metric | Result |
|---|---:|
| Backend Coverage | 93.85% |
| Minimum Coverage Gate | 90% |
| Local Automated Tests | 50 Passed |
| GitHub Actions CI | Successful |
| React Production Build | Successful |

These results represent the verified baseline associated with the initial CI implementation. Future test runs should be evaluated independently rather than assuming these results guarantee subsequent releases.

---

**Document Owner:** Quality Engineering Project

**Purpose:** Define the testing scope, environment, execution process, acceptance criteria, and deliverables for the Taiwan Mobile Service Hub project.