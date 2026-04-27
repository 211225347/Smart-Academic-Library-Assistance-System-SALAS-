"""
repositories/filesystem/filesystem_repositories.py
Filesystem JSON stub implementation — future storage backend.

This stub demonstrates how the repository interfaces designed in
Assignment 11 make swapping storage backends trivial. A future
developer only needs to implement the same interfaces using JSON
file storage rather than an in-memory dict.

Status: STUB — method signatures are complete, implementations
        marked with TODO for future Sprint work.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import json
from typing import Optional, List
from repositories.interfaces import ResourceRepository, UserRepository
from src.models import Resource, User


class FileSystemResourceRepository(ResourceRepository):
    """
    Filesystem JSON implementation of ResourceRepository.
    Serializes Resource objects to a JSON file for persistence
    across application restarts.

    Future implementation target: Sprint 4
    Maps to: FR-02, FR-06
    """

    def __init__(self, file_path: str = "data/resources.json"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def _load(self) -> dict:
        """Load all records from the JSON file."""
        if not os.path.exists(self._file_path):
            return {}
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        """Persist all records back to the JSON file."""
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, entity: Resource) -> None:
        # TODO Sprint 4: Serialize Resource to dict and save to JSON
        data = self._load()
        data[entity.resource_id] = {
            "resource_id": entity.resource_id,
            "title": entity.title,
            "author": entity.author,
            "isbn": entity.isbn,
            "genre": entity._genre,
            "published_year": entity._published_year,
            "total_copies": entity._total_copies,
            "available_copies": entity.available_copies,
            "location": entity._location,
        }
        self._save_all(data)

    def find_by_id(self, entity_id: str) -> Optional[Resource]:
        # TODO Sprint 4: Deserialize dict back to Resource object
        data = self._load()
        record = data.get(entity_id)
        if not record:
            return None
        return Resource(
            resource_id=record["resource_id"],
            title=record["title"],
            author=record["author"],
            isbn=record["isbn"],
            genre=record["genre"],
            published_year=record["published_year"],
            total_copies=record["total_copies"],
            location=record["location"]
        )

    def find_all(self) -> List[Resource]:
        # TODO Sprint 4: Deserialize all records
        data = self._load()
        results = []
        for record in data.values():
            results.append(Resource(
                resource_id=record["resource_id"],
                title=record["title"],
                author=record["author"],
                isbn=record["isbn"],
                genre=record["genre"],
                published_year=record["published_year"],
                total_copies=record["total_copies"],
                location=record["location"]
            ))
        return results

    def delete(self, entity_id: str) -> bool:
        # TODO Sprint 4: Remove record from JSON file
        data = self._load()
        if entity_id in data:
            del data[entity_id]
            self._save_all(data)
            return True
        return False

    def count(self) -> int:
        return len(self._load())

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._load()

    def find_by_title(self, title: str) -> List[Resource]:
        # TODO Sprint 4: Filter loaded records by title
        return [r for r in self.find_all()
                if title.lower() in r.title.lower()]

    def find_by_author(self, author: str) -> List[Resource]:
        return [r for r in self.find_all()
                if author.lower() in r.author.lower()]

    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        for r in self.find_all():
            if r.isbn.replace("-", "") == isbn.replace("-", ""):
                return r
        return None

    def find_available(self) -> List[Resource]:
        return [r for r in self.find_all() if r.available_copies > 0]

    def find_by_genre(self, genre: str) -> List[Resource]:
        return [r for r in self.find_all()
                if r._genre.lower() == genre.lower()]

    def search(self, keyword: str) -> List[Resource]:
        kw = keyword.lower()
        return [r for r in self.find_all()
                if kw in r.title.lower()
                or kw in r.author.lower()
                or kw in r.isbn]


class DatabaseResourceRepository(ResourceRepository):
    """
    PostgreSQL database stub implementation of ResourceRepository.
    Uses SQLAlchemy ORM for actual database operations.

    This stub shows the interface contract is preserved regardless
    of storage backend. The business logic layer (services) never
    needs to change when swapping from InMemory → Filesystem → Database.

    Future implementation target: Sprint 5
    Maps to: FR-02, FR-06, NFR-07 (1,000 concurrent users)
    """

    def __init__(self, connection_string: str = None):
        # TODO Sprint 5: Initialize SQLAlchemy engine and session factory
        self._connection_string = (
            connection_string
            or "postgresql://salas_user:password@localhost:5432/salas_db"
        )
        self._session = None  # TODO: SQLAlchemy Session

    def save(self, entity: Resource) -> None:
        # TODO Sprint 5:
        # session.merge(ResourceORM.from_domain(entity))
        # session.commit()
        raise NotImplementedError(
            "DatabaseResourceRepository.save() — "
            "Scheduled for Sprint 5 implementation."
        )

    def find_by_id(self, entity_id: str) -> Optional[Resource]:
        # TODO Sprint 5:
        # record = session.query(ResourceORM).filter_by(resource_id=entity_id).first()
        # return record.to_domain() if record else None
        raise NotImplementedError(
            "DatabaseResourceRepository.find_by_id() — "
            "Scheduled for Sprint 5 implementation."
        )

    def find_all(self) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def count(self) -> int:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_by_title(self, title: str) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_by_author(self, author: str) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_by_isbn(self, isbn: str) -> Optional[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_available(self) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_by_genre(self, genre: str) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def search(self, keyword: str) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

class FileSystemUserRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, user):
        raise NotImplementedError("Filesystem storage not implemented yet")

    def find_by_id(self, user_id: str):
        raise NotImplementedError("Filesystem storage not implemented yet")

    def find_all(self):
        raise NotImplementedError("Filesystem storage not implemented yet")

    def delete(self, user_id: str):
        raise NotImplementedError("Filesystem storage not implemented yet")

