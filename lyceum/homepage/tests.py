from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from feedback.forms import FeedbackForm
from feedback.models import Feedback
from parameterized import parameterized


import catalog.models


__all__ = []


class HomepageUrlTests(TestCase):
    @parameterized.expand(
        [
            ("/"),
            (reverse("homepage:homepage")),
        ],
    )
    def test_rendered_file(
        self,
        url,
    ):
        response = Client().get(url)
        self.assertTemplateUsed(response, "homepage/home.html")

    @parameterized.expand(
        [
            (
                reverse("homepage:homepage"),
                HTTPStatus.OK,
                'img src="/static/images/logo.png"',
            ),
            ("/", HTTPStatus.OK, 'img src="/static/images/logo.png"'),
            ("/", HTTPStatus.OK, 'img src="/static/images/logo.png"'),
            ("/", HTTPStatus.OK, '<nav class="navbar navbar-expand-lg"'),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )


class CoffeeUrlContentTest(TestCase):
    @parameterized.expand(
        [
            ("/coffee/", HTTPStatus.IM_A_TEAPOT, "Я чайник"),
            (reverse("homepage:coffee"), HTTPStatus.IM_A_TEAPOT, "Я чайник"),
        ],
    )
    def test_status_and_content(
        self,
        url,
        expected_status,
        expected_content,
    ):
        response = Client().get(url)
        self.assertContains(
            response,
            expected_content,
            status_code=expected_status,
        )


class Checker(TestCase):
    def check(
        self,
        item,
        exist,
        prefetched,
        not_loaded,
    ):
        item_dict = item.__dict__
        for value in exist:
            self.assertIn(value, item_dict)

        for value in prefetched:
            self.assertIn(value, item_dict["_prefetched_objects_cache"])

        for value in not_loaded:
            self.assertNotIn(value, item_dict)


class ItemMainContext(Checker):
    fixtures = ["data.json"]

    def test_type(self):
        response = Client().get("/")
        for item in response.context["items"]:
            self.assertIsInstance(item, catalog.models.Item)

    def test_item_size(self):
        response = Client().get("/")
        self.assertEqual(len(response.context["items"]), 0)

    def test_loaded_value(self):
        response = Client().get("/")
        for item in response.context["items"]:
            self.check(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_on_main",
                    "image",
                    "is_published",
                ),
            )

            self.check(
                item.tags.all()[0],
                ("name",),
                (),
                ("is_published"),
            )


class FeedbackFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_context(self):
        response = self.client.get(reverse("homepage:echo"))
        self.assertIn("form", response.context)

    def test_text_label(self):
        text_label = FeedbackFormTest.form.fields["text"].label
        self.assertEqual(text_label, "Отзыв")

    def test_text_help_text(self):
        text_help_text = FeedbackFormTest.form.fields["text"].help_text
        self.assertEqual(text_help_text, "Отзыв <= 100 символов")

    def test_feedback_form_creates_model_instance(self):
        form_data = {
            "text": "Превосходно",
        }
        self.assertFalse(
            Feedback.objects.filter(
                text="Превосходно",
            ).exists(),
        )
        initial_count = Feedback.objects.count()

        self.client.post(
            reverse("homepage:echo_submit"),
            data=form_data,
        )

        self.assertEqual(Feedback.objects.count(), initial_count + 1)

        self.assertTrue(
            Feedback.objects.filter(
                text="Превосходно",
            ).exists(),
        )
