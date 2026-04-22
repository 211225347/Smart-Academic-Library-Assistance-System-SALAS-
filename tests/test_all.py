# tests/test_all.py
import threading
from src.models import Student, Resource, NotificationType
from creational_patterns.simple_factory import UserFactory
from creational_patterns.factory_method import get_notification_creator
from creational_patterns.abstract_factory import get_export_factory
from creational_patterns.builder import ResourceBuilder
from creational_patterns.prototype import ResourceCache, create_resource_from_prototype
from creational_patterns.singleton import DatabaseConnection

# ─────────────────────────────────────────────
# Simple Factory
# ─────────────────────────────────────────────

def test_simple_factory_creates_student():
    student = UserFactory.create_user(
        role="STUDENT",
        user_id="s1",
        name="Test",
        email="t@u.ac.za",
        password="Pass@123",
        student_number="100",
        course_enrollment=["CS"]
    )
    assert isinstance(student, Student)

# ─────────────────────────────────────────────
# Factory Method
# ─────────────────────────────────────────────

def test_factory_method_creates_notification():
    creator = get_notification_creator("DUE_SOON")
    notification = creator.create_notification(
        Student("s1", "A", "a@u.ac.za", "x", "100", [])
    )
    assert notification.type == NotificationType.DUE_SOON

# ─────────────────────────────────────────────
# Abstract Factory
# ─────────────────────────────────────────────

def test_abstract_factory_creates_consistent_family():
    factory = get_export_factory("CSV")
    formatter = factory.create_formatter()
    renderer = factory.create_renderer()
    assert formatter is not None and renderer is not None

# ─────────────────────────────────────────────
# Builder
# ─────────────────────────────────────────────

def test_builder_constructs_resource():
    resource = (
        ResourceBuilder("r1", "Book", "Author", "1234567890")
        .with_genre("Test")
        .build()
    )
    assert isinstance(resource, Resource)

# ─────────────────────────────────────────────
# Prototype
# ─────────────────────────────────────────────

def test_prototype_cloning_independent():
    ResourceCache.load_cache()
    r1 = create_resource_from_prototype(
        "TEXTBOOK", "r1", "Book 1", "Author", "1234567890"
    )
    r2 = create_resource_from_prototype(
        "TEXTBOOK", "r2", "Book 2", "Author", "1234567890"
    )
    assert r1 is not r2

# ─────────────────────────────────────────────
# Singleton
# ─────────────────────────────────────────────

def test_singleton_single_instance():
    DatabaseConnection.reset_instance()
    a = DatabaseConnection.get_instance()
    b = DatabaseConnection.get_instance()
    assert a is b
