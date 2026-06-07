# src/models.py
from enum import Enum
from datetime import date
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

class LoanStatus(Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class FineStatus(Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"

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

    def calculate_fine(self) -> float:
        if self.status == LoanStatus.OVERDUE and date.today() > self.due_date:
            days_overdue = (date.today() - self.due_date).days
            fine = days_overdue * 5.0
            return min(fine, 200.0)  # BR-10: Max cap R200
        return 0.0

class Reservation:
    def __init__(self, reservation_id: str, user_id: str, resource_id: str, reservation_date: date):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.resource_id = resource_id
        self.reservation_date = reservation_date
        self.status = ReservationStatus.PENDING

class Fine:
    def __init__(self, fine_id: str, loan_id: str, student_id: str, amount: float):
        self.fine_id = fine_id
        self.loan_id = loan_id
        self.student_id = student_id
        self.amount = amount
        self.status = FineStatus.UNPAID

class Recommendation:
    def __init__(self, recommendation_id: str, user_id: str, title: str, author: str, isbn: str):
        self.recommendation_id = recommendation_id
        self.user_id = user_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = RecommendationStatus.PENDING

class Notification:
    def __init__(self, user, notification_type: NotificationType, message):
        self.user = user
        self.type = notification_type
        self.message = message
        self.status = NotificationStatus.SCHEDULED

class Report:
    def __init__(self, report_id, title):
        self.report_id = report_id
        self.title = title

    def generate(self, data):
        self.data = data
        return self

class Catalogue:
    def __init__(self, catalogue_id):
        self.catalogue_id = catalogue_id