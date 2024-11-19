import django.forms

from feedback.models import Feedback, FeedbackAuther


__all__ = ["FeedbackForm", "FeedbackAutherForm"]


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackAutherForm(BootstrapForm):

    class Meta:
        model = FeedbackAuther
        fields = {
            FeedbackAuther.name.field.name,
            FeedbackAuther.mail.field.name,
        }
        labels = {
            FeedbackAuther.name.field.name: "Имя",
            FeedbackAuther.mail.field.name: "Почта",
        }
        help_texts = {
            FeedbackAuther.name.field.name: "Имя <=  200 символов",
            FeedbackAuther.mail.field.name: "Корректная электронная почта",
        }


class FeedbackForm(BootstrapForm):
    name = FeedbackAuther.name.field.formfield(
        required=False,
        label="Имя",
        help_text="Имя <=  200 символов",
    )
    mail = FeedbackAuther.mail.field.formfield(
        required=False,
        label="Почта",
        help_text="Корректная электронная почта",
    )

    class Meta:
        model = Feedback
        exclude = (
            Feedback.id.field.name,
            Feedback.created_on.field.name,
        )
        labels = {
            Feedback.text.field.name: "Отзыв",
        }
        help_texts = {
            Feedback.text.field.name: "Отзыв <= 250 символов",
        }
