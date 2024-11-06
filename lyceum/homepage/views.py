from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def home(request):
    template = "homepage/home.html"
    all_items = Item.objects.all()
    return render(request, template, {"all_items": all_items})
    # return HttpResponse("<body>Главная</body>")


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
