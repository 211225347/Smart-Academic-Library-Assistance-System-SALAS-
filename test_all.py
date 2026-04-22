"""
tests/test_all.py
Unit tests for SALAS — all class implementations and all 6 creational patterns.
Run with: pytest tests/test_all.py -v --tb=short
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import threading
from datetime import date, timedelta
from unittest.mock import patch

from src.models import (
    Student, Librarian, Resource, Loan, Reservation, Fine,
    ReadingList, Recommendation, Notification, Catalogue, Report,
    Role, AccountStatus, LoanStatus, FineStatus,
    NotificationType, NotificationStatus, ResourceStatus
)
from creational_patterns.simple_factory import UserFactory
from creational_patterns.factory_method import (
    get_notification_creator, DueSoonNotificationCreator,
    OverdueNotificationCreator, ReservationConfirmedCreator
)
from creational_patterns.abstract_factory import (
    CSVReportFactory, PDFReportFactory, get_export_factory
)
from creational_patterns.builder import ResourceBuilder, ResourceDirector
from creational_patterns.prototype import ResourceCache, create_resource_from_prototype
from creational_patterns.singleton import DatabaseConnection, CatalogueService


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def student():
    return Student(
        user_id="s001",
        name="Alice Dlamini",
        email="alice@university.ac.za",
        password="Pass@123",
        student_number="211001",
        course_enrollment=["Computer Science"]
    )


@pytest.fixture
def librarian():
    return Librarian(
        user_id="l001",
        name="Bob Nkosi",
        email="bob@university.ac.za",
        password="Staff@456",
        staff_id="LIB001",
        department="Reference"
    )


@pytest.fixture
def resource():
    return Resource(
        resource_id="r001",
        title="Clean Code",
        author="Robert C. Martin",
        isbn="9780132350884",
        genre="Software Engineering",
        published_year=2008,
        total_copies=3,
        location="CS Shelf 4B"
    )


@pytest.fixture
def catalogue():
    return Catalogue("cat_001")


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset DatabaseConnection singleton before every test."""
    DatabaseConnection.reset_instance()
    yield
    DatabaseConnection.reset_instance()


@pytest.fixture(autouse=True)
def load_prototypes():
    """Load resource cache before prototype tests."""
    ResourceCache.load_cache()


# ══════════════════════════════════════════════════════════════════════════════
# 1. CLASS IMPLEMENTATION TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestStudent:

    def test_student_creation(self, student):
        assert student.user_id == "s001"
        assert student.name == "Alice Dlamini"
        assert student.role == Role.STUDENT
        assert student.account_status == AccountStatus.ACTIVE
        assert student.outstanding_fines == 0.0

    def test_student_login_success(self, student):
        assert student.login("Pass@123") is True

    def test_student_login_failure(self, student):
        assert student.login("wrong_password") is False

    def test_account_locked_after_5_failures(self, student):
        for _ in range(5):
            student.login("wrong")
        assert student.account_status == AccountStatus.LOCKED

    def test_locked_account_raises_on_login(self, student):
        for _ in range(5):
            student.login("wrong")
        with pytest.raises(PermissionError):
            student.login("wrong")

    def test_student_eligibility_with_fine(self, student):
        student.add_fine(150.0)
        assert student.is_eligible_to_borrow() is False

    def test_student_eligibility_fine_below_threshold(self, student):
        student.add_fine(50.0)
        assert student.is_eligible_to_borrow() is True

    def test_student_borrow_resource(self, student, resource):
        loan = student.borrow_resource(resource)
        assert isinstance(loan, Loan)
        assert loan.status == LoanStatus.ACTIVE
        assert resource.available_copies == 2

    def test_student_cannot_borrow_unavailable(self, student, resource):
        resource._available_copies = 0
        with pytest.raises(ValueError, match="not available"):
            student.borrow_resource(resource)

    def test_student_ineligible_borrow_raises(self, student, resource):
        student.add_fine(200.0)
        with pytest.raises(ValueError, match="not eligible"):
            student.borrow_resource(resource)

    def test_reading_list_is_created(self, student):
        assert isinstance(student.reading_list, ReadingList)

    def test_max_loans_enforcement(self, student):
        """BR-01: Max 5 active loans."""
        resources = [
            Resource(f"r{i}", f"Book {i}", "Author", "9780132350884",
                     "General", 2020, 1, "Shelf")
            for i in range(5)
        ]
        for r in resources:
            student.borrow_resource(r)
        extra = Resource("r_extra", "Extra Book", "Author",
                         "9780132350884", "General", 2020, 1, "Shelf")
        with pytest.raises(ValueError):
            student.borrow_resource(extra)

    def test_deactivate_account(self, student):
        student.deactivate_account()
        assert student.account_status == AccountStatus.DEACTIVATED


