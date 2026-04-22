"""
creational_patterns/builder.py
Pattern: Builder
Use Case: Constructing Resource objects step-by-step — a Resource has
          many optional attributes (cover image, genre, location, etc.)
          and a required core (title, author, ISBN). Builder separates
          mandatory construction from optional configuration.

Justification: FR-06 requires librarians to add resources with variable
sets of metadata. Some resources have cover images; others don't. Some
have physical locations; digital resources do not. Builder prevents
constructors with 10+ parameters and makes the creation process readable.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Resource


class ResourceBuilder:
    """
    Builder for constructing Resource objects step-by-step.
    Mandatory fields are set in the constructor.
    Optional fields are set via chained setter methods.
    """

    def __init__(self, resource_id: str, title: str,
                 author: str, isbn: str):
        """
        Initialise with mandatory fields only.

        Args:
            resource_id: Unique resource identifier
            title: Resource title (mandatory)
            author: Author name (mandatory)
            isbn: ISBN-10 or ISBN-13 (mandatory, validated on build)
        """
        self._resource_id = resource_id
        self._title = title
        self._author = author
        self._isbn = isbn
        # Optional fields with defaults
        self._genre = "General"
        self._published_year = 2024
        self._total_copies = 1
        self._location = "General Stacks"
        self._cover_image_url = ""

    def with_genre(self, genre: str) -> "ResourceBuilder":
        self._genre = genre
        return self

    def with_published_year(self, year: int) -> "ResourceBuilder":
        if year < 1000 or year > 2100:
            raise ValueError(f"Invalid year: {year}")
        self._published_year = year
        return self

    def with_copies(self, total_copies: int) -> "ResourceBuilder":
        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")
        self._total_copies = total_copies
        return self

    def with_location(self, location: str) -> "ResourceBuilder":
        self._location = location
        return self

    def with_cover_image(self, url: str) -> "ResourceBuilder":
        self._cover_image_url = url
        return self

    def build(self) -> Resource:
        """
        Constructs and returns the Resource.
        Validates ISBN before building (BR-05).

        Returns:
            Fully configured Resource object

        Raises:
            ValueError: If ISBN validation fails
        """
        resource = Resource(
            resource_id=self._resource_id,
            title=self._title,
            author=self._author,
            isbn=self._isbn,
            genre=self._genre,
            published_year=self._published_year,
            total_copies=self._total_copies,
            location=self._location
        )
        resource._cover_image_url = self._cover_image_url

        if not resource.validate_isbn():
            raise ValueError(
                f"ISBN '{self._isbn}' is invalid. "
                "Must pass ISBN-10 or ISBN-13 check digit validation."
            )
        return resource


class ResourceDirector:
    """
    Director that defines standard construction sequences.
    Provides preset configurations for common resource types.
    """

    @staticmethod
    def construct_textbook(resource_id: str, title: str,
                           author: str, isbn: str) -> Resource:
        return (ResourceBuilder(resource_id, title, author, isbn)
                .with_genre("Textbook")
                .with_copies(5)
                .with_location("Textbook Reserve")
                .build())

    @staticmethod
    def construct_journal(resource_id: str, title: str,
                          author: str, isbn: str) -> Resource:
        return (ResourceBuilder(resource_id, title, author, isbn)
                .with_genre("Journal")
                .with_copies(2)
                .with_location("Periodicals Section")
                .build())

    @staticmethod
    def construct_reference(resource_id: str, title: str,
                            author: str, isbn: str) -> Resource:
        return (ResourceBuilder(resource_id, title, author, isbn)
                .with_genre("Reference")
                .with_copies(1)
                .with_location("Reference Section — No Checkout")
                .build())


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Manual builder chain
    resource = (
        ResourceBuilder("r001", "Clean Code", "Robert C. Martin",
                        "9780132350884")
        .with_genre("Software Engineering")
        .with_published_year(2008)
        .with_copies(3)
        .with_location("Computer Science — Shelf 4B")
        .with_cover_image("https://covers.openlibrary.org/b/id/8401411-L.jpg")
        .build()
    )
    print(f"Built: {resource}")
    print(f"  Genre: {resource._genre}")
    print(f"  Copies: {resource.available_copies}")
    print(f"  Location: {resource._location}")

    # Director shortcut
    textbook = ResourceDirector.construct_textbook(
        "r002", "Introduction to Algorithms",
        "Cormen et al.", "9780262033848"
    )
    print(f"\nTextbook: {textbook}")
    print(f"  Genre: {textbook._genre}")
    print(f"  Copies: {textbook.available_copies}")
