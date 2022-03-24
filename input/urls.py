from django.urls import path

from . import views

app_name = "input"

urlpatterns = [
    path("", views.input_home, name="input_home"),
    path("products", views.Products.as_view(), name="product-list"),
    path("product/add", views.add_product, name="add-product"),
    path("product/edit/<int:pk>", views.edit_product, name="edit-product"),
    path("product/delete/<int:pk>", views.delete_product, name="delete-product"),
]
