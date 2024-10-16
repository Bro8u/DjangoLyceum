from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized


class CatalogMain(TestCase):

    @parameterized.expand(
        [
            ("/catalog/", HTTPStatus.OK, "Список элементов"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )


class CatalogID(TestCase):

    @parameterized.expand(
        [
            ("/catalog/5/", HTTPStatus.OK, f"Подробно элемент {5}"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )


class CatalogRegularExpression(TestCase):

    @parameterized.expand(
        [
            ("/catalog/re/123/", HTTPStatus.OK, "123"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )

    @parameterized.expand(
        [
            ("/catalog/re/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/re/-11/", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_status(self, url, expected_status):
        response = Client().get(url)
        self.assertEqual(response.status_code, expected_status)


class CatalogConverter(TestCase):

    @parameterized.expand(
        [
            ("/catalog/converter/123/", HTTPStatus.OK, "123"),
        ]
    )
    def test_status_and_content(self, url, expected_status, expected_content):
        response = Client().get(url)
        self.assertContains(
            response, expected_content, status_code=expected_status
        )

    @parameterized.expand(
        [
            ("/catalog/converter/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/0/", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/-11/", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_status(self, url, expected_status):
        response = Client().get(url)
        self.assertEqual(response.status_code, expected_status)
