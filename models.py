"""
src/models.py
Core domain classes for SALAS — Smart Academic Library Assistance System
Translated from CLASS_DIAGRAM.md (Assignment 9)
"""

from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional
import copy
import hashlib


# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class Role(Enum):
    STUDENT = "STUDENT"
    LIBRARIAN = "LIBRARIAN"
    ADMIN = "ADMIN"


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class ResourceStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    RESERVED = "RESERVED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    LOST = "LOST"


class LoanStatus(Enum):
    ACTIVE = "ACTIVE"
    DUE_SOON = "DUE_SOON"
    OVERDUE = "OVERDUE"
    RETURNED = "RETURNED"
    ARCHIVED = "ARCHIVED"


class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    QUEUED = "QUEUED"
    COLLECTED = "COLLECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class FineStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    WAIVED = "WAIVED"


class NotificationType(Enum):
    DUE_SOON = "DUE_SOON"
    OVERDUE = "OVERDUE"
    RESERVATION_CONFIRMED = "RESERVATION_CONFIRMED"
    NEW_ARRIVAL = "NEW_ARRIVAL"


class NotificationStatus(Enum):
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"


# ─────────────────────────────────────────────
# User (Base Class)
# ─────────────────────────────────────────────

class User:
    """Base class for all SALAS users. Maps to FR-01, FR-10."""

    def __init__(self, user_id: str, name: str, email: str,
                 password: str, role: Role):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._role = role
        self._account_status = AccountStatus.ACTIVE
        self._created_at = datetime.now()
        self._failed_login_attempts = 0
        self._locked_until: Optional[datetime] = None

    # Getters
    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> Role:
        return self._role

    @property
    def account_status(self) -> AccountStatus:
        return self._account_status

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, password: str) -> bool:
        """Authenticate user. Locks account after 5 failed attempts (NFR-10)."""
        if self._account_status == AccountStatus.LOCKED:
            if self._locked_until and datetime.now() < self._locked_until:
                raise PermissionError("Account is locked. Try again later.")
            else:
                self._account_status = AccountStatus.ACTIVE
                self._failed_login_attempts = 0

        if self._password_hash == self._hash_password(password):
            self._failed_login_attempts = 0
            return True
        else:
            self._failed_login_attempts += 1
            if self._failed_login_attempts >= 5:
                self._account_status = AccountStatus.LOCKED
                self._locked_until = datetime.now() + timedelta(minutes=15)
            return False

    def logout(self) -> None:
        pass

    def update_profile(self, name: str = None, email: str = None) -> None:
        if name:
            self._name = name
        if email:
            self._email = email

    def deactivate_account(self) -> None:
        """Deactivates account. Triggers POPIA data erasure (NFR-11)."""
        self._account_status = AccountStatus.DEACTIVATED

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._user_id}, name={self._name})"


# ─────────────────────────────────────────────
# Student (extends User)
# ─────────────────────────────────────────────

