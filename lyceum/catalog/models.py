from django.core import validators
from django.db import models
import django.utils
import sorl.thumbnail

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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    def image_tmb(self):
        if self.main_image.image:
            thumbnail = self.main_image.get_image_50x50
            print(thumbnail.url)
            return django.utils.safestring.mark_safe(
                f'<img src="{thumbnail.url}">'
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class BaseImage(models.Model):
    image = models.ImageField(
        "изображение",
        upload_to="items",
        default=None,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "50x50",
            crop="center",
            quality=51,
        )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Image {self.id}"


class MainImage(BaseImage):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "главная картинка"
        verbose_name_plural = "главные картинки"

    def __str__(self):
        return f"Image {self.id}"


class Image(BaseImage):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = "дополнительная картинка"
        verbose_name_plural = "дополнительные картинки"

    def __str__(self):
        return f"Image {self.id}"
