# Generated by Django 5.1.5 on 2025-02-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_notification_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksolved',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
