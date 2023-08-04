"""Urls list for 'api' app."""
from django.urls import path

from api.views import delete_contacts, get_contacts

urlpatterns = [
    path("contacts/", get_contacts),
    path("contacts/delete/", delete_contacts),
]
