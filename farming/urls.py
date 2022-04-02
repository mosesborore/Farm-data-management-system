from django.urls import path

from . import views

app_name = "farming"

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/edit", views.edit_season, name="edit-season"),
    path("<int:pk>/delete", views.delete_season, name="delete-season"),
    path("crops", views.crop_list, name="crop-list"),
    path("crops/<int:pk>/edit", views.edit_crop, name="edit-crop"),
    path("crops/<int:pk>/delete", views.delete_crop, name="delete-crop"),
]