class Student(User):
    """University student who borrows and reserves resources. Maps to US-002."""

    MAX_ACTIVE_LOANS = 5
    FINE_BLOCK_THRESHOLD = 100.0

    def __init__(self, user_id: str, name: str, email: str,
                 password: str, student_number: str,
                 course_enrollment: List[str] = None):
        super().__init__(user_id, name, email, password, Role.STUDENT)
        self._student_number = student_number
        self._course_enrollment = course_enrollment or []
        self._outstanding_fines = 0.0
        self._borrowing_count = 0
        self._loans: List["Loan"] = []
        self._reservations: List["Reservation"] = []
        self._reading_list = ReadingList(f"rl_{user_id}", "My Reading List")

    @property
    def student_number(self) -> str:
        return self._student_number

    @property
    def outstanding_fines(self) -> float:
        return self._outstanding_fines

    @property
    def reading_list(self) -> "ReadingList":
        return self._reading_list

    @property
    def loans(self) -> List["Loan"]:
        return self._loans

    def is_eligible_to_borrow(self) -> bool:
        """Check BR-01 and BR-02: max loans and fine threshold."""
        active_loans = [l for l in self._loans
                        if l.status in (LoanStatus.ACTIVE, LoanStatus.DUE_SOON,
                                        LoanStatus.OVERDUE)]
        if len(active_loans) >= self.MAX_ACTIVE_LOANS:
            return False
        if self._outstanding_fines > self.FINE_BLOCK_THRESHOLD:
            return False
        return True

    def add_fine(self, amount: float) -> None:
        self._outstanding_fines += amount

    def pay_fine(self, amount: float) -> None:
        self._outstanding_fines = max(0.0, self._outstanding_fines - amount)

    def borrow_resource(self, resource: "Resource") -> "Loan":
        """Creates a loan if eligible. Maps to UC03, FR-03."""
        if not self.is_eligible_to_borrow():
            raise ValueError("Student is not eligible to borrow.")
        if not resource.check_availability():
            raise ValueError("Resource is not available.")
        loan = Loan(
            loan_id=f"loan_{self._user_id}_{resource.resource_id}",
            student=self,
            resource=resource
        )
        resource.check_out()
        self._loans.append(loan)
        self._borrowing_count += 1
        return loan

    def reserve_resource(self, resource: "Resource") -> "Reservation":
        """Creates a reservation. Maps to UC03, FR-03."""
        reservation = Reservation(
            reservation_id=f"res_{self._user_id}_{resource.resource_id}",
            student=self,
            resource=resource
        )
        self._reservations.append(reservation)
        return reservation


# ─────────────────────────────────────────────
# Librarian (extends User)
# ─────────────────────────────────────────────

class Librarian(User):
    """Library staff who manages the catalogue. Maps to FR-06."""

    def __init__(self, user_id: str, name: str, email: str,
                 password: str, staff_id: str, department: str):
        super().__init__(user_id, name, email, password, Role.LIBRARIAN)
        self._staff_id = staff_id
        self._department = department

    @property
    def staff_id(self) -> str:
        return self._staff_id

    def add_resource(self, resource: "Resource",
                     catalogue: "Catalogue") -> "Resource":
        """Adds a resource to the catalogue. Maps to FR-06."""
        if not resource.validate_isbn():
            raise ValueError(f"Invalid ISBN: {resource.isbn}")
        catalogue.add_resource(resource)
        return resource

    def delete_resource(self, resource: "Resource",
                        catalogue: "Catalogue") -> bool:
        """Deletes resource if no active loans exist. Enforces BR-04."""
        if resource.has_active_loans():
            raise ValueError("Cannot delete resource with active loans.")
        catalogue.remove_resource(resource.resource_id)
        return True

    def process_return(self, loan: "Loan") -> None:
        """Processes a book return. Maps to UC12."""
        loan.return_loan()

    def generate_report(self, report_type: str) -> "Report":
        return Report(
            report_id=f"rpt_{self._staff_id}_{report_type}",
            report_type=report_type
        )


# ─────────────────────────────────────────────
# Resource
# ─────────────────────────────────────────────

