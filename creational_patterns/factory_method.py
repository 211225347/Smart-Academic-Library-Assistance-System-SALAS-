"""
creational_patterns/factory_method.py
Pattern: Factory Method
Use Case: Notification creation — different notification types (DueSoon,
          Overdue, ReservationConfirmed) are created by dedicated creator
          subclasses, each producing the correctly configured Notification.

Justification: FR-07 requires notifications triggered by different events
(loan due, overdue, reservation ready). Each event type has different
message content and delivery urgency. Factory Method delegates creation to
the appropriate subclass without the client needing to know the details.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from src.models import Notification, NotificationType, User


# ── Abstract Creator ──────────────────────────────────────────────────────────

class NotificationCreator(ABC):
    """Abstract creator declaring the factory method."""

    @abstractmethod
    def create_notification(self, notification_id: str,
                            user: User) -> Notification:
        """Factory method — subclasses decide which Notification to create."""
        pass

    def send_notification(self, notification_id: str, user: User) -> bool:
        """
        Template method: uses factory method then sends.
        The creator does not need to know which Notification subtype was made.
        """
        notification = self.create_notification(notification_id, user)
        return notification.send()


# ── Concrete Creators ─────────────────────────────────────────────────────────

class DueSoonNotificationCreator(NotificationCreator):
    """Creates a DUE_SOON notification — sent 3 days before due date."""

    def create_notification(self, notification_id: str,
                            user: User) -> Notification:
        return Notification(
            notification_id=notification_id,
            user=user,
            notification_type=NotificationType.DUE_SOON,
            channel="EMAIL"
        )


class OverdueNotificationCreator(NotificationCreator):
    """Creates an OVERDUE notification — sent 1 day after due date."""

    def create_notification(self, notification_id: str,
                            user: User) -> Notification:
        return Notification(
            notification_id=notification_id,
            user=user,
            notification_type=NotificationType.OVERDUE,
            channel="EMAIL"
        )


class ReservationConfirmedCreator(NotificationCreator):
    """Creates a RESERVATION_CONFIRMED notification."""

    def create_notification(self, notification_id: str,
                            user: User) -> Notification:
        return Notification(
            notification_id=notification_id,
            user=user,
            notification_type=NotificationType.RESERVATION_CONFIRMED,
            channel="EMAIL"
        )


class NewArrivalNotificationCreator(NotificationCreator):
    """Creates a NEW_ARRIVAL in-app notification."""

    def create_notification(self, notification_id: str,
                            user: User) -> Notification:
        return Notification(
            notification_id=notification_id,
            user=user,
            notification_type=NotificationType.NEW_ARRIVAL,
            channel="IN_APP"
        )


# ── Factory Method Registry ───────────────────────────────────────────────────

NOTIFICATION_CREATORS = {
    "DUE_SOON": DueSoonNotificationCreator,
    "OVERDUE": OverdueNotificationCreator,
    "RESERVATION_CONFIRMED": ReservationConfirmedCreator,
    "NEW_ARRIVAL": NewArrivalNotificationCreator,
}


def get_notification_creator(event_type: str) -> NotificationCreator:
    """Returns the correct creator for a given event type."""
    creator_class = NOTIFICATION_CREATORS.get(event_type.upper())
    if not creator_class:
        raise ValueError(f"No creator for event type: '{event_type}'")
    return creator_class()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from src.models import Student

    student = Student("u001", "Alice", "alice@uni.ac.za",
                      "Pass@123", "211001")

    for event in ["DUE_SOON", "OVERDUE", "RESERVATION_CONFIRMED", "NEW_ARRIVAL"]:
        creator = get_notification_creator(event)
        notification = creator.create_notification(f"notif_{event}", student)
        print(f"Created: {notification.status} | "
              f"Type: {notification._type} | "
              f"Channel: {notification._channel}")
