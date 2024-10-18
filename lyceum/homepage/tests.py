from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized


class HomepageUrlTests(TestCase):

    @parameterized.expand(
        [
            ("/coffee/", HTTPStatus.IM_A_TEAPOT, "Я чайник"),
            ("/", HTTPStatus.OK, "Главна"),
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
