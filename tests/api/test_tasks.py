"""Module for testing api.tasks."""
from typing import Dict, List

import pytest
from django.db import connection
from django.test import Client
from django.urls import reverse
from faker import Faker

from api.tasks import run_updating_contacts


@pytest.mark.django_db
class TestRunUpdatingContacts:
    """Class for testing run_updating_contacts."""

    pytestmark = pytest.mark.django_db

    def test_run_updating_contacts_inserting(
        self,
        fill_contacts_table_with_data: List[Dict],
        get_nimble_data: List[Dict],
        client: Client,
        faker: Faker,
    ) -> None:
        """Test run_updating_contacts."""
        contacts: List[Dict] = get_nimble_data
        run_updating_contacts()
        url: str = reverse("get_contacts")
        response = client.get(url)
        result: List = response.json().get("contacts")
        for i, contact in enumerate(result[-len(contacts):]):
            for key, value in contacts[i].items():
                assert contact[key] == value

    def test_run_updating_contacts_updating(
        self,
        fill_contacts_table_with_data: List[Dict],
        get_nimble_data: List[Dict],
        client: Client,
        faker: Faker,
    ) -> None:
        """Test run_updating_contacts."""
        contacts: List[Dict] = get_nimble_data
        with connection.cursor() as cursor:
            for i in range(3):
                query = (
                    f"INSERT INTO contacts (first_name, last_name, email) "
                    f"VALUES ('{contacts[i].get('first_name')}', "
                    f"'{contacts[i].get('last_name')}', 'abc');"
                )
                cursor.execute(query)
        run_updating_contacts()
        url: str = reverse("get_contacts")
        response = client.get(url)
        result: List = response.json().get("contacts")

        for i, contact in enumerate(result[3 - len(contacts):]):
            for key, value in contacts[i + 3].items():
                assert contact[key] == value
