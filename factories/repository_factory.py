"""
factories/repository_factory.py
Repository Factory — returns the correct storage backend implementation
based on a configuration string.

Design Choice: Factory Pattern over Dependency Injection
-------------------------------------------------------
The assignment offered two options: Factory Pattern or Dependency Injection.

Factory Pattern was chosen because:
1. SALAS is currently a solo academic project — DI frameworks (like Python's
   'injector' or 'dependency_injector') add complexity without proportional benefit
   at this scale.
2. The Factory provides a single, explicit place to configure storage — any
   developer can read `RepositoryFactory.get_resource_repo("MEMORY")` and
   immediately understand which backend is active.
3. When the project grows to need DI (Sprint 5+, multiple developers, testing
   with mock injection), the Factory can be replaced without changing any service
   or controller code — they all depend on the interfaces, not the factory.

The Factory accepts a storage type string: "MEMORY", "FILESYSTEM", or "DATABASE".
This makes it trivial to switch backends via environment variable:
    storage_type = os.environ.get("SALAS_STORAGE", "MEMORY")
    repo = RepositoryFactory.get_resource_repo(storage_type)
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
    FileSystemResourceRepository, DatabaseResourceRepository
)


# Valid storage type constants
STORAGE_MEMORY = "MEMORY"
STORAGE_FILESYSTEM = "FILESYSTEM"
STORAGE_DATABASE = "DATABASE"

VALID_STORAGE_TYPES = {STORAGE_MEMORY, STORAGE_FILESYSTEM, STORAGE_DATABASE}


class RepositoryFactory:
    """
    Factory that returns the correct repository implementation
    based on the requested storage type.

    Usage:
        repo = RepositoryFactory.get_resource_repo("MEMORY")
        repo.save(resource)

        # Switch to filesystem with no changes to calling code:
        repo = RepositoryFactory.get_resource_repo("FILESYSTEM")
        repo.save(resource)  # Same interface, different backend
    """

    @staticmethod
    def _validate(storage_type: str) -> str:
        st = storage_type.upper()
        if st not in VALID_STORAGE_TYPES:
            raise ValueError(
                f"Invalid storage type: '{storage_type}'. "
                f"Must be one of: {sorted(VALID_STORAGE_TYPES)}"
            )
        return st

    # ── User Repository ────────────────────────────────────────────────────

    @staticmethod
    def get_user_repo(storage_type: str = STORAGE_MEMORY) -> UserRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryUserRepository()
        elif st == STORAGE_FILESYSTEM:
            # TODO Sprint 4: return FileSystemUserRepository()
            raise NotImplementedError(
                "Filesystem UserRepository scheduled for Sprint 4."
            )
        elif st == STORAGE_DATABASE:
            # TODO Sprint 5: return DatabaseUserRepository()
            raise NotImplementedError(
                "Database UserRepository scheduled for Sprint 5."
            )

    # ── Resource Repository ────────────────────────────────────────────────

    @staticmethod
    def get_resource_repo(
            storage_type: str = STORAGE_MEMORY,
            file_path: str = "data/resources.json") -> ResourceRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryResourceRepository()
        elif st == STORAGE_FILESYSTEM:
            return FileSystemResourceRepository(file_path)
        elif st == STORAGE_DATABASE:
            return DatabaseResourceRepository()

    # ── Loan Repository ────────────────────────────────────────────────────

    @staticmethod
    def get_loan_repo(storage_type: str = STORAGE_MEMORY) -> LoanRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryLoanRepository()
        else:
            raise NotImplementedError(
                f"{st} LoanRepository scheduled for Sprint 5."
            )

    # ── Reservation Repository ─────────────────────────────────────────────

    @staticmethod
    def get_reservation_repo(
            storage_type: str = STORAGE_MEMORY) -> ReservationRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryReservationRepository()
        else:
            raise NotImplementedError(
                f"{st} ReservationRepository scheduled for Sprint 5."
            )

    # ── Fine Repository ────────────────────────────────────────────────────

    @staticmethod
    def get_fine_repo(
            storage_type: str = STORAGE_MEMORY) -> FineRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryFineRepository()
        else:
            raise NotImplementedError(
                f"{st} FineRepository scheduled for Sprint 5."
            )

    # ── Notification Repository ────────────────────────────────────────────

    @staticmethod
    def get_notification_repo(
            storage_type: str = STORAGE_MEMORY) -> NotificationRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryNotificationRepository()
        else:
            raise NotImplementedError(
                f"{st} NotificationRepository scheduled for Sprint 5."
            )

    # ── Recommendation Repository ──────────────────────────────────────────

    @staticmethod
    def get_recommendation_repo(
            storage_type: str = STORAGE_MEMORY) -> RecommendationRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryRecommendationRepository()
        else:
            raise NotImplementedError(
                f"{st} RecommendationRepository scheduled for Sprint 5."
            )

    # ── Report Repository ──────────────────────────────────────────────────

    @staticmethod
    def get_report_repo(
            storage_type: str = STORAGE_MEMORY) -> ReportRepository:
        st = RepositoryFactory._validate(storage_type)
        if st == STORAGE_MEMORY:
            return InMemoryReportRepository()
        else:
            raise NotImplementedError(
                f"{st} ReportRepository scheduled for Sprint 5."
            )

    # ── Convenience: Get All Repos ─────────────────────────────────────────

    @staticmethod
    def get_all(storage_type: str = STORAGE_MEMORY) -> dict:
        """
        Returns a dict of all repositories for the given storage type.
        Useful for service layer initialisation.

        Example:
            repos = RepositoryFactory.get_all("MEMORY")
            user_service = UserService(repos["users"])
            resource_service = ResourceService(repos["resources"])
        """
        return {
            "users": RepositoryFactory.get_user_repo(storage_type),
            "resources": RepositoryFactory.get_resource_repo(storage_type),
            "loans": RepositoryFactory.get_loan_repo(storage_type),
            "reservations": RepositoryFactory.get_reservation_repo(
                storage_type),
            "fines": RepositoryFactory.get_fine_repo(storage_type),
            "notifications": RepositoryFactory.get_notification_repo(
                storage_type),
            "recommendations": RepositoryFactory.get_recommendation_repo(
                storage_type),
            "reports": RepositoryFactory.get_report_repo(storage_type),
        }
