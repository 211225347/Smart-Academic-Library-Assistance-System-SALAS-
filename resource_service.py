"""
services/resource_service.py
ResourceService — encapsulates all business logic for Resource operations.

Uses the ResourceRepository (Assignment 11) for persistence.
Enforces BR-04 (no delete with active loans), BR-05 (ISBN validation).
Maps to: FR-02 (Search), FR-06 (Catalogue Management).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import Optional, List
from src.models import Resource
from repositories.interfaces import ResourceRepository, LoanRepository


class ResourceNotFoundError(Exception):
    """Raised when a resource does not exist."""
    pass


class ResourceHasActiveLoansError(Exception):
    """Raised when trying to delete a resource with active loans (BR-04)."""
    pass


class InvalidISBNError(Exception):
    """Raised when ISBN fails validation (BR-05)."""
    pass


class ResourceService:
    """
    Service class encapsulating all Resource business operations.

    Depends on ResourceRepository and optionally LoanRepository
    (to check active loans before deletion). Both injected —
    never instantiated directly inside the service.

    Usage:
        resource_repo = RepositoryFactory.get_resource_repository("MEMORY")
        loan_repo = RepositoryFactory.get_loan_repository("MEMORY")
        service = ResourceService(resource_repo, loan_repo)
    """

    def __init__(self, resource_repository: ResourceRepository,
                 loan_repository: LoanRepository = None):
        self._repo = resource_repository
        self._loan_repo = loan_repository

    # ── Create ─────────────────────────────────────────────────────────────

    def add_resource(self, resource_id: str, title: str, author: str,
                     isbn: str, genre: str, published_year: int,
                     total_copies: int, location: str) -> Resource:
        """
        Adds a new resource to the catalogue.
        Validates ISBN before saving (BR-05).
        Maps to FR-06 (Catalogue Management).
        """
        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")

        resource = Resource(
            resource_id=resource_id,
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            published_year=published_year,
            total_copies=total_copies,
            location=location
        )
        if not resource.validate_isbn():
            raise InvalidISBNError(
                f"ISBN '{isbn}' is invalid. "
                "Must pass ISBN-10 or ISBN-13 check digit validation (BR-05)."
            )
        self._repo.save(resource)
        return resource

    # ── Read ───────────────────────────────────────────────────────────────

    def get_resource(self, resource_id: str) -> Resource:
        """Retrieve a resource by ID. Raises ResourceNotFoundError if missing."""
        resource = self._repo.find_by_id(resource_id)
        if not resource:
            raise ResourceNotFoundError(
                f"Resource '{resource_id}' not found."
            )
        return resource

    def get_all_resources(self) -> List[Resource]:
        """Return all resources in the catalogue."""
        return self._repo.find_all()

    def search(self, keyword: str) -> List[Resource]:
        """
        Full-text keyword search across title, author, and ISBN.
        Maps to FR-02 (Search Library Catalogue).
        """
        if not keyword or len(keyword.strip()) < 1:
            raise ValueError("Search keyword must not be empty.")
        return self._repo.search(keyword.strip())

    def get_available_resources(self) -> List[Resource]:
        """Return resources with at least one available copy (FR-02)."""
        return self._repo.find_available()

    def get_by_genre(self, genre: str) -> List[Resource]:
        """Filter resources by genre (FR-02)."""
        return self._repo.find_by_genre(genre)

    def get_by_isbn(self, isbn: str) -> Optional[Resource]:
        """Find resource by exact ISBN."""
        return self._repo.find_by_isbn(isbn)

    # ── Update ─────────────────────────────────────────────────────────────

    def update_resource(self, resource_id: str, title: str = None,
                        author: str = None, genre: str = None,
                        total_copies: int = None,
                        location: str = None) -> Resource:
        """
        Updates resource metadata.
        Maps to FR-06 (Catalogue Management — Edit).
        """
        resource = self.get_resource(resource_id)

        if title:
            resource._title = title
        if author:
            resource._author = author
        if genre:
            resource._genre = genre
        if total_copies is not None:
            if total_copies < 1:
                raise ValueError("Total copies must be at least 1.")
            diff = total_copies - resource._total_copies
            resource._total_copies = total_copies
            resource._available_copies = max(
                0, resource._available_copies + diff
            )
        if location:
            resource._location = location

        self._repo.save(resource)
        return resource

    # ── Delete ─────────────────────────────────────────────────────────────

    def delete_resource(self, resource_id: str) -> None:
        """
        Deletes a resource from the catalogue.
        Blocks deletion if active loans exist (BR-04).
        Maps to FR-06 (Catalogue Management — Delete).
        """
        resource = self.get_resource(resource_id)

        if self._loan_repo:
            active_loans = self._loan_repo.find_by_resource(resource_id)
            if active_loans:
                raise ResourceHasActiveLoansError(
                    f"Cannot delete '{resource_id}': "
                    f"{len(active_loans)} active loan(s) exist (BR-04)."
                )

        self._repo.delete(resource_id)

    # ── Availability ───────────────────────────────────────────────────────

    def check_availability(self, resource_id: str) -> dict:
        """
        Returns real-time availability information for a resource.
        Maps to FR-02 acceptance criteria: availability shown in results.
        """
        resource = self.get_resource(resource_id)
        return {
            "resource_id": resource_id,
            "title": resource.title,
            "total_copies": resource._total_copies,
            "available_copies": resource.available_copies,
            "is_available": resource.check_availability(),
            "status": resource.status.value
        }
