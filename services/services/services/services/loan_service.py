"""
services/loan_service.py
LoanService — encapsulates all business logic for Loan operations.

Uses LoanRepository, ResourceRepository, and UserRepository.
Enforces BR-01 (max 5 loans), BR-02 (fine threshold), BR-09 (renewal).
Maps to: FR-03 (Borrowing), FR-04 (Dashboard), FR-07 (Notifications).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import List
from datetime import date
from src.models import Loan, Student, Resource, LoanStatus
from repositories.interfaces import (
    LoanRepository, UserRepository, ResourceRepository
)


class LoanNotFoundError(Exception):
    pass


class StudentNotEligibleError(Exception):
    pass


class ResourceUnavailableError(Exception):
    pass


class LoanAlreadyReturnedError(Exception):
    pass


class LoanService:
    """
    Service class encapsulating all Loan business operations.

    Enforces:
    - BR-01: Max 5 active loans per student
    - BR-02: Borrowing blocked if fines exceed R100
    - BR-10: Fine = R5/day, capped at R200

    Usage:
        loan_service = LoanService(loan_repo, user_repo, resource_repo)
        loan = loan_service.checkout(student_id, resource_id)
    """

    def __init__(self, loan_repository: LoanRepository,
                 user_repository: UserRepository,
                 resource_repository: ResourceRepository):
        self._loan_repo = loan_repository
        self._user_repo = user_repository
        self._resource_repo = resource_repository

    # ── Checkout ───────────────────────────────────────────────────────────

    def checkout(self, student_id: str, resource_id: str) -> Loan:
        """
        Checks out a resource to a student.

        Business rules enforced:
        - Student must exist and be ACTIVE
        - Student must be eligible (BR-01, BR-02)
        - Resource must be available

        Maps to FR-03, UC03.
        """
        # Validate student
        student = self._get_student(student_id)

        # Validate resource
        resource = self._resource_repo.find_by_id(resource_id)
        if not resource:
            raise ResourceUnavailableError(
                f"Resource '{resource_id}' not found."
            )

        # Check eligibility (BR-01 and BR-02)
        active_loans = self._loan_repo.find_active_by_student(student_id)
        if len(active_loans) >= Student.MAX_ACTIVE_LOANS:
            raise StudentNotEligibleError(
                f"Student has reached the maximum of "
                f"{Student.MAX_ACTIVE_LOANS} active loans (BR-01)."
            )
        if student.outstanding_fines > Student.FINE_BLOCK_THRESHOLD:
            raise StudentNotEligibleError(
                f"Student has outstanding fines of "
                f"R{student.outstanding_fines:.2f} exceeding R100 (BR-02)."
            )

        # Check availability
        if not resource.check_availability():
            raise ResourceUnavailableError(
                f"Resource '{resource_id}' has no available copies."
            )

        # Create the loan
        loan_id = f"loan_{student_id}_{resource_id}_{date.today()}"
        loan = Loan(loan_id=loan_id, student=student, resource=resource)
        resource.check_out()

        # Persist both
        self._loan_repo.save(loan)
        self._resource_repo.save(resource)
        self._user_repo.save(student)

        return loan

    # ── Return ─────────────────────────────────────────────────────────────

    def return_loan(self, loan_id: str) -> Loan:
        """
        Processes a book return.
        Calculates and records fine if overdue (BR-10).
        Maps to UC12, FR-03.
        """
        loan = self._get_loan(loan_id)

        if loan.status == LoanStatus.RETURNED:
            raise LoanAlreadyReturnedError(
                f"Loan '{loan_id}' has already been returned."
            )

        loan.return_loan()

        # Persist updated loan and resource
        self._loan_repo.save(loan)
        self._resource_repo.save(loan.resource)
        self._user_repo.save(loan._student)

        return loan

    # ── Renewal ────────────────────────────────────────────────────────────

    def renew_loan(self, loan_id: str) -> Loan:
        """
        Renews a loan for an additional 14 days.
        Blocked if the resource has active reservations (BR-09).
        """
        loan = self._get_loan(loan_id)

        if loan.status == LoanStatus.RETURNED:
            raise LoanAlreadyReturnedError(
                f"Cannot renew returned loan '{loan_id}'."
            )

        success = loan.renew_loan()
        if not success:
            raise StudentNotEligibleError(
                f"Loan '{loan_id}' cannot be renewed."
            )

        self._loan_repo.save(loan)
        return loan

    # ── Read ───────────────────────────────────────────────────────────────

    def get_loan(self, loan_id: str) -> Loan:
        """Retrieve a loan by ID."""
        return self._get_loan(loan_id)

    def get_all_loans(self) -> List[Loan]:
        """Return all loans."""
        return self._loan_repo.find_all()

    def get_student_loans(self, student_id: str) -> List[Loan]:
        """Return all loans for a student (FR-04 Dashboard)."""
        return self._loan_repo.find_by_student(student_id)

    def get_active_loans(self, student_id: str) -> List[Loan]:
        """Return only active loans for a student."""
        return self._loan_repo.find_active_by_student(student_id)

    def get_overdue_loans(self) -> List[Loan]:
        """Return all overdue loans (used by FR-07 notification scheduler)."""
        return self._loan_repo.find_overdue()

    def get_loans_due_within(self, days: int) -> List[Loan]:
        """Return loans due within N days (for DueSoon notifications)."""
        if days < 0:
            raise ValueError("Days must be a non-negative integer.")
        return self._loan_repo.find_due_within_days(days)

    def get_fine_summary(self, loan_id: str) -> dict:
        """
        Returns fine information for a loan.
        Maps to BR-10: R5/day capped at R200.
        """
        loan = self._get_loan(loan_id)
        fine_amount = loan.calculate_fine()
        return {
            "loan_id": loan_id,
            "is_overdue": loan.is_overdue(),
            "due_date": str(loan.due_date),
            "fine_amount": fine_amount,
            "fine_currency": "ZAR",
            "borrowing_blocked": fine_amount > Student.FINE_BLOCK_THRESHOLD
        }

    # ── Private Helpers ────────────────────────────────────────────────────

    def _get_loan(self, loan_id: str) -> Loan:
        loan = self._loan_repo.find_by_id(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan '{loan_id}' not found.")
        return loan

    def _get_student(self, student_id: str) -> Student:
        user = self._user_repo.find_by_id(student_id)
        if not user:
            raise StudentNotEligibleError(
                f"Student '{student_id}' not found."
            )
        if not isinstance(user, Student):
            raise StudentNotEligibleError(
                f"User '{student_id}' is not a student."
            )
        return user
