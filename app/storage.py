"""
storage.py

Simple JSON file storage with robust loading:
- If file is missing -> returns default (empty list)
- If JSON is invalid -> prints error and returns default
- If items are invalid -> skips them, prints error, continues

Designed to satisfy "invalid data must not stop execution".
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


def _safe_print(message: str) -> None:
    # Centralized print to ease testing/mocking if needed
    print(message)


class JsonStore:
    """Stores a list of dict-like records in a JSON file."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    @property
    def file_path(self) -> Path:
        return self._file_path

    def load_records(
        self,
        *,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
        default: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Loads records from JSON file.
        - Returns default ([]) on missing file or JSON decode errors.
        - If validator is provided, invalid records are skipped.
        """
        if default is None:
            default = []

        if not self._file_path.exists():
            return list(default)

        try:
            raw = self._file_path.read_text(encoding="utf-8").strip()
            if not raw:
                return list(default)
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            _safe_print(f"[ERROR] Invalid JSON in {self._file_path.name}: {exc}")
            return list(default)

        if not isinstance(data, list):
            _safe_print(
                f"[ERROR] Invalid data format in {self._file_path.name}: "
                "expected a list"
            )
            return list(default)

        records: List[Dict[str, Any]] = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                _safe_print(
                    f"[ERROR] Invalid record type at index {idx} in "
                    f"{self._file_path.name}: expected dict"
                )
                continue
            if validator is not None and not validator(item):
                _safe_print(
                    f"[ERROR] Invalid record fields at index {idx} in "
                    f"{self._file_path.name}: {item}"
                )
                continue
            records.append(item)
        return records

    def save_records(self, records: List[Dict[str, Any]]) -> None:
        """Saves list of dict records as pretty JSON."""
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)
        self._file_path.write_text(text + "\n", encoding="utf-8")

    def upsert_record(
        self,
        record: Any,
        *,
        key_field: str,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> None:
        """
        Insert or update a record by key_field.
        record can be a dataclass or dict.
        """
        payload = self._to_dict(record)
        if validator is not None and not validator(payload):
            raise ValueError("Record does not pass validation")

        records = self.load_records(validator=validator, default=[])
        updated = False

        for idx, existing in enumerate(records):
            if existing.get(key_field) == payload.get(key_field):
                records[idx] = payload
                updated = True
                break

        if not updated:
            records.append(payload)

        self.save_records(records)

    def delete_record(
        self,
        record_id: str,
        *,
        key_field: str,
        validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> bool:
        """Deletes by key. Returns True if deleted."""
        records = self.load_records(validator=validator, default=[])
        kept = [r for r in records if r.get(key_field) != record_id]
        deleted = len(kept) != len(records)
        self.save_records(kept)
        return deleted

    @staticmethod
    def _to_dict(obj: Any) -> Dict[str, Any]:
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, dict):
            return dict(obj)
        raise TypeError("Record must be a dict or a dataclass instance")