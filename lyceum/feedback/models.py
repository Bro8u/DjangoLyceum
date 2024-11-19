from django.db import models

__all__ = ["Feedback", "FeedbackAuther"]


class Feedback(models.Model):
    text = models.CharField(
        "Отзыв",
        max_length=250,
    )
    created = models.DateField(
        "время создания",
        auto_now_add=True,
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
    )
    mail = models.EmailField(
        "Почта",
        max_length=200,
    )
