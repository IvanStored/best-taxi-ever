from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from star_ratings.models import Rating


class Manufacturer(models.Model):
    name = models.CharField(max_length=63, unique=True)
    country = models.CharField(max_length=63)
    slug = models.SlugField(null=True, blank=True, max_length=70, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Manufacturer, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def get_absolute_url(self):
        return reverse("taxi:manufacturer-detail", kwargs={"slug": self.slug})


class Car(models.Model):
    model = models.CharField(max_length=63, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cars"
    )
    slug = models.SlugField(null=True, unique=True, max_length=70, blank=True)
    ratings = GenericRelation(Rating, related_query_name="cars")

    class Meta:
        ordering = ["-ratings__average"]

    def __str__(self) -> str:
        return str(self.model)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.model)
        return super(Car, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def get_absolute_url(self):
        return reverse("taxi:car-detail", kwargs={"slug": self.slug})


class Driver(AbstractUser):
    avatar = models.ImageField(
        default="default.png",
        null=True,
        blank=True,
        upload_to=settings.MEDIA_ROOT,
    )
    license_number = models.CharField(max_length=8, unique=True)
    slug = models.SlugField(null=True, blank=True, max_length=100, unique=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self) -> str:
        return self.username

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"slug": self.slug})
