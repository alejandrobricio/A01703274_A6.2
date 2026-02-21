# pylint: disable=consider-using-with
"""Unit tests for customer CRUD operations and validation."""

import tempfile
import unittest
from pathlib import Path

from app.customer import Customer
from app.system import ReservationSystem


class TestCustomer(unittest.TestCase):
    """Tests for Customer behaviors in ReservationSystem."""

    # pylint: disable=consider-using-with
    def setUp(self):
        """Create a temporary ReservationSystem for each test."""
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.system = ReservationSystem(Path(self.tmp_dir.name))

    def test_create_and_get_customer(self):
        """Create a customer and verify it can be retrieved."""
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        got = self.system.get_customer("C1")
        self.assertIsNotNone(got)
        self.assertEqual("Ale", got.name)

    def test_modify_customer(self):
        """Modify a customer and verify the update is stored."""
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        modified = Customer("C1", "Ale Updated", "ale@test.com")
        self.system.modify_customer(modified)

        got = self.system.get_customer("C1")
        self.assertEqual("Ale Updated", got.name)

    def test_delete_customer(self):
        """Delete a customer and verify it no longer exists."""
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        deleted = self.system.delete_customer("C1")
        self.assertTrue(deleted)
        self.assertIsNone(self.system.get_customer("C1"))

    def test_create_customer_invalid_email_raises(self):
        """Creating a customer with invalid email should raise ValueError."""
        customer = Customer("C2", "Bad", "bad-email")
        with self.assertRaises(ValueError):
            self.system.create_customer(customer)
