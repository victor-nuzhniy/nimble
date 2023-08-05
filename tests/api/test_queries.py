"""Module for testing api.queries."""
from api.queries import get_select_contacts_query


class TestGetSelectContactsQuery:
    """Class for testing get_select_contacts_query."""

    def test_get_select_contacts_query(self) -> None:
        """Test get_select_contacts_query."""
        response = get_select_contacts_query()
        assert response == "SELECT * FROM contacts"
