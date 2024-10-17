import re

from core.models import CommonFieldsModel
import django.core.exceptions
import django.core.validators
from django.db import models


def validate_text(value):
    if not re.search(r"\b(превосходно|роскошно)\b", value, re.IGNORECASE):
        raise django.core.exceptions.ValidationError(
            'Текст должен содержать слово "превосходно" или "роскошно".'
        )


class CatalogItem(CommonFieldsModel):
    text = models.TextField(validators=[validate_text], verbose_name="Текст")
    category = models.ForeignKey(
        "CatalogCategory",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(
        "CatalogTag", related_name="items", verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


slug_validator = django.core.validators.RegexValidator(
    regex=r"^[a-zA-Z0-9_-]+$",
    message="Слаг может содержать только"
    "латинские буквы, цифры, дефисы и подчёркивания.",
)


class CatalogTag(CommonFieldsModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        validators=[slug_validator],
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class CatalogCategory(CommonFieldsModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        validators=[slug_validator],
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )
    weight = models.PositiveSmallIntegerField(
        default=100,
        verbose_name="Вес",
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
