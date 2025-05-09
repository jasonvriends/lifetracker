from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_alter_diary_content'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL - Drop the ingredients column if it exists
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'diary_diary'
                    AND column_name = 'ingredients'
                ) THEN
                    ALTER TABLE diary_diary DROP COLUMN ingredients;
                END IF;
            END $$;
            """,
            # Reverse SQL - Add the ingredients column back (with NULL allowed)
            """
            ALTER TABLE diary_diary ADD COLUMN ingredients text NULL;
            """
        ),
    ] 