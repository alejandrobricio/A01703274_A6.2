"""
customer.py

Customer entity and validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    email: str


def validate_customer_dict(data: Dict[str, Any]) -> bool:
    required = {"customer_id", "name", "email"}
    if not required.issubset(data.keys()):
        return False

    if not isinstance(data["customer_id"], str) or not data["customer_id"].strip():
        return False
    if not isinstance(data["name"], str) or not data["name"].strip():
        return False
    if not isinstance(data["email"], str) or "@" not in data["email"]:
        return False

    return True