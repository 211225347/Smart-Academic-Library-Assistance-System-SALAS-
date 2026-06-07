"""
api/main.py
SALAS REST API — FastAPI application.

Exposes RESTful endpoints for User, Resource, Loan, and Reservation entities.
Auto-generates OpenAPI/Swagger documentation at /docs.

Start server:
    uvicorn api.main:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
OpenAPI JSON: http://localhost:8000/openapi.json
"""

import sys
import os
import uuid
from datetime import date
from typing import List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.models import Reservation, ReservationStatus
from factories.repository_factory import RepositoryFactory
from services.user_service import (
    UserService, UserNotFoundError, UserAlreadyExistsError,
    InvalidCredentialsError, AccountLockedError
)
from services.resource_service import (
    ResourceService, ResourceNotFoundError,
    ResourceHasActiveLoansError, InvalidISBNError
)
from services.loan_service import (
    LoanService, LoanNotFoundError, StudentNotEligibleError,
    ResourceUnavailableError, LoanAlreadyReturnedError
)

# ── App Initialisation ────────────────────────────────────────────────────────

app = FastAPI(
    title="SALAS — Smart Academic Library Assistance System",
    description=(
        "REST API for the Smart Academic Library Assistance System. "
        "Provides endpoints for managing users, library resources, "
        "loan transactions, and reservations. Built with FastAPI on top of a "
        "repository-based persistence layer (Assignment 11)."
    ),
    version="1.0.0",
    contact={
        "name": "Phola Qwalana",
        "email": "211225347@university.ac.za"
    },
    license_info={
        "name": "MIT"
    }
)

# ── Dependency Injection via Factory ─────────────────────────────────────────

_repos = RepositoryFactory.get_all("MEMORY")

user_service = UserService(_repos["users"])
resource_service = ResourceService(_repos["resources"], _repos["loans"])
loan_service = LoanService(
    _repos["loans"], _repos["users"], _repos["resources"]
)
# Concrete reference to reservation storage layer for Issue #36
reservation_repo = _repos["reservations"]

# ── Pydantic Request / Response Models ───────────────────────────────────────

class RegisterStudentRequest(BaseModel):
    user_id: str = Field(..., example="s001")
    name: str = Field(..., example="Alice Dlamini")
    email: str = Field(..., example="alice@university.ac.za")
    password: str = Field(..., min_length=8, example="Pass@123")
    student_number: str = Field(..., example="211001")
    course_enrollment: List[str] = Field(
        default=[], example=["Computer Science"]
    )

class RegisterLibrarianRequest(BaseModel):
    user_id: str = Field(..., example="l001")
    name: str = Field(..., example="Bob Nkosi")
    email: str = Field(..., example="bob@university.ac.za")
    password: str = Field(..., min_length=8, example="Staff@456")
    staff_id: str = Field(..., example="LIB001")
    department: str = Field(..., example="Reference")

class LoginRequest(BaseModel):
    email: str = Field(..., example="alice@university.ac.za")
    password: str = Field(..., example="Pass@123")

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, example="Alice Updated")
    email: Optional[str] = Field(None, example="alice.new@university.ac.za")

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    account_status: str

class AddResourceRequest(BaseModel):
    resource_id: str = Field(..., example="r001")
    title: str = Field(..., example="Clean Code")
    author: str = Field(..., example="Robert C. Martin")
    isbn: str = Field(..., example="9780132350884")
    genre: str = Field(..., example="Software Engineering")
    published_year: int = Field(..., example=2008)
    total_copies: int = Field(..., ge=1, example=3)
    location: str = Field(..., example="CS Shelf 4B")

class UpdateResourceRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    total_copies: Optional[int] = Field(None, ge=1)
    location: Optional[str] = None

class ResourceResponse(BaseModel):
    resource_id: str
    title: str
    author: str
    isbn: str
    genre: str
    published_year: int
    total_copies: int
    available_copies: int
    location: str
    status: str

