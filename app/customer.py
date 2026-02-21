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

    customer_id = data.get("customer_id")
    name = data.get("name")
    email = data.get("email")

    checks = [
        isinstance(customer_id, str) and customer_id.strip(),
        isinstance(name, str) and name.strip(),
        isinstance(email, str) and "@" in email,
    ]
    return all(checks)
