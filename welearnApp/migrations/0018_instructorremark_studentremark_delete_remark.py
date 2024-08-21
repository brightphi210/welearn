# Generated by Django 5.0.6 on 2024-06-22 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welearnApp', '0017_remove_remark_course_remove_remark_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructorRemark', to='welearnApp.instructorprofile')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='welearnApp.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='welearnApp.instructorprofile')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='welearnApp.studentprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='Remark',
        ),
    ]
