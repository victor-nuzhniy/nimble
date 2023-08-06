"""Module for testing api utils."""
from typing import Dict, List, Tuple

import pytest
from django.db import connection
from django.test import Client
from django.urls import reverse

from api.queries import get_select_contacts_query
from api.utils import create_contact_list, dictfetchall, update_contacts_data


@pytest.mark.django_db
class TestDictfetchall:
    """Class for testing dictfetchall."""

    pytestmark = pytest.mark.django_db

    def test_dictfetchall(
        self,
        fill_contacts_table_with_data: None,
        client: Client,
    ) -> None:
        """Test dictfetchall."""
        url: str = reverse("get_contacts")
        response = client.get(url)
        response: List = response.json().get("contacts")
        with connection.cursor() as cursor:
            cursor.execute(get_select_contacts_query())
            result: List = dictfetchall(cursor)
        for i, contact in enumerate(response):
            for key, value in result[i].items():
                assert contact[key] == value


class TestCreateContactList:
    """Class for testing create_contact_list."""

    def test_create_contact_list(
        self,
        create_fake_contacts_lists_with_diff_keys: Tuple[List, List],
    ) -> None:
        """Test create_contact_list."""
        input_list, output_list = create_fake_contacts_lists_with_diff_keys
        result: List = create_contact_list(input_list)
        for i, contact in enumerate(output_list):
            for key, value in result[i].items():
                assert contact[key] == value

    def test_create_contact_list_empty(
        self,
    ) -> None:
        """Test create_contact_list with broken input."""
        input_list: List = [
            {
                "fields": {
                    "email": dict(),
                    "first name": None,
                    "last name": "abc",
                }
            }
        ]
        result: List = create_contact_list(input_list)
        assert not result
        assert isinstance(result, List)

    def test_create_contact_list_without_values(self) -> None:
        """Test create_contact_list with empty input values."""
        input_list: List = [
            {
                "fields": {
                    "email": [{"hello": "world"}],
                    "first name": [{"abc": "cdf"}],
                    "last name": [{"zxy": 123}],
                }
            }
        ]
        result: List = create_contact_list(input_list)
        assert result[0]["first_name"] is None
        assert result[0]["last_name"] is None
        assert result[0]["email"] is None


@pytest.mark.django_db
class TestUpdateContactsData:
    """Class for testing update_contacts_data."""

    pytestmark = pytest.mark.django_db

    def test_update_contacts_data(
        self,
        create_fake_contacts_list: List[Dict],
        fill_contacts_table_with_data: List[Dict],
        client: Client,
    ) -> None:
        """Test update_contacts_data."""
        contacts: List[Dict] = create_fake_contacts_list
        update_contacts_data(contacts)
        url: str = reverse("get_contacts")
        response = client.get(url)
        result: List = response.json().get("contacts")
        for i, contact in enumerate(result[-len(contacts) :]):
            for key, value in contacts[i].items():
                assert contact[key] == value
