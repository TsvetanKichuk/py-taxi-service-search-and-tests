from django.test import TestCase, Client

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car


class CarListViewTest(TestCase):
    def setUp(self):
        # Create test data
        manufacturer1 = Manufacturer.objects.create(name="Manufacturer 1")
        manufacturer2 = Manufacturer.objects.create(name="Manufacturer 2")
        car1 = Car.objects.create(model="Car 1", manufacturer=manufacturer1)
        car2 = Car.objects.create(model="Car 2", manufacturer=manufacturer2)

    def test_get_context_data(self):
        client = Client()
        response = client.get("/cars/")  # Assuming URL pattern
        context = response.context

        self.assertIsInstance(context["search_form"], CarSearchForm)
        self.assertEqual(context["search_form"].initial["model"], "")

    def test_get_queryset_no_model(self):
        client = Client()
        response = client.get("/cars/")
        queryset = response.context["car_list"]

        self.assertEqual(queryset.count(), 2)  # Assuming two cars in the database

    def test_get_queryset_with_model(self):
        client = Client()
        response = client.get("/cars/?model=Car 1")
        queryset = response.context["car_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].model, "Car 1")

    def test_pagination(self):
        client = Client()
        response = client.get("/cars/")
        queryset = response.context["car_list"]

        self.assertEqual(queryset.count(), 2)  # Assuming two cars in the database
        self.assertEqual(queryset.paginator.num_pages, 2)

    def test_select_related(self):
        client = Client()
        response = client.get("/cars/")
        car = response.context["car_list"][0]

        # Ensure select_related is working correctly
        self.assertNumQueries(1, lambda: car.manufacturer.name)