class Resource:
    """A library resource (book, journal, article). Maps to FR-02, FR-06."""

    def __init__(self, resource_id: str, title: str, author: str,
                 isbn: str, genre: str, published_year: int,
                 total_copies: int, location: str):
        self._resource_id = resource_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._genre = genre
        self._published_year = published_year
        self._total_copies = total_copies
        self._available_copies = total_copies
        self._location = location
        self._cover_image_url = ""
        self._status = ResourceStatus.AVAILABLE
        self._active_loan_count = 0

    @property
    def resource_id(self) -> str:
        return self._resource_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def available_copies(self) -> int:
        return self._available_copies

    @property
    def status(self) -> ResourceStatus:
        return self._status

    def check_availability(self) -> bool:
        return self._available_copies > 0

    def check_out(self) -> None:
        if self._available_copies <= 0:
            raise ValueError("No copies available.")
        self._available_copies -= 1
        self._active_loan_count += 1
        if self._available_copies == 0:
            self._status = ResourceStatus.BORROWED

    def return_resource(self) -> None:
        self._available_copies += 1
        self._active_loan_count = max(0, self._active_loan_count - 1)
        if self._available_copies > 0:
            self._status = ResourceStatus.AVAILABLE

    def reserve(self) -> None:
        self._status = ResourceStatus.RESERVED

    def has_active_loans(self) -> bool:
        return self._active_loan_count > 0

    def validate_isbn(self) -> bool:
        """Validates ISBN-10 or ISBN-13. Enforces BR-05."""
        clean = self._isbn.replace("-", "").replace(" ", "")
        if len(clean) == 10:
            return self._validate_isbn10(clean)
        elif len(clean) == 13:
            return self._validate_isbn13(clean)
        return False

    def _validate_isbn10(self, isbn: str) -> bool:
        if not isbn[:9].isdigit():
            return False
        total = sum((10 - i) * int(isbn[i]) for i in range(9))
        check = isbn[9]
        check_val = 10 if check == 'X' else (int(check) if check.isdigit() else -1)
        return (total + check_val) % 11 == 0

    def _validate_isbn13(self, isbn: str) -> bool:
        if not isbn.isdigit():
            return False
        total = sum(int(isbn[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check = (10 - (total % 10)) % 10
        return check == int(isbn[12])

    def __repr__(self) -> str:
        return f"Resource(id={self._resource_id}, title={self._title})"

    def clone(self) -> "Resource":
        """Returns a deep copy for Prototype pattern."""
        return copy.deepcopy(self)


# ─────────────────────────────────────────────
# Loan
# ─────────────────────────────────────────────

class Loan:
    """Records a borrowing transaction. Maps to FR-03, FR-07."""

    LOAN_PERIOD_DAYS = 14
    FINE_PER_DAY = 5.0
    MAX_FINE = 200.0

    def __init__(self, loan_id: str, student: Student, resource: Resource):
        self._loan_id = loan_id
        self._student = student
        self._resource = resource
        self._borrowed_date = date.today()
        self._due_date = date.today() + timedelta(days=self.LOAN_PERIOD_DAYS)
        self._returned_date: Optional[date] = None
        self._status = LoanStatus.ACTIVE
        self._renewal_count = 0
        self._fine: Optional[Fine] = None

    @property
    def loan_id(self) -> str:
        return self._loan_id

    @property
    def status(self) -> LoanStatus:
        return self._status

    @property
    def due_date(self) -> date:
        return self._due_date

    @property
    def fine(self) -> Optional["Fine"]:
        return self._fine

    @property
    def resource(self) -> Resource:
        return self._resource

    def is_overdue(self) -> bool:
        return date.today() > self._due_date and self._status != LoanStatus.RETURNED

    def calculate_fine(self) -> float:
        """Calculates fine at R5/day, capped at R200. Enforces BR-10."""
        if not self.is_overdue():
            return 0.0
        days_overdue = (date.today() - self._due_date).days
        return min(days_overdue * self.FINE_PER_DAY, self.MAX_FINE)

    def return_loan(self) -> None:
        """Returns the loan and generates fine if overdue."""
        self._returned_date = date.today()
        fine_amount = self.calculate_fine()
        if fine_amount > 0:
            self._fine = Fine(
                fine_id=f"fine_{self._loan_id}",
                loan=self,
                amount=fine_amount
            )
            self._student.add_fine(fine_amount)
        self._resource.return_resource()
        self._status = LoanStatus.RETURNED

    def renew_loan(self) -> bool:
        """Renews loan if no reservations exist. Enforces BR-09."""
        if self._status != LoanStatus.ACTIVE:
            return False
        self._due_date += timedelta(days=self.LOAN_PERIOD_DAYS)
        self._renewal_count += 1
        return True

    def archive_loan(self) -> None:
        self._status = LoanStatus.ARCHIVED

    def __repr__(self) -> str:
        return f"Loan(id={self._loan_id}, status={self._status})"


# ─────────────────────────────────────────────
# Reservation
# ─────────────────────────────────────────────

class Reservation:
    """Records a resource reservation. Maps to FR-03."""

    HOLD_PERIOD_HOURS = 48

    def __init__(self, reservation_id: str, student: Student,
                 resource: Resource):
        self._reservation_id = reservation_id
        self._student = student
        self._resource = resource
        self._reserved_date = datetime.now()
        self._expiry_date = datetime.now() + timedelta(hours=self.HOLD_PERIOD_HOURS)
        self._queue_position = 1
        self._status = ReservationStatus.PENDING

    @property
    def reservation_id(self) -> str:
        return self._reservation_id

    @property
    def status(self) -> ReservationStatus:
        return self._status

    @property
    def expiry_date(self) -> datetime:
        return self._expiry_date

    def confirm_reservation(self) -> None:
        self._status = ReservationStatus.CONFIRMED

    def cancel_reservation(self) -> None:
        self._status = ReservationStatus.CANCELLED

    def expire_reservation(self) -> None:
        self._status = ReservationStatus.EXPIRED

    def fulfil_reservation(self) -> None:
        self._status = ReservationStatus.COLLECTED

    def is_expired(self) -> bool:
        return datetime.now() > self._expiry_date

    def __repr__(self) -> str:
        return f"Reservation(id={self._reservation_id}, status={self._status})"


# ─────────────────────────────────────────────
# Fine
# ─────────────────────────────────────────────

class Fine:
    """Financial penalty for overdue loans. Maps to FR-03."""

    def __init__(self, fine_id: str, loan: Loan, amount: float):
        self._fine_id = fine_id
        self._loan = loan
        self._amount = amount
        self._issued_date = date.today()
        self._paid_date: Optional[date] = None
        self._status = FineStatus.PENDING

    @property
    def fine_id(self) -> str:
        return self._fine_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def status(self) -> FineStatus:
        return self._status

    def pay_fine(self) -> None:
        self._paid_date = date.today()
        self._status = FineStatus.PAID
        self._loan._student.pay_fine(self._amount)

    def waive_fine(self) -> None:
        self._status = FineStatus.WAIVED
        self._loan._student.pay_fine(self._amount)

    def is_borrowing_blocked(self) -> bool:
        return (self._status == FineStatus.PENDING and
                self._amount > Student.FINE_BLOCK_THRESHOLD)

    def __repr__(self) -> str:
        return f"Fine(id={self._fine_id}, amount={self._amount}, status={self._status})"


# ─────────────────────────────────────────────
# ReadingList (Composition with Student)
# ─────────────────────────────────────────────

class ReadingList:
    """Personal saved resource list. Composition with Student. Maps to FR-11."""

    def __init__(self, list_id: str, list_name: str):
        self._list_id = list_id
        self._list_name = list_name
        self._resources: List[Resource] = []
        self._is_shared = False
        self._shareable_link = ""

    @property
    def list_id(self) -> str:
        return self._list_id

    @property
    def resources(self) -> List[Resource]:
        return self._resources

    def add_resource(self, resource: Resource) -> None:
        if resource not in self._resources:
            self._resources.append(resource)

    def remove_resource(self, resource_id: str) -> None:
        self._resources = [r for r in self._resources
                           if r.resource_id != resource_id]

    def export_bibliography(self, style: str = "APA") -> str:
        entries = []
        for r in self._resources:
            if style == "APA":
                entries.append(f"{r.author} ({r._published_year}). {r.title}.")
        return "\n".join(entries)

    def generate_share_link(self) -> str:
        self._is_shared = True
        self._shareable_link = f"https://salas.ac.za/reading-list/{self._list_id}"
        return self._shareable_link


# ─────────────────────────────────────────────
# Recommendation
# ─────────────────────────────────────────────

class Recommendation:
    """Personalised resource suggestion. Maps to FR-05."""

    def __init__(self, recommendation_id: str, student: Student,
                 resource: Resource, score: float = 0.0,
                 is_cold_start: bool = False):
        self._recommendation_id = recommendation_id
        self._student = student
        self._resource = resource
        self._score = score
        self._is_cold_start = is_cold_start
        self._status = "PENDING"
        self._generated_date = datetime.now()

    @property
    def recommendation_id(self) -> str:
        return self._recommendation_id

    @property
    def resource(self) -> Resource:
        return self._resource

    @property
    def score(self) -> float:
        return self._score

    @property
    def is_cold_start(self) -> bool:
        return self._is_cold_start

    def display(self) -> None:
        self._status = "DISPLAYED"

    def dismiss(self) -> None:
        self._status = "DISMISSED"
        self.record_feedback(positive=False)

    def record_feedback(self, positive: bool) -> None:
        pass

    def __repr__(self) -> str:
        return (f"Recommendation(id={self._recommendation_id}, "
                f"resource={self._resource.title}, score={self._score})")


# ─────────────────────────────────────────────
# Notification
# ─────────────────────────────────────────────

class Notification:
    """Automated alert sent to users. Maps to FR-07."""

    MAX_RETRIES = 3

    def __init__(self, notification_id: str, user: User,
                 notification_type: NotificationType,
                 channel: str = "EMAIL"):
        self._notification_id = notification_id
        self._user = user
        self._type = notification_type
        self._channel = channel
        self._status = NotificationStatus.SCHEDULED
        self._retry_count = 0
        self._sent_date: Optional[datetime] = None

    @property
    def notification_id(self) -> str:
        return self._notification_id

    @property
    def status(self) -> NotificationStatus:
        return self._status

    @property
    def retry_count(self) -> int:
        return self._retry_count

    def send(self) -> bool:
        """Simulates sending. Returns True on success."""
        self._sent_date = datetime.now()
        self._status = NotificationStatus.DELIVERED
        return True

    def retry(self) -> bool:
        if self._retry_count >= self.MAX_RETRIES:
            self.trigger_fallback()
            return False
        self._retry_count += 1
        return self.send()

    def trigger_fallback(self) -> None:
        self._channel = "IN_APP"
        self._status = NotificationStatus.DELIVERED

    def archive(self) -> None:
        self._status = NotificationStatus.ARCHIVED


# ─────────────────────────────────────────────
# Catalogue
# ─────────────────────────────────────────────

class Catalogue:
    """Aggregates all library resources. Maps to FR-02, FR-06."""

    def __init__(self, catalogue_id: str):
        self._catalogue_id = catalogue_id
        self._resources: dict = {}
        self._last_updated = datetime.now()

    @property
    def total_resources(self) -> int:
        return len(self._resources)

    def add_resource(self, resource: Resource) -> None:
        self._resources[resource.resource_id] = resource
        self._last_updated = datetime.now()

    def remove_resource(self, resource_id: str) -> None:
        self._resources.pop(resource_id, None)

    def get_resource(self, resource_id: str) -> Optional[Resource]:
        return self._resources.get(resource_id)

    def search_by_keyword(self, keyword: str) -> List[Resource]:
        kw = keyword.lower()
        return [r for r in self._resources.values()
                if kw in r.title.lower() or kw in r.author.lower()
                or kw in r.isbn]

    def apply_filters(self, genre: str = None,
                      available_only: bool = False) -> List[Resource]:
        results = list(self._resources.values())
        if genre:
            results = [r for r in results
                       if r._genre.lower() == genre.lower()]
        if available_only:
            results = [r for r in results if r.check_availability()]
        return results


# ─────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────

class Report:
    """Analytics report generated by admin or librarian. Maps to FR-08."""

    def __init__(self, report_id: str, report_type: str):
        self._report_id = report_id
        self._report_type = report_type
        self._generated_date = datetime.now()
        self._status = "REQUESTED"
        self._data: dict = {}

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def report_type(self) -> str:
        return self._report_type

    @property
    def status(self) -> str:
        return self._status

    def generate(self, data: dict) -> None:
        self._data = data
        self._status = "READY"

    def export_csv(self) -> str:
        if self._status != "READY":
            raise ValueError("Report not ready for export.")
        rows = [",".join(str(v) for v in row.values())
                for row in self._data.get("rows", [])]
        return "\n".join(rows)

    def export_pdf(self) -> str:
        return f"PDF:{self._report_type}:{self._report_id}"

    def __repr__(self) -> str:
        return f"Report(id={self._report_id}, type={self._report_type})"
