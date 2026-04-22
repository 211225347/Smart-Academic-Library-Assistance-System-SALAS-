"""
creational_patterns/simple_factory.py
Pattern: Simple Factory
Use Case: Centralised creation of User objects (Student, Librarian, Admin)
          based on a role string — used during registration (FR-01).

Justification: The registration endpoint receives a role string from the
request payload. A Simple Factory centralises the branching logic so the
controller never needs to know which subclass to instantiate.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Student, Librarian, User, Role


class UserFactory:
    """
    Simple Factory that creates the correct User subclass based on role string.
    Maps to FR-01 (Registration) and FR-10 (RBAC).
    """

    @staticmethod
    def create_user(role: str, user_id: str, name: str, email: str,
                    password: str, **kwargs) -> User:
        """
        Factory method — returns the correct User subclass.

        Args:
            role: "STUDENT", "LIBRARIAN", or "ADMIN"
            user_id: Unique identifier
            name: Full name
            email: University email
            password: Plain-text password (hashed internally)
            **kwargs: Role-specific fields (student_number, staff_id, etc.)

        Returns:
            Student or Librarian instance

        Raises:
            ValueError: If role is not recognised
        """
        role_upper = role.upper()

        if role_upper == "STUDENT":
            return Student(
                user_id=user_id,
                name=name,
                email=email,
                password=password,
                student_number=kwargs.get("student_number", ""),
                course_enrollment=kwargs.get("course_enrollment", [])
            )
        elif role_upper == "LIBRARIAN":
            return Librarian(
                user_id=user_id,
                name=name,
                email=email,
                password=password,
                staff_id=kwargs.get("staff_id", ""),
                department=kwargs.get("department", "General")
            )
        else:
            raise ValueError(
                f"Unknown role: '{role}'. Must be STUDENT or LIBRARIAN."
            )


# ── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    student = UserFactory.create_user(
        role="STUDENT",
        user_id="u001",
        name="Alice Dlamini",
        email="alice@university.ac.za",
        password="Pass@123",
        student_number="211001",
        course_enrollment=["Computer Science"]
    )
    librarian = UserFactory.create_user(
        role="LIBRARIAN",
        user_id="u002",
        name="Bob Nkosi",
        email="bob@university.ac.za",
        password="Staff@456",
        staff_id="LIB001",
        department="Reference"
    )
    print(student)
    print(librarian)
    print(f"Student role: {student.role}")
    print(f"Librarian role: {librarian.role}")
