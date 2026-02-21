"""
hotel.py

Hotel entity and validation helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Hotel:
    """Represents a hotel in the reservation system."""

    hotel_id: str
    name: str
    city: str
    total_rooms: int
    available_rooms: int


def validate_hotel_dict(data: Dict[str, Any]) -> bool:
    """Validate that a dict contains a valid Hotel structure."""
    required = {
        "hotel_id",
        "name",
        "city",
        "total_rooms",
        "available_rooms",
    }

    if not required.issubset(data.keys()):
        return False

    hotel_id = data.get("hotel_id")
    name = data.get("name")
    city = data.get("city")
    total_rooms = data.get("total_rooms")
    available_rooms = data.get("available_rooms")

    checks = [
        isinstance(hotel_id, str) and hotel_id.strip(),
        isinstance(name, str) and name.strip(),
        isinstance(city, str) and city.strip(),
        isinstance(total_rooms, int) and total_rooms > 0,
        isinstance(available_rooms, int),
        isinstance(total_rooms, int)
        and isinstance(available_rooms, int)
        and 0 <= available_rooms <= total_rooms,
    ]

    return all(checks)
