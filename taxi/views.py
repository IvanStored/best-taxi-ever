import sweetify
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    DriverForm,
    DriverLicenseUpdate,
    CarForm,
    ManufacturerForm,
    SettingsForm,
    ContactForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
)
from .models import Driver, Car, Manufacturer


from sweetify.views import SweetifySuccessMixin


class StaffRequiredMixin(SweetifySuccessMixin):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            sweetify.error(
                request, "Ooops, you not allowed to do this", icon="error"
            )
            return HttpResponseRedirect("/")

        return super(StaffRequiredMixin, self).get(request, *args, **kwargs)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5
    queryset = model.objects.all()
    template_name = "taxi/manufacturer_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        context["form"] = ManufacturerForm()
        search = self.request.GET.get("search", "")
        context["search_form"] = ManufacturerSearchForm(
            initial={"search": search}
        )
        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["search"]
            return self.queryset.filter(
                Q(name__icontains=query) | Q(country__icontains=query)
            )
        return self.queryset


class ManufacturerCreateView(StaffRequiredMixin, generic.CreateView):
    model = Manufacturer
    form_class = ManufacturerForm

    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was created!"


class ManufacturerUpdateView(StaffRequiredMixin, generic.UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was updated!"


class ManufacturerDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = Manufacturer

    def get_success_url(self):
        sweetify.success(self.request, "Manufacturer was deleted")
        return reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search_form"] = CarSearchForm(initial={"search": search})
        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                Q(model__icontains=form.cleaned_data["search"])
                | Q(
                    manufacturer__country__icontains=form.cleaned_data[
                        "search"
                    ]
                )
            )
        return self.queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer
    queryset = Manufacturer.objects.all()


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(StaffRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car was created!"


class CarUpdateView(StaffRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car was updated!"


class CarDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car was deleted"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DriverSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = DriverSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


class DriverCreateView(StaffRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "Driver was created!"


class DriverDeleteView(StaffRequiredMixin, generic.DeleteView):
    model = get_user_model()
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "Driver was deleted"


class DriverUpdateView(SweetifySuccessMixin, generic.UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdate
    success_message = "License number was successfully updated!"

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super(DriverUpdateView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(DriverUpdateView, self).get(request, *args, **kwargs)
        sweetify.error(
            request, "Ooops, you not allowed to do this", icon="error"
        )
        return HttpResponseRedirect("/")


class SettingsUpdateView(SweetifySuccessMixin, generic.UpdateView):

    model = get_user_model()
    form_class = SettingsForm
    success_message = "Driver was updated!"

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super(SettingsUpdateView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(SettingsUpdateView, self).get(
                request, *args, **kwargs
            )
        sweetify.error(
            request, "Ooops, you not allowed to do this", icon="error"
        )
        return HttpResponseRedirect("/")


def assign_to_car(request, slug):
    car = Car.objects.get(slug=slug)
    car.drivers.add(request.user.id)
    car.save()
    return HttpResponseRedirect(
        reverse_lazy("taxi:car-detail", kwargs={"slug": slug})
    )


def delete_from_car(request, slug):
    car = Car.objects.get(slug=slug)
    car.drivers.remove(request.user.id)
    car.save()
    return HttpResponseRedirect(
        reverse_lazy("taxi:car-detail", kwargs={"slug": slug})
    )


class Register(generic.CreateView):
    template_name = "registration/register.html"
    model = get_user_model()
    form_class = DriverForm

    def get(self, request, *args, **kwargs):
        context = {"form": DriverForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = DriverForm(request.POST or None, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            sweetify.success(request, f"Welcome to our site, {user.username}")
            return HttpResponseRedirect(reverse_lazy("taxi:index"))
        context = {"form": form}
        return render(request, self.template_name, context)


@login_required
def contact(request):
    if request.method == "GET":
        name = request.user.first_name if request.user.first_name else None
        email = request.user.email if request.user.email else None
        form_data = {
            "name": name,
            "email": email,
        }
        form = ContactForm(initial=form_data)
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            form_data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "subject": subject,
                "message": message,
            }
            message = """
                    From:\n\t\t{}\n
                    Message:\n\t\t{}\n
                    Email:\n\t\t{}\n
                    Subject:\n\t\t{}\n
                    """.format(
                form_data["name"],
                form_data["message"],
                form_data["email"],
                form_data["subject"],
            )

            try:
                send_mail(
                    "You got a mail!", message, "", ["jus1stored@gmail.com"]
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            sweetify.success(request, "Thank you for feedback!")
            return redirect("/")
    return render(request, "email.html", {"form": form})
