from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized


class HomepageUrlTests(TestCase):
    @parameterized.expand(
        [
            ("/"),
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
            ("/", HTTPStatus.OK, 'img src="/static/images/picture.png"'),
            ("/", HTTPStatus.OK, 'img src="/static/images/logo.png"'),
            ("/", HTTPStatus.OK, 'img src="/static/images/logo.png"'),
            (
                "/",
                HTTPStatus.OK,
                '<nav class="navbar navbar-expand-lg"'
                'style="background-color: #f8f9fa; padding: 15px;">',
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


class CoffeeUrlContentTest(TestCase):
    @parameterized.expand(
        [
            ("/coffee/", HTTPStatus.IM_A_TEAPOT, "Я чайник"),
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
