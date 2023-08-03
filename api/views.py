"""Module with view funtion for 'api' app."""
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils import dictfetchall


@api_view(["GET"])
def contacts_json(request):
    """Get contacts list data."""
    query = "SELECT * FROM contacts"
    with connection.cursor() as cursor:
        cursor.execute(query)
        contacts = dictfetchall(cursor)
    return Response({"contacts": contacts})
