"""Module for 'import_contacts_from_csv' for 'api' app."""
import csv

from django.core.management import BaseCommand
from django.db import connection

from api.queries import get_insert_contact_query
from api.validators import validate_contact


class Command(BaseCommand):
    """Class for creating 'import_contacts_from_csv' command functionality."""

    help = (
        "Imports contacts from csv file. Expects columns "
        "'first name', 'last name', 'Email'."
    )

    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

    def __init__(self):
        """Add additional instance attributes."""
        super().__init__()
        self.file_path = None
        self.imported_counter = None
        self.skipped_counter = None

    def add_arguments(self, parser):
        """Add arguments to command."""
        parser.add_argument("file_path", nargs=1, type=str)

    def handle(self, *args, **options):
        """Handle Command methods."""
        self.file_path = options["file_path"][0]
        self.prepare()
        self.main()
        self.finalise()

    def prepare(self):
        """Prepare Command instance arguments."""
        self.imported_counter = 0
        self.skipped_counter = 0

    def main(self):
        """Process data from csv file to store or skipp."""
        self.stdout.write("===Importing contacts===")

        with open(self.file_path, mode="r") as f:
            reader = csv.DictReader(f)
            with connection.cursor() as cursor:
                for index, row_dict in enumerate(reader):
                    if validate_contact(row_dict):
                        query = get_insert_contact_query(row_dict)
                        cursor.execute(query)
                        self.imported_counter += 1
                    else:
                        self.stderr.write(
                            f"Error importing contacts"
                            f"{row_dict['first_name']} - {row_dict['last_name']}:\n"
                        )
                        self.skipped_counter += 1

    def finalise(self):
        """Finalise performing command with messages."""
        self.stdout.write("---------------\n")
        self.stdout.write(f"Contacts imported: {self.imported_counter}\n")
        self.stdout.write(f"Contacts skipped: {self.skipped_counter}\n")
