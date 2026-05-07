"""
repositories/base_repository.py
Single canonical generic Repository interface for SALAS.

This is the single source of truth for the generic CRUD contract.
All entity-specific repository interfaces extend this class.

Design: Generic[T, ID] avoids code duplication across all entity
repositories while preserving type safety.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """
    Generic repository interface defining standard CRUD operations.
    All entity-specific repositories must extend this interface.

    Type Parameters:
        T  — The domain entity type (e.g., Resource, Student)
        ID — The identifier type (str for all SALAS entities)
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity (upsert by ID)."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return entity by ID, or None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all stored entities as a list."""
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """Delete entity by ID. No-op if entity does not exist."""
        pass
