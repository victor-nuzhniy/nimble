"""Schemas module for 'api' app."""
import coreapi
from rest_framework.schemas import AutoSchema

contact_create_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="first_name",
            required=True,
            location="form",
            description="Contact first name",
        ),
        coreapi.Field(
            name="last_name",
            required=True,
            location="form",
            description="Contact last name",
        ),
        coreapi.Field(
            name="email", required=True, location="form", description="Contact email"
        ),
    ],
)


contact_update_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="first_name",
            required=True,
            location="form",
            description="Contact first name",
        ),
        coreapi.Field(
            name="last_name",
            required=True,
            location="form",
            description="Contact last name",
        ),
        coreapi.Field(
            name="email", required=True, location="form", description="Contact email"
        ),
    ]
)


contacts_search_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="search_data",
            required=True,
            location="form",
            description="Search string",
        ),
    ]
)
