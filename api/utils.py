"""Utility functional for 'api' app."""
from typing import Dict


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.

    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def validate_contact(contact: Dict) -> bool:
    """Validate contact."""
    if any(
        [
            len(contact["first name"]) > 100,
            len(contact["last name"]) > 100,
            len(contact["Email"]) > 100,
        ]
    ):
        return False
    return True


def get_insert_contact_query(contact: Dict) -> str:
    """Get query string with SQL statement for creating contact."""
    return (
        f"INSERT INTO contacts(first_name, last_name, email) VALUES "
        f"('{contact.get('first name')}', '{contact.get('last name')}', "
        f"'{contact.get('Email')}');"
    )
