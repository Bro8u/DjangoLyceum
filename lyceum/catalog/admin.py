from django.contrib import admin

import catalog.models


@admin.register(catalog.models.CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.CatalogItem.name.field.name,
        catalog.models.CatalogItem.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = (catalog.models.CatalogItem.tags.field.name,)


admin.site.register(catalog.models.CatalogCategory)
admin.site.register(catalog.models.CatalogTag)
