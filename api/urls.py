"""Urls list for 'api' app."""
from django.urls import path, include

from api.views import contacts_json

app_name = "api"

urlpatterns = [
    path("contacts/json/", contacts_json, name="contacts_json"),
]
