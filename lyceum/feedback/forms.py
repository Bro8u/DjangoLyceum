import django.forms
from feedback.models import FeedbackFormModel


__all__ = ["FeedbackForm"]


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class FeedbackForm(BootstrapForm):
    class Meta:
        model = FeedbackFormModel
        fields = {
            FeedbackFormModel.name.field.name,
            FeedbackFormModel.text.field.name,
            FeedbackFormModel.email.field.name,
        }
        labels = {
            FeedbackFormModel.name.field.name: "Имя",
            FeedbackFormModel.text.field.name: "Отзыв",
            FeedbackFormModel.email.field.name: "Почта",
        }
        help_texts = {
            FeedbackFormModel.name.field.name: "Имя <= 20 символов",
            FeedbackFormModel.text.field.name: "Отзыв <= 100 символов",
            FeedbackFormModel.email.field.name: "Корректная электронная почта",
        }
