"""
services/user_service.py
UserService — encapsulates all business logic for User operations.

Uses the UserRepository (Assignment 11) for persistence.
Enforces business rules from DOMAIN_MODEL.md (BR-01 to BR-10).
Maps to: FR-01 (Authentication), FR-10 (RBAC).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import Optional, List
from src.models import User, Student, Librarian, Role, AccountStatus
from repositories.interfaces import UserRepository


class UserNotFoundError(Exception):
    """Raised when a user does not exist in the repository."""
    pass


class UserAlreadyExistsError(Exception):
    """Raised when trying to register with a duplicate email."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login credentials are incorrect."""
    pass


class AccountLockedError(Exception):
    """Raised when a locked account attempts to log in."""
    pass


class UserService:
    """
    Service class encapsulating all User business operations.

    Depends on UserRepository (injected) — never instantiates
    a concrete repository directly. This makes the service
    testable with any repository implementation.

    Usage:
        repo = RepositoryFactory.get_user_repository("MEMORY")
        service = UserService(repo)
        student = service.register_student("u001", "Alice", ...)
    """

    VALID_DOMAINS = ["university.ac.za", "student.university.ac.za"]

    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    # ── Registration ───────────────────────────────────────────────────────

    def register_student(self, user_id: str, name: str, email: str,
                         password: str, student_number: str,
                         course_enrollment: List[str] = None) -> Student:
        """
        Registers a new student account.
        Validates university email domain (FR-01).
        Raises UserAlreadyExistsError if email is already registered.
        """
        self._validate_email_domain(email)
        self._ensure_email_unique(email)

        student = Student(
            user_id=user_id,
            name=name,
            email=email,
            password=password,
            student_number=student_number,
            course_enrollment=course_enrollment or []
        )
        self._repo.save(student)
        return student

    def register_librarian(self, user_id: str, name: str, email: str,
                           password: str, staff_id: str,
                           department: str) -> Librarian:
        """
        Registers a new librarian account.
        Validates university email domain.
        """
        self._validate_email_domain(email)
        self._ensure_email_unique(email)

        librarian = Librarian(
            user_id=user_id,
            name=name,
            email=email,
            password=password,
            staff_id=staff_id,
            department=department
        )
        self._repo.save(librarian)
        return librarian

    # ── Authentication ─────────────────────────────────────────────────────

    def login(self, email: str, password: str) -> User:
        """
        Authenticates a user by email and password.
        Enforces 5-attempt lockout (BR-06 / NFR-10).

        Returns the authenticated User on success.
        Raises InvalidCredentialsError or AccountLockedError on failure.
        """
        user = self._repo.find_by_email(email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password.")

        if user.account_status == AccountStatus.LOCKED:
            raise AccountLockedError(
                "Account is locked due to too many failed attempts. "
                "Try again in 15 minutes."
            )

        success = user.login(password)
        self._repo.save(user)  # Persist updated attempt count / lock status

        if not success:
            raise InvalidCredentialsError("Invalid email or password.")

        return user

    # ── CRUD Operations ────────────────────────────────────────────────────

    def get_user(self, user_id: str) -> User:
        """Retrieve a user by ID. Raises UserNotFoundError if missing."""
        user = self._repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return user

    def get_all_users(self) -> List[User]:
        """Return all registered users."""
        return self._repo.find_all()

    def get_users_by_role(self, role: str) -> List[User]:
        """Return all users with the given role (FR-10 RBAC)."""
        return self._repo.find_by_role(role)

    def update_profile(self, user_id: str, name: str = None,
                       email: str = None) -> User:
        """Update a user's profile. Validates new email if provided."""
        user = self.get_user(user_id)
        if email and email != user.email:
            self._validate_email_domain(email)
            self._ensure_email_unique(email)
        user.update_profile(name=name, email=email)
        self._repo.save(user)
        return user

    def deactivate_user(self, user_id: str) -> User:
        """
        Deactivates a user account.
        Triggers POPIA data erasure within 30 days (NFR-11 / BR-07).
        """
        user = self.get_user(user_id)
        user.deactivate_account()
        self._repo.save(user)
        return user

    def delete_user(self, user_id: str) -> None:
        """Permanently removes a user from the repository."""
        self.get_user(user_id)  # Raises if not found
        self._repo.delete(user_id)

    # ── Queries ────────────────────────────────────────────────────────────

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address."""
        return self._repo.find_by_email(email)

    def get_active_users(self) -> List[User]:
        """Return all users with ACTIVE account status."""
        return self._repo.find_active_users()

    # ── Private Validators ─────────────────────────────────────────────────

    def _validate_email_domain(self, email: str) -> None:
        """Enforce university email domain (FR-01)."""
        domain = email.split("@")[-1].lower() if "@" in email else ""
        if domain not in self.VALID_DOMAINS:
            raise ValueError(
                f"Email must use a university domain. "
                f"Accepted: {self.VALID_DOMAINS}"
            )

    def _ensure_email_unique(self, email: str) -> None:
        """Prevent duplicate email registrations."""
        existing = self._repo.find_by_email(email)
        if existing:
            raise UserAlreadyExistsError(
                f"An account with email '{email}' already exists."
            )
