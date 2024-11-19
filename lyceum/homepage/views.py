from http import HTTPStatus

import django.http
from django.shortcuts import render

import catalog.models
from feedback.forms import FeedbackForm
from feedback.models import Feedback


__all__ = ["home", "coffee", "echo", "echo_submit"]


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method != "GET":
        return django.http.HttpResponseNotAllowed(["GET"])

    template = "homepage/echo.html"
    form = FeedbackForm()
    context = {"form": form}
    return render(request, template, context)


def echo_submit(request):
    if request.method != "POST":
        return django.http.HttpResponseNotAllowed(["POST"])

    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        Feedback.objects.create(**form.cleaned_data)
        return django.http.HttpResponse(
            form.cleaned_data["text"],
            content_type="text/plain; charset=utf-8",
        )

    return django.http.HttpResponse(
        "Не валидная форма",
        content_type="text/plain; charset=utf-8",
    )
