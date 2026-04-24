"""
repositories/interfaces.py
Generic and entity-specific repository interfaces for SALAS.

Design Rationale:
- Generic Repository[T, ID] avoids code duplication across all entity repos.
- Entity-specific interfaces add domain-relevant query methods beyond basic CRUD.
- All interfaces are pure Python ABCs — no storage details leak into the contract.
- Any storage backend (in-memory, filesystem, database, REST API) must implement
  these interfaces, making swapping trivial.

Maps to:
  FR-01 (User auth), FR-02 (Search), FR-03 (Borrow/Reserve),
  FR-04 (Dashboard), FR-05 (Recommendations), FR-06 (Catalogue),
  FR-07 (Notifications), FR-08 (Reports)
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import (
    User, Student, Librarian, Resource, Loan, Reservation,
    Fine, ReadingList, Recommendation, Notification, Report,
    LoanStatus, ResourceStatus, ReservationStatus, NotificationStatus
)

# ─────────────────────────────────────────────
# Generic Base Interface
# ─────────────────────────────────────────────

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """
    Generic CRUD repository interface.
    All entity-specific repositories extend this.

    Generic parameters:
        T  — The domain entity type (e.g., Resource, Student)
        ID — The identifier type (typically str)
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity (upsert by ID)."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return entity by ID, or None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all stored entities."""
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> bool:
        """
        Delete entity by ID.
        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Return total number of stored entities."""
        pass

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with the given ID exists."""
        pass


# ─────────────────────────────────────────────
# Entity-Specific Interfaces
# ─────────────────────────────────────────────

class UserRepository(Repository[User, str], ABC):
    """
    Repository interface for User entities (Student and Librarian).
    Maps to FR-01, FR-10.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email — used during login (FR-01)."""
        pass

    @abstractmethod
    def find_by_role(self, role: str) -> List[User]:
        """Return all users with a given role (FR-10 RBAC)."""
        pass

    @abstractmethod
    def find_active_users(self) -> List[User]:
        """Return all users with ACTIVE account status."""
        pass


class ResourceRepository(Repository[Resource, str], ABC):
    """
    Repository interface for library Resource entities.
    Maps to FR-02, FR-06.
    """

    @abstractmethod
    def find_by_title(self, title: str) -> List[Resource]:
        """Search by title keyword (FR-02)."""
        pass

    @abstractmethod
    def find_by_author(self, author: str) -> List[Resource]:
        """Search by author keyword (FR-02)."""
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        """Find resource by exact ISBN — used during catalogue management (FR-06)."""
        pass

    @abstractmethod
    def find_available(self) -> List[Resource]:
        """Return all resources with at least one available copy (FR-02)."""
        pass

    @abstractmethod
    def find_by_genre(self, genre: str) -> List[Resource]:
        """Filter resources by genre (FR-02)."""
        pass

    @abstractmethod
    def search(self, keyword: str) -> List[Resource]:
        """Full-text keyword search across title, author, and ISBN (FR-02)."""
        pass


class LoanRepository(Repository[Loan, str], ABC):
    """
    Repository interface for Loan entities.
    Maps to FR-03, FR-04, FR-07.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Loan]:
        """Return all loans for a given student (FR-04 Dashboard)."""
        pass

    @abstractmethod
    def find_active_by_student(self, student_id: str) -> List[Loan]:
        """Return only active loans for a student — used for eligibility check."""
        pass

    @abstractmethod
    def find_overdue(self) -> List[Loan]:
        """Return all overdue loans — used by notification scheduler (FR-07)."""
        pass

    @abstractmethod
    def find_due_within_days(self, days: int) -> List[Loan]:
        """Return loans due within N days — used for DueSoon notifications."""
        pass

    @abstractmethod
    def find_by_resource(self, resource_id: str) -> List[Loan]:
        """Return all loans for a resource — used to block deletion (FR-06)."""
        pass


class ReservationRepository(Repository[Reservation, str], ABC):
    """
    Repository interface for Reservation entities.
    Maps to FR-03.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Reservation]:
        """Return all reservations for a given student."""
        pass

    @abstractmethod
    def find_active_by_resource(self, resource_id: str) -> List[Reservation]:
        """Return active (non-expired, non-cancelled) reservations for a resource."""
        pass

    @abstractmethod
    def find_expired(self) -> List[Reservation]:
        """Return all expired reservations — for cleanup scheduler."""
        pass

    @abstractmethod
    def find_queue_for_resource(self, resource_id: str) -> List[Reservation]:
        """Return queued reservations ordered by queue position."""
        pass


class FineRepository(Repository[Fine, str], ABC):
    """
    Repository interface for Fine entities.
    Maps to FR-03 (borrowing eligibility).
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Fine]:
        """Return all fines for a student — used for eligibility check."""
        pass

    @abstractmethod
    def find_pending_by_student(self, student_id: str) -> List[Fine]:
        """Return only PENDING (unpaid) fines for a student."""
        pass

    @abstractmethod
    def find_by_loan(self, loan_id: str) -> Optional[Fine]:
        """Return the fine associated with a specific loan."""
        pass


class NotificationRepository(Repository[Notification, str], ABC):
    """
    Repository interface for Notification entities.
    Maps to FR-07.
    """

    @abstractmethod
    def find_by_user(self, user_id: str) -> List[Notification]:
        """Return all notifications for a user."""
        pass

    @abstractmethod
    def find_scheduled(self) -> List[Notification]:
        """Return all scheduled (unsent) notifications — for the scheduler."""
        pass

    @abstractmethod
    def find_failed(self) -> List[Notification]:
        """Return all failed notifications — for retry processing."""
        pass


class RecommendationRepository(Repository[Recommendation, str], ABC):
    """
    Repository interface for Recommendation entities.
    Maps to FR-05.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Recommendation]:
        """Return all recommendations for a student (FR-04 Dashboard)."""
        pass

    @abstractmethod
    def find_ready_by_student(self, student_id: str) -> List[Recommendation]:
        """Return only READY recommendations for dashboard display."""
        pass


class ReportRepository(Repository[Report, str], ABC):
    """
    Repository interface for Report entities.
    Maps to FR-08.
    """

    @abstractmethod
    def find_by_type(self, report_type: str) -> List[Report]:
        """Return all reports of a given type."""
        pass

    @abstractmethod
    def find_ready(self) -> List[Report]:
        """Return all generated (READY) reports."""
        pass
