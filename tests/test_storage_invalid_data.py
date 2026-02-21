"""Unit tests for JsonStore invalid data handling."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from app.hotel import validate_hotel_dict
from app.storage import JsonStore


class TestStorageInvalidData(unittest.TestCase):
    """Tests for robust loading when JSON or records are invalid."""

    def setUp(self):
        """Create a temporary data directory for each test."""
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.data_dir = Path(self.tmp_dir.name)

    def test_invalid_json_does_not_crash_and_returns_default(self):
        """Invalid JSON should be reported and return the default value."""
        file_path = self.data_dir / "hotels.json"
        file_path.write_text("{not valid json", encoding="utf-8")

        store = JsonStore(file_path)

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            records = store.load_records(
                validator=validate_hotel_dict,
                default=[],
            )

        self.assertEqual([], records)
        self.assertIn("Invalid JSON", buffer.getvalue())

    def test_invalid_record_is_skipped_and_execution_continues(self):
        """Invalid records should be skipped while valid ones are loaded."""
        file_path = self.data_dir / "hotels.json"

        file_path.write_text(
            "\n".join(
                [
                    "[",
                    '  {"hotel_id": "H1", "name": "X", "city": "QRO", '
                    '"total_rooms": 0, "available_rooms": 0},',
                    '  {"hotel_id": "H2", "name": "Ok", "city": "QRO", '
                    '"total_rooms": 2, "available_rooms": 2}',
                    "]",
                ]
            ),
            encoding="utf-8",
        )

        store = JsonStore(file_path)

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            records = store.load_records(
                validator=validate_hotel_dict,
                default=[],
            )

        self.assertEqual(1, len(records))
        self.assertEqual("H2", records[0]["hotel_id"])
        self.assertIn("Invalid record fields", buffer.getvalue())
