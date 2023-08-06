"""Pytest fixtures for 'API' project."""

import random
from typing import Dict, List

import pytest
from django.db import connection
from faker import Faker


@pytest.fixture(scope="function", autouse=True)
def faker_seed() -> None:
    """Generate random seed for Faker instance."""
    return random.seed(version=3)


@pytest.fixture
def fill_contacts_table_with_data(faker: Faker) -> List[Dict]:
    """Fill test db with fake data."""
    result: List = []
    with connection.cursor() as cursor:
        for _ in range(30):
            first_name: str = faker.first_name()
            last_name: str = faker.pystr(min_chars=10, max_chars=100)
            email: str = faker.email()
            query = (
                f"INSERT INTO contacts (first_name, last_name, email) "
                f"VALUES ('{first_name}', "
                f"'{last_name}', "
                f"'{email}');"
            )
            cursor.execute(query)
            result.append(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                }
            )
    return result
