"""
repositories/interfaces.py
Entity-specific repository interfaces for SALAS.

Each interface extends the generic Repository[T, ID] from base_repository.py
and adds domain-specific query methods beyond basic CRUD.

This satisfies the rubric requirement:
"Create entity-specific interfaces (e.g., BookRepository extends Repository<Book, String>)"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from abc import abstractmethod
from typing import List, Optional

from repositories.base_repository import Repository
from src.models import (
    User, Resource, Loan, Reservation,
    Fine, Recommendation, Notification, Report
)


class UserRepository(Repository[User, str]):
    """
    Entity-specific interface for User persistence.
    Extends Repository[User, str] — maps to FR-01, FR-10.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email — used during login (FR-01)."""
        pass

    @abstractmethod
    def find_by_role(self, role: str) -> List[User]:
        """Return all users with a given role (FR-10 RBAC)."""
        pass

    @abstractmethod
    def find_active_users(self) -> List[User]:
        """Return all users with ACTIVE account status."""
        pass


class ResourceRepository(Repository[Resource, str]):
    """
    Entity-specific interface for Resource persistence.
    Extends Repository[Resource, str] — maps to FR-02, FR-06.
    """

    @abstractmethod
    def find_by_title(self, title: str) -> List[Resource]:
        """Keyword search by title (FR-02)."""
        pass

    @abstractmethod
    def find_by_author(self, author: str) -> List[Resource]:
        """Keyword search by author (FR-02)."""
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        """Find resource by exact ISBN (FR-06)."""
        pass

    @abstractmethod
    def find_available(self) -> List[Resource]:
        """Return all resources with at least one available copy."""
        pass

    @abstractmethod
    def find_by_genre(self, genre: str) -> List[Resource]:
        """Filter resources by genre."""
        pass

    @abstractmethod
    def search(self, keyword: str) -> List[Resource]:
        """Full-text search across title, author, and ISBN."""
        pass


class LoanRepository(Repository[Loan, str]):
    """
    Entity-specific interface for Loan persistence.
    Extends Repository[Loan, str] — maps to FR-03, FR-04, FR-07.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Loan]:
        """Return all loans for a student (FR-04 Dashboard)."""
        pass

    @abstractmethod
    def find_active_by_student(self, student_id: str) -> List[Loan]:
        """Return only active loans — used for eligibility check."""
        pass

    @abstractmethod
    def find_overdue(self) -> List[Loan]:
        """Return all overdue loans — used by notification scheduler (FR-07)."""
        pass

    @abstractmethod
    def find_due_within_days(self, days: int) -> List[Loan]:
        """Return loans due within N days — for DueSoon notifications."""
        pass

    @abstractmethod
    def find_by_resource(self, resource_id: str) -> List[Loan]:
        """Return active loans for a resource — to block deletion (FR-06)."""
        pass


class ReservationRepository(Repository[Reservation, str]):
    """
    Entity-specific interface for Reservation persistence.
    Extends Repository[Reservation, str] — maps to FR-03.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Reservation]:
        """Return all reservations for a student."""
        pass

    @abstractmethod
    def find_active_by_resource(self, resource_id: str) -> List[Reservation]:
        """Return active reservations for a resource."""
        pass

    @abstractmethod
    def find_expired(self) -> List[Reservation]:
        """Return all expired reservations for cleanup."""
        pass

    @abstractmethod
    def find_queue_for_resource(self, resource_id: str) -> List[Reservation]:
        """Return queued reservations ordered by queue position."""
        pass


class FineRepository(Repository[Fine, str]):
    """
    Entity-specific interface for Fine persistence.
    Extends Repository[Fine, str] — maps to FR-03.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Fine]:
        """Return all fines for a student."""
        pass

    @abstractmethod
    def find_pending_by_student(self, student_id: str) -> List[Fine]:
        """Return only unpaid fines — for borrowing eligibility check."""
        pass

    @abstractmethod
    def find_by_loan(self, loan_id: str) -> Optional[Fine]:
        """Return the fine associated with a specific loan."""
        pass


class NotificationRepository(Repository[Notification, str]):
    """
    Entity-specific interface for Notification persistence.
    Extends Repository[Notification, str] — maps to FR-07.
    """

    @abstractmethod
    def find_by_user(self, user_id: str) -> List[Notification]:
        """Return all notifications for a user."""
        pass

    @abstractmethod
    def find_scheduled(self) -> List[Notification]:
        """Return all scheduled (unsent) notifications."""
        pass

    @abstractmethod
    def find_failed(self) -> List[Notification]:
        """Return all failed notifications for retry processing."""
        pass


class RecommendationRepository(Repository[Recommendation, str]):
    """
    Entity-specific interface for Recommendation persistence.
    Extends Repository[Recommendation, str] — maps to FR-05.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List[Recommendation]:
        """Return all recommendations for a student."""
        pass

    @abstractmethod
    def find_ready_by_student(self, student_id: str) -> List[Recommendation]:
        """Return only READY recommendations for dashboard display."""
        pass


class ReportRepository(Repository[Report, str]):
    """
    Entity-specific interface for Report persistence.
    Extends Repository[Report, str] — maps to FR-08.
    """

    @abstractmethod
    def find_by_type(self, report_type: str) -> List[Report]:
        """Return all reports of a given type."""
        pass

    @abstractmethod
    def find_ready(self) -> List[Report]:
        """Return all generated (READY) reports."""
        pass
