from django.db import models

__all__ = ["FeedbackFormModel"]


class FeedbackFormModel(models.Model):
    name = models.CharField(
        "Имя",
        max_length=20,
    )
    text = models.CharField(
        "Отзыв",
        max_length=100,
    )
    created_on = models.DateField(
        "время создания",
        auto_now_add=True,
    )
    email = models.EmailField(
        "Почта",
        max_length=100,
    )
