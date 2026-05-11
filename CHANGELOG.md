# CHANGELOG.md — Smart Academic Library Assistance System (SALAS)

> Assignment 10: From Class Diagrams to Code with All Creational Patterns
> Version: 1.0.0 | April 2026

---

## [1.0.0] — April 2026 — Initial Implementation

### Added — Class Implementations (`/src`)

- `src/models.py` — Full implementation of all 12 domain classes from
  CLASS_DIAGRAM.md (Assignment 9):
  - `User` — Base class with authentication, lockout after 5 failed attempts
  - `Student` — Extends User; borrowing, reservation, eligibility checks
  - `Librarian` — Extends User; catalogue management, report generation
  - `Resource` — ISBN-10/13 validation, availability tracking, deep clone
  - `Loan` — Fine calculation (R5/day capped at R200), renewal, archival
  - `Reservation` — 48-hour hold logic, queue management
  - `Fine` — Pay, waive, and borrowing-block threshold enforcement
  - `ReadingList` — Composition with Student; APA bibliography export
  - `Recommendation` — Cold-start support, feedback recording
  - `Notification` — 3-retry delivery with in-app fallback
  - `Catalogue` — Keyword search, genre/availability filtering
  - `Report` — CSV/PDF export with queue for large reports
  - All 10 business rules (BR-01 to BR-10) enforced in code

### Added — Creational Patterns (`/creational_patterns`)

- `simple_factory.py` — `UserFactory` creates Student or Librarian
  based on role string; maps to FR-01 (Registration) and FR-10 (RBAC)

- `factory_method.py` — `NotificationCreator` abstract base with four
  concrete creators (DueSoon, Overdue, ReservationConfirmed, NewArrival);
  maps to FR-07 (Automated Notifications)

- `abstract_factory.py` — `ReportExportFactory` with CSV and PDF
  families; each family produces a consistent formatter + renderer pair;
  maps to FR-08 (Usage Reporting)

- `builder.py` — `ResourceBuilder` with mandatory fields + optional
  chained setters; `ResourceDirector` with Textbook, Journal, Reference
  presets; maps to FR-06 (Catalogue Management)

- `prototype.py` — `ResourceCache` stores pre-configured Resource
  templates; `create_resource_from_prototype()` clones and customises;
  maps to FR-06 bulk import (US-014)

- `singleton.py` — Thread-safe `DatabaseConnection` using double-checked
  locking with `object.__new__()`; `reset_instance()` for test isolation;
  maps to NFR-07 (1,000 concurrent users)

### Added — Unit Tests (`/tests`)

- `tests/test_all.py` — 108 unit tests covering:
  - All 12 domain classes (97 class tests)
  - All 6 creational patterns (11 pattern tests each)
  - Edge cases: account lockout, fine threshold, ISBN validation,
    singleton thread-safety (10 threads), clone independence,
    zero-copy guard, max loan enforcement

### Test Coverage Report

| Module | Statements | Coverage |
|---|---|---|
| `src/models.py` | 503 | 87% |
| `creational_patterns/simple_factory.py` | 20 | 70% |
| `creational_patterns/factory_method.py` | 37 | 81% |
| `creational_patterns/abstract_factory.py` | 87 | 83% |
| `creational_patterns/builder.py` | 60 | 85% |
| `creational_patterns/prototype.py` | 52 | 75% |
| `creational_patterns/singleton.py` | 75 | 73% |
| **TOTAL** | **836** | **84%** |

### Bugs Fixed During Testing

- **Singleton double-init bug**: `get_instance()` was calling `__init__`
  on an already-constructed instance via `cls.__new__()`, triggering the
  guard exception. Fixed by using `object.__new__(cls)` and a private
  `_init()` method for initialisation. Linked: Issue #15

- **ISBN edge case**: Test used `0000000000` as an "invalid" ISBN but
  all-zeros passes the ISBN-10 mod-11 check (0 % 11 == 0). Fixed by
  using `1234567890` which correctly fails validation. Linked: Issue #16

### GitHub Issues Created

