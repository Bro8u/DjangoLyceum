import os

import django.contrib.messages
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from feedback.forms import FeedbackForm
from feedback.models import FeedbackFormModel


__all__ = ["feedback"]


def feedback(request):
    if request.method == "GET":
        print("GET")
        template = "feedback/feedback.html"
        form = FeedbackForm()
        context = {
            "form": form,
        }
        return render(request, template, context)

    if request.method == "POST":
        print("POST")
        template = "feedback/feedback.html"
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            feedback = form.cleaned_data
            send_mail(
                "Обратная связь",  # Тема письма
                feedback["text"],  # Тело письма
                os.environ.get(
                    "DJANGO_MAIL"
                ),  # Отправитель (из переменной окружения)
                [feedback["email"]],  # Получатель
            )
            FeedbackFormModel.objects.create(**form.cleaned_data)
            django.contrib.messages.success(
                request,
                "Фидбек отправлен. Спасибо!",
            )
            return redirect(
                reverse("feedback:feedback"),
            )
        return HttpResponseBadRequest("Данные заполнены некорректно.")
