from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.forms import FileInput

from taxi.models import Car, Manufacturer


class LicenseMixin(forms.ModelForm):
    LETTERS = 3
    NUMBERS = 5
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                rf"^[A-Z]{{{LETTERS}}}[0-9]{{{NUMBERS}}}$",
                message=f"License number must consist "
                f"first {LETTERS} uppercase letters and "
                f"last {NUMBERS} digits",
            )
        ],
    )


class DriverForm(LicenseMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "avatar",
        )


class SettingsForm(forms.ModelForm):

    avatar = forms.FileField(widget=FileInput, label="")

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "avatar",
        )


class ContactForm(forms.Form):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your name"}),
        label="",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Email"}),
        label="",
    )
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Subject"}),
        label="",
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Message:"}),
        required=True,
        label="",
    )


class DriverLicenseUpdate(LicenseMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class ManufacturerForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        label=False,
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
    country = forms.CharField(
        max_length=255,
        label=False,
        widget=forms.TextInput(attrs={"placeholder": "Country"}),
    )

    class Meta:
        model = Manufacturer
        fields = "__all__"


class CarSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by model or country...",
                "type": "search",
                "id": "form1",
            }
        ),
    )


class ManufacturerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name or country..."}
        ),
    )


class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."}),
    )