class TestLibrarian:

    def test_librarian_creation(self, librarian):
        assert librarian.role == Role.LIBRARIAN
        assert librarian.staff_id == "LIB001"

    def test_librarian_add_resource(self, librarian, resource, catalogue):
        result = librarian.add_resource(resource, catalogue)
        assert result is resource
        assert catalogue.total_resources == 1

    def test_librarian_rejects_invalid_isbn(self, librarian, catalogue):
        bad_resource = Resource("r_bad", "Bad Book", "Author",
                                "1234567890", "General", 2020, 1, "Shelf")
        with pytest.raises(ValueError, match="Invalid ISBN"):
            librarian.add_resource(bad_resource, catalogue)

    def test_librarian_delete_resource_with_no_loans(
            self, librarian, resource, catalogue):
        catalogue.add_resource(resource)
        result = librarian.delete_resource(resource, catalogue)
        assert result is True

    def test_librarian_cannot_delete_with_active_loans(
            self, librarian, student, resource, catalogue):
        catalogue.add_resource(resource)
        student.borrow_resource(resource)
        with pytest.raises(ValueError, match="active loans"):
            librarian.delete_resource(resource, catalogue)


class TestResource:

    def test_resource_creation(self, resource):
        assert resource.title == "Clean Code"
        assert resource.available_copies == 3
        assert resource.status == ResourceStatus.AVAILABLE

    def test_checkout_decrements_copies(self, resource):
        resource.check_out()
        assert resource.available_copies == 2

    def test_return_increments_copies(self, resource):
        resource.check_out()
        resource.return_resource()
        assert resource.available_copies == 3

    def test_check_availability_true(self, resource):
        assert resource.check_availability() is True

    def test_check_availability_false_when_no_copies(self, resource):
        resource._available_copies = 0
        assert resource.check_availability() is False

    def test_checkout_raises_when_no_copies(self, resource):
        resource._available_copies = 0
        with pytest.raises(ValueError):
            resource.check_out()

    def test_validate_isbn13_valid(self, resource):
        assert resource.validate_isbn() is True

    def test_validate_isbn13_invalid(self):
        bad = Resource("r_bad", "Test", "Author", "9999999999999",
                       "General", 2020, 1, "Shelf")
        assert bad.validate_isbn() is False

    def test_validate_isbn10_valid(self):
        r = Resource("r10", "Test", "Author", "0306406152",
                     "General", 2020, 1, "Shelf")
        assert r.validate_isbn() is True

    def test_resource_clone_is_independent(self, resource):
        clone = resource.clone()
        clone._title = "Modified"
        assert resource.title == "Clean Code"


class TestLoan:

    def test_loan_creation(self, student, resource):
        loan = Loan("loan_001", student, resource)
        assert loan.status == LoanStatus.ACTIVE
        assert loan.due_date == date.today() + timedelta(days=14)

    def test_loan_not_overdue_initially(self, student, resource):
        loan = Loan("loan_001", student, resource)
        assert loan.is_overdue() is False

    def test_loan_calculates_zero_fine_when_not_overdue(
            self, student, resource):
        loan = Loan("loan_001", student, resource)
        assert loan.calculate_fine() == 0.0

    def test_overdue_loan_calculates_fine(self, student, resource):
        loan = Loan("loan_001", student, resource)
        loan._due_date = date.today() - timedelta(days=5)
        assert loan.calculate_fine() == 25.0  # 5 days * R5

    def test_fine_capped_at_200(self, student, resource):
        loan = Loan("loan_001", student, resource)
        loan._due_date = date.today() - timedelta(days=100)
        assert loan.calculate_fine() == 200.0

    def test_return_loan(self, student, resource):
        resource.check_out()
        loan = Loan("loan_001", student, resource)
        loan.return_loan()
        assert loan.status == LoanStatus.RETURNED
        assert resource.available_copies == 3

    def test_return_generates_fine_when_overdue(self, student, resource):
        resource.check_out()
        loan = Loan("loan_001", student, resource)
        loan._due_date = date.today() - timedelta(days=3)
        loan.return_loan()
        assert loan.fine is not None
        assert loan.fine.amount == 15.0

    def test_renew_loan(self, student, resource):
        loan = Loan("loan_001", student, resource)
        original_due = loan.due_date
        loan.renew_loan()
        assert loan.due_date == original_due + timedelta(days=14)


