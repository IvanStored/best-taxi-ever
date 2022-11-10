from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverDetailView,
    DriverCreateView,
    DriverDeleteView,
    DriverUpdateView,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    assign_to_car,
    delete_from_car,
    Register,
    SettingsUpdateView,
    contact,
    ManufacturerDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<slug:slug>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<slug:slug>/detail/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),
    path(
        "manufacturers/<slug:slug>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<slug:slug>/", CarDetailView.as_view(), name="car-detail"),
    path(
        "cars/<slug:slug>/assign-to-car/", assign_to_car, name="assign-to-car"
    ),
    path(
        "cars/<slug:slug>/delete-from-car/",
        delete_from_car,
        name="delete-from-car",
    ),
    path(
        "cars/<slug:slug>/update/", CarUpdateView.as_view(), name="car-update"
    ),
    path(
        "cars/<slug:slug>/delete/", CarDeleteView.as_view(), name="car-delete"
    ),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    path(
        "drivers/<slug:slug>/",
        DriverDetailView.as_view(),
        name="driver-detail",
    ),
    path(
        "drivers/<slug:slug>/delete/",
        DriverDeleteView.as_view(),
        name="driver-delete",
    ),
    path(
        "drivers/<slug:slug>/update/",
        DriverUpdateView.as_view(),
        name="driver-update",
    ),
    path(
        "drivers/<slug:slug>/settings/",
        SettingsUpdateView.as_view(),
        name="driver-settings",
    ),
    path("register/", Register.as_view(), name="register"),
    path("contact/", contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "taxi"
