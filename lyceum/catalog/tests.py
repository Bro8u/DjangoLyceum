from django.test import TestCase
from django.urls import reverse


class CatalogUrlTests(TestCase):

    def setUp(self):
        self.default_id = 5

    def test_item_list_url(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_item_list_url_by_name(self):
        url = reverse("item_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_item_list_content(self):
        response = self.client.get("/catalog/")
        self.assertContains(response, "Список элементов")

    def test_item_detail_url(self):
        url = reverse("item_detail", args=[self.default_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_item_detail_content(self):
        url = reverse("item_detail", args=[self.default_id])
        response = self.client.get(url)
        self.assertContains(response, f"Подробно элемент {self.default_id}")
