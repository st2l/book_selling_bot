# Generated by Django 5.1.5 on 2025-02-04 20:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_tasksolved_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_to_send', models.DateTimeField()),
                ('theme_all', models.BooleanField(default=False)),
                ('photo_1', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('photo_2', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('photo_3', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('photo_4', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('photo_5', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('video_1', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('video_2', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('video_3', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('button_text', models.CharField(choices=[('option1', 'Нет кнопки'), ('option2', 'Кнопка на ЛК'), ('option3', 'Кнопка на задания'), ('option4', 'Кнопка на покупку книги'), ('option5', 'Кнопка на покупку методичек')], max_length=50)),
                ('theme_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.themepool')),
            ],
        ),
    ]
