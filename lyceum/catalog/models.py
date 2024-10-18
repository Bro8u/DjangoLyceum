import re

from django.core import exceptions, validators
from django.db import models

from core.models import CommonFieldsModel


def validate_text(value):
    if not re.search(r"\b(превосходно|роскошно)\b", value, re.IGNORECASE):
        raise exceptions.ValidationError(
            'Текст должен содержать слово "превосходно" или "роскошно".'
        )


class Item(CommonFieldsModel):
    text = models.TextField(
        validators=[validate_text],
        verbose_name="Текст",
        help_text="Введите полное описание товара.",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(
        "Tag", related_name="items", verbose_name="Теги"
    )
    TAGS_FIELD = "tags"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


slug_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z0-9_-]+$",
    message="Слаг может содержать только"
    "латинские буквы, цифры, дефисы и подчёркивания.",
)


class Tag(CommonFieldsModel):
    slug = models.TextField(
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


class Category(CommonFieldsModel):
    slug = models.TextField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        validators=[slug_validator],
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )
    weight = models.IntegerField(
        default=100,
        verbose_name="Вес",
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(32767),
        ],
        help_text="Введите целое число от 0 до 32767",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