class LoanResponse(BaseModel):
    loan_id: str
    student_id: str
    resource_id: str
    resource_title: str
    borrowed_date: str
    due_date: str
    status: str
    fine_amount: float

class CreateReservationRequest(BaseModel):
    user_id: str = Field(..., example="s001")
    resource_id: str = Field(..., example="r001")

class ReservationResponse(BaseModel):
    reservation_id: str
    user_id: str
    resource_id: str
    reservation_date: str
    status: str

# ── Helpers ───────────────────────────────────────────────────────────────────

def user_to_response(user) -> UserResponse:
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        role=user.role.value,
        account_status=user.account_status.value
    )

def resource_to_response(r) -> ResourceResponse:
    return ResourceResponse(
        resource_id=r.resource_id,
        title=r.title,
        author=r.author,
        isbn=r.isbn,
        genre=r._genre,
        published_year=r._published_year,
        total_copies=r._total_copies,
        available_copies=r.available_copies,
        location=r._location,
        status=r.status.value
    )

def loan_to_response(loan) -> LoanResponse:
    return LoanResponse(
        loan_id=loan.loan_id,
        student_id=loan._student.user_id,
        resource_id=loan.resource.resource_id,
        resource_title=loan.resource.title,
        borrowed_date=str(loan._borrowed_date),
        due_date=str(loan.due_date),
        status=loan.status.value,
        fine_amount=loan.calculate_fine()
    )

# ═══════════════════════════════════════════════════════════════════════════════
# USER ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/users/register/student",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new student",
    description=(
        "Creates a new student account. Email must use a valid university "
        "domain (@university.ac.za). Password must be at least 8 characters. "
        "Maps to FR-01 and UC01."
    )
)
def register_student(request: RegisterStudentRequest):
    try:
        student = user_service.register_student(
            user_id=request.user_id,
            name=request.name,
            email=request.email,
            password=request.password,
            student_number=request.student_number,
            course_enrollment=request.course_enrollment
        )
        return user_to_response(student)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/api/users/register/librarian",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new librarian"
)
def register_librarian(request: RegisterLibrarianRequest):
    try:
        librarian = user_service.register_librarian(
            user_id=request.user_id,
            name=request.name,
            email=request.email,
            password=request.password,
            staff_id=request.staff_id,
            department=request.department
        )
        return user_to_response(librarian)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/api/users/login",
    tags=["Users"],
    summary="Login with email and password",
    description=(
        "Authenticates a user. Account is locked after 5 failed "
        "attempts for 15 minutes (NFR-10 / BR-06)."
    )
)
def login(request: LoginRequest):
    try:
        user = user_service.login(request.email, request.password)
        return {
            "message": "Login successful.",
            "user": user_to_response(user)
        }
    except AccountLockedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get(
    "/api/users",
    response_model=List[UserResponse],
    tags=["Users"],
    summary="Get all users"
)
def get_all_users():
    return [user_to_response(u) for u in user_service.get_all_users()]


