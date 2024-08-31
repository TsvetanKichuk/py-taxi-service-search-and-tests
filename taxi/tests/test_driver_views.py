from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Driver, Car, Manufacturer


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create(username=self.client)
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        self.car = Car.objects.create(model='Test Car', manufacturer=self.manufacturer)
        self.client.login(username='testuser', password='12345')
        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add(self):
        response = self.client.post(reverse('taxi:toggle-car-assign', args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('taxi:car-detail', args=[self.car.id]))
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        response = self.client.post(reverse('taxi:toggle-car-assign', args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('taxi:car-detail', args=[self.car.id]))
        self.assertNotIn(self.car, self.user.cars.all())


class DriverListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create(username=self.client)
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer2")
        self.car = Car.objects.create(model='Test Car', manufacturer=self.manufacturer)
        self.client.login(username='testuser2', password='123456')
        self.client.force_login(self.user)

    def test_get_context_data(self):
        client = Client()
        response = client.get("/username/")  # Assuming URL pattern
        context = response.context

        self.assertIsInstance(context["search_form"], DriverSearchForm)
        self.assertEqual(context["search_form"].initial["username"], "")

    # def test_get_queryset_no_username(self):
    #     client = Client()
    #     response = client.get("/drivers/")
    #     queryset = response.context["driver_list"]
    #
    #     self.assertEqual(queryset.count(), 2)  # Assuming two drivers in the database

    def test_get_queryset_with_username(self):
        client = Client()
        response = client.get("/drivers/?username=driver1")
        queryset = response.context["driver_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].username, "driver1")

    def test_pagination(self):
        client = Client()
        response = client.get("/drivers/")
        queryset = response.context["driver_list"]

        self.assertEqual(queryset.count(), 2)  # Assuming two drivers in the database
        self.assertEqual(queryset.paginator.num_pages, 2)

    def test_prefetch_related(self):
        client = Client()
        response = client.get("/drivers/")
        driver = response.context["driver_list"][0]

        self.assertQuerysetEqual(
            driver.cars.all(),
            [('Car 1',), ('Car 2',)],
            transform=lambda x: (x.model,)
        )

        # Ensure prefetching is working correctly
        self.assertNumQueries(1, lambda: driver.cars.all()[0].manufacturer.name)