| Issue | Title | Status |
|---|---|---|
| #15 | Fix: Thread-safe Singleton implementation | ✅ Closed |
| #16 | Fix: ISBN test edge case with all-zero input | ✅ Closed |
| #17 | Implement all 6 creational patterns | ✅ Closed |
| #18 | Write unit tests for all patterns | ✅ Closed |
| #19 | Add coverage report to CHANGELOG | ✅ Closed |

---

## Upcoming — [1.1.0] — Sprint 2 Implementation

### Planned
- Implement REST API endpoints for FR-01, FR-02, FR-03 (US-002, US-001, US-003)
- Integrate PostgreSQL via SQLAlchemy ORM replacing in-memory models
- Add Elasticsearch client for Resource indexing (FR-02)
- Implement JWT authentication middleware (NFR-10)
- Add integration tests for borrow/return workflow

---

## [1.1.0] — April 2026 — Repository Layer (Assignment 11)

### Added — Repository Interfaces (`/repositories`)
- `repositories/interfaces.py` — Generic `Repository[T, ID]` base interface
  with CRUD + `count()` + `exists()`. Entity-specific interfaces:
  `UserRepository`, `ResourceRepository`, `LoanRepository`,
  `ReservationRepository`, `FineRepository`, `NotificationRepository`,
  `RecommendationRepository`, `ReportRepository` — each adds domain-specific
  query methods beyond basic CRUD.

### Added — In-Memory Implementations (`/repositories/inmemory`)
- `inmemory_repositories.py` — HashMap (dict) implementations of all 8
  repository interfaces. `InMemoryRepository` base class provides shared
  CRUD. All query methods use in-memory filtering with no external deps.

### Added — Future Storage Stubs (`/repositories/filesystem`)
- `filesystem_repositories.py` — `FileSystemResourceRepository` serializes
  to JSON (functional). `DatabaseResourceRepository` stub with
  `NotImplementedError` and Sprint 5 TODOs.

### Added — Repository Factory (`/factories`)
- `repository_factory.py` — `RepositoryFactory` with static methods per
  entity type. `get_all("MEMORY")` returns all 8 repos. Environment-variable
  friendly: `RepositoryFactory.get_resource_repo(os.environ.get("SALAS_STORAGE", "MEMORY"))`.

### Tests
- `tests/test_repositories.py` — 87 new tests covering all 8 repos
  (CRUD + domain queries) and RepositoryFactory (all backends, edge cases,
  filesystem integration test).

### Test Coverage (Combined Assignments 10 + 11)
| Module | Coverage |
|---|---|
| `src/models.py` | 93% |
| `repositories/inmemory/` | 98% |
| `factories/repository_factory.py` | 86% |
| `repositories/interfaces.py` | 71% (ABCs — expected) |
| **TOTAL (195 tests)** | **87%** |

### GitHub Issues Closed
- #20 Design generic Repository interface
- #21 Implement all 8 in-memory repositories
- #22 Create RepositoryFactory with MEMORY/FILESYSTEM/DATABASE backends
- #23 Write 87 repository unit tests
- #24 Add filesystem stub for future-proofing

# CHANGELOG.md — Smart Academic Library Assistance System (SALAS)

> Assignment 10: From Class Diagrams to Code with All Creational Patterns
> Version: 1.0.0 | April 2026

---

## [1.0.0] — April 2026 — Initial Implementation

### Added — Class Implementations (`/src`)

- `src/models.py` — Full implementation of all 12 domain classes from
  CLASS_DIAGRAM.md (Assignment 9):
  - `User` — Base class with authentication, lockout after 5 failed attempts
  - `Student` — Extends User; borrowing, reservation, eligibility checks
  - `Librarian` — Extends User; catalogue management, report generation
  - `Resource` — ISBN-10/13 validation, availability tracking, deep clone
  - `Loan` — Fine calculation (R5/day capped at R200), renewal, archival
  - `Reservation` — 48-hour hold logic, queue management
  - `Fine` — Pay, waive, and borrowing-block threshold enforcement
  - `ReadingList` — Composition with Student; APA bibliography export
  - `Recommendation` — Cold-start support, feedback recording
  - `Notification` — 3-retry delivery with in-app fallback
  - `Catalogue` — Keyword search, genre/availability filtering
  - `Report` — CSV/PDF export with queue for large reports
  - All 10 business rules (BR-01 to BR-10) enforced in code

