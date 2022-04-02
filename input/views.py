from email import message

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django_prices.models import MoneyField

from .forms import (
    InputCategoryForm,
    InputInventoryForm,
    InputInventoryItemForm,
    InputProductForm,
)
from .models import InputInventory, InputProduct


# Create your views here.
@login_required(login_url="/account/login/")
def input_home(request):
    # products = InputProduct.objects.all()
    # count items per inventory
    inventories = InputInventory.objects.prefetch_related("items").annotate(
        item_count=Count("items")
    )

    context = {"inventories": inventories}
    return render(request, "input/index.html", context)


@login_required(login_url="/account/login")
def delete_inventory(request, ref_code):
    delete = request.POST.get("delete")

    if delete:
        # if the checkbox is checked
        inventory = get_object_or_404(InputInventory, ref_code=ref_code)
        name = inventory.name
        inventory.delete()
        messages.success(request, f"{name} delete successfully")
    else:
        messages.info(
            request,
            _("If you want to delete the record, make sure the checkbox is checked"),
        )
    return redirect("input:input_home")


@login_required(login_url="/account/login/")
def inventory_item_list(request, ref_code):

    try:
        inventory = get_object_or_404(InputInventory, ref_code=ref_code)
        items = inventory.items.select_related("input_product").all()

        if request.method == "POST":
            new_item_form = InputInventoryItemForm(request.POST)
            if new_item_form.is_valid():
                new_item_form.save()
                messages.success(request, "New Inventory added successfully")
            else:
                messages.error(request, new_item_form.errors.as_ul())
        if request.method == "DELETE":
            print("delete meho")

    except Http404:
        messages.error(
            request, f'Inventory with reference code: "{ref_code}" does not exist'
        )
        return redirect("input:input_home")

    form = InputInventoryItemForm()

    context = {
        "items": items,
        "inventory_name": inventory.name,
        "ref_code": ref_code,
        "currency": "KSH",
        "form": form,
        "inventory_total_cost": inventory.get_total_cost(),
    }
    return render(request, "input/inventory-item-list.html", context)


class Products(LoginRequiredMixin, ListView):
    template_name = "input/product-list.html"

    def get_queryset(self):
        return InputProduct.objects.all()

    def get_unit_measurement_options(self):
        return (
            ("KG", _("kilograms")),
            ("G", _("grams")),
            ("L", _("liter")),
            ("BAG", _("bag")),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["products"] = self.get_queryset()
        context["product_form"] = InputProductForm()
        context["unit_measurement"] = self.get_unit_measurement_options()
        return context


@require_POST
@login_required(login_url="/account/login/")
def add_product(request):
    form = InputProductForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "new product added successfully")
    else:
        messages.error(request, form.errors.as_text())

    return redirect("input:product-list")


@require_POST
@login_required(login_url="/account/login/")
def edit_product(request, pk):
    product = get_object_or_404(InputProduct, pk=pk)
    form = InputProductForm(request.POST or None, instance=product)
    if form.is_valid():
        name = request.POST.get("name")
        form.save()
        messages.success(request, f"{name} updated successfully")
    else:
        messages.error(request, form.errors.as_text())

    return redirect("input:product-list")


@require_POST
@login_required(login_url="/account/login/")
def delete_product(request, pk):
    try:
        delete = request.POST.get("delete", None)
        if delete:
            # if the checkbox is checked
            product = get_object_or_404(InputProduct, pk=pk)
            name = product.name
            product.delete()
            messages.success(request, f"{name} delete successfully")
        else:
            messages.info(
                request,
                _(
                    "If you want to delete the record, make sure the checkbox is checked"
                ),
            )
        return redirect("input:product-list")
    except InputProduct.DoesNotExist:
        messages.error(request, "Product with that name does not exist. Try again")
