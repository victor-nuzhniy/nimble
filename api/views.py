"""Module with view funtion for 'api' app."""
from typing import Dict, List, Optional, Tuple

from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from api.queries import (
    get_create_single_contact_query,
    get_delete_contacts_query,
    get_delete_single_contact_query,
    get_read_single_contact_query,
    get_search_contacts_query,
    get_select_contacts_query,
    get_update_single_contact_query,
)
from api.schemas import (
    contact_create_schema,
    contact_update_schema,
    contacts_search_schema,
)
from api.utils import dictfetchall
from api.validators import validate_contact_input


@api_view(["GET"])
@permission_classes([AllowAny])
def get_contacts(request: Request) -> Response:
    """Get or delete contacts list data."""
    query: Tuple[str, Tuple] = get_select_contacts_query()
    with connection.cursor() as cursor:
        cursor.execute(*query)
        contacts: List[Dict] = dictfetchall(cursor)
    return Response({"contacts": contacts}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
@schema(contacts_search_schema)
def search_contacts(request: Request) -> Response:
    """Get contacts list in accordance with search input."""
    search_data: str = request.data.get("search_data")
    query: Tuple[str, Tuple] = get_search_contacts_query(search_data)
    with connection.cursor() as cursor:
        cursor.execute(*query)
        contacts: List[Dict] = dictfetchall(cursor)
    return Response({"contacts": contacts}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_contacts(request: Request) -> Response:
    """Delete all contacts data. Only for ADMIN."""
    query: Tuple[str, Tuple] = get_delete_contacts_query()
    with connection.cursor() as cursor:
        cursor.execute(*query)
    return Response({"operation": "successful"}, status=status.HTTP_200_OK)


@api_view(["GET", "DELETE"])
@permission_classes([IsAdminUser])
def contact(request: Request, pk: int) -> Response:
    """Perform read and delete operations with contacts table. Only for ADMIN."""
    if request.method == "GET":
        query: Tuple[str, Tuple] = get_read_single_contact_query(pk)
        with connection.cursor() as cursor:
            cursor.execute(*query)
            data: List[Optional[Dict]] = (
                dictfetchall(cursor) if cursor.description else []
            )
            result: Dict = data[0] if data else dict()
        return Response({"contact": result}, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        query = get_delete_single_contact_query(pk)
        with connection.cursor() as cursor:
            cursor.execute(*query)
        return Response(
            {"result": "Successfully deleted contact."}, status=status.HTTP_200_OK
        )
    return Response(
        {"Error": "Method not implemented"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@api_view(["PUT"])
@permission_classes([IsAdminUser])
@schema(contact_update_schema)
def update_contact(request: Request, pk: int) -> Response:
    """Perform update operation with contacts table. Only for ADMIN."""
    data: Dict = request.data
    if not validate_contact_input(data):
        return Response(
            {"Error": "Invalid data"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
    query: Tuple[str, Tuple] = get_update_single_contact_query(
        pk, data["first_name"], data["last_name"], data["email"]
    )
    with connection.cursor() as cursor:
        cursor.execute(*query)
    return Response(
        {"result": "Successfully updated contact."}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAdminUser])
@schema(contact_create_schema)
def create_contact(request: Request) -> Response:
    """Create single contact. Only for ADMIN."""
    data: Dict = request.data
    if validate_contact_input(data):
        query: Tuple[str, Tuple] = get_create_single_contact_query(
            data["first_name"], data["last_name"], data["email"]
        )
        with connection.cursor() as cursor:
            cursor.execute(*query)
        return Response({"result": "Contact was created."}, status=status.HTTP_200_OK)
    return Response({"Error": "Invalid data."}, status=status.HTTP_406_NOT_ACCEPTABLE)
