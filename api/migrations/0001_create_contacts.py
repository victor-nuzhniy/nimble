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
            email varchar(100),
            CONSTRAINT rector_pk PRIMARY KEY (contact_id)
            );
            CREATE SEQUENCE IF NOT EXISTS contact_id_seq
             AS bigint START WITH 1 INCREMENT BY 1;
            ALTER TABLE contacts ALTER COLUMN contact_id
             SET DEFAULT nextval('contact_id_seq');
            CREATE UNIQUE INDEX first_last_name_idx ON contacts(first_name, last_name);
            """,
            """
            DROP TABLE contacts;
            """,
        )
    ]
