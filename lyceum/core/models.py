from django.db import models


__all__ = ["CommonFieldsModel"]


class CommonFieldsModel(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="Введите короткое название, не более 50 символов.",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )

    class Meta:
        abstract = True