class TestFine:

    def test_fine_creation(self, student, resource):
        loan = Loan("loan_001", student, resource)
        fine = Fine("fine_001", loan, 25.0)
        assert fine.amount == 25.0
        assert fine.status == FineStatus.PENDING

    def test_pay_fine(self, student, resource):
        student.add_fine(25.0)
        loan = Loan("loan_001", student, resource)
        fine = Fine("fine_001", loan, 25.0)
        fine.pay_fine()
        assert fine.status == FineStatus.PAID
        assert student.outstanding_fines == 0.0

    def test_waive_fine(self, student, resource):
        student.add_fine(25.0)
        loan = Loan("loan_001", student, resource)
        fine = Fine("fine_001", loan, 25.0)
        fine.waive_fine()
        assert fine.status == FineStatus.WAIVED

    def test_borrowing_blocked_when_fine_over_threshold(
            self, student, resource):
        loan = Loan("loan_001", student, resource)
        fine = Fine("fine_001", loan, 150.0)
        assert fine.is_borrowing_blocked() is True

    def test_borrowing_not_blocked_below_threshold(
            self, student, resource):
        loan = Loan("loan_001", student, resource)
        fine = Fine("fine_001", loan, 50.0)
        assert fine.is_borrowing_blocked() is False


class TestReadingList:

    def test_add_resource(self, student, resource):
        student.reading_list.add_resource(resource)
        assert len(student.reading_list.resources) == 1

    def test_no_duplicate_resources(self, student, resource):
        student.reading_list.add_resource(resource)
        student.reading_list.add_resource(resource)
        assert len(student.reading_list.resources) == 1

    def test_remove_resource(self, student, resource):
        student.reading_list.add_resource(resource)
        student.reading_list.remove_resource(resource.resource_id)
        assert len(student.reading_list.resources) == 0

    def test_generate_share_link(self, student):
        link = student.reading_list.generate_share_link()
        assert "salas.ac.za" in link

    def test_export_bibliography_apa(self, student, resource):
        student.reading_list.add_resource(resource)
        bib = student.reading_list.export_bibliography("APA")
        assert "Clean Code" in bib
        assert "Robert C. Martin" in bib


class TestCatalogue:

    def test_add_resource(self, catalogue, resource):
        catalogue.add_resource(resource)
        assert catalogue.total_resources == 1

    def test_get_resource(self, catalogue, resource):
        catalogue.add_resource(resource)
        found = catalogue.get_resource("r001")
        assert found is resource

    def test_remove_resource(self, catalogue, resource):
        catalogue.add_resource(resource)
        catalogue.remove_resource("r001")
        assert catalogue.total_resources == 0

    def test_search_by_keyword(self, catalogue, resource):
        catalogue.add_resource(resource)
        results = catalogue.search_by_keyword("clean")
        assert len(results) == 1
        assert results[0].title == "Clean Code"

    def test_search_returns_empty_for_no_match(self, catalogue, resource):
        catalogue.add_resource(resource)
        results = catalogue.search_by_keyword("quantum physics")
        assert len(results) == 0

    def test_apply_filter_genre(self, catalogue, resource):
        catalogue.add_resource(resource)
        results = catalogue.apply_filters(genre="Software Engineering")
        assert len(results) == 1

    def test_apply_filter_available_only(self, catalogue, resource):
        catalogue.add_resource(resource)
        resource._available_copies = 0
        results = catalogue.apply_filters(available_only=True)
        assert len(results) == 0


