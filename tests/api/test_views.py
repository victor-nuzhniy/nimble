"""Module for testing api views."""
import json
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
        token, created = Token.objects.get_or_create(user=user)
        force_authenticate(request, user, token)
        response = delete_contacts(request)
        assert response.status_code == 200
        response = client.get(reverse("get_contacts"))
        result = response.json().get("contacts")
        assert not result
        assert isinstance(result, List)


@pytest.mark.django_db
class TestContact:
    """Class for testing contact functionality."""

    pytestmark = pytest.mark.django_db

    def test_contact_get(
        self,
        fill_contacts_table_with_data: List[Dict],
        django_user_model: User,
        client: Client,
        faker: Faker,
    ) -> None:
        """Test contact get functionality."""
        contacts: List[Dict] = fill_contacts_table_with_data
        index: int = faker.random_int(min=1, max=len(contacts))
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        help_response = client.get(reverse("get_contacts"))
        result_contacts = help_response.json().get("contacts")
        first_id: int = result_contacts[0].get("contact_id")
        pk = first_id + index - 1
        url = reverse("contact", kwargs={"pk": pk})
        token, created = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token.key}"}
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        result = response.json().get("contact")
        for key, value in contacts[index - 1].items():
            assert result[key] == value

    def test_contact_delete(
        self,
        fill_contacts_table_with_data: List[Dict],
        django_user_model: User,
        client: Client,
        faker: Faker,
    ) -> None:
        """Test contact delete functionality."""
        contacts: List[Dict] = fill_contacts_table_with_data
        index: int = faker.random_int(min=1, max=len(contacts))
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        help_response = client.get(reverse("get_contacts"))
        result_contacts = help_response.json().get("contacts")
        first_id: int = result_contacts[0].get("contact_id")
        pk = first_id + index - 1
        url = reverse("contact", kwargs={"pk": pk})
        token, created = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token.key}"}
        response = client.delete(url, headers=headers)
        contacts = contacts[: index - 1] + contacts[index:]
        help_response = client.get(reverse("get_contacts"))
        result_contacts = help_response.json().get("contacts")
        assert response.status_code == 200
        result = response.json().get("result")
        assert result == "Successfully deleted contact."
        for i, contact in enumerate(contacts):
            for key, value in contact.items():
                assert result_contacts[i][key] == value


@pytest.mark.django_db
class TestUpdateContact:
    """Class for testing update_contact."""

    pytestmark = pytest.mark.django_db

    def test_update_contact(
        self,
        fill_contacts_table_with_data: List[Dict],
        django_user_model: User,
        client: Client,
        faker: Faker,
    ) -> None:
        """Test update_contact."""
        contacts: List[Dict] = fill_contacts_table_with_data
        index: int = faker.random_int(min=1, max=len(contacts))
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        new_data: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
        help_response = client.get(reverse("get_contacts"))
        result_contacts = help_response.json().get("contacts")
        first_id: int = result_contacts[0].get("contact_id")
        pk = first_id + index - 1
        url = reverse("update_contact", kwargs={"pk": pk})
        token, created = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token.key}"}
        response = client.put(
            url,
            headers=headers,
            data=json.dumps(new_data),
            content_type="application/json",
        )
        help_response = client.get(
            reverse("contact", kwargs={"pk": pk}), headers=headers
        )
        result_contact = help_response.json().get("contact")
        assert response.status_code == 200
        result = response.json().get("result")
        assert result == "Successfully updated contact."
        for key, value in contacts[index - 1].items():
            assert result_contact[key] != value
            assert result_contact[key] == new_data[key]


@pytest.mark.django_db
class TestCreateContact:
    """Class for testing create_contact."""

    pytestmark = pytest.mark.django_db

    def test_create_contact(
        self,
        fill_contacts_table_with_data: List[Dict],
        django_user_model: User,
        client: Client,
        faker: Faker,
    ) -> None:
        """Test create_contact."""
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        new_data: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
        token, created = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token.key}"}
        url = reverse("create_contact")
        response = client.post(url, headers=headers, data=new_data)
        help_response = client.get(reverse("get_contacts"))
        result_contact = help_response.json().get("contacts")[-1]
        assert response.status_code == 200
        result = response.json().get("result")
        assert result == "Contact was created."
        for key, value in new_data.items():
            assert result_contact[key] == value

    def test_create_contact_invalid_input(
        self,
        fill_contacts_table_with_data: List[Dict],
        django_user_model: User,
        client: Client,
        faker: Faker,
    ) -> None:
        """Test create_contact."""
        user = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        new_data: Dict = {
            "first_name": faker.first_name(),
            "last_name": faker.pystr(min_chars=101, max_chars=200),
            "email": faker.email(),
        }
        token, created = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token.key}"}
        url = reverse("create_contact")
        response = client.post(url, headers=headers, data=new_data)
        assert response.status_code == 406
        result = response.json().get("Error")
        assert result == "Invalid data."
