from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized


class AboutUrlTestsContent(TestCase):
    @parameterized.expand(
        [
            ("/about/", HTTPStatus.OK, "О нас"),
            ("/about/", HTTPStatus.OK, "Информация о компании..."),
            (
                "/",
                HTTPStatus.OK, '<nav class="navbar navbar-expand-lg"'
            ),
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
