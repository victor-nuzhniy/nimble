"""Migration 0002 for full text search for 'api' app."""

from django.db import migrations


class Migration(migrations.Migration):
    """Class for migration/creating Contacts table."""

    initial = True

    dependencies = [("api", "0001_create_contacts")]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION make_tsvector(first_name TEXT, last_name TEXT,
             email TEXT)
                RETURNS tsvector AS $$
            BEGIN
                RETURN (setweight(to_tsvector('english', first_name), 'A') ||
                    setweight(to_tsvector('english', last_name), 'B') ||
                    setweight(to_tsvector('english', email), 'C'));
            END
            $$ LANGUAGE 'plpgsql' IMMUTABLE;
            CREATE INDEX IF NOT EXISTS idx_contacts_full ON contacts
                USING gin(make_tsvector(first_name, last_name, email));
            """,
            """
            DROP INDEX IF EXISTS idx_contacts_full;
            DROP FUNCTION IF EXISTS make_tsvector;
            """,
        )
    ]
