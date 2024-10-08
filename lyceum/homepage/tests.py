from django.test import Client, TestCase
from django.urls import reverse


class HomepageUrlTests(TestCase):
    def test_homepage_url(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_by_name(self):
        url = reverse("home")
        response = Client().get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        response = Client().get("/")
        self.assertContains(response, "Главная")
