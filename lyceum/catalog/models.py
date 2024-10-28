from django.core import validators
from django.db import models

import catalog.validators
from core.models import CommonFieldsModel


class Tag(CommonFieldsModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(CommonFieldsModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )
    weight = models.PositiveSmallIntegerField(
        default=100,
        verbose_name="вес",
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(32767),
        ],
        help_text="Введите целое число от 1 до 32766",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(CommonFieldsModel):
    text = models.TextField(
        validators=[catalog.validators.validate_text],
        verbose_name="Текст",
        help_text="Введите полное описание товара.",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag)
    TAGS_FIELD = "tags"

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
