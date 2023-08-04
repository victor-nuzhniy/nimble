"""Module with view funtion for 'api' app."""
from django.db import connection
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from api.utils import dictfetchall, get_delete_contacts_query


@api_view(["GET"])
@permission_classes([AllowAny])
def get_contacts(request: HttpRequest) -> Response:
    """Get or delete contacts list data."""
    query = "SELECT * FROM contacts"
    with connection.cursor() as cursor:
        cursor.execute(query)
        contacts = dictfetchall(cursor)
    return Response({"contacts": contacts}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_contacts(request: HttpRequest) -> Response:
    """Delete all contacts data."""
    query = get_delete_contacts_query()
    with connection.cursor() as cursor:
        cursor.execute(query)
    return Response({"operation": "successful"}, status=status.HTTP_200_OK)
