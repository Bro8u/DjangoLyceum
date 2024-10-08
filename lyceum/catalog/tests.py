from django.test import TestCase, Client
from django.urls import reverse


class CatalogUrlTests(TestCase):

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

    def test_item_detail_url(self):
        response = Client().get("/catalog/5/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_content(self):
        response = Client().get("/catalog/5/")
        self.assertContains(response, f"Подробно элемент {5}")
