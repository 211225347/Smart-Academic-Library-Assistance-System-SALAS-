"""
repositories/inmemory/inmemory_repositories.py
In-memory HashMap implementations of all repository interfaces.

Each class implements the entity-specific interface which extends
Repository[T, ID] from base_repository.py.

Extra helper methods (count, exists, clear) are only on the concrete
classes — NOT on the base interface — to avoid strict-marking issues.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from typing import Optional, List, Dict
from datetime import date, timedelta, datetime

from src.models import (
    User, Resource, Loan, Reservation, Fine,
    Recommendation, Notification, Report,
    LoanStatus, ReservationStatus, NotificationStatus,
    AccountStatus, FineStatus
)
from repositories.interfaces import (
    UserRepository, ResourceRepository, LoanRepository,
    ReservationRepository, FineRepository, NotificationRepository,
    RecommendationRepository, ReportRepository
)


class InMemoryUserRepository(UserRepository):
    """
    In-memory HashMap implementation of UserRepository.
    Maps to FR-01 (Authentication) and FR-10 (RBAC).
    """

    def __init__(self):
        self._storage: Dict[str, User] = {}

    def save(self, user: User) -> None:
        self._storage[user.user_id] = user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._storage.get(user_id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def delete(self, user_id: str) -> None:
        self._storage.pop(user_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_email(self, email: str) -> Optional[User]:
        email_lower = email.lower()
        for user in self._storage.values():
            if user.email.lower() == email_lower:
                return user
        return None

    def find_by_role(self, role: str) -> List[User]:
        role_upper = role.upper()
        return [u for u in self._storage.values()
                if u.role.value == role_upper]

    def find_active_users(self) -> List[User]:
        return [u for u in self._storage.values()
                if u.account_status == AccountStatus.ACTIVE]

    # ── Concrete-only helpers (NOT on interface) ──────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, user_id: str) -> bool:
        return user_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryResourceRepository(ResourceRepository):
    """
    In-memory HashMap implementation of ResourceRepository.
    Maps to FR-02 (Search) and FR-06 (Catalogue Management).
    """

    def __init__(self):
        self._storage: Dict[str, Resource] = {}

    def save(self, resource: Resource) -> None:
        self._storage[resource.resource_id] = resource

    def find_by_id(self, resource_id: str) -> Optional[Resource]:
        return self._storage.get(resource_id)

    def find_all(self) -> List[Resource]:
        return list(self._storage.values())

    def delete(self, resource_id: str) -> None:
        self._storage.pop(resource_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_title(self, title: str) -> List[Resource]:
        kw = title.lower()
        return [r for r in self._storage.values()
                if kw in r.title.lower()]

    def find_by_author(self, author: str) -> List[Resource]:
        kw = author.lower()
        return [r for r in self._storage.values()
                if kw in r.author.lower()]

    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        clean = isbn.replace("-", "").replace(" ", "")
        for r in self._storage.values():
            if r.isbn.replace("-", "").replace(" ", "") == clean:
                return r
        return None

    def find_available(self) -> List[Resource]:
        return [r for r in self._storage.values()
                if r.available_copies > 0]

    def find_by_genre(self, genre: str) -> List[Resource]:
        return [r for r in self._storage.values()
                if r._genre.lower() == genre.lower()]

    def search(self, keyword: str) -> List[Resource]:
        kw = keyword.lower()
        seen = set()
        results = []
        for r in self._storage.values():
            if (kw in r.title.lower()
                    or kw in r.author.lower()
                    or kw in r.isbn.replace("-", "")):
                if r.resource_id not in seen:
                    results.append(r)
                    seen.add(r.resource_id)
        return results

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, resource_id: str) -> bool:
        return resource_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryLoanRepository(LoanRepository):
    """
    In-memory HashMap implementation of LoanRepository.
    Maps to FR-03, FR-04, FR-07.
    """

    def __init__(self):
        self._storage: Dict[str, Loan] = {}

    def save(self, loan: Loan) -> None:
        self._storage[loan.loan_id] = loan

    def find_by_id(self, loan_id: str) -> Optional[Loan]:
        return self._storage.get(loan_id)

    def find_all(self) -> List[Loan]:
        return list(self._storage.values())

    def delete(self, loan_id: str) -> None:
        self._storage.pop(loan_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_student(self, student_id: str) -> List[Loan]:
        return [l for l in self._storage.values()
                if l._student.user_id == student_id]

    def find_active_by_student(self, student_id: str) -> List[Loan]:
        active = {LoanStatus.ACTIVE, LoanStatus.DUE_SOON, LoanStatus.OVERDUE}
        return [l for l in self._storage.values()
                if l._student.user_id == student_id
                and l.status in active]

    def find_overdue(self) -> List[Loan]:
        return [l for l in self._storage.values() if l.is_overdue()]

    def find_due_within_days(self, days: int) -> List[Loan]:
        cutoff = date.today() + timedelta(days=days)
        return [l for l in self._storage.values()
                if (l.status in {LoanStatus.ACTIVE, LoanStatus.DUE_SOON}
                    and l.due_date <= cutoff
                    and l.due_date >= date.today())]

    def find_by_resource(self, resource_id: str) -> List[Loan]:
        return [l for l in self._storage.values()
                if (l.resource.resource_id == resource_id
                    and l.status not in {
                        LoanStatus.RETURNED, LoanStatus.ARCHIVED})]

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, loan_id: str) -> bool:
        return loan_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryReservationRepository(ReservationRepository):
    """
    In-memory HashMap implementation of ReservationRepository.
    Maps to FR-03.
    """

    def __init__(self):
        self._storage: Dict[str, Reservation] = {}

    def save(self, reservation: Reservation) -> None:
        self._storage[reservation.reservation_id] = reservation

    def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        return self._storage.get(reservation_id)

    def find_all(self) -> List[Reservation]:
        return list(self._storage.values())

    def delete(self, reservation_id: str) -> None:
        self._storage.pop(reservation_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_student(self, student_id: str) -> List[Reservation]:
        return [r for r in self._storage.values()
                if r._student.user_id == student_id]

    def find_active_by_resource(self, resource_id: str) -> List[Reservation]:
        active = {ReservationStatus.PENDING, ReservationStatus.CONFIRMED,
                  ReservationStatus.QUEUED}
        return [r for r in self._storage.values()
                if r._resource.resource_id == resource_id
                and r.status in active]

    def find_expired(self) -> List[Reservation]:
        return [r for r in self._storage.values()
                if r.is_expired()
                and r.status not in {
                    ReservationStatus.CANCELLED,
                    ReservationStatus.COLLECTED}]

    def find_queue_for_resource(self, resource_id: str) -> List[Reservation]:
        queued = [r for r in self._storage.values()
                  if r._resource.resource_id == resource_id
                  and r.status == ReservationStatus.QUEUED]
        return sorted(queued, key=lambda r: r._queue_position)

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, reservation_id: str) -> bool:
        return reservation_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryFineRepository(FineRepository):
    """
    In-memory HashMap implementation of FineRepository.
    Maps to FR-03 (borrowing eligibility).
    """

    def __init__(self):
        self._storage: Dict[str, Fine] = {}

    def save(self, fine: Fine) -> None:
        self._storage[fine.fine_id] = fine

    def find_by_id(self, fine_id: str) -> Optional[Fine]:
        return self._storage.get(fine_id)

    def find_all(self) -> List[Fine]:
        return list(self._storage.values())

    def delete(self, fine_id: str) -> None:
        self._storage.pop(fine_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_student(self, student_id: str) -> List[Fine]:
        return [f for f in self._storage.values()
                if f._loan._student.user_id == student_id]

    def find_pending_by_student(self, student_id: str) -> List[Fine]:
        return [f for f in self._storage.values()
                if f._loan._student.user_id == student_id
                and f.status == FineStatus.PENDING]

    def find_by_loan(self, loan_id: str) -> Optional[Fine]:
        for f in self._storage.values():
            if f._loan.loan_id == loan_id:
                return f
        return None

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, fine_id: str) -> bool:
        return fine_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryNotificationRepository(NotificationRepository):
    """
    In-memory HashMap implementation of NotificationRepository.
    Maps to FR-07.
    """

    def __init__(self):
        self._storage: Dict[str, Notification] = {}

    def save(self, notification: Notification) -> None:
        self._storage[notification.notification_id] = notification

    def find_by_id(self, notification_id: str) -> Optional[Notification]:
        return self._storage.get(notification_id)

    def find_all(self) -> List[Notification]:
        return list(self._storage.values())

    def delete(self, notification_id: str) -> None:
        self._storage.pop(notification_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_user(self, user_id: str) -> List[Notification]:
        return [n for n in self._storage.values()
                if n._user.user_id == user_id]

    def find_scheduled(self) -> List[Notification]:
        return [n for n in self._storage.values()
                if n.status == NotificationStatus.SCHEDULED]

    def find_failed(self) -> List[Notification]:
        return [n for n in self._storage.values()
                if n.status == NotificationStatus.FAILED]

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, notification_id: str) -> bool:
        return notification_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryRecommendationRepository(RecommendationRepository):
    """
    In-memory HashMap implementation of RecommendationRepository.
    Maps to FR-05.
    """

    def __init__(self):
        self._storage: Dict[str, Recommendation] = {}

    def save(self, recommendation: Recommendation) -> None:
        self._storage[recommendation.recommendation_id] = recommendation

    def find_by_id(self, recommendation_id: str) -> Optional[Recommendation]:
        return self._storage.get(recommendation_id)

    def find_all(self) -> List[Recommendation]:
        return list(self._storage.values())

    def delete(self, recommendation_id: str) -> None:
        self._storage.pop(recommendation_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_student(self, student_id: str) -> List[Recommendation]:
        return [r for r in self._storage.values()
                if r._student.user_id == student_id]

    def find_ready_by_student(self, student_id: str) -> List[Recommendation]:
        return [r for r in self._storage.values()
                if r._student.user_id == student_id
                and r._status == "READY"]

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, recommendation_id: str) -> bool:
        return recommendation_id in self._storage

    def clear(self) -> None:
        self._storage.clear()


class InMemoryReportRepository(ReportRepository):
    """
    In-memory HashMap implementation of ReportRepository.
    Maps to FR-08.
    """

    def __init__(self):
        self._storage: Dict[str, Report] = {}

    def save(self, report: Report) -> None:
        self._storage[report.report_id] = report

    def find_by_id(self, report_id: str) -> Optional[Report]:
        return self._storage.get(report_id)

    def find_all(self) -> List[Report]:
        return list(self._storage.values())

    def delete(self, report_id: str) -> None:
        self._storage.pop(report_id, None)

    # ── Domain-specific queries ───────────────────────────────────────────

    def find_by_type(self, report_type: str) -> List[Report]:
        return [r for r in self._storage.values()
                if r.report_type == report_type]

    def find_ready(self) -> List[Report]:
        return [r for r in self._storage.values()
                if r.status == "READY"]

    # ── Concrete-only helpers ─────────────────────────────────────────────

    def count(self) -> int:
        return len(self._storage)

    def exists(self, report_id: str) -> bool:
        return report_id in self._storage

    def clear(self) -> None:
        self._storage.clear()
