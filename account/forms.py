from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from .models import Farmer, Login, Worker


class SignUpForm(UserCreationForm):
    class Meta:
        model = Login
        fields = (
            "username",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    pass


class FarmerForm(ModelForm):
    class Meta:
        model = Farmer
        fields = [
            "first_name",
            "last_name",
            "national_id",
            "phone_no",
        ]


class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "national_id", "phone_no"]
