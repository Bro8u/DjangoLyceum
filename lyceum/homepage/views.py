from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from feedback.forms import FeedbackForm
from feedback.models import Feedback

import catalog.models


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
        return HttpResponseNotAllowed([""])

    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        Feedback.objects.create(
            **form.cleaned_data,
        )
        return HttpResponse(
            form.cleaned_data["text"],
            content_type="text/plain; charset=utf-8",
        )
