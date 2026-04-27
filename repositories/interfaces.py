
"""
Repository interfaces for SALAS (Assignment 11).

Defines abstract base classes for all repository contracts.
Concrete implementations (in-memory, filesystem, database)
must implement these interfaces.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class UserRepository(ABC):
    @abstractmethod
    def add(self, user) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass


class ResourceRepository(ABC):
    @abstractmethod
    def add(self, resource) -> None:
        pass

    @abstractmethod
    def get_by_id(self, resource_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass


class LoanRepository(ABC):
    @abstractmethod
    def add(self, loan) -> None:
        pass

    @abstractmethod
    def get_by_id(self, loan_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass


class ReservationRepository(ABC):
    @abstractmethod
    def add(self, reservation) -> None:
        pass

    @abstractmethod
    def get_by_id(self, reservation_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass
