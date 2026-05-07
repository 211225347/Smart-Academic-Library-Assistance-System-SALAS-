"""
factories/repository_factory.py
Repository Factory — single abstraction point for storage backend switching.

Design Choice: Factory Pattern
All repository creation goes through this factory.
Storage type switching happens ONLY here — business logic never changes.

Usage:
    repo = RepositoryFactory.get_user_repository("MEMORY")
    repo = RepositoryFactory.get_resource_repository("FILESYSTEM")
    repo = RepositoryFactory.get_resource_repository("DATABASE")  # future
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from repositories.interfaces import (
    UserRepository, ResourceRepository, LoanRepository,
    ReservationRepository, FineRepository, NotificationRepository,
    RecommendationRepository, ReportRepository
)
from repositories.inmemory.inmemory_repositories import (
    InMemoryUserRepository, InMemoryResourceRepository,
    InMemoryLoanRepository, InMemoryReservationRepository,
    InMemoryFineRepository, InMemoryNotificationRepository,
    InMemoryRecommendationRepository, InMemoryReportRepository
)
from repositories.filesystem.filesystem_repositories import (
    FileSystemResourceRepository, FileSystemUserRepository
)


class RepositoryFactory:
    """
    Factory that returns the correct repository implementation
    based on the requested storage type string.

    Supported storage types: "MEMORY", "FILESYSTEM", "DATABASE"

    Example:
        repo = RepositoryFactory.get_user_repository("MEMORY")
        repo.save(student)

        # Switch to filesystem — no changes to calling code:
        repo = RepositoryFactory.get_user_repository("FILESYSTEM")
        repo.save(student)
    """

    @staticmethod
    def get_user_repository(
            storage_type: str = "MEMORY") -> UserRepository:
        if storage_type == "MEMORY":
            return InMemoryUserRepository()
        elif storage_type == "FILESYSTEM":
            return FileSystemUserRepository("data/users.json")
        elif storage_type == "DATABASE":
            raise NotImplementedError(
                "DatabaseUserRepository scheduled for Sprint 5."
            )
        else:
            raise ValueError(
                f"Unsupported storage type: '{storage_type}'. "
                "Must be MEMORY, FILESYSTEM, or DATABASE."
            )

    @staticmethod
    def get_resource_repository(
            storage_type: str = "MEMORY",
            file_path: str = "data/resources.json") -> ResourceRepository:
        if storage_type == "MEMORY":
            return InMemoryResourceRepository()
        elif storage_type == "FILESYSTEM":
            return FileSystemResourceRepository(file_path)
        elif storage_type == "DATABASE":
            raise NotImplementedError(
                "DatabaseResourceRepository scheduled for Sprint 5."
            )
        else:
            raise ValueError(
                f"Unsupported storage type: '{storage_type}'."
            )

    @staticmethod
    def get_loan_repository(
            storage_type: str = "MEMORY") -> LoanRepository:
        if storage_type == "MEMORY":
            return InMemoryLoanRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} LoanRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_reservation_repository(
            storage_type: str = "MEMORY") -> ReservationRepository:
        if storage_type == "MEMORY":
            return InMemoryReservationRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} ReservationRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_fine_repository(
            storage_type: str = "MEMORY") -> FineRepository:
        if storage_type == "MEMORY":
            return InMemoryFineRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} FineRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_notification_repository(
            storage_type: str = "MEMORY") -> NotificationRepository:
        if storage_type == "MEMORY":
            return InMemoryNotificationRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} NotificationRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_recommendation_repository(
            storage_type: str = "MEMORY") -> RecommendationRepository:
        if storage_type == "MEMORY":
            return InMemoryRecommendationRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} RecommendationRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_report_repository(
            storage_type: str = "MEMORY") -> ReportRepository:
        if storage_type == "MEMORY":
            return InMemoryReportRepository()
        else:
            raise NotImplementedError(
                f"{storage_type} ReportRepository scheduled for Sprint 5."
            )

    @staticmethod
    def get_all(storage_type: str = "MEMORY") -> dict:
        """
        Returns all repositories for the given storage type.
        Useful for service layer initialisation.

        Returns:
            dict with keys: users, resources, loans, reservations,
                            fines, notifications, recommendations, reports
        """
        return {
            "users": RepositoryFactory.get_user_repository(storage_type),
            "resources": RepositoryFactory.get_resource_repository(
                storage_type),
            "loans": RepositoryFactory.get_loan_repository(storage_type),
            "reservations": RepositoryFactory.get_reservation_repository(
                storage_type),
            "fines": RepositoryFactory.get_fine_repository(storage_type),
            "notifications": RepositoryFactory.get_notification_repository(
                storage_type),
            "recommendations": RepositoryFactory.get_recommendation_repository(
                storage_type),
            "reports": RepositoryFactory.get_report_repository(storage_type),
        }
