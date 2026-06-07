# src/models.py
from enum import Enum
from datetime import date, timedelta
import copy

# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class Role(Enum):
    STUDENT = "STUDENT"
    LIBRARIAN = "LIBRARIAN"
    ADMIN = "ADMIN"

class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    LOCKED = "LOCKED"

class NotificationType(Enum):
    DUE_SOON = "DUE_SOON"
    OVERDUE = "OVERDUE"
    RESERVATION_CONFIRMED = "RESERVATION_CONFIRMED"
    NEW_ARRIVAL = "NEW_ARRIVAL"

class NotificationStatus(Enum):
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

class LoanStatus(Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    DUE_SOON = "DUE_SOON"
    ARCHIVED = "ARCHIVED"

class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    QUEUED = "QUEUED"
    COLLECTED = "COLLECTED"

class FineStatus(Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    PENDING = "PENDING"

class RecommendationStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# ─────────────────────────────────────────────
# Core Domain Classes
# ─────────────────────────────────────────────

class User:
    def __init__(self, user_id, name, email, password, role: Role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.account_status = AccountStatus.ACTIVE

class Student(User):
    def __init__(self, user_id, name, email, password,
                 student_number, course_enrollment):
        super().__init__(user_id, name, email, password, Role.STUDENT)
        self.student_number = student_number
        self.course_enrollment = course_enrollment

class Librarian(User):
    def __init__(self, user_id, name, email, password,
                 staff_id, department):
        super().__init__(user_id, name, email, password, Role.LIBRARIAN)
        self.staff_id = staff_id
        self.department = department

class Resource:
    def __init__(self, resource_id, title, author, isbn,
                 genre, published_year, total_copies, location):
        self.resource_id = resource_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self._genre = genre
        self._published_year = published_year
        self._total_copies = total_copies
        self._location = location
        self._available_copies = total_copies
        self.status = Enum("ResourceStatus", {"AVAILABLE": "AVAILABLE", "UNAVAILABLE": "UNAVAILABLE"})("AVAILABLE")

    def validate_isbn(self) -> bool:
        return isinstance(self.isbn, str) and len(self.isbn) in (10, 13)

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        self._available_copies = value

    def __deepcopy__(self, memo):
        return copy.copy(self)

class Loan:
    def __init__(self, loan_id: str, student: Student, resource: Resource, borrowed_date: date, due_date: date):
        self.loan_id = loan_id
        self._student = student
        self.resource = resource
        self._borrowed_date = borrowed_date
        self.due_date = due_date
        self.status = LoanStatus.ACTIVE

    def is_overdue(self) -> bool:
        return self.status == LoanStatus.OVERDUE or (date.today() > self.due_date and self.status != LoanStatus.RETURNED)

    def calculate_fine(self) -> float:
        if self.is_overdue() and date.today() > self.due_date:
            days_overdue = (date.today() - self.due_date).days
            fine = days_overdue * 5.0
            return min(fine, 200.0)
        return 0.0

class Reservation:
    def __init__(self, reservation_id: str, student: Student, resource: Resource, reservation_date: date = None):
        self.reservation_id = reservation_id
        self._student = student
        self._resource = resource
        self.reservation_date = reservation_date if reservation_date else date.today()
        self.expiry_date = self.reservation_date + timedelta(days=2)  # 48-hour pickup window
        self.status = ReservationStatus.PENDING
        self._queue_position = 0

    def is_expired(self) -> bool:
        return date.today() > self.expiry_date

class Fine:
    def __init__(self, fine_id: str, loan: Loan, amount: float):
        self.fine_id = fine_id
        self._loan = loan
        self.amount = amount
        self.status = FineStatus.PENDING

class Recommendation:
    def __init__(self, recommendation_id: str, student: Student, title: str, author: str, isbn: str):
        self.recommendation_id = recommendation_id
        self._student = student
        self.title = title
        self.author = author
        self.isbn = isbn
        self._status = "PENDING"

class Notification:
    def __init__(self, notification_id: str, user: User, notification_type: NotificationType, message: str):
        self.notification_id = notification_id
        self._user = user
        self.type = notification_type
        self.message = message
        self.status = NotificationStatus.SCHEDULED

class Report:
    def __init__(self, report_id: str, title: str, report_type: str = "GENERAL"):
        self.report_id = report_id
        self.title = title
        self.report_type = report_type
        self.status = "PENDING"

    def generate(self, data):
        self.data = data
        self.status = "READY"
        return self

class Catalogue:
    def __init__(self, catalogue_id):
        self.catalogue_id = catalogue_id