import tempfile
import unittest
from pathlib import Path

from app.customer import Customer
from app.system import ReservationSystem


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.system = ReservationSystem(Path(self.tmp_dir.name))

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_create_and_get_customer(self):
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        got = self.system.get_customer("C1")
        self.assertIsNotNone(got)
        self.assertEqual("Ale", got.name)

    def test_modify_customer(self):
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        modified = Customer("C1", "Ale Updated", "ale@test.com")
        self.system.modify_customer(modified)

        got = self.system.get_customer("C1")
        self.assertEqual("Ale Updated", got.name)

    def test_delete_customer(self):
        customer = Customer("C1", "Ale", "ale@test.com")
        self.system.create_customer(customer)

        deleted = self.system.delete_customer("C1")
        self.assertTrue(deleted)
        self.assertIsNone(self.system.get_customer("C1"))

    # Negative case
    def test_create_customer_invalid_email_raises(self):
        customer = Customer("C2", "Bad", "bad-email")
        with self.assertRaises(ValueError):
            self.system.create_customer(customer)
