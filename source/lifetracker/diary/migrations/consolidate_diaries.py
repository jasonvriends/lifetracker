from django.db import migrations
from django.utils import timezone
import datetime

def transfer_diary_entries(apps, schema_editor):
    # Since we've already deleted the old apps, we can't transfer data
    # This migration now serves as a marker for the consolidation
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('diary', '0001_initial'),  # Update this to your latest migration
    ]

    operations = [
        migrations.RunPython(transfer_diary_entries),
    ] 