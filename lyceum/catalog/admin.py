from django.contrib import admin

import catalog.models


@admin.register(catalog.models.CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


admin.site.register(catalog.models.CatalogCategory)
admin.site.register(catalog.models.CatalogTag)
