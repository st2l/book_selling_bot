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


class Subscription(models.Model):
    # for subscriptions of users

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # can be "weekly" or "monthly", "3 mounths"
    subscription_type = models.CharField(max_length=255)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription}"


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
    date_of_solving = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.number_of_chapter}"
