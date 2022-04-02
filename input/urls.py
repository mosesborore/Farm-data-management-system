from django.urls import path

from . import views

app_name = "input"

urlpatterns = [
    path("inventory/", views.input_home, name="input_home"),
    path(
        "inventory/<str:ref_code>/delete",
        views.delete_inventory,
        name="delete-inventory",
    ),
    path(
        "inventory/<str:ref_code>",
        views.inventory_item_list,
        name="inventory-item-list",
    ),
    path("products", views.Products.as_view(), name="product-list"),
    path("product/add", views.add_product, name="add-product"),
    path("product/<int:pk>/edit", views.edit_product, name="edit-product"),
    path("product/<int:pk>/delete", views.delete_product, name="delete-product"),
]
