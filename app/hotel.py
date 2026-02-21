"""
hotel.py

Hotel entity and validation helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Hotel:
    hotel_id: str
    name: str
    city: str
    total_rooms: int
    available_rooms: int


def validate_hotel_dict(data: Dict[str, Any]) -> bool:
    required = {"hotel_id", "name", "city", "total_rooms", "available_rooms"}
    if not required.issubset(data.keys()):
        return False

    if not isinstance(data["hotel_id"], str) or not data["hotel_id"].strip():
        return False
    if not isinstance(data["name"], str) or not data["name"].strip():
        return False
    if not isinstance(data["city"], str) or not data["city"].strip():
        return False
    if not isinstance(data["total_rooms"], int) or data["total_rooms"] <= 0:
        return False
    if not isinstance(data["available_rooms"], int):
        return False
    if data["available_rooms"] < 0 or data["available_rooms"] > data["total_rooms"]:
        return False

    return True