@app.get(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get a user by ID"
)
def get_user(user_id: str):
    try:
        return user_to_response(user_service.get_user(user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Update a user's profile"
)
def update_profile(user_id: str, request: UpdateProfileRequest):
    try:
        user = user_service.update_profile(
            user_id, name=request.name, email=request.email
        )
        return user_to_response(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (UserAlreadyExistsError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user account"
)
def delete_user(user_id: str):
    try:
        user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get(
    "/api/resources",
    response_model=List[ResourceResponse],
    tags=["Resources"],
    summary="Get all resources",
    description="Returns all resources in the library catalogue (FR-02)."
)
def get_all_resources(
    keyword: Optional[str] = Query(None, description="Search keyword"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    available_only: bool = Query(False, description="Show only available resources")
):
    if keyword:
        resources = resource_service.search(keyword)
    elif genre:
        resources = resource_service.get_by_genre(genre)
    elif available_only:
        resources = resource_service.get_available_resources()
    else:
        resources = resource_service.get_all_resources()
    return [resource_to_response(r) for r in resources]


@app.post(
    "/api/resources",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Resources"],
    summary="Add a new resource to the catalogue",
    description=(
        "Creates a new library resource. ISBN is validated using "
        "ISBN-10 or ISBN-13 check digit rules (BR-05). Maps to FR-06."
    )
)
def add_resource(request: AddResourceRequest):
    try:
        resource = resource_service.add_resource(
            resource_id=request.resource_id,
            title=request.title,
            author=request.author,
            isbn=request.isbn,
            genre=request.genre,
            published_year=request.published_year,
            total_copies=request.total_copies,
            location=request.location
        )
        return resource_to_response(resource)
    except InvalidISBNError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/resources/{resource_id}",
    response_model=ResourceResponse,
    tags=["Resources"],
    summary="Get a resource by ID"
)
def get_resource(resource_id: str):
    try:
        return resource_to_response(
            resource_service.get_resource(resource_id)
        )
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/api/resources/{resource_id}/availability",
    tags=["Resources"],
    summary="Check real-time availability of a resource",
    description="Returns availability status and copy counts (FR-02)."
)
def check_availability(resource_id: str):
    try:
        return resource_service.check_availability(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put(
    "/api/resources/{resource_id}",
    response_model=ResourceResponse,
    tags=["Resources"],
    summary="Update resource metadata"
)
def update_resource(resource_id: str, request: UpdateResourceRequest):
    try:
        resource = resource_service.update_resource(
            resource_id=resource_id,
            title=request.title,
            author=request.author,
            genre=request.genre,
            total_copies=request.total_copies,
            location=request.location
        )
        return resource_to_response(resource)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete(
    "/api/resources/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Resources"],
    summary="Delete a resource from the catalogue",
    description=(
        "Deletes a resource. Blocked if active loans exist (BR-04)."
    )
)
def delete_resource(resource_id: str):
    try:
        resource_service.delete_resource(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ResourceHasActiveLoansError as e:
        raise HTTPException(status_code=409, detail=str(e))


# ── LOAN ENDPOINTS ────────────────────────────────────────────────────────────

@app.get(
    "/api/loans",
    response_model=List[LoanResponse],
    tags=["Loans"],
    summary="Get all loans"
)
def get_all_loans():
    return [loan_to_response(l) for l in loan_service.get_all_loans()]


@app.get(
    "/api/loans/{loan_id}",
    response_model=LoanResponse,
    tags=["Loans"],
    summary="Get a specific loan by ID"
)
def get_loan(loan_id: str):
    try:
        return loan_to_response(loan_service.get_loan(loan_id))
    except LoanNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post(
    "/api/loans/checkout",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Loans"],
    summary="Checkout a resource to a student",
    description=(
        "Creates a loan for a student. Enforces: max 5 active loans "
        "(BR-01), fines under R100 (BR-02), resource availability. "
        "Maps to FR-03, UC03."
    )
)
def checkout(
    student_id: str = Query(..., description="Student user ID"),
    resource_id: str = Query(..., description="Resource ID to borrow")
):
    try:
        loan = loan_service.checkout(student_id, resource_id)
        return loan_to_response(loan)
    except StudentNotEligibleError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ResourceUnavailableError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.post(
    "/api/loans/{loan_id}/return",
    response_model=LoanResponse,
    tags=["Loans"],
    summary="Return a borrowed resource",
    description=(
        "Marks a loan as returned. Calculates overdue fine if applicable "
        "(BR-10: R5/day, max R200). Maps to UC12."
    )
)
def return_loan(loan_id: str):
    try:
        loan = loan_service.return_loan(loan_id)
        return loan_to_response(loan)
    except LoanNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LoanAlreadyReturnedError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.post(
    "/api/loans/{loan_id}/renew",
    response_model=LoanResponse,
    tags=["Loans"],
    summary="Renew a loan for 14 more days",
    description="Extends the loan period. Blocked if reservations exist (BR-09)."
)
def renew_loan(loan_id: str):
    try:
        loan = loan_service.renew_loan(loan_id)
        return loan_to_response(loan)
    except LoanNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (LoanAlreadyReturnedError, StudentNotEligibleError) as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get(
    "/api/loans/{loan_id}/fine",
    tags=["Loans"],
    summary="Get fine details for a loan",
    description="Returns fine amount and whether borrowing is blocked (BR-10)."
)
def get_fine(loan_id: str):
    try:
        return loan_service.get_fine_summary(loan_id)
    except LoanNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/api/students/{student_id}/loans",
    response_model=List[LoanResponse],
    tags=["Loans"],
    summary="Get all loans for a student",
    description="Returns borrowing history and active loans (FR-04 Dashboard)."
)
def get_student_loans(student_id: str):
    return [loan_to_response(l)
            for l in loan_service.get_student_loans(student_id)]


@app.get(
    "/api/loans/overdue/all",
    response_model=List[LoanResponse],
    tags=["Loans"],
    summary="Get all overdue loans",
    description="Returns all overdue loans system-wide (used by FR-07 scheduler)."
)
def get_overdue_loans():
    return [loan_to_response(l) for l in loan_service.get_overdue_loans()]


# ═══════════════════════════════════════════════════════════════════════════════
# RESERVATION ENDPOINTS (Issue #36)
# ═══════════════════════════════════════════════════════════════════════════════

@app.post(
    "/api/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Reservations"],
    summary="Create a new resource reservation",
    description="Creates a valid reservation record. Applies strict business criteria checks."
)
def create_reservation(request: CreateReservationRequest):
    try:
        # 1. Core verification: Validate user and resource context via underlying services
        student = user_service.get_user(request.user_id)
        resource = resource_service.get_resource(request.resource_id)

        # 2. Business Logic Guard: Blocks reservation if there are copies sitting available on the shelf
        if resource.available_copies > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource '{request.resource_id}' has available copies on shelf. Checkout instead."
            )

        # 3. Business Logic Guard: Cap active tracking entities per student
        active_student_reservations = reservation_repo.find_by_student(request.user_id)
        pending_or_queued = [
            r for r in active_student_reservations 
            if r.status in {ReservationStatus.PENDING, ReservationStatus.QUEUED}
        ]
        if len(pending_or_queued) >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student has reached the maximum limit of 3 active reservations."
            )

        # 4. Process identity initialization
        res_id = f"res-{uuid.uuid4().hex[:6]}"
        reservation = Reservation(
            reservation_id=res_id,
            student=student,
            resource=resource,
            reservation_date=date.today()
        )

        # 5. Evaluate current waiting listing sizes to determine status allocation
        existing_active = reservation_repo.find_active_by_resource(request.resource_id)
        if len(existing_active) > 0:
            reservation.status = ReservationStatus.QUEUED
            reservation._queue_position = len(existing_active) + 1
        else:
            reservation.status = ReservationStatus.PENDING

        # 6. Save directly to your persistent storage collection layer
        reservation_repo.save(reservation)

        return ReservationResponse(
            reservation_id=reservation.reservation_id,
            user_id=reservation._student.user_id,
            resource_id=reservation._resource.resource_id,
            reservation_date=str(reservation.reservation_date),
            status=reservation.status.value
        )

    except (UserNotFoundError, ResourceNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/api/reservations",
    response_model=List[ReservationResponse],
    tags=["Reservations"],
    summary="Get all reservations",
    description="Returns a tracked list array of system-wide academic reservations."
)
def get_all_reservations():
    all_records = reservation_repo.find_all()
    return [
        ReservationResponse(
            reservation_id=r.reservation_id,
            user_id=r._student.user_id,
            resource_id=r._resource.resource_id,
            reservation_date=str(r.reservation_date),
            status=r.status.value
        )
        for r in all_records
    ]


# ── Health Check ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"], summary="API health check")
def root():
    return {
        "system": "SALAS — Smart Academic Library Assistance System",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }