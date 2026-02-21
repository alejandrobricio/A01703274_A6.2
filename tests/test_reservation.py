# pylint: disable=consider-using-with
"""Unit tests for reservation creation and cancellation rules."""

import tempfile
import unittest
from pathlib import Path

from app.customer import Customer
from app.hotel import Hotel
from app.reservation import Reservation, STATUS_CANCELLED
from app.system import ReservationSystem


class TestReservation(unittest.TestCase):
    """Tests for Reservation behaviors in ReservationSystem."""

    def setUp(self):
        """Create a temporary system with one hotel and one customer."""
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.system = ReservationSystem(Path(self.tmp_dir.name))

        self.system.create_hotel(Hotel("H1", "Hotel One", "QRO", 1, 1))
        self.system.create_customer(Customer("C1", "Ale", "ale@test.com"))

    def test_create_reservation_decreases_rooms(self):
        """Creating a reservation should decrease available rooms by 1."""
        self.system.create_reservation(Reservation("R1", "H1", "C1"))

        hotel = self.system.get_hotel("H1")
        self.assertEqual(0, hotel.available_rooms)

    def test_cancel_reservation_increases_rooms(self):
        """Cancelling a reservation should increase rooms and set status."""
        self.system.create_reservation(Reservation("R1", "H1", "C1"))
        self.system.cancel_reservation("R1")

        hotel = self.system.get_hotel("H1")
        self.assertEqual(1, hotel.available_rooms)

        reservation = self.system.get_reservation("R1")
        self.assertEqual(STATUS_CANCELLED, reservation.status)

    def test_reservation_with_missing_hotel_raises(self):
        """Reservation with missing hotel should raise ValueError."""
        with self.assertRaises(ValueError):
            self.system.create_reservation(
                Reservation("R2", "NO_HOTEL", "C1")
            )

    def test_reservation_with_missing_customer_raises(self):
        """Reservation with missing customer should raise ValueError."""
        with self.assertRaises(ValueError):
            self.system.create_reservation(
                Reservation("R3", "H1", "NO_CUSTOMER")
            )

    def test_reservation_when_no_rooms_available_raises(self):
        """Reservation should fail when the hotel has no available rooms."""
        self.system.create_reservation(Reservation("R1", "H1", "C1"))
        with self.assertRaises(ValueError):
            self.system.create_reservation(
                Reservation("R2", "H1", "C1")
            )

    def test_cancel_nonexistent_reservation_raises(self):
        """Cancelling a missing reservation should raise ValueError."""
        with self.assertRaises(ValueError):
            self.system.cancel_reservation("NO_RES")
