"""Module for SQL queries for 'api' app."""
from typing import Dict


def get_select_contacts_query():
    """Get query for retrievnig all contacts."""
    return "SELECT * FROM contacts"


def get_insert_contact_query(contact: Dict) -> str:
    """Get query string with SQL statement for creating contact."""
    return (
        f"INSERT INTO contacts(first_name, last_name, email) VALUES "
        f"('{contact.get('first name')}', '{contact.get('last name')}', "
        f"'{contact.get('Email')}');"
    )


def get_delete_contacts_query() -> str:
    """Get query string with SQL statement for deleting contacts."""
    return "DELETE FROM contacts;"


def get_read_single_contact_query(pk: int) -> str:
    """Get read query to retrieve single contact."""
    return f"SELECT * FROM contacts WHERE contact_id = {pk};"


def get_create_single_contact_query(first_name: str, last_name: str, email: str) -> str:
    """Get create query to create single contact."""
    return (
        f"INSERT INTO contacts(first_name, last_name, email) VALUES"
        f"('{first_name}', '{last_name}', '{email}');"
    )


def get_update_single_contact_query(
    pk: int, first_name: str, last_name: str, email: str
) -> str:
    """Get update query to update single contact."""
    return (
        f"UPDATE contacts "
        f"SET first_name = '{first_name}', last_name = '{last_name}', "
        f"email = '{email}' WHERE contact_id = {pk};"
    )


def get_delete_single_contact_query(pk: int) -> str:
    """Get delete query to delete single contact."""
    return f"DELETE FROM contacts WHERE contact_id = {pk};"
