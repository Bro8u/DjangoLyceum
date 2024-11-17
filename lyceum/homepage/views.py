from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
from homepage.forms import FeedbackForm


__all__ = ["home", "coffee", "echo", "echo_submit"]


def home(request):
    template = "homepage/home.html"

    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    template = "homepage/echo.html"
    form = FeedbackForm()
    context = {"form": form}
    return render(request, template, context)


def echo_submit(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        return HttpResponse(
            form.cleaned_data["text"], content_type="text/plain"
        )
