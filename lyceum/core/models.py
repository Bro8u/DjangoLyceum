from django.db import models


class CommonFieldsModel(models.Model):
    id = models.AutoField(primary_key=True)
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликовано"
    )
    name = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        abstract = True
