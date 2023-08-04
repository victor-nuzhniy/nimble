"""Validators for 'api' app."""
from typing import Dict


def validate_contact(contact: Dict) -> bool:
    """Validate contact from csv."""
    if any(
        [
            0 > len(contact.get("first name", "")) > 100,
            0 > len(contact.get("last name", "")) > 100,
            0 > len(contact.get("Email", "")) > 100,
        ]
    ):
        return False
    return True


def validate_contact_input(contact: Dict) -> bool:
    """Validate contact from api input."""
    if any(
        [
            0 > len(contact.get("first_name", "")) > 100,
            0 > len(contact.get("last_name", "")) > 100,
            0 > len(contact.get("email", "")) > 100,
        ]
    ):
        return False
    return True
