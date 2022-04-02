from django import forms
from django.forms.widgets import DateInput

from account.models import Worker
from input.models import InputProduct

from .models import FarmTask


class CustomManyToManyInput(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        """from: https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024"""
        return "%s" % obj.name


class WorkerCustomManyToManyInput(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        """from: https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024"""
        return "%s %s" % (obj.first_name, obj.last_name)


class FarmTaskForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )
    deadline = forms.DateField(
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=("%Y-%m-%d",),
    )
    # products = CustomManyToManyInput(
    # 	queryset = InputProduct.objects.all(),
    # 	widget=forms.CheckboxSelectMultiple
    # )
    workers = WorkerCustomManyToManyInput(
        queryset=Worker.objects.all(),
    )

    class Meta:
        model = FarmTask
        exclude = ("curreny", "updated_on", "created_by")
