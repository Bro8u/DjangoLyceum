from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, id):
    template = "catalog/item.html"
    return render(request, template)


def converter_and_reqular_expression(request, number):
    return HttpResponse(number)
