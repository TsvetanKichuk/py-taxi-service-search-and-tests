from django.test import TestCase

from taxi.models import Car


class ModelTest(TestCase):
    def test_model(self):
        obj = Car.objects.create(model="Test model", manufacturer="test manufacturer")
        self.assertEqual(str(obj), obj)
