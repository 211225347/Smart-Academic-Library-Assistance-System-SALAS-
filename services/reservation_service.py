# services/reservation_service.py
import uuid
from datetime import date
from typing import List, Optional
from src.models import Reservation, ReservationStatus

# Custom exceptions matching the project's architecture style
class ReservationError(Exception):
    pass

class ReservationLimitExceededError(ReservationError):
    pass

class ResourceStillAvailableError(ReservationError):
    pass

class ReservationService:
    def __init__(self, reservation_repo, user_repo, resource_repo):
        self.reservation_repo = reservation_repo
        self.user_repo = user_repo
        self.resource_repo = resource_repo

    def create_reservation(self, user_id: str, resource_id: str) -> Reservation:
        """
        Creates a reservation following library business rules.
        """
        # 1. Verify existence of User and Resource
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found.")

        resource = self.resource_repo.find_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource '{resource_id}' not found.")

        # 2. BR Rule: Prevent reservation if copies are currently sitting available on shelves
        if resource.available_copies > 0:
            raise ResourceStillAvailableError(
                f"Resource '{resource_id}' has available copies on the shelf. Please check out instead."
            )

        # 3. BR Rule: Max active reservations limit per student (e.g., max 3 active reservations)
        active_reservations = self.reservation_repo.find_by_student(user_id)
        pending_or_queued = [
            r for r in active_reservations 
            if r.status in {ReservationStatus.PENDING, ReservationStatus.QUEUED}
        ]
        if len(pending_or_queued) >= 3:
            raise ReservationLimitExceededError("Student has reached the maximum limit of 3 active reservations.")

        # 4. Process the reservation queue mapping logic
        existing_active = self.reservation_repo.find_active_by_resource(resource_id)
        
        res_id = f"res-{uuid.uuid4().hex[:6]}"
        reservation = Reservation(
            reservation_id=res_id,
            student=user,
            resource=resource,
            reservation_date=date.today()
        )

        # If others are already waiting for this item, set status to QUEUED and track position
        if len(existing_active) > 0:
            reservation.status = ReservationStatus.QUEUED
            reservation._queue_position = len(existing_active) + 1
        else:
            reservation.status = ReservationStatus.PENDING

        # 5. Save and return
        self.reservation_repo.save(reservation)
        return reservation

    def get_all_reservations(self) -> List[Reservation]:
        return self.reservation_repo.find_all()

    def get_student_reservations(self, student_id: str) -> List[Reservation]:
        return self.reservation_repo.find_by_student(student_id)