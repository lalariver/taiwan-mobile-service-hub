# Test Cases

**Project:** Taiwan Mobile Service Hub
**Document:** Test Cases
**Version:** 1.0
**Last Updated:** 2026-11-08
**Verified Commit:** `32d5c99`

## 1. Test Overview

This document defines the 50 automated test cases implemented in the QA test suite.

| Test Level | Test Cases | Scope |
|---|---:|---|
| API Testing | 37 | CRUD operations, input validation, HTTP error handling |
| Unit Testing | 4 | Transaction handling and database session lifecycle |
| Integration Testing | 1 | Transaction rollback across multiple database sessions |
| E2E Testing | 8 | Enterprise service management UI workflows |
| **Total** | **50** | |

## 2. Test Environment and Preconditions

### 2.1 API Test Environment

- Python 3.12
- FastAPI TestClient
- SQLAlchemy
- SQLite
- Pytest
- Each test uses an isolated temporary SQLite database.
- FastAPI's `get_db` dependency is overridden to use the test database.

### 2.2 Test Data

Default service payload:

| Field | Value |
|---|---|
| code | `QA-TEST-001` |
| name | `QA Test Service` |
| category | `connectivity` |
| description | `Test service for automation testing.` |
| is_active | `true` |

### 2.3 General Preconditions

- The application and test dependencies are installed.
- Database fixtures are initialized successfully.
- API tests use an isolated test database.
- E2E tests use the dedicated E2E environment and test database.
- Each test starts with its own isolated test data.

## 3. API Test Cases

### 3.1 GET — Retrieve Enterprise Services

| ID | Scenario / Test Data | Expected Result | Pytest Function |
|---|---|---|---|
| API-001 | Retrieve services when no records exist. | HTTP 200; response is an empty list. | `test_list_enterprise_services_returns_empty_list` |
| API-002 | Create two services and retrieve the list. | HTTP 200; two records returned. | `test_list_enterprise_services_returns_all_records` |
| API-003 | Filter services by `category=connectivity`. | HTTP 200; only matching category is returned. | `test_list_services_by_category` |
| API-004 | Filter services by `is_active=true`. | HTTP 200; only active services are returned. | `test_list_services_by_active_status` |
| API-005 | Filter by category and active status simultaneously. | HTTP 200; only records matching both conditions are returned. | `test_list_services_by_multiple_filters` |
| API-006 | Retrieve an existing service by ID. | HTTP 200; returned service code matches the created record. | `test_get_existing_enterprise_service` |
| API-007 | Retrieve a nonexistent service using ID `9999`. | HTTP 404. | `test_get_nonexistent_service_returns_404` |

### 3.2 POST — Create Enterprise Services

