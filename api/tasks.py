"""Module for celery tasks for 'api' app."""
from __future__ import absolute_import, unicode_literals

from typing import Dict, List

from celery import shared_task

from api.utils import get_nimble_api_data, update_contacts_data


@shared_task
def run_updating_contacts() -> None:
    """
    Run updating contacts table with data.

    Data will be received from Nimble api.
    """
    contacts: List[Dict] = get_nimble_api_data()
    update_contacts_data(contacts)
