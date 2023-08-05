"""Pytest fixtures for 'API' project."""

import random

import pytest
from django.db import connection
from faker import Faker


@pytest.fixture(scope="function", autouse=True)
def faker_seed() -> None:
    """Generate random seed for Faker instance."""
    return random.seed(version=3)


@pytest.fixture
def fill_contacts_table_with_data(faker: Faker) -> None:
    """Fill test db with fake data."""
    with connection.cursor() as cursor:
        for _ in range(30):
            query = (
                f"INSERT INTO contacts (first_name, last_name, email) "
                f"VALUES ('{faker.first_name()}', "
                f"'{faker.last_name()}', "
                f"'{faker.email()}');"
            )
            cursor.execute(query)