| ID | Scenario / Test Data | Expected Result | Pytest Function |
|---|---|---|---|
| API-008 | Create a service using the default valid payload. | HTTP 201; returned code and name match the request; active status is true; generated ID is positive. | `test_create_enterprise_service` |
| API-009 | Create a service without `is_active`. | HTTP 201; `is_active` defaults to true. | `test_create_service_with_default_active_status` |
| API-010 | Submit the same service code twice. | First request returns HTTP 201; second request returns HTTP 409. | `test_create_duplicate_service_code_returns_409` |
| API-011 | Code length: 2 characters (`AB`). | HTTP 422. | `test_service_code_length_boundaries` |
| API-012 | Code length: 3 characters (`ABC`). | HTTP 201. | `test_service_code_length_boundaries` |
| API-013 | Code length: 30 characters. | HTTP 201. | `test_service_code_length_boundaries` |
| API-014 | Code length: 31 characters. | HTTP 422. | `test_service_code_length_boundaries` |
| API-015 | Invalid code format: `abc-001`. | HTTP 422. | `test_create_service_with_invalid_code_format` |
| API-016 | Invalid code format: `A--001`. | HTTP 422. | `test_create_service_with_invalid_code_format` |
| API-017 | Invalid code format: `-ABC`. | HTTP 422. | `test_create_service_with_invalid_code_format` |
| API-018 | Invalid code format: `ABC-`. | HTTP 422. | `test_create_service_with_invalid_code_format` |
| API-019 | Invalid code format: `ABC_001`. | HTTP 422. | `test_create_service_with_invalid_code_format` |
| API-020 | Name is an empty string. | HTTP 422. | `test_service_name_length_boundaries` |
| API-021 | Name contains 1 character. | HTTP 201. | `test_service_name_length_boundaries` |
| API-022 | Name contains 150 characters. | HTTP 201. | `test_service_name_length_boundaries` |
| API-023 | Name contains 151 characters. | HTTP 422. | `test_service_name_length_boundaries` |
| API-024 | Description is an empty string. | HTTP 422. | `test_service_description_length_boundaries` |
| API-025 | Description contains 1 character. | HTTP 201. | `test_service_description_length_boundaries` |
| API-026 | Description contains 2,000 characters. | HTTP 201. | `test_service_description_length_boundaries` |
| API-027 | Description contains 2,001 characters. | HTTP 422. | `test_service_description_length_boundaries` |
| API-028 | Submit an unsupported category: `invalid_category`. | HTTP 422. | `test_create_service_with_invalid_category_returns_422` |
| API-029 | Omit the required `description` field. | HTTP 422. | `test_create_service_without_required_field_returns_422` |

### 3.3 PUT — Update Enterprise Services

| ID | Scenario / Test Data | Expected Result | Pytest Function |
|---|---|---|---|
| API-030 | Update an existing service name to `Updated QA Service`. | HTTP 200; response contains the updated name. | `test_update_enterprise_service` |
| API-031 | Update a service and query the database directly. | HTTP 200; database record contains the updated name. | `test_update_service_persists_record` |
| API-032 | Update a service without the required `description` field. | HTTP 422. | `test_update_service_without_required_field_returns_422` |
| API-033 | Update a nonexistent service using ID `9999`. | HTTP 404. | `test_update_nonexistent_service_returns_404` |
| API-034 | Update a service using a code already assigned to another record. | HTTP 409. | `test_update_service_with_duplicate_code_returns_409` |

### 3.4 DELETE — Delete Enterprise Services

| ID | Scenario / Test Data | Expected Result | Pytest Function |
|---|---|---|---|
| API-035 | Delete an existing service. | HTTP 204; response body is empty; subsequent GET returns HTTP 404. | `test_delete_enterprise_service` |
| API-036 | Delete a service and query the database directly. | HTTP 204; database record no longer exists. | `test_delete_service_persists_removal` |
| API-037 | Delete a nonexistent service using ID `9999`. | HTTP 404. | `test_delete_nonexistent_service_returns_404` |

## 4. Unit Test Cases

| ID | Scenario | Expected Result | Pytest Function |
|---|---|---|---|
| UNIT-001 | `commit()` raises a UNIQUE constraint `IntegrityError` for a duplicate service code. | HTTP 409 is raised; `commit()` and `rollback()` are each called once. | `test_commit_transaction_rolls_back_on_duplicate_code` |
| UNIT-002 | `commit()` raises a NOT NULL constraint `IntegrityError`. | Original `IntegrityError` is re-raised; rollback is called once. | `test_commit_transaction_rolls_back_on_other_integrity_error` |
| UNIT-003 | `commit()` raises an unexpected `RuntimeError`. | Original `RuntimeError` is re-raised; rollback is called once. | `test_commit_transaction_rolls_back_on_unexpected_error` |
| UNIT-004 | Execute the `get_db()` generator until completion. | The yielded session is the mocked session; `close()` is called once. | `test_get_db_closes_session` |

## 5. Integration Test Cases

| ID | Scenario | Expected Result | Pytest Function |
|---|---|---|---|
| INT-001 | Two independent database sessions validate the same service code. Session A inserts and commits the code. Session B inserts a valid record and a duplicate record, then attempts to commit. | Session B receives HTTP 409 and rolls back the entire transaction. A new session confirms that only Session A's record remains; Session B's otherwise-valid pending record is also absent. | `test_unique_constraint_rolls_back_all_pending_changes` |

