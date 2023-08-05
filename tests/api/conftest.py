"""Fixtures for testing 'api' app."""
from typing import Dict, List

from faker import Faker


def create_fake_contacts_list(faker: Faker) -> List[Dict]:
    """Create fake contacts dict list."""
    contacts: List = []
    for _ in range(faker.random_int(min=4, max=40)):
        contacts.append(
            {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
            }
        )
    return contacts
