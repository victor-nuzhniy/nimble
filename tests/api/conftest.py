"""Fixtures for testing 'api' app."""
from typing import Dict, List

import pytest
from faker import Faker

from api.utils import get_nimble_api_data


@pytest.fixture(scope="function")
def create_fake_contacts_list(faker: Faker) -> List[Dict]:
    """Create fake contacts dict list."""
    contacts: List = []
    for _ in range(faker.random_int(min=4, max=4)):
        contacts.append(
            {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
            }
        )
    return contacts


@pytest.fixture(scope="session")
def get_nimble_data() -> List[Dict]:
    """Get Nimble api data."""
    return get_nimble_api_data()
