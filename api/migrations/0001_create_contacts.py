"""Initial migration for 'api' app."""

from django.db import migrations


class Migration(migrations.Migration):
    """Class for migration/creating Contacts table."""

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS contacts(
            contact_id integer NOT NULL,
            first_name varchar(100) NOT NULL,
            last_name varchar(100) NOT NULL,
            email varchar(100)
            );
            """
        )
    ]
