[README_A12.md](https://github.com/user-attachments/files/27610547/README_A12.md)
# Smart Academic Library Assistance System (SALAS)

An intelligent library platform for university students.

## Project Documents

### Assignments 3–11
See previous README sections for all prior assignment documents.

### Assignment 12 — Service Layer and REST API
| File | Description |
|---|---|
| [services/user_service.py](./services/user_service.py) | UserService — registration, login, RBAC, profile management |
| [services/resource_service.py](./services/resource_service.py) | ResourceService — catalogue CRUD, search, ISBN validation, availability |
| [services/loan_service.py](./services/loan_service.py) | LoanService — checkout, return, renewal, fine calculation |
| [api/main.py](./api/main.py) | FastAPI REST API — 19 endpoints for Users, Resources, Loans |
| [docs/openapi.md](./docs/openapi.md) | API documentation — endpoints, schemas, error codes |
| [tests/services/test_services.py](./tests/services/test_services.py) | 55 service unit tests |
| [tests/api/test_api.py](./tests/api/test_api.py) | 39 API integration tests |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

## API Endpoints (19 total)

### Users
- `POST /api/users/register/student` — Register student
- `POST /api/users/register/librarian` — Register librarian
- `POST /api/users/login` — Login
- `GET /api/users` — Get all users
- `GET /api/users/{id}` — Get user
- `PUT /api/users/{id}` — Update profile
- `DELETE /api/users/{id}` — Delete user

### Resources
- `GET /api/resources` — Search/filter catalogue
- `POST /api/resources` — Add resource
- `GET /api/resources/{id}` — Get resource
- `GET /api/resources/{id}/availability` — Check availability
- `PUT /api/resources/{id}` — Update resource
- `DELETE /api/resources/{id}` — Delete resource

### Loans
- `GET /api/loans` — All loans
- `GET /api/loans/{id}` — Get loan
- `POST /api/loans/checkout` — Checkout
- `POST /api/loans/{id}/return` — Return
- `POST /api/loans/{id}/renew` — Renew
- `GET /api/loans/{id}/fine` — Fine details
- `GET /api/students/{id}/loans` — Student loans
- `GET /api/loans/overdue/all` — All overdue

## Running the API
```bash
pip install fastapi uvicorn pytest httpx
uvicorn api.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
# OpenAPI JSON: http://localhost:8000/openapi.json
```

## Running Tests
```bash
pytest tests/ -v
# Result: 289 tests passing
```

## Architecture
```
Request → FastAPI Router → Service Layer → Repository → In-Memory Storage
```
Services never access repositories directly — they use injected repository
interfaces, making the business logic testable and storage-agnostic.

## Author
**Phola Qwalana 211225347** | Software Engineering | May 2026
