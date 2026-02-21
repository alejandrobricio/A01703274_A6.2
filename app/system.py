"""
system.py

Reservation System service layer:
- CRUD for Hotels and Customers
- Create/cancel Reservations
- File-based persistence via JsonStore
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from app.customer import Customer, validate_customer_dict
from app.hotel import Hotel, validate_hotel_dict
from app.reservation import (
    Reservation,
    STATUS_ACTIVE,
    STATUS_CANCELLED,
    validate_reservation_dict,
)
from app.storage import JsonStore


class ReservationSystem:
    """Main application service that coordinates storage and rules."""

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._hotels_store = JsonStore(data_dir / "hotels.json")
        self._customers_store = JsonStore(data_dir / "customers.json")
        self._reservations_store = JsonStore(data_dir / "reservations.json")

    # ---------- Hotels ----------
    def create_hotel(self, hotel: Hotel) -> None:
        if not validate_hotel_dict(hotel.__dict__):
            raise ValueError("Invalid hotel data")
        self._hotels_store.upsert_record(
            hotel,
            key_field="hotel_id",
            validator=validate_hotel_dict,
        )

    def delete_hotel(self, hotel_id: str) -> bool:
        return self._hotels_store.delete_record(
            hotel_id,
            key_field="hotel_id",
            validator=validate_hotel_dict,
        )

    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        hotels = self.list_hotels()
        for h in hotels:
            if h.hotel_id == hotel_id:
                return h
        return None

    def list_hotels(self) -> List[Hotel]:
        records = self._hotels_store.load_records(validator=validate_hotel_dict)
        return [Hotel(**r) for r in records]

    def modify_hotel(self, hotel: Hotel) -> None:
        # Same as create because upsert
        self.create_hotel(hotel)

    # ---------- Customers ----------
    def create_customer(self, customer: Customer) -> None:
        if not validate_customer_dict(customer.__dict__):
            raise ValueError("Invalid customer data")
        self._customers_store.upsert_record(
            customer,
            key_field="customer_id",
            validator=validate_customer_dict,
        )

    def delete_customer(self, customer_id: str) -> bool:
        return self._customers_store.delete_record(
            customer_id,
            key_field="customer_id",
            validator=validate_customer_dict,
        )

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        customers = self.list_customers()
        for c in customers:
            if c.customer_id == customer_id:
                return c
        return None

    def list_customers(self) -> List[Customer]:
        records = self._customers_store.load_records(validator=validate_customer_dict)
        return [Customer(**r) for r in records]

    def modify_customer(self, customer: Customer) -> None:
        self.create_customer(customer)

    # ---------- Reservations ----------
    def create_reservation(self, reservation: Reservation) -> None:
        """
        Creates a reservation if:
        - hotel exists
        - customer exists
        - hotel has available rooms
        """
        if not validate_reservation_dict(reservation.__dict__):
            raise ValueError("Invalid reservation data")

        hotel = self.get_hotel(reservation.hotel_id)
        if hotel is None:
            raise ValueError("Hotel does not exist")

        customer = self.get_customer(reservation.customer_id)
        if customer is None:
            raise ValueError("Customer does not exist")

        if hotel.available_rooms <= 0:
            raise ValueError("No rooms available")

        # Save reservation
        self._reservations_store.upsert_record(
            reservation,
            key_field="reservation_id",
            validator=validate_reservation_dict,
        )

        # Decrease available rooms
        updated_hotel = Hotel(
            hotel_id=hotel.hotel_id,
            name=hotel.name,
            city=hotel.city,
            total_rooms=hotel.total_rooms,
            available_rooms=hotel.available_rooms - 1,
        )
        self.modify_hotel(updated_hotel)

    def cancel_reservation(self, reservation_id: str) -> None:
        reservation = self.get_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation does not exist")

        if reservation.status == STATUS_CANCELLED:
            # idempotent cancel: do nothing
            return

        # Mark reservation cancelled
        cancelled = Reservation(
            reservation_id=reservation.reservation_id,
            hotel_id=reservation.hotel_id,
            customer_id=reservation.customer_id,
            status=STATUS_CANCELLED,
        )
        self._reservations_store.upsert_record(
            cancelled,
            key_field="reservation_id",
            validator=validate_reservation_dict,
        )

        # Increase hotel's available rooms back
        hotel = self.get_hotel(reservation.hotel_id)
        if hotel is None:
            # If hotel missing, still keep reservation cancelled
            return

        updated_hotel = Hotel(
            hotel_id=hotel.hotel_id,
            name=hotel.name,
            city=hotel.city,
            total_rooms=hotel.total_rooms,
            available_rooms=min(hotel.total_rooms, hotel.available_rooms + 1),
        )
        self.modify_hotel(updated_hotel)

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        reservations = self.list_reservations()
        for r in reservations:
            if r.reservation_id == reservation_id:
                return r
        return None

    def list_reservations(self) -> List[Reservation]:
        records = self._reservations_store.load_records(
            validator=validate_reservation_dict
        )
        return [Reservation(**r) for r in records]

    # ---------- Convenience Display ----------
    def display_state(self) -> Dict[str, int]:
        """Small helper so you can show system content if needed."""
        return {
            "hotels": len(self.list_hotels()),
            "customers": len(self.list_customers()),
            "reservations": len(self.list_reservations()),
        }