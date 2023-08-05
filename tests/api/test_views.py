"""Module for testing api views."""
from typing import List

import pytest
from django.db import connection
from django.test import Client
from django.urls import reverse
from faker import Faker


@pytest.mark.django_db
class TestSearchView:
    """Class for testing search_contacts."""

    pytestmark = pytest.mark.django_db

    def test_search_view(
        self,
        client: Client,
        fill_contacts_table_with_data: None,
        faker: Faker,
    ) -> None:
        """Test search_view."""
        contacts: List = []
        for _ in range(3):
            contacts.append(
                {
                    "first_name": faker.city(),
                    "last_name": faker.country(),
                    "email": faker.email(),
                }
            )
        with connection.cursor() as cursor:
            for contact in contacts:
                query = (
                    f"INSERT INTO contacts (first_name, last_name, email) "
                    f"VALUES ('{contact.get('first_name')}', "
                    f"'{contact.get('last_name')}', '{contact.get('email')}');"
                )
                cursor.execute(query)
        url = reverse("search_contact")
        form_data = {
            "search_data": f"{contacts[2].get('first_name')} or "
            f"{contacts[1].get('last_name')} or "
            f"{contacts[0].get('email')}"
        }
        response = client.post(url, form_data)
        assert response.status_code == 200
        result = response.json().get("contacts")
        for i, contact in enumerate(contacts):
            for key, value in contact.items():
                assert result[i][key] == value
