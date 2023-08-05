"""Validators for 'api' app."""
from typing import Dict


def validate_contact(contact: Dict) -> bool:
    """Validate contact from csv."""
    if (
        not contact.get("first name")
        or not contact.get("last name")
        or any(
            [
                len(contact.get("first name")) > 100,
                len(contact.get("last name")) > 100,
            ]
        )
    ):
        return False
    return True


def validate_contact_input(contact: Dict) -> bool:
    """Validate contact from api input."""
    if (
        not contact.get("first_name")
        or not contact.get("last_name")
        or any(
            [
                len(contact.get("first_name")) > 100,
                len(contact.get("last_name")) > 100,
            ]
        )
    ):
        return False
    return True
