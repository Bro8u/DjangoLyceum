from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized


class CatalogUrlTests(TestCase):
    @parameterized.expand(
        [
            ("/about/", HTTPStatus.OK, "О проекте"),
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
