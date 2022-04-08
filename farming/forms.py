from django import forms

from .models import Crop, FarmingSeason, FarmingStage


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = "__all__"


class FarmingSeasonForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )

    class Meta:
        model = FarmingSeason
        fields = "__all__"


class FarmingStageForm(forms.ModelForm):
    class Meta:
        model = FarmingStage
        fields = "__all__"
