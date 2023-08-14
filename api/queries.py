"""Module for SQL queries for 'api' app."""
from typing import Dict, Tuple


def get_select_contacts_query() -> Tuple[str, Tuple]:
    """Get query for retrievnig all contacts."""
    return "SELECT * FROM contacts ORDER BY contact_id ASC;", tuple()


def get_search_contacts_query(search_data: str) -> Tuple[str, Tuple]:
    """Get query for searching contacts with full text search."""
    return (
        "SELECT * FROM contacts WHERE make_tsvector(first_name, last_name,"
        " email) @@ websearch_to_tsquery('english', %s);",
        (search_data,),
    )


def get_insert_contact_query(contact: Dict) -> Tuple[str, Tuple]:
    """Get query string with SQL statement for creating contact."""
    return (
        "INSERT INTO contacts(first_name, last_name, email) VALUES (%s, %s, %s);",
        (contact.get("first name"), contact.get("last name"), contact.get("Email")),
    )


def get_delete_contacts_query() -> Tuple[str, Tuple]:
    """Get query string with SQL statement for deleting contacts."""
    return "DELETE FROM contacts;", tuple()


def get_read_single_contact_query(pk: int) -> Tuple[str, Tuple]:
    """Get read query to retrieve single contact."""
    return "SELECT * FROM contacts WHERE contact_id = %s;", (pk,)


def get_create_single_contact_query(
    first_name: str, last_name: str, email: str
) -> Tuple[str, Tuple]:
    """Get create query to create single contact."""
    return (
        "INSERT INTO contacts(first_name, last_name, email) VALUES (%s, %s, %s);",
        (first_name, last_name, email),
    )


def get_update_single_contact_query(
    pk: int, first_name: str, last_name: str, email: str
) -> Tuple[str, Tuple]:
    """Get update query to update single contact."""
    return (
        "UPDATE contacts "
        "SET first_name = %s, last_name = %s, email = %s WHERE contact_id = %s;",
        (first_name, last_name, email, pk),
    )


def get_delete_single_contact_query(pk: int) -> Tuple[str, Tuple]:
    """Get delete query to delete single contact."""
    return "DELETE FROM contacts WHERE contact_id = %s;", (pk,)


def get_insert_with_update_contacts_query(contact: Dict) -> Tuple[str, Tuple]:
    """Get insert query with on-conflict option with do update."""
    return (
        "INSERT INTO contacts (first_name, last_name, email) "
        "VALUES (%s, %s, %s) ON CONFLICT (first_name, last_name) "
        "DO UPDATE SET email = %s;",
        (
            contact.get("first_name", ""),
            contact.get("last_name", ""),
            contact.get("email", ""),
            contact.get("email", ""),
        ),
    )
