from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class FormsTests(TestCase):
    def test_driver_license_update(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "Test licence",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