class TestNotification:

    def test_notification_creation(self, student):
        n = Notification("n001", student, NotificationType.DUE_SOON)
        assert n.status == NotificationStatus.SCHEDULED
        assert n.retry_count == 0

    def test_send_notification(self, student):
        n = Notification("n001", student, NotificationType.DUE_SOON)
        result = n.send()
        assert result is True
        assert n.status == NotificationStatus.DELIVERED

    def test_retry_after_failure(self, student):
        n = Notification("n001", student, NotificationType.OVERDUE)
        n._status = NotificationStatus.FAILED
        n.retry()
        assert n.retry_count == 1

    def test_fallback_after_max_retries(self, student):
        n = Notification("n001", student, NotificationType.OVERDUE)
        n._retry_count = 3
        n.retry()
        assert n._channel == "IN_APP"

    def test_archive_notification(self, student):
        n = Notification("n001", student, NotificationType.DUE_SOON)
        n.send()
        n.archive()
        assert n.status == NotificationStatus.ARCHIVED


class TestReport:

    def test_report_creation(self):
        r = Report("rpt001", "Top 20 Borrowed")
        assert r.status == "REQUESTED"

    def test_generate_report(self):
        r = Report("rpt001", "Top 20 Borrowed")
        r.generate({"rows": [{"title": "Clean Code", "borrows": 45}]})
        assert r.status == "READY"

    def test_export_csv(self):
        r = Report("rpt001", "Top 20 Borrowed")
        r.generate({"rows": [{"title": "Clean Code", "borrows": 45}]})
        csv = r.export_csv()
        assert "Clean Code" in csv

    def test_export_csv_raises_when_not_ready(self):
        r = Report("rpt001", "Top 20 Borrowed")
        with pytest.raises(ValueError, match="not ready"):
            r.export_csv()


# ══════════════════════════════════════════════════════════════════════════════
# 2. SIMPLE FACTORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestSimpleFactory:

    def test_creates_student(self):
        user = UserFactory.create_user(
            "STUDENT", "u001", "Alice", "alice@uni.ac.za",
            "Pass@123", student_number="211001"
        )
        assert isinstance(user, Student)
        assert user.role == Role.STUDENT

    def test_creates_librarian(self):
        user = UserFactory.create_user(
            "LIBRARIAN", "u002", "Bob", "bob@uni.ac.za",
            "Staff@456", staff_id="LIB001", department="Reference"
        )
        assert isinstance(user, Librarian)
        assert user.role == Role.LIBRARIAN

    def test_case_insensitive_role(self):
        user = UserFactory.create_user(
            "student", "u003", "Carol", "carol@uni.ac.za", "Pass@789",
            student_number="211002"
        )
        assert isinstance(user, Student)

    def test_unknown_role_raises(self):
        with pytest.raises(ValueError, match="Unknown role"):
            UserFactory.create_user(
                "ADMIN", "u004", "Dave", "dave@uni.ac.za", "Pass@000"
            )

    def test_student_has_correct_attributes(self):
        user = UserFactory.create_user(
            "STUDENT", "u005", "Eve", "eve@uni.ac.za", "Pass@123",
            student_number="211005",
            course_enrollment=["Mathematics"]
        )
        assert user.student_number == "211005"
        assert "Mathematics" in user._course_enrollment


# ══════════════════════════════════════════════════════════════════════════════
# 3. FACTORY METHOD TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestFactoryMethod:

    def test_due_soon_creator(self, student):
        creator = DueSoonNotificationCreator()
        n = creator.create_notification("n001", student)
        assert n._type == NotificationType.DUE_SOON
        assert n._channel == "EMAIL"

    def test_overdue_creator(self, student):
        creator = OverdueNotificationCreator()
        n = creator.create_notification("n002", student)
        assert n._type == NotificationType.OVERDUE

    def test_reservation_confirmed_creator(self, student):
        creator = ReservationConfirmedCreator()
        n = creator.create_notification("n003", student)
        assert n._type == NotificationType.RESERVATION_CONFIRMED

    def test_new_arrival_uses_in_app_channel(self, student):
        creator = get_notification_creator("NEW_ARRIVAL")
        n = creator.create_notification("n004", student)
        assert n._channel == "IN_APP"

    def test_get_creator_by_string(self, student):
        creator = get_notification_creator("DUE_SOON")
        n = creator.create_notification("n005", student)
        assert isinstance(n, Notification)

    def test_unknown_event_raises(self):
        with pytest.raises(ValueError, match="No creator"):
            get_notification_creator("UNKNOWN_EVENT")

    def test_send_notification_via_creator(self, student):
        creator = get_notification_creator("OVERDUE")
        result = creator.send_notification("n006", student)
        assert result is True


