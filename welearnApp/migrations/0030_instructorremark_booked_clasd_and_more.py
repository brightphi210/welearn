# Generated by Django 5.0.6 on 2024-09-11 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welearnApp', '0029_adminseeremarks_alter_user_user_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorremark',
            name='booked_clasd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='welearnApp.booking'),
        ),
        migrations.AddField(
            model_name='studentremark',
            name='booked_clasd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='welearnApp.booking'),
        ),
    ]
