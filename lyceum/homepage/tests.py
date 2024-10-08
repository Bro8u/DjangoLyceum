from django.test import TestCase
from django.urls import reverse


class HomepageUrlTests(TestCase):
    def test_homepage_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_by_name(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        response = self.client.get("/")
        self.assertContains(response, "Главная")