# ══════════════════════════════════════════════════════════════════════════════
# 4. ABSTRACT FACTORY TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestAbstractFactory:

    @pytest.fixture
    def ready_report(self):
        r = Report("rpt001", "Top 20 Borrowed")
        r.generate({"rows": [
            {"title": "Clean Code", "borrows": 45},
            {"title": "Design Patterns", "borrows": 38}
        ]})
        return r

    def test_csv_factory_produces_csv_output(self, ready_report):
        factory = CSVReportFactory()
        rows = [{"title": "Clean Code", "borrows": 45}]
        output = factory.export(ready_report, rows)
        assert "Clean Code" in output
        assert "45" in output

    def test_pdf_factory_produces_pdf_output(self, ready_report):
        factory = PDFReportFactory()
        rows = [{"title": "Clean Code", "borrows": 45}]
        output = factory.export(ready_report, rows)
        assert "PDF" in output
        assert "Clean Code" in output

    def test_csv_renderer_extension(self):
        factory = CSVReportFactory()
        renderer = factory.create_renderer()
        assert renderer.get_file_extension() == ".csv"

    def test_pdf_renderer_extension(self):
        factory = PDFReportFactory()
        renderer = factory.create_renderer()
        assert renderer.get_file_extension() == ".pdf"

    def test_get_factory_by_string_csv(self):
        factory = get_export_factory("CSV")
        assert isinstance(factory, CSVReportFactory)

    def test_get_factory_by_string_pdf(self):
        factory = get_export_factory("PDF")
        assert isinstance(factory, PDFReportFactory)

    def test_unknown_format_raises(self):
        with pytest.raises(ValueError, match="Unsupported export format"):
            get_export_factory("XML")

    def test_csv_and_pdf_are_different_families(self, ready_report):
        rows = [{"col": "val"}]
        csv_out = get_export_factory("CSV").export(ready_report, rows)
        pdf_out = get_export_factory("PDF").export(ready_report, rows)
        assert csv_out != pdf_out


# ══════════════════════════════════════════════════════════════════════════════
# 5. BUILDER TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestBuilder:

    def test_builder_creates_resource(self):
        resource = (ResourceBuilder("r001", "Clean Code",
                                    "Robert C. Martin", "9780132350884")
                    .build())
        assert resource.title == "Clean Code"
        assert resource.available_copies == 1

    def test_builder_with_all_optional_fields(self):
        resource = (ResourceBuilder("r001", "Clean Code",
                                    "Robert C. Martin", "9780132350884")
                    .with_genre("Software Engineering")
                    .with_published_year(2008)
                    .with_copies(5)
                    .with_location("CS Shelf 4B")
                    .with_cover_image("https://example.com/cover.jpg")
                    .build())
        assert resource._genre == "Software Engineering"
        assert resource._published_year == 2008
        assert resource.available_copies == 5
        assert resource._location == "CS Shelf 4B"

    def test_builder_rejects_invalid_isbn(self):
        with pytest.raises(ValueError, match="invalid"):
            (ResourceBuilder("r_bad", "Bad Book", "Author", "1234567890")
             .build())

    def test_builder_rejects_zero_copies(self):
        with pytest.raises(ValueError, match="at least 1"):
            (ResourceBuilder("r001", "Test", "Author", "9780132350884")
             .with_copies(0)
             .build())

    def test_builder_rejects_invalid_year(self):
        with pytest.raises(ValueError, match="Invalid year"):
            (ResourceBuilder("r001", "Test", "Author", "9780132350884")
             .with_published_year(500)
             .build())

    def test_director_constructs_textbook(self):
        t = ResourceDirector.construct_textbook(
            "r001", "Intro to Algorithms",
            "Cormen", "9780262033848"
        )
        assert t._genre == "Textbook"
        assert t.available_copies == 5

    def test_director_constructs_journal(self):
        j = ResourceDirector.construct_journal(
            "r002", "IEEE Journal", "IEEE", "9780262033848"
        )
        assert j._genre == "Journal"
        assert j.available_copies == 2

    def test_director_constructs_reference(self):
        r = ResourceDirector.construct_reference(
            "r003", "Oxford Dictionary", "Oxford", "9780201633610"
        )
        assert r._genre == "Reference"
        assert r.available_copies == 1

    def test_builder_chaining_returns_self(self):
        builder = ResourceBuilder("r001", "Test", "Author", "9780132350884")
        result = builder.with_genre("Fiction")
        assert result is builder


