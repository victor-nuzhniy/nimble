"""Urls list for 'api' app."""
from django.urls import path

from api.views import (
    contact,
    create_contact,
    delete_contacts,
    get_contacts,
    search_contacts,
    update_contact,
)

urlpatterns = [
    path("contacts/", get_contacts, name="get_contacts"),
    path("contacts/delete/", delete_contacts, name="delete_contacts"),
    path("contact/create/", create_contact, name="create_contact"),
    path("contact/<int:pk>/", contact, name="contact"),
    path("contact/<int:pk>/update", update_contact, name="update_contact"),
    path("contacts/search/", search_contacts, name="search_contact"),
]