**Test objective:** Verify transaction atomicity. All pending changes within the failed transaction must be rolled back.

**Limitation:** This test simulates a uniqueness conflict using two independent sessions and sequential commits. It is not a concurrent load or stress test.

## 6. End-to-End Test Cases

| ID | Scenario | Expected Result | Pytest Function |
|---|---|---|---|
| E2E-001 | Open the enterprise service management dashboard. | Dashboard headings are visible and the empty-state message is displayed. | `test_dashboard_loads_successfully` |
| E2E-002 | Create a service through the UI. | The new service appears in the table with the correct code, name, and active status. | `test_create_enterprise_service` |
| E2E-003 | Edit an existing service name. | The table displays the updated service name. | `test_update_enterprise_service` |
| E2E-004 | Delete an existing service. | A confirmation dialog appears with the expected message; the service row is removed after confirmation. | `test_delete_enterprise_service` |
| E2E-005 | Attempt to create a service using an existing code. | The UI displays the API duplicate-code error message. | `test_duplicate_service_code_displays_error` |
| E2E-006 | Disable and then re-enable a service. | The UI status changes from active to inactive and back to active. | `test_toggle_enterprise_service_status` |
| E2E-007 | Search for `Network Service` after creating two services. | The matching row remains visible; the nonmatching row is removed from the displayed results. | `test_search_enterprise_services` |
| E2E-008 | Create a service and reload the page. | The created service remains visible after reload. | `test_service_persists_after_page_reload` |

## 7. Requirements Traceability Matrix

The following functional requirement groups are derived from the implemented application behavior and test coverage. They are not a substitute for a separately approved business requirements specification.

| Requirement ID | Functional Requirement | Related Test Cases |
|---|---|---|
| FR-01 | Retrieve and filter enterprise services. | API-001 to API-007, E2E-001, E2E-007 |
| FR-02 | Create enterprise services. | API-008 to API-029, E2E-002 |
| FR-03 | Update enterprise services. | API-030 to API-034, E2E-003 |
| FR-04 | Delete enterprise services. | API-035 to API-037, E2E-004 |
| FR-05 | Enforce service code uniqueness and handle conflicts. | API-010, API-034, UNIT-001, UNIT-002, INT-001, E2E-005 |
| FR-06 | Validate service input fields and boundaries. | API-011 to API-029 |
| FR-07 | Manage service activation status. | API-004, API-005, API-008, API-009, E2E-002, E2E-006 |
| FR-08 | Persist service changes in the database. | API-031, API-036, INT-001, E2E-008 |
| FR-09 | Manage database transaction and session lifecycle. | UNIT-001 to UNIT-004, INT-001 |

## 8. Test Execution

Run all tests:

```bash
./.venv/bin/python -m pytest -v qa/tests
```

Collect test cases without executing them:

```bash
./.venv/bin/python -m pytest --collect-only -vv qa/tests
```

Run tests with coverage:

```bash
./.venv/bin/python -m pytest -v qa/tests \
  --cov=backend \
  --cov-branch \
  --cov-fail-under=90 \
  --cov-report=term-missing
```

## 9. Test Results Baseline

Verified baseline:

| Metric | Result |
|---|---:|
| Total collected tests | 50 |
| API tests | 37 |
| Unit tests | 4 |
| Integration tests | 1 |
| E2E tests | 8 |
| Backend coverage | 93.85% |
| Coverage threshold | 90% |
| Local test execution | 50 passed |

**Verified commit:** `32d5c99`

## 10. Known Limitations

- Authentication and role-based access control are not covered.
- Security and penetration testing are not covered.
- Performance and load testing are not covered.
- E2E browser coverage is limited to Chromium.
- Integration testing does not simulate concurrent load.
- Database-specific error handling currently reflects SQLite behavior.
- The requirements traceability matrix is derived from implemented functionality; formal business requirement approval is outside this document's scope.