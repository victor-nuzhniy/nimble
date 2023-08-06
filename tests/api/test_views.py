"""Module for testing api views."""
from typing import Dict, List

import pytest
from django.db import connection
from django.test import Client, RequestFactory
from django.urls import reverse
from faker import Faker
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

from api.views import delete_contacts


@pytest.mark.django_db
class TestSearchView:
    """Class for testing search_contacts."""

    pytestmark = pytest.mark.django_db

    def test_search_view(
        self,
        client: Client,
        fill_contacts_table_with_data: List[Dict],
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


@pytest.mark.django_db
class TestGetContacts:
    """Class for testing get_contacts."""

    pytestmark = pytest.mark.django_db

    def test_get_contacts(
        self,
        fill_contacts_table_with_data: List[Dict],
        client: Client,
    ) -> None:
        """Test get_contacts."""
        contacts: List[Dict] = fill_contacts_table_with_data
        url = reverse("get_contacts")
        response = client.get(url)
        assert response.status_code == 200
        result = response.json().get("contacts")
        for i, contact in enumerate(contacts):
            for key, value in contact.items():
                assert result[i][key] == value


@pytest.mark.django_db
class TestDeleteContacts:
    """Class for testing delete_contacts."""

    pytestmark = pytest.mark.django_db

    def test_delete_contacts(
        self,
        fill_contacts_table_with_data: List[Dict],
        rf: RequestFactory,
        django_user_model: User,
        client: Client,
    ) -> None:
        """Test delete_contacts."""
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        url = reverse("delete_contacts")
        request = rf.delete(url)
        token = Token.objects.get_or_create(user=user)[0]
        force_authenticate(request, user, token)
        response = delete_contacts(request)
        assert response.status_code == 200
        response = client.get(reverse("get_contacts"))
        result = response.json().get("contacts")
        assert not result
        assert isinstance(result, List)
