# Generated by Django 5.0.6 on 2024-06-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welearnApp', '0011_booking_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]