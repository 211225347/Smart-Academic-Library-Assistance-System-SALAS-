"""
creational_patterns/prototype.py
Pattern: Prototype
Use Case: ResourceCache — stores pre-configured Resource prototypes
          (e.g., standard textbook template, journal template) and
          clones them when a librarian adds a new resource of the same
          type. Avoids re-running expensive ISBN validation and indexing
          for templated resources.

Justification: FR-06 requires bulk CSV import of up to 1,000 resources.
Many resources share the same genre, location, and copy count. Cloning
from a prototype is faster than constructing each from scratch, and
ensures consistent defaults across similar resources.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import copy
from typing import Dict, Optional
from src.models import Resource


class ResourcePrototype:
    """
    Defines the clone interface for Resource objects.
    Resource.clone() is already implemented via copy.deepcopy in models.py.
    This wrapper adds prototype registry management.
    """

    def clone(self) -> "Resource":
        raise NotImplementedError


class ResourceCache:
    """
    Prototype registry that stores and clones pre-configured Resource templates.
    Acts as the central cache for common resource configurations.
    """

    _cache: Dict[str, Resource] = {}

    @classmethod
    def load_cache(cls) -> None:
        """
        Pre-populates the cache with standard resource templates.
        Called once at application startup.
        """
        # Textbook template
        textbook = Resource(
            resource_id="PROTO_TEXTBOOK",
            title="[Template]",
            author="[Author]",
            isbn="9780132350884",  # Valid ISBN-13 for prototype
            genre="Textbook",
            published_year=2024,
            total_copies=3,
            location="Textbook Reserve"
        )
        cls._cache["TEXTBOOK"] = textbook

        # Journal template
        journal = Resource(
            resource_id="PROTO_JOURNAL",
            title="[Template]",
            author="[Author]",
            isbn="9780262033848",  # Valid ISBN-13 for prototype
            genre="Journal",
            published_year=2024,
            total_copies=1,
            location="Periodicals Section"
        )
        cls._cache["JOURNAL"] = journal

        # Reference template
        reference = Resource(
            resource_id="PROTO_REFERENCE",
            title="[Template]",
            author="[Author]",
            isbn="9780201633610",  # Valid ISBN-13 for prototype
            genre="Reference",
            published_year=2024,
            total_copies=1,
            location="Reference Section — No Checkout"
        )
        cls._cache["REFERENCE"] = reference

    @classmethod
    def get_clone(cls, prototype_key: str) -> Resource:
        """
        Returns a deep clone of the requested prototype.

        Args:
            prototype_key: Key identifying the prototype (e.g., "TEXTBOOK")

        Returns:
            A deep copy of the prototype Resource

        Raises:
            KeyError: If prototype_key is not in the cache
        """
        prototype = cls._cache.get(prototype_key.upper())
        if not prototype:
            raise KeyError(
                f"No prototype found for key: '{prototype_key}'. "
                f"Available: {list(cls._cache.keys())}"
            )
        cloned = copy.deepcopy(prototype)
        return cloned

    @classmethod
    def register_prototype(cls, key: str, resource: Resource) -> None:
        """Registers a new prototype in the cache."""
        cls._cache[key.upper()] = resource

    @classmethod
    def list_prototypes(cls) -> list:
        return list(cls._cache.keys())


def create_resource_from_prototype(prototype_key: str, resource_id: str,
                                   title: str, author: str,
                                   isbn: str) -> Resource:
    """
    Convenience function: clones a prototype and customises identity fields.

    Args:
        prototype_key: Which template to clone
        resource_id: New unique ID for the cloned resource
        title: Actual title for the new resource
        author: Actual author for the new resource
        isbn: Actual ISBN for the new resource

    Returns:
        Customised Resource clone
    """
    cloned = ResourceCache.get_clone(prototype_key)
    cloned._resource_id = resource_id
    cloned._title = title
    cloned._author = author
    cloned._isbn = isbn
    return cloned


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load prototypes once
    ResourceCache.load_cache()
    print("Prototypes loaded:", ResourceCache.list_prototypes())

    # Clone a textbook prototype and customise it
    new_textbook = create_resource_from_prototype(
        prototype_key="TEXTBOOK",
        resource_id="r_clean_code",
        title="Clean Code",
        author="Robert C. Martin",
        isbn="9780132350884"
    )
    print(f"\nCloned textbook: {new_textbook}")
    print(f"  Genre: {new_textbook._genre}")
    print(f"  Location: {new_textbook._location}")
    print(f"  Copies: {new_textbook.available_copies}")

    # Verify clone independence — changing clone does not affect prototype
    new_textbook._available_copies = 10
    original = ResourceCache.get_clone("TEXTBOOK")
    print(f"\nOriginal prototype copies: {original.available_copies}")
    print(f"Cloned resource copies: {new_textbook.available_copies}")
    print("Clone is independent of prototype:",
          original.available_copies != new_textbook.available_copies)
