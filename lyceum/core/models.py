from django.db import models


class CommonFieldsModel(models.Model):
    NAME_FIELD = "name"
    IS_PUBLISHED_FIELD = "is_published"
    id = models.AutoField(
        primary_key=True,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="Введите короткое название, не более 50 символов.",
    )

    class Meta:
        abstract = True
