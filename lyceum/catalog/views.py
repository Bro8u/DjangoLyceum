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
    queryset = catalog.models.Item.objects.prefetch_images(
        catalog.models.Item.objects.published(),
    )
    item = get_object_or_404(
        queryset,
        pk=item_id,
    )
    context = {"item": item}
    return render(request, template, context)


def converter_and_reqular_expression(request, number):
    return HttpResponse(number)
