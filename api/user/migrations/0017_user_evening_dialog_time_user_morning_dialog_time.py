# Generated by Django 5.1.5 on 2025-02-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_ratingrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='evening_dialog_time',
            field=models.CharField(default='22:00', max_length=5, verbose_name='Время вечернего диалога'),
        ),
        migrations.AddField(
            model_name='user',
            name='morning_dialog_time',
            field=models.CharField(default='10:00', max_length=5, verbose_name='Время утреннего диалога'),
        ),
    ]