### Added — Creational Patterns (`/creational_patterns`)

- `simple_factory.py` — `UserFactory` creates Student or Librarian
  based on role string; maps to FR-01 (Registration) and FR-10 (RBAC)

- `factory_method.py` — `NotificationCreator` abstract base with four
  concrete creators (DueSoon, Overdue, ReservationConfirmed, NewArrival);
  maps to FR-07 (Automated Notifications)

- `abstract_factory.py` — `ReportExportFactory` with CSV and PDF
  families; each family produces a consistent formatter + renderer pair;
  maps to FR-08 (Usage Reporting)

- `builder.py` — `ResourceBuilder` with mandatory fields + optional
  chained setters; `ResourceDirector` with Textbook, Journal, Reference
  presets; maps to FR-06 (Catalogue Management)

- `prototype.py` — `ResourceCache` stores pre-configured Resource
  templates; `create_resource_from_prototype()` clones and customises;
  maps to FR-06 bulk import (US-014)

- `singleton.py` — Thread-safe `DatabaseConnection` using double-checked
  locking with `object.__new__()`; `reset_instance()` for test isolation;
  maps to NFR-07 (1,000 concurrent users)

### Added — Unit Tests (`/tests`)

- `tests/test_all.py` — 108 unit tests covering:
  - All 12 domain classes (97 class tests)
  - All 6 creational patterns (11 pattern tests each)
  - Edge cases: account lockout, fine threshold, ISBN validation,
    singleton thread-safety (10 threads), clone independence,
    zero-copy guard, max loan enforcement

### Test Coverage Report

| Module | Statements | Coverage |
|---|---|---|
| `src/models.py` | 503 | 87% |
| `creational_patterns/simple_factory.py` | 20 | 70% |
| `creational_patterns/factory_method.py` | 37 | 81% |
| `creational_patterns/abstract_factory.py` | 87 | 83% |
| `creational_patterns/builder.py` | 60 | 85% |
| `creational_patterns/prototype.py` | 52 | 75% |
| `creational_patterns/singleton.py` | 75 | 73% |
| **TOTAL** | **836** | **84%** |

### Bugs Fixed During Testing

- **Singleton double-init bug**: `get_instance()` was calling `__init__`
  on an already-constructed instance via `cls.__new__()`, triggering the
  guard exception. Fixed by using `object.__new__(cls)` and a private
  `_init()` method for initialisation. Linked: Issue #15

- **ISBN edge case**: Test used `0000000000` as an "invalid" ISBN but
  all-zeros passes the ISBN-10 mod-11 check (0 % 11 == 0). Fixed by
  using `1234567890` which correctly fails validation. Linked: Issue #16

### GitHub Issues Created

| Issue | Title | Status |
|---|---|---|
| #15 | Fix: Thread-safe Singleton implementation | ✅ Closed |
| #16 | Fix: ISBN test edge case with all-zero input | ✅ Closed |
| #17 | Implement all 6 creational patterns | ✅ Closed |
| #18 | Write unit tests for all patterns | ✅ Closed |
| #19 | Add coverage report to CHANGELOG | ✅ Closed |

---

## Upcoming — [1.1.0] — Sprint 2 Implementation

### Planned
- Implement REST API endpoints for FR-01, FR-02, FR-03 (US-002, US-001, US-003)
- Integrate PostgreSQL via SQLAlchemy ORM replacing in-memory models
- Add Elasticsearch client for Resource indexing (FR-02)
- Implement JWT authentication middleware (NFR-10)
- Add integration tests for borrow/return workflow

---

## [1.1.0] — April 2026 — Repository Layer (Assignment 11)

