from __future__ import annotations

from typing import Any

from django.contrib import admin

from api.user.models import User, BotText, Subscription, Methodic, ShortMethodic, \
    Book, History, Task, TaskSolved, SubscriptionDetails, Theme, ThemePool, Notification, Rating, \
    SendMessage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups", "user_permissions")

    list_display = (
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    def save_model(
        self,
        request: Any,
        obj: User,
        form: None,
        change: bool,  # noqa: FBT001
    ) -> None:
        """Update user password if it is not raw.

        This is needed to hash password when updating user from admin panel.
        """
        has_raw_password = obj.password.startswith("pbkdf2_sha256")
        if not has_raw_password:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


@admin.register(BotText)
class BotTextAdmin(admin.ModelAdmin):
    list_display = ("name", "text")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "subscription_type", "date_of_creation")


@admin.register(Methodic)
class MethodicAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description", "material")


@admin.register(ShortMethodic)
class ShortMethodicAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description", "material")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description", "material")


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "methodic", "short_methodic",
                    "book", "date_of_purchase")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("number_of_chapter", "text")


@admin.register(TaskSolved)
class TaskSolvedAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "date_of_solving")


@admin.register(SubscriptionDetails)
class SubscriptionDetailsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description")


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("user", "theme_type")


@admin.register(ThemePool)
class ThemePoolAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("text", "time")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "rating")

@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    list_display = ("message", "date_to_send", "theme_type")
