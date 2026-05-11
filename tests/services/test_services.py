"""
tests/services/test_services.py
Unit tests for UserService, ResourceService, and LoanService.

Run with: pytest tests/services/test_services.py -v --tb=short
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from datetime import timedelta, date

from src.models import Student, Librarian, Resource, Loan, LoanStatus
from repositories.inmemory.inmemory_repositories import (
    InMemoryUserRepository, InMemoryResourceRepository,
    InMemoryLoanRepository
)
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


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def user_repo():
    return InMemoryUserRepository()

@pytest.fixture
def resource_repo():
    return InMemoryResourceRepository()

@pytest.fixture
def loan_repo():
    return InMemoryLoanRepository()

@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)

@pytest.fixture
def resource_service(resource_repo, loan_repo):
    return ResourceService(resource_repo, loan_repo)

@pytest.fixture
def loan_service(loan_repo, user_repo, resource_repo):
    return LoanService(loan_repo, user_repo, resource_repo)

@pytest.fixture
def registered_student(user_service):
    return user_service.register_student(
        "s001", "Alice Dlamini", "alice@university.ac.za",
        "Pass@123", "211001", ["CS"]
    )

@pytest.fixture
def registered_resource(resource_service):
    return resource_service.add_resource(
        "r001", "Clean Code", "Robert C. Martin",
        "9780132350884", "Software Engineering", 2008, 3, "CS Shelf 4B"
    )


# ══════════════════════════════════════════════════════════════════════════════
# USER SERVICE TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestUserService:

    def test_register_student_success(self, user_service):
        student = user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        assert isinstance(student, Student)
        assert student.user_id == "s001"
        assert student.email == "alice@university.ac.za"

    def test_register_librarian_success(self, user_service):
        lib = user_service.register_librarian(
            "l001", "Bob", "bob@university.ac.za",
            "Staff@456", "LIB001", "Reference"
        )
        assert isinstance(lib, Librarian)

    def test_register_invalid_email_domain(self, user_service):
        with pytest.raises(ValueError, match="university domain"):
            user_service.register_student(
                "s002", "Eve", "eve@gmail.com",
                "Pass@123", "211002"
            )

    def test_register_duplicate_email(self, user_service):
        user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        with pytest.raises(UserAlreadyExistsError):
            user_service.register_student(
                "s002", "Alice2", "alice@university.ac.za",
                "Pass@456", "211002"
            )

    def test_login_success(self, user_service):
        user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        user = user_service.login("alice@university.ac.za", "Pass@123")
        assert user.user_id == "s001"

    def test_login_wrong_password(self, user_service):
        user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        with pytest.raises(InvalidCredentialsError):
            user_service.login("alice@university.ac.za", "wrong")

    def test_login_nonexistent_user(self, user_service):
        with pytest.raises(InvalidCredentialsError):
            user_service.login("nobody@university.ac.za", "Pass@123")

    def test_account_locked_after_5_failures(self, user_service):
        user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        for _ in range(5):
            try:
                user_service.login("alice@university.ac.za", "wrong")
            except InvalidCredentialsError:
                pass
        with pytest.raises(AccountLockedError):
            user_service.login("alice@university.ac.za", "Pass@123")

    def test_get_user_success(self, user_service, registered_student):
        user = user_service.get_user("s001")
        assert user.user_id == "s001"

    def test_get_user_not_found(self, user_service):
        with pytest.raises(UserNotFoundError):
            user_service.get_user("nonexistent")

    def test_get_all_users(self, user_service, registered_student):
        user_service.register_librarian(
            "l001", "Bob", "bob@university.ac.za",
            "Staff@456", "LIB001", "Reference"
        )
        all_users = user_service.get_all_users()
        assert len(all_users) == 2

    def test_get_users_by_role(self, user_service, registered_student):
        user_service.register_librarian(
            "l001", "Bob", "bob@university.ac.za",
            "Staff@456", "LIB001", "Reference"
        )
        students = user_service.get_users_by_role("STUDENT")
        assert len(students) == 1

    def test_update_profile(self, user_service, registered_student):
        updated = user_service.update_profile("s001", name="Alice Updated")
        assert updated.name == "Alice Updated"

    def test_deactivate_user(self, user_service, registered_student):
        from src.models import AccountStatus
        user = user_service.deactivate_user("s001")
        assert user.account_status == AccountStatus.DEACTIVATED

    def test_delete_user(self, user_service, registered_student):
        user_service.delete_user("s001")
        with pytest.raises(UserNotFoundError):
            user_service.get_user("s001")

    def test_delete_nonexistent_user(self, user_service):
        with pytest.raises(UserNotFoundError):
            user_service.delete_user("ghost")

    def test_find_by_email(self, user_service, registered_student):
        user = user_service.find_by_email("alice@university.ac.za")
        assert user is not None
        assert user.user_id == "s001"


# ══════════════════════════════════════════════════════════════════════════════
# RESOURCE SERVICE TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestResourceService:

    def test_add_resource_valid_isbn(self, resource_service):
        r = resource_service.add_resource(
            "r001", "Clean Code", "R. Martin",
            "9780132350884", "SE", 2008, 3, "Shelf 4B"
        )
        assert r.resource_id == "r001"
        assert r.title == "Clean Code"

    def test_add_resource_invalid_isbn(self, resource_service):
        with pytest.raises(InvalidISBNError, match="invalid"):
            resource_service.add_resource(
                "r_bad", "Bad Book", "Author",
                "1234567890", "General", 2020, 1, "Shelf"
            )

    def test_add_resource_zero_copies(self, resource_service):
        with pytest.raises(Exception):
            resource_service.add_resource(
                "r001", "Test", "Author",
                "9780132350884", "General", 2020, 0, "Shelf"
            )

    def test_get_resource_success(self, resource_service, registered_resource):
        r = resource_service.get_resource("r001")
        assert r.title == "Clean Code"

    def test_get_resource_not_found(self, resource_service):
        with pytest.raises(ResourceNotFoundError):
            resource_service.get_resource("ghost")

    def test_get_all_resources(self, resource_service, registered_resource):
        resource_service.add_resource(
            "r002", "Design Patterns", "GoF",
            "9780201633610", "SE", 1994, 2, "Shelf 4C"
        )
        all_r = resource_service.get_all_resources()
        assert len(all_r) == 2

    def test_search_by_keyword(self, resource_service, registered_resource):
        results = resource_service.search("clean")
        assert len(results) == 1
        assert results[0].title == "Clean Code"

    def test_search_empty_keyword(self, resource_service):
        with pytest.raises(ValueError, match="empty"):
            resource_service.search("")

    def test_get_available_resources(
            self, resource_service, registered_resource):
        results = resource_service.get_available_resources()
        assert len(results) == 1

    def test_get_available_excludes_zero_copies(
            self, resource_service, registered_resource):
        registered_resource._available_copies = 0
        resource_service._repo.save(registered_resource)
        results = resource_service.get_available_resources()
        assert len(results) == 0

    def test_get_by_genre(self, resource_service, registered_resource):
        results = resource_service.get_by_genre("Software Engineering")
        assert len(results) == 1

    def test_update_resource(self, resource_service, registered_resource):
        updated = resource_service.update_resource(
            "r001", title="Clean Code 2nd Ed", total_copies=5
        )
        assert updated.title == "Clean Code 2nd Ed"
        assert updated._total_copies == 5

    def test_update_resource_invalid_copies(
            self, resource_service, registered_resource):
        with pytest.raises(ValueError):
            resource_service.update_resource("r001", total_copies=0)

    def test_delete_resource_no_loans(
            self, resource_service, registered_resource):
        resource_service.delete_resource("r001")
        with pytest.raises(ResourceNotFoundError):
            resource_service.get_resource("r001")

    def test_delete_resource_with_active_loans(
            self, resource_service, registered_resource,
            user_service, loan_service):
        user_service.register_student(
            "s001", "Alice", "alice@university.ac.za",
            "Pass@123", "211001"
        )
        loan_service.checkout("s001", "r001")
        with pytest.raises(ResourceHasActiveLoansError):
            resource_service.delete_resource("r001")

    def test_check_availability(self, resource_service, registered_resource):
        info = resource_service.check_availability("r001")
        assert info["is_available"] is True
        assert info["available_copies"] == 3

    def test_check_availability_not_found(self, resource_service):
        with pytest.raises(ResourceNotFoundError):
            resource_service.check_availability("ghost")


# ══════════════════════════════════════════════════════════════════════════════
# LOAN SERVICE TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestLoanService:

    @pytest.fixture(autouse=True)
    def setup(self, user_service, resource_service,
              registered_student, registered_resource):
        self.student = registered_student
        self.resource = registered_resource

    def test_checkout_success(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        assert isinstance(loan, Loan)
        assert loan.status == LoanStatus.ACTIVE
        assert loan._student.user_id == "s001"

    def test_checkout_decrements_copies(self, loan_service, resource_repo):
        loan_service.checkout("s001", "r001")
        r = resource_repo.find_by_id("r001")
        assert r.available_copies == 2

    def test_checkout_student_not_found(self, loan_service):
        with pytest.raises(StudentNotEligibleError, match="not found"):
            loan_service.checkout("ghost", "r001")

    def test_checkout_resource_not_found(self, loan_service):
        with pytest.raises(ResourceUnavailableError, match="not found"):
            loan_service.checkout("s001", "ghost")

    def test_checkout_resource_unavailable(self, loan_service):
        self.resource._available_copies = 0
        loan_service._resource_repo.save(self.resource)
        with pytest.raises(ResourceUnavailableError, match="no available"):
            loan_service.checkout("s001", "r001")

    def test_checkout_max_loans_enforced(
            self, loan_service, resource_service):
        """BR-01: Maximum 5 active loans per student."""
        # Borrow r001 first, then 4 more = 5 total (hits limit)
        loan_service.checkout("s001", "r001")
        for i in range(2, 6):
            resource_service.add_resource(
                f"r00{i}", f"Book {i}", "Author",
                "9780132350884", "General", 2020, 1, "Shelf"
            )
            loan_service.checkout("s001", f"r00{i}")
        # 6th checkout should be blocked
        resource_service.add_resource(
            "r006", "Book 6", "Author",
            "9780132350884", "General", 2020, 1, "Shelf"
        )
        with pytest.raises(StudentNotEligibleError, match="maximum"):
            loan_service.checkout("s001", "r006")

    def test_checkout_fine_blocks_borrowing(self, loan_service, user_repo):
        self.student.add_fine(150.0)
        user_repo.save(self.student)
        with pytest.raises(StudentNotEligibleError, match="fines"):
            loan_service.checkout("s001", "r001")

    def test_return_loan(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        returned = loan_service.return_loan(loan.loan_id)
        assert returned.status == LoanStatus.RETURNED

    def test_return_increments_copies(self, loan_service, resource_repo):
        loan = loan_service.checkout("s001", "r001")
        loan_service.return_loan(loan.loan_id)
        r = resource_repo.find_by_id("r001")
        assert r.available_copies == 3

    def test_return_already_returned(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        loan_service.return_loan(loan.loan_id)
        with pytest.raises(LoanAlreadyReturnedError):
            loan_service.return_loan(loan.loan_id)

    def test_return_overdue_generates_fine(self, loan_service, user_repo):
        loan = loan_service.checkout("s001", "r001")
        loan._due_date = date.today() - timedelta(days=5)
        loan_service._loan_repo.save(loan)
        returned = loan_service.return_loan(loan.loan_id)
        assert returned.fine is not None
        assert returned.fine.amount == 25.0

    def test_renew_loan(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        original_due = loan.due_date
        renewed = loan_service.renew_loan(loan.loan_id)
        assert renewed.due_date == original_due + timedelta(days=14)

    def test_renew_returned_loan_fails(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        loan_service.return_loan(loan.loan_id)
        with pytest.raises(LoanAlreadyReturnedError):
            loan_service.renew_loan(loan.loan_id)

    def test_get_loan_success(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        found = loan_service.get_loan(loan.loan_id)
        assert found.loan_id == loan.loan_id

    def test_get_loan_not_found(self, loan_service):
        with pytest.raises(LoanNotFoundError):
            loan_service.get_loan("ghost")

    def test_get_student_loans(self, loan_service):
        loan_service.checkout("s001", "r001")
        loans = loan_service.get_student_loans("s001")
        assert len(loans) == 1

    def test_get_overdue_loans(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        loan._due_date = date.today() - timedelta(days=3)
        loan_service._loan_repo.save(loan)
        overdue = loan_service.get_overdue_loans()
        assert len(overdue) == 1

    def test_get_fine_summary_no_fine(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        summary = loan_service.get_fine_summary(loan.loan_id)
        assert summary["fine_amount"] == 0.0
        assert summary["is_overdue"] is False

    def test_get_fine_summary_overdue(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        loan._due_date = date.today() - timedelta(days=4)
        loan_service._loan_repo.save(loan)
        summary = loan_service.get_fine_summary(loan.loan_id)
        assert summary["fine_amount"] == 20.0
        assert summary["is_overdue"] is True

    def test_get_loans_due_within(self, loan_service):
        loan = loan_service.checkout("s001", "r001")
        loan._due_date = date.today() + timedelta(days=2)
        loan_service._loan_repo.save(loan)
        results = loan_service.get_loans_due_within(3)
        assert len(results) == 1

    def test_get_loans_due_within_negative_raises(self, loan_service):
        with pytest.raises(ValueError):
            loan_service.get_loans_due_within(-1)
