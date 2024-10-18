import re

from django.core import exceptions, validators
from django.db import models

from core.models import CommonFieldsModel


def validate_text(value):
    if not re.search(r"\b(превосход\w*|роскош\w*)\b", value, re.IGNORECASE):
        raise exceptions.ValidationError(
            'Текст должен содержать слово с корнем "превосход" или "роскош".',
        )


slug_validator = validators.RegexValidator(
    regex=r"^[a-zA-Z0-9_-]+$",
    message="Слаг может содержать только"
    "латинские буквы, цифры, дефисы и подчёркивания.",
)


class Tag(CommonFieldsModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[slug_validator],
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
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
        validators=[slug_validator],
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )
    weight = models.IntegerField(
        default=100,
        verbose_name="вес",
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(32767),
        ],
        help_text="Введите целое число от 0 до 32767",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(CommonFieldsModel):
    text = models.TextField(
        validators=[validate_text],
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
