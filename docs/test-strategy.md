# QA Test Strategy
## Taiwan Mobile Service Hub

[繁體中文版](./test-strategy.zh-TW.md)

**Document Version:** 1.0  
**Last Updated:** November 8, 2026  
**Project:** Taiwan Mobile Service Hub  
**Testing Framework:** Pytest + Playwright  
**Status:** Active

---

## 1. Purpose

This document defines the overall testing strategy for the Taiwan Mobile Service Hub project.

The primary objective is to establish a maintainable and reliable automation framework that validates backend APIs, business logic, database operations, and frontend administrative workflows.

The strategy focuses on identifying defects early, preventing regressions, and providing confidence in software releases through continuous integration.

## 2. System Under Test (SUT)

The Taiwan Mobile Service Hub is an enterprise service management platform.

The application consists of:

- **Backend:** Python, FastAPI, SQLAlchemy.
- **Frontend:** React and Vite.
- **Database:** SQLite.
- **API:** RESTful Enterprise Service Management APIs.

### Core Functionalities

1. Retrieve enterprise service records.
2. Filter services by category and active status.
3. Create enterprise services.
4. Update existing enterprise services.
5. Delete enterprise services.
6. Enable or disable enterprise services.

## 3. Testing Scope

### 3.1 In Scope

**API Testing**
- HTTP response status validation.
- Request payload validation.
- Required field validation.
- Boundary value validation.
- Duplicate service code handling.
- Invalid resource handling.
- Filtering and query parameters.

**Backend Unit Testing**
- Transaction commit handling.
- Transaction rollback handling.
- Database exception handling.
- Database session cleanup.

**Database Integration Testing**
- SQLAlchemy ORM operations.
- Database unique constraints.
- Transaction integrity.
- Data persistence.
- Rollback verification.

**Frontend E2E Testing**
- Dashboard loading.
- Creating enterprise services.
- Updating enterprise services.
- Deleting enterprise services.
- Duplicate code error handling.
- Service status toggling.
- Keyword searching.
- Data persistence after page reload.

**CI Automation**
- Automated test execution.
- Code coverage validation.
- Frontend production build.
- Test report generation.
- Test artifact storage.

### 3.2 Out of Scope

The following areas are not currently covered:

- Authentication and role-based access control.
- Performance and load testing.
- Security penetration testing.
- Cross-browser compatibility beyond Chromium.
- Production deployment validation.
- True concurrent load and multi-process race condition testing.

These areas may be included in future testing phases.

## 4. Testing Approach

The project uses a layered testing strategy.

| Test Level | Framework | Purpose |
|---|---|---|
| Unit Testing | Pytest | Validate individual business logic and error handling |
| API Testing | Pytest + FastAPI TestClient | Validate REST API behavior |
| Integration Testing | Pytest + SQLAlchemy + SQLite | Validate database operations and transaction integrity |
| E2E Testing | Playwright | Validate complete frontend-to-backend workflows |

### 4.1 Test Design Techniques

**Equivalence Partitioning**

Divide input data into valid and invalid groups to reduce redundant test cases.

**Boundary Value Analysis**

Test values around the defined field constraints.

| Field | Minimum | Maximum |
|---|---:|---:|
| Service Code | 3 | 30 |
| Service Name | 1 | 150 |
| Description | 1 | 2,000 |

**Negative Testing**

Validate how the system handles invalid inputs, missing resources, duplicate data, and database errors.

**Database Integrity Testing**

Verify that database constraints prevent invalid data and that failed transactions do not leave partial changes.

**Regression Testing**

Execute the automated test suite after code changes to detect previously fixed defects or unexpected behavior changes.

## 5. Test Environment

### Local Environment

| Component | Technology |
|---|---|
| Operating System | macOS |
| Python | 3.12 |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | SQLite |
| Frontend | React |
| Build Tool | Vite |
| Test Framework | Pytest |
| API Testing | FastAPI TestClient |
| UI Automation | Playwright |
| Browser | Chromium |

### CI Environment

| Component | Configuration |
|---|---|
| CI Platform | GitHub Actions |
| Runner | Ubuntu Latest |
| Python | 3.12 |
| Node.js | 24 |
| Browser | Chromium |
| Database | Isolated SQLite |
| Coverage Tool | pytest-cov |

## 6. Test Data Management

Test data must be isolated from the development database.

The framework uses:

- Pytest `tmp_path` for temporary API test databases.
- SQLAlchemy Session Factory for test database connections.
- FastAPI Dependency Overrides for API test isolation.
- A separate temporary SQLite database for E2E testing.
- Database cleanup before each E2E test.

The development database must never be modified by automated tests.

## 7. Automation Architecture

The automation framework is organized into four test layers:

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

The framework uses shared fixtures and test utilities to reduce duplicated setup code and improve maintainability.

## 8. Continuous Integration Strategy

GitHub Actions executes automated quality checks when:

- Code is pushed to the `main` branch.
- A Pull Request targets the `main` branch.
- A workflow is triggered manually.

The CI pipeline performs:

1. Repository checkout.
2. Python and Node.js environment setup.
3. Dependency installation.
4. Playwright Chromium installation.
5. Automated test execution.
6. Backend coverage validation.
7. React production build.
8. Test report artifact upload.

### Quality Gate

The minimum required backend code coverage is **90%**.

A CI run fails when the coverage threshold is not achieved or when an automated test fails.

Code coverage is used as a measurement of executed code, not as the sole indicator of test quality.

## 9. Test Reporting

The framework produces the following test evidence:

| Artifact | Purpose |
|---|---|
| JUnit XML | Structured test execution results |
| HTML Coverage Report | Source code coverage analysis |
| Screenshots | Visual evidence of browser test failures |
| Playwright Trace | Browser action and debugging history |

CI artifacts are retained for 14 days.

## 10. Entry and Exit Criteria

### Entry Criteria

- Required application dependencies are available.
- Database configuration is valid.
- Frontend dependencies are installed.
- Test environments can be initialized.
- Backend and frontend services can start successfully.

### Exit Criteria

- All required automated tests pass.
- Backend code coverage is at least 90%.
- React production build succeeds.
- No unresolved critical defects remain in the tested scope.
- CI workflow completes successfully.
- Test reports are generated and uploaded.

## 11. Known Limitations and Risks

1. The current project uses SQLite. Database behavior may differ from PostgreSQL or other production databases.
2. The transaction integration test simulates interleaved operations using separate sessions; it is not a true concurrent load test.
3. Database-specific IntegrityError message handling may require adaptation when changing database engines.
4. Current E2E coverage focuses on Chromium.
5. Authentication, authorization, security, and performance testing have not yet been implemented.

These limitations should be considered when evaluating the current test coverage.

## 12. Current Testing Baseline

The initial automation baseline is:

| Test Type | Test Cases |
|---|---:|
| API Testing | 37 |
| Unit Testing | 4 |
| Integration Testing | 1 |
| E2E Testing | 8 |
| **Total** | **50** |

**Backend Code Coverage:** 93.85%  
**Minimum Coverage Threshold:** 90%  
**Local Test Status:** 50 Passed  
**GitHub Actions CI:** Successful

---

**Document Owner:** Quality Engineering Project  
**Purpose:** Establish a maintainable automated testing strategy and continuous quality validation process.

