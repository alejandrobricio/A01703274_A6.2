"""
customer.py

Customer entity and validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Customer:
    """Represents a customer in the reservation system."""

    customer_id: str
    name: str
    email: str


def validate_customer_dict(data: Dict[str, Any]) -> bool:
    """Validate that a dict contains a valid Customer structure."""
    required = {"customer_id", "name", "email"}
    if not required.issubset(data.keys()):
        return False

    if not isinstance(data["customer_id"], str):
        return False
    if not data["customer_id"].strip():
        return False

    if not isinstance(data["name"], str):
        return False
    if not data["name"].strip():
        return False

    if not isinstance(data["email"], str):
        return False
    if "@" not in data["email"]:
        return False

    return True
