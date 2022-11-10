from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverLicenseUpdate,
    DriverForm,
    ContactForm,
)
from taxi.models import Car, Manufacturer


class DriverFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "BHJ12345",
            "avatar": "default.png",
        }
        form = DriverForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):

        form_data = {"license_number": "NJK12345"}
        form = DriverLicenseUpdate(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_settings_update_form(self):
        response = self.client.post(
            reverse("taxi:driver-settings", kwargs={"slug": self.user.slug}),
            data={"first_name": "test", "last_name": "test"},
        )
        self.assertEqual(response.status_code, 302)


class SearchFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )

        self.client.force_login(self.user)

    def test_driver_search_by_username(self):
        get_user_model().objects.create_user(
            username="test.username",
            license_number="TSS23345",
            first_name="TEST",
            last_name="USER",
            password="test",
        )
        response = self.client.get(reverse("taxi:driver-list") + "?username=t")
        drivers = get_user_model().objects.filter(username__icontains="t")

        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertEqual(len(response.context["driver_list"]), len(drivers))

    def test_car_search_by_model(self):

        Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create(
                name="test", country="test"
            ),
        )
        response = self.client.get(reverse("taxi:car-list") + "?search=t")
        cars = Car.objects.filter(model__icontains="t")

        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertEqual(len(response.context["car_list"]), len(cars))

    def test_car_search_by_country(self):
        manufacturer = Manufacturer.objects.create(name="zaz", country="test")

        Car.objects.create(model="mazda", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list") + "?search=t")
        cars = Car.objects.filter(manufacturer__country__icontains="t")

        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertEqual(len(response.context["car_list"]), len(cars))

    def test_car_search_by_manufacturer(self):

        manufacturer = Manufacturer.objects.create(name="zaz", country="test")

        Car.objects.create(model="mazda", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list") + "?search=a")
        cars = Car.objects.filter(manufacturer__name__icontains="a")

        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertEqual(len(response.context["car_list"]), len(cars))

    def test_manufacturer_search_by_name(self):

        Manufacturer.objects.create(name="Daewoo", country="Ukraine")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=w"
        )

        manufacturers = Manufacturer.objects.filter(name__icontains="w")

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]), len(manufacturers)
        )

    def test_manufacturer_search_by_country(self):
        Manufacturer.objects.create(name="Daewoo", country="Ukraine")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search=u"
        )

        manufacturers = Manufacturer.objects.filter(country__icontains="u")

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]), len(manufacturers)
        )


class ContactFormSearch(TestCase):
    def test_contact_form(self):

        form_data = {
            "name": "test",
            "email": "asd@gmail.com",
            "subject": "test",
            "message": "asdsa",
        }

        form = ContactForm(data=form_data)

        self.assertEqual(form.data, form_data)
        self.assertTrue(form.is_valid())
