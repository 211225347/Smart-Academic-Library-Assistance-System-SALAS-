"""
repositories/inmemory/inmemory_repositories.py
In-memory HashMap implementations of all repository interfaces.

Uses Python dict as the HashMap storage backend.
All implementations are fully interchangeable with future storage backends
(filesystem, database) because they implement the same interfaces.

Design: Each repository stores entities keyed by their ID string.
All query methods perform in-memory filtering — no external dependencies.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Optional, List, Dict
from datetime import date, timedelta

from src.models import (
    User, Student, Librarian, Resource, Loan, Reservation,
    Fine, Recommendation, Notification, Report,
    LoanStatus, ResourceStatus, ReservationStatus, NotificationStatus,
    AccountStatus
)
from repositories.interfaces import (
    UserRepository, ResourceRepository, LoanRepository,
    ReservationRepository, FineRepository, NotificationRepository,
    RecommendationRepository, ReportRepository
)


# ─────────────────────────────────────────────
# Base In-Memory Repository
# ─────────────────────────────────────────────

class InMemoryRepository:
    """
    Base class providing HashMap storage and generic CRUD for all
    in-memory repository implementations.
    """

    def __init__(self):
        self._storage: Dict[str, object] = {}

    def save(self, entity) -> None:
        entity_id = self._get_id(entity)
        self._storage[entity_id] = entity

    def find_by_id(self, entity_id: str):
        return self._storage.get(entity_id, None)

    def find_all(self) -> list:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def count(self) -> int:
        return len(self._storage)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def _get_id(self, entity) -> str:
        """Extract ID from entity using common attribute naming conventions."""
        for attr in ("user_id", "resource_id", "loan_id", "reservation_id",
                     "fine_id", "notification_id", "recommendation_id",
                     "report_id", "list_id"):
            if hasattr(entity, attr):
                return getattr(entity, attr)
        raise AttributeError(
            f"Cannot determine ID for entity of type {type(entity).__name__}"
        )

    def clear(self) -> None:
        """Clears all stored entities — used in tests for isolation."""
        self._storage.clear()


# ─────────────────────────────────────────────
# User Repository
# ─────────────────────────────────────────────

class InMemoryUserRepository(InMemoryRepository, UserRepository):
    """
    In-memory implementation of UserRepository.
    Maps to FR-01 (Authentication) and FR-10 (RBAC).
    """

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address (case-insensitive)."""
        email_lower = email.lower()
        for user in self._storage.values():
            if user.email.lower() == email_lower:
                return user
        return None

    def find_by_role(self, role: str) -> List[User]:
        """Return all users with the given role string."""
        role_upper = role.upper()
        return [
            u for u in self._storage.values()
            if u.role.value == role_upper
        ]

    def find_active_users(self) -> List[User]:
        """Return all users with ACTIVE account status."""
        return [
            u for u in self._storage.values()
            if u.account_status == AccountStatus.ACTIVE
        ]


# ─────────────────────────────────────────────
# Resource Repository
# ─────────────────────────────────────────────

class InMemoryResourceRepository(InMemoryRepository, ResourceRepository):
    """
    In-memory implementation of ResourceRepository.
    Maps to FR-02 (Search) and FR-06 (Catalogue Management).
    """

    def find_by_title(self, title: str) -> List[Resource]:
        """Case-insensitive partial title match."""
        kw = title.lower()
        return [
            r for r in self._storage.values()
            if kw in r.title.lower()
        ]

    def find_by_author(self, author: str) -> List[Resource]:
        """Case-insensitive partial author match."""
        kw = author.lower()
        return [
            r for r in self._storage.values()
            if kw in r.author.lower()
        ]

    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        """Exact ISBN match (strips hyphens and spaces)."""
        clean = isbn.replace("-", "").replace(" ", "")
        for r in self._storage.values():
            if r.isbn.replace("-", "").replace(" ", "") == clean:
                return r
        return None

    def find_available(self) -> List[Resource]:
        """Return resources with at least one available copy."""
        return [
            r for r in self._storage.values()
            if r.available_copies > 0
        ]

    def find_by_genre(self, genre: str) -> List[Resource]:
        """Case-insensitive exact genre match."""
        g = genre.lower()
        return [
            r for r in self._storage.values()
            if r._genre.lower() == g
        ]

    def search(self, keyword: str) -> List[Resource]:
        """
        Full-text search across title, author, and ISBN.
        Simulates Elasticsearch keyword search for in-memory testing.
        """
        kw = keyword.lower()
        results = []
        seen = set()
        for r in self._storage.values():
            if (kw in r.title.lower()
                    or kw in r.author.lower()
                    or kw in r.isbn.replace("-", "")):
                if r.resource_id not in seen:
                    results.append(r)
                    seen.add(r.resource_id)
        return results


# ─────────────────────────────────────────────
# Loan Repository
# ─────────────────────────────────────────────

