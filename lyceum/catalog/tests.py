from django.test import Client, TestCase
from django.urls import reverse


class CatalogMain(TestCase):

    def test_item_list_url(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_item_list_url_by_name(self):
        url = reverse("item_list")
        response = Client().get(url)
        self.assertEqual(response.status_code, 200)

    def test_item_list_content(self):
        response = Client().get("/catalog/")
        self.assertContains(response, "Список элементов")


class CatalogID(TestCase):

    def test_item_detail_url(self):
        response = Client().get("/catalog/5/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_content(self):
        response = Client().get("/catalog/5/")
        self.assertContains(response, f"Подробно элемент {5}")


class CatalogRegularExpression(TestCase):

    def test_reqular_expression_url(self):
        response = Client().get("/catalog/re/123/")
        self.assertEqual(response.status_code, 200)

    def test_reqular_expression_url_by_name(self):
        url = reverse("reqular_expression", args=[123])
        response = Client().get(url)
        self.assertEqual(response.status_code, 200)

    def test_reqular_expression_number(self):
        response = Client().get("/catalog/re/123/")
        self.assertContains(response, "123")

    def test_reqular_expression_number_not_empty(self):
        response = Client().get("/catalog/re/")
        self.assertEqual(response.status_code, 404)

    def test_reqular_expression_not_zero(self):
        response = Client().get("/catalog/re/0")
        self.assertEqual(response.status_code, 404)

    def test_reqular_expression_not_negative(self):
        response = Client().get("/catalog/re/-11")
        self.assertEqual(response.status_code, 404)


class CatalogConverter(TestCase):

    def test_converter_url(self):
        response = Client().get("/catalog/converter/123/")
        self.assertEqual(response.status_code, 200)

    def test_converter_url_by_name(self):
        url = reverse("converter", args=[123])
        response = Client().get(url)
        self.assertEqual(response.status_code, 200)

    def test_converter_number(self):
        response = Client().get("/catalog/converter/123/")
        self.assertContains(response, "123")

    def test_converter_number_not_empty(self):
        response = Client().get("/catalog/converter/")
        self.assertEqual(response.status_code, 404)

    def test_converter_number_not_zero(self):
        response = Client().get("/catalog/converter/0")
        self.assertEqual(response.status_code, 404)

    def test_converter_number_not_negative(self):
        response = Client().get("/catalog/converter/-11")
        self.assertEqual(response.status_code, 404)
