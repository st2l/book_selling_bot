# Generated by Django 5.1.5 on 2025-02-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='time',
            field=models.TextField(null=True),
        ),
    ]
