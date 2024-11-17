from http import HTTPStatus

import django.db.models
from django.http import HttpResponse
from django.shortcuts import render

import catalog.models 


__all__ = ["home", "coffee"]


def home(request):
    template = "homepage/home.html"
    
    items = (
        catalog.models.Item.objects.on_main()
    )
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
