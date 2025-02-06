from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class BotText(models.Model):
    # for bot texts

    name = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.name


class SubscriptionDetails(models.Model):
    # for subscription details

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    # for subscriptions of users

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(
        SubscriptionDetails, on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"


class ThemePool(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Theme(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme_type = models.ForeignKey(ThemePool, on_delete=models.CASCADE)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    time = models.TextField(null=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Methodic(models.Model):
    # for methodics in shop

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    material = models.FileField(upload_to="methodics/")

    def __str__(self):
        return self.name


class ShortMethodic(models.Model):
    # for short methodics in shop

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    material = models.FileField(upload_to="short_methodics/", null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    # for book in shop

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    material = models.FileField(upload_to="books/")

    def __str__(self):
        return self.name


class History(models.Model):
    # for history of user's purchases

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    methodic = models.ForeignKey(
        Methodic, on_delete=models.CASCADE, null=True, blank=True)

    short_methodic = models.ForeignKey(
        ShortMethodic, on_delete=models.CASCADE, null=True, blank=True)

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, blank=True)

    date_of_purchase = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.methodic} - {self.short_methodic} - {self.book}"


class Task(models.Model):

    number_of_chapter = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"Chapter {self.number_of_chapter}"


class TaskSolved(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField(default='')
    date_of_solving = models.DateTimeField(auto_now_add=True)

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

    message = models.TextField()
    date_to_send = models.DateTimeField()
    theme_type = models.ForeignKey(ThemePool, on_delete=models.CASCADE)
    theme_all = models.BooleanField(default=False)

    photo_1 = models.ImageField(upload_to='photos/', null=True, blank=True)
    photo_2 = models.ImageField(upload_to='photos/', null=True, blank=True)
    photo_3 = models.ImageField(upload_to='photos/', null=True, blank=True)
    photo_4 = models.ImageField(upload_to='photos/', null=True, blank=True)
    photo_5 = models.ImageField(upload_to='photos/', null=True, blank=True)

    video_1 = models.FileField(upload_to='videos/', null=True, blank=True)
    video_2 = models.FileField(upload_to='videos/', null=True, blank=True)
    video_3 = models.FileField(upload_to='videos/', null=True, blank=True)

    button_text = models.CharField(max_length=50, choices=BUTTON_TEXT_CHOICES)

    def __str__(self):
        return self.message


class DialogTask(models.Model):
    day_number = models.IntegerField()  # День отправки (1-90)
    message = models.TextField()  # Сообщение с заданием
    time_of_day = models.CharField(
        max_length=10,
        choices=[('утро', 'Утро'), ('вечер', 'Вечер')]
    )

    def __str__(self):
        return f"День {self.day_number} - {self.time_of_day}"


class DialogResponse(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dialog_task = models.ForeignKey(DialogTask, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - День {self.dialog_task.day_number}"
