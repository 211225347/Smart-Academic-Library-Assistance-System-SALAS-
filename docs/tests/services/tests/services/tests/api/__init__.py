"""
tests/api/test_api.py
Integration tests for SALAS REST API endpoints.
Uses FastAPI TestClient (no server needed).

Run with: pytest tests/api/test_api.py -v --tb=short
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from fastapi.testclient import TestClient
from api.main import app, user_service, resource_service, loan_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repos():
    """Clear all repos before each test for isolation."""
    user_service._repo.clear()
    resource_service._repo.clear()
    loan_service._loan_repo.clear()
    yield
    user_service._repo.clear()
    resource_service._repo.clear()
    loan_service._loan_repo.clear()


@pytest.fixture
def student_payload():
    return {
        "user_id": "s001",
        "name": "Alice Dlamini",
        "email": "alice@university.ac.za",
        "password": "Pass@123",
        "student_number": "211001",
        "course_enrollment": ["Computer Science"]
    }

@pytest.fixture
def resource_payload():
    return {
        "resource_id": "r001",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "genre": "Software Engineering",
        "published_year": 2008,
        "total_copies": 3,
        "location": "CS Shelf 4B"
    }

@pytest.fixture
def registered_student(student_payload):
    client.post("/api/users/register/student", json=student_payload)

@pytest.fixture
def registered_resource(resource_payload):
    client.post("/api/resources", json=resource_payload)


# ══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════════════

class TestHealthCheck:

    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "SALAS" in data["system"]


# ══════════════════════════════════════════════════════════════════════════════
# USER API TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestUserAPI:

    def test_register_student_201(self, student_payload):
        response = client.post(
            "/api/users/register/student", json=student_payload
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == "s001"
        assert data["role"] == "STUDENT"

    def test_register_student_invalid_domain_400(self):
        response = client.post("/api/users/register/student", json={
            "user_id": "s002", "name": "Eve",
            "email": "eve@gmail.com",
            "password": "Pass@123",
            "student_number": "211002",
            "course_enrollment": []
        })
        assert response.status_code == 400
        assert "university domain" in response.json()["detail"]

    def test_register_duplicate_email_409(self, student_payload):
        client.post("/api/users/register/student", json=student_payload)
        response = client.post(
            "/api/users/register/student", json={
                **student_payload, "user_id": "s999"
            }
        )
        assert response.status_code == 409

    def test_register_librarian_201(self):
        response = client.post("/api/users/register/librarian", json={
            "user_id": "l001", "name": "Bob Nkosi",
            "email": "bob@university.ac.za",
            "password": "Staff@456",
            "staff_id": "LIB001",
            "department": "Reference"
        })
        assert response.status_code == 201
        assert response.json()["role"] == "LIBRARIAN"

    def test_login_success_200(self, student_payload, registered_student):
        response = client.post("/api/users/login", json={
            "email": "alice@university.ac.za",
            "password": "Pass@123"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful."

    def test_login_wrong_password_401(self, registered_student):
        response = client.post("/api/users/login", json={
            "email": "alice@university.ac.za",
            "password": "WrongPass"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user_401(self):
        response = client.post("/api/users/login", json={
            "email": "ghost@university.ac.za",
            "password": "Pass@123"
        })
        assert response.status_code == 401

    def test_get_all_users_200(self, registered_student):
        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_user_by_id_200(self, registered_student):
        response = client.get("/api/users/s001")
        assert response.status_code == 200
        assert response.json()["user_id"] == "s001"

    def test_get_user_not_found_404(self):
        response = client.get("/api/users/ghost")
        assert response.status_code == 404

    def test_update_profile_200(self, registered_student):
        response = client.put(
            "/api/users/s001",
            json={"name": "Alice Updated", "email": None}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Alice Updated"

    def test_delete_user_204(self, registered_student):
        response = client.delete("/api/users/s001")
        assert response.status_code == 204

    def test_delete_nonexistent_user_404(self):
        response = client.delete("/api/users/ghost")
        assert response.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# RESOURCE API TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestResourceAPI:

    def test_add_resource_201(self, resource_payload):
        response = client.post("/api/resources", json=resource_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["resource_id"] == "r001"
        assert data["available_copies"] == 3

    def test_add_resource_invalid_isbn_400(self):
        response = client.post("/api/resources", json={
            "resource_id": "r_bad", "title": "Bad", "author": "Auth",
            "isbn": "1234567890", "genre": "General",
            "published_year": 2020, "total_copies": 1,
            "location": "Shelf"
        })
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower()

    def test_get_all_resources_200(self, registered_resource):
        response = client.get("/api/resources")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_resources_200(self, registered_resource):
        response = client.get("/api/resources?keyword=clean")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_filter_by_genre_200(self, registered_resource):
        response = client.get(
            "/api/resources?genre=Software Engineering"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_available_only(self, registered_resource):
        response = client.get("/api/resources?available_only=true")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_resource_by_id_200(self, registered_resource):
        response = client.get("/api/resources/r001")
        assert response.status_code == 200
        assert response.json()["title"] == "Clean Code"

    def test_get_resource_not_found_404(self):
        response = client.get("/api/resources/ghost")
        assert response.status_code == 404

    def test_check_availability_200(self, registered_resource):
        response = client.get("/api/resources/r001/availability")
        assert response.status_code == 200
        data = response.json()
        assert data["is_available"] is True
        assert data["available_copies"] == 3

    def test_update_resource_200(self, registered_resource):
        response = client.put("/api/resources/r001", json={
            "title": "Clean Code 2nd Ed",
            "total_copies": 5
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Clean Code 2nd Ed"

    def test_update_resource_not_found_404(self):
        response = client.put("/api/resources/ghost", json={
            "title": "New Title"
        })
        assert response.status_code == 404

    def test_delete_resource_204(self, registered_resource):
        response = client.delete("/api/resources/r001")
        assert response.status_code == 204

    def test_delete_resource_with_loans_409(
            self, registered_resource, student_payload):
        client.post("/api/users/register/student", json=student_payload)
        client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        response = client.delete("/api/resources/r001")
        assert response.status_code == 409


# ══════════════════════════════════════════════════════════════════════════════
# LOAN API TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestLoanAPI:

    @pytest.fixture(autouse=True)
    def setup(self, student_payload, resource_payload):
        client.post("/api/users/register/student", json=student_payload)
        client.post("/api/resources", json=resource_payload)

    def test_checkout_201(self):
        response = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        assert response.status_code == 201
        data = response.json()
        assert data["student_id"] == "s001"
        assert data["resource_id"] == "r001"
        assert data["status"] == "ACTIVE"

    def test_checkout_resource_unavailable_409(self):
        resource_service._repo.find_by_id("r001")._available_copies = 0
        response = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        assert response.status_code == 409

    def test_checkout_student_not_found_403(self):
        response = client.post(
            "/api/loans/checkout?student_id=ghost&resource_id=r001"
        )
        assert response.status_code == 403

    def test_get_all_loans_200(self):
        client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        response = client.get("/api/loans")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_loan_by_id_200(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        response = client.get(f"/api/loans/{loan_id}")
        assert response.status_code == 200
        assert response.json()["loan_id"] == loan_id

    def test_get_loan_not_found_404(self):
        response = client.get("/api/loans/ghost")
        assert response.status_code == 404

    def test_return_loan_200(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        response = client.post(f"/api/loans/{loan_id}/return")
        assert response.status_code == 200
        assert response.json()["status"] == "RETURNED"

    def test_return_already_returned_409(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        client.post(f"/api/loans/{loan_id}/return")
        response = client.post(f"/api/loans/{loan_id}/return")
        assert response.status_code == 409

    def test_renew_loan_200(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        response = client.post(f"/api/loans/{loan_id}/renew")
        assert response.status_code == 200

    def test_get_fine_200(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        response = client.get(f"/api/loans/{loan_id}/fine")
        assert response.status_code == 200
        data = response.json()
        assert data["fine_amount"] == 0.0
        assert data["is_overdue"] is False

    def test_get_student_loans_200(self):
        client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        response = client.get("/api/students/s001/loans")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_overdue_loans_200(self):
        checkout = client.post(
            "/api/loans/checkout?student_id=s001&resource_id=r001"
        )
        loan_id = checkout.json()["loan_id"]
        # Make it overdue
        from datetime import timedelta, date
        loan = loan_service._loan_repo.find_by_id(loan_id)
        loan._due_date = date.today() - timedelta(days=3)
        loan_service._loan_repo.save(loan)

        response = client.get("/api/loans/overdue/all")
        assert response.status_code == 200
        assert len(response.json()) == 1
