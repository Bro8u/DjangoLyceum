from django.test import TestCase
from django.urls import reverse


class CatalogUrlTests(TestCase):
    def test_about_url(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_about_url_by_name(self):
        url = reverse("description")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_about_content(self):
        response = self.client.get("/about/")
        self.assertContains(response, "О проекте")