# ══════════════════════════════════════════════════════════════════════════════
# 6. PROTOTYPE TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestPrototype:

    def test_cache_loads_prototypes(self):
        keys = ResourceCache.list_prototypes()
        assert "TEXTBOOK" in keys
        assert "JOURNAL" in keys
        assert "REFERENCE" in keys

    def test_clone_is_not_same_object(self):
        clone = ResourceCache.get_clone("TEXTBOOK")
        original = ResourceCache.get_clone("TEXTBOOK")
        assert clone is not original

    def test_clone_has_same_attributes(self):
        clone = ResourceCache.get_clone("TEXTBOOK")
        assert clone._genre == "Textbook"
        assert clone.available_copies == 3

    def test_clone_is_independent(self):
        clone = ResourceCache.get_clone("TEXTBOOK")
        clone._available_copies = 99
        original = ResourceCache.get_clone("TEXTBOOK")
        assert original.available_copies == 3

    def test_create_from_prototype_sets_identity(self):
        r = create_resource_from_prototype(
            "TEXTBOOK", "r_new", "New Book", "Jane Doe", "9780132350884"
        )
        assert r._resource_id == "r_new"
        assert r._title == "New Book"
        assert r._author == "Jane Doe"
        assert r._genre == "Textbook"

    def test_unknown_prototype_raises(self):
        with pytest.raises(KeyError, match="No prototype"):
            ResourceCache.get_clone("UNKNOWN_TYPE")

    def test_register_custom_prototype(self):
        custom = Resource(
            "proto_custom", "Template", "Author", "9780132350884",
            "Fiction", 2024, 2, "Fiction Section"
        )
        ResourceCache.register_prototype("FICTION", custom)
        assert "FICTION" in ResourceCache.list_prototypes()
        clone = ResourceCache.get_clone("FICTION")
        assert clone._genre == "Fiction"

    def test_resource_clone_method(self):
        r = Resource("r001", "Test", "Author", "9780132350884",
                     "General", 2020, 3, "Shelf")
        clone = r.clone()
        clone._title = "Modified"
        assert r.title == "Test"


# ══════════════════════════════════════════════════════════════════════════════
# 7. SINGLETON TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestSingleton:

    def test_same_instance_returned(self):
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        assert db1 is db2

    def test_connection_ids_are_identical(self):
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        assert db1.connection_id == db2.connection_id

    def test_is_connected(self):
        db = DatabaseConnection.get_instance()
        assert db.is_connected is True

    def test_query_execution(self):
        db = DatabaseConnection.get_instance()
        result = db.execute_query(
            "SELECT * FROM resources WHERE resource_id = %s", ("r001",)
        )
        assert result["rows_affected"] == 1
        assert result["query_number"] == 1

    def test_query_count_increments(self):
        db = DatabaseConnection.get_instance()
        db.execute_query("SELECT 1")
        db.execute_query("SELECT 2")
        assert db.query_count == 2

    def test_direct_instantiation_raises(self):
        DatabaseConnection.get_instance()
        with pytest.raises(RuntimeError, match="Singleton"):
            DatabaseConnection()

    def test_thread_safety(self):
        """All threads must receive the same instance."""
        results = []
        lock = threading.Lock()

        def get_db():
            db = DatabaseConnection.get_instance()
            with lock:
                results.append(db.connection_id)

        threads = [threading.Thread(target=get_db) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(results)) == 1, "Multiple instances created!"

    def test_catalogue_service_shares_connection(self):
        svc1 = CatalogueService()
        svc2 = CatalogueService()
        assert svc1._db is svc2._db

    def test_reset_allows_new_instance(self):
        db1 = DatabaseConnection.get_instance()
        id1 = db1.connection_id
        DatabaseConnection.reset_instance()
        db2 = DatabaseConnection.get_instance()
        assert db2.connection_id != id1
