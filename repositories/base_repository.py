
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity"""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Retrieve a single entity by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Retrieve all entities"""
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """Delete an entity by ID"""
        pass
``
