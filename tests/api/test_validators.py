"""Module for testing api validators."""
from typing import Dict

from faker import Faker

from api.validators import validate_contact, validate_contact_input


class TestValidateContact:
    """Class for testing validate_contact."""

    def test_validate_contact(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first name": faker.first_name(),
            "last name": faker.last_name(),
            "Email": faker.email(),
        }
        assert validate_contact(contact)

    def test_validate_contact_low(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first name": faker.first_name(),
            "last name": None,
            "Email": None,
        }
        assert not validate_contact(contact)

    def test_validate_contact_high(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first name": faker.first_name(),
            "last name": faker.pystr(min_chars=101, max_chars=400),
            "Email": faker.email(),
        }
        assert not validate_contact(contact)


class TestValidateContactInput:
    """Class for testing validate_contact_input."""

    def test_validate_contact_input(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
        assert validate_contact_input(contact)

    def test_validate_contact_input_low(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first_name": None,
            "last_name": faker.last_name(),
            "email": None,
        }
        assert not validate_contact_input(contact)

    def test_validate_contact_input_high(self, faker: Faker) -> None:
        """Test validate_contact."""
        contact: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.pystr(min_chars=101, max_chars=400),
            "email": faker.email(),
        }
        assert not validate_contact_input(contact)
