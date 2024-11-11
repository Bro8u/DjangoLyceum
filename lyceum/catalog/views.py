from django.http import HttpResponse
from django.shortcuts import render


__all__ = ["item_list", "item_detail", "converter_and_reqular_expression"]


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, item_id):
    template = "catalog/item.html"
    context = {"item_id": item_id}
    return render(request, template, context)


def converter_and_reqular_expression(request, number):
    return HttpResponse(number)
