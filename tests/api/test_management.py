"""Module for testing management functionality 'api' app."""
import csv
from typing import Dict, List

import pytest
from django.core.management import call_command
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestImportContactFromCsv:
    """Class for testing import_contacts_from_csv functionality."""

    pytestmark = pytest.mark.django_db

    def test_import_contacts_from_csv(
        self,
        client: Client,
    ) -> None:
        """Test import_contacts_from_csv functionality."""
        call_command("import_contacts_from_csv", "data/nimble_contacts.csv")
        response = client.get(reverse("get_contacts"))
        contacts: List[Dict] = response.json().get("contacts")
        with open("data/nimble_contacts.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for i, row_dict in enumerate(reader):
                assert row_dict["first name"] == contacts[i]["first_name"]
                assert row_dict["last name"] == contacts[i]["last_name"]
                assert row_dict["Email"] == contacts[i]["email"]
