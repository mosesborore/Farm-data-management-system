from django.urls import path

from . import views

app_name = "input"

urlpatterns = [
    path("", views.input_home, name="input_home"),
    path("products", views.Products.as_view(), name="product-list"),
    path("add-product", views.add_product, name="add-product"),
]
