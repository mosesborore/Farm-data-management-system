from django import forms
from django.conf import settings

from .models import InputCategory, InputInventory, InputInventoryItem, InputProduct

AVAILABLE_CURRENCIES = [settings.DEFAULT_CURRENCY]


class InputCategoryForm(forms.ModelForm):
    class Meta:
        model = InputCategory
        fields = "__all__"


class InputProductForm(forms.ModelForm):
    # unit_price = MoneyField(label="Unit Price", available_currencies=AVAILABLE_CURRENCIES)
    class Meta:
        model = InputProduct
        exclude = ("unit_price",)


class InputInventoryForm(forms.ModelForm):
    class Meta:
        model = InputInventory
        fields = "__all__"


class InputInventoryItemForm(forms.ModelForm):
    # total_cost = MoneyField(
    #     label="Total Cost", available_currencies=AVAILABLE_CURRENCIES
    # )

    class Meta:
        model = InputInventoryItem
        fields = "__all__"
