from django.test import TestCase
from django.urls import reverse
from feedback.forms import FeedbackForm
from feedback.models import FeedbackFormModel


__all__ = ["FeedbackFormTest"]


class FeedbackFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_name_help_text(self):
        name_help_text = FeedbackFormTest.form.fields["name"].help_text
        self.assertEqual(name_help_text, "Имя <= 20 символов")

    def test_name_label(self):
        name_label = FeedbackFormTest.form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_text_label(self):
        text_label = FeedbackForm().fields["text"].label
        self.assertEqual(text_label, "Отзыв")

    def test_text_help_text(self):
        text_help_text = FeedbackForm().fields["text"].help_text
        self.assertEqual(text_help_text, "Отзыв <= 100 символов")

    def test_email_label(self):
        email_label = FeedbackForm().fields["email"].label
        self.assertEqual(email_label, "Почта")

    def test_email_help_text(self):
        email_help_text = FeedbackForm().fields["email"].help_text
        self.assertEqual(email_help_text, "Корректная электронная почта")

    def test_feedback_form_creates_model_instance(self):
        form_data = {
            "name": "Тестовый отзыв",
            "text": "Превосходно",
            "email": "test@example.com",
        }
        self.assertFalse(
            FeedbackFormModel.objects.filter(
                name="Тестовый отзыв",
            ).exists(),
        )
        initial_count = FeedbackFormModel.objects.count()

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse("feedback:feedback"))

        self.assertEqual(FeedbackFormModel.objects.count(), initial_count + 1)

        self.assertTrue(
            FeedbackFormModel.objects.filter(
                name="Тестовый отзыв",
            ).exists(),
        )

    def test_feedback_form_fail_creates_model_instance(self):
        form_data = {
            "name": "Неправильный отзыв",
            "text": "Ужас",
            "email": "badtestbad.com",
        }

        initial_count = FeedbackFormModel.objects.count()

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(FeedbackFormModel.objects.count(), initial_count)
