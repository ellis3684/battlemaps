from django.test import TestCase, Client


class MapsTestCase(TestCase):
    def test_home(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        client = Client()
        response = client.get("/about/")
        self.assertEqual(response.status_code, 200)