class InMemoryLoanRepository(InMemoryRepository, LoanRepository):
    """
    In-memory implementation of LoanRepository.
    Maps to FR-03 (Borrowing), FR-04 (Dashboard), FR-07 (Notifications).
    """

    def find_by_student(self, student_id: str) -> List[Loan]:
        """Return all loans (any status) for a given student."""
        return [
            loan for loan in self._storage.values()
            if loan._student.user_id == student_id
        ]

    def find_active_by_student(self, student_id: str) -> List[Loan]:
        """Return only non-returned loans for a student."""
        active_statuses = {
            LoanStatus.ACTIVE, LoanStatus.DUE_SOON, LoanStatus.OVERDUE
        }
        return [
            loan for loan in self._storage.values()
            if (loan._student.user_id == student_id
                and loan.status in active_statuses)
        ]

    def find_overdue(self) -> List[Loan]:
        """Return all loans past their due date and not returned."""
        return [
            loan for loan in self._storage.values()
            if loan.is_overdue()
        ]

    def find_due_within_days(self, days: int) -> List[Loan]:
        """Return active loans due within the specified number of days."""
        cutoff = date.today() + timedelta(days=days)
        return [
            loan for loan in self._storage.values()
            if (loan.status in {LoanStatus.ACTIVE, LoanStatus.DUE_SOON}
                and loan.due_date <= cutoff
                and loan.due_date >= date.today())
        ]

    def find_by_resource(self, resource_id: str) -> List[Loan]:
        """Return all active loans for a specific resource."""
        return [
            loan for loan in self._storage.values()
            if (loan.resource.resource_id == resource_id
                and loan.status != LoanStatus.RETURNED
                and loan.status != LoanStatus.ARCHIVED)
        ]


# ─────────────────────────────────────────────
# Reservation Repository
# ─────────────────────────────────────────────

class InMemoryReservationRepository(InMemoryRepository, ReservationRepository):
    """
    In-memory implementation of ReservationRepository.
    Maps to FR-03 (Reservation Management).
    """

    def find_by_student(self, student_id: str) -> List[Reservation]:
        return [
            r for r in self._storage.values()
            if r._student.user_id == student_id
        ]

    def find_active_by_resource(self, resource_id: str) -> List[Reservation]:
        """Return non-expired, non-cancelled reservations for a resource."""
        active = {ReservationStatus.PENDING, ReservationStatus.CONFIRMED,
                  ReservationStatus.QUEUED}
        return [
            r for r in self._storage.values()
            if (r._resource.resource_id == resource_id
                and r.status in active)
        ]

    def find_expired(self) -> List[Reservation]:
        """Return all expired reservations."""
        return [
            r for r in self._storage.values()
            if r.is_expired()
            and r.status not in {
                ReservationStatus.CANCELLED, ReservationStatus.COLLECTED
            }
        ]

    def find_queue_for_resource(self, resource_id: str) -> List[Reservation]:
        """Return QUEUED reservations sorted by queue position."""
        queued = [
            r for r in self._storage.values()
            if (r._resource.resource_id == resource_id
                and r.status == ReservationStatus.QUEUED)
        ]
        return sorted(queued, key=lambda r: r._queue_position)


# ─────────────────────────────────────────────
# Fine Repository
# ─────────────────────────────────────────────

class InMemoryFineRepository(InMemoryRepository, FineRepository):
    """
    In-memory implementation of FineRepository.
    Maps to FR-03 (borrowing eligibility).
    """

    def find_by_student(self, student_id: str) -> List[Fine]:
        return [
            f for f in self._storage.values()
            if f._loan._student.user_id == student_id
        ]

    def find_pending_by_student(self, student_id: str) -> List[Fine]:
        from src.models import FineStatus
        return [
            f for f in self._storage.values()
            if (f._loan._student.user_id == student_id
                and f.status == FineStatus.PENDING)
        ]

    def find_by_loan(self, loan_id: str) -> Optional[Fine]:
        for f in self._storage.values():
            if f._loan.loan_id == loan_id:
                return f
        return None


# ─────────────────────────────────────────────
# Notification Repository
# ─────────────────────────────────────────────

class InMemoryNotificationRepository(InMemoryRepository, NotificationRepository):
    """
    In-memory implementation of NotificationRepository.
    Maps to FR-07 (Automated Notifications).
    """

    def find_by_user(self, user_id: str) -> List[Notification]:
        return [
            n for n in self._storage.values()
            if n._user.user_id == user_id
        ]

    def find_scheduled(self) -> List[Notification]:
        return [
            n for n in self._storage.values()
            if n.status == NotificationStatus.SCHEDULED
        ]

    def find_failed(self) -> List[Notification]:
        return [
            n for n in self._storage.values()
            if n.status == NotificationStatus.FAILED
        ]


# ─────────────────────────────────────────────
# Recommendation Repository
# ─────────────────────────────────────────────

class InMemoryRecommendationRepository(
        InMemoryRepository, RecommendationRepository):
    """
    In-memory implementation of RecommendationRepository.
    Maps to FR-05 (Personalized Recommendations).
    """

    def find_by_student(self, student_id: str) -> List[Recommendation]:
        return [
            r for r in self._storage.values()
            if r._student.user_id == student_id
        ]

    def find_ready_by_student(self, student_id: str) -> List[Recommendation]:
        return [
            r for r in self._storage.values()
            if (r._student.user_id == student_id
                and r._status == "READY")
        ]


# ─────────────────────────────────────────────
# Report Repository
# ─────────────────────────────────────────────

class InMemoryReportRepository(InMemoryRepository, ReportRepository):
    """
    In-memory implementation of ReportRepository.
    Maps to FR-08 (Usage Reporting).
    """

    def find_by_type(self, report_type: str) -> List[Report]:
        return [
            r for r in self._storage.values()
            if r.report_type == report_type
        ]

    def find_ready(self) -> List[Report]:
        return [
            r for r in self._storage.values()
            if r.status == "READY"
        ]
