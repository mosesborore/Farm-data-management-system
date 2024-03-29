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
    path(
        "inventory/<str:ref_code>/items/<int:pk>/edit",
        views.edit_inventory_item,
        name="edit-item",
    ),
    path(
        "inventory/<str:ref_code>/items/<int:pk>/delete",
        views.delete_inventory_item,
        name="delete-item",
    ),
    path("products", views.Products.as_view(), name="product-list"),
    path("product/add", views.add_product, name="add-product"),
    path("product/<int:pk>/edit", views.edit_product, name="edit-product"),
    path("product/<int:pk>/delete", views.delete_product, name="delete-product"),
    path("category/add", views.add_category, name="add-category"),
]