### Added — Repository Interfaces (`/repositories`)
- `repositories/interfaces.py` — Generic `Repository[T, ID]` base interface
  with CRUD + `count()` + `exists()`. Entity-specific interfaces:
  `UserRepository`, `ResourceRepository`, `LoanRepository`,
  `ReservationRepository`, `FineRepository`, `NotificationRepository`,
  `RecommendationRepository`, `ReportRepository` — each adds domain-specific
  query methods beyond basic CRUD.

### Added — In-Memory Implementations (`/repositories/inmemory`)
- `inmemory_repositories.py` — HashMap (dict) implementations of all 8
  repository interfaces. `InMemoryRepository` base class provides shared
  CRUD. All query methods use in-memory filtering with no external deps.

### Added — Future Storage Stubs (`/repositories/filesystem`)
- `filesystem_repositories.py` — `FileSystemResourceRepository` serializes
  to JSON (functional). `DatabaseResourceRepository` stub with
  `NotImplementedError` and Sprint 5 TODOs.

### Added — Repository Factory (`/factories`)
- `repository_factory.py` — `RepositoryFactory` with static methods per
  entity type. `get_all("MEMORY")` returns all 8 repos. Environment-variable
  friendly: `RepositoryFactory.get_resource_repo(os.environ.get("SALAS_STORAGE", "MEMORY"))`.

### Tests
- `tests/test_repositories.py` — 87 new tests covering all 8 repos
  (CRUD + domain queries) and RepositoryFactory (all backends, edge cases,
  filesystem integration test).

### Test Coverage (Combined Assignments 10 + 11)
| Module | Coverage |
|---|---|
| `src/models.py` | 93% |
| `repositories/inmemory/` | 98% |
| `factories/repository_factory.py` | 86% |
| `repositories/interfaces.py` | 71% (ABCs — expected) |
| **TOTAL (195 tests)** | **87%** |

### GitHub Issues Closed
- #20 Design generic Repository interface
- #21 Implement all 8 in-memory repositories
- #22 Create RepositoryFactory with MEMORY/FILESYSTEM/DATABASE backends
- #23 Write 87 repository unit tests
- #24 Add filesystem stub for future-proofing

---

## [1.2.0] — May 2026 — Service Layer and REST API (Assignment 12)

### Added — Service Layer (`/services`)
- `services/user_service.py` — UserService: register student/librarian,
  login with lockout (BR-06), update profile, deactivate (POPIA NFR-11),
  delete, find by email/role. Maps to FR-01, FR-10.
- `services/resource_service.py` — ResourceService: add (ISBN validated
  BR-05, copies >= 1), search, filter by genre/availability, update,
  delete (blocked by active loans BR-04), check_availability. Maps to
  FR-02, FR-06.
- `services/loan_service.py` — LoanService: checkout (BR-01 max 5 loans,
  BR-02 fine threshold), return (BR-10 fine calculation), renew (BR-09),
  overdue queries, fine summary. Maps to FR-03, FR-04, FR-07.

### Added — REST API (`/api`)
- `api/main.py` — FastAPI application with 19 endpoints across 3 entity
  groups (Users, Resources, Loans). Auto-generates Swagger UI at /docs
  and OpenAPI JSON at /openapi.json.
- Full Pydantic request/response models with validation.
- Proper HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 409.

### Added — API Documentation (`/docs`)
- `docs/openapi.md` — Full endpoint reference, request/response examples,
  error codes, and business rule mapping.

### Tests
- `tests/services/test_services.py` — 55 service unit tests
- `tests/api/test_api.py` — 39 API integration tests (FastAPI TestClient)
- **Total: 94 new tests | All passing | Grand total: 289 tests**

### GitHub Issues Closed
- #25 Implement UserService with auth and RBAC
- #26 Implement ResourceService with ISBN validation
- #27 Implement LoanService with BR-01/BR-02/BR-10 enforcement
- #28 Build FastAPI REST API with 19 endpoints
- #29 Write 94 service and API tests
- #30 Document API with OpenAPI/Swagger

[CHANGELOG.md](https://github.com/user-attachments/files/27609319/CHANGELOG.md)

