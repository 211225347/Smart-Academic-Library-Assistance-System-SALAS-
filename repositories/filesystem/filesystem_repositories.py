"""
repositories/filesystem/filesystem_repositories.py
Filesystem JSON implementations — future storage backend (Sprint 4).

Both FileSystemResourceRepository and FileSystemUserRepository are
functional for basic operations. DatabaseResourceRepository is a stub.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import json
from typing import Optional, List
from repositories.interfaces import ResourceRepository, UserRepository
from src.models import Resource, User, Student, Librarian, Role


class FileSystemResourceRepository(ResourceRepository):
    """
    Filesystem JSON implementation of ResourceRepository.
    Serializes Resource objects to a JSON file.
    Future implementation target: Sprint 4. Maps to FR-02, FR-06.
    """

    def __init__(self, file_path: str = "data/resources.json"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)

    def _load(self) -> dict:
        if not os.path.exists(self._file_path):
            return {}
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, entity: Resource) -> None:
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
        return [self.find_by_id(rid) for rid in self._load()]

    def delete(self, entity_id: str) -> None:
        data = self._load()
        data.pop(entity_id, None)
        self._save_all(data)

    def find_by_title(self, title: str) -> List[Resource]:
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

    def count(self) -> int:
        return len(self._load())

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._load()


class FileSystemUserRepository(UserRepository):
    """
    Filesystem JSON implementation of UserRepository.
    Serializes User objects to a JSON file.
    Future implementation target: Sprint 4. Maps to FR-01, FR-10.
    """

    def __init__(self, file_path: str = "data/users.json"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)

    def _load(self) -> dict:
        if not os.path.exists(self._file_path):
            return {}
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _save_all(self, data: dict) -> None:
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, entity: User) -> None:
        data = self._load()
        data[entity.user_id] = {
            "user_id": entity.user_id,
            "name": entity.name,
            "email": entity.email,
            "role": entity.role.value,
        }
        self._save_all(data)

    def find_by_id(self, entity_id: str) -> Optional[User]:
        # TODO Sprint 4: Full deserialization
        data = self._load()
        return data.get(entity_id)

    def find_all(self) -> List[User]:
        return list(self._load().values())

    def delete(self, entity_id: str) -> None:
        data = self._load()
        data.pop(entity_id, None)
        self._save_all(data)

    def find_by_email(self, email: str) -> Optional[User]:
        for record in self._load().values():
            if isinstance(record, dict):
                if record.get("email", "").lower() == email.lower():
                    return record
        return None

    def find_by_role(self, role: str) -> List[User]:
        return [r for r in self._load().values()
                if isinstance(r, dict) and r.get("role") == role.upper()]

    def find_active_users(self) -> List[User]:
        return list(self._load().values())

    def count(self) -> int:
        return len(self._load())

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._load()


class DatabaseResourceRepository(ResourceRepository):
    """
    PostgreSQL stub — future implementation (Sprint 5).
    Uses SQLAlchemy ORM. Interface contract preserved.
    Maps to FR-02, FR-06, NFR-07.
    """

    def __init__(self, connection_string: str = None):
        self._connection_string = (
            connection_string
            or "postgresql://salas_user:password@localhost:5432/salas_db"
        )

    def save(self, entity: Resource) -> None:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_by_id(self, entity_id: str) -> Optional[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def find_all(self) -> List[Resource]:
        raise NotImplementedError("Scheduled for Sprint 5.")

    def delete(self, entity_id: str) -> None:
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
