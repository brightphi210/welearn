# Generated by Django 5.0.6 on 2024-09-14 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welearnApp', '0030_instructorremark_booked_clasd_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_secret',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
