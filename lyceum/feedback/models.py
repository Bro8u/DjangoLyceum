from django.db import models

__all__ = ["Feedback", "FeedbackAuther"]


class Feedback(models.Model):
    text = models.CharField(
        "Отзыв",
        max_length=250,
    )
    created_on = models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )
    name = models.CharField(
        "Имя",
        max_length=200,
        blank=True,
        null=True,
    )
    mail = models.EmailField(
        "Почта",
        blank=True,
        null=True,
    )


class FeedbackAuther(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        related_name="author",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        "Имя",
        max_length=200,
        blank=True,
        null=True,
    )
    mail = models.EmailField(
        "Почта",
    )
