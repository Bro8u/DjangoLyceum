from django.test import Client, override_settings, TestCase


class TestMiddlewareReverse(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_on(self):
        client = Client()
        for response_number in range(1, 11):
            response = client.get("/")
            if response_number % 10 == 0:
                self.assertContains(response, "яанвалГ".encode("utf-8"))
            else:
                self.assertContains(response, "Главная".encode("utf-8"))

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_off(self):
        client = Client()
        for _response_number in range(1, 11):
            response = client.get("/")
            self.assertContains(response, "Главная".encode("utf-8"))
