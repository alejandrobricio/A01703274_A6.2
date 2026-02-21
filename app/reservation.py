"""
reservation.py

Reservation entity and validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


STATUS_ACTIVE = "ACTIVE"
STATUS_CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class Reservation:
    reservation_id: str
    hotel_id: str
    customer_id: str
    status: str = STATUS_ACTIVE


def validate_reservation_dict(data: Dict[str, Any]) -> bool:
    required = {"reservation_id", "hotel_id", "customer_id", "status"}
    if not required.issubset(data.keys()):
        return False

    for key in ("reservation_id", "hotel_id", "customer_id"):
        if not isinstance(data[key], str) or not data[key].strip():
            return False

    if data["status"] not in {STATUS_ACTIVE, STATUS_CANCELLED}:
        return False

    return True
