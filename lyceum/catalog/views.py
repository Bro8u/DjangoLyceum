import django.db.models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = ["item_list", "item_detail", "converter_and_reqular_expression"]


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published()
    context = {"items": items}
    return render(request, template, context)


def item_detail(request, item_id):
    template = "catalog/item.html"
    queryset = catalog.models.Item.objects.published().prefetch_related(
        django.db.models.Prefetch(
            catalog.models.Item.images.field.related_query_name(),
            queryset=catalog.models.Image.objects.only(
                catalog.models.Image.image.field.name,
                catalog.models.Image.item_id.field.name,
            ),
        ),
    )

    item = get_object_or_404(
        queryset,
        pk=item_id,
    )
    context = {"item": item}
    return render(request, template, context)


def converter_and_reqular_expression(request, number):
    return HttpResponse(number)
