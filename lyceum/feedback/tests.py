from django.test import TestCase
from django.urls import reverse

from feedback.forms import FeedbackAutherForm, FeedbackForm
from feedback.models import Feedback, FeedbackAuther


__all__ = ["FeedbackFormTest"]


class FeedbackFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()
        cls.auther_form = FeedbackAutherForm()

    def test_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_name_help_text(self):
        name_help_text = FeedbackFormTest.auther_form.fields["name"].help_text
        self.assertEqual(name_help_text, "Имя <= 200 символов")

    def test_name_label(self):
        name_label = FeedbackFormTest.auther_form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_text_label(self):
        text_label = FeedbackFormTest.form.fields["text"].label
        self.assertEqual(text_label, "Отзыв")

    def test_text_help_text(self):
        text_help_text = FeedbackFormTest.form.fields["text"].help_text
        self.assertEqual(text_help_text, "Отзыв <= 200 символов")

    def test_email_label(self):
        email_label = FeedbackFormTest.auther_form.fields["mail"].label
        self.assertEqual(email_label, "Почта")

    def test_email_help_text(self):
        email_help_text = FeedbackFormTest.auther_form.fields["mail"].help_text
        self.assertEqual(email_help_text, "Корректная электронная почта")

    def test_feedback_auther_form_creates_model_instance(self):
        form_data = {
            "name": "Тестовый отзыв",
            "text": "Превосходно",
            "mail": "test@example.com",
        }
        self.assertFalse(
            FeedbackAuther.objects.filter(
                name="Тестовый отзыв",
                mail="test@example.com",
            ).exists(),
        )
        initial_count = Feedback.objects.count()

        self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(Feedback.objects.count(), initial_count + 1)

        self.assertTrue(
            FeedbackAuther.objects.filter(
                name="Тестовый отзыв",
                mail="test@example.com",
            ).exists(),
        )

    def test_redirect(self):
        form_data = {
            "name": "Тестовый отзыв",
            "text": "Превосходно",
            "mail": "test@example.com",
        }

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

        self.assertContains(response, "Фидбек отправлен. Спасибо!")

    def test_feedback_form_fail_creates_model_instance(self):
        form_data = {
            "name": "Неправильный отзыв",
            "text": "Ужас",
            "mail": "badtestbad.com",
        }

        initial_count = Feedback.objects.count()

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertTrue(response.context["form"].has_error("mail"))

        self.assertEqual(Feedback.objects.count(), initial_count)
