from http import HTTPStatus
import unittest

from django.test import Client, override_settings, TestCase
from parameterized import parameterized

from lyceum.middleware import reverse_cyrillic_words


class TestMiddlewareReverse(TestCase):

    @parameterized.expand(
        [
            (
                "/",
                HTTPStatus.OK,
                "Контент не подвезли :( тут можно просить картинку енотика",
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
