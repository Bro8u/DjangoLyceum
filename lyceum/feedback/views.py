import django.contrib.messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from feedback.forms import FeedbackForm
from feedback.models import FeedbackFormModel


__all__ = ["feedback"]


def feedback(request):
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        template = "feedback/feedback.html"
        feedback = form.cleaned_data
        send_mail(
            "Отзыв",
            feedback["text"],
            django.conf.settings.FEEDBACK_SENDER,
            [feedback["email"]],
        )
        FeedbackFormModel.objects.create(**form.cleaned_data)
        django.contrib.messages.success(
            request,
            "Фидбек отправлен. Спасибо!",
        )
        return redirect(
            reverse("feedback:feedback"),
        )

    template = "feedback/feedback.html"
    form = FeedbackForm()
    context = {
        "form": form,
    }
    return render(request, template, context)
