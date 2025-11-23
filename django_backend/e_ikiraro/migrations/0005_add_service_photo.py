"""
Migration to add service_photo ImageField to Service
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_ikiraro', '0004_alter_passportapplication_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_photo',
            field=models.ImageField(
                blank=True, null=True, upload_to='documents/service_photos/'),
        ),
    ]
