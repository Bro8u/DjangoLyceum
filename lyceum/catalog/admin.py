from django.contrib import admin
from django.utils import html

import catalog.models


__all__ = ["CatalogItemAdmin", "ImageInline", "MainImageInline"]


class MainImageInline(admin.StackedInline):
    model = catalog.models.MainImage
    fields = (
        "image_tag",
        "image",
    )
    readonly_fields = ("image_tag",)

    def image_tag(self, obj: catalog.models.Image):
        if obj.id and obj.image:
            return html.format_html(
                '<img src="{}" />', obj.get_image_300x300().url
            )
        else:
            return "Нет изображения"

    image_tag.short_description = "Предпросмотр"


class ImageInline(admin.TabularInline):
    model = catalog.models.Image
    fields = (
        "image_tag",
        "image",
    )
    readonly_fields = ("image_tag",)

    def image_tag(self, obj: catalog.models.Image):
        if obj.id and obj.image:
            return html.format_html(
                '<img src="{}" />',
                obj.get_image_300x300().url,
            )
        else:
            return "Нет изображения"

    image_tag.short_description = "Предпросмотр"


@admin.register(catalog.models.Item)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.image_tmb,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [
        MainImageInline,
        ImageInline,
    ]


admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)
