# Generated by Django 4.1.1 on 2024-05-15 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('welearnApp', '0009_class_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorprofile',
            name='is_hired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instructorprofile',
            name='number_of_trained_students',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='welearnApp.instructorprofile')),
            ],
        ),
    ]