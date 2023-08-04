"""Urls list for 'api' app."""
from django.urls import path

from api.views import (
    contact,
    create_contact,
    delete_contacts,
    get_contacts,
    update_contact,
)

urlpatterns = [
    path("contacts/", get_contacts),
    path("contacts/delete/", delete_contacts),
    path("contact/create/", create_contact),
    path("contact/<int:pk>/", contact),
    path("contact/<int:pk>/update", update_contact),
]
