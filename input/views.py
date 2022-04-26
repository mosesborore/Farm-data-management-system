from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import (
    InputCategoryForm,
    InputInventoryForm,
    InputInventoryItemForm,
    InputProductForm,
)
from .models import InputCategory, InputInventory, InputInventoryItem, InputProduct


# Create your views here.
@login_required(login_url="/account/login/")
def input_home(request):
    # products = InputProduct.objects.all()
    # count items per inventory
    inventories = InputInventory.objects.annotate(item_count=Count("items"))

    if request.method == "POST":
        # add new inventory
        form = InputInventoryForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"inventories": inventories, "form": InputInventoryForm()}
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
                quantity = request.POST.get("quantity")
                product_pk = request.POST.get("input_product")

                product = get_object_or_404(InputProduct, pk=product_pk)
                product_name = product.name
                try:
                    # decrease the product quantity
                    product.decrease_unit(quantity)
                    
                    new_item_form.save()
                    messages.success(request, "New Inventory added successfully")
                except Exception:
                    messages.error(request, f'Cannot add item. The available quantity for "{product_name}" is zero. Please refill')
            else:
                messages.error(request, new_item_form.errors.as_ul())

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


def edit_inventory_item(request, ref_code, pk):
    item = get_object_or_404(InputInventoryItem, input_inventory__ref_code=ref_code, pk=pk)

    item_product = item.input_product
    if request.method == "POST":
        form = InputInventoryItemForm(request.POST or None, instance=item)
        
        quantity = int(request.POST.get('quantity'))
        initial_quantity = item.quantity
        
        # for instance, b4 quantity was 5 and now quantity is 8
        # meaning the quantity has been increased by 3 (8-5)
        requested_quantity = quantity - initial_quantity
        
        # quantity is not updated
        if item.quantity == quantity:
            if form.is_valid():
                form.save()
                messages.error(request, f"Item details updated successfully")
                return redirect('input:inventory-item-list', ref_code)
            else:
                messages.error(request, form.errors.as_text)
        # quantity has been updated
        # if the requested quantity is greater than the available product quantity
        elif item_product.available_units < int(requested_quantity):
            rem = item_product.available_units
            messages.error(request, f'Unable to allocate the request quantity. Remaining quantity for product: "{item_product.name}" is {rem}')
        elif item_product.available_units >= int(requested_quantity):
            if form.is_valid():
                # get the product and decrease it quantity
                product = get_object_or_404(InputProduct, pk=item_product.id)
                product.decrease_unit(requested_quantity)
                form.save()
                messages.error(request, f"Item details updated successfully")
                return redirect('input:inventory-item-list', ref_code)
            else:
                messages.error(request, form.errors.as_text)
                
    form = InputInventoryItemForm(instance=item)
    context = {
        "form": form,
        "name": item_product.name
    }
    return render(request, "input/edit-item.html", context)
    

@require_POST
@login_required(login_url="/account/login/")
def delete_inventory_item(request, ref_code, pk):
    inventory = get_object_or_404(InputInventory, ref_code=ref_code)

    if request.method == "POST":
        delete = request.POST.get("delete", None)
        print(delete)
        if delete:
            # delete on the item not the product
            item = inventory.items.filter(pk=pk)
            item.delete()
            messages.success(request, "Inventory item deleted successfully")
        else:
            messages.info(
                request,
                _("If you want to delete the item, make sure the checkbox is checked"),
            )
    return redirect("input:inventory-item-list", ref_code)


class Products(LoginRequiredMixin, ListView):
    template_name = "input/product-list.html"

    def get_queryset(self):
        return InputProduct.objects.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["products"] = self.get_queryset()
        context["product_form"] = InputProductForm()
        context["category_form"] = InputCategoryForm()
        return context


@require_POST
@login_required(login_url="/account/login/")
def add_product(request):
    form = InputProductForm(request.POST)
    if form.is_valid():
        units = request.POST.get("total_units")
        product = form.save(commit=False)

        # add initial available units
        product.available_units = units
        product.save()
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


@require_POST
@login_required(login_url="/account/login/")
def add_category(request):
    if request.method == "POST" or request.is_ajax():
        form = InputCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            stage = get_object_or_404(InputCategory, name=request.POST.get("name"))

        context = {"data": [{"name": stage.name, "id": stage.id}]}
    return JsonResponse(context)
