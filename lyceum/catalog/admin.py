from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Item)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.NAME_FIELD,
        catalog.models.Item.IS_PUBLISHED_FIELD,
    )
    list_editable = (catalog.models.Item.IS_PUBLISHED_FIELD,)
    list_display_links = (catalog.models.Item.NAME_FIELD,)
    filter_horizontal = (catalog.models.Item.TAGS_FIELD,)


admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)
