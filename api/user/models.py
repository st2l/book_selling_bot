from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class BotText(models.Model):
    # for bot texts

    name = models.CharField('Наименование', max_length=255)
    text = models.TextField('Текст сообщения')

    class Meta:
        verbose_name = 'Текст бота'
        verbose_name_plural = 'Тексты бота'

    def __str__(self):
        return self.name


class SubscriptionDetails(models.Model):
    # for subscription details

    name = models.CharField('Наименование подписки', max_length=255)
    description = models.TextField('Описание подписки')
    price = models.DecimalField('Цена подписки', max_digits=10, decimal_places=2)
    days = models.IntegerField('Количество дней (по хорошему не менять)', default=0)

    class Meta:
        verbose_name = 'Тарифы подписок'
        verbose_name_plural = 'Тарифы подписок'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    # for subscriptions of users

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(
        SubscriptionDetails, verbose_name='Тариф подписки', on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField('Дата оформления подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользовательская подписка'
        verbose_name_plural = 'Пользовательские подписки'

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"


class ThemePool(models.Model):
    name = models.CharField('Название темы', max_length=255)

    class Meta:
        verbose_name = 'Доступные пользователю темы'
        verbose_name_plural = 'Доступные пользователю темы'

    def __str__(self):
        return self.name


class Theme(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    theme_type = models.ForeignKey(ThemePool, verbose_name='Тип темы', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Выбранная пользователем тема'
        verbose_name_plural = 'Выбранные пользователем темы'


class Notification(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    text = models.TextField('Текст уведомления')
    time = models.TextField('Время уведомления', null=True)

    class Meta:
        verbose_name = 'Пользовательское уведомление'
        verbose_name_plural = 'Пользовательские уведомления'

    def __str__(self):
        return self.text


class Rating(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rating = models.IntegerField('Оценка')

    class Meta:
        verbose_name = 'Оценка пользователя'
        verbose_name_plural = 'Оценки пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


class Methodic(models.Model):
    # for methodics in shop

    name = models.CharField('Наименование методички', max_length=255)
    price = models.DecimalField('Цена методички', max_digits=10, decimal_places=2)
    description = models.TextField('Описание методички')
    material = models.FileField(upload_to="methodics/")

    class Meta:
        verbose_name = 'Методичка'
        verbose_name_plural = 'Методички'

    def __str__(self):
        return self.name


class ShortMethodic(models.Model):
    # for short methodics in shop

    name = models.CharField('Наименование краткой методички', max_length=255)
    price = models.DecimalField('Цена краткой методички', max_digits=10, decimal_places=2)
    description = models.TextField('Описание краткой методички')
    material = models.FileField(upload_to="short_methodics/", null=True)

    class Meta:
        verbose_name = 'Краткая методичка'
        verbose_name_plural = 'Краткие методички'

    def __str__(self):
        return self.name


class Book(models.Model):
    # for book in shop

    name = models.CharField('Наименование книги', max_length=255)
    price = models.DecimalField('Цена книги', max_digits=10, decimal_places=2)
    description = models.TextField('Описание книги')
    material = models.FileField(upload_to="books/")

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name


class History(models.Model):
    # for history of user's purchases

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    methodic = models.ForeignKey(
        Methodic, verbose_name='Методичка', on_delete=models.CASCADE, null=True, blank=True)

    short_methodic = models.ForeignKey(
        ShortMethodic, verbose_name='Краткая методичка', on_delete=models.CASCADE, null=True, blank=True)

    book = models.ForeignKey(
        Book, verbose_name='Книга', on_delete=models.CASCADE, null=True, blank=True)

    date_of_purchase = models.DateTimeField('Дата покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'

    def __str__(self):
        return f"{self.user.username} - {self.methodic} - {self.short_methodic} - {self.book}"


class Task(models.Model):

    number_of_chapter = models.IntegerField('Номер главы')
    text = models.TextField('Текст задания')

    class Meta:
        verbose_name = 'Глава и задания к ней'
        verbose_name_plural = 'Главы и задания к ним'

    def __str__(self):
        return f"Глава {self.number_of_chapter}"


class TaskSolved(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE)
    text = models.TextField('Текст решения', default='')
    date_of_solving = models.DateTimeField('Дата решения', auto_now_add=True)

    class Meta:
        verbose_name = 'Решённое пользователем ызадание'
        verbose_name_plural = 'Решённые пользователем задания'

    def __str__(self):
        return f"{self.user.username} - {self.task.number_of_chapter}"


class SendMessage(models.Model):

    BUTTON_TEXT_CHOICES = (
        ('option1', 'Нет кнопки'),
        ('option2', 'Кнопка на ЛК'),
        ('option3', 'Кнопка на задания'),
        ('option4', 'Кнопка на покупку книги'),
        ('option5', 'Кнопка на покупку методичек'),
    )

    message = models.TextField('Сообщение')
    date_to_send = models.DateTimeField('Дата отправки')
    theme_type = models.ForeignKey(ThemePool, verbose_name='Тип темы', on_delete=models.CASCADE)
    theme_all = models.BooleanField('Для всех тем', default=False)

    photo_1 = models.ImageField('Фото 1', upload_to='photos/', null=True, blank=True)
    photo_2 = models.ImageField('Фото 2', upload_to='photos/', null=True, blank=True)
    photo_3 = models.ImageField('Фото 3', upload_to='photos/', null=True, blank=True)
    photo_4 = models.ImageField('Фото 4', upload_to='photos/', null=True, blank=True)
    photo_5 = models.ImageField('Фото 5', upload_to='photos/', null=True, blank=True)

    video_1 = models.FileField('Видео 1', upload_to='videos/', null=True, blank=True)
    video_2 = models.FileField('Видео 2', upload_to='videos/', null=True, blank=True)
    video_3 = models.FileField('Видео 3', upload_to='videos/', null=True, blank=True)

    button_text = models.CharField('Тип кнопки', max_length=50, choices=BUTTON_TEXT_CHOICES)

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'

    def __str__(self):
        return self.message


class DialogTask(models.Model):
    day_number = models.IntegerField('День')
    message = models.TextField('Сообщение')
    time_of_day = models.CharField(
        'Время дня',
        max_length=10,
        choices=[('утро', 'Утро'), ('вечер', 'Вечер')]
    )

    class Meta:
        verbose_name = 'Ежедневное диалог-задание'
        verbose_name_plural = 'Ежедневные диалог-задания'

    def __str__(self):
        return f"День {self.day_number} - {self.time_of_day}"


class DialogResponse(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    dialog_task = models.ForeignKey(DialogTask, verbose_name='Задание диалога', on_delete=models.CASCADE)
    response_text = models.TextField('Текст ответа', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Ответ на диалог'
        verbose_name_plural = 'Ответы на диалоги'

    def __str__(self):
        return f"{self.user.username} - День {self.dialog_task.day_number}"


class SubscriptionRenewal(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionDetails, verbose_name='Тариф подписки', on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Продление подписки'
        verbose_name_plural = 'Продления подписок'

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"
