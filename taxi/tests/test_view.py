from django.test import TestCase, Client
from django.urls import reverse


DRIVER_URL = reverse("taxi:driver-list")


class DriverPublicLoginTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)
