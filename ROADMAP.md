[ROADMAP.md](https://github.com/user-attachments/files/28105468/ROADMAP.md)
# ROADMAP.md — SALAS Development Roadmap
## Smart Academic Library Assistance System

> This roadmap outlines planned features and improvements for future
> sprints. Items are prioritised using MoSCoW (Must/Should/Could/Won't).
> Contributors are welcome to pick up any item labelled `good-first-issue`
> or `feature-request` in the Issues tab.

---

## Current Status (v1.0 — Assignments 3–14)

| Component | Status |
|---|---|
| Domain model (12 classes) | ✅ Complete |
| 6 Creational design patterns | ✅ Complete |
| Repository layer (8 repos, 3 backends) | ✅ Complete |
| Service layer (User, Resource, Loan) | ✅ Complete |
| FastAPI REST API (19 endpoints) | ✅ Complete |
| CI/CD pipeline (GitHub Actions) | ✅ Complete |
| In-memory storage | ✅ Complete |
| 289 unit and integration tests | ✅ Complete |

---

## Sprint 2 — Core Borrowing Workflows (Must-Have)

These features are required for the system to replace the manual
library process completely.

### Feature 1: Reservation Management API
**Issue label:** `good-first-issue`
Add REST endpoints for the Reservation entity:
```
POST   /api/reservations              — Place a reservation
GET    /api/reservations/{id}         — Get reservation details
DELETE /api/reservations/{id}         — Cancel a reservation
GET    /api/students/{id}/reservations — Get student reservations
```
**Files to modify:** `api/main.py`, `services/` (add ReservationService)
**Tests required:** `tests/api/test_api.py`, `tests/services/`

---

### Feature 2: Fine Management API
**Issue label:** `good-first-issue`
Add REST endpoints for Fine operations:
```
GET  /api/fines/{student_id}    — Get all fines for a student
POST /api/fines/{fine_id}/pay   — Pay a fine
POST /api/fines/{fine_id}/waive — Waive a fine (librarian only)
```
**Files to modify:** `api/main.py`, add `services/fine_service.py`
**Tests required:** Full test coverage for FineService

---

### Feature 3: PostgreSQL Database Backend
**Issue label:** `feature-request`
Replace the in-memory HashMap storage with a real PostgreSQL database
using SQLAlchemy ORM.
- Add `DatabaseResourceRepository` implementation
- Add `DatabaseUserRepository` implementation
- Add `DatabaseLoanRepository` implementation
- Update `RepositoryFactory` to return DB repos when `DATABASE` is selected
- Add database migration scripts (Alembic)

**Dependencies:** `sqlalchemy`, `alembic`, `psycopg2-binary`

---

### Feature 4: JWT Authentication Middleware
**Issue label:** `feature-request`
Implement proper JWT token authentication on the API:
- Issue JWT on login (`POST /api/users/login`)
- Validate JWT on all protected endpoints
- Implement token refresh endpoint (`POST /api/auth/refresh`)
- Add role-based route protection (student vs librarian vs admin)

**Dependencies:** `python-jose`, `passlib`

---

## Sprint 3 — Search and Recommendations (Should-Have)

### Feature 5: Elasticsearch Integration
**Issue label:** `feature-request`
Replace the in-memory keyword search with Elasticsearch for full-text
search with ranking:
- Set up Elasticsearch client
- Add `ElasticsearchResourceRepository`
- Implement relevance scoring and fuzzy matching
- Index resources automatically on save

**Dependencies:** `elasticsearch-py`

---

### Feature 6: Recommendation Engine (Basic)
**Issue label:** `feature-request`
Implement a basic collaborative filtering recommendation system:
- Track student borrowing history
- Generate "Students who borrowed X also borrowed Y" recommendations
- Expose via `GET /api/students/{id}/recommendations`
- Implement cold-start: course-based defaults for new students

**Dependencies:** `scikit-learn`, `numpy`

---

### Feature 7: Redis Caching Layer
**Issue label:** `feature-request`
Add Redis caching for frequently accessed data:
- Cache search results (TTL: 5 minutes)
- Cache student dashboard data (TTL: 1 minute)
- Cache recommendation results (TTL: 24 hours)
- Invalidate cache on resource updates

**Dependencies:** `redis`, `hiredis`

---

## Sprint 4 — Notifications and Reporting (Should-Have)

### Feature 8: Email Notification Service
**Issue label:** `good-first-issue`
Implement automated email notifications:
- Overdue reminder (3 days before due date)
- Due today notification
- Overdue notice (1 day after due date)
- Reservation confirmation
- Use SendGrid or SMTP

**Dependencies:** `sendgrid` or `smtplib`

---

### Feature 9: Admin Reporting Dashboard
**Issue label:** `good-first-issue`
Add reporting endpoints:
```
GET /api/reports/top-borrowed        — Top 20 borrowed resources
GET /api/reports/overdue-rate        — Overdue rate by month
GET /api/reports/active-users        — Active users by faculty
GET /api/reports/export?format=csv   — Export report as CSV
```

---

### Feature 10: Scheduled Task Runner
**Issue label:** `feature-request`
Add a background task scheduler (APScheduler or Celery):
- Run overdue notification job hourly
- Run recommendation batch job daily
- Run reservation expiry cleanup every 30 minutes

**Dependencies:** `apscheduler` or `celery`

---

## Sprint 5 — Mobile and Deployment (Could-Have)

### Feature 11: Docker Containerisation
**Issue label:** `good-first-issue`
Create a `Dockerfile` and `docker-compose.yml` to run the full stack:
```yaml
services:
  api:      # FastAPI application
  db:       # PostgreSQL database
  redis:    # Redis cache
  elastic:  # Elasticsearch
```

---

### Feature 12: Student Mobile App (React Native)
**Issue label:** `feature-request`
Build a mobile app that consumes the SALAS REST API:
- Search and browse catalogue
- View dashboard (loans, due dates)
- Borrow and reserve resources
- Receive push notifications

---

### Feature 13: Accessibility Improvements (WCAG 2.1 AA)
**Issue label:** `good-first-issue`
Improve the API to better support accessible frontends:
- Add alt-text metadata field to Resource
- Add screen-reader friendly error messages
- Ensure all error responses follow consistent format

---

### Feature 14: OpenAPI Client Generation
**Issue label:** `good-first-issue`
Generate a typed Python client from the OpenAPI spec:
```bash
openapi-generator generate -i openapi.json -g python -o salas-client/
```
This allows any Python application to consume the SALAS API with
full type safety and auto-completion.

---

## Won't Have (This Semester)

These are deliberately out of scope:

- RFID integration for physical book scanning
- Deep learning recommendation model
- University SSO (Single Sign-On) integration
- Multi-tenant support (multiple university instances)
- Blockchain-based loan verification

---

## How to Contribute to the Roadmap

1. Pick any item above that interests you
2. Check the Issues tab — it may already have a related issue
3. If not, create a new issue with the label `feature-request`
4. Comment on the issue before starting work
5. Follow the contribution guidelines in `CONTRIBUTING.md`

Items marked `good-first-issue` are specifically designed to be
approachable for new contributors with no prior knowledge of the
full codebase.
