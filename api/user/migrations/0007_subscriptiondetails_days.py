# Generated by Django 5.1.5 on 2025-02-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_notification_themepool_rating_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiondetails',
            name='days',
            field=models.IntegerField(default=0),
        ),
    ]
