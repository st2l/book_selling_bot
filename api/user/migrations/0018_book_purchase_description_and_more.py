# Generated by Django 5.1.5 on 2025-02-20 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_user_evening_dialog_time_user_morning_dialog_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='purchase_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание при покупке'),
        ),
        migrations.AddField(
            model_name='methodic',
            name='purchase_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание при покупке'),
        ),
        migrations.AddField(
            model_name='shortmethodic',
            name='purchase_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание при покупке'),
        ),
    ]
