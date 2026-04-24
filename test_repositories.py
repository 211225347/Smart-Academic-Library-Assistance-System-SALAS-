"""
tests/test_repositories.py
Unit tests for Assignment 11 — Repository Layer.
Tests all in-memory repository CRUD operations and the RepositoryFactory.

Run with: pytest tests/test_repositories.py -v --tb=short
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from datetime import date, timedelta, datetime

from src.models import (
    Student, Librarian, Resource, Loan, Reservation, Fine,
    Recommendation, Notification, Report,
    NotificationType, NotificationStatus, ReservationStatus,
    LoanStatus, FineStatus, AccountStatus
)
from repositories.inmemory.inmemory_repositories import (
    InMemoryUserRepository, InMemoryResourceRepository,
    InMemoryLoanRepository, InMemoryReservationRepository,
    InMemoryFineRepository, InMemoryNotificationRepository,
    InMemoryRecommendationRepository, InMemoryReportRepository
)
from factories.repository_factory import RepositoryFactory, STORAGE_MEMORY


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def student():
    return Student("s001", "Alice Dlamini", "alice@university.ac.za",
                   "Pass@123", "211001", ["Computer Science"])

@pytest.fixture
def student2():
    return Student("s002", "Bob Sithole", "bob@university.ac.za",
                   "Pass@456", "211002", ["Mathematics"])

@pytest.fixture
def librarian():
    return Librarian("l001", "Carol Nkosi", "carol@university.ac.za",
                     "Staff@789", "LIB001", "Reference")

@pytest.fixture
def resource():
    return Resource("r001", "Clean Code", "Robert C. Martin",
                    "9780132350884", "Software Engineering",
                    2008, 3, "CS Shelf 4B")

@pytest.fixture
def resource2():
    return Resource("r002", "Design Patterns", "Gang of Four",
                    "9780201633610", "Software Engineering",
                    1994, 2, "CS Shelf 4C")

@pytest.fixture
def loan(student, resource):
    resource.check_out()
    return Loan("loan_001", student, resource)

@pytest.fixture
def reservation(student, resource):
    return Reservation("res_001", student, resource)

@pytest.fixture
def fine(student, resource, loan):
    loan._due_date = date.today() - timedelta(days=5)
    return Fine("fine_001", loan, 25.0)

@pytest.fixture
def notification(student):
    return Notification("notif_001", student, NotificationType.DUE_SOON)

@pytest.fixture
def recommendation(student, resource):
    rec = Recommendation("rec_001", student, resource, score=0.95)
    rec._status = "READY"
    return rec

@pytest.fixture
def report():
    r = Report("rpt_001", "Top 20 Borrowed")
    r.generate({"rows": [{"title": "Clean Code", "borrows": 45}]})
    return r

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
def reservation_repo():
    return InMemoryReservationRepository()

@pytest.fixture
def fine_repo():
    return InMemoryFineRepository()

@pytest.fixture
def notification_repo():
    return InMemoryNotificationRepository()

@pytest.fixture
def recommendation_repo():
    return InMemoryRecommendationRepository()

@pytest.fixture
def report_repo():
    return InMemoryReportRepository()


# ══════════════════════════════════════════════════════════════════════════════
# USER REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryUserRepository:

    def test_save_and_find_by_id(self, user_repo, student):
        user_repo.save(student)
        found = user_repo.find_by_id("s001")
        assert found is student

    def test_find_by_id_returns_none_if_missing(self, user_repo):
        assert user_repo.find_by_id("nonexistent") is None

    def test_find_all_returns_all_users(self, user_repo, student, librarian):
        user_repo.save(student)
        user_repo.save(librarian)
        assert len(user_repo.find_all()) == 2

    def test_delete_existing_user(self, user_repo, student):
        user_repo.save(student)
        result = user_repo.delete("s001")
        assert result is True
        assert user_repo.find_by_id("s001") is None

    def test_delete_nonexistent_returns_false(self, user_repo):
        assert user_repo.delete("nonexistent") is False

    def test_count(self, user_repo, student, librarian):
        user_repo.save(student)
        user_repo.save(librarian)
        assert user_repo.count() == 2

    def test_exists_true(self, user_repo, student):
        user_repo.save(student)
        assert user_repo.exists("s001") is True

    def test_exists_false(self, user_repo):
        assert user_repo.exists("ghost") is False

    def test_save_updates_existing(self, user_repo, student):
        user_repo.save(student)
        student.update_profile(name="Alice Updated")
        user_repo.save(student)
        assert user_repo.count() == 1
        assert user_repo.find_by_id("s001").name == "Alice Updated"

    def test_find_by_email(self, user_repo, student):
        user_repo.save(student)
        found = user_repo.find_by_email("alice@university.ac.za")
        assert found is student

    def test_find_by_email_case_insensitive(self, user_repo, student):
        user_repo.save(student)
        found = user_repo.find_by_email("ALICE@UNIVERSITY.AC.ZA")
        assert found is student

    def test_find_by_email_not_found(self, user_repo):
        assert user_repo.find_by_email("nobody@nowhere.com") is None

    def test_find_by_role_student(self, user_repo, student, librarian):
        user_repo.save(student)
        user_repo.save(librarian)
        students = user_repo.find_by_role("STUDENT")
        assert len(students) == 1
        assert students[0] is student

    def test_find_by_role_librarian(self, user_repo, student, librarian):
        user_repo.save(student)
        user_repo.save(librarian)
        librarians = user_repo.find_by_role("LIBRARIAN")
        assert len(librarians) == 1

    def test_find_active_users(self, user_repo, student, librarian):
        user_repo.save(student)
        user_repo.save(librarian)
        librarian.deactivate_account()
        active = user_repo.find_active_users()
        assert len(active) == 1
        assert active[0] is student


# ══════════════════════════════════════════════════════════════════════════════
# RESOURCE REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryResourceRepository:

    def test_save_and_find_by_id(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.find_by_id("r001") is resource

    def test_find_all(self, resource_repo, resource, resource2):
        resource_repo.save(resource)
        resource_repo.save(resource2)
        assert len(resource_repo.find_all()) == 2

    def test_delete(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.delete("r001") is True
        assert resource_repo.find_by_id("r001") is None

    def test_count(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.count() == 1

    def test_exists(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.exists("r001") is True
        assert resource_repo.exists("r999") is False

    def test_find_by_title_partial_match(self, resource_repo, resource):
        resource_repo.save(resource)
        results = resource_repo.find_by_title("clean")
        assert len(results) == 1

    def test_find_by_title_case_insensitive(self, resource_repo, resource):
        resource_repo.save(resource)
        results = resource_repo.find_by_title("CLEAN CODE")
        assert len(results) == 1

    def test_find_by_title_no_match(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.find_by_title("quantum physics") == []

    def test_find_by_author(self, resource_repo, resource):
        resource_repo.save(resource)
        results = resource_repo.find_by_author("martin")
        assert len(results) == 1

    def test_find_by_isbn(self, resource_repo, resource):
        resource_repo.save(resource)
        found = resource_repo.find_by_isbn("9780132350884")
        assert found is resource

    def test_find_by_isbn_not_found(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.find_by_isbn("9999999999999") is None

    def test_find_available(self, resource_repo, resource, resource2):
        resource_repo.save(resource)
        resource_repo.save(resource2)
        resource2._available_copies = 0
        available = resource_repo.find_available()
        assert len(available) == 1
        assert available[0] is resource

    def test_find_by_genre(self, resource_repo, resource, resource2):
        resource_repo.save(resource)
        resource_repo.save(resource2)
        results = resource_repo.find_by_genre("Software Engineering")
        assert len(results) == 2

    def test_search_by_title_keyword(self, resource_repo, resource):
        resource_repo.save(resource)
        results = resource_repo.search("clean")
        assert len(results) == 1

    def test_search_by_author_keyword(self, resource_repo, resource):
        resource_repo.save(resource)
        results = resource_repo.search("martin")
        assert len(results) == 1

    def test_search_no_results(self, resource_repo, resource):
        resource_repo.save(resource)
        assert resource_repo.search("zzz_no_match_zzz") == []

    def test_search_no_duplicates(self, resource_repo, resource):
        """A resource matching title AND author should only appear once."""
        resource_repo.save(resource)
        results = resource_repo.search("c")
        ids = [r.resource_id for r in results]
        assert len(ids) == len(set(ids))


# ══════════════════════════════════════════════════════════════════════════════
# LOAN REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryLoanRepository:

    def test_save_and_find_by_id(self, loan_repo, loan):
        loan_repo.save(loan)
        assert loan_repo.find_by_id("loan_001") is loan

    def test_delete(self, loan_repo, loan):
        loan_repo.save(loan)
        assert loan_repo.delete("loan_001") is True

    def test_find_by_student(self, loan_repo, loan, student):
        loan_repo.save(loan)
        results = loan_repo.find_by_student("s001")
        assert len(results) == 1

    def test_find_by_student_empty(self, loan_repo):
        assert loan_repo.find_by_student("nobody") == []

    def test_find_active_by_student(self, loan_repo, loan, student):
        loan_repo.save(loan)
        active = loan_repo.find_active_by_student("s001")
        assert len(active) == 1

    def test_find_active_excludes_returned(
            self, loan_repo, loan, resource):
        loan_repo.save(loan)
        loan.return_loan()
        active = loan_repo.find_active_by_student("s001")
        assert len(active) == 0

    def test_find_overdue(self, loan_repo, loan):
        loan_repo.save(loan)
        loan._due_date = date.today() - timedelta(days=3)
        overdue = loan_repo.find_overdue()
        assert len(overdue) == 1

    def test_find_overdue_excludes_current(self, loan_repo, loan):
        loan_repo.save(loan)
        overdue = loan_repo.find_overdue()
        assert len(overdue) == 0

    def test_find_due_within_days(self, loan_repo, loan):
        loan_repo.save(loan)
        loan._due_date = date.today() + timedelta(days=2)
        results = loan_repo.find_due_within_days(3)
        assert len(results) == 1

    def test_find_due_within_days_excludes_later(self, loan_repo, loan):
        loan_repo.save(loan)
        loan._due_date = date.today() + timedelta(days=10)
        results = loan_repo.find_due_within_days(3)
        assert len(results) == 0

    def test_find_by_resource(self, loan_repo, loan, resource):
        loan_repo.save(loan)
        results = loan_repo.find_by_resource("r001")
        assert len(results) == 1

    def test_find_by_resource_excludes_returned(
            self, loan_repo, loan, resource):
        loan_repo.save(loan)
        loan.return_loan()
        results = loan_repo.find_by_resource("r001")
        assert len(results) == 0


# ══════════════════════════════════════════════════════════════════════════════
# RESERVATION REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryReservationRepository:

    def test_save_and_find_by_id(self, reservation_repo, reservation):
        reservation_repo.save(reservation)
        assert reservation_repo.find_by_id("res_001") is reservation

    def test_find_by_student(self, reservation_repo, reservation):
        reservation_repo.save(reservation)
        assert len(reservation_repo.find_by_student("s001")) == 1

    def test_find_active_by_resource(self, reservation_repo, reservation):
        reservation_repo.save(reservation)
        reservation.confirm_reservation()
        results = reservation_repo.find_active_by_resource("r001")
        assert len(results) == 1

    def test_find_active_excludes_cancelled(
            self, reservation_repo, reservation):
        reservation_repo.save(reservation)
        reservation.cancel_reservation()
        results = reservation_repo.find_active_by_resource("r001")
        assert len(results) == 0

    def test_find_expired(self, reservation_repo, reservation):
        reservation_repo.save(reservation)
        reservation._expiry_date = datetime.now() - timedelta(hours=1)
        results = reservation_repo.find_expired()
        assert len(results) == 1

    def test_find_queue_for_resource(
            self, reservation_repo, student, student2, resource):
        res1 = Reservation("res_q1", student, resource)
        res2 = Reservation("res_q2", student2, resource)
        res1._status = ReservationStatus.QUEUED
        res1._queue_position = 1
        res2._status = ReservationStatus.QUEUED
        res2._queue_position = 2
        reservation_repo.save(res1)
        reservation_repo.save(res2)
        queue = reservation_repo.find_queue_for_resource("r001")
        assert len(queue) == 2
        assert queue[0]._queue_position == 1


# ══════════════════════════════════════════════════════════════════════════════
# FINE REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryFineRepository:

    def test_save_and_find_by_id(self, fine_repo, fine):
        fine_repo.save(fine)
        assert fine_repo.find_by_id("fine_001") is fine

    def test_find_by_student(self, fine_repo, fine):
        fine_repo.save(fine)
        results = fine_repo.find_by_student("s001")
        assert len(results) == 1

    def test_find_pending_by_student(self, fine_repo, fine):
        fine_repo.save(fine)
        pending = fine_repo.find_pending_by_student("s001")
        assert len(pending) == 1

    def test_find_pending_excludes_paid(self, fine_repo, fine, student):
        student.add_fine(25.0)
        fine_repo.save(fine)
        fine.pay_fine()
        pending = fine_repo.find_pending_by_student("s001")
        assert len(pending) == 0

    def test_find_by_loan(self, fine_repo, fine):
        fine_repo.save(fine)
        found = fine_repo.find_by_loan("loan_001")
        assert found is fine

    def test_find_by_loan_not_found(self, fine_repo):
        assert fine_repo.find_by_loan("no_loan") is None


# ══════════════════════════════════════════════════════════════════════════════
# NOTIFICATION REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryNotificationRepository:

    def test_save_and_find_by_id(self, notification_repo, notification):
        notification_repo.save(notification)
        assert notification_repo.find_by_id("notif_001") is notification

    def test_find_by_user(self, notification_repo, notification):
        notification_repo.save(notification)
        results = notification_repo.find_by_user("s001")
        assert len(results) == 1

    def test_find_scheduled(self, notification_repo, notification):
        notification_repo.save(notification)
        scheduled = notification_repo.find_scheduled()
        assert len(scheduled) == 1

    def test_find_scheduled_excludes_delivered(
            self, notification_repo, notification):
        notification_repo.save(notification)
        notification.send()
        scheduled = notification_repo.find_scheduled()
        assert len(scheduled) == 0

    def test_find_failed(self, notification_repo, notification):
        notification_repo.save(notification)
        notification._status = NotificationStatus.FAILED
        failed = notification_repo.find_failed()
        assert len(failed) == 1

    def test_delete(self, notification_repo, notification):
        notification_repo.save(notification)
        assert notification_repo.delete("notif_001") is True


# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATION REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryRecommendationRepository:

    def test_save_and_find_by_id(
            self, recommendation_repo, recommendation):
        recommendation_repo.save(recommendation)
        assert recommendation_repo.find_by_id("rec_001") is recommendation

    def test_find_by_student(
            self, recommendation_repo, recommendation):
        recommendation_repo.save(recommendation)
        results = recommendation_repo.find_by_student("s001")
        assert len(results) == 1

    def test_find_ready_by_student(
            self, recommendation_repo, recommendation):
        recommendation_repo.save(recommendation)
        ready = recommendation_repo.find_ready_by_student("s001")
        assert len(ready) == 1

    def test_find_ready_excludes_pending(
            self, recommendation_repo, student, resource):
        rec = Recommendation("rec_002", student, resource, 0.5)
        rec._status = "PENDING"
        recommendation_repo.save(rec)
        ready = recommendation_repo.find_ready_by_student("s001")
        assert len(ready) == 0


# ══════════════════════════════════════════════════════════════════════════════
# REPORT REPOSITORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestInMemoryReportRepository:

    def test_save_and_find_by_id(self, report_repo, report):
        report_repo.save(report)
        assert report_repo.find_by_id("rpt_001") is report

    def test_find_by_type(self, report_repo, report):
        report_repo.save(report)
        results = report_repo.find_by_type("Top 20 Borrowed")
        assert len(results) == 1

    def test_find_ready(self, report_repo, report):
        report_repo.save(report)
        ready = report_repo.find_ready()
        assert len(ready) == 1

    def test_find_ready_excludes_requested(self, report_repo):
        r = Report("rpt_002", "Overdue Rate")
        report_repo.save(r)
        ready = report_repo.find_ready()
        assert len(ready) == 0

    def test_count(self, report_repo, report):
        report_repo.save(report)
        assert report_repo.count() == 1


# ══════════════════════════════════════════════════════════════════════════════
# REPOSITORY FACTORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestRepositoryFactory:

    def test_get_user_repo_memory(self):
        repo = RepositoryFactory.get_user_repo("MEMORY")
        assert isinstance(repo, InMemoryUserRepository)

    def test_get_resource_repo_memory(self):
        repo = RepositoryFactory.get_resource_repo("MEMORY")
        assert isinstance(repo, InMemoryResourceRepository)

    def test_get_loan_repo_memory(self):
        repo = RepositoryFactory.get_loan_repo("MEMORY")
        assert isinstance(repo, InMemoryLoanRepository)

    def test_get_reservation_repo_memory(self):
        repo = RepositoryFactory.get_reservation_repo("MEMORY")
        assert isinstance(repo, InMemoryReservationRepository)

    def test_get_fine_repo_memory(self):
        repo = RepositoryFactory.get_fine_repo("MEMORY")
        assert isinstance(repo, InMemoryFineRepository)

    def test_get_notification_repo_memory(self):
        repo = RepositoryFactory.get_notification_repo("MEMORY")
        assert isinstance(repo, InMemoryNotificationRepository)

    def test_get_recommendation_repo_memory(self):
        repo = RepositoryFactory.get_recommendation_repo("MEMORY")
        assert isinstance(repo, InMemoryRecommendationRepository)

    def test_get_report_repo_memory(self):
        repo = RepositoryFactory.get_report_repo("MEMORY")
        assert isinstance(repo, InMemoryReportRepository)

    def test_invalid_storage_type_raises(self):
        with pytest.raises(ValueError, match="Invalid storage type"):
            RepositoryFactory.get_resource_repo("ORACLE")

    def test_case_insensitive_storage_type(self):
        repo = RepositoryFactory.get_resource_repo("memory")
        assert isinstance(repo, InMemoryResourceRepository)

    def test_get_all_returns_all_repos(self):
        repos = RepositoryFactory.get_all("MEMORY")
        assert "users" in repos
        assert "resources" in repos
        assert "loans" in repos
        assert "reservations" in repos
        assert "fines" in repos
        assert "notifications" in repos
        assert "recommendations" in repos
        assert "reports" in repos
        assert len(repos) == 8

    def test_get_all_repos_are_independent_instances(self):
        repos1 = RepositoryFactory.get_all("MEMORY")
        repos2 = RepositoryFactory.get_all("MEMORY")
        assert repos1["resources"] is not repos2["resources"]

    def test_filesystem_resource_repo_available(self, tmp_path):
        from repositories.filesystem.filesystem_repositories import (
            FileSystemResourceRepository
        )
        repo = RepositoryFactory.get_resource_repo(
            "FILESYSTEM",
            file_path=str(tmp_path / "resources.json")
        )
        assert isinstance(repo, FileSystemResourceRepository)

    def test_database_repo_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            RepositoryFactory.get_resource_repo("DATABASE").find_all()

    def test_filesystem_save_and_retrieve(self, tmp_path, resource):
        """Integration test: save to filesystem and retrieve."""
        repo = RepositoryFactory.get_resource_repo(
            "FILESYSTEM",
            file_path=str(tmp_path / "resources.json")
        )
        repo.save(resource)
        found = repo.find_by_id("r001")
        assert found is not None
        assert found.title == "Clean Code"

    def test_each_factory_call_returns_fresh_repo(self):
        """Repos are not singletons — each call returns a new instance."""
        repo1 = RepositoryFactory.get_user_repo("MEMORY")
        repo2 = RepositoryFactory.get_user_repo("MEMORY")
        assert repo1 is not repo2
