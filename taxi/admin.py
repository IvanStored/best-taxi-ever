from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from taxi.models import Car, Manufacturer, Driver


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        "model",
        "manufacturer",
        "list_of_drivers",
    ]
    search_fields = ["model"]
    list_filter = ["manufacturer", "manufacturer__country"]
    prepopulated_fields = {"slug": ("model",)}

    @staticmethod
    def list_of_drivers(obj) -> str:
        return ", ".join([driver.username for driver in obj.drivers.all()])


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ["name", "country"]
    list_display = ["name", "country"]
    list_filter = ["country"]


@admin.register(Driver)
class DriverAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "license_number",
        "avatar",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "license_number",
                    "avatar",
                    "slug",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "license_number",
                    "avatar",
                    "slug",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
    )
