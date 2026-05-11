[openapi.md](https://github.com/user-attachments/files/27612188/openapi.md)
# SALAS REST API Documentation
## Smart Academic Library Assistance System — OpenAPI Reference

> Version: 1.0.0 | Framework: FastAPI | Auto-docs: http://localhost:8000/docs

FastAPI automatically generates a full interactive Swagger UI and OpenAPI JSON
from the route decorators and Pydantic models in `api/main.py`.

**To view live documentation:**
```bash
pip install fastapi uvicorn
uvicorn api.main:app --reload --port 8000
# Then open: http://localhost:8000/docs
```

---

## Base URL
```
http://localhost:8000
```

---

## Endpoints Summary

### 🔐 Users (`/api/users`)

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `POST` | `/api/users/register/student` | Register a new student | 201, 400, 409 |
| `POST` | `/api/users/register/librarian` | Register a new librarian | 201, 400, 409 |
| `POST` | `/api/users/login` | Login with email and password | 200, 401, 403 |
| `GET` | `/api/users` | Get all users | 200 |
| `GET` | `/api/users/{user_id}` | Get user by ID | 200, 404 |
| `PUT` | `/api/users/{user_id}` | Update user profile | 200, 400, 404 |
| `DELETE` | `/api/users/{user_id}` | Delete user account | 204, 404 |

---

### 📚 Resources (`/api/resources`)

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `GET` | `/api/resources` | Get all resources (supports ?keyword, ?genre, ?available_only) | 200 |
| `POST` | `/api/resources` | Add resource to catalogue | 201, 400 |
| `GET` | `/api/resources/{resource_id}` | Get resource by ID | 200, 404 |
| `GET` | `/api/resources/{resource_id}/availability` | Check real-time availability | 200, 404 |
| `PUT` | `/api/resources/{resource_id}` | Update resource metadata | 200, 400, 404 |
| `DELETE` | `/api/resources/{resource_id}` | Delete resource | 204, 404, 409 |

---

### 📋 Loans (`/api/loans`)

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `GET` | `/api/loans` | Get all loans | 200 |
| `GET` | `/api/loans/{loan_id}` | Get loan by ID | 200, 404 |
| `POST` | `/api/loans/checkout` | Checkout resource to student | 201, 403, 409 |
| `POST` | `/api/loans/{loan_id}/return` | Return a borrowed resource | 200, 404, 409 |
| `POST` | `/api/loans/{loan_id}/renew` | Renew loan for 14 more days | 200, 404, 409 |
| `GET` | `/api/loans/{loan_id}/fine` | Get fine details for a loan | 200, 404 |
| `GET` | `/api/students/{student_id}/loans` | Get all loans for a student | 200 |
| `GET` | `/api/loans/overdue/all` | Get all overdue loans | 200 |

---

## Request / Response Examples

### Register Student
**POST** `/api/users/register/student`
```json
{
  "user_id": "s001",
  "name": "Alice Dlamini",
  "email": "alice@university.ac.za",
  "password": "Pass@123",
  "student_number": "211001",
  "course_enrollment": ["Computer Science"]
}
```
**Response 201:**
```json
{
  "user_id": "s001",
  "name": "Alice Dlamini",
  "email": "alice@university.ac.za",
  "role": "STUDENT",
  "account_status": "ACTIVE"
}
```

---

### Add Resource
**POST** `/api/resources`
```json
{
  "resource_id": "r001",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "9780132350884",
  "genre": "Software Engineering",
  "published_year": 2008,
  "total_copies": 3,
  "location": "CS Shelf 4B"
}
```
**Response 201:**
```json
{
  "resource_id": "r001",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "9780132350884",
  "genre": "Software Engineering",
  "published_year": 2008,
  "total_copies": 3,
  "available_copies": 3,
  "location": "CS Shelf 4B",
  "status": "AVAILABLE"
}
```

---

### Checkout a Resource
**POST** `/api/loans/checkout?student_id=s001&resource_id=r001`

**Response 201:**
```json
{
  "loan_id": "loan_s001_r001_2026-04-01",
  "student_id": "s001",
  "resource_id": "r001",
  "resource_title": "Clean Code",
  "borrowed_date": "2026-04-01",
  "due_date": "2026-04-15",
  "status": "ACTIVE",
  "fine_amount": 0.0
}
```

---

## Error Responses

All errors return a JSON body with a `detail` field:

```json
{ "detail": "Resource 'r001' has no available copies." }
```

| HTTP Code | Meaning |
|---|---|
| `400` | Bad request — invalid input (e.g. invalid ISBN, empty keyword) |
| `401` | Unauthorized — wrong email or password |
| `403` | Forbidden — account locked or student ineligible to borrow |
| `404` | Not found — resource, user, or loan does not exist |
| `409` | Conflict — duplicate email, active loans blocking deletion, already returned |

---

## Business Rules Enforced by the API

| Rule | Endpoint | HTTP Response |
|---|---|---|
| BR-01: Max 5 active loans | `POST /api/loans/checkout` | 403 |
| BR-02: Fines > R100 block borrowing | `POST /api/loans/checkout` | 403 |
| BR-04: No delete with active loans | `DELETE /api/resources/{id}` | 409 |
| BR-05: ISBN must be valid | `POST /api/resources` | 400 |
| BR-06: Lockout after 5 failed logins | `POST /api/users/login` | 403 |
| BR-10: Fine = R5/day, max R200 | `GET /api/loans/{id}/fine` | 200 |
