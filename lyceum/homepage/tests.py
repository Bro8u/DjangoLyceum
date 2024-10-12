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

    def test_homepage_coffee_url(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, 418)

    def test_homepage_coffee_url_by_name(self):
        url = reverse("coffee")
        response = Client().get(url)
        self.assertEqual(response.status_code, 418)

    def test_homepage_coffee_content(self):
        response = Client().get("/coffee/")
        self.assertContains(response, "Я чайник", status_code=418)
