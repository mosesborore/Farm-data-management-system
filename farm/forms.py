from django import forms
from django.forms.widgets import DateInput

from .models import Farm, Soil


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ["name", "location", "area", "area_unit"]


class SoilForm(forms.ModelForm):
    testing_date = forms.DateField(
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )
    last_testing_date = forms.DateField(
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )
    next_testing_date = forms.DateField(
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )

    class Meta:
        model = Soil
        fields = "__all__"
