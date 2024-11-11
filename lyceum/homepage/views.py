from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


__all__ = ["home", "coffee"]


def home(request):
    template = "homepage/home.html"
    all_items = Item.objects.all()
    return render(request, template, {"all_items": all_items})


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
