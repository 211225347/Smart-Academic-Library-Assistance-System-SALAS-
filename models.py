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

class NotificationType(Enum):
    DUE_SOON = "DUE_SOON"
    OVERDUE = "OVERDUE"
    RESERVATION_CONFIRMED = "RESERVATION_CONFIRMED"
    NEW_ARRIVAL = "NEW_ARRIVAL"

class NotificationStatus(Enum):
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"

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
        self._resource_id = resource_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._genre = genre
        self._published_year = published_year
        self._total_copies = total_copies
        self._location = location
        self._available_copies = total_copies

    def validate_isbn(self) -> bool:
        return isinstance(self._isbn, str) and len(self._isbn) in (10, 13)

    @property
    def available_copies(self):
        return self._available_copies

    def __deepcopy__(self, memo):
        return copy.copy(self)

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
