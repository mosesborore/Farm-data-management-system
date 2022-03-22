
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView


from .models import InputProduct,InputInventory

from .forms import (
    InputProductForm, InputInventoryForm, InputCategoryForm
)

# Create your views here.
@login_required(login_url='/account/login/')
def input_home(request):
    # products = InputProduct.objects.all()
    # count items per inventory
    inventories = InputInventory.objects.all().annotate(item_count=Count("items"))
    
    context = {
        "inventories": inventories
    }
    return render(request, 'input/index.html', context) 

class Products(ListView):
    template_name = "input/product-list.html"
    
    def get_queryset(self):
        return InputProduct.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = self.get_queryset()
        return context

@require_POST
@login_required(login_url='/account/login/')
def add_product(request):
    form = InputProductForm(request.POST)
    if form.is_valid():
        print(request.POST)
        form.save()
        messages.success(request, "new product added successfully")
    else:
        messages.error(request, form.errors.as_text())
        return render(request, 'input/add-product.html', {"product_form": form}) 
    
    context = {
        "product_form": InputProductForm(),
    }
    return render(request, 'input/add-product.html', context) 