from email import message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import InputProduct


from .forms import (
    InputProductForm, InputInventoryForm, InputCategoryForm
)


# Create your views here.
@login_required(login_url='/account/login/')
def input_home(request):
    
    products = InputProduct.objects.all()
    print(products)
    context = {
        "products": products
    }
    return render(request, 'input/index.html', context) 

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