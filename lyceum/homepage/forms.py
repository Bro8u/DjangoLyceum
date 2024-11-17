from django import forms


__all__ = ["FeedbackForm"]


class FeedbackForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        max_length=200,
    )
