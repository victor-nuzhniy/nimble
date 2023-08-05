"""Fixtures for testing 'api' app."""
from typing import Dict, List, Tuple

import pytest
from faker import Faker

from api.utils import get_nimble_api_data


@pytest.fixture(scope="function")
def create_fake_contacts_list(faker: Faker) -> List[Dict]:
    """Create fake contacts dict list."""
    contacts: List = []
    for _ in range(faker.random_int(min=4, max=10)):
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


@pytest.fixture
def create_fake_contacts_lists_with_diff_keys(faker: Faker) -> Tuple[List, List]:
    """Create dicts lists with different keys and same values."""
    input_list: List = []
    output_list: List = []
    for _ in range(faker.random_int(min=3, max=10)):
        first_name: str = faker.first_name()
        last_name: str = faker.last_name()
        email: str = faker.email()
        output_list.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            }
        )
        resource: Dict = dict()
        fields: Dict = dict()
        fields["first name"] = [{"value": first_name}]
        fields["last name"] = [{"value": last_name}]
        fields["email"] = [{"value": email}]
        resource["fields"] = fields
        input_list.append(resource)
    return input_list, output_list
