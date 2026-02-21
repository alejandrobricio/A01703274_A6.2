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
    STATUS_CANCELLED,
    validate_reservation_dict,
)
from app.storage import JsonStore


class ReservationSystem:
    """Service layer coordinating persistence and business rules."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize stores using the given data directory."""
        self._data_dir = data_dir
        self._hotels_store = JsonStore(data_dir / "hotels.json")
        self._customers_store = JsonStore(data_dir / "customers.json")
        self._reservations_store = JsonStore(data_dir / "reservations.json")

    # ---------- Hotels ----------
    def create_hotel(self, hotel: Hotel) -> None:
        """Create or update a hotel record."""
        if not validate_hotel_dict(hotel.__dict__):
            raise ValueError("Invalid hotel data")

        self._hotels_store.upsert_record(
            hotel,
            key_field="hotel_id",
            validator=validate_hotel_dict,
        )

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel by id. Returns True if a record was deleted."""
        return self._hotels_store.delete_record(
            hotel_id,
            key_field="hotel_id",
            validator=validate_hotel_dict,
        )

    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        """Return a hotel by id, or None if not found."""
        for hotel in self.list_hotels():
            if hotel.hotel_id == hotel_id:
                return hotel
        return None

    def list_hotels(self) -> List[Hotel]:
        """Return a list of all hotels stored."""
        records = self._hotels_store.load_records(
            validator=validate_hotel_dict
        )
        return [Hotel(**record) for record in records]

    def modify_hotel(self, hotel: Hotel) -> None:
        """Modify a hotel record (implemented as an upsert)."""
        self.create_hotel(hotel)

    # ---------- Customers ----------
    def create_customer(self, customer: Customer) -> None:
        """Create or update a customer record."""
        if not validate_customer_dict(customer.__dict__):
            raise ValueError("Invalid customer data")

        self._customers_store.upsert_record(
            customer,
            key_field="customer_id",
            validator=validate_customer_dict,
        )

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer by id. Returns True if a record was deleted."""
        return self._customers_store.delete_record(
            customer_id,
            key_field="customer_id",
            validator=validate_customer_dict,
        )

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Return a customer by id, or None if not found."""
        for customer in self.list_customers():
            if customer.customer_id == customer_id:
                return customer
        return None

    def list_customers(self) -> List[Customer]:
        """Return a list of all customers stored."""
        records = self._customers_store.load_records(
            validator=validate_customer_dict
        )
        return [Customer(**record) for record in records]

    def modify_customer(self, customer: Customer) -> None:
        """Modify a customer record (implemented as an upsert)."""
        self.create_customer(customer)

    # ---------- Reservations ----------
    def create_reservation(self, reservation: Reservation) -> None:
        """
        Create a reservation if:
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

        self._reservations_store.upsert_record(
            reservation,
            key_field="reservation_id",
            validator=validate_reservation_dict,
        )

        updated_hotel = Hotel(
            hotel_id=hotel.hotel_id,
            name=hotel.name,
            city=hotel.city,
            total_rooms=hotel.total_rooms,
            available_rooms=hotel.available_rooms - 1,
        )
        self.modify_hotel(updated_hotel)

    def cancel_reservation(self, reservation_id: str) -> None:
        """Cancel a reservation by id. Raises ValueError if not found."""
        reservation = self.get_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation does not exist")

        if reservation.status == STATUS_CANCELLED:
            return

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

        hotel = self.get_hotel(reservation.hotel_id)
        if hotel is None:
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
        """Return a reservation by id, or None if not found."""
        for reservation in self.list_reservations():
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def list_reservations(self) -> List[Reservation]:
        """Return a list of all reservations stored."""
        records = self._reservations_store.load_records(
            validator=validate_reservation_dict,
        )
        return [Reservation(**record) for record in records]

    # ---------- Convenience Display ----------
    def display_state(self) -> Dict[str, int]:
        """Return counts of stored hotels, customers, and reservations."""
        return {
            "hotels": len(self.list_hotels()),
            "customers": len(self.list_customers()),
            "reservations": len(self.list_reservations()),
        }
