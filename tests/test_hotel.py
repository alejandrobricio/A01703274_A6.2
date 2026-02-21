"""Unit tests for hotel CRUD operations and validation."""

import tempfile
import unittest
from pathlib import Path

from app.hotel import Hotel
from app.system import ReservationSystem


class TestHotel(unittest.TestCase):
    """Tests for Hotel behaviors in ReservationSystem."""

    def setUp(self):
        """Create a temporary ReservationSystem for each test."""
        # pylint: disable=consider-using-with
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.system = ReservationSystem(Path(self.tmp_dir.name))

    def test_create_and_get_hotel(self):
        """Create a hotel and verify it can be retrieved."""
        hotel = Hotel("H1", "Hotel One", "QRO", 10, 10)
        self.system.create_hotel(hotel)

        got = self.system.get_hotel("H1")
        self.assertIsNotNone(got)
        self.assertEqual("Hotel One", got.name)

    def test_modify_hotel(self):
        """Modify a hotel and verify the update is stored."""
        hotel = Hotel("H1", "Hotel One", "QRO", 10, 10)
        self.system.create_hotel(hotel)

        modified = Hotel("H1", "Hotel One Updated", "QRO", 10, 8)
        self.system.modify_hotel(modified)

        got = self.system.get_hotel("H1")
        self.assertEqual("Hotel One Updated", got.name)
        self.assertEqual(8, got.available_rooms)

    def test_delete_hotel(self):
        """Delete a hotel and verify it no longer exists."""
        hotel = Hotel("H1", "Hotel One", "QRO", 10, 10)
        self.system.create_hotel(hotel)

        deleted = self.system.delete_hotel("H1")
        self.assertTrue(deleted)
        self.assertIsNone(self.system.get_hotel("H1"))

    def test_create_hotel_invalid_rooms_raises(self):
        """Creating a hotel with invalid rooms should raise ValueError."""
        hotel = Hotel("H2", "Bad Hotel", "QRO", 0, 0)
        with self.assertRaises(ValueError):
            self.system.create_hotel(hotel)
