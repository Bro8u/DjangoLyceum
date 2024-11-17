from http import HTTPStatus
import unittest

from django.test import Client, override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized

from lyceum.middleware import reverse_cyrillic_words


__all__ = ["TestReverseCyrillicWords"]


class TestMiddlewareReverse(TestCase):
    @parameterized.expand(
        [
            ("/coffee/", HTTPStatus.IM_A_TEAPOT, "Я чайник", "Я кинйач"),
            (
                reverse("homepage:coffee"),
                HTTPStatus.IM_A_TEAPOT,
                "Я чайник",
                "Я кинйач",
            ),
        ],
    )
    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_on(
        self,
        url,
        expected_status,
        expected_content_1,
        expected_content_2,
    ):
        client = Client()
        for response_number in range(1, 11):
            response = client.get(url)
            if response_number % 10 == 0:
                self.assertContains(
                    response,
                    expected_content_2,
                    status_code=expected_status,
                )
            else:
                self.assertContains(
                    response,
                    expected_content_1,
                    status_code=expected_status,
                )

    @parameterized.expand(
        [
            (reverse("homepage:coffee"), HTTPStatus.IM_A_TEAPOT, "Я чайник"),
            (
                "/coffee/",
                HTTPStatus.IM_A_TEAPOT,
                "Я чайник",
            ),
        ],
    )
    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_off(
        self,
        url,
        expected_status,
        expected_content,
    ):
        client = Client()
        for _response_number in range(1, 11):
            response = client.get(url)
            self.assertContains(
                response,
                expected_content,
                status_code=expected_status,
            )


class TestReverseCyrillicWords(unittest.TestCase):

    def test_reverse_cyrillic_words(self):
        self.assertEqual(
            reverse_cyrillic_words("Привет, мир!"),
            "тевирП, рим!",
        )
        self.assertEqual(
            reverse_cyrillic_words("Тест 1234 тестирование!"),
            "тсеТ 1234 еинаворитсет!",
        )
        self.assertEqual(
            reverse_cyrillic_words("Hello World!"),
            "Hello World!",
        )
        self.assertEqual(
            reverse_cyrillic_words("<body>Код</body>"),
            "<body>доК</body>",
        )
