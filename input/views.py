from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import InputCategoryForm, InputInventoryForm, InputProductForm
from .models import InputInventory, InputProduct


# Create your views here.
@login_required(login_url="/account/login/")
def input_home(request):
    # products = InputProduct.objects.all()
    # count items per inventory
    inventories = InputInventory.objects.all().annotate(item_count=Count("items"))

    context = {"inventories": inventories}
    return render(request, "input/index.html", context)


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
        print(request.POST)
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
