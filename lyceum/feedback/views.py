import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls

from feedback.forms import FeedbackAutherForm, FeedbackForm
from feedback.models import Feedback, FeedbackAuther


__all__ = ["feedback"]


def feedback(request):
    feedback_author = FeedbackAutherForm(request.POST or None)
    feedback_form = FeedbackForm(request.POST or None)
    context = {
        "feedback_form": feedback_form,
        "feedback_auther": feedback_author,
    }

    forms = (feedback_form, feedback_author)

    if request.method == "POST" and all(form.is_valid() for form in forms):
        django.core.mail.send_mail(
            f"Привет {feedback_author.cleaned_data['name']}",
            f"{feedback_form.cleaned_data['text']}",
            django.conf.settings.FEEDBACK_SENDER,
            [feedback_author.cleaned_data["mail"]],
            fail_silently=True,
        )
        feedback_item = Feedback.objects.create(**feedback_form.cleaned_data)
        feedback_item.save()
        FeedbackAuther.objects.create(
            feedback=feedback_item,
            **feedback_author.cleaned_data,
        )
        django.contrib.messages.success(
            request,
            "Фидбек отправлен. Спасибо!",
        )
        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )

    return django.shortcuts.render(
        request,
        "feedback/feedback.html",
        context,
    )
