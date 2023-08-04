"""Utility functional for 'api' app."""
from typing import Dict, List

import requests
from django.db import connection

from api.queries import get_insert_with_update_contacts_query


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.

    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def create_contact_list(resources: Dict) -> List:
    """Create dict list with contact data."""
    contacts: List = []
    for resource in resources:
        contact_dict: Dict = dict()
        fields_dict: Dict = resource.get("fields")
        if first_name_list := fields_dict.get("first name"):
            contact_dict["first_name"] = first_name_list[0].get("value")
        if last_name_list := fields_dict.get("last name"):
            contact_dict["last_name"] = last_name_list[0].get("value")
        if email_list := fields_dict.get("email"):
            contact_dict["email"] = email_list[0].get("value")
        if contact_dict:
            contacts.append(contact_dict)
    return contacts


def get_nimble_api_data() -> List:
    """Get Nimble api data for updating."""
    url: str = "https://api.nimble.com/api/v1/contacts"
    headers: Dict = {"Authorization": "Bearer NxkA2RlXS3NiR8SKwRdDmroA992jgu"}
    fields: str = "first name,last name,email"
    contacts: List = []
    page: int = 1
    pages: int = 2
    while page <= pages:
        response = requests.get(
            url=url, headers=headers, params={"fields": fields, "page": page}
        )
        resources = response.json().get("resources")
        pages = response.json().get("meta", dict()).get("pages", 0)
        page += 1
        contacts += create_contact_list(resources)
    return contacts


def update_contacts_data(contacts: List) -> None:
    """Update contacts table data with given dict."""
    with connection.cursor() as cursor:
        for contact in contacts:
            query: str = get_insert_with_update_contacts_query(contact)
            cursor.execute(query)
