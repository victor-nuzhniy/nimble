"""Module for testing api.queries."""
from typing import Dict

from faker import Faker

from api.queries import (
    get_create_single_contact_query,
    get_delete_contacts_query,
    get_delete_single_contact_query,
    get_insert_contact_query,
    get_insert_with_update_contacts_query,
    get_read_single_contact_query,
    get_search_contacts_query,
    get_select_contacts_query,
    get_update_single_contact_query,
)


class TestGetSelectContactsQuery:
    """Class for testing get_select_contacts_query."""

    def test_get_select_contacts_query(self) -> None:
        """Test get_select_contacts_query."""
        result: str = get_select_contacts_query()
        assert result == "SELECT * FROM contacts"


class TestGetSearchContactsQuery:
    """Class for testing get_search_contacts_query."""

    def test_get_search_contacts_query(self, faker: Faker) -> None:
        """Test get_search_contacts_query."""
        search_data: str = faker.pystr(min_chars=1, max_chars=40)
        result: str = get_search_contacts_query(search_data)
        assert result == (
            f"SELECT * FROM contacts WHERE make_tsvector(first_name, last_name,"
            f" email) @@ websearch_to_tsquery('english', '{search_data}');"
        )


class TestGetInsertContactQuery:
    """Class for testing get_insert_contact_query."""

    def test_get_insert_contact_query(self, faker: Faker) -> None:
        """Test get_insert_contact_query."""
        contact: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
        result: str = get_insert_contact_query(contact)
        assert result == (
            f"INSERT INTO contacts(first_name, last_name, email) VALUES "
            f"('{contact.get('first name')}', '{contact.get('last name')}', "
            f"'{contact.get('Email')}');"
        )


class TestGetDeleteContactsQuery:
    """Class for testing get_delete_contacts_query."""

    def test_get_delete_contacts_query(self) -> None:
        """Test get_delete_contacts_query."""
        result: str = get_delete_contacts_query()
        assert result == "DELETE FROM contacts;"


class TestGetReadSingleContactQuery:
    """Class for testing get_read_single_contact_query."""

    def test_get_read_single_contact_query(self, faker: Faker) -> None:
        """Test get_read_single_contact_query."""
        pk: int = faker.random_int(min=1)
        result: str = get_read_single_contact_query(pk)
        assert result == f"SELECT * FROM contacts WHERE contact_id = {pk};"


class TestGetCreateSingleContactQuery:
    """Class for testing get_create_single_contact_query."""

    def test_get_create_single_contact_query(self, faker: Faker) -> None:
        """Test get_create_single_contact_query."""
        first_name: str = faker.first_name()
        last_name: str = faker.last_name()
        email: str = faker.email()
        result: str = get_create_single_contact_query(first_name, last_name, email)
        assert result == (
            f"INSERT INTO contacts(first_name, last_name, email) VALUES"
            f"('{first_name}', '{last_name}', '{email}');"
        )


class TestGetUpdateSingleContactQuery:
    """Class for testing get_update_single_contact_query."""

    def test_get_update_single_contact_query(self, faker: Faker) -> None:
        """Test get_update_single_contact_query."""
        pk: int = faker.random_int(min=1)
        first_name: str = faker.first_name()
        last_name: str = faker.last_name()
        email: str = faker.email()
        result: str = get_update_single_contact_query(pk, first_name, last_name, email)
        assert result == (
            f"UPDATE contacts "
            f"SET first_name = '{first_name}', last_name = '{last_name}', "
            f"email = '{email}' WHERE contact_id = {pk};"
        )


class TestGetDeleteSingleContactQuery:
    """Class for testing get_delete_single_contact_query."""

    def test_get_delete_single_contact_query(self, faker: Faker) -> None:
        """Test get_delete_single_contact_query."""
        pk: int = faker.random_int(min=1)
        result: str = get_delete_single_contact_query(pk)
        assert result == f"DELETE FROM contacts WHERE contact_id = {pk};"


class TestGetInsertWithUpdateContactsQuery:
    """Class for testing get_insert_with_update_contacts_query."""

    def test_get_insert_with_update_contacts_query(self, faker: Faker) -> None:
        """Test get_insert_with_update_contacts_query."""
        contact: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
        result: str = get_insert_with_update_contacts_query(contact)
        assert result == (
            f"INSERT INTO contacts (first_name, last_name, email) "
            f"VALUES ('{contact.get('first_name', '')}', "
            f"'{contact.get('last_name', '')}', "
            f"'{contact.get('email', '')}') "
            f"ON CONFLICT (first_name, last_name) "
            f"DO UPDATE SET email = '{contact.get('email', '')}';"
        )
